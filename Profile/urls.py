from django.urls import path
from .views import profile_view, create_blog

urlpatterns = [
    path('', profile_view, name='profile-view'),
    path('create-blog/', create_blog, name='create-blog'),
]