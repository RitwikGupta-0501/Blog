from django.contrib import messages
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.shortcuts import render, redirect
from django.core.exceptions import ValidationError

# Helper Functions
def unauthenticated_user(view_func):
    """
    Decorator to check if user is authenticated.
    If not, redirect to login page.

    :param view_func:
    :return:
    """
    def wrapper(request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect("home")
        else:
            return view_func(request, *args, **kwargs)
    return wrapper


# Django Views
@login_required
def profile_view(request):
    blogs = request.user.blog_posts.all()
    return render(request, "profile.html", {'blogs': blogs})


@unauthenticated_user
def register_view(request):
    """
    Handles Registrations of the Web App.\n
    If POST --> Database updates\n
    Else --> Renders the form

    :param request:
    :returns HTML render:
    """
    if request.method == "POST":
        if request.POST["password1"] == request.POST["password2"]:
            try:
                validate_password(request.POST["password1"])
                user = User.objects.create_user(username=request.POST["username"], password=request.POST["password1"])
                user.save()
                login(request, user)
                messages.success(request, "Registration successful!")
                return redirect("home")
            except ValidationError as e:
                for error in e.messages:
                    messages.error(request, error)
            except IntegrityError as _:
                messages.error(request, "Username Already exists.")
        else:
            messages.error(request, "Passwords do not match.")
    return render(request, "register.html")


@unauthenticated_user
def login_view(request):
    """
    Handles Login of User.
    If POST --> Authenticates and Logs In\n
    Else --> Renders the form

    :param request:
    :return:
    """
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password1"]
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect("home")
        else:
            messages.error(request, "Invalid Username or Password.")
    return render(request, "login.html")


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

