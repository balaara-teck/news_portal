
from django.shortcuts import render,redirect
from django.views import View
from .forms import NewsForm,CommentNewsForm,ReplyCommentForm,UserLoginForm,UserSignupForm
from .models import NewsModel,CommentNewsModel,ReplyComment
from django.views.generic.base import TemplateView
from django.urls import reverse_lazy,reverse
from django.db.models import Q
from allauth.account.views import LoginView,SignupView
from django.contrib import messages

class UserSignupView(SignupView):
    form_class = UserSignupForm
    
    def form_invalid(self, form):
        return super().form_invalid(form)
    
class UserLoginView(LoginView):
    form_class = UserLoginForm

class HomeView(View):
    template_name = "index.html"
    success_url = reverse_lazy("home")

    def get(self,request):
        news = NewsModel.objects.all()
        context = {"news":news}
        return render(request,self.template_name,context)
    
class NewsView(View):
    template_name = "news.html"
    form_class = NewsForm
    success_url = reverse_lazy("home")

    def get(self,request):
        return render(self.request,self.template_name)
    
    def post(self,request,*args,**kwargs):
        form = self.form_class(request.POST)

        if form.is_valid():
            news = form.save(commit=False)
            news.comments = 0
            news.save()
            return redirect(self.success_url)
        return render(request,self.template_name)

class ReadNews(View):

    template_name = "detail.html"

    def get(self,request,*args,**kwargs):

        news_id = self.kwargs.get("pk")
        news = NewsModel.objects.filter(id=news_id).first()
        comments = CommentNewsModel.objects.filter(news=news)
        no_of_comments = len(comments)
        context = {"news":news,"comments":comments,"no_of_comments":no_of_comments}


        return render(request,self.template_name,context)
    
    def post(self,request,*args,**kwargs):

        decision = self.kwargs.get("decision")
        news_id = self.kwargs.get("pk")
        news = NewsModel.objects.filter(id=news_id).first()
        comments = CommentNewsModel.objects.filter(news=news)
        no_of_comments = len(comments)
        context = {"news":news,"comments":comments,"no_of_comments":no_of_comments}

        if decision == "comment":
            form = CommentNewsForm(request.POST)

            if form.is_valid():
                comment = form.save(commit=False)
                comment.user = self.request.user
                comment.news = news
                comment.save()
                return redirect(reverse("readnews",kwargs={"pk":news_id,"decision":news.title}))
            return redirect(reverse("readnews",kwargs={"pk":news_id,"decision":news.title}))
        else:
             form = ReplyComment(request.POST)  
             if form.is_valid():
                reply = form.save(commit=False)  

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