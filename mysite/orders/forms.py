from django import forms
from .models import OrderItem


class OrderItemForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        if kwargs.get("adv_space"):
            self._adv_space = kwargs.pop("adv_space")
        super(OrderItemForm, self).__init__(*args, **kwargs)

    class Meta:
        model = OrderItem
        fields = ["date_from", "date_to", "price"]
        labels = {
            "date_from": "Date from",
            "date_to": "Date to",
            "price": "Price per month"
        }
        widgets = {
            "date_from": forms.DateInput(attrs={"id": "date-from"}),
            "date_to": forms.DateInput(attrs={"id": "date-to"}),
            "price": forms.NumberInput(attrs={"id": "price"})
        }

    def save(self, commit=True):
        instance = super(OrderItemForm, self).save(commit=False)
        instance.advertising_space = self._adv_space

        if commit:
            instance.save()

        return instance

