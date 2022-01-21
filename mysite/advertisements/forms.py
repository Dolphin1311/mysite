from django import forms
from django.urls import reverse_lazy

from .models import AdvertisingSpaceImage, AdvertisingSpace


class AdvertisingSpaceForm(forms.ModelForm):
    car_model = forms.CharField()
    prod_year = forms.IntegerField()
    car_type = forms.CharField()
    adv_place = forms.CharField()

    class Meta:
        model = AdvertisingSpace
        fields = ['title', 'description', 'advertising_space_category', 'price']
        success_url = reverse_lazy('home')

    # def save(self, commit=True):
    #     car_model = self.cleaned_data['car_model']
    #     prod_year = self.cleaned_data['prod_year']
    #     car_type = self.cleaned_data['car_type']
    #     adv_place = self.cleaned_data['adv_place']
    #
    #     json_data = {
    #         'car_model': car_model,
    #         'prod_year': prod_year,
    #         'car_type': car_type,
    #         'adv_place': adv_place
    #     }




# class AdvertisingSpaceImageForm(forms.ModelForm):
#     class Meta:
#         model = AdvertisingSpaceImage
#         fields = forms.ImageField
