"""
Management command: ping_search_engines

Submits published blog post URLs (and static pages) to search engines
for immediate crawling. Two modes:

1. IndexNow (default, no auth needed)
   Pings Bing, Yandex, and any other IndexNow-compatible engine.

2. Google Indexing API (optional, requires a service-account JSON key)
   Tells Google to re-crawl specific URLs right away.
   NOTE: Google officially supports this only for JobPosting /
   BroadcastEvent pages, but it often works for regular URLs too.

Usage examples:
    # Ping IndexNow for all published posts + static pages
    python manage.py ping_search_engines

    # Only ping IndexNow for the last 5 published posts
    python manage.py ping_search_engines --limit 5

    # Also call the Google Indexing API (requires service account key)
    python manage.py ping_search_engines --google --keyfile service_account.json

    # Target a single URL only
    python manage.py ping_search_engines --url /blog/my-post-slug/
"""

import os
import logging
from django.core.management.base import BaseCommand, CommandError
from django.urls import reverse
from django.conf import settings

from Home.models import Blog
from Home.indexnow import ping_indexnow

logger = logging.getLogger(__name__)

STATIC_PAGES = ["home", "about", "blog", "egg_donation", "calculator", "contact"]


class Command(BaseCommand):
    help = "Ping IndexNow (and optionally Google Indexing API) for all published blog URLs."

    def add_arguments(self, parser):
        parser.add_argument(
            "--limit",
            type=int,
            default=None,
            help="Only submit the N most recently published posts (default: all).",
        )
        parser.add_argument(
            "--url",
            type=str,
            default=None,
            help="Submit a single URL path, e.g. /blog/my-post-slug/",
        )
        parser.add_argument(
            "--google",
            action="store_true",
            default=False,
            help="Also ping the Google Indexing API (requires --keyfile).",
        )
        parser.add_argument(
            "--keyfile",
            type=str,
            default="service_account.json",
            help="Path to Google service-account JSON key (used with --google).",
        )
        parser.add_argument(
            "--static",
            action="store_true",
            default=False,
            help="Include static pages (home, about, blog, etc.) in the submission.",
        )

    def handle(self, *args, **options):
        site_url = getattr(settings, "SITE_URL", "").rstrip("/")
        if not site_url:
            raise CommandError("SITE_URL is not set in settings. Add it to your .env file.")

        urls = []

        # ── Single URL mode ─────────────────────────────────────────────────
        if options["url"]:
            path = options["url"]
            full = path if path.startswith("http") else f"{site_url}{path}"
            urls = [full]
            self.stdout.write(f"Single URL mode: {full}")

        else:
            # ── Static pages ─────────────────────────────────────────────────
            if options["static"]:
                for name in STATIC_PAGES:
                    try:
                        urls.append(f"{site_url}{reverse(name)}")
                    except Exception:
                        pass
                self.stdout.write(f"  + {len(urls)} static page(s) queued")

            # ── Blog posts ───────────────────────────────────────────────────
            qs = Blog.objects.filter(published=True).order_by("-blog_date")
            if options["limit"]:
                qs = qs[: options["limit"]]

            for post in qs:
                urls.append(f"{site_url}{reverse('blog_post', args=[post.blog_slug])}")

            self.stdout.write(f"  + {qs.count()} blog post(s) queued")

        if not urls:
            self.stdout.write(self.style.WARNING("No URLs to submit."))
            return

        self.stdout.write(f"\nTotal URLs to submit: {len(urls)}")

        # ── IndexNow ─────────────────────────────────────────────────────────
        self.stdout.write("\n[1/2] Submitting to IndexNow...")
        # IndexNow accepts max 10 000 URLs per batch; chunk just in case
        chunk_size = 100
        success = True
        for i in range(0, len(urls), chunk_size):
            batch = urls[i : i + chunk_size]
            ok = ping_indexnow(batch)
            if ok:
                self.stdout.write(
                    self.style.SUCCESS(f"  ✓ Batch {i // chunk_size + 1}: {len(batch)} URL(s) submitted")
                )
            else:
                self.stdout.write(
                    self.style.WARNING(f"  ✗ Batch {i // chunk_size + 1}: submission failed (check INDEXNOW_KEY)")
                )
                success = False

        # ── Google Indexing API (optional) ────────────────────────────────────
        if options["google"]:
            self.stdout.write("\n[2/2] Submitting to Google Indexing API...")
            self._submit_to_google(urls, options["keyfile"])
        else:
            self.stdout.write("\n[2/2] Google Indexing API skipped (pass --google --keyfile path/to/key.json to enable)")

        if success:
            self.stdout.write(self.style.SUCCESS("\nDone. URLs queued for indexing."))
        else:
            self.stdout.write(self.style.WARNING("\nDone with some errors. Check logs above."))

    # ──────────────────────────────────────────────────────────────────────────
    def _submit_to_google(self, urls: list[str], keyfile: str):
        """
        Submit URLs to the Google Indexing API using a service account.

        Requires:
            pip install google-auth google-auth-httplib2 google-api-python-client

        Setup:
            1. Google Cloud Console → Enable "Indexing API"
            2. Create a Service Account → download JSON key → save as service_account.json
            3. Google Search Console → Settings → Users → add service account email as Owner
        """
        try:
            from google.oauth2 import service_account
            from googleapiclient.discovery import build
        except ImportError:
            self.stdout.write(
                self.style.ERROR(
                    "  Missing libraries. Run:\n"
                    "  pip install google-auth google-auth-httplib2 google-api-python-client"
                )
            )
            return

        if not os.path.exists(keyfile):
            self.stdout.write(
                self.style.ERROR(
                    f"  Service account key not found: {keyfile}\n"
                    "  Download it from Google Cloud Console and place it in the project root."
                )
            )
            return

        try:
            credentials = service_account.Credentials.from_service_account_file(
                keyfile,
                scopes=["https://www.googleapis.com/auth/indexing"],
            )
            service = build("indexing", "v3", credentials=credentials)

            submitted, failed = 0, 0
            for url in urls:
                try:
                    body = {"url": url, "type": "URL_UPDATED"}
                    service.urlNotifications().publish(body=body).execute()
                    self.stdout.write(f"  ✓ {url}")
                    submitted += 1
                except Exception as exc:
                    self.stdout.write(self.style.WARNING(f"  ✗ {url} — {exc}"))
                    failed += 1

            self.stdout.write(
                self.style.SUCCESS(f"  Google Indexing API: {submitted} submitted, {failed} failed")
            )

        except Exception as exc:
            self.stdout.write(self.style.ERROR(f"  Google Indexing API error: {exc}"))
