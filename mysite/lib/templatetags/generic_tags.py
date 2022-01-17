from django import template

register = template.Library()


@register.inclusion_tag('header.html')
def show_header(user):
    return {'user': user}


@register.inclusion_tag('user-cabinet-sidebar.html')
def show_sidebar(user):
    return {'user': user}
