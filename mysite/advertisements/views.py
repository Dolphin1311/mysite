from django.shortcuts import render, redirect
from django.views.generic import CreateView, TemplateView, ListView
from .utils import DataMixin
from .forms import AdvertisingSpaceForm
from .models import AdvertisingSpace


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


def add_adv_space(request):
    if request.method == 'POST':
        adv_space_form = AdvertisingSpaceForm(request.POST)
        print(adv_space_form.is_valid())
        if adv_space_form.is_valid():
            # data variables from form
            car_model = adv_space_form.cleaned_data['car_model']
            prod_year = adv_space_form.cleaned_data['prod_year']
            car_type = adv_space_form.cleaned_data['car_type']
            adv_place = adv_space_form.cleaned_data['adv_place']
            user = request.user

            json_data = {
                'car_model': car_model,
                'prod_year': prod_year,
                'car_type': car_type,
                'adv_place': adv_place
            }
            try:
                adv_space = adv_space_form.save(commit=False)
                adv_space.user = user
                adv_space.data = json_data
                adv_space.save()
            except Exception as e:
                print(e)

            return redirect('home')

    adv_space_form = AdvertisingSpaceForm()

    return render(request, 'advertisements/add-adv-space.html', context={'adv_space_form': adv_space_form})
