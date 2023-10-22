from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.admin import UserAdmin

from .models import User, PChat, PMessage


@admin.register(User)
class MyUserAdmin(UserAdmin):
    """
    Custom admin class to add extend OG class
    """
    fieldsets = UserAdmin.fieldsets + \
        ((_('Customs'), {'fields': ('bio', 'photo')}),)


admin.site.register(PChat)
admin.site.register(PMessage)
