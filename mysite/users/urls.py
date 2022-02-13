from django.urls import path
from .views import signup_view, login_view, logout_view, UserCabinetAdvSpacesView

urlpatterns = [
    path("", UserCabinetAdvSpacesView.as_view(), name="user_cabinet"),
    path("signup/", signup_view, name="signup"),
    path("login/", login_view, name="login"),
    path("logout/", logout_view, name="logout"),
    # change here
    path("messages/", logout_view, name="user_messages"),
    path("data/", logout_view, name="user_data"),
    path("change-password/", logout_view, name="user_change_pass"),
]
