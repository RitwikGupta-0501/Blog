from django.http import Http404
from django.shortcuts import render, redirect
from django.shortcuts import get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, EmptyPage
from .models import Blog


# Create your views here.
def home_view(request, *args, **kwargs):
    """
    Home Page of the Web App

    :param request:
    :return:
    """
    page_number = request.GET.get('page', 1)
    try:
        page_number = int(page_number)
        if page_numebr < 1:
            page_number = 1
    except ValueError:
        page_number = 1
    
    blogs = Blog.objects.filter(status=Blog.Status.PUBLISHED).select_related("author")
    
    pages = Paginator(blogs, 10)
    try:
        page = pages.get_page(page_number)
    except EmptyPage:
        page = pages.get_page(pages.count)
    
    context = {
        'blogs': page,
        'last_page': pages.count
    }
    return render(request, "index.html",context=context)


def blog_view(request, slug, *args, **kwargs):
    blog = get_object_or_404(Blog, slug=slug)    
    return render(request, "blog.html", {'blog': blog})


@login_required
def create_blog(request, *args, **kwargs):
    """
    Handles Blog Creation.
    If POST --> Creates a blog\n
    Else --> Renders the form

    :param request:
    :return:
    """
    if request.method == "GET":
        return render(request, "new_blog.html")
    elif request.method == "POST":
        title = request.POST["title"]
        content = request.POST["content"]
        author = request.user
        blog = Blog.objects.create(title=title, content=content, author=author)
        blog.save()
        messages.success(request, "Your blog has been created!")
        return redirect("blog-view", slug=blog.slug)


@login_required
def edit_blog(request, slug, *args, **kwargs):
    blog = get_object_or_404(Blog, slug=slug)

    # To create a blog = GET, to edit a blog = POST
    if request.method == "GET":
        return render(request, "new_blog.html", {'blog': blog, "edit": True})
    elif request.method == "POST":
        if blog.author != request.user:
            messages.error(request, "You cannot edit this blog!")
            return redirect("blog-view", slug=slug)
        
        blog.title = request.POST["title"]
        blog.content = request.POST["content"]
        blog.save()
        messages.success(request, "Your blog has been updated!")
        return redirect("blog-view", slug=slug)


@login_required
def delete_blog(request, slug, *args, **kwargs):
    blog = get_object_or_404(Blog, slug=slug)

    if blog.author != request.user:
        messages.error(request, "You cannot delete this blog!")
        return redirect("blog-view", slug=slug)
    
    blog.delete()
    messages.success(request, "Your blog has been deleted!")
    return redirect("profile-view")
