from django.contrib import admin
from .models import User, Person


class PersonInline(admin.TabularInline):
    model = Person


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ("id", "email", "last_login", "date_joined", "is_active")
    inlines = [
        PersonInline,
    ]

