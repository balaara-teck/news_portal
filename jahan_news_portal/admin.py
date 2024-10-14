from django.contrib import admin
from .models import NewsModel,CommentNewsModel,ReplyComment
# Register your models here.

admin.site.register(NewsModel)
admin.site.register(CommentNewsModel)
admin.site.register(ReplyComment)
