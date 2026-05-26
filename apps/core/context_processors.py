from django.conf import settings


def site_meta(request):
    return {
        "SITE_NAME": getattr(settings, "SITE_NAME", "AvtoBilet"),
        "SITE_TAGLINE": getattr(settings, "SITE_TAGLINE", ""),
    }
