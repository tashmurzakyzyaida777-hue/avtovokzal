from django.db import models
from django.urls import reverse
from django.utils.text import slugify
from django.utils.translation import gettext_lazy as _


class City(models.Model):
    name = models.CharField(_("Город"), max_length=100)
    slug = models.SlugField(_("Слаг"), max_length=110, unique=True, blank=True)
    region = models.CharField(_("Регион/Область"), max_length=100, blank=True)
    country = models.CharField(_("Страна"), max_length=80, default="Кыргызстан")
    latitude = models.DecimalField(_("Широта"), max_digits=9, decimal_places=6, null=True, blank=True)
    longitude = models.DecimalField(_("Долгота"), max_digits=9, decimal_places=6, null=True, blank=True)
    is_active = models.BooleanField(_("Активен"), default=True)

    class Meta:
        verbose_name = _("Город")
        verbose_name_plural = _("Города")
        ordering = ("name",)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name, allow_unicode=True) or self.name.lower().replace(" ", "-")
        super().save(*args, **kwargs)


class Station(models.Model):
    city = models.ForeignKey(City, on_delete=models.CASCADE, related_name="stations", verbose_name=_("Город"))
    name = models.CharField(_("Название автовокзала"), max_length=150)
    address = models.CharField(_("Адрес"), max_length=255, blank=True)
    phone = models.CharField(_("Телефон"), max_length=32, blank=True)
    latitude = models.DecimalField(_("Широта"), max_digits=9, decimal_places=6, null=True, blank=True)
    longitude = models.DecimalField(_("Долгота"), max_digits=9, decimal_places=6, null=True, blank=True)
    is_active = models.BooleanField(_("Активен"), default=True)

    class Meta:
        verbose_name = _("Автовокзал")
        verbose_name_plural = _("Автовокзалы")
        ordering = ("city__name", "name")

    def __str__(self):
        return f"{self.name} ({self.city.name})"


class Route(models.Model):
    origin = models.ForeignKey(Station, on_delete=models.PROTECT, related_name="routes_out", verbose_name=_("Откуда"))
    destination = models.ForeignKey(Station, on_delete=models.PROTECT, related_name="routes_in", verbose_name=_("Куда"))
    code = models.CharField(_("Код маршрута"), max_length=20, unique=True)
    distance_km = models.PositiveIntegerField(_("Расстояние, км"), default=0)
    duration_minutes = models.PositiveIntegerField(_("Длительность, мин"), default=0)
    description = models.TextField(_("Описание"), blank=True)
    is_active = models.BooleanField(_("Активен"), default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = _("Маршрут")
        verbose_name_plural = _("Маршруты")
        ordering = ("origin__city__name", "destination__city__name")
        constraints = [
            models.CheckConstraint(check=~models.Q(origin=models.F("destination")), name="route_origin_ne_destination"),
        ]

    def __str__(self):
        return f"{self.origin.city.name} → {self.destination.city.name} ({self.code})"

    def get_absolute_url(self):
        return reverse("routes:detail", kwargs={"pk": self.pk})

    @property
    def duration_display(self):
        h, m = divmod(self.duration_minutes, 60)
        return f"{h} ч {m:02d} мин" if h else f"{m} мин"


class RouteStop(models.Model):
    route = models.ForeignKey(Route, on_delete=models.CASCADE, related_name="stops")
    station = models.ForeignKey(Station, on_delete=models.PROTECT, related_name="route_stops")
    order = models.PositiveSmallIntegerField(_("Порядок"))
    offset_minutes = models.PositiveIntegerField(_("Смещение от старта, мин"), default=0)
    stop_minutes = models.PositiveSmallIntegerField(_("Стоянка, мин"), default=5)

    class Meta:
        verbose_name = _("Промежуточная остановка")
        verbose_name_plural = _("Промежуточные остановки")
        ordering = ("route", "order")
        unique_together = (("route", "order"), ("route", "station"))

    def __str__(self):
        return f"{self.route.code}: #{self.order} {self.station.name}"
