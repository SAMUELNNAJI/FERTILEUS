"""
Fix fallback placeholder cards in blog.html and index.html.
- Wraps each hardcoded card in an <a href="{% url 'blog' %}"> anchor
- Adds a "Read article" span to match the real post cards
"""
import os, re

BASE = os.path.join(os.path.dirname(__file__), "templates", "home")


def read(fname):
    with open(os.path.join(BASE, fname), "r", encoding="utf-8") as f:
        return f.read()


def write(fname, content):
    with open(os.path.join(BASE, fname), "w", encoding="utf-8") as f:
        f.write(content)


# ── blog.html ─────────────────────────────────────────────────────────────────
blog = read("blog.html")

old_empty = '''      {% empty %}
      <!-- No posts in DB yet — show placeholder cards so the page looks complete -->
      <article class="journal-card" data-category="Fertility">
        <div class="journal-img-wrap">
          <img
            src="{% static 'assests/image/Fertility.jpg' %}"
            alt="Understanding Your Fertile Window"
            class="journal-img"
          />
        </div>
        <div class="journal-body">
          <p class="journal-meta">
            <span class="journal-cat">Fertility</span> · 29 March 2026 · 6 min
            read
          </p>
          <h3>Understanding Your Fertile Window</h3>
          <p>
            Six days a cycle really matter. Here is how to find yours using
            cycle length, cervical mucus and simple tracking — no expensive
            gadgets required.
          </p>
        </div>
      </article>
      <article class="journal-card" data-category="Pregnancy">
        <div class="journal-img-wrap">
          <img
            src="{% static 'assests/image/pregnacy.jpg' %}"
            alt="When Conception Takes Longer Than Expected"
            class="journal-img"
          />
        </div>
        <div class="journal-body">
          <p class="journal-meta">
            <span class="journal-cat">Pregnancy</span> · 28 March 2026 · 7 min
            read
          </p>
          <h3>When Conception Takes Longer Than Expected</h3>
          <p>
            Trying for months without a positive test is exhausting. Here is
            what is actually happening, what is normal, and the point at which
            testing becomes worthwhile.
          </p>
        </div>
      </article>
      <article class="journal-card" data-category="Donation">
        <div class="journal-img-wrap">
          <img
            src="{% static 'assests/image/donations.jpg' %}"
            alt="What Egg Donation Really Involves"
            class="journal-img"
          />
        </div>
        <div class="journal-body">
          <p class="journal-meta">
            <span class="journal-cat">Donation</span> · 26 March 2026 · 5 min
            read
          </p>
          <h3>What Egg Donation Really Involves</h3>
          <p>
            From screening to retrieval, a clear and honest walkthrough of the
            egg donation process — including the questions donors are often too
            shy to ask.
          </p>
        </div>
      </article>'''

new_empty = '''      {% empty %}
      <!-- No posts in DB yet — show placeholder cards so the page looks complete -->
      <a href="{% url 'blog' %}" class="journal-card-link">
        <article class="journal-card" data-category="Fertility">
          <div class="journal-img-wrap">
            <img
              src="{% static 'assests/image/Fertility.jpg' %}"
              alt="Understanding Your Fertile Window"
              class="journal-img"
            />
          </div>
          <div class="journal-body">
            <p class="journal-meta">
              <span class="journal-cat">Fertility</span> · 29 March 2026 · 6 min read
            </p>
            <h3>Understanding Your Fertile Window</h3>
            <p>
              Six days a cycle really matter. Here is how to find yours using
              cycle length, cervical mucus and simple tracking — no expensive
              gadgets required.
            </p>
            <span class="journal-link">Read article</span>
          </div>
        </article>
      </a>
      <a href="{% url 'blog' %}" class="journal-card-link">
        <article class="journal-card" data-category="Pregnancy">
          <div class="journal-img-wrap">
            <img
              src="{% static 'assests/image/pregnacy.jpg' %}"
              alt="When Conception Takes Longer Than Expected"
              class="journal-img"
            />
          </div>
          <div class="journal-body">
            <p class="journal-meta">
              <span class="journal-cat">Pregnancy</span> · 28 March 2026 · 7 min read
            </p>
            <h3>When Conception Takes Longer Than Expected</h3>
            <p>
              Trying for months without a positive test is exhausting. Here is
              what is actually happening, what is normal, and the point at which
              testing becomes worthwhile.
            </p>
            <span class="journal-link">Read article</span>
          </div>
        </article>
      </a>
      <a href="{% url 'blog' %}" class="journal-card-link">
        <article class="journal-card" data-category="Donation">
          <div class="journal-img-wrap">
            <img
              src="{% static 'assests/image/donations.jpg' %}"
              alt="What Egg Donation Really Involves"
              class="journal-img"
            />
          </div>
          <div class="journal-body">
            <p class="journal-meta">
              <span class="journal-cat">Donation</span> · 26 March 2026 · 5 min read
            </p>
            <h3>What Egg Donation Really Involves</h3>
            <p>
              From screening to retrieval, a clear and honest walkthrough of the
              egg donation process — including the questions donors are often too
              shy to ask.
            </p>
            <span class="journal-link">Read article</span>
          </div>
        </article>
      </a>'''

