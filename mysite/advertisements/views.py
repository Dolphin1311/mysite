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


class AddAdv(CreateView):
    form_class = AdvertisingSpaceForm
    template_name = 'advertisements/add_adv.html'
