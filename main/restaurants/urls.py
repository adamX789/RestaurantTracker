from django.urls import path
from .views import *

urlpatterns = [
    path("", restaurants, name="restaurants"),
    path("<int:id>/", RestaurantView.as_view(), name="view"),
    path("<int:id>/add/", AddView.as_view(), name="add"),
]
