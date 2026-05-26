from django.db import models
from django.utils.translation import gettext_lazy as _


class HeroBanner(models.Model):
    title = models.CharField(_("Заголовок"), max_length=200)
    subtitle = models.CharField(_("Подзаголовок"), max_length=300, blank=True)
    image = models.ImageField(_("Изображение"), upload_to="banners/", blank=True, null=True)
    cta_text = models.CharField(_("Текст кнопки"), max_length=80, blank=True)
    cta_url = models.CharField(_("Ссылка"), max_length=255, blank=True)
    order = models.PositiveSmallIntegerField(_("Порядок"), default=0)
    is_active = models.BooleanField(_("Активен"), default=True)

    class Meta:
        verbose_name = _("Баннер")
        verbose_name_plural = _("Баннеры")
        ordering = ("order",)

    def __str__(self):
        return self.title


class NewsArticle(models.Model):
    title = models.CharField(_("Заголовок"), max_length=200)
    slug = models.SlugField(_("Слаг"), max_length=220, unique=True)
    summary = models.CharField(_("Краткое описание"), max_length=300, blank=True)
    body = models.TextField(_("Текст"))
    cover = models.ImageField(_("Обложка"), upload_to="news/", blank=True, null=True)
    published_at = models.DateTimeField(_("Опубликована"), auto_now_add=True)
    is_published = models.BooleanField(_("Опубликована"), default=True)

    class Meta:
        verbose_name = _("Новость")
        verbose_name_plural = _("Новости")
        ordering = ("-published_at",)

    def __str__(self):
        return self.title


class FAQ(models.Model):
    question = models.CharField(_("Вопрос"), max_length=255)
    answer = models.TextField(_("Ответ"))
    order = models.PositiveSmallIntegerField(_("Порядок"), default=0)
    is_active = models.BooleanField(_("Активен"), default=True)

    class Meta:
        verbose_name = _("FAQ")
        verbose_name_plural = _("Часто задаваемые вопросы")
        ordering = ("order",)

    def __str__(self):
        return self.question


class ContactMessage(models.Model):
    name = models.CharField(_("Имя"), max_length=120)
    email = models.EmailField(_("Email"))
    phone = models.CharField(_("Телефон"), max_length=32, blank=True)
    subject = models.CharField(_("Тема"), max_length=200, blank=True)
    message = models.TextField(_("Сообщение"))
    created_at = models.DateTimeField(auto_now_add=True)
    is_processed = models.BooleanField(_("Обработано"), default=False)

    class Meta:
        verbose_name = _("Обращение")
        verbose_name_plural = _("Обращения")
        ordering = ("-created_at",)

    def __str__(self):
        return f"{self.name} • {self.created_at:%Y-%m-%d}"