if old_empty in blog:
    blog = blog.replace(old_empty, new_empty)
    write("blog.html", blog)
    print("blog.html — fixed")
else:
    print("blog.html — marker not found, check manually")


# ── index.html ────────────────────────────────────────────────────────────────
index = read("index.html")

old_index_empty = '''      {% empty %}
      <!-- Fallback when no posts exist in the database yet -->
      <article class="journal-card">
        <div class="journal-img-wrap">
          <img
            src="{% static 'assests/image/Fertility.jpg' %}"
            alt="Understanding Your Fertile Window"
            class="journal-img"
          />
        </div>
        <div class="journal-body">
          <p class="journal-meta">
            <span class="journal-cat">Fertility</span> · 29 March 2026
          </p>
          <h3>Understanding Your Fertile Window</h3>
          <p>
            Six days a cycle really matter. Here is how to find yours using
            simple tracking.
          </p>
        </div>
      </article>
      <article class="journal-card">
        <div class="journal-img-wrap">
          <img
            src="{% static 'assests/image/pregnacy.jpg' %}"
            alt="When Conception Takes Longer"
            class="journal-img"
          />
        </div>
        <div class="journal-body">
          <p class="journal-meta">
            <span class="journal-cat">Pregnancy</span> · 28 March 2026
          </p>
          <h3>When Conception Takes Longer Than Expected</h3>
          <p>
            Trying for months without a positive test is exhausting. Here is
            what is actually happening.
          </p>
        </div>
      </article>
      <article class="journal-card">
        <div class="journal-img-wrap">
          <img
            src="{% static 'assests/image/donations.jpg' %}"
            alt="What Egg Donation Really Involves"
            class="journal-img"
          />
        </div>
        <div class="journal-body">
          <p class="journal-meta">
            <span class="journal-cat">Donation</span> · 26 March 2026
          </p>
          <h3>What Egg Donation Really Involves</h3>
          <p>
            From screening to retrieval, a clear and honest walkthrough of the
            egg donation process.
          </p>
        </div>
      </article>'''

new_index_empty = '''      {% empty %}
      <!-- Fallback when no posts exist in the database yet -->
      <a href="{% url 'blog' %}" class="journal-card-link">
        <article class="journal-card">
          <div class="journal-img-wrap">
            <img
              src="{% static 'assests/image/Fertility.jpg' %}"
              alt="Understanding Your Fertile Window"
              class="journal-img"
            />
          </div>
          <div class="journal-body">
            <p class="journal-meta">
              <span class="journal-cat">Fertility</span> · 29 March 2026
            </p>
            <h3>Understanding Your Fertile Window</h3>
            <p>
              Six days a cycle really matter. Here is how to find yours using
              simple tracking.
            </p>
            <span class="journal-link">Read article</span>
          </div>
        </article>
      </a>
      <a href="{% url 'blog' %}" class="journal-card-link">
        <article class="journal-card">
          <div class="journal-img-wrap">
            <img
              src="{% static 'assests/image/pregnacy.jpg' %}"
              alt="When Conception Takes Longer"
              class="journal-img"
            />
          </div>
          <div class="journal-body">
            <p class="journal-meta">
              <span class="journal-cat">Pregnancy</span> · 28 March 2026
            </p>
            <h3>When Conception Takes Longer Than Expected</h3>
            <p>
              Trying for months without a positive test is exhausting. Here is
              what is actually happening.
            </p>
            <span class="journal-link">Read article</span>
          </div>
        </article>
      </a>
      <a href="{% url 'blog' %}" class="journal-card-link">
        <article class="journal-card">
          <div class="journal-img-wrap">
            <img
              src="{% static 'assests/image/donations.jpg' %}"
              alt="What Egg Donation Really Involves"
              class="journal-img"
            />
          </div>
          <div class="journal-body">
            <p class="journal-meta">
              <span class="journal-cat">Donation</span> · 26 March 2026
            </p>
            <h3>What Egg Donation Really Involves</h3>
            <p>
              From screening to retrieval, a clear and honest walkthrough of the
              egg donation process.
            </p>
            <span class="journal-link">Read article</span>
          </div>
        </article>
      </a>'''

if old_index_empty in index:
    index = index.replace(old_index_empty, new_index_empty)
    write("index.html", index)
    print("index.html — fixed")
else:
    print("index.html — marker not found, check manually")

print("\nDone.")
