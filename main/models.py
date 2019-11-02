from django.db import models
from djgeojson.fields import PointField



# Create your models here.

class Blog(models.Model):
    title = models.CharField(max_length=255)
    body = models.TextField()
    date_created = models.DateTimeField(auto_now_add=True)
    last_modified = models.DateTimeField(auto_now=True)
    is_draft = models.BooleanField(default=True)
    slug = models.SlugField(max_length=100)
    categories = models.ManyToManyField('main.Category')

    def __str__(self):
        return self.title


class Comment(models.Model):
    blog = models.ForeignKey(Blog, related_name='comments', on_delete=models.CASCADE)
    text = models.TextField()
    is_active = models.BooleanField(default=True)
    date_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.text


class Category(models.Model):
    name = models.CharField(max_length=100)
    is_active = models.BooleanField(default=True)

    class Meta:
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'

    def __str__(self):
        return self.name


class Place(models.Model):
    name = models.CharField(max_length=50)
    location = PointField()

    def __str__(self):
        return self.name
