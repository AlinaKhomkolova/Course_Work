from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
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


class ClientCreateView(LoginRequiredMixin, CreateView):
    model = Client
    template_name = 'mailings/client_form.html'
    form_class = ClientForm
    success_url = reverse_lazy('mailings:home')

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        data['title'] = 'Добавление клиента'
        return data

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            messages.error(request, 'Пожалуйста, войдите в систему или зарегистрируйтесь, чтобы создать клиента.')
            return redirect('users:login')
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        # Привязка пользователя к создаваемому клиенту
        form.instance.owner = self.request.user
        return super().form_valid(form)


class ClientListView(PermissionRequiredMixin, ListView):
    model = Client
    template_name = 'mailings/client_list.html'
    context_object_name = 'clients'
    permission_required = 'mailings.can_view_users'

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

    def dispatch(self, request, *args, **kwargs):
        if not self.has_permission():
            messages.error(request, 'У вас нет доступа к этой странице.')
            return redirect('mailings:home')

        return super().dispatch(request, *args, **kwargs)


class ClientUpdateView(LoginRequiredMixin, UpdateView):
    model = Client
    template_name = 'mailings/client_form.html'
    success_url = reverse_lazy('mailings:client_list')
    form_class = ClientForm

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        data['title'] = 'Изменение клиента'
        return data

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            messages.error(request,
                           'Пожалуйста, войдите в систему или зарегистрируйтесь, чтобы изменить данные клиента.')
            return redirect('users:login')
        obj = self.get_object()
        if obj.owner != self.request.user:
            messages.error(request, "Вы не можете редактировать этого клиента, так как он вам не принадлежит.")
            return redirect('mailings:client_list')

        return super().dispatch(request, *args, **kwargs)

    def get_object(self, queryset=None):
        return super().get_object(queryset)


class ClientDeleteView(LoginRequiredMixin, DeleteView):
    model = Client
    success_url = reverse_lazy('mailings:client_list')

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        data['title'] = 'Удаление клиента'
        return data

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            messages.error(request, 'Пожалуйста, войдите в систему или зарегистрируйтесь, чтобы удалить клиента.')
            return redirect('users:login')
        obj = self.get_object()
        if obj.owner != self.request.user:
            messages.error(request, "Вы не можете удалить этого клиента, так как он вам не принадлежит.")
            return redirect('mailings:client_list')

        return super().dispatch(request, *args, **kwargs)

    def get_object(self, queryset=None):
        return super().get_object(queryset)


class MessageCreateView(LoginRequiredMixin, CreateView):
    model = Message
    form_class = MessageForm
    template_name = 'mailings/message_form.html'
    success_url = reverse_lazy('mailings:home')

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        data['title'] = 'Создание письма'
        return data

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            messages.error(request, 'Пожалуйста, войдите в систему или зарегистрируйтесь, чтобы создать письмо.')
            return redirect('users:login')
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        # Привязка пользователя к создаваемому письму
        form.instance.owner = self.request.user
        return super().form_valid(form)


class MessageListView(ListView):
    model = Message
    template_name = 'mailings/message_list.html'
    context_object_name = 'message_list'

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


class MessageUpdateView(LoginRequiredMixin, UpdateView):
    model = Message
    template_name = 'mailings/message_form.html'
    success_url = reverse_lazy('mailings:message_list')
    form_class = MessageForm

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        data['title'] = 'Изменение письма для рассылки'
        return data

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            messages.error(request, 'Пожалуйста, войдите в систему или зарегистрируйтесь, чтобы изменить письмо.')
            return redirect('users:login')

        obj = self.get_object()
        if obj.owner != self.request.user:
            messages.error(request, "Вы не можете редактировать это письмо, так как он вам не принадлежит.")
            return redirect('mailings:message_list')

        return super().dispatch(request, *args, **kwargs)




class MessageDeleteView(LoginRequiredMixin, DeleteView):
    model = Message
    success_url = reverse_lazy('mailings:message_list')

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        data['title'] = 'Удаление письма для рассылки'
        return data

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            messages.error(request, 'Пожалуйста, войдите в систему или зарегистрируйтесь, чтобы удалить письмо.')
            return redirect('users:login')

        obj = self.get_object()
        if obj.owner != self.request.user:
            messages.error(request, "Вы не можете удалить это письмо, так как он вам не принадлежит.")
            return redirect('mailings:message_list')

        return super().dispatch(request, *args, **kwargs)


