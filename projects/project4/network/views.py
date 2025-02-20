from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseBadRequest
from django.shortcuts import render, redirect
from django import forms
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

    return render(request, "network/index.html", {
        "form": PostForm(),
        "posts": Post.objects.all().order_by("-created_at")
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
        user = User.objects.get(id=user_id)
    except User.DoesNotExist:
        return HttpResponseBadRequest("User does not exist")
    return render(request, "network/profile_page.html", {
        "user": user,
        "posts": Post.objects.filter(author=user).order_by("-created_at")
    })