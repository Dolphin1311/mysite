from .models import AdvertisingSpaceType


class DataMixin:
    @staticmethod
    def get_user_context(**kwargs):
        context = kwargs
        adv_types = AdvertisingSpaceType.objects.all()
        context['adv_types'] = adv_types

        return context
