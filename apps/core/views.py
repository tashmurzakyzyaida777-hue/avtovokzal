from django.contrib import messages
from django.db.models import Count, Q
from django.shortcuts import redirect, render
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from django.views.generic import DetailView, ListView, TemplateView

from apps.routes.models import City, Route
from apps.schedule.models import Trip
from .forms import ContactForm, TripSearchForm
from .models import FAQ, HeroBanner, NewsArticle


class HomeView(TemplateView):
    template_name = "core/home.html"

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["search_form"] = TripSearchForm()
        ctx["banners"] = HeroBanner.objects.filter(is_active=True)
        ctx["news"] = NewsArticle.objects.filter(is_published=True)[:3]
        ctx["faqs"] = FAQ.objects.filter(is_active=True)[:6]
        ctx["popular_routes"] = (
            Route.objects.filter(is_active=True)
            .select_related("origin__city", "destination__city")
            .annotate(trip_count=Count("trips"))
            .order_by("-trip_count")[:6]
        )
        ctx["cities"] = City.objects.filter(is_active=True)
        ctx["stats"] = {
            "cities": City.objects.filter(is_active=True).count(),
            "routes": Route.objects.filter(is_active=True).count(),
            "trips_today": Trip.objects.filter(
                departure_at__date=timezone.localdate(),
                status__in=[Trip.Status.SCHEDULED, Trip.Status.BOARDING],
            ).count(),
        }
        return ctx


class AboutView(TemplateView):
    template_name = "core/about.html"


class FAQView(ListView):
    model = FAQ
    template_name = "core/faq.html"
    context_object_name = "faqs"

    def get_queryset(self):
        return FAQ.objects.filter(is_active=True)


class NewsListView(ListView):
    model = NewsArticle
    template_name = "core/news_list.html"
    context_object_name = "news_list"
    paginate_by = 9

    def get_queryset(self):
        return NewsArticle.objects.filter(is_published=True)


class NewsDetailView(DetailView):
    model = NewsArticle
    template_name = "core/news_detail.html"
    context_object_name = "article"
    slug_url_kwarg = "slug"


def contact(request):
    if request.method == "POST":
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, _("Спасибо! Ваше сообщение отправлено."))
            return redirect("core:contact")
    else:
        form = ContactForm()
    return render(request, "core/contact.html", {"form": form})


def search(request):
    """Trip search results page. Accepts GET params from home search form."""
    form = TripSearchForm(request.GET or None)
    trips = Trip.objects.none()
    if request.GET and form.is_valid():
        origin = form.cleaned_data["origin"]
        destination = form.cleaned_data["destination"]
        date = form.cleaned_data["date"]
        passengers = form.cleaned_data["passengers"]
        trips = (
            Trip.objects.filter(
                route__origin__city=origin,
                route__destination__city=destination,
                departure_at__date=date,
                status__in=[Trip.Status.SCHEDULED, Trip.Status.BOARDING],
            )
            .select_related("route__origin__city", "route__destination__city", "bus", "bus__bus_type", "driver")
            .order_by("departure_at")
        )
        # If asking for HTMX partial — return only results fragment
        if request.headers.get("HX-Request"):
            return render(request, "core/_search_results.html", {
                "trips": trips, "passengers": passengers, "date": date,
            })
    return render(request, "core/search.html", {
        "form": form,
        "trips": trips,
        "submitted": bool(request.GET),
    })


def city_autocomplete(request):
    """HTMX autocomplete for cities."""
    q = request.GET.get("q", "").strip()
    field = request.GET.get("field", "origin")
    cities = City.objects.filter(is_active=True)
    if q:
        cities = cities.filter(Q(name__icontains=q) | Q(name_ru__icontains=q) | Q(name_en__icontains=q))
    cities = cities[:10]
    return render(request, "core/_city_suggestions.html", {"cities": cities, "field": field})
