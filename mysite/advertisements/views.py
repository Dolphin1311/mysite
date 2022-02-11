from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import TemplateView, ListView, DetailView
from django.forms import inlineformset_factory
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
    template_name = "advertisements/adv_space.html"
    slug_url_kwarg = "adv_space_slug"

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        my_context = self.get_user_context(title=self.object.title)
        if self.request.user.user_type.name == "person":
            my_context["person"] = Person.objects.get(user=self.request.user)

        return context | my_context


def adv_space_delete_view(request, adv_space_slug):
    adv_space = AdvertisingSpace.objects.get(slug=adv_space_slug)
    adv_space.delete()

    return redirect("user_adv_spaces")


@login_required
def edit_adv_space_view(request, adv_space_slug):
    adv_space = get_object_or_404(AdvertisingSpace, slug=adv_space_slug)
    adv_space_images_formset = inlineformset_factory(AdvertisingSpace, AdvertisingSpaceImage, fields=["image"], extra=8)

    adv_space_json_data = adv_space.data
    adv_space_initial_dict = {
        "car_model": adv_space_json_data["car_model"],
        "prod_year": adv_space_json_data["prod_year"],
        "car_type": adv_space_json_data["car_type"],
        "adv_place": adv_space_json_data["adv_place"],
    }

    if request.method == "POST":
        adv_space_form = AdvertisingSpaceForm(
            data=request.POST, initial=adv_space_initial_dict, instance=adv_space
        )
        images_formset = adv_space_images_formset(request.POST, request.FILES, instance=adv_space)

        if all([adv_space_form.is_valid(), images_formset.is_valid()]):
            try:
                adv_space_form.save()
                images_formset.save()
            except Exception as e:
                import traceback

                print(traceback.format_exc())

            return redirect("user_adv_spaces")

    adv_space_form = AdvertisingSpaceForm(initial=adv_space_initial_dict, instance=adv_space)
    images_formset = adv_space_images_formset(instance=adv_space)

    return render(
        request,
        "advertisements/edit_adv_space.html",
        context={
            "adv_space_form": adv_space_form,
            "adv_space_image_form": images_formset,
        },
    )


@login_required
def add_adv_space_view(request):
    if request.method == "POST":
        adv_space_form = AdvertisingSpaceForm(data=request.POST, user=request.user)
        adv_space_image_form = AdvertisingSpaceImageForm(request.POST, request.FILES)
        images = request.FILES.getlist('image')

        if all([adv_space_form.is_valid(), adv_space_image_form.is_valid()]):
            try:
                adv_space = adv_space_form.save()
                for image in images:
                    adv_space_image = AdvertisingSpaceImage.objects.create(image=image, advertising_space=adv_space)
                    adv_space_image.save()
            except Exception:
                import traceback

                print(traceback.format_exc())

            return redirect("user_adv_spaces")

    adv_space_form = AdvertisingSpaceForm(user=request.user)
    adv_space_image_form = AdvertisingSpaceImageForm()

    return render(
        request,
        "advertisements/add_adv_space.html",
        context={
            "adv_space_form": adv_space_form,
            "adv_space_image_form": adv_space_image_form,
        }
    )
