
from django.urls import path
from . import views

urlpatterns = [
    path("signup/",views.UserSignupView.as_view(),name="account_signup"),
    path("home/",views.HomeView.as_view(),name="home"),
    path("createnews/",views.NewsView.as_view(),name="createnews"),
    path("readnews/<int:pk>/<str:decision>/",views.ReadNews.as_view(),name="readnews"),
    path("search/<str:category>/",views.Search.as_view(),name="search"),
    path("login/",views.UserLoginView.as_view(),name="account_login"),
    


]
