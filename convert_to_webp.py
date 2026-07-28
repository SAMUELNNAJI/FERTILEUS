from PIL import Image
import os

# Image files to convert
images_to_convert = [
    'static/assests/image/Fertility.jpg',
    'static/assests/image/about.jpg',
    'static/assests/image/donations.jpg',
    'static/assests/image/fertility education.jpg',
    'static/assests/image/hero-image.jpg',
    'static/assests/image/pregancy.jpg',
]

for image_path in images_to_convert:
    if os.path.exists(image_path):
        try:
            img = Image.open(image_path)
            webp_path = image_path.replace('.jpg', '.webp')
            img.save(webp_path, 'webp', quality=85, method=6)
            print(f'Converted: {image_path} -> {webp_path}')
        except Exception as e:
            print(f'Error converting {image_path}: {e}')
    else:
        print(f'File not found: {image_path}')

print('Conversion complete!')
