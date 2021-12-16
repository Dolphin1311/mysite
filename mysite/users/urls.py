from django.urls import path
from .views import register_user, LoginUserView

urlpatterns = [
    path('registration/', register_user, name='registration'),
    path('login/', LoginUserView.as_view(), name='login')
]
