from .models import AdvertisingSpaceType


class DataMixin:
    @staticmethod
    def get_user_context(**kwargs):
        context = kwargs

        return context
