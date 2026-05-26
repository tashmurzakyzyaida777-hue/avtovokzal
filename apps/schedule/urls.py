from django.urls import path
from . import views

app_name = "schedule"

urlpatterns = [
    path("", views.TripListView.as_view(), name="trip_list"),
    path("<int:pk>/", views.TripDetailView.as_view(), name="trip_detail"),
    path("<int:pk>/seats.json", views.trip_seats_json, name="trip_seats_json"),
]
