from django.views.generic.base import ContextMixin


class DataMixin(ContextMixin):
    def get_context_data(self, **kwargs):
        context = super(DataMixin, self).get_context_data(**kwargs)

        return context
