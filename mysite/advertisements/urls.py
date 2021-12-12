from django.urls import path
from .views import HomeView, AddAdv


urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('add-adv/', AddAdv.as_view())
]
