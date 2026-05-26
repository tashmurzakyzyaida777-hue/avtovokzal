from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django.utils.translation import gettext_lazy as _

User = get_user_model()


class SignUpForm(UserCreationForm):
    first_name = forms.CharField(label=_("Имя"), max_length=80)
    last_name = forms.CharField(label=_("Фамилия"), max_length=80)
    email = forms.EmailField(label=_("Email"))
    phone = forms.CharField(label=_("Телефон"), max_length=20)

    class Meta:
        model = User
        fields = ("username", "first_name", "last_name", "email", "phone", "password1", "password2")

    def save(self, commit=True):
        user = super().save(commit=False)
        user.first_name = self.cleaned_data["first_name"]
        user.last_name = self.cleaned_data["last_name"]
        user.email = self.cleaned_data["email"]
        user.phone = self.cleaned_data["phone"]
        if commit:
            user.save()
        return user


class ProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ("first_name", "last_name", "email", "phone", "avatar", "birth_date", "passport_number")
        widgets = {
            "birth_date": forms.DateInput(attrs={"type": "date"}),
        }
