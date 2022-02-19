from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.views.generic import (
    TemplateView,
    ListView,
    DetailView,
    UpdateView,
    CreateView,
    DeleteView,
)
from .utils import DataMixin
from .forms import AdvertisingSpaceForm, AdvertisingSpaceImagesFormSet
from .models import AdvertisingSpace
from users.models import Person


class HomeView(DataMixin, TemplateView):
    template_name = "advertisements/index.html"

    # use DataMixin class and load to template custom context data
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        my_context = self.get_user_context(title="Main page")

        return context | my_context


class AdvSpaceListView(ListView, DataMixin):
    template_name = "advertisements/advertising_spaces.html"
    model = AdvertisingSpace
    context_object_name = "adv_spaces"

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        my_context = self.get_user_context(title="Advertising Spaces")

        return context | my_context

    def get_queryset(self):
        return AdvertisingSpace.objects.filter(is_published=True)


class AdvSpaceDetailView(DetailView, DataMixin):
    model = AdvertisingSpace
    context_object_name = "adv_space"
    template_name = "advertisements/advertising_space.html"
    slug_url_kwarg = "adv_space_slug"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        my_context = self.get_user_context(title=self.object.title)
        # check if it is an anonymous user or logged-in user
        if not self.request.user.is_anonymous:
            # check user_type
            if self.request.user.user_type.name == "person":
                my_context["person"] = Person.objects.get(user=self.request.user)

        return context | my_context


class AdvSpaceDeleteView(DeleteView):
    model = AdvertisingSpace
    success_url = reverse_lazy("user_cabinet")
    slug_url_kwarg = "adv_space_slug"

    def get(self, *args, **kwargs):
        return self.post(*args, **kwargs)


class AdvSpaceUpdateView(UpdateView, DataMixin, LoginRequiredMixin):
    model = AdvertisingSpace
    form_class = AdvertisingSpaceForm
    template_name = "advertisements/update_advertising_space.html"
    context_object_name = "adv_space"
    slug_url_kwarg = "adv_space_slug"

    def __init__(self):
        self.object = None
        self.object_initial_data = {}

        super(AdvSpaceUpdateView, self).__init__()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        object_json_data = self.object.data
        self.object_initial_data = {
            "car_model": object_json_data["car_model"],
            "prod_year": object_json_data["prod_year"],
            "car_type": object_json_data["car_type"],
            "adv_place": object_json_data["adv_place"],
        }
        context["adv_space_images_formset"] = AdvertisingSpaceImagesFormSet(
            instance=self.object
        )
        context["adv_space_form"] = AdvertisingSpaceForm(
            initial=self.object_initial_data, instance=self.object
        )
        my_context = self.get_user_context(title="Edit advertising space")

        return context | my_context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.form_class(
            data=request.POST, initial=self.object_initial_data, instance=self.object
        )
        images_formset = AdvertisingSpaceImagesFormSet(
            self.request.POST, self.request.FILES, instance=self.object
        )

        if all([form.is_valid(), images_formset.is_valid]):
            form.save()
            images_formset.save()

            return redirect("user_cabinet")


class AdvSpaceCreateView(CreateView, DataMixin, LoginRequiredMixin):
    model = AdvertisingSpace
    form_class = AdvertisingSpaceForm
    template_name = "advertisements/create_advertising_space.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["adv_space_form"] = AdvertisingSpaceForm(user=self.request.user)
        context["adv_space_images_formset"] = AdvertisingSpaceImagesFormSet()
        my_context = self.get_user_context(title="Add advertising space")

        return my_context | context

    def post(self, request, *args, **kwargs):
        form = self.form_class(data=request.POST, user=request.user)
        images_formset = AdvertisingSpaceImagesFormSet(
            self.request.POST,
            self.request.FILES,
        )

        if all([form.is_valid(), images_formset.is_valid()]):
            adv_space = form.save()
            adv_space_images = images_formset.save(commit=False)
            for image in adv_space_images:
                image.advertising_space = adv_space
                image.save()

            return redirect("user_cabinet")
        else:
            return render(
                self.request,
                "advertisements/create_advertising_space.html",
                {"adv_space_form": form, "adv_space_images_formset": images_formset},
            )
