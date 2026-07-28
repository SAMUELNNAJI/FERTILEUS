"""
IndexNow helper — instantly notifies Bing, Yandex, and other
IndexNow-compatible engines when a URL is created or updated.

Usage:
    from Home.indexnow import ping_indexnow
    ping_indexnow("https://fertileus.com.ng/blog/my-post-slug/")
"""

import logging
import requests
from django.conf import settings

logger = logging.getLogger(__name__)

INDEXNOW_ENDPOINT = "https://api.indexnow.org/indexnow"


def ping_indexnow(urls: list[str] | str) -> bool:
    """
    Submit one or more absolute URLs to the IndexNow API.

    Returns True on success (HTTP 200/202), False otherwise.
    Set INDEXNOW_KEY in your .env to enable. If the key is missing,
    the function logs a warning and returns False gracefully.
    """
    key = getattr(settings, "INDEXNOW_KEY", None)
    site_url = getattr(settings, "SITE_URL", "").rstrip("/")

    if not key:
        logger.warning("IndexNow skipped: INDEXNOW_KEY not set in settings.")
        return False

    if isinstance(urls, str):
        urls = [urls]

    # Ensure all URLs are absolute
    absolute_urls = [
        u if u.startswith("http") else f"{site_url}{u}"
        for u in urls
    ]

    host = site_url.replace("https://", "").replace("http://", "")

    payload = {
        "host": host,
        "key": key,
        "keyLocation": f"{site_url}/{key}.txt",
        "urlList": absolute_urls,
    }

    try:
        response = requests.post(
            INDEXNOW_ENDPOINT,
            json=payload,
            headers={"Content-Type": "application/json; charset=utf-8"},
            timeout=10,
        )
        if response.status_code in (200, 202):
            logger.info("IndexNow: submitted %d URL(s) — status %s", len(absolute_urls), response.status_code)
            return True
        else:
            logger.warning("IndexNow: unexpected status %s — %s", response.status_code, response.text)
            return False
    except requests.RequestException as exc:
        logger.error("IndexNow: request failed — %s", exc)
        return False
