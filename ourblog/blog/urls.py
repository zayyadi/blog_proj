from django.urls import path

from blog import views
from .feeds import LatestPostsFeed, AtomSiteNewsFeed


urlpatterns=[
    path("feed/rss", LatestPostsFeed(), name="post_feed"),
    path("feed/atom", AtomSiteNewsFeed()),
    # path("", IndexView.as_view(), name='index'),
    #path('article/<int:pk>/', ArticleDetailView.as_view(), name='article-detail'),
    path('dashboard/',views.dashboard,name = "dashboard"),
    path('addarticle/',views.addArticle,name = "addarticle"),
    path('article/<slug:slug>/',views.detail,name = "detail"),
    path('update/<slug:slug>',views.updateArticle,name = "update"),
    path('delete/<slug:slug>',views.deleteArticle,name = "delete"),
    path('',views.articles,name = "articles"),
    path('comment/<slug:slug>',views.addComment,name = "comment"),
]