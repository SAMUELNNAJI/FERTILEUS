from django.db import models
from django.contrib.auth import get_user_model
from django.utils.text import slugify
from .image_optimizer import optimize_image

User = get_user_model()


CATEGORY_CHOICES = [
    ('Fertility', 'Fertility'),
    ('Pregnancy', 'Pregnancy'),
    ('Donation',  'Donation'),
]


class Blog(models.Model):
    blog_title    = models.CharField(max_length=200)
    blog_slug     = models.SlugField(max_length=220, unique=True, blank=True)
    blog_content  = models.TextField()
    # Uploads route to ImageKit CDN via DEFAULT_FILE_STORAGE in settings.py
    # Files land at: https://ik.imagekit.io/fertileus/blog/
    blog_image    = models.ImageField(upload_to='blog/', blank=True, null=True)
    blog_category = models.CharField(max_length=20, choices=CATEGORY_CHOICES, default='Fertility')
    blog_author   = models.CharField(max_length=100, default='Dr. Cee Fertility')
    blog_read_time = models.PositiveSmallIntegerField(default=5, help_text='Minutes to read')
    blog_date     = models.DateTimeField(auto_now_add=True)
    published     = models.BooleanField(default=True)

    class Meta:
        verbose_name        = 'Blog Post'
        verbose_name_plural = 'Blog Posts'
        ordering            = ['-blog_date']

    def __str__(self):
        return self.blog_title

    def save(self, *args, **kwargs):
        if not self.blog_slug:
            self.blog_slug = slugify(self.blog_title)
        
        # Optimize image before saving
        if self.blog_image:
            self.blog_image = optimize_image(
                self.blog_image,
                max_width=1920,
                max_height=1080,
                quality=85
            )
        
        super().save(*args, **kwargs)

    def approved_comments(self):
        return self.comments.filter(approved=True)


class Comment(models.Model):
    blog      = models.ForeignKey(Blog, on_delete=models.CASCADE, related_name='comments')
    parent    = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='replies')
    name      = models.CharField(max_length=80, blank=True, default='Anonymous')
    user      = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='comments')
    body      = models.TextField(max_length=1200)
    created   = models.DateTimeField(auto_now_add=True)
    approved  = models.BooleanField(default=True)
    likes     = models.PositiveIntegerField(default=0)

    class Meta:
        verbose_name        = 'Comment'
        verbose_name_plural = 'Comments'
        ordering            = ['created']

    def __str__(self):
        display_name = self.name if self.name else 'Anonymous'
        return f'{display_name} on "{self.blog.blog_title}"'
