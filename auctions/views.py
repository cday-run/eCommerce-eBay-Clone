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

#Define all possible categories for a listing
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

"""
Create a template for users to view a listing
"""
def listed(request, item_id):
    #Get information required to render the template
    user = request.user
    username = user.username
    listed = Listing.objects.get(pk=item_id)
    high_bid = Bid.objects.get(listing_id=item_id)
    winner = high_bid.bidder
    #Render the template
    return render(request, "auctions/listed.html", {
        "listed_id": item_id,
        "title": listed.item_name,
        "description": listed.item_description,
        "image": listed.image,
        "price": listed.price,
        "available": listed.available,
        "comments": Comment.objects.filter(listing_id=item_id),
        "high_bid": Bid.objects.filter(listing_id=item_id),
        "winner": winner,
        "seller": listed.seller,
        "username":username
        })

"""
Create a function that allows users to create a listing on the website
"""
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

        messages.warning(request, "Listing Created!")
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/create.html", {
            "categories" : Categories
            })

"""
Create a function that allows users to post comments on a listing 
"""
@login_required
def comment(request, item_id):
    if request.method == "POST":
        #Get the list id
        listed = Listing.objects.get(pk=item_id)
        #Get the id of the user making the comment
        user_id = request.user
        username = user_id.username
        #Get the content of the comment from the form
        comment = request.POST.get("new_comment")
        #Create the comment and save it in the Comment model
        new_comment = Comment.objects.create(listing_id=Listing.objects.get(listed_id=item_id),
            commenter=username, comment=comment)
        new_comment.save()

        #Render the listing template
        high_bid = Bid.objects.get(listing_id=item_id)
        winner = high_bid.bidder
        messages.warning(request, "Comment Posted!")
        return render(request, "auctions/listed.html", {
            "listed_id": item_id,
            "title": listed.item_name,
            "description": listed.item_description,
            "image": listed.image,
            "price": listed.price,
            "available": listed.available,
            "comments": Comment.objects.filter(listing_id=item_id),
            "high_bid": Bid.objects.filter(listing_id=item_id),
            "winner": winner,
            "seller": listed.seller,
            "username":username
        })

"""
Create a function that allows users to bid on a listing
"""
@login_required
def bid(request, item_id):
    if request.method == "POST":
        listed = Listing.objects.get(pk=item_id)
        #Get the id of the user making the bid
        user_id = request.user
        username = user_id.username
        #Get the value of the bif from the form
        bid_value = int(request.POST.get("new_bid"))
        #Get the item being bidded on
        item = Bid.objects.get(listing_id=item_id)
        current_bid = int(item.value)
        #Check that the bid is higher than the current highest bid
        if bid_value > current_bid:
            item.value = bid_value
            item.save()
            #Render the listing template
            high_bid = Bid.objects.get(listing_id=item_id)
            winner = high_bid.bidder
            messages.warning(request, "Bid Submitted!")
            return render(request, "auctions/listed.html", {
                "listed_id": item_id,
                "title": listed.item_name,
                "description": listed.item_description,
                "image": listed.image,
                "price": listed.price,
                "available": listed.available,
                "comments": Comment.objects.filter(listing_id=item_id),
                "high_bid": Bid.objects.filter(listing_id=item_id),
                "winner": winner,
                "seller": listed.seller,
                "username":username
            })
        #If bid is not higher then return an error
        else:
            #Render the listing template
            high_bid = Bid.objects.get(listing_id=item_id)
            winner = high_bid.bidder
            messages.warning(request, "Bid must be higher than current highest!")
            return render(request, "auctions/listed.html", {
                "listed_id": item_id,
                "title": listed.item_name,
                "description": listed.item_description,
                "image": listed.image,
                "price": listed.price,
                "available": listed.available,
                "comments": Comment.objects.filter(listing_id=item_id),
                "high_bid": Bid.objects.filter(listing_id=item_id),
                "winner": winner,
                "seller": listed.seller,
                "username":username
            })
    else:
        return HttpResponseRedirect(reverse("index"))

"""
Create a search funtion that allows users to query the listings
"""
def search(request):
    #Get the title parameter from the search form input
    title = request.POST.get("q")
    #Find listings with query as a substring in their title
    results = Listing.objects.filter(
        Q(item_name__contains=title))
    return render(request, "auctions/results.html", {
        "results": results
        })

"""
Give users the ability to add a listing to their watchlist
"""
@login_required
def add_watch(request, item_id):
    if request.method == "POST":
        #Get the id if the user adding the item to watchlist
        user = request.user
        user_id = user.id
        #Get the id of the item being added
        listed = Listing.objects.get(pk=item_id)
        #Check if item is already on the user's watchlist
        #If already on watchlist redirect them to their watchlist and notify them it is already it
        if Wishlist.objects.filter(listing_id=item_id):
            messages.warning(request, "Item already on Watchlist")
            return render(request, "auctions/wishlist.html", {
                "items": Wishlist.objects.filter(user_id=user_id)
                })
        #Otherwise add the item to their watchlist and redirect them to their watchlist
        else:
            new_wishlist = Wishlist.objects.create(user_id=user_id, listing_id=Listing.objects.get(listed_id=item_id), wished_item=listed.item_name)
            new_wishlist.save()
            messages.warning(request, "Item added to Watchlist")
            return render(request, "auctions/wishlist.html", {
                "items": Wishlist.objects.filter(user_id=user_id)
                })           
    else:
        return HttpResponseRedirect(reverse("wishlist"))

"""
Give users the ability to remove items from their watchlist
"""
@login_required
def delete_watch(request, item_id):
    if request.method == "POST":
        #Get the id of the user
        user = request.user
        user_id = user.id
        #Get the id of the item
        listed = Listing.objects.get(pk=item_id)
        #Remove the item from the watchlist and redirect them to their watch list
        delete_item = Wishlist.objects.filter(listing_id=item_id).delete()
        messages.warning(request, "Item removed from Watchlist")
        return render( request, "auctions/wishlist.html", {
                "items": Wishlist.objects.filter(user_id=user_id)
                })

"""
Create a route to a watchlist template for users to view their watchlist
"""
@login_required
def wishlist(request):
    user = request.user
    user_id = user.id
    return render(request, "auctions/wishlist.html", {
        "items": Wishlist.objects.filter(user_id=user_id)
        })

"""
Create a route to a categories page for users to view listing categories
"""
def categories(request):
    return render(request, "auctions/categories.html", {
    "categories": Categories
    })

"""
When user clicks on a category on the categories page return results filtered to that category
"""
def filtered(request, name):
    results = Listing.objects.filter(category=name)
    return render(request, "auctions/filtered.html", {
    "results": results,
    "name" : name
    })

"""
Give functionality to listing creator to close the listing
"""
@login_required
def close(request, item_id):
    if request.method == "POST":
        listed = Listing.objects.get(pk=item_id)
        listed.available = False
        listed.save()
        #Add message saying auction has been closed
        messages.warning(request, "Listing Has Been Closed!")
        return HttpResponseRedirect(reverse("index"))