from django.db import models
from django.contrib.auth.models import User


class Post(models.Model):
    created = models.DateField(auto_now_add=True)
    title = models.CharField(max_length=100)
    post_text = models.TextField(default="Comment")
    author = models.ForeignKey(User, on_delete=models.CASCADE)


class Comment(models.Model):
    created = models.DateField(auto_now_add=True)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    comment_text = models.TextField(default="Comment")


class Like(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='likes')
    user = models.ForeignKey(User, on_delete=models.CASCADE)