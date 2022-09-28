from django.db import models
from django.contrib.auth import get_user_model
from ckeditor.fields import RichTextField
from django.shortcuts import reverse
# Create your models here.



class Blog(models.Model):
    class Meta:
        ordering = ['-add_time']
    # name = models.CharField(max_length=100)
    title = models.CharField(max_length=200)
    text = RichTextField(blank=True, null=True)
    photo = models.ImageField(upload_to='images/', blank=True)
    add_time = models.DateTimeField(auto_now_add=True, null=True)
    author = models.ForeignKey(
        get_user_model(),
        on_delete=models.CASCADE,
        null=True
    )
    def __str__(self):
        return f"{self.title}"




class Comment(models.Model):
    article = models.ForeignKey(Blog, on_delete=models.CASCADE, related_name='comments', null=True, blank=True)
    name = models.CharField(max_length=200, null=True, blank=True)
    body = RichTextField(null=True, blank=True)
    created_on = models.DateTimeField(auto_now_add=True, null=True)


    def __str__(self):
        return str(self.name)













