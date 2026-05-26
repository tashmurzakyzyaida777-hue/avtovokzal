from django.http import JsonResponse
from django.shortcuts import get_object_or_404, render
from django.utils import timezone
from django.views.generic import DetailView, ListView

from .models import Trip


class TripListView(ListView):
    model = Trip
    template_name = "schedule/trip_list.html"
    context_object_name = "trips"
    paginate_by = 20

    def get_queryset(self):
        return (
            Trip.objects.filter(departure_at__gte=timezone.now())
            .select_related("route__origin__city", "route__destination__city", "bus")
            .order_by("departure_at")
        )


class TripDetailView(DetailView):
    model = Trip
    template_name = "schedule/trip_detail.html"
    context_object_name = "trip"

    def get_queryset(self):
        return super().get_queryset().select_related(
            "route__origin__city", "route__destination__city", "bus__bus_type", "driver"
        )

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        trip = self.object
        taken = trip.taken_seat_numbers
        per_row = trip.bus.seats_per_row or 4
        rows = []
        current_row = []
        for n in range(1, trip.seats_total + 1):
            current_row.append({"number": n, "taken": n in taken})
            if len(current_row) == per_row:
                rows.append(current_row)
                current_row = []
        if current_row:
            rows.append(current_row)
        ctx["seat_rows"] = rows
        ctx["seats_per_row"] = per_row
        ctx["aisle_after"] = per_row // 2
        ctx["taken_seats"] = list(taken)
        return ctx


def trip_seats_json(request, pk):
    trip = get_object_or_404(Trip, pk=pk)
    return JsonResponse({
        "trip_id": trip.pk,
        "taken": list(trip.taken_seat_numbers),
        "total": trip.seats_total,
        "available": trip.seats_available,
    })
