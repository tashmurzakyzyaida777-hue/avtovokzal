"""URL configuration for avtovokzal project."""
from django.conf import settings
from django.conf.urls.i18n import i18n_patterns
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("admin/", admin.site.urls),
    path("i18n/", include("django.conf.urls.i18n")),
]

urlpatterns += i18n_patterns(
    path("", include("apps.core.urls", namespace="core")),
    path("accounts/", include("apps.accounts.urls", namespace="accounts")),
    path("routes/", include("apps.routes.urls", namespace="routes")),
    path("schedule/", include("apps.schedule.urls", namespace="schedule")),
    path("booking/", include("apps.booking.urls", namespace="booking")),
    path("payments/", include("apps.payments.urls", namespace="payments")),
    path("dashboard/", include("apps.dashboard.urls", namespace="dashboard")),
    prefix_default_language=False,
)

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
