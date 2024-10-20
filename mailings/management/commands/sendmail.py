from django.core.mail import send_mail
from django.core.management import BaseCommand

from config import settings
from mailings.models import Mailings


class Command(BaseCommand):
    def handle(self, *args, **options):
        mailings = Mailings.objects.filter(status__in=['created'])

        for mailing in mailings:
            for client in mailing.clients.all():
                response = send_mail(subject=mailing.message.title,
                                     message=mailing.message.body,
                                     from_email=settings.EMAIL_HOST_USER,
                                     recipient_list=[client.email],
                                     fail_silently=False)
