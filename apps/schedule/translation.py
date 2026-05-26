from modeltranslation.translator import TranslationOptions, register
from .models import BusType


@register(BusType)
class BusTypeTR(TranslationOptions):
    fields = ("name", "description")
