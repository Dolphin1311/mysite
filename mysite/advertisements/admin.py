from django.contrib import admin
from .models import AdvertisingSpace, AdvertisingSpaceType


class AdvertisingSpaceAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'description', 'slug', 'data', 'user')
    # list_display_links = ('id', 'title')
    # search_fields = ('title', 'content')
    # list_editable = ('is_published',)
    # list_filter = ('is_published', 'time_created')
    # prepopulated_fields = {'slug': ('title',)}


class AdvertisingSpaceTypeAdmin(admin.ModelAdmin):
    list_display = ('id',)


admin.site.register(AdvertisingSpace)
admin.site.register(AdvertisingSpaceType, AdvertisingSpaceTypeAdmin)
