from django.urls import path
from .views import signup_view, login_view, logout_view, UserCabinetAdvSpacesView

urlpatterns = [
    path('', UserCabinetAdvSpacesView.as_view(), name='user_adv_spaces'),
    path('registration/', signup_view, name='signup'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout')
]
