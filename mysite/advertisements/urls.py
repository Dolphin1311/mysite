from django.urls import path
from .views import HomeView, AddAdv, AdvSpacesView


urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('adv-spaces/', AdvSpacesView.as_view(), name='adv_spaces'),
    path('add-adv/', AddAdv.as_view())
]
