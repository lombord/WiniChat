from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.admin import UserAdmin

from .models import (User, PChat, PMessage, MessageFile, Group, GroupRole,
                     GroupMember, GroupBan, GroupMessage, GroupMessageFile)


@admin.register(User)
class MyUserAdmin(UserAdmin):
    """
    Custom admin class to add extend OG class
    """
    fieldsets = UserAdmin.fieldsets + \
        ((_('Customs'), {'fields': ('bio', 'photo')}),)


admin.site.register(PChat)
admin.site.register(PMessage)
admin.site.register(MessageFile)
admin.site.register(Group)
admin.site.register(GroupRole)
admin.site.register(GroupMember)
admin.site.register(GroupBan)
admin.site.register(GroupMessage)
admin.site.register(GroupMessageFile)
