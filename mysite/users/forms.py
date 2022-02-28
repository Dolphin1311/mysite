from django import forms
from django.contrib.auth import authenticate
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import User, Person


class UserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ["email", "user_type"]
        widgets = {"password": forms.PasswordInput()}
        labels = {"email": "E-mail", "user_type": "User type"}


class PersonForm(forms.ModelForm):
    class Meta:
        model = Person
        fields = ["first_name", "last_name", "phone", "date_birthday"]
        widgets = {"date_birthday": forms.DateInput(attrs={"type": "date"})}
        labels = {
            "first_name": "First name",
            "last_name": "Last name",
            "phone": "Phone",
            "date_birthday": "Date of birthday",
        }


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
