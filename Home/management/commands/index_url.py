from django.core.management.base import BaseCommand
from Home.indexing import index_url
from django.conf import settings


class Command(BaseCommand):
    help = 'Manually submit a URL to Google Indexing API'

    def add_arguments(self, parser):
        parser.add_argument('url', type=str, help='The URL to index')
        parser.add_argument(
            '--action',
            type=str,
            default='URL_UPDATED',
            choices=['URL_UPDATED', 'URL_DELETED'],
            help='Action: URL_UPDATED (default) or URL_DELETED'
        )

    def handle(self, *args, **options):
        url = options['url']
        action = options['action']
        
        self.stdout.write(f'Submitting {url} to Google Indexing API with action: {action}')
        
        success = index_url(url, action=action)
        
        if success:
            self.stdout.write(self.style.SUCCESS(f'Successfully submitted: {url}'))
        else:
            self.stdout.write(self.style.ERROR(f'Failed to submit: {url}'))
