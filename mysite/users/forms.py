from django import forms
from django.contrib.auth import authenticate
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import User


class UserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ["email", "user_type"]
        widgets = {"password": forms.PasswordInput()}
        labels = {"email": "E-mail", "user_type": "User type"}


class LoginForm(AuthenticationForm):
    def clean(self):
        username = self.cleaned_data.get("username")
        password = self.cleaned_data.get("password")

        if username is not None and password:
            self.user_cache = authenticate(
                self.request, email=username, password=password
            )
            if self.user_cache is None:
                raise self.get_invalid_login_error()
            else:
                self.confirm_login_allowed(self.user_cache)

        return self.cleaned_data
