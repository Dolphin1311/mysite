from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.views.generic import CreateView, TemplateView, ListView
from .utils import DataMixin
from .forms import AdvertisingSpaceForm, AdvertisingSpaceImageForm
from .models import AdvertisingSpace, AdvertisingSpaceImage


class HomeView(DataMixin, TemplateView):
    template_name = 'advertisements/index.html'

    # use DataMixin class and load to template custom context data
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        my_context = self.get_user_context(title='Main page')

        return context | my_context


class AdvSpacesView(ListView, DataMixin):
    template_name = 'advertisements/advertising-spaces.html'
    model = AdvertisingSpace
    context_object_name = 'adv_spaces'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        my_context = self.get_user_context(title='Advertising Spaces')

        return context | my_context

    def get_queryset(self):
        return AdvertisingSpace.objects.filter(is_published=True)


@login_required
def add_adv_space_view(request):
    if request.method == 'POST':
        adv_space_form = AdvertisingSpaceForm(data=request.POST, user=request.user)
        adv_space_image_form = AdvertisingSpaceImageForm(request.POST, request.FILES)

        if all([adv_space_form.is_valid(), adv_space_image_form.is_valid()]):
            try:
                adv_space = adv_space_form.save()
                adv_space_image = adv_space_image_form.save(commit=False)
                adv_space_image.advertising_space = adv_space
                adv_space_image.save()
            except Exception as e:
                print(e)

            return redirect('add_adv_space')

    adv_space_form = AdvertisingSpaceForm(user=request.user)
    adv_space_image_form = AdvertisingSpaceImageForm()

    return render(request, 'advertisements/add-adv-space.html', context={
        'adv_space_form': adv_space_form,
        'adv_space_image_form': adv_space_image_form
    })
