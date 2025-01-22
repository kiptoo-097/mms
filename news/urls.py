from django.urls import path
from . import views

app_name = 'news'

urlpatterns = [
    # Homepage
    path('', views.HomeView.as_view(), name='home'),
    
    # Categories
    path('category/<slug:slug>/', views.CategoryView.as_view(), name='category'),
    
    # Articles
    path('article/<slug:slug>/', views.ArticleDetailView.as_view(), name='article_detail'),
    path('article/<slug:slug>/comment/', views.AddCommentView.as_view(), name='add_comment'),
    
    # Article Listings
    path('trending/', views.TrendingArticlesView.as_view(), name='trending'),
    path('latest/', views.LatestArticlesView.as_view(), name='latest'),
    
    # Search
    path('search/', views.SearchResultsView.as_view(), name='search'),
]