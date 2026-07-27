"""
Custom ImageKit storage backend for Django 4.2+

Stores the full CDN URL in the database (not the file_id or filename),
so post.blog_image.url always returns the CDN URL directly without
making an extra API call.
"""
import base64
import os

from django.conf import settings
from django.core.files.storage import Storage
from django.utils.deconstruct import deconstructible

from imagekitio import ImageKit
from imagekitio.models.UploadFileRequestOptions import UploadFileRequestOptions


def _get_ik():
    """Lazily instantiate the ImageKit client from settings."""
    ik_cfg = settings.IMAGEKIT_STORAGE
    return ImageKit(
        private_key=ik_cfg['PRIVATE_KEY'],
        public_key=ik_cfg['PUBLIC_KEY'],
        url_endpoint=ik_cfg['URL_ENDPOINT'],
    )


@deconstructible
class ImageKitStorage(Storage):
    """
    Uploads files to ImageKit CDN and stores the returned CDN URL
    in the model's ImageField so .url always works without extra API calls.
    """

    def _save(self, name, content):
        ik = _get_ik()
        ik_cfg = settings.IMAGEKIT_STORAGE

        # Determine folder: use upload_options folder + the file's subdirectory
        upload_opts = ik_cfg.get('UPLOAD_OPTIONS', {})
        base_folder = upload_opts.get('folder', '/fertileus/')

        # Strip directory from name — just use the bare filename
        file_name = os.path.basename(name)

        # Read and base64-encode the file content
        content.seek(0)
        encoded = base64.b64encode(content.read()).decode('utf-8')

        options = UploadFileRequestOptions(
            use_unique_file_name=upload_opts.get('use_unique_file_name', True),
            folder=base_folder,
            is_private_file=upload_opts.get('is_private_file', False),
            overwrite_file=upload_opts.get('overwrite_file', True),
        )

        response = ik.upload_file(
            file=encoded,
            file_name=file_name,
            options=options,
        )

        # Store the full CDN URL — so .url returns it directly
        return response.url

    def url(self, name):
        # name IS the full CDN URL after _save stores it
        if name and name.startswith('http'):
            return name
        # Fallback for old records that stored a path instead of URL
        endpoint = settings.IMAGEKIT_STORAGE.get('URL_ENDPOINT', '').rstrip('/')
        return f"{endpoint}/{name.lstrip('/')}"

    def exists(self, name):
        # Always allow saving — ImageKit handles deduplication
        return False

    def delete(self, name):
        # Deletion via ImageKit API is optional; skip for now
        pass

    def _open(self, name, mode='rb'):
        raise NotImplementedError("ImageKitStorage does not support opening files.")

    def get_available_name(self, name, max_length=None):
        return name
