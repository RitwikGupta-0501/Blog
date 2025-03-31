from django.db import models
from django.utils import timezone
from django.conf import settings
from django.utils.text import slugify
from django.urls import reverse
from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.db.models import Q


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
        verbose_name = "Blog Post"
        verbose_name_plural = "Blog Posts"

    title = models.CharField(max_length=100, help_text="Enter the title of the blog post.")
    content = models.TextField(help_text="Write the content of the blog post.")
    pub_date = models.DateTimeField(default=timezone.now, blank=True, help_text="The date and time the blog post was published.")
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="blog_posts")
    slug = models.SlugField(unique=True, help_text="Unique identifier for the blog post (auto-generated).")
    status = models.CharField(
        max_length=2,
        choices=Status.choices,
        default=Status.DRAFT,
        help_text="The publication status of the blog post."
    )

    def __str__(self):
        return f"{self.title} by {self.author}"

    def get_absolute_url(self):
        return reverse("blog-view", kwargs={"slug": self.slug})


@receiver(pre_save, sender=Blog)
def generate_slug(sender, instance, **kwargs):
    if not instance.slug:
        base_slug = slugify(instance.title)
        slug = base_slug
        counter = 1
        while Blog.objects.filter(Q(slug=slug) & ~Q(id=instance.id)).exists():
            slug = f"{base_slug}-{counter}"
            counter += 1
        instance.slug = slug