from django.core.exceptions import ValidationError
from django.utils import timezone
from django.views.generic.base import ContextMixin


class DataMixin(ContextMixin):
    def get_context_data(self, **kwargs):
        context = super(DataMixin, self).get_context_data(**kwargs)

        return context


def no_future_date(value):
    today = timezone.now().date()
    if value > today:
        raise ValidationError("Date of birthday can't be in future.")
