from distutils.command.upload import upload
from django.contrib.auth.models import AbstractUser
from django.db import models

#from project2.auctions.views import watchlist


class User(AbstractUser):
    pass

class Category(models.Model):
    name = models.CharField(max_length=64)

    def __str__(self):
        return f"{self.name}"

class Listing(models.Model):
    title = models.CharField(max_length=64)
    description = models.CharField(max_length=300)
    imageURL = models.URLField(max_length=300, blank=True)
    #image = models.ImageField(upload_to="images")
    startingBid = models.FloatField()
    date = models.DateTimeField(auto_now_add=True, null=True)
    active = models.BooleanField(default=True)
    #currentBid = models.ForeignKey
    seller = models.ForeignKey(User, on_delete=models.CASCADE, related_name="sellings")
    winner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="winnings", null=True, blank=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="categories")
    watchers = models.ManyToManyField(User, blank=True, related_name="watchlist")

    def __str__(self):
        return f"{self.title}"

class Bid(models.Model):
    price = models.FloatField()
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="listingBids", null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="userBids", null=True)

    def __str__(self):
        return f"{self.user}: {self.price} for {self.listing}"

class Comment(models.Model):
    content = models.CharField(max_length=300)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="userComments")
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="listingComments", null=True)
    date = models.DateTimeField(auto_now_add=True, null=True)