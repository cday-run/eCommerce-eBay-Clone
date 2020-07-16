from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from .models import User, Listing, Bid, Comment, Wishlist
from django.contrib import messages
from django.db.models import Q
from django.contrib.auth.decorators import login_required
import datetime

Categories = ["Other", "Appliances", "Auto", "Clothing", "Electronics", "Home", "Kitchen", "Outdoors"]

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
        new_listing.pk
        #Add post to bids
        new_bid = Bid.objects.create(listing_id=Listing.objects.get(listed_id=new_listing.pk), 
            bidder=seller, value=price)
        new_bid.save()
        """
        ###Change redirect to listing page
        """
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/create.html", {
            "categories" : Categories
            })

def listed(request, item_id):
    listed = Listing.objects.get(pk=item_id)
    return render(request, "auctions/listed.html", {
        "listed_id": item_id,
        "title": listed.item_name,
        "description": listed.item_description,
        "price": listed.price,
        "comments": Comment.objects.filter(listing_id=item_id),
        "high_bid": Bid.objects.filter(listing_id=item_id)
        })

@login_required
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

@login_required
def bid(request, item_id):
    if request.method == "POST":
        user_id = request.user
        username = user_id.username
        bid_value = int(request.POST.get("new_bid"))
        item = Bid.objects.get(listing_id=item_id)
        current_bid = int(item.value)
        if bid_value > current_bid:
            item.value = bid_value
            item.save()
            return HttpResponseRedirect(reverse("index"))
        else:
            messages.warning(request, "Bid must be higher than current highest!")
            return HttpResponseRedirect(reverse("listed"))
    else:
        return HttpResponseRedirect(reverse("index"))

def search(request):
    #Get the title parameter from the search form input
    title = request.POST.get("q")
    #Find listings with query as a substrin in their title
    results = Listing.objects.filter(
        Q(item_name__contains=title))
    return render(request, "auctions/results.html", {
        "results": results
        })

def add_watch(request, item_id):
    if request.method == "POST":
        user = request.user
        user_id = user.id
        listed = Listing.objects.get(pk=item_id)
        if Wishlist.objects.filter(listing_id=item_id):
            messages.warning(request, "Item already on Watchlist")
            return render(request, "auctions/wishlist.html", {
                "items": Wishlist.objects.filter(user_id=user_id)
                })
        else:
            new_wishlist = Wishlist.objects.create(user_id=user_id, listing_id=Listing.objects.get(listed_id=item_id), wished_item=listed.item_name)
            new_wishlist.save()
            messages.warning(request, "Item added to Watchlist")
            return render(request, "auctions/wishlist.html", {
                "items": Wishlist.objects.filter(user_id=user_id)
                })           
    else:
        return HttpResponseRedirect(reverse("wishlist"))

def delete_watch(request, item_id):
    if request.method == "POST":
        user = request.user
        user_id = user.id
        listed = Listing.objects.get(pk=item_id)
        delete_item = Wishlist.objects.filter(listing_id=item_id).delete()
        return render( request, "auctions/wishlist.html", {
                "items": Wishlist.objects.filter(user_id=user_id)
                })

def wishlist(request):
    user = request.user
    user_id = user.id
    return render(request, "auctions/wishlist.html", {
        "items": Wishlist.objects.filter(user_id=user_id)
        })

def categories(request):
    return render(request, "auctions/categories.html", {
    "categories": Categories
    })

def filtered(request, name):
    results = Listing.objects.filter(category=name)
    return render(request, "auctions/filtered.html", {
    "results": results,
    "name" : name
    })