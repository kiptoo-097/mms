from django.urls import path
from . import views

app_name = 'news'

urlpatterns = [
    path('', views.ArticleListView.as_view(), name='article_list'),
    path('category/<slug:category_slug>/', views.CategoryArticleListView.as_view(), name='category_articles'),
    path('article/<slug:slug>/', views.ArticleDetailView.as_view(), name='article_detail'),
    path('trending/', views.TrendingArticlesView.as_view(), name='trending_articles'),
    path('latest/', views.LatestArticlesView.as_view(), name='latest_articles'),
    path('article/<slug:slug>/comment/', views.AddCommentView.as_view(), name='add_comment'),
]