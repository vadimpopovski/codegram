from django.urls import path
from . import views
from .feeds import LatestPostsFeed


urlpatterns = [
    path('', views.index, name='index'),
    path('welcome/', views.welcome, name='welcome'),
    path('support/', views.support, name='support'),
    path('markdown/', views.markdown, name='markdown'),
    path('rocket/', views.rocket, name='rocket'),
    path('terms/', views.terms, name='terms'),
    
    path('posts/?page=<int:page>/', views.posts, name='posts'),
    path('users/?page=<int:page>/', views.users, name='users'),

    path("feed/", LatestPostsFeed(), name="feed"),
]