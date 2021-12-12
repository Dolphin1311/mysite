from .models import AdvertisingSpaceType


class DataMixin:
    def get_user_context(self, **kwargs):
        context = kwargs
        adv_types = AdvertisingSpaceType.objects.all()
        context['adv_types'] = adv_types

        return context
