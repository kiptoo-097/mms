from django.views.generic import ListView, DetailView, CreateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from .models import Article, Category, Comment

class ArticleListView(ListView):
    model = Article
    template_name = 'news/article_list.html'
    context_object_name = 'articles'
    paginate_by = 10

    def get_queryset(self):
        return Article.objects.filter(status='published').order_by('-created_at')

class CategoryArticleListView(ListView):
    model = Article
    template_name = 'news/category_articles.html'
    context_object_name = 'articles'
    paginate_by = 10

    def get_queryset(self):
        self.category = get_object_or_404(Category, slug=self.kwargs['category_slug'])
        return Article.objects.filter(category=self.category, status='published')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['category'] = self.category
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
        context['comments'] = self.object.comments.all()
        return context

class TrendingArticlesView(ListView):
    model = Article
    template_name = 'news/trending_articles.html'
    context_object_name = 'articles'

    def get_queryset(self):
        return Article.objects.filter(status='published', is_trending=True)

class LatestArticlesView(ListView):
    model = Article
    template_name = 'news/latest_articles.html'
    context_object_name = 'articles'
    paginate_by = 10

    def get_queryset(self):
        return Article.objects.filter(status='published').order_by('-created_at')

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
        return reverse_lazy('news:article_detail', kwargs={'slug': self.kwargs['slug']})