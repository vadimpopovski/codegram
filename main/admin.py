# THE CODE IS CLEAN

from django.contrib import admin

# Models
from .models import Person, Post, Comment, Ad, Skill, Notification, Cloud, File


# Add models to admin panel
@admin.register(Person)
class PersonAdmin(admin.ModelAdmin):
    list_display = ['username', 'name', 'public_email']


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ['title', 'author', 'slug']


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ['author']


@admin.register(Ad)
class AdAdmin(admin.ModelAdmin):
    list_display = ['post', 'type', 'end_date']


@admin.register(Skill)
class CommentAdmin(admin.ModelAdmin):
    pass


@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    pass


class FileInline(admin.TabularInline):
    model = File


@admin.register(Cloud)
class CloudAdmin(admin.ModelAdmin):
    inlines = [FileInline]
