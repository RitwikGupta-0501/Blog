from django.urls import path
from . import views

urlpatterns = [
    path('', views.home_view, name='home'),
    path('login/', views.login_view, name='login'),
    path('register/', views.register_view, name='register'),
    path('logout/', views.logout_view, name='logout'),
    path('blog/<int:blog_id>/', views.blog_view, name='blog-view'),
    path('blog/<int:blog_id>/edit/', views.edit_blog, name='edit-blog'),
    path('blog/<int:blog_id>/delete/', views.delete_blog, name='delete-blog'),
]