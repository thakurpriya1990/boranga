from django.conf import settings
from django.urls import include
from rest_framework import routers
from boranga.components.species_and_communities import docs_api
from django.conf.urls import url

# API patterns
router = routers.DefaultRouter()
router.register(r'species_documents', docs_api.SpeciesDocumentsViewSet)

api_patterns = [
]

# URL Patterns
urlpatterns = [
    url(r'^docs_api/',include(router.urls)),
    url(r'^docs_api/species_data/species_data_internal/(?P<species_id>[0-9]+)/', docs_api.species_data_internal, name='species_data_internal'),
    url(r'^docs_api/species_documents/species_documents_list/$', docs_api.SpeciesDocumentsViewSet.as_view({'get': 'list'}), name='species_documents'),
]