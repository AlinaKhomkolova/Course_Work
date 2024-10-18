from django.db import models

from mailings.common import NULLABLE


class Client(models.Model):
    email = models.EmailField(verbose_name='Email', help_text='Введите email')
    full_name = models.CharField(max_length=150, verbose_name='Ф.И.О', help_text='Введите ФИО')
    comment = models.TextField(**NULLABLE, verbose_name='Комментарий', help_text='Введите комментарий')

    def __str__(self):
        return f'{self.email}'

    class Meta:
        verbose_name = 'Клиент'
        verbose_name_plural = 'Клиенты'
        ordering = ('email',)


class Message(models.Model):
    title = models.CharField(max_length=150, verbose_name='Тема письма', help_text='Введите тему письма')
    body = models.TextField(verbose_name='Тела письма', help_text='Введите содержание письма')

    def __str__(self):
        return f'{self.title}'

    class Meta:
        verbose_name = 'Сообщение для рассылки'
        verbose_name_plural = 'Сообщения для рассылки'
        ordering = ('title',)


class Mailings(models.Model):
    PERIODICITY = [
        ('once_per_minute', 'Раз в минуту'),
        ('once_a_day', 'Раз в день'),
        ('once_a_week', 'раз в неделю'),
        ('once_a_month', 'раз в месяц'),
    ]
    STATUS = [
        ('completed', 'завершена'),
        ('created', 'создана'),
        ('launched', 'запущена'),
    ]

    date_first_dispatch = models.DateTimeField(auto_now_add=True, verbose_name='Дата и время последней отправки')
    periodicity = models.CharField(max_length=15, choices=PERIODICITY, verbose_name='Периодичность')
    status = models.CharField(max_length=15, choices=STATUS, verbose_name='Статус рассылки')

    # Связи с другими моделями
    message = models.ForeignKey(Message, related_name='mailings', on_delete=models.CASCADE, verbose_name='Сообщение')
    client = models.ManyToManyField(Client, related_name='mailings', verbose_name='Клиенты')

    def __str__(self):
        return f'Рассылка ({self.status}) от {self.date_first_dispatch}'

    class Meta:
        verbose_name = 'Рассылка'
        verbose_name_plural = 'Рассылки'
        ordering = ('date_first_dispatch',)


class MailingAttempt(models.Model):
    STATUS = [
        ('successfully', 'успешно'),
        ('fail', 'не успешно'),
    ]
    date_last_dispatch = models.DateTimeField(auto_now=True, verbose_name='Дата и время последней попытки')
    status = models.CharField(max_length=15, choices=STATUS, verbose_name='Статус попытки')
    mail_service_response = models.CharField(max_length=250, **NULLABLE, verbose_name='Ответ почтового сервиса')

    # Связь с рассылкой
    mailing = models.ForeignKey(Mailings, on_delete=models.CASCADE, related_name='mailings', verbose_name='Рассылки')

    def __str__(self):
        return f'Попытка ({self.status})'

    class Meta:
        verbose_name = 'Попытка рассылки'
        verbose_name_plural = 'Попытки рассылки:'
        ordering = ('status',)
