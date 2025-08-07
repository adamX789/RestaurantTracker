import json
from django.shortcuts import render, redirect
from .models import *
from django.http import HttpResponse
from django.conf import settings
from django.views import View
import googlemaps
from .forms import *
from django.contrib import messages
from user_profile.models import Profile

# Create your views here.

key = settings.GOOGLE_API_KEY


def get_coords(res):
    gmaps = googlemaps.Client(settings.GOOGLE_API_KEY)
    adress_string = str(res.address + ", " + res.zipcode +
                        ", " + res.city + ", " + res.country)
    data = gmaps.geocode(adress_string)
    if data:
        geometry = data[0]["geometry"]["location"]
        lat = geometry["lat"]
        lng = geometry["lng"]
        return lat, lng
    else:
        # Vrat defaultni hodnoty nebo ošetři chybu jiným způsobem
        return 0, 0


class HomeView(View):
    def get(self, request):
        if request.user.is_authenticated:
            current_user = request.user
            restaurant_data = []
            for restaurant in Restaurant.objects.all():
                res_lat, res_lng = get_coords(restaurant)
                data = {
                    "lat": res_lat,
                    "lng": res_lng,
                    "name": restaurant.name,
                    "id": restaurant.id,
                    "people_count": restaurant.people_set.all().count(),
                }
                restaurant_data.append(data)
            form = MapForm()
            return render(request, "home.html", {"username": current_user, "locations": restaurant_data, "key": key, "form": form})
        else:
            return render(request, "not_logged_in.html", {})

    def post(self, request):
        current_user = request.user
        form = MapForm(request.POST)
        if form.is_valid():
            rest_type = form.cleaned_data["type"]
            restaurant_data = []
            if rest_type == "Všechny":
                valid_restaurants = Restaurant.objects.all()
            else:
                valid_restaurants = Restaurant.objects.filter(type=rest_type)
            for rest in valid_restaurants:
                rest_lat, rest_lng = get_coords(rest)
                data = {
                    "lat": rest_lat,
                    "lng": rest_lng,
                    "name": rest.name,
                    "id": rest.id,
                    "people_count": rest.people_set.all().count(),
                }
                restaurant_data.append(data)
        else:
            form = MapForm()
        return render(request, "home.html", {"username": current_user, "locations": restaurant_data, "key": key, "form": form})


def restaurants(request):
    res_list = Restaurant.objects.all()
    return render(request, "restaurants.html", {"restaurants": res_list})


class RestaurantView(View):
    def get(self, request, id):
        res = Restaurant.objects.get(id=id)
        profile = request.user.profile
        reviews, count, sum_, average = self._get_res_info(res)
        lat, lng = get_coords(res)
        coords = {"lat": lat, "lng": lng}
        coords_json = json.dumps(coords)
        context = {
            "restaurant": res,
            "reviews": reviews,
            "count": count,
            "average": average,
            "coords":coords_json,
            "key": key,
            "profile": profile,
            "people": res.people_set.all()
        }

        return render(request, "view.html", context)

    def post(self, request, id):
        res = Restaurant.objects.get(id=id)
        profile = request.user.profile
        reviews, count, sum_, average = self._get_res_info(res)
        lat, lng = get_coords(res)
        coords = {"lat": lat, "lng": lng}
        coords_json = json.dumps(coords)
        if request.POST.get("enter"):
            profile.in_restaurant = True
            profile.restaurant = res
            res.people_set.create(profile=profile)
        elif request.POST.get("logout"):
            profile.in_restaurant = False
            profile.restaurant = None
            res.people_set.filter(profile=profile).delete()
        res.save()
        profile.save()
        context = {
            "restaurant": res,
            "reviews": reviews,
            "count": count,
            "average": average,
            "coords":coords_json,
            "key": key,
            "profile": profile,
            "people": res.people_set.all()
        }
        return render(request, "view.html", context)

    def _get_res_info(self, res):
        count = 0
        sum_ = 0
        average = 0
        reviews = res.review_set.all()
        for r in reviews:
            count += 1
            sum_ += r.rating
        if count != 0:
            average = sum_ / count
        return reviews, count, sum_, average


class AddView(View):
    def get(self, request, id):
        res = Restaurant.objects.get(id=id)
        return render(request, "add.html", {"restaurant": res})

    def post(self, request, id):
        profile = request.user.profile
        res = Restaurant.objects.get(id=id)
        text = str(request.POST.get("text"))
        try:
            rating = float(request.POST.get("rating"))
            if 0 <= rating <= 10 and 3 <= len(text) <= 300:
                res.review_set.create(
                    profile=profile, rating=rating, text=text)
                res.save()
                return redirect("view", id=id)
        except ValueError:
            messages.error(request, "Neplatná hodnota v poli hodnocení.")
            return render(request, "add.html", {"restaurant": res})
        if rating < 0:
            messages.error(request, "Hodnocení nemůže být záporné.")
        elif rating > 10:
            messages.error(request, "Hodnocení nemůže být větší než 10.")
        if len(text) < 3:
            messages.error(request, "Text je moc krátký.")
        elif len(text) > 300:
            messages.error(request, "Text je moc dlouhý.")
        return render(request, "add.html", {"restaurant": res})
