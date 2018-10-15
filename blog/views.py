from distutils import errors

from django.db import transaction
from django.shortcuts import render, get_object_or_404
from django.utils import timezone
from .models import Blog, Category


def index(request, slug):
    categories = Category.objects.all()
    category = categories.filter(slug=slug).get()
    posts = Blog.objects.filter(category=category.id, posted_on__lte=timezone.now()).order_by('posted_on')
    return render(request, 'blog/index.html', {'posts': posts, 'categories': categories, 'cat_slug': slug})


def blog_detail(request, cat_slug, slug, pk):
    post = Blog.increment_view(pk=pk)
    return render(request, 'blog/blog_detail.html', {'post': post})


def home(request):
    categories = Category.objects.all()[:4]
    carousel_blogs = Blog.objects.filter(posted_on__lte=timezone.now()).order_by('posted_on')[:4]
    popular_blogs = Blog.objects.filter(posted_on__lte=timezone.now()).order_by('views')[:6]
    return render(request, 'blog/home.html',
                  {'carousel_blogs': carousel_blogs, 'popular_blogs': popular_blogs, 'categories': categories})