class MailingCreateView(LoginRequiredMixin, CreateView):
    model = Mailings
    success_url = reverse_lazy('mailings:home')
    template_name = 'mailings/mailings_form.html'
    form_class = MailingsForm

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        data['title'] = 'Создание рассылки'
        return data

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            messages.error(request, 'Пожалуйста, войдите в систему или зарегистрируйтесь, чтобы создать рассылку.')
            return redirect('users:login')
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        # Привязка пользователя к создаваемой рассылке
        form.instance.owner = self.request.user
        return super().form_valid(form)


class MailingListView(PermissionRequiredMixin, ListView):
    model = Mailings
    template_name = 'mailings/mailings_list.html'
    context_object_name = 'mailings'
    permission_required = 'mailings.can_view_all_mailings'

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

    def dispatch(self, request, *args, **kwargs):
        if not self.has_permission():
            messages.error(request, 'У вас нет доступа к этой странице.')
            return redirect('mailings:home')

        return super().dispatch(request, *args, **kwargs)


class MailingUpdateView(LoginRequiredMixin, UpdateView):
    model = Mailings
    template_name = 'mailings/mailings_form.html'
    success_url = reverse_lazy('mailings:mailings_list')
    form_class = MailingsForm
    permission_required = 'mailings.can_disable_mailings'

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        data['title'] = 'Изменение рассылки'
        return data

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            messages.error(request, 'Пожалуйста, войдите в систему или зарегистрируйтесь, чтобы изменить рассылку.')
            return redirect('users:login')

        obj = self.get_object()
        if obj.owner != self.request.user:
            messages.error(request, "Вы не можете редактировать эту рассылку, так как она вам не принадлежит.")
            return redirect('mailings:mailings_list')

        return super().dispatch(request, *args, **kwargs)

    def get_object(self, queryset=None):
        return super().get_object(queryset)


class MailingDeleteView(LoginRequiredMixin, DeleteView):
    model = Mailings
    success_url = reverse_lazy('mailings:mailings_list')
    permission_required = 'mailings.can_disable_mailings'

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        data['title'] = 'Удаление рассылки'
        return data

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            messages.error(request, 'Пожалуйста, войдите в систему или зарегистрируйтесь, чтобы удалить рассылку.')
            return redirect('users:login')
        obj = self.get_object()
        if obj.owner != self.request.user:
            messages.error(request, "Вы не можете удалить эту рассылку, так как она вам не принадлежит.")
            return redirect('mailings:mailings_list')

        return super().dispatch(request, *args, **kwargs)

    def get_object(self, queryset=None):
        return super().get_object(queryset)


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


class MailingToggleActiveView(PermissionRequiredMixin, View):
    permission_required = 'mailings.can_disable_mailings'

    def get(self, request, pk):
        mailing = Mailings.objects.get(pk=pk)
        mailing.is_active = not mailing.is_active
        mailing.save()
        return redirect('mailings:mailings_detail', pk=pk)

    def dispatch(self, request, *args, **kwargs):
        if not self.has_permission():
            messages.error(request, 'У вас нет доступа к этой странице.')
            return redirect('mailings:mailings_list')

        return super().dispatch(request, *args, **kwargs)


class RunMailingCommandView(PermissionRequiredMixin, View):
    success_url = reverse_lazy('mailings:mailings_list')
    permission_required = 'mailings.can_disable_mailings'

    def get(self, request):
        try:
            call_command('periodic_send')  # вызов команды
            messages.success(request, 'Рассылка успешно запущена!')
        except Exception as e:
            messages.error(request, f'Ошибка при запуске рассылки: {e}')
        return redirect('mailings:mailings_list')

    def dispatch(self, request, *args, **kwargs):
        if not self.has_permission():
            messages.error(request, 'У вас нет доступа к этой странице.')
            return redirect('mailings:mailings_list')

        return super().dispatch(request, *args, **kwargs)

# @permission_required('mailings.can_disable_mailings')
# def disable_mailing(request, mailing_id):
#     mailing = get_object_or_404(Mailings, id=mailing_id)
#     mailing.is_active = False
#     mailing.save()
#     return redirect('view_mailings')  # Перенаправление обратно на список рассылок
#
# @permission_required('mailings.can_block_users')
# def block_client(request, client_id):
#     client = get_object_or_404(User, id=client_id)
#     client.is_active = False  # Блокировка пользователя
#     client.save()
#     return redirect('mailings:client_list')
