from django.utils import timezone
from django.db import models
from django.conf import settings
from advertisements.models import AdvertisingSpace


class OrderItem(models.Model):
    date_from = models.DateField(verbose_name="Date from", default=timezone.now)
    date_to = models.DateField(verbose_name="Date to", default=timezone.now)
    price = models.DecimalField(max_digits=8, decimal_places=2)
    advertising_space = models.ForeignKey(
        AdvertisingSpace, on_delete=models.CASCADE, verbose_name="Advertising space id"
    )


class Order(models.Model):
    date_created = models.DateTimeField(auto_now_add=True, verbose_name="Date created")
    is_confirmed = models.BooleanField(default=False, verbose_name="Is confirmed")
    order_item = models.ForeignKey(
        OrderItem, on_delete=models.CASCADE, verbose_name="Order item"
    )
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name="owner",
        verbose_name="Owner id",
    )
    client = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name="client",
        verbose_name="Client id",
    )
