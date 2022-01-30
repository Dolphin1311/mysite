from django.urls import path
from .views import HomeView, add_adv_space_view, AdvSpacesView


urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('adv-spaces/', AdvSpacesView.as_view(), name='adv_spaces'),
    path('add-adv/', add_adv_space_view, name='add_adv_space'),
    path('adv-space/')
]
