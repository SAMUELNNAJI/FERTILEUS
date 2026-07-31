from django.conf import settings
from django.http import HttpResponse
from django.template import loader
import logging

logger = logging.getLogger(__name__)


class MaintenanceModeMiddleware:
    """
    Middleware to show maintenance page when MAINTENANCE_MODE is enabled.
    Allows access to admin panel regardless of maintenance mode.
    """
    
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Check if maintenance mode is enabled
        maintenance_mode = getattr(settings, 'MAINTENANCE_MODE', False)
        logger.info(f"MAINTENANCE_MODE setting: {maintenance_mode}")
        
        if maintenance_mode:
            # Allow access to admin panel and static files
            if request.path.startswith('/admin/') or request.path.startswith('/static/'):
                return self.get_response(request)
            
            # Allow access to maintenance page itself
            if request.path == '/maintenance/':
                return self.get_response(request)
            
            # Allow access if user is superuser (optional - for testing)
            if hasattr(request, 'user') and request.user.is_authenticated and request.user.is_superuser:
                return self.get_response(request)
            
            # Show maintenance page for all other requests
            logger.info(f"Showing maintenance page for: {request.path}")
            template = loader.get_template('maintenance.html')
            return HttpResponse(template.render(), status=503)
        
        return self.get_response(request)
