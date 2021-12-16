from django.urls import path
from .views import sign_up_user, sign_in_user

urlpatterns = [
    path('registration/', sign_up_user, name='registration'),
    path('login/', sign_in_user, name='login')
]
