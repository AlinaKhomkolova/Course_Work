from random import sample

from django.views.generic import TemplateView

from blog.models import Blog
from mailings.models import Mailings, Client


class BlogView(TemplateView):
    template_name = 'blog/blog_home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Статистика рассылок
        total_mailings = Mailings.objects.count()
        active_mailings = Mailings.objects.filter(is_active=True).count()
        unique_clients = Client.objects.distinct().count()

        # Случайные три статьи из блога
        blog_posts = list(Blog.objects.all())
        random_posts = sample(blog_posts, 3) if len(blog_posts) >= 3 else blog_posts

        context.update({
            'title': 'Главная страница блога',
            'total_mailings': total_mailings,
            'active_mailings': active_mailings,
            'unique_clients': unique_clients,
            'random_posts': random_posts,
        })
        context['title'] = 'Главная страница блога'
        return context
