import json
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseBadRequest, JsonResponse
from django.shortcuts import render, redirect
from django import forms
from django.views.decorators.csrf import csrf_exempt

from .models import User, Post

class PostForm(forms.Form):
    post = forms.CharField(label="", required=True, 
                         widget=forms.TextInput(attrs={
                             'autofocus': True,
                             'class': 'form-control',
                             'style': 'width: 95%; padding: 10px; margin-top: 10px; margin-bottom: 10px;'
                         }))

def index(request):
    if request.method == "POST":
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.cleaned_data["post"]
            Post.objects.create(author=request.user,content=post)
            return redirect("index")
        
    posts = Post.objects.all().order_by("-created_at")
    for post in posts:
        post.is_liked = post.likes.filter(id=request.user.id).exists()
    
    paginator = Paginator(posts, 10)
    page_number = request.GET.get("page", 1)
    posts = paginator.get_page(page_number)

    return render(request, "network/index.html", {
        "form": PostForm(),
        "posts": posts
    })


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return redirect("index")
        else:
            return render(request, "network/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "network/login.html")


def logout_view(request):
    logout(request)
    return redirect("index")


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "network/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "network/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return redirect("index")
    else:
        return render(request, "network/register.html")

def profile_page(request, user_id):
    try: 
        profile_user = User.objects.get(id=user_id)
    except User.DoesNotExist:
        return HttpResponseBadRequest("User does not exist")
    button = ""
    if request.user.is_authenticated and request.user != profile_user:
        if profile_user.followers.filter(id=request.user.id).exists():
            button = "Unfollow"
        else:
            button = "Follow"

    posts = Post.objects.filter(author=profile_user).order_by("-created_at")
    for post in posts:
        post.is_liked = post.likes.filter(id=request.user.id).exists()

    paginator = Paginator(posts, 10)
    page_number = request.GET.get("page", 1)
    posts = paginator.get_page(page_number)

    return render(request, "network/profile_page.html", {
        "profile_user": profile_user,
        "posts": posts,
        "button": button
    })

@login_required
def follow_or_unfollow(request):
    if request.method == "POST":
        followee_id = request.POST["followee_id"]
        followee = User.objects.get(id=followee_id)
        follower_id = request.user.id
        follower = User.objects.get(id=follower_id)
        if request.POST["operation"] == "follow":
            if not follower.followees.filter(id=followee_id).exists():
                follower.followees.add(followee)
            if not followee.followers.filter(id=follower_id).exists():
                followee.followers.add(follower)
        else:
            if follower.followees.filter(id=followee_id).exists():
                follower.followees.remove(followee)
            if followee.followers.filter(id=follower_id).exists():
                followee.followers.remove(follower)

        return redirect("profile_page", user_id=followee_id)

@login_required
def following(request):
    followees = request.user.followees.all()
    followees_posts = Post.objects.filter(author__in=followees).order_by("-created_at")
    for followees_post in followees_posts:
        followees_post.is_liked = followees_post.likes.filter(id=request.user.id).exists()

    paginator = Paginator(followees_posts, 10)
    page_number = request.GET.get("page", 1)
    followees_posts = paginator.get_page(page_number)

    return render(request, "network/followees_posts.html", {
        "form": PostForm(),
        "posts": followees_posts
    })

@csrf_exempt
@login_required
def edit(request, post_id):
    if request.method != "PUT":
        return JsonResponse({
            "error": "PUT request required."
        }, status=400)
    try:
        post = Post.objects.get(pk=post_id)
    except Post.DoesNotExist:
        return JsonResponse({"error": "Post not found."}, status=404)
    
    if request.user != post.author:
        return JsonResponse({"error": "Forbidden"}, status=403)
    
    data = json.loads(request.body)
    post.content = data["content"]
    post.save()
    return HttpResponse(status=204)

@csrf_exempt
@login_required
def like_or_unlike(request, post_id):
    if request.method != "PUT":
        return JsonResponse({
            "error": "PUT request required."
        }, status=400)
    try:
        post = Post.objects.get(pk=post_id)
    except Post.DoesNotExist:
        return JsonResponse({"error": "Post not found."}, status=404)
    # if not follower.followees.filter(id=followee_id).exists():
    if not post.likes.filter(id=request.user.id).exists():
        post.likes.add(request.user)
    else:
        post.likes.remove(request.user)
    post.save()
    return HttpResponse(status=204)