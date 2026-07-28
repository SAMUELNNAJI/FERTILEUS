"""
Django management command to optimize all existing blog images.
Run with: python manage.py optimize_images
"""
from django.core.management.base import BaseCommand
from Home.models import Blog
from Home.image_optimizer import optimize_image
from django.core.files import File
import sys


class Command(BaseCommand):
    help = 'Optimize all existing blog post images'

    def add_arguments(self, parser):
        parser.add_argument(
            '--force',
            action='store_true',
            help='Force re-optimization of all images',
        )
        parser.add_argument(
            '--quality',
            type=int,
            default=85,
            help='JPEG quality (1-100, default: 85)',
        )

    def handle(self, *args, **options):
        force = options['force']
        quality = options['quality']
        
        self.stdout.write(self.style.SUCCESS('Starting image optimization...'))
        self.stdout.write(f'Quality setting: {quality}')
        
        # Get all blog posts with images
        posts_with_images = Blog.objects.exclude(blog_image__isnull=True).exclude(blog_image='')
        total = posts_with_images.count()
        
        if total == 0:
            self.stdout.write(self.style.WARNING('No images found to optimize.'))
            return
        
        self.stdout.write(f'Found {total} blog posts with images')
        
        optimized_count = 0
        skipped_count = 0
        error_count = 0
        
        for index, post in enumerate(posts_with_images, 1):
            try:
                # Show progress
                self.stdout.write(f'[{index}/{total}] Processing: {post.blog_title[:50]}...')
                
                if post.blog_image:
                    # Open and optimize
                    optimized = optimize_image(
                        post.blog_image,
                        max_width=1920,
                        max_height=1080,
                        quality=quality
                    )
                    
                    if optimized:
                        # Save optimized image
                        old_name = post.blog_image.name
                        post.blog_image.save(old_name, File(optimized), save=False)
                        post.save(update_fields=['blog_image'])
                        
                        optimized_count += 1
                        self.stdout.write(self.style.SUCCESS(f'  ✓ Optimized: {old_name}'))
                    else:
                        skipped_count += 1
                        self.stdout.write(self.style.WARNING(f'  - Skipped (no optimization needed)'))
                else:
                    skipped_count += 1
                    self.stdout.write(self.style.WARNING(f'  - Skipped (no image)'))
                    
            except Exception as e:
                error_count += 1
                self.stdout.write(self.style.ERROR(f'  ✗ Error: {str(e)}'))
        
        # Summary
        self.stdout.write('\n' + '='*50)
        self.stdout.write(self.style.SUCCESS(f'Optimization complete!'))
        self.stdout.write(f'  Optimized: {optimized_count}')
        self.stdout.write(f'  Skipped:   {skipped_count}')
        self.stdout.write(f'  Errors:    {error_count}')
        self.stdout.write('='*50)
