from django.contrib import admin
from .models import User
from django.contrib.auth.admin import UserAdmin
class UserAdmin(UserAdmin):
    list_display = ['email', 'username', 'first_name', 'last_name', 'phone', 'is_active']
    list_display_links = ['username', 'email']
    readonly_fields = ('last_login', 'date_joined',)
    ordering = ('-date_joined',)
    filter_horizontal = ()
    list_filter = ()
    fieldsets = ()

admin.site.register(User, UserAdmin)

