from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.models import User
from django.db import IntegrityError


# Create your views here.
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

