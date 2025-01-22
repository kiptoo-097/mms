from django.db import models
from django.utils import timezone

class Program(models.Model):
    title = models.CharField(max_length=200)
    host = models.CharField(max_length=100)
    description = models.TextField()
    image = models.ImageField(upload_to='radio/programs/', blank=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.title

    def get_current_schedule(self):
        now = timezone.now()
        return self.schedule_set.filter(
            start_time__lte=now,
            end_time__gte=now
        ).first()

class Schedule(models.Model):
    DAYS_OF_WEEK = [
        (0, 'Monday'),
        (1, 'Tuesday'),
        (2, 'Wednesday'),
        (3, 'Thursday'),
        (4, 'Friday'),
        (5, 'Saturday'),
        (6, 'Sunday'),
    ]

    program = models.ForeignKey(Program, on_delete=models.CASCADE)
    day_of_week = models.IntegerField(choices=DAYS_OF_WEEK)
    start_time = models.TimeField()
    end_time = models.TimeField()
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ['day_of_week', 'start_time']

    def __str__(self):
        return f"{self.get_day_of_week_display()} - {self.program.title}"

    def is_current(self):
        now = timezone.now()
        return (
            now.weekday() == self.day_of_week and
            self.start_time <= now.time() <= self.end_time
        )