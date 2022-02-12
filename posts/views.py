from django.http.response import HttpResponse
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect, JsonResponse
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from main.functions import get_authenticated_user, get_new_notifications, translate_to_html, ads_list, delete_comment_completely, post_slug_generator

# Models
from main.models import Person, Post, Comment, Notification, Ad

# Forms
from .forms import PostForm, CommentForm


# /user/<str:username>/post/<str:slug>/
def detail(request, username, slug):
    authenticated_user = get_authenticated_user(request)
    person = get_object_or_404(Person, username=username) # Get the Person
    post = get_object_or_404(Post, author=person, slug=slug) # Get the Post

    # Add to post view
    post.views = int(post.views) + 1
    post.save()

    # Add post to user's viewed posts
    if authenticated_user is not None:
        authenticated_user.viewed_posts.add(post)
        authenticated_user.save()

    context = {
        'authenticated_user': authenticated_user,
        'new_notifications': get_new_notifications(authenticated_user),
        'post': post,
        'person': person,
        'post_body': translate_to_html(post.body),
        'ads_list': ads_list(),
    }

    # Show 'user/post/detail.html' to user
    return render(request, 'user/post/detail.html', context)


# /user/<str:username>/post/<str:slug>/edit/
@login_required
def edit(request, username, slug):
    authenticated_user = get_authenticated_user(request)
    person = get_object_or_404(Person, username=username) # Get the Person
    post = get_object_or_404(Post, author=person, slug=slug) # Get the Post

    # If registered user is post author
    if authenticated_user == post.author:
        if request.method == 'POST':
            form = PostForm(request.POST) # Get form

            if form.is_valid():
                title = form.cleaned_data['titleInput'] # Read title
                body = form.cleaned_data['bodyInput'] # Read body
                cover = form.cleaned_data['coverInput'] # Read cover
                short_description = form.cleaned_data['shortDescriptionInput'] # Read short_description

                # Give new data to post
                post.title = title 
                post.body = body
                post.cover = cover
                post.short_description = short_description
                post.save() # Save it
                
                # Redirect user to 'person:post:detail' url
                return HttpResponseRedirect('/user/' + username + '/post/' + slug)

        # If request.method == 'GET'
        else:
            form = PostForm(initial={
                'titleInput': post.title,
                'bodyInput': post.body,
                'coverInput': post.cover,
                'shortDescriptionInput': post.short_description,
            })

        context = {
            'authenticated_user': authenticated_user,
            'new_notifications': get_new_notifications(authenticated_user),
            'form': form,
            'post': post,
        }

        # Show 'user/post/edit.html' to user
        return render(request, 'user/post/edit.html', context)

    context = {
        'authenticated_user': authenticated_user,
        'new_notifications': get_new_notifications(authenticated_user),
    }

    return render(request, 'forbidden.html', context)


# /user/<str:username>/post/<str:slug>/delete/
@login_required
def delete(request, username, slug):
    authenticated_user = get_authenticated_user(request)
    person = get_object_or_404(Person, username=username) # Get the Person
    post = get_object_or_404(Post, author=person, slug=slug) # Get the Post

    # If registered user is post author
    if authenticated_user == post.author:
        # Delete post comments
        for comment in post.comments.all():
            delete_comment_completely(comment)

        post.delete() # Delete post

        # Redirect user to 'person:profile' url
        return HttpResponseRedirect('/user/' + username)

    # If registered user not post author
    context = {
        'authenticated_user': authenticated_user,
        'new_notifications': get_new_notifications(authenticated_user),
    }

    # Show 'forbidden.html' to user
    return render(request, 'forbidden.html', context)


# /user/<str:username>/post/<str:slug>/comment/add/
@login_required
def add_comment(request, username, slug):
    authenticated_user = get_authenticated_user(request)
    person = get_object_or_404(Person, username=username) # Get the Person
    post = get_object_or_404(Post, author=person, slug=slug) # Get the Post

    if request.method == 'POST':
        form = CommentForm(request.POST) # Get form

        if form.is_valid():
            text = form.cleaned_data['textInput'] # Read body

            # Create a Comment model with form data
            comment = Comment(
                author=authenticated_user,
                text=text,
            )
            comment.save() # Save it

            post.comments.add(comment)
            post.len_comments = int(post.len_comments) + 1
            post.save()

            notif = Notification(receiver=post.author, message=f'<a href="/user/{authenticated_user.username}/">{authenticated_user.name}</a> نظری روی مطلب «<a href="/user/{username}/post/{slug}/">{post.title}</a>» شما ارسال کرد', notif_type='comment')
            notif.save()

    # Redirect user to 'person:post:detail' url
    return HttpResponseRedirect('/user/' + username + '/post/' + slug)


# /user/<str:username>/post/<str:slug>/comment/<int:comment_id>/edit/
@login_required
def edit_comment(request, username, slug, comment_id):
    authenticated_user = get_authenticated_user(request)
    person = get_object_or_404(Person, username=username) # Get the Person
    post = get_object_or_404(Post, author=person, slug=slug) # Get the Post
    comment = get_object_or_404(post.comments, id=comment_id) # Get the Comment

    if authenticated_user == comment.author:
        if request.method == 'POST':
            form = CommentForm(request.POST) # Get form

            if form.is_valid():
                text = form.cleaned_data['textInput'] # Read body

                # Replace comment text with new one
                comment.text = text
                comment.save() # Save it

        # Redirect user to 'person:post:detail' url
        return HttpResponseRedirect('/user/' + username + '/post/' + slug)

    # If registered user not comment author
    context = {
        'authenticated_user': authenticated_user,
        'new_notifications': get_new_notifications(authenticated_user),
    }

    # Show 'forbidden.html' to user
    return render(request, 'forbidden.html', context)


