from django.shortcuts import redirect, get_object_or_404
from django.views.generic import CreateView
from .forms import OrderForm
from .models import Order
from advertisements.models import AdvertisingSpace


class OrderCreateView(CreateView):
    model = Order
    form_class = OrderForm
    template_name = "orders/create_order.html"

    def post(self, request, *args, **kwargs):
        form = self.form_class(data=request.POST, **self.get_form_kwargs())

        if form.is_valid():
            form.save()

            return redirect("user_cabinet")

    def _get_adv_space(self, adv_space_id):
        return AdvertisingSpace.objects.get(pk=adv_space_id)

    def get_form_kwargs(self):
        return {
            "adv_space": AdvertisingSpace.objects.get(
                pk=self.kwargs.get("adv_space_id")
            ),
            "client": self.request.user,
        }


def accept_order_view(request, order_id):
    order = get_object_or_404(Order, pk=order_id)
    order.is_confirmed = True
    order.owner_answer = True
    order.save()

    return redirect("user_orders")


def decline_order_view(request, order_id):
    order = get_object_or_404(Order, pk=order_id)
    order.is_confirmed = False
    order.owner_answer = True
    order.save()

    return redirect("user_orders")
