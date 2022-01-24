from django import template
from advertisements.models import AdvertisingSpaceImage

register = template.Library()


@register.filter
def get_image(item, count='all'):
    '''
    Get images for selected adv space
    :param item: object of adv space
    :param count: count of images
    :return: queryset of images
    '''
    if count == 'all':
        images = AdvertisingSpaceImage.objects.values('image').filter(advertising_space=item)
    else:
        images = AdvertisingSpaceImage.objects.values('image').filter(advertising_space=item)[:count]
        print(images)

    return images
