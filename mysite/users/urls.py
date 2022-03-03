from django.urls import path
from .views import (
    logout_view,
    UserCabinetAdvSpacesListView,
    UserLoginView,
    UserCabinetOrdersListView,
    UserCabinetUpdatePersonalDataView,
    UserSignupView
)

urlpatterns = [
    path("", UserCabinetAdvSpacesListView.as_view(), name="user_cabinet"),
    path("signup/", UserSignupView.as_view(), name="signup"),
    path("login/", UserLoginView.as_view(), name="login"),
    path("logout/", logout_view, name="logout"),
    path("orders/", UserCabinetOrdersListView.as_view(), name="user_orders"),
    path("data/", UserCabinetUpdatePersonalDataView.as_view(), name="user_data")
]
