from django import forms
from django.urls import reverse_lazy

from .models import AdvertisingSpaceImage, AdvertisingSpace


class AdvertisingSpaceForm(forms.ModelForm):
    car_model = forms.CharField()
    prod_year = forms.IntegerField()
    car_type = forms.CharField()
    adv_place = forms.CharField()

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user')
        super(AdvertisingSpaceForm, self).__init__(*args, **kwargs)

    class Meta:
        model = AdvertisingSpace
        fields = ['title', 'description', 'advertising_space_category', 'price']
        success_url = reverse_lazy('home')

    def save(self, commit=True):
        car_model = self.cleaned_data['car_model']
        prod_year = self.cleaned_data['prod_year']
        car_type = self.cleaned_data['car_type']
        adv_place = self.cleaned_data['adv_place']

        json_data = {
            'car_model': car_model,
            'prod_year': prod_year,
            'car_type': car_type,
            'adv_place': adv_place
        }

        instance = super(AdvertisingSpaceForm, self).save(commit=False)
        instance.data = json_data
        instance.user = self.user

        if commit:
            instance.save()

        return instance

