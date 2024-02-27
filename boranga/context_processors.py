from django.conf import settings
from django.core.cache import cache
from confy import env
import json

from boranga.settings import (
    KMI_SERVER_URL,
)
 
def config(request):
    page_status = {'species_and_communities': False, 'conservation_status': False, 'meetings': False, 'occurrence_report': False}
    if request.path == '/internal/species-communities':
        page_status['species_and_communities'] = True
    elif request.path == '/internal/conservation-status':
        page_status['conservation_status'] = True
    elif request.path == '/internal/meetings':
        page_status['meetings'] = True
    elif request.path == '/external/conservation-status':
        page_status['conservation_status'] = True
    elif request.path == '/external/occurrence-report':
        page_status['occurrence_report'] = True
    config = {
        'template_group': 'bioscience',
        'template_title': settings.TEMPLATE_TITLE,
        'build_tag': settings.BUILD_TAG,
        "KMI_SERVER_URL": KMI_SERVER_URL,
        'app_build_url': settings.DEV_APP_BUILD_URL,
        'page_status': page_status,
    }
    #print( config )
    return config

