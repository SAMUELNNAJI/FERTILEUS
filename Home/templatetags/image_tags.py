"""
Custom template tags for optimized image rendering.
Provides lazy loading, responsive images, and ImageKit CDN transformations.
"""
from django import template
from django.utils.safestring import mark_safe
from urllib.parse import urlparse

register = template.Library()


@register.simple_tag
def responsive_img(image_url, alt_text="", css_class="", width=None, height=None, loading="lazy"):
    """
    Render an optimized, responsive image with lazy loading.
    
    Usage in templates:
        {% load image_tags %}
        {% responsive_img post.blog_image.url post.blog_title "journal-img" %}
    
    Args:
        image_url: URL of the image
        alt_text: Alt text for accessibility
        css_class: CSS classes to apply
        width: Optional width attribute
        height: Optional height attribute
        loading: Loading strategy ("lazy" or "eager")
    
    Returns:
        HTML img tag with optimization attributes
    """
    if not image_url:
        return ''
    
    # Build attributes
    attrs = []
    attrs.append(f'src="{image_url}"')
    attrs.append(f'alt="{alt_text}"')
    
    if css_class:
        attrs.append(f'class="{css_class}"')
    
    if width:
        attrs.append(f'width="{width}"')
    
    if height:
        attrs.append(f'height="{height}"')
    
    # Add loading attribute (lazy by default)
    attrs.append(f'loading="{loading}"')
    
    # Add decoding attribute for better performance
    attrs.append('decoding="async"')
    
    return mark_safe(f'<img {" ".join(attrs)} />')


@register.simple_tag
def imagekit_transform(image_url, width=None, height=None, quality=85, format=None):
    """
    Generate ImageKit CDN transformation URL.
    
    Usage:
        {% imagekit_transform post.blog_image.url width=800 quality=80 %}
    
    Args:
        image_url: Original ImageKit URL
        width: Target width
        height: Target height
        quality: JPEG/WebP quality (1-100)
        format: Output format (webp, jpg, png)
    
    Returns:
        Transformed ImageKit URL
    """
    if not image_url or 'imagekit.io' not in image_url:
        return image_url
    
    # Parse the URL
    parsed = urlparse(image_url)
    path_parts = parsed.path.split('/')
    
    # Build transformation string
    transformations = []
    
    if width:
        transformations.append(f'w-{width}')
    
    if height:
        transformations.append(f'h-{height}')
    
    if quality and quality != 85:
        transformations.append(f'q-{quality}')
    
    if format:
        transformations.append(f'f-{format}')
    
    # Add auto optimization
    transformations.append('fo-auto')
    
    # Construct transformed URL
    if transformations:
        # Insert transformation string after /tr/
        transform_string = ','.join(transformations)
        
        # Check if URL already has transformations
        if '/tr:' in image_url or '/tr/' in image_url:
            # Replace existing transformations
            base_url = image_url.split('/tr')[0]
            file_path = '/' + '/'.join(path_parts[-2:])  # Get last 2 parts (folder/filename)
            return f"{base_url}/tr:{transform_string}{file_path}"
        else:
            # Add new transformations
            base_url = parsed.scheme + '://' + parsed.netloc
            file_path = parsed.path
            return f"{base_url}/tr:{transform_string}{file_path}"
    
    return image_url


@register.inclusion_tag('home/partials/responsive_picture.html')
def picture_tag(image_url, alt_text="", css_class="", sizes="100vw"):
    """
    Render a <picture> element with multiple sources for responsive images.
    Provides WebP format with JPEG fallback.
    
    Usage:
        {% picture_tag post.blog_image.url post.blog_title "hero-img" %}
    
    Args:
        image_url: Base image URL
        alt_text: Alt text for accessibility
        css_class: CSS classes
        sizes: Sizes attribute for responsive images
    
    Returns:
        Context dict for the template
    """
    return {
        'image_url': image_url,
        'alt_text': alt_text,
        'css_class': css_class,
        'sizes': sizes,
    }
