import secrets
from django.urls import reverse

from django.core.mail import send_mail
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView

from config.settings import DEFAULT_FROM_EMAIL
from users.forms import UserRegisterForm
from users.models import User


class RegisterView(CreateView):
    model = User
    form_class = UserRegisterForm
    template_name = 'users/register.html'
    success_url = reverse_lazy('users:login')

    def form_valid(self, form):
        user = form.save(commit=False)
        user.is_active = False
        token = secrets.token_hex(16)
        user_token = token
        user.token = user_token
        host = self.request.get_host()
        url = f'http://{host}/users/email-confirm/{user_token}/'
        user.save()

        try:
            send_mail(
                subject='Подтверждение',
                message=f'Привет, чтобы подтвердить свою почту перейди по ссылке {url}\n',
                from_email=DEFAULT_FROM_EMAIL,
                recipient_list=[user.email],
            )
        except Exception as e:
            print(f"Ошибка при отправке письма: {e}")

        return super().form_valid(form)


def email_verification(request, token):
    user = get_object_or_404(User, token=token)
    user.is_active = True
    user.save()
    return redirect(reverse('users:login'))
