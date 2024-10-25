from django.db import models

from mailings.common import NULLABLE
from users.models import User


class Client(models.Model):
    email = models.EmailField(verbose_name='Email', help_text='Введите email')
    full_name = models.CharField(max_length=150, verbose_name='Ф.И.О', help_text='Введите ФИО')
    comment = models.TextField(**NULLABLE, verbose_name='Комментарий', help_text='Введите комментарий')

    owner = models.ForeignKey(User, **NULLABLE, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.email}'

    class Meta:
        verbose_name = 'Клиент'
        verbose_name_plural = 'Клиенты'
        ordering = ('email',)


class Message(models.Model):
    title = models.CharField(max_length=150, verbose_name='Тема письма', help_text='Введите тему письма')
    body = models.TextField(verbose_name='Тела письма', help_text='Введите содержание письма')

    owner = models.ForeignKey(User, **NULLABLE, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.title}'

    class Meta:
        verbose_name = 'Сообщение для рассылки'
        verbose_name_plural = 'Сообщения для рассылки'
        ordering = ('title',)


class Mailings(models.Model):
    PERIODICITY = [
        (60, 'Раз в минуту'),
        (300, 'Раз в 5 минут'),
        (600, 'Раз в 10 минут'),
        (3600, 'Раз в час'),
    ]
    STATUS = [
        ('completed', 'завершена'),
        ('created', 'создана'),
        ('launched', 'запущена'),
    ]

    date_first_dispatch = models.DateTimeField(**NULLABLE, verbose_name='Дата и время первой отправки')
    periodicity = models.IntegerField(choices=PERIODICITY, verbose_name='Периодичность')
    status = models.CharField(max_length=15, choices=STATUS, default='created', verbose_name='Статус рассылки')
    is_active = models.BooleanField(default=True, verbose_name='Активна ли рассылка')
    next_send_date_time = models.DateTimeField(auto_now_add=True, verbose_name='Дата и время следующей отправки')
    last_send_date_time = models.DateTimeField(auto_now=True, verbose_name='Дата и время последней отправки')

    # Связи с другими моделями
    message = models.ForeignKey(Message, related_name='mailings', on_delete=models.CASCADE, verbose_name='Сообщение')
    clients = models.ManyToManyField(Client, related_name='mailings', verbose_name='Клиенты')

    owner = models.ForeignKey(User, **NULLABLE, on_delete=models.CASCADE)

    def __str__(self):
        return f'Рассылка ({self.status}) от {self.date_first_dispatch}'

    class Meta:
        verbose_name = 'Рассылка'
        verbose_name_plural = 'Рассылки'
        ordering = ('date_first_dispatch',)

        permissions = [
            ("can_view_all_mailings", "Can view all mailings"),
            ("can_view_users", "Can view all users"),
            ("can_block_users", "Can block users"),
            ("can_disable_mailings", "Can disable mailings"),
        ]


class MailingAttempt(models.Model):
    STATUS = [
        ('successfully', 'успешно'),
        ('fail', 'не успешно'),
    ]
    date_last_dispatch = models.DateTimeField(auto_now=True, verbose_name='Дата и время последней попытки')
    status = models.CharField(max_length=15, choices=STATUS, verbose_name='Статус попытки')
    mail_service_response = models.CharField(max_length=250, **NULLABLE, verbose_name='Ответ почтового сервиса')

    # Связь с рассылкой
    mailing = models.ForeignKey(Mailings, on_delete=models.CASCADE, related_name='mailing_attempts', verbose_name='Рассылки')
    client = models.ForeignKey(Client, on_delete=models.CASCADE, **NULLABLE, related_name='mailing_attempts')

    def __str__(self):
        return f'Попытка ({self.status})'

    class Meta:
        verbose_name = 'Попытка рассылки'
        verbose_name_plural = 'Попытки рассылки:'
        ordering = ('status',)
