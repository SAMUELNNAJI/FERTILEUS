"""One-shot script to fix Django template tags split across lines."""
import os

BASE = os.path.join(os.path.dirname(__file__), "templates", "home")


def fix(filename, new_header, body_start_marker):
    """Replace everything up to body_start_marker with new_header."""
    path = os.path.join(BASE, filename)
    with open(path, "r", encoding="utf-8") as f:
        content = f.read()

    idx = content.find(body_start_marker)
    if idx == -1:
        print(f"  SKIP {filename} — marker not found")
        return

    new_content = new_header + "\n" + content[idx:]
    with open(path, "w", encoding="utf-8") as f:
        f.write(new_content)

    # Verify
    with open(path, "r", encoding="utf-8") as f:
        first = f.readline().strip()
    print(f"  OK {filename} — first line: {first}")


# ── 403 ──────────────────────────────────────────────────────────────────────
fix(
    "403.html",
    '{% extends "home/base.html" %}\n'
    "{% load static %}\n\n"
    "{% block title %}Permission denied - FertilEus Network{% endblock %}\n"
    "{% block meta_description %}You do not have permission to access this page.{% endblock %}\n"
    "{% block og_type %}website{% endblock %}\n",
    "{% block content %}",
)

# ── 404 ──────────────────────────────────────────────────────────────────────
fix(
    "404.html",
    '{% extends "home/base.html" %}\n'
    "{% load static %}\n\n"
    "{% block title %}Page not found - FertilEus Network{% endblock %}\n"
    "{% block meta_description %}The page you are looking for does not exist or has been moved.{% endblock %}\n"
    "{% block og_type %}website{% endblock %}\n",
    "{% block content %}",
)

# ── 500 ──────────────────────────────────────────────────────────────────────
fix(
    "500.html",
    '{% extends "home/base.html" %}\n'
    "{% load static %}\n\n"
    "{% block title %}Something went wrong - FertilEus Network{% endblock %}\n"
    "{% block meta_description %}We are experiencing a technical issue. Please try again later.{% endblock %}\n"
    "{% block og_type %}website{% endblock %}\n",
    "{% block content %}",
)

# ── about ─────────────────────────────────────────────────────────────────────
fix(
    "about.html",
    '{% extends "home/base.html" %}\n'
    "{% load static %}\n\n"
    "{% block title %}About Us - FertilEus Network{% endblock %}\n"
    "{% block meta_description %}Learn how FertilEus supports fertility education, informed choices, and compassionate care across Africa.{% endblock %}\n",
    "{% block content %}",
)

# ── blog ──────────────────────────────────────────────────────────────────────
fix(
    "blog.html",
    '{% extends "home/base.html" %}\n'
    "{% load static %}\n\n"
    "{% block title %}Journal - FertilEus Network{% endblock %}\n"
    "{% block meta_description %}Explore expert fertility insights, pregnancy information, and egg donation guidance from FertilEus.{% endblock %}\n",
    "{% block content %}",
)

# ── contact ───────────────────────────────────────────────────────────────────
fix(
    "contact.html",
    '{% extends "home/base.html" %}\n'
    "{% load static %}\n\n"
    "{% block title %}Contact - FertilEus Network{% endblock %}\n"
    "{% block meta_description %}Contact FertilEus for compassionate fertility guidance, education, and support across Africa.{% endblock %}\n",
    "{% block content %}",
)

# ── egg-donation ──────────────────────────────────────────────────────────────
fix(
    "egg-donation.html",
    '{% extends "home/base.html" %}\n'
    "{% load static %}\n\n"
    "{% block title %}Egg Donation - FertilEus Network{% endblock %}\n"
    "{% block meta_description %}Understand egg donation, explore your options, and find supportive fertility guidance with FertilEus.{% endblock %}\n",
    "{% block content %}",
)

# ── calculator ────────────────────────────────────────────────────────────────
fix(
    "calculator.html",
    '{% extends "home/base.html" %}\n'
    "{% load static %}\n\n"
    "{% block title %}Fertility Calculator - FertilEus Network{% endblock %}\n"
    "{% block meta_description %}Use the FertilEus fertility calculator to better understand your menstrual cycle and likely fertile window.{% endblock %}\n",
    "{% block content %}",
)

# ── index ─────────────────────────────────────────────────────────────────────
fix(
    "index.html",
    '{% extends "home/base.html" %}\n'
    "{% load static %}\n\n"
    "{% block title %}FertilEus - Your Fertile Health Matters to Us{% endblock %}\n"
    "{% block meta_description %}Trusted fertility education, personalised guidance, and community support for people across Africa.{% endblock %}\n",
    "{% block content %}",
)

# ── blog-post ─────────────────────────────────────────────────────────────────
fix(
    "blog-post.html",
    '{% extends "home/base.html" %}\n'
    "{% load static %}\n\n"
    "{% block title %}{{ post.blog_title }} - FertilEus Network{% endblock %}\n"
    "{% block meta_description %}{{ post.blog_content|striptags|truncatechars:155 }}{% endblock %}\n"
    "{% block og_type %}article{% endblock %}\n"
    "{% block og_title %}{{ post.blog_title }} - FertilEus Network{% endblock %}\n"
    "{% block og_description %}{{ post.blog_content|striptags|truncatechars:155 }}{% endblock %}\n"
    "{% block twitter_title %}{{ post.blog_title }} - FertilEus Network{% endblock %}\n"
    "{% block twitter_description %}{{ post.blog_content|striptags|truncatechars:155 }}{% endblock %}\n",
    "{% block extra_head %}",
)

print("\nDone.")
