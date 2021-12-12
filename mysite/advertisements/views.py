from django.http import HttpResponse, HttpRequest
from django.views.generic import CreateView, TemplateView

from .utils import DataMixin
from .forms import AdvertisingSpaceForm


class HomeView(DataMixin, TemplateView):
    template_name = 'advertisements/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        my_context = self.get_user_context(title='Main page')

        return context | my_context


def index(request: HttpRequest):
    return HttpResponse('First page')


class AddAdv(CreateView):
    form_class = AdvertisingSpaceForm
    template_name = 'advertisements/add_adv.html'
