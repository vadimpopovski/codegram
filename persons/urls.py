from django.urls import path, include
from . import views


app_name = 'person'
urlpatterns = [
    path('notifications/?page=<int:page>/', views.notifications, name='notifications'),

    path('user/<str:username>/', views.profile, name='profile'),
    path('user/<str:username>/followers/?page=<int:page>/', views.followers, name='followers'),
    path('user/<str:username>/followings/?page=<int:page>/', views.followings, name='followings'),
    path('user/<str:username>/follow/', views.follow, name='follow'),
    
    path('user/<str:username>/posts/?page=<int:page>/', views.posts, name='posts'),

    path('', include('posts.urls')),
    # path('', include('prjects.urls')),


    path('edit/profile/', views.edit_profile, name='edit_profile'),
    
    path('friends/?page=<int:page>/', views.friends, name='friends'),
    path('friends/posts/?page=<int:page>/', views.friends_posts, name='friends_posts'),
]