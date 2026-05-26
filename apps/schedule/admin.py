from django.contrib import admin
from modeltranslation.admin import TranslationAdmin

from .models import BusType, Bus, Driver, Trip


@admin.register(BusType)
class BusTypeAdmin(TranslationAdmin):
    list_display = ("name", "seats_default", "has_wifi", "has_ac", "has_toilet")
    search_fields = ("name",)


@admin.register(Bus)
class BusAdmin(admin.ModelAdmin):
    list_display = ("plate_number", "model_name", "bus_type", "seats", "is_active")
    list_filter = ("bus_type", "is_active")
    search_fields = ("plate_number", "model_name")
    autocomplete_fields = ("bus_type",)


@admin.register(Driver)
class DriverAdmin(admin.ModelAdmin):
    list_display = ("full_name", "phone", "license_number", "experience_years", "is_active")
    list_filter = ("is_active",)
    search_fields = ("full_name", "phone", "license_number")


@admin.register(Trip)
class TripAdmin(admin.ModelAdmin):
    list_display = ("route", "bus", "driver", "departure_at", "arrival_at", "base_price", "status", "seats_available")
    list_filter = ("status", "route", "departure_at")
    search_fields = ("route__code", "bus__plate_number")
    autocomplete_fields = ("route", "bus", "driver")
    date_hierarchy = "departure_at"
    readonly_fields = ("arrival_at",)
