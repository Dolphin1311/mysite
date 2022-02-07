from django import template
from users.models import Person, UserType

register = template.Library()


@register.inclusion_tag('header.html')
def show_header(user):
    # TODO: make this tag like show_cabinet_navigation tag
    return {'user': user}


@register.inclusion_tag('user-cabinet-navigation.html')
def show_cabinet_navigation(nav_selected=0):
    cabinet_navigation = [
        {'title': 'Advertising Spaces', 'url': 'user_adv_spaces'},
        {'title': 'Messages', 'url': 'user_messages'},
        {'title': 'Personal data', 'url': 'user_data'},
        {'title': 'Change password', 'url': 'user_change_pass'}
    ]

    return {'cabinet_nav': cabinet_navigation, 'cabinet_nav_selected': nav_selected}
