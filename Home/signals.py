"""
Signals for the Home app.

- Fires IndexNow ping whenever a Blog post is saved as published.
  Only pings when the post transitions to published=True or is
  updated while already published (content change).
"""

import logging
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.urls import reverse
from django.conf import settings

from .models import Blog

logger = logging.getLogger(__name__)


@receiver(post_save, sender=Blog)
def notify_indexnow_on_publish(sender, instance, created, **kwargs):
    """
    Ping IndexNow whenever a blog post is saved with published=True.

    - New post published immediately → ping
    - Existing post updated while published → ping (content changed)
    - Post saved as draft (published=False) → skip
    """
    if not instance.published:
        return

    try:
        from .indexnow import ping_indexnow

        site_url = getattr(settings, "SITE_URL", "").rstrip("/")
        path = reverse("blog_post", args=[instance.blog_slug])
        full_url = f"{site_url}{path}"

        action = "created" if created else "updated"
        logger.info("Blog post %s (%s) — pinging IndexNow for %s", instance.blog_slug, action, full_url)

        ping_indexnow(full_url)

    except Exception as exc:
        # Never let a signal failure break the save operation
        logger.error("IndexNow signal error for '%s': %s", instance.blog_slug, exc)
