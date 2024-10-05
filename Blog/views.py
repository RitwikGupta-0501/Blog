import django.db
from django.contrib import messages
from django.urls import reverse
from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.contrib.auth.models import User
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


def register_view(request):
    """
    Handles Registrations of the Web App.\n
    If POST --> Database updates\n
    Else --> Renders the form

    :param request:
    :returns HTML render:
    """
    if not request.user.is_authenticated:
        if request.method == "POST":
            if request.POST["password1"] == request.POST["password2"]:
                try:
                    user = User.objects.create_user(username=request.POST["username"], password=request.POST["password1"])
                    user.save()
                    login(request, user)
                    return redirect("home")
                except django.db.IntegrityError as _:
                    messages.error(request, "Username Already exists.")
            else:
                messages.error(request, "Passwords do not match.")
        return render(request, "register.html")
    return redirect("home")


def authenticate_user(username:str, password:str) -> int:
    try:
        user = User.objects.get(username=username)
        if user.check_password(password):
            return 1
        else:
            return 0
    except User.DoesNotExist:
        return -1


def login_view(request):
    """
    Handles Login of User.
    If POST --> Authenticates and Logs In\n
    Else --> Renders the form

    :param request:
    :return:
    """
    if not request.user.is_authenticated:
        if request.method == "POST":
            username = request.POST["username"]
            password = request.POST["password1"]
            checked = authenticate_user(username, password)
            if checked == 1:
                login(request, User.objects.get(username=username))
                return redirect("home")
            elif checked == 0:
                messages.error(request, "Invalid Username or Password.")
            else:
                messages.error(request,
                               'User doesn\'t exist. <a class="alert-link" href="{}">Click here to create an account.</a>'.format(
                                   reverse('register')))
        return render(request, "login.html")
    return redirect("home")


def logout_view(request):
    """
    Handles user logout.

    :param request:
    :return:
    """
    logout(request)
    messages.info(request, "Successfully Logged Out!")
    return redirect('home')


def blog_view(request, blog_id):
    blog = Blog.objects.get(id=blog_id)
    return render(request, "blog.html", {'blog': blog})


def edit_blog(request, blog_id):
    if request.method == "GET":
        blog = Blog.objects.get(id=blog_id)
        return render(request, "new_blog.html", {'blog': blog, "edit": True})
    elif request.method == "POST":
        blog = Blog.objects.get(id=blog_id)
        title = request.POST["title"]
        content = request.POST["content"]
        blog.title = title
        blog.content = content
        blog.save()
        messages.success(request, "Your blog has been updated!")
        return redirect("blog-view", blog_id=blog_id)


def delete_blog(request, blog_id):
    Blog.objects.filter(id=blog_id).delete()
    messages.success(request, "Your blog has been deleted!")
    return redirect("profile-view")
