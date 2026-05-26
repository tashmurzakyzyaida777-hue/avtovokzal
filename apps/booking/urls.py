from django.urls import path
from . import views

app_name = "booking"

urlpatterns = [
    path("select-seats/<int:trip_id>/", views.select_seats, name="select_seats"),
    path("passengers/<int:trip_id>/", views.passengers, name="passengers"),
    path("confirm/<int:trip_id>/", views.confirm, name="confirm"),
    path("b/<str:code>/", views.detail, name="detail"),
    path("b/<str:code>/cancel/", views.cancel, name="cancel"),
    path("ticket/<str:code>/", views.ticket, name="ticket"),
]
