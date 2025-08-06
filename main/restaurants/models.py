from django.db import models
from user_profile.models import Profile


class Restaurant(models.Model):
    name = models.CharField(max_length=100)
    zipcode = models.CharField(max_length=200, blank=True, null=True)
    city = models.CharField(max_length=200, blank=True, null=True)
    country = models.CharField(max_length=200, blank=True, null=True)
    address = models.CharField(max_length=200, blank=True, null=True)
    type = models.CharField(max_length=50, null=True)
    image = models.CharField(null=True, max_length=512)

    def __str__(self) -> str:
        return str(self.name)


class Review(models.Model):
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE)
    profile = models.ForeignKey(
        Profile, on_delete=models.CASCADE, null=True, blank=True)
    text = models.CharField(max_length=300)
    rating = models.FloatField()


class People(models.Model):
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE)
    profile = models.OneToOneField(Profile, on_delete=models.CASCADE)
