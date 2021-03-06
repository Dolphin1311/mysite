from django.utils import timezone
from django.db import models
from django.conf import settings
from advertisements.models import AdvertisingSpace


class Order(models.Model):
    date_created = models.DateTimeField(auto_now_add=True, verbose_name="Date created")
    is_confirmed = models.BooleanField(default=False, verbose_name="Is confirmed")
    owner_answer = models.BooleanField(
        default=False, verbose_name="Owner answered on order"
    )
    date_from = models.DateField(verbose_name="Date from", default=timezone.now)
    date_to = models.DateField(verbose_name="Date to", default=timezone.now)
    price = models.DecimalField(max_digits=8, decimal_places=2)
    advertising_space = models.ForeignKey(
        AdvertisingSpace, on_delete=models.CASCADE, verbose_name="Advertising space id"
    )
    client = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name="client",
        verbose_name="Client id",
    )

    def __str__(self):
        return f"Status: {self.is_confirmed}, client: {self.client}"
