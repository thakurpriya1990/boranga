from django.conf import settings
from django.core.cache import cache
from confy import env
import json

from boranga.settings import (
    KMI_SERVER_URL,
)
 
def config(request):
    config = {
        'template_group': 'bioscience',
        'template_title': settings.TEMPLATE_TITLE,
        'build_tag': settings.BUILD_TAG,
        "KMI_SERVER_URL": KMI_SERVER_URL,
    }
    #print( config )
    return config

