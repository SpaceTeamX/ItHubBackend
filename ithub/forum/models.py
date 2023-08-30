from django.db import models
from taggit.managers import TaggableManager
from users.models import User
from ckeditor_uploader.fields import RichTextUploadingField


class Category(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()

    def __str__(self):
        return self.title


class Question(models.Model):
    title = models.CharField(max_length=200)
    categories = models.ManyToManyField(Category)
    content = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    slug = models.SlugField()
    tags = TaggableManager()

    def __str__(self):
        return self.title


class Comment(models.Model):
    content = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='comments')
    username = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_name')
    text = models.TextField()
    created_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_date']

    def __str__(self):
        return self.text
