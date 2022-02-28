from django.urls import path
from .views import OrderCreateView, accept_order_view, decline_order_view

urlpatterns = [
    path(
        "make-order/<int:adv_space_id>/<int:client_id>",
        OrderCreateView.as_view(),
        name="make_order",
    ),
    path("accept-order/<int:order_id>", accept_order_view, name="accept_order"),
    path("decline-order/<int:order_id>", decline_order_view, name="decline_order"),
]
