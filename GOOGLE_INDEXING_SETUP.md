# Google Indexing API Setup Instructions

## Overview
This integration automatically submits your blog post URLs to Google's Indexing API when they are published or updated in the Django admin, helping Google discover and index your content faster.

## Setup Steps

### 1. Add Service Account JSON to Environment Variables

You need to add your Google Service Account JSON key to your environment variables.

**For local development (.env file):**
```env
GOOGLE_SERVICE_ACCOUNT_JSON='{"type": "service_account", "project_id": "...", "private_key_id": "...", "private_key": "...", "client_email": "...", "client_id": "...", "auth_uri": "...", "token_uri": "...", "auth_provider_x509_cert_url": "...", "client_x509_cert_url": "..."}'
```

**For production (Render/other hosting):**
Add the same `GOOGLE_SERVICE_ACCOUNT_JSON` variable to your environment configuration.

**Note:** The entire JSON content should be on a single line with proper escaping for quotes.

### 2. Verify the Setup

After adding the environment variable, restart your Django server to load the new setting.

### 3. Test the Integration

**Option A: Test via Management Command**
```bash
python manage.py index_url https://fertileus.com.ng/blog/your-post-slug/
```

**Option B: Test via Admin Panel**
1. Go to Django Admin → Blog
2. Edit any published blog post
3. Save the post
4. Check the console/logs for indexing API response

### 4. How It Works

- **Automatic Indexing**: When you save a blog post in the admin panel with `published=True`, the URL is automatically submitted to Google's Indexing API
- **Manual Indexing**: Use the management command to manually submit any URL
- **Delete from Index**: Use `--action=URL_DELETED` to remove a URL from Google's index

### 5. Quota Limits

Google Indexing API has daily quota limits:
- 200 URL submissions per day for URL_UPDATED
- 200 URL submissions per day for URL_DELETED

If you exceed the quota, the integration will log an error but won't break your application.

### 6. Troubleshooting

**Error: "Indexing service not available"**
- Check that `GOOGLE_SERVICE_ACCOUNT_JSON` is set in your environment variables
- Verify the JSON is properly formatted and on a single line

**Error: "HTTP Error 403"**
- Verify the service account email is added as an Owner in Google Search Console
- Check that the Indexing API is enabled in Google Cloud Console

**Error: "HTTP Error 400"**
- Verify the URL format is correct (must be absolute URL with domain)
- Ensure the URL belongs to a verified property in Search Console

## Files Modified/Created

1. `FERTILEUS/settings.py` - Added `GOOGLE_SERVICE_ACCOUNT_JSON` setting
2. `Home/indexing.py` - Indexing API utility functions
3. `Home/admin.py` - Integrated indexing into BlogAdmin save_model
4. `Home/management/commands/index_url.py` - Management command for manual indexing
