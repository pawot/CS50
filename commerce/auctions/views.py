#from unicodedata import category
from unicodedata import name
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from .models import Bid, Category, Listing, User, Comment


def index(request):
    listings = Listing.objects.filter(active=True)
    return render(request, "auctions/index.html", {
        "listings": listings
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


def new_listing(request):
    if request.method == "POST":
        # Store form data in variables
        title = request.POST["title"]
        description = request.POST["description"]
        imageURL = request.POST["imageURL"]
        startingBid = request.POST["startingBid"]
        category_id = int(request.POST["category"])
        category = Category.objects.get(pk=category_id)
        logged_user_id = request.user.id
        seller = User.objects.get(pk=logged_user_id)
        # Create and save new listing
        listing = Listing(title=title, description=description, imageURL=imageURL, startingBid=startingBid, category=category, seller=seller, active=True)
        listing.save()
        return HttpResponseRedirect(reverse("index"))

    categories = Category.objects.all()
    return render(request, "auctions/new-listing.html", {
        "categories": categories
    })


def listing(request, listing_id):
    listing = Listing.objects.get(pk=listing_id)
    comments = listing.listingComments.all()
    if request.method == "POST":
        
        price = float(request.POST["bid"])
        # Check if placed bid is valid
        if price <= listing.startingBid or (listing.listingBids.all() and price <= listing.listingBids.last().price):
            return render(request, "auctions/listing.html", {
                "listing": listing,
                "message": "Invalid bid. Bid must be higher than current price",
                "comments": comments
            }) 
        
        user = User.objects.get(pk=request.user.id)


        # Add bid to database
        bid = Bid(price=price, listing=listing, user=user)
        bid.save()
        # Set leader of the auction
        #listing.leader = user
        #listing.save()
        return render(request, "auctions/listing.html", {
            "listing": listing,
            "price": price,
            "comments": comments
        })
    if request.user.id:
        user = User.objects.get(pk=request.user.id)
        return render(request, "auctions/listing.html", {
            "listing": listing,
            "user": user,
            "comments": comments
        })
    return render(request, "auctions/listing.html", {
        "listing": listing,
        "comments": comments
    })


def closing(request, listing_id):
    listing = Listing.objects.get(pk=listing_id)
    # Set winner and change listing item
    if listing.listingBids.all():
        winner = listing.listingBids.last().user
        listing.winner = winner
    listing.active = False
    listing.save()
    return HttpResponseRedirect(reverse("index"))
    #return render(request, "auctions/closed.html")


def closed(request):
    listings = Listing.objects.filter(active=False)
    user = User.objects.get(pk=request.user.id)
    return render(request, "auctions/closed.html", {
        "listings": listings,
        "user": user
    })

@login_required(login_url='login')
def comment(request, listing_id):
    listing = Listing.objects.get(pk=listing_id)
    content = request.POST["comment"]
    user = User.objects.get(pk=request.user.id)
    comment = Comment(content=content, user=user, listing=listing)
    comment.save()
    comments = listing.listingComments.all()
    return render(request, "auctions/listing.html", {
        "listing": listing,
        "comments": comments
    })

def watchlist(request):
    user = User.objects.get(pk=request.user.id)
    listings = user.watchlist.all()
    
    return render(request, "auctions/watchlist.html", {
        "listings": listings, 
    })

def watchlist_change(request, listing_id):
    user = User.objects.get(pk=request.user.id)
    listings = user.watchlist.all()
    listing = Listing.objects.get(pk=listing_id)
    
    if listing in listings:
        user.watchlist.remove(listing)
    else:
        user.watchlist.add(listing)
    
    return render(request, "auctions/watchlist.html", {
        "listings": user.watchlist.all(), 
    })

def categories(request):
    categories = Category.objects.all()
    return render(request, "auctions/categories.html", {
        "categories": categories
    })

def category_listings(request, category_id):
    categoryName = Category.objects.get(pk=category_id)
    listings = Listing.objects.filter(category=category_id, active=True)

    return render(request, "auctions/category-listings.html", {
        "listings": listings,
        "categoryName": categoryName
    })