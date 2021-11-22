from django.contrib import admin
from .models import *


class PersonInline(admin.TabularInline):
    model = Person


class UserAdmin(admin.ModelAdmin):
    list_display = ('id', 'email', 'username', 'last_login', 'date_joined', 'is_active')
    inlines = [
        PersonInline,
    ]


admin.site.register(User, UserAdmin)
