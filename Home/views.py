from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from .models import Blog, Comment
from .forms import CommentForm
from django.contrib import messages


def error_404(request, exception=None):
    return render(request, 'home/404.html', status=404)


def error_500(request):
    return render(request, 'home/500.html', status=500)


def error_403(request, exception=None):
    return render(request, 'home/403.html', status=403)


def home(request):
    posts = Blog.objects.filter(published=True)[:3]
    return render(request, 'home/index.html', {'posts': posts})


def about(request):
    return render(request, 'home/about.html')


def egg_donation(request):
    return render(request, 'home/egg-donation.html')


def calculator(request):
    return render(request, 'home/calculator.html')


def blog(request):
    category = request.GET.get('category', 'all')
    posts = Blog.objects.filter(published=True)
    if category != 'all':
        posts = posts.filter(blog_category=category)
    return render(request, 'home/blog.html', {
        'posts': posts,
        'active_category': category,
    })


def blog_post(request, slug):
    post     = get_object_or_404(Blog, blog_slug=slug, published=True)
    comments = post.comments.filter(approved=True, parent=None)

    # Related posts: same category, exclude current, max 3
    related_posts = (
        Blog.objects
        .filter(published=True, blog_category=post.blog_category)
        .exclude(pk=post.pk)[:3]
    )

    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.blog = post
            if not comment.name:
                comment.name = 'Anonymous'
            # Handle reply parent
            parent_id = request.POST.get('parent_id')
            if parent_id:
                comment.parent = get_object_or_404(Comment, id=parent_id)
            comment.save()
            messages.success(request, 'Your comment has been posted successfully.')
            return redirect('blog_post', slug=slug)
    else:
        form = CommentForm()

    return render(request, 'home/blog-post.html', {
        'post':          post,
        'comments':      comments,
        'related_posts': related_posts,
        'form':          form,
    })


def delete_comment(request, comment_id):
    comment = get_object_or_404(Comment, id=comment_id)
    slug = comment.blog.blog_slug
    comment.delete()
    messages.success(request, 'Your comment has been deleted successfully.')
    return redirect('blog_post', slug=slug)


def edit_comment(request, comment_id):
    comment = get_object_or_404(Comment, id=comment_id)
    slug = comment.blog.blog_slug
    
    if request.method == 'POST':
        form = CommentForm(request.POST, instance=comment)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your comment has been edited successfully.')
            return redirect('blog_post', slug=slug)
        else:
            messages.error(request, 'Error editing your comment.')
            return redirect('blog_post', slug=slug)
    
    return redirect('blog_post', slug=slug)


def like_comment(request, comment_id):
    comment = get_object_or_404(Comment, id=comment_id)
    comment.likes += 1
    comment.save()
    return JsonResponse({'likes': comment.likes})


def contact(request):
    return render(request, 'home/contact.html')
