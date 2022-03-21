from django.conf import settings
from django.core.cache import cache
import json
 
def config(request):
    config = {
        'template_group': 'bioscience',
        'template_title': settings.TEMPLATE_TITLE,
        'build_tag': settings.BUILD_TAG,
    }
    #print( config )
    return config
