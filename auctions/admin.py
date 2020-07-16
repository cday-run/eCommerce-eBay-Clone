from django.contrib import admin

from .models import User, Listing, Bid, Comment, Wishlist

class ListingAdmin(admin.ModelAdmin):
	list_display = ("listed_id", "item_name", "item_description", "category",
		"seller", "buyer", "price", "image", "listing_date")

class BidAdmin(admin.ModelAdmin):
	list_display = ("bid_id", "listing_id", "bidder", "value")

class CommentAdmin(admin.ModelAdmin):
	list_display = ("comment_id", "listing_id", "commenter", "comment")

# Register your models here.
admin.site.register(User)
admin.site.register(Listing, ListingAdmin)
admin.site.register(Bid, BidAdmin)
admin.site.register(Comment, CommentAdmin)
admin.site.register(Wishlist)