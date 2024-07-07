from django.shortcuts import render, redirect
from django.contrib import messages
from Blog.models import Blog


# Create your views here.
def profile_view(request):
    blogs = request.user.blog_set.all()
    return render(request, "profile.html", {'blogs': blogs})


def create_blog(request):
    if request.method == "POST":
        blog = Blog()
        blog.title = request.POST['title']
        blog.content = request.POST['content']
        blog.author = request.user
        blog.save()
        messages.success(request, "Your blog has been created!")
        return redirect("home")
    else:
        return render(request, 'new_blog.html')
