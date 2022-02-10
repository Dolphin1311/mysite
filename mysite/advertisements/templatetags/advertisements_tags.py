from django import template
from advertisements.models import AdvertisingSpaceImage

register = template.Library()


@register.filter
def get_images(item, count="all"):
    """
    Get images for selected adv space
    :param item: object of adv space
    :param count: count of images
    :return: queryset of images
    """
    if count == "all":
        images = AdvertisingSpaceImage.objects.values("image").filter(
            advertising_space=item
        )
    else:
        images = AdvertisingSpaceImage.objects.values("image").filter(
            advertising_space=item
        )[:count]

    return images


@register.filter
def get_data_from_json(item, data):
    return item[data]


@register.inclusion_tag("advertisements/adv_space_form.html", takes_context=True)
def show_adv_space_form(context, action):
    return {
        "adv_space_form": context["adv_space_form"],
        "adv_space_image_form": context["adv_space_image_form"],
        "action": action.capitalize
    }
