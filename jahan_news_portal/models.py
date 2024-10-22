
from django.db import models
from django.contrib.auth.models import User


class UserProfileModel(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='profile_pics/', blank=True, null=True)

    def save(self, *args, **kwargs):
            # Call the original save method to store the image
            super().save(*args, **kwargs)

            # Now update the image_urls field with the image URL if an image is provided
            if self.image:
                self.image_urls = self.image.url
                # Save again to update the image URL field
                super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.user}'s profile picture"




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
    user = models.ForeignKey(UserProfileModel,on_delete=models.CASCADE)
    news = models.ForeignKey(NewsModel,on_delete=models.CASCADE)
    body = models.TextField()
    date = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return f"{self.user}"
