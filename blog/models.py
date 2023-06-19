from django.db import models
from ckeditor.fields import RichTextField
from django.utils import timezone
from members.models import CustomUser


class Blog(models.Model):
    class Meta:
        ordering = ['-add_time']

    title = models.CharField(max_length=200)
    text = RichTextField(blank=True, null=True)
    photo = models.ImageField(upload_to='images/', blank=True)
    add_time = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return f"{self.title}"

    @property
    def views_count(self):
        return PostViews.objects.filter(post=self).count()


class PostViews(models.Model):
    IPAddres = models.GenericIPAddressField(default="45.243.82.169")
    post = models.ForeignKey(Blog, on_delete=models.CASCADE)

    def __str__(self):
        return '{} in {} post'.format(self.IPAddres, self.post.title)


class Comment(models.Model):
    article = models.ForeignKey(Blog, on_delete=models.CASCADE)
    body = RichTextField()
    created_on = models.DateTimeField(default=timezone.now)
    subscriber = models.ForeignKey(CustomUser, on_delete=models.CASCADE)

    def __str__(self):
        return self.article.title
