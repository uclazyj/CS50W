import json
import os

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django import forms
from django.views.decorators.csrf import csrf_exempt

from .models import User, PlayerIcon, Image
from .utils import extract_names_from_image


class NameForm(forms.Form):
    name = forms.CharField(label="", required=True, max_length=20, widget=forms.TextInput(attrs={
        'autofocus': True,
        'placeholder': 'name',
        'style': 'width: 150px; margin: 10px;'
        }))

class ImageUploadForm(forms.ModelForm):

    image = forms.ImageField(label="Choose screenshot")

    class Meta:
        model = Image
        fields = ['image']

# Create your views here.
def index(request):
    image = Image.objects.all().first()
    return render(request, "soccer/index.html", {"image": image})

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
        if name == "":
            return JsonResponse({"error": "Name cannot be blank."}, status=400)
        if not PlayerIcon.objects.filter(name=name).exists():
            player = PlayerIcon(name=name)
            player.save()
        return redirect("team_split")

    players = PlayerIcon.objects.all()
    return render(request, "soccer/team_split.html", {
        "form": NameForm(),
        "image_upload_form": ImageUploadForm(),
        "players": players
    })

@csrf_exempt
def update_player(request):
    if request.method != "PUT":
        return JsonResponse({"error": "PUT request required."}, status=400)
    
    data = json.loads(request.body)
    player_id = int(data["player_id"])
    try:
        player = PlayerIcon.objects.get(id=player_id)
        player.x = int(data["x"])
        player.y = int(data["y"])
        team_id = int(data["team_id"])
        
        # 0 means the player does not belong to any team
        # -1 means no update in team_id
        if team_id != -1:
            player.team_id = team_id
        player.save()
        return JsonResponse({"message": "Player position updated successfully."}, status=200)
    except PlayerIcon.DoesNotExist:
        return JsonResponse({"error": "PlayerIcon not found."}, status=404)

@csrf_exempt
def delete_player(request):
    if request.method != "DELETE":
        return JsonResponse({"error": "DELETE request required."}, status=400)
    
    data = json.loads(request.body)
    player_id = int(data["player_id"])
    try:
        player = PlayerIcon.objects.get(id=player_id)
        player.delete()
        return JsonResponse({"message": "Player deleted successfully."}, status=200)
    except PlayerIcon.DoesNotExist:
        return JsonResponse({"error": "PlayerIcon not found."}, status=404)

@csrf_exempt
def get_players(request):
    players = PlayerIcon.objects.all().order_by('name')
    players_data = [{
        'id': player.id,
        'name': player.name,
        'x': player.x,
        'y': player.y,
        'team_id': player.team_id
    } for player in players]

    return JsonResponse({'players': players_data})

def upload_image(request):
    if request.method == "POST":
        form = ImageUploadForm(request.POST, request.FILES) 
        if form.is_valid():
            images = Image.objects.all()
            for image in images:
                if os.path.isfile(image.image.path):
                    os.remove(image.image.path)
                image.delete()
            form.save()

            # Extract names from the image
            image_path = Image.objects.all()[0].image.path
            extracted_names = extract_names_from_image(image_path=image_path)
            print("extracted_names: ",extracted_names)
            for name in extracted_names:
                if not PlayerIcon.objects.filter(name=name).exists():
                    player = PlayerIcon(name=name)
                    player.save()
            return redirect("team_split")