from django.urls import path
from .views import OrderCreateView

urlpatterns = [
    path(
        "make-order/<int:adv_space_id>/<int:client_id>",
        OrderCreateView.as_view(),
        name="make_order",
    )
]
