from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group, Permission

class Command(BaseCommand):
    help = 'Create manager group and assign permissions'

    def handle(self, *args, **kwargs):
        group, created = Group.objects.get_or_create(name='Managers')

        permissions = [
            'can_view_all_mailings',
            'can_view_users',
            'can_block_users',
            'can_disable_mailings',
        ]

        for perm in permissions:
            permission = Permission.objects.get(codename=perm)
            group.permissions.add(permission)

        self.stdout.write(self.style.SUCCESS('Successfully created Managers group and assigned permissions.'))
