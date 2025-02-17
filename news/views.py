from django.views.generic import ListView, DetailView, CreateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404
from django.db.models import Q
from django.core.paginator import Paginator
from .models import Article, Category, Comment, Epaper
from django.urls import reverse

class HomeView(ListView):
    model = Article
    template_name = 'news/index.html'
    context_object_name = 'articles'
    paginate_by = 8  # Display 8 articles per page

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['featured_articles'] = Article.objects.filter(
            status='published'
        ).order_by('-created_at')[:3]
        context['trending_articles'] = Article.objects.filter(
            status='published',
            is_trending=True
        )[:5]
        context['latest_articles'] = Article.objects.filter(
            status='published'
        ).order_by('-created_at')[:6]

        # Fetch all categories and their latest articles
        categories_with_latest_articles = []
        for category in Category.objects.all():
            latest_article = category.article_set.filter(status='published').order_by('-created_at').first()
            if latest_article:
                categories_with_latest_articles.append((category, latest_article))
        context['categories_with_latest_articles'] = categories_with_latest_articles

        return context


class CategoryView(ListView):
    model = Article
    template_name = 'news/category.html'
    context_object_name = 'articles'
    paginate_by = 10

    def get_queryset(self):
        self.category = get_object_or_404(Category, slug=self.kwargs['slug'])
        return Article.objects.filter(
            category=self.category,
            status='published'
        ).order_by('-created_at')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['category'] = self.category
        context['trending_articles'] = Article.objects.filter(
            status='published',
            is_trending=True
        )[:5]
        return context

class ArticleDetailView(DetailView):
    model = Article
    template_name = 'news/article_detail.html'
    context_object_name = 'article'

    def get_object(self):
        obj = super().get_object()
        obj.view_count += 1
        obj.save()
        return obj

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['related_articles'] = Article.objects.filter(
            category=self.object.category
        ).exclude(id=self.object.id)[:3]
        context['comments'] = self.object.comments.all()
        return context

class SearchResultsView(ListView):
    model = Article
    template_name = 'news/search_results.html'
    context_object_name = 'articles'
    paginate_by = 10

    def get_queryset(self):
        query = self.request.GET.get('q', '')
        if query:
            return Article.objects.filter(
                Q(title__icontains=query) |
                Q(content__icontains=query),
                status='published'
            ).order_by('-created_at')
        return Article.objects.none()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['query'] = self.request.GET.get('q', '')
        context['trending_articles'] = Article.objects.filter(
            status='published',
            is_trending=True
        )[:5]
        return context

class TrendingArticlesView(ListView):
    model = Article
    template_name = 'news/trending.html'
    context_object_name = 'articles'
    paginate_by = 10

    def get_queryset(self):
        return Article.objects.filter(
            status='published',
            is_trending=True
        ).order_by('-created_at')

class LatestArticlesView(ListView):
    model = Article
    template_name = 'news/latest.html'
    context_object_name = 'articles'
    paginate_by = 10

    def get_queryset(self):
        return Article.objects.filter(
            status='published'
        ).order_by('-created_at')

class AddCommentView(LoginRequiredMixin, CreateView):
    model = Comment
    template_name = 'news/add_comment.html'
    fields = ['content']
    login_url = 'login'

    def form_valid(self, form):
        form.instance.article = get_object_or_404(Article, slug=self.kwargs['slug'])
        form.instance.user = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('news:article_detail', kwargs={'slug': self.object.article.slug})

from django.shortcuts import render

def about(request):
    return render(request, 'news/about.html')

def epaper_list_view(request):
    epapers = Epaper.objects.all().order_by('-date_uploaded')
    paginator = Paginator(epapers, 6)  # Show 6 epapers per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'epaper/epaper_list.html', {'page_obj': page_obj})

def epaper_detail_view(request, pk):
    epaper = get_object_or_404(Epaper, pk=pk)
    return render(request, 'epaper/epaper_detail.html', {'epaper': epaper})
