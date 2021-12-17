from django.urls import path
from .views import sign_up, log_in, log_out

urlpatterns = [
    path('registration/', sign_up, name='registration'),
    path('login/', log_in, name='login'),
    path('logout/', log_out, name='logout')
]
