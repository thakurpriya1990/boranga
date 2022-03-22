from django.conf import settings
from rest_framework import routers
from boranga.components.species_and_communities import docs_api
from django.conf.urls import url

# API patterns
router = routers.DefaultRouter()
router.register(r'species_documents_paginated', docs_api.SpeciesDocumentsViewSet)

api_patterns = [

]

# URL Patterns
urlpatterns = [
    # url(r'^internal/proposal/(?P<proposal_pk>\d+)/referral/(?P<referral_pk>\d+)/$', views.ReferralView.as_view(), name='internal-referral-detail'),
    # url(r'^proposal/$', proposal_views.ProposalView.as_view(), name='proposal'),
]