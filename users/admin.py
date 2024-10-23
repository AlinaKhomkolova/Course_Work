from django.contrib import admin

from mailings.models import Client, Mailings, Message
from users.models import User

admin.site.register(User)


class MailingAdmin(admin.ModelAdmin):
    list_display = ('title', 'owner', 'is_active')
