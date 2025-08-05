from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class Motto(models.Model):
    text = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self) -> str:
        return str(self.text)

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    motto = models.ForeignKey(Motto, on_delete=models.SET_NULL,null=True,blank=True)
    in_restaurant = models.BooleanField(default=False)
    restaurant = models.ForeignKey(
        "restaurants.Restaurant", on_delete=models.SET_NULL, null=True, blank=True,default=None)

    def __str__(self) -> str:
        return str(self.user.username)
