from django.urls import path
from . import views

urlpatterns = [
    path('', views.home_view, name='home'),
    path('blog/<slug:slug>/', views.blog_view, name='blog-view'),
    path('blog/<slug:slug>/edit/', views.edit_blog, name='edit-blog'),
    path('blog/<slug:slug>/delete/', views.delete_blog, name='delete-blog'),
    path('create-blog/', views.create_blog, name='create-blog'),
]