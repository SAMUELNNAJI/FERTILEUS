from django.core.management.base import BaseCommand
from Home.indexnow import ping_indexnow
from django.conf import settings


class Command(BaseCommand):
    help = 'Test IndexNow API configuration and submission'

    def add_arguments(self, parser):
        parser.add_argument(
            '--url',
            type=str,
            default=None,
            help='Specific URL to test (optional)'
        )

    def handle(self, *args, **options):
        self.stdout.write('Testing IndexNow configuration...\n')
        
        # Check if INDEXNOW_KEY is set
        key = getattr(settings, 'INDEXNOW_KEY', None)
        site_url = getattr(settings, 'SITE_URL', '').rstrip('/')
        
        if not key:
            self.stdout.write(self.style.ERROR('INDEXNOW_KEY is not set in settings'))
            self.stdout.write('Add INDEXNOW_KEY to your .env file to enable IndexNow')
            return
        
        self.stdout.write(self.style.SUCCESS(f'INDEXNOW_KEY: {key[:8]}... (truncated)'))
        self.stdout.write(self.style.SUCCESS(f'SITE_URL: {site_url}'))
        
        # Test URL
        test_url = options.get('url') or f'{site_url}/'
        
        self.stdout.write(f'\nSubmitting test URL: {test_url}')
        
        success = ping_indexnow(test_url)
        
        if success:
            self.stdout.write(self.style.SUCCESS('✓ IndexNow submission successful!'))
            self.stdout.write('Your IndexNow configuration is working correctly.')
        else:
            self.stdout.write(self.style.ERROR('✗ IndexNow submission failed'))
            self.stdout.write('Check your INDEXNOW_KEY and ensure it matches:')
            self.stdout.write('  1. The key in your IndexNow account')
            self.stdout.write('  2. The key file at yourdomain.com/INDEXNOW_KEY.txt')
