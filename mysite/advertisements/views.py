from django.views.generic import CreateView, TemplateView


from .utils import DataMixin
from .forms import AdvertisingSpaceForm


class HomeView(DataMixin, TemplateView):
    template_name = 'advertisements/index.html'

    # use DataMixin class and load to template custom context data
    def get_context_data(self, **kwargs):
        user = self.request.user
        context = super().get_context_data(**kwargs)
        my_context = self.get_user_context(title='Main page', user=user)

        return context | my_context


class AddAdv(CreateView):
    form_class = AdvertisingSpaceForm
    template_name = 'advertisements/add_adv.html'
