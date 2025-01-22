from django.views.generic import TemplateView, ListView
from django.utils import timezone
from .models import Program, Schedule

class RadioPlayerView(TemplateView):
    template_name = 'radio/player.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        now = timezone.now()
        
        context.update({
            'current_program': Program.objects.filter(
                schedule__day_of_week=now.weekday(),
                schedule__start_time__lte=now.time(),
                schedule__end_time__gte=now.time(),
                schedule__is_active=True
            ).first(),
            
            'daily_schedule': Schedule.objects.filter(
                day_of_week=now.weekday(),
                is_active=True
            ).order_by('start_time'),
            
            'radio_stream_url': 'https://stream.mestowotnews.com/live'
        })
        return context

class ScheduleView(ListView):
    model = Schedule
    template_name = 'radio/schedule.html'
    context_object_name = 'schedules'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['days'] = [
            'Monday', 'Tuesday', 'Wednesday', 
            'Thursday', 'Friday', 'Saturday', 'Sunday'
        ]
        context['current_day'] = timezone.now().weekday()
        return context

    def get_queryset(self):
        return Schedule.objects.filter(
            is_active=True
        ).order_by('day_of_week', 'start_time')