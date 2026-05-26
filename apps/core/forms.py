from django import forms
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from apps.routes.models import City
from .models import ContactMessage


class TripSearchForm(forms.Form):
    origin = forms.ModelChoiceField(
        queryset=City.objects.filter(is_active=True),
        label=_("Откуда"),
        empty_label=_("Выберите город"),
        widget=forms.Select(attrs={"class": "form-select", "x-model": "origin"}),
    )
    destination = forms.ModelChoiceField(
        queryset=City.objects.filter(is_active=True),
        label=_("Куда"),
        empty_label=_("Выберите город"),
        widget=forms.Select(attrs={"class": "form-select", "x-model": "destination"}),
    )
    date = forms.DateField(
        label=_("Дата отправления"),
        initial=timezone.localdate,
        widget=forms.DateInput(attrs={"type": "date", "class": "form-input", "x-model": "date"}),
    )
    passengers = forms.IntegerField(
        label=_("Пассажиров"),
        min_value=1, max_value=8, initial=1,
        widget=forms.NumberInput(attrs={"class": "form-input", "min": 1, "max": 8, "x-model.number": "passengers"}),
    )

    def clean(self):
        cleaned = super().clean()
        if cleaned.get("origin") and cleaned.get("destination") and cleaned["origin"] == cleaned["destination"]:
            raise forms.ValidationError(_("Город отправления и прибытия не могут совпадать."))
        return cleaned


class ContactForm(forms.ModelForm):
    class Meta:
        model = ContactMessage
        fields = ("name", "email", "phone", "subject", "message")
        widgets = {
            "message": forms.Textarea(attrs={"rows": 5}),
        }
