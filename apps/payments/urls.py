from django.urls import path
from . import views

app_name = "payments"

urlpatterns = [
    path("checkout/<str:code>/", views.checkout, name="checkout"),
    path("success/<str:code>/", views.success, name="success"),
]
