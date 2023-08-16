import logging

from django.conf import settings
from ledger_api_client.ledger_models import EmailUserRO as EmailUser, Address
from boranga.components.species_and_communities.models import(
    GroupType,
    Species,
    Community,
    Taxonomy,
    CommunityTaxonomy
    )
from boranga.components.occurrence.models import(
    OccurrenceReport,
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

class ListOccurrenceReportSerializer(serializers.ModelSerializer):
    group_type = serializers.SerializerMethodField()
    scientific_name = serializers.SerializerMethodField()
    community_name = serializers.SerializerMethodField()
    customer_status = serializers.CharField(source='get_customer_status_display')
    class Meta:
        model = OccurrenceReport
        fields = (
                'id',
                'occurrence_report_number',
                'group_type',
                'scientific_name',
                'community_name',
                'processing_status',
                'customer_status',
                'can_user_edit',
                'can_user_view',
            )
        datatables_always_serialize = (
                'id',
                'occurrence_report_number',
                'group_type',
                'scientific_name',
                'community_name',
                'processing_status',
                'customer_status',
                'can_user_edit',
                'can_user_view',
            )   

    def get_group_type(self,obj):
        if obj.group_type:
            return obj.group_type.get_name_display()
        return ''

    def get_scientific_name(self,obj):
        if obj.species:
            if obj.species.taxonomy:
                return obj.species.taxonomy.scientific_name
        return ''

    def get_community_name(self,obj):
        if obj.community:
            try:
                taxonomy = CommunityTaxonomy.objects.get(community = obj.community)
                return taxonomy.community_name
            except CommunityTaxonomy.DoesNotExist:
                return ''
        return ''

