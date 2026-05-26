from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _


class User(AbstractUser):
    class Role(models.TextChoices):
        CUSTOMER = "customer", _("Клиент")
        CASHIER = "cashier", _("Кассир")
        DISPATCHER = "dispatcher", _("Диспетчер")
        DRIVER = "driver", _("Водитель")
        ADMIN = "admin", _("Администратор")

    phone = models.CharField(_("Телефон"), max_length=20, blank=True)
    role = models.CharField(_("Роль"), max_length=20, choices=Role.choices, default=Role.CUSTOMER)
    avatar = models.ImageField(_("Аватар"), upload_to="avatars/", blank=True, null=True)
    birth_date = models.DateField(_("Дата рождения"), blank=True, null=True)
    passport_number = models.CharField(_("Паспорт"), max_length=32, blank=True)
    email_verified = models.BooleanField(_("Email подтверждён"), default=False)
    created_at = models.DateTimeField(_("Создан"), auto_now_add=True)

    class Meta:
        verbose_name = _("Пользователь")
        verbose_name_plural = _("Пользователи")
        ordering = ("-date_joined",)

    def __str__(self) -> str:
        return self.get_full_name() or self.username

    @property
    def is_staff_role(self) -> bool:
        return self.role in {self.Role.CASHIER, self.Role.DISPATCHER, self.Role.ADMIN}

    @property
    def full_name(self) -> str:
        return self.get_full_name() or self.username
