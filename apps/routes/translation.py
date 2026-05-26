from modeltranslation.translator import TranslationOptions, register
from .models import City, Station, Route


@register(City)
class CityTR(TranslationOptions):
    fields = ("name", "region", "country")


@register(Station)
class StationTR(TranslationOptions):
    fields = ("name", "address")


@register(Route)
class RouteTR(TranslationOptions):
    fields = ("description",)
