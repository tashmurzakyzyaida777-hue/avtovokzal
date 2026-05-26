from decimal import Decimal

from django.contrib import messages
from django.db import transaction
from django.http import HttpResponseBadRequest, JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from django.views.decorators.http import require_POST

from apps.schedule.models import Trip
from .forms import BookingContactForm, PassengerFormSet
from .models import Booking, Ticket


CHILD_DISCOUNT = Decimal("0.5")


def _parse_seats(raw: str) -> list[int]:
    if not raw:
        return []
    try:
        seats = sorted({int(s) for s in raw.split(",") if s.strip()})
    except ValueError:
        return []
    return seats


def select_seats(request, trip_id):
    """Step 1: select seats — usually triggered from trip detail; we show a confirmation page with picked seats."""
    trip = get_object_or_404(Trip, pk=trip_id)
    raw = request.POST.get("seats") if request.method == "POST" else request.GET.get("seats")
    seats = _parse_seats(raw)
    if not seats:
        messages.warning(request, _("Выберите хотя бы одно место."))
        return redirect("schedule:trip_detail", pk=trip.pk)
    taken = trip.taken_seat_numbers
    conflicts = [s for s in seats if s in taken or s < 1 or s > trip.seats_total]
    if conflicts:
        messages.error(request, _("Некоторые места уже заняты или некорректны: %(seats)s") % {"seats": ", ".join(map(str, conflicts))})
        return redirect("schedule:trip_detail", pk=trip.pk)

    request.session["booking"] = {"trip_id": trip.pk, "seats": seats}
    return redirect("booking:passengers", trip_id=trip.pk)


def passengers(request, trip_id):
    """Step 2: enter passenger details for each selected seat."""
    trip = get_object_or_404(Trip, pk=trip_id)
    data = request.session.get("booking")
    if not data or data.get("trip_id") != trip.pk or not data.get("seats"):
        messages.warning(request, _("Сначала выберите места."))
        return redirect("schedule:trip_detail", pk=trip.pk)
    seats = data["seats"]

    initial_passengers = [{"seat_number": s} for s in seats]

    if request.method == "POST":
        pf = PassengerFormSet(request.POST, initial=initial_passengers, prefix="p")
        cf = BookingContactForm(request.POST)
        if pf.is_valid() and cf.is_valid():
            passengers_data = []
            for form in pf:
                if form.cleaned_data:
                    passengers_data.append(form.cleaned_data)
            request.session["booking"]["passengers"] = passengers_data
            request.session["booking"]["contact"] = cf.cleaned_data
            request.session.modified = True
            return redirect("booking:confirm", trip_id=trip.pk)
    else:
        pf = PassengerFormSet(initial=initial_passengers, prefix="p")
        cf_initial = {}
        if request.user.is_authenticated:
            cf_initial = {
                "contact_name": request.user.full_name,
                "contact_phone": request.user.phone,
                "contact_email": request.user.email,
            }
        cf = BookingContactForm(initial=cf_initial)

    return render(request, "booking/passengers.html", {
        "trip": trip,
        "seats": seats,
        "passenger_formset": pf,
        "contact_form": cf,
        "base_price": trip.base_price,
        "estimated_total": trip.base_price * len(seats),
    })


def confirm(request, trip_id):
    """Step 3: review and confirm — creates booking + tickets, redirects to payment."""
    trip = get_object_or_404(Trip, pk=trip_id)
    data = request.session.get("booking")
    if not data or data.get("trip_id") != trip.pk or not data.get("passengers"):
        messages.warning(request, _("Сессия бронирования истекла."))
        return redirect("schedule:trip_detail", pk=trip.pk)

    passengers_data = data["passengers"]
    contact = data["contact"]
    seats = data["seats"]

    # Calculate total
    total = Decimal("0")
    line_items = []
    for p in passengers_data:
        price = trip.base_price * (CHILD_DISCOUNT if p.get("is_child") else Decimal("1"))
        line_items.append({"seat": p["seat_number"], "name": p["passenger_name"], "is_child": p.get("is_child", False), "price": price})
        total += price

    if request.method == "POST":
        # re-check availability
        taken = trip.taken_seat_numbers
        conflicts = [s for s in seats if s in taken]
        if conflicts:
            messages.error(request, _("Некоторые места были забронированы только что: %(seats)s") % {"seats": ", ".join(map(str, conflicts))})
            return redirect("schedule:trip_detail", pk=trip.pk)

        with transaction.atomic():
            booking = Booking.objects.create(
                user=request.user if request.user.is_authenticated else None,
                trip=trip,
                contact_name=contact["contact_name"],
                contact_phone=contact["contact_phone"],
                contact_email=contact.get("contact_email", ""),
                note=contact.get("note", ""),
            )
            for item in line_items:
                p = next(p for p in passengers_data if p["seat_number"] == item["seat"])
                Ticket.objects.create(
                    booking=booking,
                    trip=trip,
                    seat_number=item["seat"],
                    passenger_name=p["passenger_name"],
                    passenger_document=p.get("passenger_document", ""),
                    passenger_phone=p.get("passenger_phone", ""),
                    is_child=p.get("is_child", False),
                    price=item["price"],
                )
            booking.recalc_total()
            booking.save(update_fields=["total_price"])

        request.session.pop("booking", None)
        return redirect("payments:checkout", code=booking.code)

    return render(request, "booking/confirm.html", {
        "trip": trip,
        "seats": seats,
        "line_items": line_items,
        "contact": contact,
        "total": total,
    })


def detail(request, code):
    booking = get_object_or_404(
        Booking.objects.select_related(
            "trip__route__origin__city", "trip__route__destination__city", "trip__bus", "trip__driver"
        ).prefetch_related("tickets"),
        code=code,
    )
    if request.user.is_authenticated and booking.user_id and booking.user_id != request.user.id and not request.user.is_staff_role:
        return HttpResponseBadRequest("Нет доступа")
    return render(request, "booking/detail.html", {"booking": booking})


def ticket(request, code):
    """Single ticket page with QR for boarding check."""
    t = get_object_or_404(Ticket.objects.select_related("booking", "trip__route__origin__city", "trip__route__destination__city"), code=code)
    return render(request, "booking/ticket.html", {"ticket": t})


@require_POST
def cancel(request, code):
    booking = get_object_or_404(Booking, code=code)
    if booking.status not in [Booking.Status.PENDING, Booking.Status.PAID]:
        messages.warning(request, _("Эту бронь нельзя отменить."))
        return redirect("booking:detail", code=code)
    booking.status = Booking.Status.CANCELED
    booking.tickets.update(status=Ticket.Status.CANCELED)
    booking.save(update_fields=["status", "updated_at"])
    messages.success(request, _("Бронирование отменено."))
    return redirect("booking:detail", code=code)
