from django.contrib import admin
from .models import Program, Schedule

@admin.register(Program)
class ProgramAdmin(admin.ModelAdmin):
    list_display = ('title', 'host', 'is_active')
    list_filter = ('is_active',)
    search_fields = ('title', 'host', 'description')
    fieldsets = (
        ('Program Information', {
            'fields': ('title', 'host', 'description')
        }),
        ('Media', {
            'fields': ('image',)
        }),
        ('Status', {
            'fields': ('is_active',)
        }),
    )

@admin.register(Schedule)
class ScheduleAdmin(admin.ModelAdmin):
    list_display = ('program', 'get_day_display', 'start_time', 'end_time', 'is_active')
    list_filter = ('day_of_week', 'is_active', 'program')
    search_fields = ('program__title',)

    def get_day_display(self, obj):
        return obj.get_day_of_week_display()
    get_day_display.short_description = 'Day'