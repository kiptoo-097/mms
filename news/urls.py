from django.urls import path
from . import views

app_name = 'news'

urlpatterns = [
    path('', views.HomeView.as_view(), name='home'),
    path('category/<slug:slug>/', views.CategoryView.as_view(), name='category'),
    path('article/<slug:slug>/', views.ArticleDetailView.as_view(), name='article_detail'),
    path('article/<slug:slug>/comment/', views.AddCommentView.as_view(), name='add_comment'),
    path('search/', views.SearchResultsView.as_view(), name='search'),
    path('trending/', views.TrendingArticlesView.as_view(), name='trending'),
    path('latest/', views.LatestArticlesView.as_view(), name='latest'),
    path('categories/', views.CategoryListView.as_view(), name='category_list'),
]