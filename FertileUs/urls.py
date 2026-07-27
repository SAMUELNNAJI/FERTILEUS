from django.contrib import admin
from django.urls import path, include
from django.contrib.sitemaps.views import sitemap
from django.http import HttpResponse
from Home.sitemaps import BlogSitemap, StaticViewSitemap
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('sitemap.xml', sitemap, {'sitemaps': {
        'pages': StaticViewSitemap,
        'posts': BlogSitemap,
    }}, name='django.contrib.sitemaps.views.sitemap'),
    path('robots.txt', lambda request: HttpResponse(
        'User-agent: *\nAllow: /\nSitemap: ' + request.build_absolute_uri('/sitemap.xml') + '\n',
        content_type='text/plain',
    ), name='robots'),
    path('admin/', admin.site.urls),
    path('', include('Home.urls')),
    path('ai-bot/', include('aibot.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
