from django.contrib import admin
from .models import Order


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ("date_created", "is_confirmed", "order_item", "owner", "client")
