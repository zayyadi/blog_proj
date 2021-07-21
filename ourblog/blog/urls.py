from django.urls import path

from .views import IndexView, ArticleCreateView, article_post, PostUpdateView, PostDeleteView
from .feeds import LatestPostsFeed, AtomSiteNewsFeed


urlpatterns=[
    path("feed/rss", LatestPostsFeed(), name="post_feed"),
    path("feed/atom", AtomSiteNewsFeed()),
    path("", IndexView.as_view(), name='index'),
    #path('article/<int:pk>/', ArticleDetailView.as_view(), name='article-detail'),
    path('<int:pk>/', article_post, name='article-post'),
    path('article/new', ArticleCreateView.as_view(), name='new-article'),
    path('article/<int:pk>/update/', PostUpdateView.as_view(), name='article-update'),
    path('article/<int:pk>/delete/', PostDeleteView.as_view(), name='article-delete'),
]