from django import forms
from django.urls import reverse_lazy

from .models import AdvertisingSpaceImage


class AdvertisingSpaceForm(forms.ModelForm):
    class Meta:
        model = AdvertisingSpaceImage
        fields = ['image', 'advertising_space']
        success_url = reverse_lazy('home')
