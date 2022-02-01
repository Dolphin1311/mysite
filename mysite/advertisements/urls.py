from django.urls import path
from .views import HomeView, add_adv_space_view, AdvSpacesListView, AdvSpaceDetailView


urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('adv-spaces/', AdvSpacesListView.as_view(), name='adv_spaces'),
    path('add-adv/', add_adv_space_view, name='add_adv_space'),
    path('adv-space/<slug:adv_space_slug>', AdvSpaceDetailView.as_view(), name='adv_space')
]
