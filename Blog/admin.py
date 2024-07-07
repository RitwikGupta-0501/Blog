from django.contrib import admin
from .models import Blog
from django.http import Http404
from django.urls import reverse


class RestrictStaffToAdminMiddleware(object):
    """
    A middleware that restricts staff members access to administration panels.
    """

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):

        if request.path.startswith(reverse("admin:index")):
            if request.user.is_authenticated:
                if not request.user.is_staff:
                    raise Http404
            else:
                raise Http404

        return self.get_response(request)

# Register your models here.
admin.site.register(Blog)
