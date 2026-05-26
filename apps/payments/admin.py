from django.contrib import admin
from .models import Payment


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ("transaction_id", "booking", "method", "amount", "status", "created_at")
    list_filter = ("method", "status", "created_at")
    search_fields = ("transaction_id", "booking__code", "payer_name")
    readonly_fields = ("transaction_id", "created_at", "updated_at", "raw_response")
    autocomplete_fields = ("booking",)
