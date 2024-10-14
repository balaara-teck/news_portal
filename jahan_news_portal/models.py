
from django.db import models
from django.contrib.auth.models import User


class NewsModel(models.Model):
    title = models.CharField(max_length=150)
    category = models.CharField(max_length=70)
    body = models.TextField()
    comments = models.PositiveIntegerField()
    approved = models.BooleanField(default=False)
    date = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return f"{self.title}"
    
class CommentNewsModel(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    news = models.ForeignKey(NewsModel,on_delete=models.CASCADE)
    body = models.TextField()
    date = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return f"{self.user}"

class ReplyComment(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    comment = models.ForeignKey(CommentNewsModel,on_delete=models.CASCADE)
    body = models.TextField()
    date = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return f"{self.user}"