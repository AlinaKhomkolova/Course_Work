import smtplib
from datetime import timedelta

from django.core.mail import send_mail

from config import settings
from mailings.models import Mailings, MailingAttempt


def send_mailing():
    # Получаем активные рассылки
    mailings = Mailings.objects.filter(is_active=True)

    for mailing in mailings:
        # Получаем список email-ов клиентов
        emails_list = mailing.client.values_list('email', flat=True)
        for client in mailing.client.all():
            try:
                # Отправка сообщения через Django send_mail
                response = send_mail(subject=mailing.message.title,
                                     message=mailing.message.body,
                                     from_email=settings.EMAIL_HOST_USER,
                                     recipient_list=[client.email],
                                     fail_silently=False)
                # Если отправка успешна, создаем запись в MailingAttempt
                MailingAttempt.objects.create(
                    mail_service_response='Сообщение доставлено',
                    status='successfully',
                    mailing=mailing,
                    client=client
                )
            except smtplib.SMTPException as e:
                # Если произошла ошибка, записываем это в MailingAttempt
                MailingAttempt.objects.create(
                    mail_service_response=str(e),
                    status='fail',
                    mailing=mailing,
                    client=client
                )

            # Обновляем статус рассылки
            if mailing.status == 'created':
                mailing.status = 'launched'

            # Обновляем время следующей отправки
            mailing.next_send_date_time += timedelta(seconds=mailing.periodicity)

            # Если рассылка завершена, меняем ее статус
            if mailing.last_send_date_time and mailing.next_send_date_time > mailing.last_send_date_time:
                mailing.status = 'completed'

            # Сохраняем изменения в рассылке
            mailing.save()
