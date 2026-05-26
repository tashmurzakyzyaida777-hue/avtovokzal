from django.urls import path
from . import views

app_name = "dashboard"

urlpatterns = [
    path("", views.index, name="index"),
    path("bookings/", views.bookings, name="bookings"),
    path("trips/", views.trips, name="trips"),
]
