from django.contrib import admin
from .models import Category, Article, Comment, Epaper

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug']
    prepopulated_fields = {'slug': ('name',)}

@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = ['title', 'author', 'category', 'status', 'created_at', 'is_trending']
    list_filter = ['status', 'created_at', 'category', 'is_trending']
    search_fields = ['title', 'content']
    prepopulated_fields = {'slug': ('title',)}
    raw_id_fields = ['author']
    date_hierarchy = 'created_at'
    list_editable = ['status', 'is_trending']

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ['user', 'article', 'created_at']
    list_filter = ['created_at']
    search_fields = ['content', 'user__username']

@admin.register(Epaper)
class EpaperAdmin(admin.ModelAdmin):
    list_display = ['title', 'date_uploaded']
    search_fields = ['title']
