from datetime import timedelta

from django.contrib.sitemaps import Sitemap
from django.urls import reverse
from django.utils import timezone

from .models import Blog

# Posts newer than this are treated as "fresh" and get tighter signals
FRESH_DAYS = 14


class StaticViewSitemap(Sitemap):
    protocol = 'https'

    # Per-page priority and change frequency
    _meta = {
        'home':         (1.0, 'daily'),
        'blog':         (0.9, 'daily'),
        'egg_donation': (0.8, 'monthly'),
        'about':        (0.7, 'monthly'),
        'calculator':   (0.7, 'monthly'),
        'contact':      (0.6, 'monthly'),
    }

    def items(self):
        return list(self._meta.keys())

    def location(self, item):
        return reverse(item)

    def priority(self, item):
        return self._meta[item][0]

    def changefreq(self, item):
        return self._meta[item][1]


class BlogSitemap(Sitemap):
    protocol = 'https'

    def items(self):
        return Blog.objects.filter(published=True).order_by('-blog_date')

    def location(self, item):
        return reverse('blog_post', args=[item.blog_slug])

    def lastmod(self, item):
        return item.blog_date

    def priority(self, item):
        """
        Fresh posts (< 14 days old) get priority 0.9 so Googlebot
        re-visits them sooner; older posts settle to 0.7.
        """
        cutoff = timezone.now() - timedelta(days=FRESH_DAYS)
        return 0.9 if item.blog_date >= cutoff else 0.7

    def changefreq(self, item):
        """
        Fresh posts: 'daily' — tells crawlers to come back soon.
        Older posts: 'weekly' — still active but not brand-new.
        """
        cutoff = timezone.now() - timedelta(days=FRESH_DAYS)
        return 'daily' if item.blog_date >= cutoff else 'weekly'

