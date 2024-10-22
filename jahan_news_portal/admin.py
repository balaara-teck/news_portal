from django.contrib import admin
from .models import NewsModel,CommentNewsModel,UserProfileModel
# Register your models here.

admin.site.register(NewsModel)
admin.site.register(CommentNewsModel)
admin.site.register(UserProfileModel)
