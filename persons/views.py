from django.http.response import HttpResponse
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from social_django.models import UserSocialAuth
from django.core.paginator import Paginator
from main.functions import get_authenticated_user, get_new_notifications, translate_to_html
import os

# Models
from main.models import Person, Post, Skill, Notification

# Forms
from .forms import ProfileEditForm, RezomeForm


# /notifications/?page=<int:page>/
@login_required
def notifications(request, page):
    authenticated_user = get_authenticated_user(request)
    notifications = Notification.objects.filter(receiver=authenticated_user, done=False).order_by('-id') # Give unread notifications
    done = False # User has unread notification

    # Mark notifications as read
    for notification in notifications:
        notification.done = True
        notification.save()

    # If there's no unread notification give all notifications
    if len(notifications) == 0:
        notifications = Notification.objects.filter(receiver=authenticated_user).order_by('-id')
        paginate = Paginator(notifications, 10)
        done = True # User hasn't unread notification

    context = {
        'authenticated_user': authenticated_user,
        'new_notifications': get_new_notifications(authenticated_user),
        'notifications': notifications if done is False else paginate.page(page),
        'done': done,
    }

    # Show 'notifications.html' to user
    return render(request, 'notifications.html', context)


# /user/<str:username>/
def profile(request, username):
    authenticated_user = get_authenticated_user(request)
    person = get_object_or_404(Person, username=username) # Get Person
    posts = Post.objects.filter(author=person).order_by('-publish_time') # Get the Posts

    paginate = Paginator(posts, 5)
    
    skills_are_available = False
    if len(person.skills.all()) > 0:
        skills_are_available = True

    context = {
        'authenticated_user': authenticated_user,
        'new_notifications': get_new_notifications(authenticated_user),
        'person': person,
        'rezome': translate_to_html(person.rezome),
        'posts': paginate.page(1),
        'skills_are_available': skills_are_available,
    }

    # Show 'user/profile.html' to user
    return render(request, 'user/profile.html', context)


# /user/<str:username>/followers/?page=<int:page>/
def followers(request, username, page):
    authenticated_user = get_authenticated_user(request)
    person = get_object_or_404(Person, username=username) # Get Person
    followers = person.followers.all().order_by('-join_time') # Get person followers

    followers_are_available = False
    if len(followers) > 0:
        followers_are_available = True

    paginate = Paginator(followers, 5)
            
    context = {
        'authenticated_user': authenticated_user,
        'new_notifications': get_new_notifications(authenticated_user),
        'person': person,
        'followers': paginate.page(page),
        'followers_are_available': followers_are_available,
    }

    # Show 'user/followers.html' to user
    return render(request, 'user/followers.html', context)


# /user/<str:username>/followings/?page=<int:page>/
def followings(request, username, page):
    authenticated_user = get_authenticated_user(request)
    person = get_object_or_404(Person, username=username) # Get Person
    followings = person.followings.all().order_by('-join_time') # Get person followings

    followings_are_available = False
    if len(followings) > 0:
        followings_are_available = True

    paginate = Paginator(followings, 5)
            
    context = {
        'authenticated_user': authenticated_user,
        'new_notifications': get_new_notifications(authenticated_user),
        'person': person,
        'followings': paginate.page(page),
        'followings_are_available': followings_are_available,
    }

    # Show 'user/followings.html' to user
    return render(request, 'user/followings.html', context)


# /user/<str:username>/follow/
@login_required
def follow(request, username):
    authenticated_user = get_authenticated_user(request)
    person = get_object_or_404(Person, username=username) # Get the Person

    # If user has followed person before
    if person in authenticated_user.followings.all():
        person.followers.remove(authenticated_user)
        person.len_followers = int(person.len_followers) - 1
        authenticated_user.followings.remove(person)
        authenticated_user.len_followings = int(authenticated_user.len_followings) - 1
        responseText = f'<button class="btn btn-success" type="button" onclick="followPerson(\'{username}\')"><i class="fas fa-user-plus"></i> دنبال کنید</button>'

    # If user has not followed person before
    else:
        person.followers.add(authenticated_user)
        person.len_followers = int(person.len_followers) + 1
        authenticated_user.followings.add(person)
        authenticated_user.len_followings = int(authenticated_user.len_followings) + 1
        responseText = f'<button class="btn btn-light" type="button" onclick="followPerson(\'{username}\')"><i class="fas fa-check"></i> دنبال می‌کنید</button>'

        notif = Notification(
            receiver=person,
            message=f'<a href="/user/{authenticated_user.username}/">{authenticated_user.name}</a> از حالا شما را دنبال می‌کند',
            notif_type='follow'
        )
        notif.save()

    authenticated_user.save()

    # Response the data
    return HttpResponse(responseText)


# /user/<str:username>/posts/?page=<int:page>/
def posts(request, username, page):
    authenticated_user = get_authenticated_user(request)
    person = get_object_or_404(Person, username=username) # Get Person
    posts = Post.objects.filter(author=person).order_by('-publish_time') # Get the Posts

    paginate = Paginator(posts, 5)

    context = {
        'authenticated_user': authenticated_user,
        'new_notifications': get_new_notifications(authenticated_user),
        'person': person,
        'posts': paginate.page(page),
    }

    # Show 'user/posts.html' to user
    return render(request, 'user/posts.html', context)


