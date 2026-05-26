import secrets
from decimal import Decimal
from django.conf import settings
from django.db import models
from django.urls import reverse
from django.utils import timezone
from django.utils.translation import gettext_lazy as _


def _gen_code(prefix: str, length: int = 8) -> str:
    return f"{prefix}-{secrets.token_hex(length // 2).upper()}"


class Booking(models.Model):
    class Status(models.TextChoices):
        PENDING = "pending", _("Ожидает оплаты")
        PAID = "paid", _("Оплачена")
        CANCELED = "canceled", _("Отменена")
        REFUNDED = "refunded", _("Возврат")
        EXPIRED = "expired", _("Истекла")

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True, blank=True,
        related_name="bookings",
        verbose_name=_("Пользователь"),
    )
    trip = models.ForeignKey("schedule.Trip", on_delete=models.PROTECT, related_name="bookings", verbose_name=_("Рейс"))
    code = models.CharField(_("Код брони"), max_length=24, unique=True, blank=True)
    contact_name = models.CharField(_("Имя контакта"), max_length=150)
    contact_phone = models.CharField(_("Телефон"), max_length=32)
    contact_email = models.EmailField(_("Email"), blank=True)
    total_price = models.DecimalField(_("Итого"), max_digits=10, decimal_places=2, default=Decimal("0"))
    status = models.CharField(_("Статус"), max_length=12, choices=Status.choices, default=Status.PENDING)
    note = models.CharField(_("Примечание"), max_length=255, blank=True)
    created_at = models.DateTimeField(_("Создана"), auto_now_add=True)
    updated_at = models.DateTimeField(_("Обновлена"), auto_now=True)
    expires_at = models.DateTimeField(_("Истекает"), null=True, blank=True)

    class Meta:
        verbose_name = _("Бронирование")
        verbose_name_plural = _("Бронирования")
        ordering = ("-created_at",)
        indexes = [models.Index(fields=["status", "expires_at"])]

    def __str__(self):
        return self.code or f"Booking #{self.pk}"

    def save(self, *args, **kwargs):
        if not self.code:
            self.code = _gen_code("BK")
        if not self.expires_at:
            self.expires_at = timezone.now() + timezone.timedelta(minutes=20)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse("booking:detail", kwargs={"code": self.code})

    def recalc_total(self):
        self.total_price = sum((t.price for t in self.tickets.all()), Decimal("0"))
        return self.total_price

    @property
    def is_expired(self) -> bool:
        return self.status == self.Status.PENDING and self.expires_at and self.expires_at < timezone.now()


class Ticket(models.Model):
    class Status(models.TextChoices):
        BOOKED = "booked", _("Забронирован")
        PAID = "paid", _("Оплачен")
        CANCELED = "canceled", _("Отменён")
        USED = "used", _("Использован")

    booking = models.ForeignKey(Booking, on_delete=models.CASCADE, related_name="tickets")
    trip = models.ForeignKey("schedule.Trip", on_delete=models.PROTECT, related_name="tickets")
    seat_number = models.PositiveSmallIntegerField(_("Место"))
    passenger_name = models.CharField(_("ФИО пассажира"), max_length=150)
    passenger_document = models.CharField(_("Документ"), max_length=64, blank=True)
    passenger_phone = models.CharField(_("Телефон"), max_length=32, blank=True)
    is_child = models.BooleanField(_("Ребёнок"), default=False)
    price = models.DecimalField(_("Цена"), max_digits=10, decimal_places=2)
    status = models.CharField(_("Статус"), max_length=12, choices=Status.choices, default=Status.BOOKED)
    code = models.CharField(_("Код билета"), max_length=24, unique=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = _("Билет")
        verbose_name_plural = _("Билеты")
        ordering = ("trip__departure_at", "seat_number")
        unique_together = (("trip", "seat_number"),)

    def __str__(self):
        return f"{self.code} • место {self.seat_number}"

    def save(self, *args, **kwargs):
        if not self.code:
            self.code = _gen_code("TK")
        super().save(*args, **kwargs)
