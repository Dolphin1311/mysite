from django.contrib.auth.decorators import login_required
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import TemplateView, ListView, DetailView, DeleteView
from .utils import DataMixin
from .forms import AdvertisingSpaceForm, AdvertisingSpaceImageForm
from .models import AdvertisingSpace, AdvertisingSpaceImage
from users.models import Person


class HomeView(DataMixin, TemplateView):
    template_name = "advertisements/index.html"

    # use DataMixin class and load to template custom context data
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        my_context = self.get_user_context(title="Main page")

        return context | my_context


class AdvSpacesListView(ListView, DataMixin):
    template_name = "advertisements/advertising-spaces.html"
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
    template_name = "advertisements/adv-space.html"
    slug_url_kwarg = "adv_space_slug"

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        my_context = self.get_user_context(title=self.object.title)
        if self.request.user.user_type.name == "person":
            my_context["person"] = Person.objects.get(user=self.request.user)

        return context | my_context


def adv_space_delete_view(request, adv_space_id):
    adv_space = AdvertisingSpace.objects.get(id=adv_space_id)
    adv_space.delete()

    return redirect("user_adv_spaces")


def edit_adv_space_view(request, adv_space_slug):
    adv_space = get_object_or_404(AdvertisingSpace, slug=adv_space_slug)
    adv_space_json_data = adv_space.data

    initial_dict = {
        "car_model": adv_space_json_data["car_model"],
        "prod_year": adv_space_json_data["prod_year"],
        "car_type": adv_space_json_data["car_type"],
        "adv_place": adv_space_json_data["adv_place"]
    }

    if request.method == "POST":
        adv_space_form = AdvertisingSpaceForm(data=request.POST, initial=initial_dict, instance=adv_space)
        # adv_space_image_form = AdvertisingSpaceImageForm(request.POST, request.FILES)

        if adv_space_form.is_valid():  #all([adv_space_form.is_valid(), adv_space_image_form.is_valid()]):
            try:
                adv_space_form.save()
                # adv_space_image = adv_space_image_form.save(commit=False)
                # adv_space_image.advertising_space = adv_space
                # adv_space_image.save()
            except Exception as e:
                import traceback
                print(traceback.format_exc())

            return redirect("add_adv_space")

    adv_space_form = AdvertisingSpaceForm(initial=initial_dict, instance=adv_space)
    # adv_space_image_form = AdvertisingSpaceImageForm()

    return render(
        request,
        "advertisements/edit-adv-space.html",
        context={
            "adv_space_form": adv_space_form,
            # "adv_space_image_form": adv_space_image_form,
        },
    )


@login_required
def add_adv_space_view(request):
    if request.method == "POST":
        adv_space_form = AdvertisingSpaceForm(data=request.POST, user=request.user)
        adv_space_image_form = AdvertisingSpaceImageForm(request.POST, request.FILES)

        if all([adv_space_form.is_valid(), adv_space_image_form.is_valid()]):
            print(adv_space_form.cleaned_data)
            try:
                adv_space = adv_space_form.save()
                adv_space_image = adv_space_image_form.save(commit=False)
                adv_space_image.advertising_space = adv_space
                adv_space_image.save()
            except Exception as e:
                import traceback
                print(traceback.format_exc())

            return redirect("add_adv_space")

    adv_space_form = AdvertisingSpaceForm(user=request.user)
    adv_space_image_form = AdvertisingSpaceImageForm()

    return render(
        request,
        "advertisements/add-adv-space.html",
        context={
            "adv_space_form": adv_space_form,
            "adv_space_image_form": adv_space_image_form,
        },
    )
