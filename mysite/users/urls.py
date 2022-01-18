from django.urls import path
from .views import sign_up, log_in, log_out, UserCabinetAdvSpacesView

urlpatterns = [
    path('', UserCabinetAdvSpacesView.as_view(), name='user_adv_spaces'),
    path('registration/', sign_up, name='registration'),
    path('login/', log_in, name='login'),
    path('logout/', log_out, name='logout')
]
