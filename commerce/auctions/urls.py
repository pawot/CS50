from unicodedata import name
from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"), 
    path("new-listing", views.new_listing, name="new-listing"),
    path("closed", views.closed, name="closed"),
    path("watchlist", views.watchlist, name="watchlist"),
    path("categories", views.categories, name="categories"),
    path("<str:listing_id>/listing", views.listing, name="listing"),
    path("<str:listing_id>/comment", views.comment, name="comment"),
    path("<str:listing_id>/closing", views.closing, name="closing"),
    path("<str:listing_id>/watchlist_change", views.watchlist_change, name="watchlist_change"),
    path("<str:category_id>/listings", views.category_listings, name="category_listings"),
]
