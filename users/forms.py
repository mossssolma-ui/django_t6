from django import forms
from django.contrib.auth.forms import UserCreationForm

from catalog.forms import StyleFormMixin
from .models import CustomUser


class CustomUserCreationForm(StyleFormMixin, UserCreationForm):
    phone_number = forms.CharField(max_length=15, required=False, help_text="Номер телефона (необязательно)")

    class Meta:
        model = CustomUser
        fields = ("email", "password1", "password2")

    def clean_phone_number(self):
        phone_number = self.cleaned_data.get("phone_number")
        if phone_number and not phone_number.isdigit():
            raise forms.ValidationError("Номер должен состоять из цифр")
        return phone_number


class CustomUserRegisterForm(StyleFormMixin, UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ("email", "password1", "password2")


class ProfileUserUpdateForm(StyleFormMixin, forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ("first_name", "last_name", "phone_number", "country", "avatar")
