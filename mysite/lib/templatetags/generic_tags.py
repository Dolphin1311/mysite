from django import template

register = template.Library()


@register.inclusion_tag('header.html')
def show_header(user):
    # TODO: make this tag like show_cabinet_navigation tag
    return {'user': user}
