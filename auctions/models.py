from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass

class Listing(models.Model):
	listed_id = models.AutoField(auto_created=True, primary_key=True)
	item_name = models.CharField(max_length=64)
	item_description = models.CharField(max_length=500, default="no description")
	seller = models.CharField(max_length=64)
	price = models.DecimalField(max_digits=19, decimal_places=2)
	category = models.CharField(max_length=12, default="no category")
	image = models.CharField(max_length=255, default="no image")
	listing_date = models.DateField(default=0000-00-00)

	def __str__(self):
		return f"{self.item_name} {self.seller} {self.category} {self.price}"

class Bid(models.Model):
	bid_id = models.AutoField(primary_key=True)
	listing_id = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="bidded")
	buyer = models.CharField(max_length=64)
	value = models.DecimalField(max_digits=19, decimal_places=2)

	def __str__(self):
		return f"{self.bid_id} {self.buyer} {self.value}"

class Comment(models.Model):
	comment_id = models.AutoField(primary_key=True)
	listing_id = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="commented")
	commenter = models.CharField(max_length=64)
	comment = models.CharField(max_length=200)

	def __str__(self):
		return f"{self.comment_id} {self.commenter} {self.comment}"
