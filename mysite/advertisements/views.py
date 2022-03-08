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
from django.views.generic.edit import FormMixin
from .forms import AdvertisingSpaceForm, AdvertisingSpaceImagesFormSet, FilterAdvSpacesForm
from .models import AdvertisingSpace


class HomeView(TemplateView):
    template_name = "advertisements/index.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["adv_spaces"] = AdvertisingSpace.objects.filter(is_published=True)

        return context


class AdvSpaceListView(ListView, FormMixin):
    template_name = "advertisements/advertising_spaces.html"
    model = AdvertisingSpace
    context_object_name = "adv_spaces"
    form_class = FilterAdvSpacesForm

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        adv_spaces = AdvertisingSpace.objects.all()
        if form.is_valid():
            adv_spaces = AdvertisingSpace.objects.filter(
                advertising_space_category=form.cleaned_data["category"],
                price__gte=float(form.cleaned_data["price_from"]),
                price__lte=float(form.cleaned_data["price_to"])
            )

        return render(request, self.template_name, {"adv_spaces": adv_spaces, "form": form})

    def get_queryset(self):
        return AdvertisingSpace.objects.filter(is_published=True)


class AdvSpaceDetailView(DetailView):
    model = AdvertisingSpace
    context_object_name = "adv_space"
    template_name = "advertisements/advertising_space.html"
    slug_url_kwarg = "adv_space_slug"


class AdvSpaceDeleteView(DeleteView):
    model = AdvertisingSpace
    success_url = reverse_lazy("user_cabinet")
    slug_url_kwarg = "adv_space_slug"

    def get(self, *args, **kwargs):
        return self.post(*args, **kwargs)


class AdvSpaceUpdateView(UpdateView, LoginRequiredMixin):
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
        context["adv_space_form"] = self.form_class(
            initial=self.object_initial_data, instance=self.object
        )

        return context

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


class AdvSpaceCreateView(CreateView, LoginRequiredMixin):
    model = AdvertisingSpace
    form_class = AdvertisingSpaceForm
    template_name = "advertisements/create_advertising_space.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["adv_space_form"] = self.form_class(user=self.request.user)
        context["adv_space_images_formset"] = AdvertisingSpaceImagesFormSet()

        return context

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
                self.template_name,
                {"adv_space_form": form, "adv_space_images_formset": images_formset},
            )
