from django import template

register = template.Library()


@register.inclusion_tag('users/user_cabinet_navigation.html')
def show_cabinet_navigation(nav_selected=0):
    cabinet_navigation = [
        {'title': 'Advertising Spaces', 'url': 'user_cabinet'},
        {'title': 'Orders', 'url': 'user_orders'},
        {'title': 'Personal data', 'url': 'user_data'},
        {'title': 'Change password', 'url': 'user_change_pass'}
    ]

    return {'cabinet_nav': cabinet_navigation, 'cabinet_nav_selected': nav_selected}
