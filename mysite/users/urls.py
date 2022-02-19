from django.urls import path
from .views import signup_view, logout_view, UserCabinetAdvSpacesView, UserLoginView

urlpatterns = [
    path("", UserCabinetAdvSpacesView.as_view(), name="user_cabinet"),
    path("signup/", signup_view, name="signup"),
    path("login/", UserLoginView.as_view(), name="login"),
    path("logout/", logout_view, name="logout"),
    # change here
    path("messages/", logout_view, name="user_messages"),
    path("data/", logout_view, name="user_data"),
    path("change-password/", logout_view, name="user_change_pass"),
]
