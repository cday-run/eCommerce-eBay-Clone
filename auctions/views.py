from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from .models import User, Listing, Bid, Comment
from django.contrib.auth.decorators import login_required
import datetime

def index(request):
    return render(request, "auctions/index.html", {
        "listings": Listing.objects.all()
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
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "auctions/login.html")


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
def create_listing(request):
    if request.method == "POST":
        #Access the user
        current_user = request.user
        #Set the seller name to user name
        seller = current_user.username
        #Find item name from form
        item_name = request.POST.get("title")
        #Find description from form
        item_description = request.POST.get("description")
        #Find starting bid value from form
        price = request.POST.get("starting_bid")
        #Find image from form
        image = request.POST.get("image")
        #Find category from form
        category = request.POST.get("category")
        #Get listing date
        date = datetime.datetime.now()
        #Add post to listings
        new_listing = Listing.objects.create(item_name=item_name, 
            item_description=item_description, seller=seller, price=price,
            image=image, category=category, listing_date=date)
        new_listing.save()

        """
        ###Change redirect to listing page
        """
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/create.html")

def listed(request, item_id):
    listed = Listing.objects.get(pk=item_id)
    return render(request, "auctions/listed.html", {
        "listed_id": item_id,
        "title": listed.item_name,
        "description": listed.item_description,
        "price": listed.price,
        "comments": Comment.objects.filter(listing_id=item_id)
        })

def comment(request, item_id):
    if request.method == "POST":
        listed = Listing.objects.get(pk=item_id)
        user_id = request.user
        username = user_id.username
        comment = request.POST.get("new_comment")
        new_comment = Comment.objects.create(listing_id=Listing.objects.get(listed_id=item_id),
            commenter=username, comment=comment)
        new_comment.save()
        return HttpResponseRedirect(reverse("index"))
