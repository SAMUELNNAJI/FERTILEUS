"""Fix blog-post.html: split block tags and broken JS."""
import os

path = os.path.join(os.path.dirname(__file__), "templates", "home", "blog-post.html")

with open(path, "r", encoding="utf-8") as f:
    content = f.read()

# ── Fix 1: split endblock/block on same line (extra_head → content) ──────────
content = content.replace(
    "{% endblock %} {% block content %}",
    "{% endblock %}\n\n{% block content %}"
)

# ── Fix 2: split endblock/block on same line (content → extra_js) ────────────
content = content.replace(
    "{% endblock %} {% block extra_js %}",
    "{% endblock %}\n\n{% block extra_js %}"
)

# ── Fix 3: broken JS — replace the entire script block ───────────────────────
old_js = """<script>
  /* ---- Character counter ---- */
  const textarea = document.getElementById("comment-body");
  const charsLeft = document.getElementById("chars-left");
  if (textarea) {
    textarea.addEventListener("input", () => {
      charsLeft.textContent = 1200 - textarea.value.length;
    });
  }

  /* ---- Sort buttons ---- */
  const sortBtns = document.querySelectorAll(".disc-sort-btn");
  sortBtns.forEach((btn) => {
    btn.addEventListener("click", () => {
      sortBtns.forEach((b) => b.classList.remove("active"));
      btn.classList.add("active");
      const list = document.getElementById("commentList");
      const items = [...list.querySelectorAll(".disc-comment")];
      const sort = btn.dataset.sort;
      items.sort((a, b) => {
        if (sort === "newest") return b.dataset.created - a.dataset.created;
        if (sort === "oldest") return a.dataset.created - b.dataset.created;
        if (sort === "top") return b.dataset.likes - a.dataset.likes;
        return 0;
      });
      items.forEach((el) => list.appendChild(el));
    });
  });

  /* ---- Action buttons (Helpful, Reply, Edit, Delete) ---- */
  document.querySelectorAll(".disc-action-btn").forEach((btn) => {
    btn.addEventListener("click", () => {
      const action = btn.dataset.action;
      const id = btn.dataset.id;

      if (action === "helpful") {
        const icon = btn.querySelector("i");
        const liked = btn.classList.toggle("active");
        icon.className = liked ? "fa-solid fa-heart" : "fa-regular fa-heart";
      } else if (action === "reply") {
        const textarea = document.getElementById("comment-body");
        textarea.focus();
        textarea.value = `@${btn.closest(".disc-comment").querySelector(".disc-commenter").textContent} `;
      } else if (action === "edit") {
        alert("Edit functionality - to be implemented");
    });
  });
</script>"""

new_js = """<script>
  /* ---- Character counter ---- */
  const textarea = document.getElementById("comment-body");
  const charsLeft = document.getElementById("chars-left");
  if (textarea) {
    textarea.addEventListener("input", () => {
      charsLeft.textContent = 1200 - textarea.value.length;
    });
  }

  /* ---- Sort buttons ---- */
  const sortBtns = document.querySelectorAll(".disc-sort-btn");
  sortBtns.forEach((btn) => {
    btn.addEventListener("click", () => {
      sortBtns.forEach((b) => b.classList.remove("active"));
      btn.classList.add("active");
      const list = document.getElementById("commentList");
      const items = [...list.querySelectorAll(".disc-comment")];
      const sort = btn.dataset.sort;
      items.sort((a, b) => {
        if (sort === "newest") return b.dataset.created - a.dataset.created;
        if (sort === "oldest") return a.dataset.created - b.dataset.created;
        if (sort === "top") return b.dataset.likes - a.dataset.likes;
        return 0;
      });
      items.forEach((el) => list.appendChild(el));
    });
  });

  /* ---- Action buttons (Helpful, Reply, Edit, Delete) ---- */
  document.querySelectorAll(".disc-action-btn").forEach((btn) => {
    btn.addEventListener("click", () => {
      const action = btn.dataset.action;
      const id = btn.dataset.id;

      if (action === "helpful") {
        const icon = btn.querySelector("i");
        const liked = btn.classList.toggle("active");
        icon.className = liked ? "fa-solid fa-heart" : "fa-regular fa-heart";
      } else if (action === "reply") {
        const replyTextarea = document.getElementById("comment-body");
        replyTextarea.focus();
        replyTextarea.value = `@${btn.closest(".disc-comment").querySelector(".disc-commenter").textContent} `;
      } else if (action === "edit") {
        alert("Edit functionality - to be implemented");
      } else if (action === "delete") {
        if (confirm("Delete this comment?")) {
          btn.closest(".disc-comment").remove();
        }
      }
    });
  });
</script>"""

if old_js in content:
    content = content.replace(old_js, new_js)
    print("JS block fixed.")
else:
    print("WARNING: JS block not found — manual check needed.")

with open(path, "w", encoding="utf-8") as f:
    f.write(content)

# Verify
with open(path, "r", encoding="utf-8") as f:
    lines = f.readlines()

print(f"File written: {len(lines)} lines")
for i, line in enumerate(lines, 1):
    if "endblock" in line or "block content" in line or "block extra_js" in line:
        print(f"  Line {i}: {line.rstrip()}")
print("Done.")
