from django.urls import path
from . import views

app_name = "core"

urlpatterns = [
    path("", views.HomeView.as_view(), name="home"),
    path("about/", views.AboutView.as_view(), name="about"),
    path("faq/", views.FAQView.as_view(), name="faq"),
    path("news/", views.NewsListView.as_view(), name="news"),
    path("news/<slug:slug>/", views.NewsDetailView.as_view(), name="news_detail"),
    path("contact/", views.contact, name="contact"),
    path("search/", views.search, name="search"),
    path("api/cities/", views.city_autocomplete, name="city_autocomplete"),
]
