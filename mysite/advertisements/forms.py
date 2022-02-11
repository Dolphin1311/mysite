from django import forms
from django.forms import inlineformset_factory
from django.urls import reverse_lazy

from .models import AdvertisingSpaceImage, AdvertisingSpace


class AdvertisingSpaceImageForm(forms.ModelForm):
    class Meta:
        model = AdvertisingSpaceImage
        fields = ["image"]
        widgets = {"image": forms.FileInput(attrs={"accept": "image/png, image/jpeg", "multiple": True})}


class AdvertisingSpaceForm(forms.ModelForm):
    car_model = forms.CharField(
        label="Model", widget=forms.TextInput(attrs={"id": "model"})
    )
    prod_year = forms.IntegerField(
        label="Production year",
        widget=forms.NumberInput(
            attrs={"id": "year", "min": 1900, "max": 2022, "step": 1, "value": 2022}
        ),
    )
    car_type = forms.CharField(
        label="Car type", widget=forms.TextInput(attrs={"id": "type"})
    )
    adv_place = forms.CharField(
        label="Place for advertising on the car",
        widget=forms.TextInput(attrs={"id": "place"}),
    )

    def __init__(self, *args, **kwargs):
        if kwargs.get("user"):
            self.user = kwargs.pop("user")
        super(AdvertisingSpaceForm, self).__init__(*args, **kwargs)

    class Meta:
        model = AdvertisingSpace
        fields = ["title", "description", "advertising_space_category", "price"]
        labels = {
            "title": "Title",
            "advertising_space_category": "Category",
            "description": "Description",
            "price": "Price per month",
        }
        widgets = {
            "title": forms.TextInput(attrs={"id": "title"}),
            "advertising_space_category": forms.Select(attrs={"id": "category"}),
            "description": forms.Textarea(
                attrs={"id": "description", "cols": 30, "rows": 10}
            ),
            "price": forms.NumberInput(attrs={"id": "price"}),
        }

    def save(self, commit=True):
        json_data = {
            "car_model": self.cleaned_data["car_model"],
            "prod_year": self.cleaned_data["prod_year"],
            "car_type": self.cleaned_data["car_type"],
            "adv_place": self.cleaned_data["adv_place"],
        }

        instance = super(AdvertisingSpaceForm, self).save(commit=False)
        instance.data = json_data

        if hasattr(self, "user"):
            instance.user = self.user

        if commit:
            instance.save()

        return instance


AdvertisingSpaceImagesFormSet = inlineformset_factory(
    AdvertisingSpace,
    AdvertisingSpaceImage,
    fields=["image"],
    extra=8
)
