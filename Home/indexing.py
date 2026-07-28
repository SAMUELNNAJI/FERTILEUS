import json
import os
from django.conf import settings
from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError


def get_indexing_service():
    """
    Create and return an authenticated Google Indexing API service.
    """
    if not settings.GOOGLE_SERVICE_ACCOUNT_JSON:
        return None
    
    try:
        # Parse the JSON credentials from environment variable
        credentials_info = json.loads(settings.GOOGLE_SERVICE_ACCOUNT_JSON)
        
        # Create credentials from the service account info
        credentials = service_account.Credentials.from_service_account_info(
            credentials_info,
            scopes=['https://www.googleapis.com/auth/indexing']
        )
        
        # Build the service
        service = build('indexing', 'v3', credentials=credentials)
        return service
    except Exception as e:
        print(f"Error creating Indexing service: {e}")
        return None


def index_url(url, action='URL_UPDATED'):
    """
    Submit a URL to Google Indexing API.
    
    Args:
        url (str): The URL to index
        action (str): 'URL_UPDATED' for new/updated pages, 'URL_DELETED' for deleted pages
    
    Returns:
        bool: True if successful, False otherwise
    """
    service = get_indexing_service()
    if not service:
        print("Indexing service not available")
        return False
    
    try:
        body = {
            'url': url,
            'type': action
        }
        
        response = service.urlNotifications().publish(body=body).execute()
        print(f"Indexing API response for {url}: {response}")
        return True
    except HttpError as e:
        print(f"HTTP Error indexing {url}: {e}")
        return False
    except Exception as e:
        print(f"Error indexing {url}: {e}")
        return False


def index_blog_post(blog_post):
    """
    Index a blog post URL using Google Indexing API.
    
    Args:
        blog_post: Blog model instance
    
    Returns:
        bool: True if successful, False otherwise
    """
    if not blog_post.published:
        return False
    
    url = f"{settings.SITE_URL}/blog/{blog_post.blog_slug}/"
    return index_url(url, action='URL_UPDATED')


def delete_from_index(blog_post):
    """
    Remove a blog post URL from Google index using Indexing API.
    
    Args:
        blog_post: Blog model instance
    
    Returns:
        bool: True if successful, False otherwise
    """
    url = f"{settings.SITE_URL}/blog/{blog_post.blog_slug}/"
    return index_url(url, action='URL_DELETED')
