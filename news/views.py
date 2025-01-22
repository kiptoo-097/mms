from django.views.generic import ListView, DetailView, CreateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404
from django.db.models import Q
from .models import Article, Category, Comment

class HomeView(ListView):
    model = Article
    template_name = 'news/index.html'
    context_object_name = 'articles'
    paginate_by = 12

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
        context['categories'] = Category.objects.all()
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
        return self.object.article.get_absolute_url()