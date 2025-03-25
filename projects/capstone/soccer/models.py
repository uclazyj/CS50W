from django.contrib.auth.models import AbstractUser
from django.db import models

# Create your models here.
class User(AbstractUser):
    pass

class PlayerIcon(models.Model):
    name = models.CharField(max_length=20, unique=True)
    x_proportion = models.FloatField(null=True)
    y_proportion = models.FloatField(null=True)
    team_id = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.name} is located at x_proportion: {self.x_proportion}, y_proportion: {self.y_proportion}. Team id: {self.team_id}"

class Image(models.Model):
    image = models.ImageField(upload_to='images/')