from django.urls import path

from mailings.apps import MailingsConfig
from mailings.views import HomeView, ClientCreateView, MessageCreateView, ClientListView, ClientDeleteView, \
    ClientUpdateView, MessageListView, MessageUpdateView, MessageDeleteView

app_name = MailingsConfig.name
urlpatterns = [
    path('', HomeView.as_view(), name='home'),

    path('client_form.html', ClientCreateView.as_view(), name='client_form'),  # Форма для создания клиента
    path('client_list.html', ClientListView.as_view(), name='client_list'),  # Список клиентов
    path('client_delete/<int:pk>/', ClientDeleteView.as_view(), name='client_delete'),  # Удаление клиента
    path('client_update/<int:pk>/', ClientUpdateView.as_view(), name='client_update'),  # Изменение клиента

    path('message_form.html', MessageCreateView.as_view(), name='message_form'),  # Форма для создания письма
    path('message_list.html', MessageListView.as_view(), name='message_list'),  # Список писем для рассылки
    path('message_update/<int:pk>/', MessageUpdateView.as_view(), name='message_update'),  # Изменение письма
    path('message_delete/<int:pk>/', MessageDeleteView.as_view(), name='message_delete'),  # Удаление клиента
]
