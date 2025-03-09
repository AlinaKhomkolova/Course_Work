from django.contrib import admin

from mailings.models import Client, Message, Mailings


@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = ('id', 'email', 'full_name', 'comment',)
    list_filter = ('id',)
    search_fields = ('email', 'full_name',)


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'body',)
    list_filter = ('id',)
    search_fields = ('title',)


@admin.register(Mailings)
class MailingsAdmin(admin.ModelAdmin):
    list_display = ('id', 'periodicity', 'date_first_dispatch',)
    list_filter = ('id',)
    search_fields = ('client', 'message')
    permission = [
        ('can_view_all_mailings', 'Can view all mailings'),
        ('can_view_users', 'Can view all users'),
        ('can_block_users', 'Can block users'),
        ('can_disable_mailings', 'Can disable mailings'),
    ]
    class Meta:
        permissions = [
            ("can_view_all_mailings", "Can view all mailings"),
            ("can_view_users", "Can view all users"),
            ("can_block_users", "Can block users"),
            ("can_disable_mailings", "Can disable mailings"),
        ]
