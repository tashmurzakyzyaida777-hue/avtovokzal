from modeltranslation.translator import TranslationOptions, register
from .models import HeroBanner, NewsArticle, FAQ


@register(HeroBanner)
class HeroBannerTR(TranslationOptions):
    fields = ("title", "subtitle", "cta_text")


@register(NewsArticle)
class NewsArticleTR(TranslationOptions):
    fields = ("title", "summary", "body")


@register(FAQ)
class FAQTR(TranslationOptions):
    fields = ("question", "answer")
