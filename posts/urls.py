from django.urls import path
from . import views


app_name = 'post'
urlpatterns = [
    path('user/<str:username>/post/<str:slug>/', views.detail, name='detail'),
    path('user/<str:username>/post/<str:slug>/edit/', views.edit, name='edit'),
    path('user/<str:username>/post/<str:slug>/delete/', views.delete, name='delete'),

    path('user/<str:username>/post/<str:slug>/comment/add/', views.add_comment, name='add_comment'),
    path('user/<str:username>/post/<str:slug>/comment/<int:comment_id>/edit/', views.edit_comment, name='edit_comment'),
    path('user/<str:username>/post/<str:slug>/comment/<int:comment_id>/delete/', views.delete_comment, name='delete_comment'),
    path('user/<str:username>/post/<str:slug>/comment/<int:comment_id>/reply/', views.reply_comment, name='reply_comment'),
    
    path('user/<str:username>/post/<str:slug>/like/', views.like, name='like'),

    path('create/post/', views.create, name='create'),
]