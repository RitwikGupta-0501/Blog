from django.urls import path
from .views import *

urlpatterns = [
    path('', profile_view, name='profile-view'),
    path('create-blog/', create_blog, name='create-blog'),
]