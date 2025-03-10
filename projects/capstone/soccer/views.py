import json
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.shortcuts import render, redirect


from .models import User, PlayerIcon
from django.views.decorators.csrf import csrf_exempt

# Create your views here.
def index(request):
    return render(request, "soccer/index.html")

def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        print(username)
        password = request.POST["password"]
        print(password)
        user = authenticate(request, username=username, password=password)

        if user == None:
            print("User is None")

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return redirect("index")
        else:
            return render(request, "soccer/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "soccer/login.html")

@login_required
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
            return render(request, "soccer/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "soccer/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return redirect("index")
    else:
        return render(request, "soccer/register.html")

@csrf_exempt
def team_split(request):
    if request.method == "POST":
        name = request.POST["name"]
        if not PlayerIcon.objects.filter(name=name).exists():
            print("new player created!") 
            player = PlayerIcon(name=name)
            player.save()
    elif request.method == "DELETE":
        print("Delete request received!")
        data = json.loads(request.body)
        player_id = int(data["player_id"])
        player = PlayerIcon.objects.get(id=player_id)
        player.delete()

    return render(request, "soccer/team_split.html", {"players": PlayerIcon.objects.all()})
