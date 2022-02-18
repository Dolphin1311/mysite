from django.urls import path
from .views import (
    HomeView,
    AdvSpaceListView,
    AdvSpaceDetailView,
    AdvSpaceUpdateView,
    AdvSpaceCreateView,
    AdvSpaceDeleteView,
)


urlpatterns = [
    path("", HomeView.as_view(), name="home"),
    path("adv-spaces/", AdvSpaceListView.as_view(), name="adv_spaces"),
    path("add-adv/", AdvSpaceCreateView.as_view(), name="add_adv_space"),
    path(
        "adv-space/<slug:adv_space_slug>",
        AdvSpaceDetailView.as_view(),
        name="adv_space",
    ),
    path(
        "adv_space/<slug:adv_space_slug>/delete/",
        AdvSpaceDeleteView.as_view(),
        name="delete_adv_space",
    ),
    path(
        "adv-space/<slug:adv_space_slug>/edit/",
        AdvSpaceUpdateView.as_view(),
        name="edit_adv_space",
    ),
]