# /user/<str:username>/post/<str:slug>/comment/<int:comment_id>/delete/
@login_required
def delete_comment(request, username, slug, comment_id):
    authenticated_user = get_authenticated_user(request)
    person = get_object_or_404(Person, username=username) # Get the Person
    post = get_object_or_404(Post, author=person, slug=slug) # Get the Post
    comment = get_object_or_404(post.comments, id=comment_id) # Get the Comment

    if authenticated_user == comment.author:
        delete_comment_completely(comment)
        post.len_comments = int(post.len_comments) - 1
        post.save()

        # Redirect user to 'person:post:detail' url
        return HttpResponseRedirect('/user/' + username + '/post/' + slug)

    # If registered user not comment author
    context = {
        'authenticated_user': authenticated_user,
        'new_notifications': get_new_notifications(authenticated_user),
    }

    # Show 'forbidden.html' to user
    return render(request, 'forbidden.html', context)


# /user/<str:username>/post/<str:slug>/comment/<int:comment_id>/reply/
@login_required
def reply_comment(request, username, slug, comment_id):
    authenticated_user = get_authenticated_user(request)
    comment = get_object_or_404(Comment, id=comment_id) # Get the Comment

    if request.method == 'POST':
        form = CommentForm(request.POST) # Get form

        if form.is_valid():
            text = form.cleaned_data['textInput'] # Read body

            # Create a Comment model with form data
            new_comment = Comment(
                author=authenticated_user,
                text=text,
            )
            new_comment.save() # Save it

            # Add new comment to comment replys
            comment.replys.add(new_comment)

            notif = Notification(receiver=comment.author, message=f'<a href="/user/{authenticated_user.username}/">{authenticated_user.name}</a> پاسخی روی <a href="/user/{username}/post/{slug}/#comment_{comment.id}">نظر</a> شما ارسال کرد', notif_type='reply')
            notif.save()

    # Redirect user to 'person:post:detail' url
    return HttpResponseRedirect('/user/' + username + '/post/' + slug)


# /user/<str:username>/post/<str:slug>/like/
@login_required
def like(request, username, slug):
    authenticated_user = get_authenticated_user(request)
    person = get_object_or_404(Person, username=username) # Get the Person
    post = get_object_or_404(Post, author=person, slug=slug) # Get the Post

    # If user has liked post before
    if post in authenticated_user.liked_posts.all():
        post.likes.remove(authenticated_user)
        post.len_likes = int(post.len_likes) - 1
        authenticated_user.liked_posts.remove(post)
        responseText = f'<button class="btn btn-light me-2" type="button" onclick="likePost(\'{post.author.username}\', \'{post.slug}\', \'{post.id}\')"><i class="far fa-heart"></i> <span class="fa-num">{post.len_likes}</span></button>'

    # If user has not liked post before
    else:
        post.likes.add(authenticated_user)
        post.len_likes = int(post.len_likes) + 1
        authenticated_user.liked_posts.add(post)
        responseText = f'<button class="btn btn-outline-danger me-2" type="button" onclick="likePost(\'{post.author.username}\', \'{post.slug}\', \'{post.id}\')"><i class="fas fa-heart"></i> <span class="fa-num">{post.len_likes}</span></button>'

        notif = Notification(receiver=post.author, message=f'<a href="/user/{authenticated_user.username}/">{authenticated_user.name}</a> مطلب «<a href="/user/{username}/post/{slug}/">{post.title}</a>» شما را پسند کرد', notif_type='like')
        notif.save()

    authenticated_user.save()
    post.save()

    # Response the data
    return HttpResponse(responseText)


# /create/post/
@login_required
def create(request):
    authenticated_user = get_authenticated_user(request)

    # If form method == POST
    if request.method == 'POST':
        form = PostForm(request.POST) # Get form

        if form.is_valid():
            title = form.cleaned_data['titleInput'] # Read title
            body = form.cleaned_data['bodyInput'] # Read body
            cover = form.cleaned_data['coverInput'] # Read cover
            short_description = form.cleaned_data['shortDescriptionInput'] # Read short description

            # Create a Post model with form data
            post = Post(
                title=title,
                body=body,
                author=authenticated_user,
                cover=cover,
                short_description=short_description,
            )
            post.save() # Save it

            post.slug = post_slug_generator(post)
            post.save()
            
            # Redirect user to 'person:post:detail' url
            return HttpResponseRedirect('/user/' + post.author.username + '/post/' + post.slug)

    # If form method == GET
    else:
        form = PostForm() # Give form to user

    context = {
        'authenticated_user': authenticated_user,
        'new_notifications': get_new_notifications(authenticated_user),
        'form': form,
    }

    # Show 'create/post.html' to user
    return render(request, 'create/post.html', context)