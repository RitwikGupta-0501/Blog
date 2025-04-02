from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError


# Create your views here.
@login_required
def profile_view(request):
    blogs = request.user.blog_posts.all()
    return render(request, "profile.html", {'blogs': blogs})


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
                except IntegrityError as _:
                    messages.error(request, "Username Already exists.")
            else:
                messages.error(request, "Passwords do not match.")
        return render(request, "register.html")
    return redirect("home")


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
            user = authenticate(request, username, password)
            if user is not None:
                login(request, user)
                return redirect("home")
            else:
                messages.error(request, "Invalid Username or Password.")
        return render(request, "login.html")
    return redirect("home")


@login_required
def logout_view(request):
    """
    Handles user logout.

    :param request:
    :return:
    """
    logout(request)
    messages.info(request, "Successfully Logged Out!")
    return redirect('home')

