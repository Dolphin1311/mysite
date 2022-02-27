from django.shortcuts import render, redirect
from django.views.generic import CreateView, ListView
from .forms import OrderItemForm
from .models import Order, OrderItem
from advertisements.models import AdvertisingSpace


class OrderCreateView(CreateView):
    model = OrderItem
    form_class = OrderItemForm
    template_name = "orders/create_order.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["order_item_form"] = OrderItemForm(
            adv_space=self._get_adv_space(self.kwargs.pop("adv_space_id"))
        )
        context["title"] = "Create order"

        return context

    def post(self, request, *args, **kwargs):
        adv_space = self._get_adv_space(self.kwargs.pop("adv_space_id"))
        form = self.form_class(data=request.POST, adv_space=adv_space)

        if form.is_valid():
            order_item = form.save()
            order = Order.objects.create(
                order_item=order_item, owner=adv_space.user, client=self.request.user
            )
            order.save()

            return redirect("user_cabinet")

    def _get_adv_space(self, adv_space_id):
        return AdvertisingSpace.objects.get(pk=adv_space_id)
