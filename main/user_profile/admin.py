from django.contrib import admin
from .models import *

# Register your models here.


class ProfileAdmin(admin.ModelAdmin):
    list_display = ("user", "motto", "in_restaurant", "restaurant")


class MottoAdmin(admin.ModelAdmin):
    list_display = ["text"]


admin.site.register(Profile, ProfileAdmin)
admin.site.register(Motto, MottoAdmin)
