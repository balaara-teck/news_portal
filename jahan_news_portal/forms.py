from django import forms
from .models import NewsModel,CommentNewsModel,ReplyComment
from allauth.account.forms import LoginForm,SignupForm

class UserLoginForm(LoginForm):

    def login(self, *args, **kwargs):
        return super(UserLoginForm, self).login(*args, **kwargs)
    
class UserSignupForm(SignupForm):

    def save(self, request):
        user = super(UserSignupForm, self).save(request)
        user.save()
        return user

class NewsForm(forms.ModelForm):

    class Meta:
        model = NewsModel
        fields = ["title","category","body"]

class CommentNewsForm(forms.ModelForm):

    class Meta:
        model = CommentNewsModel
        fields = ["body"]

class ReplyCommentForm(forms.ModelForm):
    class Meta:
        model = CommentNewsModel
        fields = ["body"]