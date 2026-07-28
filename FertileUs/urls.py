from django.contrib import admin
from django.urls import path, include
from django.contrib.sitemaps.views import sitemap
from django.http import HttpResponse
from Home.sitemaps import BlogSitemap, StaticViewSitemap, BlogImageSitemap
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.staticfiles.storage import staticfiles_storage
from django.views.generic.base import RedirectView

urlpatterns = [
    path('sitemap.xml', sitemap, {'sitemaps': {
        'pages': StaticViewSitemap,
        'posts': BlogSitemap,
        'images': BlogImageSitemap,
    }}, name='django.contrib.sitemaps.views.sitemap'),
    path('robots.txt', lambda request: HttpResponse(
        'User-agent: *\n'
        'Allow: /\n'
        '\n'
        '# Disallow admin and private areas\n'
        'Disallow: /admin/\n'
        'Disallow: /ai-bot/\n'
        '\n'
        '# Sitemap location\n'
        'Sitemap: ' + request.build_absolute_uri('/sitemap.xml') + '\n',
        content_type='text/plain',
    ), name='robots'),
    # Serve favicon.ico so browsers don't get a 404
    path('favicon.ico', RedirectView.as_view(url=staticfiles_storage.url('favicon.svg'), permanent=True)),
    path('admin/', admin.site.urls),
    path('', include('Home.urls')),
    path('ai-bot/', include('aibot.urls')),
]

handler404 = 'Home.views.error_404'
handler500 = 'Home.views.error_500'
handler403 = 'Home.views.error_403'

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
