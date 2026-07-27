from django.conf import settings


def seo(request):
    return {'site_url': settings.SITE_URL}
