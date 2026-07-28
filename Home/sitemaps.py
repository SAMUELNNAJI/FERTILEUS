from django.contrib.sitemaps import Sitemap
from django.urls import reverse

from .models import Blog


class StaticViewSitemap(Sitemap):
    changefreq = 'monthly'

    def items(self):
        return ['home', 'about', 'egg_donation', 'calculator', 'blog', 'contact']

    def location(self, item):
        return reverse(item)

    def priority(self, item):
        return 1.0 if item == 'home' else 0.7


class BlogSitemap(Sitemap):
    changefreq = 'weekly'
    priority = 0.8

    def items(self):
        return Blog.objects.filter(published=True)

    def location(self, item):
        return reverse('blog_post', args=[item.blog_slug])

    def lastmod(self, item):
        return item.blog_date

