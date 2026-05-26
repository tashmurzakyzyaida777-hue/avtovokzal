from django.contrib import admin
from modeltranslation.admin import TranslationAdmin

from .models import City, Station, Route, RouteStop


class StationInline(admin.TabularInline):
    model = Station
    extra = 0
    fields = ("name", "address", "phone", "is_active")


@admin.register(City)
class CityAdmin(TranslationAdmin):
    list_display = ("name", "region", "country", "is_active")
    list_filter = ("country", "is_active")
    search_fields = ("name", "region")
    prepopulated_fields = {"slug": ("name",)}
    inlines = [StationInline]


@admin.register(Station)
class StationAdmin(TranslationAdmin):
    list_display = ("name", "city", "phone", "is_active")
    list_filter = ("city__country", "is_active")
    search_fields = ("name", "city__name", "address")
    autocomplete_fields = ("city",)


class RouteStopInline(admin.TabularInline):
    model = RouteStop
    extra = 0
    autocomplete_fields = ("station",)


@admin.register(Route)
class RouteAdmin(TranslationAdmin):
    list_display = ("code", "origin", "destination", "distance_km", "duration_display", "is_active")
    list_filter = ("is_active", "origin__city", "destination__city")
    search_fields = ("code", "origin__city__name", "destination__city__name")
    autocomplete_fields = ("origin", "destination")
    inlines = [RouteStopInline]
