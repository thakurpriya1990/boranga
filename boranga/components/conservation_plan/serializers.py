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

class ListSpeciesConservationPlanSerializer(serializers.ModelSerializer):
    group_type = serializers.SerializerMethodField()
    #conservation_plan_number = serializers.SerializerMethodField()
    plan_type = serializers.SerializerMethodField()
    #wa_plan_number = serializers.SerializerMethodField()
    processing_status = serializers.CharField(source='get_processing_status_display')
    region = serializers.SerializerMethodField()
    district = serializers.SerializerMethodField()
    # next_review_date = serializers.SerializerMethodField()
    # effective_from_date = serializers.SerializerMethodField()
    # effective_to_date = serializers.SerializerMethodField()

    class Meta:
        model = ConservationPlan
        fields = (
                'id',
                'group_type',
                'conservation_plan_number',
                'plan_type',
                'wa_plan_number',
                'region',
                'district',
                'next_review_date',
                'processing_status',
                'effective_from_date',
                'effective_to_date',
            )
        datatables_always_serialize = (
                'id',
                'group_type',
                'conservation_plan_number',
                'plan_type',
                'wa_plan_number',
                'region',
                'district',
                'next_review_date',
                'processing_status',
                'effective_from_date',
                'effective_to_date',
            )   

    def get_group_type(self,obj):
        # if obj.application_type:
        #     return obj.application_type.name
        # else:
            return obj.application_type.name # if user haven't filled up the form yet(ie. species not selected)
    
    def get_plan_type(self,obj):
        # if obj.application_type:
        #     return obj.application_type.name
        # else:
            return obj.plan_type.name # if user haven't filled up the form yet(ie. species not selected)
    
    def get_region(self,obj):
        return obj.region.name
    
    def get_district(self,obj):
        return obj.district.name

    # def get_effective_from_date(self,obj):
    #     try:
    #         approval = ConservationStatusIssuanceApprovalDetails.objects.get(conservation_status=obj.id)
    #         if approval.effective_from_date:
    #             return approval.effective_from_date
    #     except ConservationStatusIssuanceApprovalDetails.DoesNotExist:
    #         return ''
    
    # def get_effective_to_date(self,obj):
    #     try:
    #         approval = ConservationStatusIssuanceApprovalDetails.objects.get(conservation_status=obj.id)
    #         if approval.effective_to_date:
    #             return approval.effective_to_date
    #     except ConservationStatusIssuanceApprovalDetails.DoesNotExist:
    #         return ''
    
    