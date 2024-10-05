from django.db import models
from django.utils import timezone
from django.conf import settings


# Create your models here.
class Blog(models.Model):

    class Status(models.TextChoices):
        DRAFT = 'DF', 'Draft'
        PUBLISHED = 'PB', 'Published'

    class Meta:
        ordering = ["-pub_date"]
        indexes = [
            models.Index(fields=['-pub_date']),
        ]

    title = models.CharField(max_length=100)
    content = models.TextField()
    pub_date = models.DateTimeField(default=timezone.now, blank=True)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="blog_posts")
    slug = models.SlugField(unique=True)
    status = models.CharField(
        max_length=2,
        choices=Status,
        default=Status.DRAFT
    )

    def __str__(self):
        return f"{self.title} by {self.author}"