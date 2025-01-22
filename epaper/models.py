from django.db import models
from django.urls import reverse
from django.utils.text import slugify

class Epaper(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    pdf_file = models.FileField(upload_to='epapers/%Y/%m/')
    publication_date = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)
    view_count = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['-publication_date']
        verbose_name = 'E-Paper'
        verbose_name_plural = 'E-Papers'

    def __str__(self):
        return f"{self.title} - {self.publication_date}"

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('epaper:detail', kwargs={'slug': self.slug})

    def increment_view_count(self):
        self.view_count += 1
        self.save()