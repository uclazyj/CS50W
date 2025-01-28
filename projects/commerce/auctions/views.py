from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseBadRequest
from django import forms
from django.shortcuts import render, redirect
from django.urls import reverse


from .models import User, Listing, Bid, Watch

class ListingForm(forms.Form):
    title = forms.CharField(max_length=64)
    description = forms.CharField(max_length=64)
    starting_bid = forms.DecimalField(max_digits=10, decimal_places=2)
    # optional fields
    image_url = forms.URLField(required=False)
    category = forms.CharField(max_length=64, required=False)

class BidForm(forms.Form):
    bid_price = forms.DecimalField(max_digits=10, 
                               decimal_places=2,
                               label="",
                               widget=forms.TextInput(attrs={'placeholder': 'Bid'})
                               )

@login_required
def index(request):
    watched_items = Watch.objects.filter(user=request.user)
    watched_listings = [watched_item.listing for watched_item in watched_items]
    return render(request, "auctions/index.html", {
        "listings": Listing.objects.all(),
        "watched_listings": watched_listings
    })

# def index(request):
    # watched_listings = Watch.objects.filter(user=request.user).values('listing'),
    # unwatched_listings = Listing.objects.exclude(id__in=watched_listings)
    # return render(request, "auctions/index.html", {
    #     "watched_listings": watched_listings,
    #     "unwatched_listings": unwatched_listings
    # })


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "auctions/login.html")

@login_required
def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "auctions/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")


@login_required
def listings(request, listing_id):
    try:
        listing = Listing.objects.get(pk=listing_id)
    except Listing.DoesNotExist:
        return HttpResponseBadRequest("Bad Request: listing does not exist")
    if request.method == "POST":
        form = BidForm(request.POST)
        if form.is_valid():
            bid_price = form.cleaned_data["bid_price"]
            if bid_price > listing.current_price:
                # Update the listing
                listing.last_bidder = request.user
                listing.current_price = bid_price
                listing.num_bids += 1
                listing.save()
                # Add a bid to the listing
                bid = Bid(listing=listing, bidder=request.user, bid_price=bid_price)
                bid.save()
            # Explictly redirect to follow Post/Redirect/Get pattern
            return redirect("listings", listing_id=listing.id)

    return render(request, "auctions/listing.html", {
        "listing" : listing,
        "form" : BidForm()
    })


@login_required
def create_listing(request):
    if request.method == "POST":
        form = ListingForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data["title"]
            description = form.cleaned_data["description"]
            starting_bid = form.cleaned_data["starting_bid"]
            # optional fields
            image_url = form.cleaned_data["image_url"]
            category = form.cleaned_data["category"]
            listing = Listing(owner = request.user, title=title, description=description, \
                              starting_bid=starting_bid, current_price=starting_bid,\
                                num_bids=0, image_url=image_url, category=category)
            listing.save()
            return redirect("index")
        else:
            return render(request, "auctions/create_listing.html", {
                "form": form
            })
    return render(request, "auctions/create_listing.html", {
        "form": ListingForm()
    })

@login_required
def watchlist(request):
    if request.method == "POST":
        listing_id = request.POST["listing_id"]
        listing = Listing.objects.get(pk=listing_id)
        if request.POST["operation"] == "add":
            watch, created = Watch.objects.get_or_create(user=request.user, listing=listing)
            if created:
                watch.save()
            return redirect("index")
        else:
            watch = Watch.objects.get(user=request.user, listing=listing)
            watch.delete()
            return redirect("watchlist")
        
    watched_items = Watch.objects.filter(user=request.user)
    watched_listings = [watched_item.listing for watched_item in watched_items]
    return render(request, "auctions/watchlist.html", {
        "watched_listings": watched_listings
    })