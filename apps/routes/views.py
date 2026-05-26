from django.db.models import Count
from django.views.generic import DetailView, ListView

from .models import Route, Station, City


class RouteListView(ListView):
    model = Route
    template_name = "routes/route_list.html"
    context_object_name = "routes"
    paginate_by = 12

    def get_queryset(self):
        qs = (
            Route.objects.filter(is_active=True)
            .select_related("origin__city", "destination__city")
            .annotate(trip_count=Count("trips"))
        )
        q = self.request.GET.get("q", "").strip()
        if q:
            qs = qs.filter(origin__city__name__icontains=q) | qs.filter(destination__city__name__icontains=q)
        return qs


class RouteDetailView(DetailView):
    model = Route
    template_name = "routes/route_detail.html"
    context_object_name = "route"

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["upcoming_trips"] = self.object.trips.filter(
            status__in=["scheduled", "boarding"],
        ).select_related("bus", "driver").order_by("departure_at")[:20]
        ctx["stops"] = self.object.stops.select_related("station__city").order_by("order")
        return ctx


class StationListView(ListView):
    model = Station
    template_name = "routes/station_list.html"
    context_object_name = "stations"

    def get_queryset(self):
        return Station.objects.filter(is_active=True).select_related("city")
