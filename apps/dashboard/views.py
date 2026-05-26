from decimal import Decimal

from django.contrib.auth.decorators import login_required, user_passes_test
from django.db.models import Count, Sum
from django.shortcuts import render
from django.utils import timezone
from django.utils.decorators import method_decorator

from apps.booking.models import Booking, Ticket
from apps.payments.models import Payment
from apps.routes.models import City, Route
from apps.schedule.models import Trip


def staff_required(view):
    return login_required(user_passes_test(lambda u: u.is_authenticated and (u.is_staff or getattr(u, "is_staff_role", False)))(view))


@staff_required
def index(request):
    today = timezone.localdate()
    bookings_today = Booking.objects.filter(created_at__date=today)
    revenue_today = Payment.objects.filter(status=Payment.Status.SUCCESS, created_at__date=today).aggregate(s=Sum("amount"))["s"] or Decimal("0")
    upcoming_trips = (
        Trip.objects.filter(departure_at__gte=timezone.now(), status__in=[Trip.Status.SCHEDULED, Trip.Status.BOARDING])
        .select_related("route__origin__city", "route__destination__city", "bus")
        .order_by("departure_at")[:10]
    )

    stats = {
        "bookings_total": Booking.objects.count(),
        "bookings_today": bookings_today.count(),
        "tickets_total": Ticket.objects.count(),
        "revenue_today": revenue_today,
        "revenue_total": Payment.objects.filter(status=Payment.Status.SUCCESS).aggregate(s=Sum("amount"))["s"] or Decimal("0"),
        "cities": City.objects.filter(is_active=True).count(),
        "routes": Route.objects.filter(is_active=True).count(),
        "trips_upcoming": Trip.objects.filter(departure_at__gte=timezone.now()).count(),
    }

    top_routes = (
        Route.objects.annotate(c=Count("trips__bookings"))
        .select_related("origin__city", "destination__city")
        .order_by("-c")[:6]
    )

    return render(request, "dashboard/index.html", {
        "stats": stats,
        "upcoming_trips": upcoming_trips,
        "top_routes": top_routes,
        "recent_bookings": Booking.objects.select_related("trip__route__origin__city", "trip__route__destination__city").order_by("-created_at")[:8],
    })


@staff_required
def bookings(request):
    qs = Booking.objects.select_related(
        "trip__route__origin__city", "trip__route__destination__city", "user"
    ).order_by("-created_at")
    status = request.GET.get("status")
    if status:
        qs = qs.filter(status=status)
    q = request.GET.get("q", "").strip()
    if q:
        qs = qs.filter(code__icontains=q) | qs.filter(contact_phone__icontains=q) | qs.filter(contact_name__icontains=q)
    return render(request, "dashboard/bookings.html", {
        "bookings": qs[:100],
        "statuses": Booking.Status.choices,
        "current_status": status,
        "q": q,
    })


@staff_required
def trips(request):
    qs = (
        Trip.objects.select_related("route__origin__city", "route__destination__city", "bus", "driver")
        .order_by("departure_at")
    )
    when = request.GET.get("when", "upcoming")
    if when == "upcoming":
        qs = qs.filter(departure_at__gte=timezone.now())
    elif when == "today":
        qs = qs.filter(departure_at__date=timezone.localdate())
    elif when == "past":
        qs = qs.filter(departure_at__lt=timezone.now())
    return render(request, "dashboard/trips.html", {"trips": qs[:200], "when": when})
