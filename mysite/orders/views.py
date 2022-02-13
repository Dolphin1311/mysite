from django.shortcuts import render, redirect
from django.views.generic import CreateView
from .forms import OrderItemForm
from .models import Order, OrderItem
from advertisements.models import AdvertisingSpace


class OrderItemCreateView(CreateView):
    model = OrderItem
    form_class = OrderItemForm
    template_name = "orders/create_order.html"

    def __init__(self):
        self._adv_space = None
        self._owner = None

        super(OrderItemCreateView, self).__init__()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # get adv space and client for order item
        self._adv_space = self._get_adv_space(kwargs["adv_space_id"])
        self._owner = self._adv_space.user
        context["order_item_form"] = OrderItemForm(self._adv_space)
        context["title"] = "Create order"

    def post(self, request, *args, **kwargs):
        form = self.form_class(data=request.POST, adv_space=self._adv_space)

        if form.is_valid():
            order_item = form.save()
            order = Order.objects.create(
                order_item=order_item,
                owner=self._owner,
                client=self.request.user
            )

            return redirect("user_cabinet")



    def _get_adv_space(self, adv_space_id):
        return AdvertisingSpace.objects.get(pk=adv_space_id)
