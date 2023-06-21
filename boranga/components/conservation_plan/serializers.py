import logging

from django.conf import settings
from ledger_api_client.ledger_models import EmailUserRO as EmailUser, Address
from boranga.components.species_and_communities.models import(
    GroupType,
    Species,
    Community,
    )
from boranga.components.conservation_plan.models import(
    ConservationPlan,
    ConservationPlanSpecies,
    ConservationPlanCommunity,
    )

from boranga.components.users.serializers import UserSerializer
from boranga.components.users.serializers import UserAddressSerializer, DocumentSerializer
from boranga.components.main.serializers import(
    CommunicationLogEntrySerializer,
    EmailUserSerializer,
    )
from boranga.ledger_api_utils import retrieve_email_user
from rest_framework import serializers
from django.db.models import Q

logger = logging.getLogger('boranga')