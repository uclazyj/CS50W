from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("listings/<int:listing_id>", views.listings, name="listings"),
    path("create_listing", views.create_listing, name="create_listing"),
    path("watchlist", views.watchlist, name="watchlist"),
    path("close/<int:listing_id>", views.close, name="close"),
    path("my_listings", views.my_listings, name="my_listings"),
    path("listings_won", views.listings_won, name="listings_won"),
    path("categories", views.categories, name="categories"),
    path("category/<str:category_name>", views.category, name="category")
]
