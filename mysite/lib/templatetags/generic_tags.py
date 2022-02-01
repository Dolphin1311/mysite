from django import template
from users.models import Person, UserType

register = template.Library()


@register.inclusion_tag('header.html')
def show_header(user):
    return {'user': user}


@register.inclusion_tag('user-cabinet-sidebar.html')
def show_sidebar(user):
    # check if user is person type
    if user.user_type == UserType.objects.get(pk=2):
        person = Person.objects.get(user=user)
        return {'person_name': person.first_name, 'person_lastname': person.last_name}
    else:
        return {'user': user}
