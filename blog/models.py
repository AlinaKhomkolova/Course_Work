from django.db import models

from mailings.common import NULLABLE


class Blog(models.Model):
    title = models.CharField(max_length=200, verbose_name='Заголовок')
    body = models.TextField(verbose_name='Содержимое')

    image = models.ImageField(upload_to='images_blog/', verbose_name='Изображение (превью)', **NULLABLE)
    views_count = models.IntegerField(default=0, verbose_name='Количество просмотров')
    created_at = models.DateField(auto_now_add=True, verbose_name='Дата создания')
    is_published = models.BooleanField(default=True, verbose_name='Опубликовано')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Пост'
        verbose_name_plural = 'Посты'
        ordering = ('created_at',)