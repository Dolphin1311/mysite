from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User, Person


class NewUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['email']
        widgets = {
            'password': forms.PasswordInput()
        }


class NewPersonForm(forms.ModelForm):
    class Meta:
        model = Person
        fields = ['first_name', 'last_name', 'phone', 'date_birthday']
        widgets = {
            'date_birthday': forms.DateInput(attrs={'type': 'date'})
        }
