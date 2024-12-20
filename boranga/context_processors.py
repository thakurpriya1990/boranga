from django.conf import settings


def config(request):
    return {
        "template_group": "bioscience",
        "template_title": settings.TEMPLATE_TITLE,
        "build_tag": settings.BUILD_TAG,
        "GIT_COMMIT_HASH": settings.GIT_COMMIT_HASH,
        "GIS_SERVER_URL": settings.GIS_SERVER_URL,
        "vue3_entry_script": settings.VUE3_ENTRY_SCRIPT,
        "use_vite_dev_server": settings.USE_VITE_DEV_SERVER,
    }
