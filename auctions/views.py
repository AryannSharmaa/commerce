from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from .models import User,Listing,Category,Comment,Bid


def index(request):
    all_listing=Listing.objects.filter(isActive=True)
    return render(request, "auctions/index.html",{
        "alllistings":all_listing
    })

def watchlist(request):
    cur_user=request.user
    watch=cur_user.watchlist.all()
    return render(request,"auctions/watchlist.html",{
        "watchlist":watch
    })

def bid(request):
    listingid=request.POST["id"]
    bidval=request.POST["bid"]
    listingg=Listing.objects.get(pk=listingid)
    listingg.price=bidval
    
    curuser=request.user
    bidd=Bid(bid=bidval,user=curuser)
    bidd.save()
    listingg.bid=bidd
    listingg.save()
    return HttpResponseRedirect(reverse(listing,args=(listingid,)))

def close(request):
    listingid=request.POST["id"]
    listingg=Listing.objects.get(pk=listingid)
    listingg.isActive=False
    listingg.save()
    return HttpResponseRedirect(reverse(listing,args=(listingid,)))

    

def addcomment(request):
    cur_user=request.user
    comment=request.POST["comment"]
    listingid=request.POST["id"]
    listingg=Listing.objects.get(pk=listingid)
    
    comment=Comment(author=cur_user,listing=listingg,message=comment)
    comment.save()

    return HttpResponseRedirect(reverse(listing,args=(listingid,)))

def add(request,listing_id):
    item=Listing.objects.get(pk=listing_id)
    currentuser=request.user
    item.watchlist.add(currentuser)
    return HttpResponseRedirect(reverse(listing,args=(item.id,)))

def remove(request,listing_id):
    item=Listing.objects.get(pk=listing_id)
    currentuser=request.user
    item.watchlist.remove(currentuser)
    return HttpResponseRedirect(reverse(listing,args=(item.id,)))

def listing(request,listing_id):
    item=Listing.objects.get(pk=listing_id)
    watchlist_user=item.watchlist.all()
    comment=item.comment.all()
    currentuser=request.user
    ans=currentuser in watchlist_user

    return render(request,"auctions/listing.html",{
        "item":item,
        "watchlist":ans,
        "comments":comment
    })

def categories(request):
    categories=Category.objects.all()
    return render(request,"auctions/categories.html",{
        "categories":categories
    })

def dispcategory(request,category_id):
    category =Category.objects.get(id=category_id)
    all_cat=category.category.all()
    return render(request,"auctions/dispcategory.html",{
        "item":all_cat
    })


def createListing(request):
    if request.method=="GET":
        all_listing=Category.objects.all()
        all_user=User.objects.all()
        return render(request,"auctions/create.html",{
            "listings":all_listing,
            "users":all_user

        })
    
    elif request.method=="POST":
        title=request.POST["title"]
        description=request.POST["description"]
        url=request.POST["url"]
        price=request.POST["price"]
        currentUser=request.user
        category=request.POST["category"]
        category_data=Category.objects.get(categoryName=category)
        new_listing=Listing(
            title=title,
            description=description,
            imageUrl=url,
            price=float(price),
            owner=currentUser,
            category=category_data
        )
        new_listing.save()
        return HttpResponseRedirect(reverse(index))


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
