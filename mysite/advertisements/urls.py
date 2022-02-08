from django.urls import path
from .views import (
    HomeView,
    add_adv_space_view,
    AdvSpacesListView,
    AdvSpaceDetailView,
    adv_space_delete_view,
    edit_adv_space_view,
)


urlpatterns = [
    path("", HomeView.as_view(), name="home"),
    path("adv-spaces/", AdvSpacesListView.as_view(), name="adv_spaces"),
    path("add-adv/", add_adv_space_view, name="add_adv_space"),
    path(
        "adv-space/<slug:adv_space_slug>",
        AdvSpaceDetailView.as_view(),
        name="adv_space",
    ),
    path("delete/<int:adv_space_id>", adv_space_delete_view, name="delete_adv_space"),
    path(
        "adv-space/<slug:adv_space_slug>/edit", edit_adv_space_view, name="edit_adv_space"
    ),
]
