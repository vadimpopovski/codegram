# THE CODE IS CLEAN

from django.shortcuts import render
from django.core.paginator import Paginator
from main.functions import get_authenticated_user, get_new_notifications
from random import sample
import jdatetime

# Models
from main.models import Person, Post, Ad


# /
def index(request):
    authenticated_user = get_authenticated_user(request)

    # Load all posts order by there publish time
    posts = Post.objects.all().order_by('-publish_time')
    paginate = Paginator(posts, 5) # Paginate by 5

    # Load banner items
    try:
        all_ads = Ad.objects.filter(type='بنر')
        for ad in all_ads:
            if ad.end_date <= jdatetime.datetime.today():
                ad.delete()

        ad1, ad2, ad3 = sample(list(all_ads), 3)

    except:
        ad1, ad2, ad3 = None, None, None

    context = {
        'authenticated_user': authenticated_user,
        'new_notifications': get_new_notifications(authenticated_user),
        'posts': paginate.page(1),
        'ad1': ad1,
        'ad2': ad2,
        'ad3': ad3,
    }
    
    # Show 'index.html' to user
    return render(request, 'index.html', context)


# /welcome/
def welcome(request):
    authenticated_user = get_authenticated_user(request)

    context = {
        'authenticated_user': authenticated_user,
        'new_notifications': get_new_notifications(authenticated_user),
    }

    # Show 'welcome.html' to user
    return render(request, 'welcome.html', context)


# /support/
def support(request):
    authenticated_user = get_authenticated_user(request)

    context = {
        'authenticated_user': authenticated_user,
        'new_notifications': get_new_notifications(authenticated_user),
    }

    # Show 'support.html' to user
    return render(request, 'support.html', context)


# /markdown/
def markdown(request):
    authenticated_user = get_authenticated_user(request)

    context = {
        'authenticated_user': authenticated_user,
        'new_notifications': get_new_notifications(authenticated_user),
    }

    # Show 'markdown.html' to user
    return render(request, 'markdown.html', context)


# /rocket/
def rocket(request):
    authenticated_user = get_authenticated_user(request)

    context = {
        'authenticated_user': authenticated_user,
        'new_notifications': get_new_notifications(authenticated_user),
    }

    # Show 'rocket.html' to user
    return render(request, 'rocket.html', context)


# /terms/
def terms(request):
    authenticated_user = get_authenticated_user(request)

    context = {
        'authenticated_user': authenticated_user,
        'new_notifications': get_new_notifications(authenticated_user),
    }

    # Show 'terms.html' to user
    return render(request, 'terms.html', context)


# /posts/?page=<int:page>/
def posts(request, page):
    authenticated_user = get_authenticated_user(request)

    # Load all posts order by there publish time
    posts = Post.objects.all().order_by('-publish_time')
    paginate = Paginator(posts, 5) # Paginate by 5

    context = {
        'authenticated_user': authenticated_user,
        'new_notifications': get_new_notifications(authenticated_user),
        'posts': paginate.page(page),
    }

    # Show 'posts.html' to user
    return render(request, 'posts.html', context)


# /users/?page=<int:page>/
def users(request, page):
    authenticated_user = get_authenticated_user(request)

    # Load all posts order by there publish time
    users = Person.objects.all().order_by('-join_time')
    paginate = Paginator(users, 5) # Paginate by 5

    context = {
        'authenticated_user': authenticated_user,
        'new_notifications': get_new_notifications(authenticated_user),
        'users': paginate.page(page),
    }

    # Show 'users.html' to user
    return render(request, 'users.html', context)


# 404
def page_not_found_view(request, exception=None):
    authenticated_user = get_authenticated_user(request)

    context = {
        'authenticated_user': authenticated_user,
        'new_notifications': get_new_notifications(authenticated_user),
    }

    # Show 'admin/404.html' to user
    return render(request, 'admin/404.html', context)
