from django.urls import path
from . import views

urlpatterns = [
    path('', views.home_view, name='home'),
    path('blog/<int:blog_id>/', views.blog_view, name='blog-view'),
    path('blog/<int:blog_id>/edit/', views.edit_blog, name='edit-blog'),
    path('blog/<int:blog_id>/delete/', views.delete_blog, name='delete-blog'),
    path('create-blog/', views.create_blog, name='create-blog'),
]