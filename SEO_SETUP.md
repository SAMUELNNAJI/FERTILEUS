# SEO Configuration for FertileUs

## ✅ Configured Features

### 1. XML Sitemap (`/sitemap.xml`)
Your sitemap automatically includes:

#### **Static Pages Sitemap** (monthly updates)
- Home (priority: 1.0)
- About (priority: 0.7)
- Egg Donation (priority: 0.7)
- Calculator (priority: 0.7)
- Blog (priority: 0.7)
- Contact (priority: 0.7)

#### **Blog Posts Sitemap** (weekly updates)
- All published blog posts (priority: 0.8)
- Automatic last-modified date tracking
- Updates weekly

#### **Image Sitemap** (weekly updates)
- All blog post featured images
- Includes image title and caption
- Helps with Google Image Search indexing
- Priority: 0.6

### 2. Robots.txt (`/robots.txt`)
```
User-agent: *
Allow: /

# Disallow admin and private areas
Disallow: /admin/
Disallow: /ai-bot/

# Sitemap location
Sitemap: https://fertileus.com.ng/sitemap.xml
```

**What this does:**
- ✅ Allows all search engines to crawl public pages
- 🚫 Blocks crawling of admin panel (`/admin/`)
- 🚫 Blocks crawling of AI bot chat pages (`/ai-bot/`)
- 📍 Points search engines to your sitemap

### 3. SEO Meta Tags (Already in templates)
Every page includes:
- Unique page titles
- Meta descriptions
- Canonical URLs
- Open Graph tags (Facebook/LinkedIn sharing)
- Twitter Card tags
- Structured data (JSON-LD for blog posts)

## 🚀 Next Steps

### Submit to Search Engines

1. **Google Search Console**
   - Go to: https://search.google.com/search-console
   - Add your property: `https://fertileus.com.ng`
   - Submit sitemap: `https://fertileus.com.ng/sitemap.xml`

2. **Bing Webmaster Tools**
   - Go to: https://www.bing.com/webmasters
   - Add your site
   - Submit sitemap: `https://fertileus.com.ng/sitemap.xml`

### Verify Your Setup

Test that everything works:
```bash
# View your sitemap
curl https://fertileus.com.ng/sitemap.xml

# View your robots.txt
curl https://fertileus.com.ng/robots.txt
```

Or visit in browser:
- https://fertileus.com.ng/sitemap.xml
- https://fertileus.com.ng/robots.txt

## 📊 What Gets Indexed

### ✅ Indexed (Allowed)
- Homepage
- About page
- Egg Donation page
- Calculator
- Blog listing
- Individual blog posts
- Contact page
- All blog post images

### 🚫 Not Indexed (Blocked)
- Admin panel (`/admin/`)
- AI bot chat interface (`/ai-bot/`)

## 🔧 Maintenance

The sitemaps update automatically:
- **When you publish a new blog post** → automatically added to sitemap
- **When you add a featured image** → automatically added to image sitemap
- **When you update a blog post** → last-modified date updates

No manual intervention needed!

## 📝 Technical Details

### Sitemap Files Location
- Main configuration: `FertileUs/urls.py`
- Sitemap classes: `Home/sitemaps.py`

### Image Sitemap Details
The image sitemap includes:
- Image URL (`loc`)
- Image title (blog post title)
- Image caption (first 200 chars of blog content)

This helps search engines understand your images and improves visibility in Google Images.

## 🎯 SEO Best Practices Already Implemented

✅ Mobile-responsive design
✅ Fast page load times
✅ Semantic HTML structure
✅ Proper heading hierarchy (H1, H2, H3)
✅ Alt text for images
✅ Clean, descriptive URLs
✅ HTTPS (secure connection)
✅ Structured data markup
✅ Social media meta tags

---

**Last Updated:** 2026
**Site:** https://fertileus.com.ng
