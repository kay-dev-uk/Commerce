from datetime import datetime
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponseRedirect
from django.shortcuts import redirect, render
from django.urls import reverse
from .forms import CreateListing, CommentForm, BiddingForm

from .models import User, Listing, Comment, Bid, WatchlistItem


def index(request):
    return render(request, "auctions/index.html", {
        "listings": Listing.objects.filter(active=True)})


def create_listing(request):
    if request.method == "POST":
        form = CreateListing(request.POST)
        if form.is_valid():
            obj = Listing()
            obj.creator = User(request.user.id)
            obj.title = form.cleaned_data["title"]
            obj.category = form.cleaned_data["category"]
            obj.url = form.cleaned_data["url"]
            obj.description = form.cleaned_data["description"]
            obj.price = form.cleaned_data["price"]
            obj.winner = User(request.user.id)
            obj.save()
            return redirect(index)
    return render(request, "auctions/create_Listing.html", {"form": CreateListing})


def categories(request):
    return render(request, "auctions/categories_list.html", {
        "listings": Listing.objects.all()
    })


def category(request, category):
    if category == "no_category":
        return render(request, "auctions/category.html", {
        "listings": Listing.objects.filter(category="NO CATEGORY", active=True)
    })
    return render(request, "auctions/category.html", {
        "listings": Listing.objects.filter(category=category.upper(), active=True)
    })


def watchlist(request):
    return render(request, "auctions/watchlist.html", {
            "watchlist_items": WatchlistItem.objects.filter(user=User(request.user.id))
            })


def listing_view(request, id):
    listing = Listing.objects.get(pk=id)
    error_message = False
    closing_error = False

    if request.method == "POST" and "submit_comment" in request.POST:
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            obj = Comment()
            obj.listing = Listing.objects.get(pk=id)
            obj.commentator = User(request.user.id)
            obj.comment = comment_form.cleaned_data["comment"]
            obj.date = datetime.now()
            obj.save()

    elif request.method == "POST" and "submit_bid" in request.POST:
        bidding_form = BiddingForm(request.POST, initial={"bid": Listing.objects.get(pk=id).price})
        if bidding_form.is_valid():
            if len(Bid.objects.filter(listing=id)) == 0 and bidding_form.cleaned_data["bid"] >= Listing.objects.get(pk=id).price:
                obj = Bid()
                obj.listing = Listing.objects.get(pk=id)
                obj.bidder = User(request.user.id)
                obj.bid = bidding_form.cleaned_data["bid"]
                obj.save()
                listing.price = bidding_form.cleaned_data["bid"]
                listing.save()
            elif bidding_form.cleaned_data["bid"] > Listing.objects.get(pk=id).price:
                obj = Bid()
                obj.listing = Listing.objects.get(pk=id)
                obj.bidder = User(request.user.id)
                obj.bid = bidding_form.cleaned_data["bid"]
                obj.save()
                listing.price = bidding_form.cleaned_data["bid"]
                listing.save()
            else:
                error_message = True

    elif listing not in WatchlistItem.objects.filter(user=User(request.user.id)):
        if request.method == "POST" and "add_to_watchlist" in request.POST:
            obj = WatchlistItem()
            obj.listing = Listing.objects.get(pk=id)
            obj.user = User(request.user.id)
            obj.save()

    if listing not in WatchlistItem.objects.filter(user=User(request.user.id)):
        if request.method == "POST" and "remove_from_watchlist" in request.POST:
            WatchlistItem.objects.filter(listing=listing).delete()

    if request.method == "POST" and "close_listing" in request.POST:
        if len(Bid.objects.filter(listing=id)) == 0:
            obj = listing
            obj.active = False
            obj.winner = User(request.user.id)
            obj.winner_creator = True
            obj.save()
            closing_error = True
        elif Bid.objects.filter(listing=id).latest("bidder").bidder == listing.creator:
            obj = listing
            obj.active = False
            obj.winner = Bid.objects.filter(listing=id).latest("bidder").bidder
            obj.winner_creator = True
            obj.save()
        else:
            obj = listing
            obj.active = False
            obj.winner = Bid.objects.filter(listing=id).latest("bidder").bidder
            obj.save()

    return render(request, "auctions/listing_view.html", {
        "listing": Listing.objects.get(pk=id),
        "comments": Comment.objects.filter(listing=id),
        "comment_form": CommentForm,
        "bidding_form": BiddingForm(initial={"bid": Listing.objects.get(pk=id).price}),
        "bids": Bid.objects.filter(listing=id),
        "watchlist": WatchlistItem.objects.filter(listing=listing),
        "error_message": error_message,
        "closing_error": closing_error,
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
