from django.shortcuts import render, get_object_or_404
from django.utils import timezone
from .models import Blog, Category


def index(request):
    posts = Blog.objects.filter(posted_on__lte=timezone.now()).order_by('posted_on')
    return render(request, 'blog/index.html', {'posts': posts})


def blog_detail(request, slug, pk):
    post = get_object_or_404(Blog, pk=pk)
    return render(request, 'blog/blog_detail.html', {'post': post})
