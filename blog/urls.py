from django.urls import path
from django.views.decorators.cache import cache_page

from blog.apps import BlogConfig
from blog.views import BlogView

app_name = BlogConfig.name

urlpatterns = [
    path('', cache_page(60)(BlogView.as_view(), name='blog')
]
