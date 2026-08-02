from django.conf import settings
from django.http import HttpResponse
from django.template import loader
import logging

logger = logging.getLogger(__name__)


class MaintenanceModeMiddleware:
    """
    Middleware to show maintenance page when MAINTENANCE_MODE is enabled.
    Allows access to admin panel regardless of maintenance mode.

    Placement note: this middleware is intentionally placed AFTER
    AuthenticationMiddleware in MIDDLEWARE so request.user is always
    available for the superuser bypass check.
    """

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Cast to bool explicitly — Render env vars arrive as strings
        # e.g. "True" / "False", so we can't rely on truthiness alone.
        raw = getattr(settings, 'MAINTENANCE_MODE', False)
        if isinstance(raw, str):
            maintenance_mode = raw.strip().lower() in ('true', '1', 'yes')
        else:
            maintenance_mode = bool(raw)

        if not maintenance_mode:
            return self.get_response(request)

        # Always allow admin and static files through
        if request.path.startswith(('/admin/', '/static/', '/maintenance/')):
            return self.get_response(request)

        # Let superusers through so you can check the site while it's down
        # request.user is safe here because AuthenticationMiddleware runs first
        user = getattr(request, 'user', None)
        if user is not None and user.is_authenticated and user.is_superuser:
            return self.get_response(request)

        logger.info("Maintenance mode active — serving 503 for: %s", request.path)
        template = loader.get_template('maintenance.html')
        return HttpResponse(template.render({}, request), status=503)
