from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass

class Listing(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="listings")
    title = models.CharField(max_length=64)
    description = models.CharField(max_length=64)
    starting_bid = models.DecimalField(max_digits=10, decimal_places=2)
    current_price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    num_bids = models.IntegerField(default=0)
    # optional fields
    image_url = models.URLField(blank=True, default="")
    category = models.CharField(max_length=64, blank=True, default="")

    def __str__(self):
        return f"{self.title} (starts at ${self.starting_bid})"
