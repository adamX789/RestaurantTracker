from django.contrib import admin
from .models import *


class RestaurantAdmin(admin.ModelAdmin):
    list_display = ("name", "type")


class ReviewAdmin(admin.ModelAdmin):
    list_display = ("restaurant", "profile", "text", "rating")


class PeopleAdmin(admin.ModelAdmin):
    list_display = ("restaurant", "profile")


admin.site.register(Restaurant, RestaurantAdmin)
admin.site.register(Review, ReviewAdmin)
admin.site.register(People, PeopleAdmin)
