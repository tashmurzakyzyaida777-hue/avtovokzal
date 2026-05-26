from django.contrib import admin
from modeltranslation.admin import TranslationAdmin

from .models import HeroBanner, NewsArticle, FAQ, ContactMessage


@admin.register(HeroBanner)
class HeroBannerAdmin(TranslationAdmin):
    list_display = ("title", "order", "is_active")
    list_editable = ("order", "is_active")


@admin.register(NewsArticle)
class NewsArticleAdmin(TranslationAdmin):
    list_display = ("title", "published_at", "is_published")
    list_filter = ("is_published",)
    search_fields = ("title", "body")
    prepopulated_fields = {"slug": ("title",)}


@admin.register(FAQ)
class FAQAdmin(TranslationAdmin):
    list_display = ("question", "order", "is_active")
    list_editable = ("order", "is_active")


@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ("name", "email", "phone", "subject", "is_processed", "created_at")
    list_filter = ("is_processed", "created_at")
    search_fields = ("name", "email", "phone", "subject")
    readonly_fields = ("created_at",)
