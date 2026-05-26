import secrets
from django.db import models
from django.utils.translation import gettext_lazy as _


class Payment(models.Model):
    class Method(models.TextChoices):
        CARD = "card", _("Банковская карта")
        ELCART = "elcart", _("Элкарт")
        MBANK = "mbank", _("MBank")
        OPAY = "opay", _("O!Деньги")
        CASH = "cash", _("Наличные в кассе")

    class Status(models.TextChoices):
        PENDING = "pending", _("Ожидает")
        SUCCESS = "success", _("Успешно")
        FAILED = "failed", _("Ошибка")
        REFUNDED = "refunded", _("Возврат")

    booking = models.ForeignKey(
        "booking.Booking", on_delete=models.CASCADE, related_name="payments", verbose_name=_("Бронь")
    )
    method = models.CharField(_("Метод"), max_length=20, choices=Method.choices)
    amount = models.DecimalField(_("Сумма"), max_digits=10, decimal_places=2)
    status = models.CharField(_("Статус"), max_length=12, choices=Status.choices, default=Status.PENDING)
    transaction_id = models.CharField(_("ID транзакции"), max_length=64, unique=True, blank=True)
    payer_name = models.CharField(_("Плательщик"), max_length=150, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    raw_response = models.JSONField(_("Ответ"), blank=True, null=True)

    class Meta:
        verbose_name = _("Платёж")
        verbose_name_plural = _("Платежи")
        ordering = ("-created_at",)

    def __str__(self):
        return f"{self.transaction_id} ({self.get_status_display()})"

    def save(self, *args, **kwargs):
        if not self.transaction_id:
            self.transaction_id = f"TX-{secrets.token_hex(8).upper()}"
        super().save(*args, **kwargs)
