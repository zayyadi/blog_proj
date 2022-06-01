
from django.contrib.sitemaps import Sitemap
from django.urls import reverse

from .models import Article


class PostSitemap(Sitemap):
    changefreq = "weekly"
    priority = 0.8

    def items(self):
        return Article.objects.filter(status=1)

    def lastmod(self, obj):
        return obj.updated_on

    def location(self, item):
        return reverse(item)