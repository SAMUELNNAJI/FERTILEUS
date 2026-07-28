"""
Image optimization utilities for FertileUs.
Automatically resizes and compresses images on upload.
"""
from PIL import Image
from io import BytesIO
from django.core.files.uploadedfile import InMemoryUploadedFile
import sys


def optimize_image(image_field, max_width=1920, max_height=1080, quality=85):
    """
    Optimize an uploaded image by:
    - Resizing to max dimensions while maintaining aspect ratio
    - Converting to RGB if necessary
    - Compressing with specified quality
    - Keeping original format (JPEG, PNG, WebP)
    
    Args:
        image_field: Django ImageField instance
        max_width: Maximum width in pixels (default: 1920)
        max_height: Maximum height in pixels (default: 1080)
        quality: JPEG/WebP quality 1-100 (default: 85)
    
    Returns:
        Optimized InMemoryUploadedFile ready to save
    """
    if not image_field:
        return None
    
    try:
        # Open the image
        img = Image.open(image_field)
        
        # Convert RGBA to RGB if saving as JPEG
        if img.mode in ('RGBA', 'LA', 'P') and image_field.name.lower().endswith(('.jpg', '.jpeg')):
            # Create white background
            background = Image.new('RGB', img.size, (255, 255, 255))
            if img.mode == 'P':
                img = img.convert('RGBA')
            background.paste(img, mask=img.split()[-1] if img.mode == 'RGBA' else None)
            img = background
        elif img.mode not in ('RGB', 'RGBA'):
            img = img.convert('RGB')
        
        # Calculate new dimensions maintaining aspect ratio
        width, height = img.size
        if width > max_width or height > max_height:
            # Calculate scaling factor
            ratio = min(max_width / width, max_height / height)
            new_width = int(width * ratio)
            new_height = int(height * ratio)
            
            # Resize using high-quality Lanczos filter
            img = img.resize((new_width, new_height), Image.Resampling.LANCZOS)
        
        # Save to BytesIO
        output = BytesIO()
        
        # Determine format
        img_format = 'JPEG'
        if image_field.name.lower().endswith('.png'):
            img_format = 'PNG'
            # Optimize PNG
            img.save(output, format='PNG', optimize=True)
        elif image_field.name.lower().endswith('.webp'):
            img_format = 'WEBP'
            img.save(output, format='WEBP', quality=quality, method=6)
        else:
            # Default to JPEG with quality compression
            img_format = 'JPEG'
            img.save(output, format='JPEG', quality=quality, optimize=True)
        
        output.seek(0)
        
        # Create new InMemoryUploadedFile
        return InMemoryUploadedFile(
            output,
            'ImageField',
            image_field.name,
            f'image/{img_format.lower()}',
            sys.getsizeof(output),
            None
        )
    
    except Exception as e:
        print(f"Image optimization error: {e}")
        # Return original if optimization fails
        return image_field


def create_thumbnail(image_field, max_size=400, quality=80):
    """
    Create a thumbnail version of an image.
    
    Args:
        image_field: Django ImageField instance
        max_size: Maximum dimension (width or height) in pixels
        quality: Compression quality 1-100
    
    Returns:
        Optimized thumbnail as InMemoryUploadedFile
    """
    return optimize_image(image_field, max_width=max_size, max_height=max_size, quality=quality)
