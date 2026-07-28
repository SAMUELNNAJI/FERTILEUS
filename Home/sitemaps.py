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

    def lastmod(self, item):
        return item.blog_date


class BlogImageSitemap(Sitemap):
    """
    Image sitemap for blog post featured images.
    Helps search engines discover and index images for better image search results.
    """
    changefreq = 'weekly'
    priority = 0.6

    def items(self):
        # Only include posts that have images
        return Blog.objects.filter(published=True, blog_image__isnull=False).exclude(blog_image='')

    def lastmod(self, item):
        return item.blog_date

    def location(self, item):
        return reverse('blog_post', args=[item.blog_slug])

    def images(self, item):
        """
        Return a list of image dictionaries for the sitemap.
        Each dictionary should contain 'loc' (required) and optionally 'title' and 'caption'.
        """
        if item.blog_image:
            return [{
                'loc': item.blog_image.url,
                'title': item.blog_title,
                'caption': item.blog_content[:200] if item.blog_content else item.blog_title,
            }]
        return []
