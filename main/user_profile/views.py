from django.shortcuts import render, redirect
from .models import *
from django.http import HttpResponse
from django.conf import settings
from django.views import View
from restaurants.models import *
from django.contrib import messages


# Create your views here.

class ProfileView(View):
    def get(self, request):
        profile = request.user.profile
        reviews = profile.review_set.all()
        username = request.user.username
        motto_text = profile.motto.text if profile.motto else ""
        return render(request, "profile.html", {"username": username, "motto": motto_text, "reviews": reviews})

    def post(self, request):
        profile = request.user.profile
        reviews = profile.review_set.all()
        username = request.user.username
        print(request.POST.get)
        if request.POST.get("motto"):
            motto = str(request.POST.get("motto"))
            if len(motto) < 3:
                messages.error(request, "Vaše motto je moc krátké.")
            elif len(motto) > 100:
                messages.error(request, "Vaše motto je moc dlouhé.")
            else:
                if profile.motto:
                    profile.motto.text = motto
                else:
                    m = Motto.objects.create(text=motto)
                    profile.motto = m
                profile.motto.save()
                profile.save()
        else:
            for r in reviews:
                if request.POST.get("s" + str(r.id)) == "s":
                    r.delete()
            profile.save()
            reviews = profile.review_set.all()
        return render(request, "profile.html", {"username": username, "motto": profile.motto.text if profile.motto else "", "reviews": reviews})
