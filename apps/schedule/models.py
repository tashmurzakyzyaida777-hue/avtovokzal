from datetime import timedelta
from django.conf import settings
from django.db import models
from django.urls import reverse
from django.utils.translation import gettext_lazy as _


class BusType(models.Model):
    name = models.CharField(_("Тип транспорта"), max_length=80)
    description = models.TextField(_("Описание"), blank=True)
    seats_default = models.PositiveSmallIntegerField(_("Кол-во мест по умолчанию"), default=20)
    has_wifi = models.BooleanField(_("Wi-Fi"), default=False)
    has_ac = models.BooleanField(_("Кондиционер"), default=True)
    has_toilet = models.BooleanField(_("Туалет"), default=False)

    class Meta:
        verbose_name = _("Тип транспорта")
        verbose_name_plural = _("Типы транспорта")
        ordering = ("name",)

    def __str__(self):
        return self.name


class Bus(models.Model):
    bus_type = models.ForeignKey(BusType, on_delete=models.PROTECT, related_name="buses", verbose_name=_("Тип"))
    plate_number = models.CharField(_("Гос. номер"), max_length=20, unique=True)
    model_name = models.CharField(_("Модель"), max_length=80)
    seats = models.PositiveSmallIntegerField(_("Количество мест"), default=20)
    rows = models.PositiveSmallIntegerField(_("Рядов"), default=5)
    seats_per_row = models.PositiveSmallIntegerField(_("Мест в ряду"), default=4)
    photo = models.ImageField(_("Фото"), upload_to="buses/", blank=True, null=True)
    is_active = models.BooleanField(_("Активен"), default=True)

    class Meta:
        verbose_name = _("Транспорт")
        verbose_name_plural = _("Транспорт")
        ordering = ("plate_number",)

    def __str__(self):
        return f"{self.model_name} • {self.plate_number}"


class Driver(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True, blank=True,
        related_name="driver_profile",
        verbose_name=_("Пользователь"),
    )
    full_name = models.CharField(_("ФИО"), max_length=150)
    phone = models.CharField(_("Телефон"), max_length=32)
    license_number = models.CharField(_("Удостоверение"), max_length=40, blank=True)
    experience_years = models.PositiveSmallIntegerField(_("Стаж, лет"), default=0)
    photo = models.ImageField(_("Фото"), upload_to="drivers/", blank=True, null=True)
    is_active = models.BooleanField(_("Активен"), default=True)

    class Meta:
        verbose_name = _("Водитель")
        verbose_name_plural = _("Водители")
        ordering = ("full_name",)

    def __str__(self):
        return self.full_name


class Trip(models.Model):
    class Status(models.TextChoices):
        SCHEDULED = "scheduled", _("По расписанию")
        BOARDING = "boarding", _("Идёт посадка")
        DEPARTED = "departed", _("В пути")
        ARRIVED = "arrived", _("Прибыл")
        CANCELED = "canceled", _("Отменён")

    route = models.ForeignKey(
        "routes.Route", on_delete=models.PROTECT, related_name="trips", verbose_name=_("Маршрут")
    )
    bus = models.ForeignKey(Bus, on_delete=models.PROTECT, related_name="trips", verbose_name=_("Транспорт"))
    driver = models.ForeignKey(
        Driver, on_delete=models.SET_NULL, null=True, blank=True, related_name="trips", verbose_name=_("Водитель")
    )
    departure_at = models.DateTimeField(_("Отправление"))
    arrival_at = models.DateTimeField(_("Прибытие"), blank=True, null=True)
    base_price = models.DecimalField(_("Цена билета, сом"), max_digits=10, decimal_places=2)
    status = models.CharField(_("Статус"), max_length=20, choices=Status.choices, default=Status.SCHEDULED)
    note = models.CharField(_("Примечание"), max_length=255, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = _("Рейс")
        verbose_name_plural = _("Рейсы")
        ordering = ("departure_at",)
        indexes = [
            models.Index(fields=["departure_at"]),
            models.Index(fields=["route", "departure_at"]),
        ]

    def __str__(self):
        return f"{self.route.code} • {self.departure_at:%Y-%m-%d %H:%M}"

    def save(self, *args, **kwargs):
        if not self.arrival_at and self.route_id:
            self.arrival_at = self.departure_at + timedelta(minutes=self.route.duration_minutes or 0)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse("schedule:trip_detail", kwargs={"pk": self.pk})

    @property
    def seats_total(self) -> int:
        return self.bus.seats

    @property
    def seats_taken(self) -> int:
        return self.tickets.filter(status__in=["booked", "paid"]).count()

    @property
    def seats_available(self) -> int:
        return max(0, self.seats_total - self.seats_taken)

    @property
    def is_full(self) -> bool:
        return self.seats_available == 0

    @property
    def taken_seat_numbers(self) -> set[int]:
        return set(self.tickets.filter(status__in=["booked", "paid"]).values_list("seat_number", flat=True))
