import json
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django import forms


from .models import User, PlayerIcon
from django.views.decorators.csrf import csrf_exempt

class NameForm(forms.Form):
    name = forms.CharField(label="", required=True, max_length=20, widget=forms.TextInput(attrs={
        'autofocus': True,
        'placeholder': 'name',
        'style': 'width: 150px; margin-right: 5px;'
        }))

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
    # Create a new player icon
    if request.method == "POST":
        name = request.POST["name"]
        if name == "":
            return JsonResponse({"error": "Name cannot be blank."}, status=400)
        if not PlayerIcon.objects.filter(name=name).exists():
            player = PlayerIcon(name=name)
            player.save()
        return redirect("team_split")
    # Delete a player icon
    elif request.method == "DELETE":
        data = json.loads(request.body)
        player_id = int(data["player_id"])
        try:
            player = PlayerIcon.objects.get(id=player_id)
            player.delete()
            return JsonResponse({"message": "Player deleted successfully."}, status=200)
        except PlayerIcon.DoesNotExist:
            return JsonResponse({"error": "PlayerIcon not found."}, status=404)
            
    # Update the position of a player icon
    elif request.method == "PUT":
        data = json.loads(request.body)
        player_id = int(data["player_id"])
        try:
            player = PlayerIcon.objects.get(id=player_id)
            player.x = int(data["x"])
            player.y = int(data["y"])
            player.save()
            return JsonResponse({"message": "Player position updated successfully."}, status=200)
        except PlayerIcon.DoesNotExist:
            return JsonResponse({"error": "PlayerIcon not found."}, status=404)

    players = PlayerIcon.objects.all()
    return render(request, "soccer/team_split.html", {
        "form": NameForm(),
        "players": players
    })
