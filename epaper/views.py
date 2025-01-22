from django.views.generic import ListView, DetailView
from django.http import FileResponse
from django.shortcuts import get_object_or_404
from .models import Epaper

class EpaperListView(ListView):
    model = Epaper
    template_name = 'epaper/list.html'
    context_object_name = 'papers'
    paginate_by = 12
    ordering = ['-publication_date']

    def get_queryset(self):
        return Epaper.objects.filter(is_active=True)

class EpaperDetailView(DetailView):
    model = Epaper
    template_name = 'epaper/viewer.html'
    context_object_name = 'paper'

    def get_object(self):
        obj = super().get_object()
        obj.view_count += 1
        obj.save()
        return obj

def epaper_download(request, slug):
    paper = get_object_or_404(Epaper, slug=slug)
    response = FileResponse(paper.pdf_file, as_attachment=True)
    response['Content-Disposition'] = f'attachment; filename="{paper.title}.pdf"'
    return response