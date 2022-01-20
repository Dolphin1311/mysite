from django import forms
from django.urls import reverse_lazy

from .models import AdvertisingSpaceImage, AdvertisingSpace


class AdvertisingSpaceForm(forms.ModelForm):
    class Meta:
        model = AdvertisingSpace
        fields = ['title', 'advertising_space_category', 'description', 'price']
        success_url = reverse_lazy('home')


class AdvertisingSpaceImageForm(forms.ModelForm):
    class Meta:
        model = AdvertisingSpaceImage
        fields = forms.ImageField
