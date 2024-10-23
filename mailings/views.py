from django.contrib import messages
from django.core.management import call_command
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import ListView, CreateView, DeleteView, UpdateView, DetailView

from mailings.forms import ClientForm, MessageForm, MailingsForm
from mailings.models import Client, Message, Mailings


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


class MailingCreateView(CreateView):
    model = Mailings
    success_url = reverse_lazy('mailings:home')
    template_name = 'mailings/mailings_form.html'
    form_class = MailingsForm

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        data['title'] = 'Создание рассылки'
        return data


class MailingListView(ListView):
    model = Mailings
    template_name = 'mailings/mailings_list.html'
    context_object_name = 'mailings'

    def get_queryset(self):
        queryset = super().get_queryset()
        mailing_id = self.request.GET.get('mailing')
        if mailing_id:
            queryset = queryset.filter(mailing_id=mailing_id)
        return queryset

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        data['title'] = 'Список рассылок'
        return data


class MailingUpdateView(UpdateView):
    model = Mailings
    template_name = 'mailings/mailings_form.html'
    success_url = reverse_lazy('mailings:mailings_list')
    form_class = MailingsForm

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        data['title'] = 'Изменение рассылки'
        return data


class MailingDeleteView(DeleteView):
    model = Mailings
    success_url = reverse_lazy('mailings:mailings_list')

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        data['title'] = 'Удаление рассылки'
        return data


class MailingDetailView(DetailView):
    model = Mailings
    context_object_name = 'mailing'
    template_name = 'mailings/mailings_detail.html'

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        data['clients'] = self.object.client.all()  # Все клиенты, связанные с этой рассылкой
        data['mailing_attempts'] = self.object.mailings.all()  # Все попытки для этой рассылки
        data['title'] = 'Описание рассылки'

        return data


class MailingToggleActiveView(View):
    def get(self, request, pk):
        mailing = Mailings.objects.get(pk=pk)
        mailing.is_active = not mailing.is_active
        mailing.save()
        return redirect('mailings:mailings_detail', pk=pk)


class RunMailingCommandView(View):
    success_url = reverse_lazy('mailings:mailings_list')

    def get(self, request):
        try:
            call_command('periodic_send')  # вызов команды
            messages.success(request, 'Рассылка успешно запущена!')
        except Exception as e:
            messages.error(request, f'Ошибка при запуске рассылки: {e}')
        return redirect('mailings:mailings_list')
