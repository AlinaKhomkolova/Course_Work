from apscheduler.schedulers.blocking import BlockingScheduler
from django.core.management import BaseCommand

from mailings.models import Mailings
from mailings.services import send_mailing


class Command(BaseCommand):
    def handle(self, *args, **options):
        scheduler = BlockingScheduler()

        # Получаем активные рассылки
        mailings = Mailings.objects.filter(is_active=True)
        for mailing in mailings:
            scheduler.add_job(func=send_mailing, trigger='interval', seconds=mailing.periodicity)

        # Запуск
        scheduler.start()
        self.stdout.write(self.style.SUCCESS('Рассылка запущена.'))
