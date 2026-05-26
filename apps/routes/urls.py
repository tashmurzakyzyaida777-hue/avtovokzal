from django.urls import path
from . import views

app_name = "routes"

urlpatterns = [
    path("", views.RouteListView.as_view(), name="list"),
    path("stations/", views.StationListView.as_view(), name="stations"),
    path("<int:pk>/", views.RouteDetailView.as_view(), name="detail"),
]
