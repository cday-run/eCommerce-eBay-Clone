from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("create", views.create_listing, name="create_listing"),
    path("listed/<int:item_id>", views.listed, name="listed"),
    path("comment/<int:item_id>", views.comment, name="comment"),
    path("bid/<int:item_id>", views.bid, name="bid"),
    path("search", views.search, name="search"),
    path("add_watch/<int:item_id>", views.add_watch, name="add_watch"),
    path("delete_watch/<int:item_id>", views.delete_watch, name="delete_watch"),
    path("wishlist", views.wishlist, name="wishlist"),
    path("filtered/<str:name>", views.filtered, name="filtered"),
    path("categories", views.categories, name="categories"),
    path("close<int:item_id>", views.close, name="close")
] 
