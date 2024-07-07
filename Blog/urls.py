from django.urls import path
from .views import *

urlpatterns = [
    path('', home_view, name='home'),
    path('login/', login_view, name='login'),
    path('register/', register_view, name='register'),
    path('logout/', logout_view, name='logout'),
    path('blog/<int:blog_id>/', blog_view, name='blog-view'),
    path('blog/<int:blog_id>/edit/', edit_blog, name='edit-blog'),
    path('blog/<int:blog_id>/delete/', delete_blog, name='delete-blog'),
]