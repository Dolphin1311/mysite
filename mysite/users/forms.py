from django import forms
from django.contrib.auth.forms import UserCreationForm
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
