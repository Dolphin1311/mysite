from django.core.validators import MinValueValidator
from datetime import datetime
from django import forms
from django.forms import inlineformset_factory
from .models import AdvertisingSpaceImage, AdvertisingSpace, AdvertisingSpaceCategory


class AdvertisingSpaceForm(forms.ModelForm):
    car_model = forms.CharField(
        label="Model", widget=forms.TextInput(attrs={"id": "model"})
    )
    prod_year = forms.IntegerField(
        label="Production year",
        widget=forms.NumberInput(
            attrs={
                "id": "year",
                "min": 1900,
                "max": datetime.now().year,
                "step": 1,
                "value": datetime.now().year,
            }
        ),
        validators=[MinValueValidator(1900)],
    )
    car_type = forms.CharField(
        label="Car type", widget=forms.TextInput(attrs={"id": "type"})
    )
    adv_place = forms.CharField(
        label="Place for advertising on the car",
        widget=forms.TextInput(attrs={"id": "place"}),
    )
    field_order = [
        "title",
        "description",
        "price",
        "advertising_space_category",
        "car_model",
        "car_type",
        "prod_year",
        "adv_place",
    ]

    def __init__(self, *args, **kwargs):
        if kwargs.get("user") is not None:
            self._user = kwargs.pop("user")
        super(AdvertisingSpaceForm, self).__init__(*args, **kwargs)
        # set queryset for select advertising_space_category
        self.fields[
            "advertising_space_category"
        ].queryset = AdvertisingSpaceCategory.objects.all()

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
            "price": forms.NumberInput(attrs={"id": "price", "min": 0.01}),
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

        if hasattr(self, "_user"):
            instance.user = self._user

        if commit:
            instance.save()

        return instance


AdvertisingSpaceImagesFormSet = inlineformset_factory(
    AdvertisingSpace, AdvertisingSpaceImage, fields=["image"], extra=8, max_num=8
)


class FilterAdvSpacesForm(forms.Form):
    category = forms.ModelChoiceField(queryset=AdvertisingSpaceCategory.objects.all())
    price_from = forms.DecimalField(min_value=0.01, decimal_places=2)
    price_to = forms.DecimalField(min_value=0.01, decimal_places=2)

    class Meta:
        labels = {
            "category": "Category",
            "price_from": "Price from",
            "price_to": "Price to"
        }
