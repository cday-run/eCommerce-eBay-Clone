from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass

class Listings(models.Model):
	item_name = models.CharField(max_length=64)
	item_description = models.CharField(max_length=500, default="no description")
	seller = models.CharField(max_length=64)
	price = models.DecimalField(max_digits=19, decimal_places=2)
	category = models.CharField(max_length=12, default="no category")
	image = models.CharField(max_length=255, default="no image")
	listing_date = models.DateField(default=0000-00-00)

	def __str__(self):
		return f"{self.item_name} {self.seller} {self.category} {self.price}"

class Bids(models.Model):
	item = models.ForeignKey(Listings, on_delete=models.CASCADE, related_name="listings_item")
	buyer = models.CharField(max_length=64)
	value = models.DecimalField(max_digits=19, decimal_places=2)

	def __str__(self):
		return f"{self.item_name} {self.buyer} {self.value}"

class Comments(models.Model):
	post_item = models.ForeignKey(Listings, on_delete=models.CASCADE, related_name="listed_item")
	commenter = models.CharField(max_length=64)
	comment = models.CharField(max_length=200)

	def __str__(self):
		return f"{self.item_name} {self.commenter} {self.comment}"
