from django.contrib import messages
from django.db import transaction
from django.shortcuts import get_object_or_404, redirect, render
from django.utils.translation import gettext_lazy as _

from apps.booking.models import Booking, Ticket
from .models import Payment


def checkout(request, code):
    booking = get_object_or_404(
        Booking.objects.select_related("trip__route__origin__city", "trip__route__destination__city").prefetch_related("tickets"),
        code=code,
    )
    if booking.is_expired:
        booking.status = Booking.Status.EXPIRED
        booking.save(update_fields=["status"])
    if booking.status == Booking.Status.PAID:
        return redirect("booking:detail", code=booking.code)

    if request.method == "POST":
        method = request.POST.get("method")
        if method not in dict(Payment.Method.choices):
            messages.error(request, _("Выберите способ оплаты."))
            return redirect("payments:checkout", code=booking.code)

        with transaction.atomic():
            payment = Payment.objects.create(
                booking=booking,
                method=method,
                amount=booking.total_price,
                payer_name=booking.contact_name,
                status=Payment.Status.SUCCESS,  # demo — always success
            )
            booking.status = Booking.Status.PAID
            booking.save(update_fields=["status", "updated_at"])
            booking.tickets.update(status=Ticket.Status.PAID)

        messages.success(request, _("Оплата принята. Билеты доступны в личном кабинете."))
        return redirect("payments:success", code=booking.code)

    return render(request, "payments/checkout.html", {
        "booking": booking,
        "methods": Payment.Method.choices,
    })


def success(request, code):
    booking = get_object_or_404(
        Booking.objects.select_related("trip__route__origin__city", "trip__route__destination__city").prefetch_related("tickets"),
        code=code,
    )
    return render(request, "payments/success.html", {"booking": booking})
