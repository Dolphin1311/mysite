from django.urls import path
from .views import index, AddAdv


urlpatterns = [
    path('', index, name='home'),
    path('add-adv/', AddAdv.as_view())
]
