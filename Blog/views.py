import django.db
from django.contrib import messages
from django.urls import reverse
from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.contrib.auth.models import User
from django.http import Http404
from django.shortcuts import get_object_or_404
from .models import Blog


# Create your views here.
def home_view(request):
    """
    Home Page of the Web App

    :param request:
    :return:
    """
    blogs = Blog.objects.filter(status="PB")
    if len(blogs) > 8:
        blogs = blogs[:8]
    return render(request, "index.html", {'blogs': blogs})


def blog_view(request, blog_id):
    blog = get_object_or_404(Blog, pk=blog_id)
    if blog == Http404:
        messages.error(request, "Blog not found!")
        return redirect("home")
    
    return render(request, "blog.html", {'blog': blog})


def create_blog(request):
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
        if request.user.is_authenticated:
            title = request.POST["title"]
            content = request.POST["content"]
            author = request.user
            blog = Blog.objects.create(title=title, content=content, author=author)
            blog.save()
            messages.success(request, "Your blog has been created!")
            return redirect("blog-view", blog_id=blog.id)
        else:
            messages.error(request, "You must be logged in to create a blog.")
            return redirect("login")


def edit_blog(request, blog_id):
    blog = get_object_or_404(Blog, pk=blog_id)
    if blog == Http404:
        messages.error(request, "Blog not found!")
        return redirect("home")

    # To create a blog = GET, to edit a blog = POST
    if request.method == "GET":
        return render(request, "new_blog.html", {'blog': blog, "edit": True})
    elif request.method == "POST":
        if blog.author != request.user:
            messages.error(request, "You cannot edit this blog!")
            return redirect("blog-view", blog_id=blog_id)
        
        blog.title = request.POST["title"]
        blog.content = request.POST["content"]
        blog.save()
        messages.success(request, "Your blog has been updated!")
        return redirect("blog-view", blog_id=blog_id)


def delete_blog(request, blog_id, *args, **kwargs):
    blog = get_object_or_404(Blog, pk=blog_id)

    if blog == Http404:
        messages.error(request, "Blog not found!")
        return redirect("home")

    if blog.author != request.user:
        messages.error(request, "You cannot delete this blog!")
        return redirect("blog-view", blog_id=blog_id)
    
    blog.delete()
    messages.success(request, "Your blog has been deleted!")
    return redirect("profile-view")
