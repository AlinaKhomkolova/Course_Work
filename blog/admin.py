from django.contrib import admin

from blog.models import Blog


@admin.register(Blog)
class BlogAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'views_count', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('title', 'id',)
    readonly_fields = ('views_count',)
    prepopulated_fields = {'title': ('body',)}

