from django.conf import settings
from django.http import HttpResponse
from django.template import loader


class MaintenanceModeMiddleware:
    """
    Middleware to show maintenance page when MAINTENANCE_MODE is enabled.
    Allows access to admin panel regardless of maintenance mode.
    """
    
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Check if maintenance mode is enabled
        if getattr(settings, 'MAINTENANCE_MODE', False):
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
            template = loader.get_template('maintenance.html')
            return HttpResponse(template.render(), status=503)
        
        return self.get_response(request)
