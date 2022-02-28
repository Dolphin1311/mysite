from django import forms
from .models import Order


class OrderForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        if kwargs.get("adv_space"):  # get advertising space for order
            self._adv_space = kwargs.pop("adv_space")
        if kwargs.get("client"):  # get client for order
            self._client = kwargs.pop("client")
        super(OrderForm, self).__init__(*args, **kwargs)

    class Meta:
        model = Order
        fields = ["date_from", "date_to", "price"]
        labels = {
            "date_from": "Date from",
            "date_to": "Date to",
            "price": "Price per month",
        }
        widgets = {
            "date_from": forms.DateInput(attrs={"id": "date-from"}),
            "date_to": forms.DateInput(attrs={"id": "date-to"}),
            "price": forms.NumberInput(attrs={"id": "price"}),
        }

    def save(self, commit=True):
        instance = super(OrderForm, self).save(commit=False)
        instance.advertising_space = self._adv_space
        instance.client = self._client

        if commit:
            instance.save()

        return instance


class FilterOrdersForm(forms.Form):
    end_user = forms.ChoiceField(
        choices=(("client", "You client"), ("owner", "You owner"))
    )
    status = forms.ChoiceField(choices=((True, "Confirmed"), (False, "Not confirmed")))
