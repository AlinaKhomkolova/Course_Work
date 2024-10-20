from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, DeleteView, UpdateView

from mailings.forms import ClientForm, MessageForm
from mailings.models import Client, Message


class HomeView(ListView):
    model = Client
    template_name = 'mailings/home.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        data = super().get_context_data(**kwargs)
        data['title'] = 'Главная'
        return data


class ClientCreateView(CreateView):
    model = Client
    template_name = 'mailings/client_form.html'
    form_class = ClientForm
    success_url = reverse_lazy('mailings:home')

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        data['title'] = 'Добавление клиента'
        return data


class ClientListView(ListView):
    model = Client
    template_name = 'mailings/client_list.html'
    context_object_name = 'clients'

    def get_queryset(self):
        queryset = super().get_queryset()
        client_id = self.request.GET.get('client')
        if client_id:
            queryset = queryset.filter(client_id=client_id)
        return queryset

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        data['title'] = 'Список клиентов'
        return data


class ClientUpdateView(UpdateView):
    model = Client
    template_name = 'mailings/client_form.html'
    success_url = reverse_lazy('mailings:client_list')
    form_class = ClientForm

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        data['title'] = 'Изменение клиента'
        return data


class ClientDeleteView(DeleteView):
    model = Client
    success_url = reverse_lazy('mailings:client_list')

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        data['title'] = 'Удаление клиента'
        return data


class MessageCreateView(CreateView):
    model = Message
    form_class = MessageForm
    template_name = 'mailings/message_form.html'
    success_url = reverse_lazy('mailings:home')

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        data['title'] = 'Создание письма'
        return data


class MessageListView(ListView):
    model = Message
    template_name = 'mailings/message_list.html'
    context_object_name = 'messages'

    def get_queryset(self):
        queryset = super().get_queryset()
        message_id = self.request.GET.get('client')
        if message_id:
            queryset = queryset.filter(message_id=message_id)
        return queryset

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        data['title'] = 'Список писем для рассылки'
        return data


class MessageUpdateView(UpdateView):
    model = Message
    template_name = 'mailings/message_form.html'
    success_url = reverse_lazy('mailings:message_list')
    form_class = MessageForm

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        data['title'] = 'Изменение письма для рассылки'
        return data


class MessageDeleteView(DeleteView):
    model = Message
    success_url = reverse_lazy('mailings:message_list')

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        data['title'] = 'Удаление письма для рассылки'
        return data
