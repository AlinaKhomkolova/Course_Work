from django.urls import path

from mailings.apps import MailingsConfig
from mailings.views import HomeView, ClientCreateView, MessageCreateView, ClientListView, ClientDeleteView, \
    ClientUpdateView, MessageListView, MessageUpdateView, MessageDeleteView, MailingCreateView, MailingListView, \
    MailingDeleteView, MailingUpdateView, MailingDetailView, MailingToggleActiveView, RunMailingCommandView


app_name = MailingsConfig.name
urlpatterns = [
    path('', HomeView.as_view(), name='home'),

    path('client_form.html', ClientCreateView.as_view(), name='client_form'),  # Форма для создания клиента
    path('client_list.html', ClientListView.as_view(), name='client_list'),  # Список клиентов
    path('client_update/<int:pk>/', ClientUpdateView.as_view(), name='client_update'),  # Изменение клиента
    path('client_delete/<int:pk>/', ClientDeleteView.as_view(), name='client_delete'),  # Удаление клиента

    path('message_form.html', MessageCreateView.as_view(), name='message_form'),  # Форма для создания письма
    path('message_list.html', MessageListView.as_view(), name='message_list'),  # Список писем для рассылки
    path('message_update/<int:pk>/', MessageUpdateView.as_view(), name='message_update'),  # Изменение письма
    path('message_delete/<int:pk>/', MessageDeleteView.as_view(), name='message_delete'),  # Удаление клиента

    path('mailings_form.html', MailingCreateView.as_view(), name='mailings_form'),  # Форма для создания рассылки
    path('mailings_list.html', MailingListView.as_view(), name='mailings_list'),  # Список рассылок
    path('mailings_update/<int:pk>/', MailingUpdateView.as_view(), name='mailings_update'),  # Изменение рассылок
    path('mailings_delete/<int:pk>/', MailingDeleteView.as_view(), name='mailings_delete'),  # Удаление рассылок
    path('mailings_detail/<int:pk>/', MailingDetailView.as_view(), name='mailings_detail'),  # Просмотр рассылки

    path('<int:pk>/toggle-active/', MailingToggleActiveView.as_view(), name='mailings_toggle_active'),
    # Активация рассылки
    path('run-mailings/', RunMailingCommandView.as_view(), name='run_mailings'),  # Запуск рассылки

    # path('block_user/<int:pk>/', block_user, name='block_user'),
    # path('disable_mailing/<int:pk>/', disable_mailing, name='disable_mailing'),
]