# /edit/profile/
@login_required
def edit_profile(request):
    authenticated_user = get_authenticated_user(request)

    try:
        github_login = request.user.social_auth.get(provider='github')
    except UserSocialAuth.DoesNotExist:
        github_login = None

    try:
        gitlab_login = request.user.social_auth.get(provider='gitlab')
    except UserSocialAuth.DoesNotExist:
        gitlab_login = None

    if request.method == 'POST':
        form = ProfileEditForm(request.POST, request.FILES) # Get Form

        if form.is_valid():
            avatar = form.cleaned_data['avatarInput'] # Read name
            name = form.cleaned_data['nameInput'] # Read name
            description = form.cleaned_data['descriptionInput'] # Read description
            rezome = form.cleaned_data['rezomeInput'] # Read rezome
            # year_of_born = form.cleaned_data['yearOfBornInput'] # Read description
            # gender = form.cleaned_data['genderInput'] # Read gender
            skills = form.cleaned_data['skillsInput'] # Read skills
            github = form.cleaned_data['githubInput'] # Read github
            gitlab = form.cleaned_data['gitlabInput'] # Read gitlab
            stackoverflow = form.cleaned_data['stackoverflowInput'] # Read stackowerflow
            linkedin = form.cleaned_data['linkedinInput'] # Read linkedin
            dev = form.cleaned_data['devInput'] # Read dev
            facebook = form.cleaned_data['facebookInput'] # Read facebook
            instagram = form.cleaned_data['instagramInput'] # Read instagram
            twitter = form.cleaned_data['twitterInput'] # Read twitter
            virgool = form.cleaned_data['virgoolInput'] # Read virgool
            website = form.cleaned_data['websiteInput'] # Read website
            public_email = form.cleaned_data['publicEmailInput'] # Read public_name
            mobile = form.cleaned_data['mobileInput'] # Read mobile
            telegram = form.cleaned_data['telegramInput'] # Read telegram
            matrix = form.cleaned_data['matrixInput'] # Read matrix
            
            for skill in authenticated_user.skills.all():
                authenticated_user.skills.remove(skill)

            if skills != '':
                for skill_name in skills.split(' '):
                    try:
                        skill = Skill.objects.get(name=skill_name.lower())
                    
                    except Skill.DoesNotExist:
                        skill = Skill(name=skill_name.lower())
                        skill.save()

                    authenticated_user.skills.add(skill)

            # Give new data to person
            if avatar is not None:
                if avatar is False:
                    os.remove(authenticated_user.avatar.path)
                    authenticated_user.avatar = None
                    
                else:   
                    if authenticated_user.avatar != '':
                        os.remove(authenticated_user.avatar.path)

                    authenticated_user.avatar = avatar

            authenticated_user.name = name
            authenticated_user.description = description
            authenticated_user.rezome = rezome
            # authenticated_user.year_of_born = year_of_born
            # authenticated_user.gender = gender
            authenticated_user.github = github
            authenticated_user.gitlab = gitlab
            authenticated_user.stackoverflow = stackoverflow
            authenticated_user.linkedin = linkedin
            authenticated_user.dev = dev
            authenticated_user.facebook = facebook
            authenticated_user.instagram = instagram
            authenticated_user.twitter = twitter
            authenticated_user.virgool = virgool
            authenticated_user.website = website
            authenticated_user.public_email = public_email
            authenticated_user.mobile = mobile
            authenticated_user.telegram = telegram
            authenticated_user.matrix = matrix
            authenticated_user.save() # Save it
            
            # Redirect user to his/her profile page
            return HttpResponseRedirect('/user/' + authenticated_user.username)
            

    # If form method == GET
    else:
        # Give form to user
        form = ProfileEditForm(initial = {  
            'avatarInput': authenticated_user.avatar,
            'nameInput': authenticated_user.name,
            'descriptionInput': authenticated_user.description,
            'rezomeInput': authenticated_user.rezome,
            # 'yearOfBornInput': authenticated_user.year_of_born,
            # 'genderInput': authenticated_user.gender,
            'skillsInput': ' '.join([skill.name for skill in authenticated_user.skills.all()]),
            'githubInput': authenticated_user.github,
            'gitlabInput': authenticated_user.gitlab,
            'stackoverflowInput': authenticated_user.stackoverflow,
            'linkedinInput': authenticated_user.linkedin,
            'devInput': authenticated_user.dev,
            'facebookInput': authenticated_user.facebook,
            'instagramInput': authenticated_user.instagram,
            'twitterInput': authenticated_user.twitter,
            'virgoolInput': authenticated_user.virgool,
            'websiteInput': authenticated_user.website,
            'publicEmailInput': authenticated_user.public_email,
            'mobileInput': authenticated_user.mobile,
            'telegramInput': authenticated_user.telegram,
            'matrixInput': authenticated_user.matrix,
        })

    context = {
        'authenticated_user': authenticated_user,
        'new_notifications': get_new_notifications(authenticated_user),
        'form': form,
        'github_login': github_login,
        'gitlab_login': gitlab_login,
    }

    # Show 'user/edit.html' to user
    return render(request, 'user/edit.html', context)


# /friends/?page=<int:page>/
@login_required
def friends(request, page):
    authenticated_user = get_authenticated_user(request)
    friends = authenticated_user.followings.all().order_by('-join_time')

    paginate = Paginator(friends, 5)
            
    context = {
        'authenticated_user': authenticated_user,
        'new_notifications': get_new_notifications(authenticated_user),
        'friends': paginate.page(page),
    }

    # Show 'user/friends.html' to user
    return render(request, 'user/friends.html', context)


# /friends/posts/?page=<int:page>/
@login_required
def friends_posts(request, page):
    authenticated_user = get_authenticated_user(request)
    friends = authenticated_user.followings.all()
    friends_posts = Post.objects.filter(author__in=friends).order_by('-publish_time')

    paginate = Paginator(friends_posts, 5)
            
    context = {
        'authenticated_user': authenticated_user,
        'new_notifications': get_new_notifications(authenticated_user),
        'friends_posts': paginate.page(page),
    }

    # Show 'user/friends.html' to user
    return render(request, 'user/friends_posts.html', context)