from django import forms
from django.forms import formset_factory
from django.utils.translation import gettext_lazy as _


class PassengerForm(forms.Form):
    seat_number = forms.IntegerField(min_value=1, widget=forms.HiddenInput())
    passenger_name = forms.CharField(label=_("ФИО"), max_length=150)
    passenger_document = forms.CharField(label=_("Паспорт/ID"), max_length=64, required=False)
    passenger_phone = forms.CharField(label=_("Телефон"), max_length=32, required=False)
    is_child = forms.BooleanField(label=_("Детский билет"), required=False)


PassengerFormSet = formset_factory(PassengerForm, extra=0, min_num=1, validate_min=True)


class BookingContactForm(forms.Form):
    contact_name = forms.CharField(label=_("Контактное лицо"), max_length=150)
    contact_phone = forms.CharField(label=_("Телефон"), max_length=32)
    contact_email = forms.EmailField(label=_("Email"), required=False)
    note = forms.CharField(label=_("Примечание"), max_length=255, required=False, widget=forms.Textarea(attrs={"rows": 2}))
