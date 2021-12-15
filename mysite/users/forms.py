from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User, Person


class NewUserForm(UserCreationForm):
    def __init__(self, *args, **kwargs):
        super(NewUserForm, self).__init__(*args, **kwargs)
        self.fields['email'].label = 'E-mail'

    class Meta:
        model = User
        fields = ['email']
        widgets = {
            'password': forms.PasswordInput()
        }


class NewPersonForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(NewPersonForm, self).__init__(*args, **kwargs)
        self.fields['first_name'].label = 'First name'
        self.fields['last_name'].label = 'Last name'
        self.fields['phone'].label = 'Phone'
        self.fields['date_birthday'].label = 'Date of birthday'

    class Meta:
        model = Person
        fields = ['first_name', 'last_name', 'phone', 'date_birthday']
        widgets = {
            'date_birthday': forms.DateInput(attrs={'type': 'date'})
        }
