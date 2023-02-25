from django.db import models
from django_countries.fields import CountryField
from django.contrib.auth.models import AbstractUser
from django.utils import timezone
from django.core.files.storage import FileSystemStorage
import os 
from django.template.defaultfilters import slugify
import uuid

fs = FileSystemStorage()
STATUS = (
    (0,"Draft"),
    (1,"Publish")
)


class CustomUser(AbstractUser):
    resume = models.TextField(max_length=10000, null=True)
    age = models.DateField(null=True, blank=True)
    profile_image = models.ImageField(storage=fs, blank=True, null=True)
    verification_image = models.ImageField(storage=fs, blank=True, null=True)
    country = CountryField(null=True)
    interest = models.TextField(max_length=1000, null=True, blank=True)
    is_active = models.BooleanField(default=False)
    created_at = models.DateTimeField(default=timezone.now)
    # add additional fields in here


    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

    def __str__(self):
        return self.username



class Tag(models.Model):
    name = models.CharField(max_length=50, unique=True)
    slug = models.SlugField(max_length=255, unique=True, default=uuid.uuid1)


    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(Tag, self).save(*args, **kwargs)
 

class Post(models.Model):
    class Meta:
        ordering = ["-publish_date"]

    title = models.CharField(max_length=255, unique=True)
    subtitle = models.CharField(max_length=255, blank=True)
    slug = models.SlugField(max_length=255, unique=True, default=uuid.uuid1)
    body = models.TextField()
    meta_description = models.CharField(max_length=150, blank=True)
    date_created = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)
    publish_date = models.DateTimeField(default=timezone.now, blank=True, null=True)
    published = models.BooleanField(default=False)
    status = models.IntegerField(choices=STATUS, default=0)
    author = models.ForeignKey(CustomUser, on_delete=models.PROTECT)
    tags = models.ManyToManyField(Tag, blank=True)

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super(Post, self).save(*args, **kwargs)
 
class PostImage(models.Model):
    post = models.ForeignKey(Post, default=None, on_delete=models.CASCADE)
    images = models.ImageField(storage=fs, blank=True, null=True)
 
    def __str__(self):
        return self.post.title







