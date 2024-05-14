from django.conf import settings


def config(request):
    return {
        "template_group": "bioscience",
        "template_title": settings.TEMPLATE_TITLE,
        "build_tag": settings.BUILD_TAG,
        "GIT_COMMIT_HASH": settings.GIT_COMMIT_HASH,
        "GIS_SERVER_URL": settings.GIS_SERVER_URL,
        "app_build_url": settings.DEV_APP_BUILD_URL,
    }
