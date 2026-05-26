from django.contrib import admin
from .models import Booking, Ticket


class TicketInline(admin.TabularInline):
    model = Ticket
    extra = 0
    readonly_fields = ("code", "created_at")
    fields = ("seat_number", "passenger_name", "passenger_document", "passenger_phone", "is_child", "price", "status", "code")


@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ("code", "trip", "contact_name", "contact_phone", "total_price", "status", "created_at")
    list_filter = ("status", "created_at")
    search_fields = ("code", "contact_name", "contact_phone", "contact_email")
    readonly_fields = ("code", "created_at", "updated_at")
    inlines = [TicketInline]
    autocomplete_fields = ("trip", "user")


@admin.register(Ticket)
class TicketAdmin(admin.ModelAdmin):
    list_display = ("code", "trip", "seat_number", "passenger_name", "price", "status")
    list_filter = ("status", "is_child")
    search_fields = ("code", "passenger_name", "passenger_document")
    readonly_fields = ("code", "created_at")
    autocomplete_fields = ("trip", "booking")
