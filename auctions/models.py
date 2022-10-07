from datetime import datetime
from email.policy import default
from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass


class Listing(models.Model):

    CATEGORY_CHOICES = [
        ("MISC", "MISC"),
        ("ELECTRONICS", "ELECTRONICS"),
        ("TOYS", "TOYS"),
        ("FASHION", "FASHION"),
        ("HOME", "HOME"),
        ("NO CATEGORY", "NO CATEGORY"),
    ]
    creator = models.ForeignKey(User, null=True, on_delete=models.CASCADE, related_name="creator")
    title = models.CharField(max_length=64)
    category = models.CharField(choices=CATEGORY_CHOICES, default="NO CATEGORY", max_length=20)
    url = models.URLField(blank=True)
    description = models.TextField()
    price = models.IntegerField()
    active = models.BooleanField(default=True)
    winner = models.ForeignKey(User, default=creator, null=True, on_delete=models.CASCADE, related_name="winner")
    winner_creator = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.title} auctioned by {self.creator}"


class Comment(models.Model):
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE)
    commentator = models.ForeignKey(User, on_delete=models.CASCADE)
    comment = models.TextField(max_length=500)
    date = models.DateTimeField(default=datetime.now())

    def __str__(self):
        return f"{self.commentator} replyed at {self.date}: {self.comment}"


class Bid(models.Model):
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE)
    bidder = models.ForeignKey(User, on_delete=models.CASCADE)
    bid = models.IntegerField()

    def __str__(self):
        return f"{self.bidder} bade {self.bid} on {self.listing}"


class WatchlistItem(models.Model):
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f"Watchlist item {self.id} created by {self.user}"

