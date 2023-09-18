from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("create",views.createListing,name="create"),
    path("listing/<int:listing_id>",views.listing,name="listing"),
    path("categories",views.categories,name="categories"),
    path("dispcategory/<int:category_id>",views.dispcategory,name="dispcategory"),
    path("add/<int:listing_id>",views.add,name="add"),
    path("remove/<int:listing_id>", views.remove,name="remove"),
    path("watchlist",views.watchlist,name="watchlist"),
    path("addcomment",views.addcomment,name="addcomment"),
    path("bid",views.bid,name="bid"),
    path("close",views.close,name="close"),
]
