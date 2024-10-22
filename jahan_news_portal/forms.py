from django import forms
from .models import NewsModel,CommentNewsModel,UserProfileModel
from allauth.account.forms import LoginForm,SignupForm
from django.contrib.auth.models import User


class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfileModel  # Link to the UserProfileModel
        fields = ["image"]  # Specify which fields to include in the form





class UserLoginForm(LoginForm):

    def login(self, *args, **kwargs):
        return super(UserLoginForm, self).login(*args, **kwargs)

class UserSignupForm(SignupForm):
    image = forms.ImageField(required=False)

    def save(self, request):
        user = super(UserSignupForm, self).save(request)
        user.image = self.cleaned_data.get('image')
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
