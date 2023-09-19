from django.contrib import admin
from .models import User, Profile
from django.contrib.auth.admin import UserAdmin
from django.utils.html import format_html
class UserAdmin(UserAdmin):
    list_display = ['email', 'username', 'first_name', 'last_name', 'phone', 'is_active']
    list_display_links = ['username', 'email']
    readonly_fields = ('last_login', 'date_joined',)
    ordering = ('-date_joined',)
    filter_horizontal = ()
    list_filter = ()
    fieldsets = ()


class ProfileAdmin(admin.ModelAdmin):
    def thumbnail(self, object):
        return format_html('<img src="{}" width="30", style="border-radius:50%;">'.format(object.profile_image.url))
    thumbnail.short_description = 'Profile Picture'
    list_display = ['thumbnail', 'user', 'address_line_1', 'address_line_2', 'city', 'state', 'country']
    list_display_links = ['user']

admin.site.register(User, UserAdmin)
admin.site.register(Profile, ProfileAdmin)

