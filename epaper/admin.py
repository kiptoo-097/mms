from django.contrib import admin
from django.utils.text import slugify
from .models import Epaper

@admin.register(Epaper)
class EpaperAdmin(admin.ModelAdmin):
    list_display = ('title', 'publication_date', 'is_active', 'view_count')
    list_filter = ('publication_date', 'is_active')
    search_fields = ('title',)
    prepopulated_fields = {'slug': ('title',)}
    date_hierarchy = 'publication_date'
    readonly_fields = ('view_count', 'created_at')
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('title', 'slug', 'publication_date')
        }),
        ('Content', {
            'fields': ('pdf_file',)
        }),
        ('Status', {
            'fields': ('is_active',)
        }),
        ('Statistics', {
            'fields': ('view_count', 'created_at'),
            'classes': ('collapse',)
        }),
    )

    def save_model(self, request, obj, form, change):
        if not obj.slug:
            obj.slug = slugify(obj.title)
        super().save_model(request, obj, form, change)