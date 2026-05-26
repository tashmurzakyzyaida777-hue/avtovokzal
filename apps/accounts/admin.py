from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as DjangoUserAdmin
from .models import User


@admin.register(User)
class UserAdmin(DjangoUserAdmin):
    list_display = ("username", "email", "full_name", "role", "phone", "is_staff", "is_active", "date_joined")
    list_filter = ("role", "is_staff", "is_active", "email_verified")
    search_fields = ("username", "email", "first_name", "last_name", "phone", "passport_number")
    fieldsets = DjangoUserAdmin.fieldsets + (
        ("Дополнительно", {"fields": ("phone", "role", "avatar", "birth_date", "passport_number", "email_verified")}),
    )
    add_fieldsets = DjangoUserAdmin.add_fieldsets + (
        ("Дополнительно", {"fields": ("email", "phone", "role")}),
    )
