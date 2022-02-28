from django.urls import path
from .views import (
    signup_view,
    logout_view,
    UserCabinetAdvSpacesListView,
    UserLoginView,
    UserCabinetOrdersListView,
)

urlpatterns = [
    path("", UserCabinetAdvSpacesListView.as_view(), name="user_cabinet"),
    path("signup/", signup_view, name="signup"),
    path("login/", UserLoginView.as_view(), name="login"),
    path("logout/", logout_view, name="logout"),
    path("orders/", UserCabinetOrdersListView.as_view(), name="user_orders"),
    # change here
    path("data/", logout_view, name="user_data"),
    path("change-password/", logout_view, name="user_change_pass"),
]
