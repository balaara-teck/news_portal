
from django.shortcuts import render,redirect
from django.views import View
from .forms import NewsForm,CommentNewsForm,UserLoginForm,UserSignupForm,UserProfileForm
from .models import NewsModel,CommentNewsModel,UserProfileModel
from django.views.generic.base import TemplateView
from django.urls import reverse_lazy,reverse
from django.db.models import Q
from django.contrib.auth.models import User
from allauth.account.views import LoginView,SignupView
from django.contrib import messages
from allauth.socialaccount.models import SocialAccount
from django.db.models.signals import post_save
from django.dispatch import receiver
import requests
from django.core.files.base import ContentFile
from django.contrib.auth.mixins import LoginRequiredMixin


def profile(user):
    try:
        profile, created = UserProfileModel.objects.get_or_create(user=user)
        return profile
    except:
        return None

class UserProfileView(LoginRequiredMixin,View):
    form_class = UserProfileForm
    template_name = "profile.html"
    login_url = reverse_lazy("account_login")

    def get(self, request, *args, **kwargs):
        form = self.form_class()
        return render(request, self.template_name, {"profile":profile(request.user)})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST, request.FILES)

        # Check if the form is valid
        if form.is_valid():
            # Retrieve the existing profile or create a new one
            profile, created = UserProfileModel.objects.get_or_create(user=request.user)

            # Get the uploaded image
            uploaded_image = form.cleaned_data.get("image")

            request.user.first_name = request.POST.get("first_name")
            request.user.last_name = request.POST.get("last_name")
            request.user.email = request.POST.get("email")

            request.user.save()

            # Handle image upload
            if uploaded_image:

                if profile.image:
                    profile.image.delete()
                profile.image = uploaded_image
            else:

                social_account = SocialAccount.objects.filter(user=request.user).first()
                if social_account:
                    profile_pic_url = social_account.extra_data.get('picture')
                    if profile_pic_url:
                        response = requests.get(profile_pic_url)
                        if response.status_code == 200:
                            profile.image.save(
                                f'{request.user.username}_social_profile.jpg',
                                ContentFile(response.content),
                                save=True
                            )

            profile.save()  # Save the profile (new or updated)
            return redirect(reverse_lazy("home"))

        return render(request, self.template_name, {"profile":profile(request.user)})

class UserSignupView(SignupView):
    form_class = UserSignupForm

class UserLoginView(LoginView):
    form_class = UserLoginForm


class HomeView(View):
    template_name = "index.html"
    success_url = reverse_lazy("home")

    def get(self,request):
        

        news = NewsModel.objects.all()
        context = {"news":news,"profile":profile(request.user)}
        return render(request,self.template_name,context)

class NewsView(View):
    template_name = "news.html"
    form_class = NewsForm
    success_url = reverse_lazy("home")

    def get(self,request):
        return render(self.request,self.template_name,{"profile":profile(request.user)})

    def post(self,request,*args,**kwargs):
        form = self.form_class(request.POST)

        if form.is_valid():
            news = form.save(commit=False)
            news.comments = 0
            news.save()
            return redirect(self.success_url)
        return render(request,self.template_name,{"profile":profile(request.user)})

class ReadNews(LoginRequiredMixin,View):
    template_name = "detail.html"

    def get(self,request,*args,**kwargs):

        news_id = self.kwargs.get("pk")
        news = NewsModel.objects.filter(id=news_id).first()
        comments = CommentNewsModel.objects.filter(news=news)
        no_of_comments = len(comments)
        context = {"news":news,"comments":comments,"no_of_comments":no_of_comments,"profile":profile(request.user)}

        return render(request,self.template_name,context)

    def post(self,request,*args,**kwargs):


        profile, created = UserProfileModel.objects.get_or_create(user=request.user)
        news_id = self.kwargs.get("pk")
        news = NewsModel.objects.filter(id=news_id).first()
        comments = CommentNewsModel.objects.filter(news=news)
        no_of_comments = len(comments)
        context = {"news":news,"comments":comments,"no_of_comments":no_of_comments}

        form = CommentNewsForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.user = profile
            comment.news = news
            comment.save()

            return redirect(reverse("readnews",kwargs={"pk":news_id,"title":news.title}))
        return redirect(reverse("readnews",kwargs={"pk":news_id,"title":news.title}))


class Search(View):
    template_name = "index.html"

    def get(self,request,*args,**kwargs):
        category = self.kwargs.get("category")
        news = NewsModel.objects.filter(category=category)
        return render(request,self.template_name,{"news":news,"category":category})

    def post(self,request,*args,**kwargs):
        category = request.POST["input"]
        news = NewsModel.objects.filter(
            Q(comments__icontains=category) |
            Q(title__icontains=category) |
            Q(category__icontains=category) |
            Q(body__icontains=category)
        )
        return render(request,self.template_name,{"news":news,"category":category})
