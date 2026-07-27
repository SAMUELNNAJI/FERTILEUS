import django, os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'FertileUs.settings')
django.setup()

from Home.models import Blog, Comment
from aibot.models import ChatSession, Message
from django.contrib.auth.models import User
from django.db import connection

print("=== Neon DB Verification ===")
print(f"Connected to: {connection.vendor}")
print()

print(f"Blog posts : {Blog.objects.count()}")
for p in Blog.objects.all():
    print(f"  [{p.pk}] {p.blog_title[:60]}")
    print(f"         slug={p.blog_slug} | category={p.blog_category} | published={p.published}")

print()
print(f"Comments   : {Comment.objects.count()}")
for c in Comment.objects.all():
    print(f"  [{c.pk}] {c.name} on '{c.blog.blog_title[:40]}'")

print()
print(f"Auth users : {User.objects.count()}")
for u in User.objects.all():
    print(f"  [{u.pk}] {u.username} | superuser={u.is_superuser}")

print()
print(f"ChatSessions: {ChatSession.objects.count()}")
print(f"Messages    : {Message.objects.count()}")
print()
print("Verification complete.")
