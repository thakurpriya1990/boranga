import logging

from django.conf import settings
from ledger_api_client.ledger_models import EmailUserRO as EmailUser, Address
from boranga.components.species_and_communities.models import(
    GroupType,
    Species,
    Community,
    Taxonomy
    )
from boranga.components.conservation_status.models import(
    ConservationStatus,
    ConservationStatus,
    ConservationStatusLogEntry,
    ConservationStatusUserAction,
    ConservationCriteria,
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


# class SpeciesConservationStatusSerializer(ConservationStatusSerializer):
#     class Meta:
#         model = ConservationStatus
#         fields = (
#             'id',
#             'conservation_status_number',
#             'species',
#             'current_conservation_status',
#             'current_conservation_list',
#             'current_conservation_category',
#             #'current_conservation_criteria',
#             'effective_status_date',
#             )


# class CommunityConservationStatusSerializer(ConservationStatusSerializer):
#     class Meta:
#         model = ConservationStatus
#         fields = (
#             'id',
#             'conservation_status_number',
#             'community',
#             'current_conservation_status',
#             'current_conservation_list',
#             'current_conservation_category',
#             #'current_conservation_criteria',
#             'effective_status_date',
#             )


class ConservationCriteriaSerializer(serializers.ModelSerializer):

    class Meta:
        model = ConservationCriteria
        fields = ('id',
            'code',
            'label'
            )
        read_only_fields = ('id',)


class ListConservationStatusSerializer(serializers.ModelSerializer):
    scientific_name = serializers.SerializerMethodField()
    community_name = serializers.SerializerMethodField()
    conservation_list = serializers.SerializerMethodField()
    conservation_category = serializers.SerializerMethodField()
    class Meta:
        model = ConservationStatus
        fields = (
                'id',
                'conservation_status_number',
                'group_type',
                'scientific_name',
                'community_name',
                'conservation_list',
                'conservation_category',
                'processing_status',
                'customer_status',
                'can_user_edit',
                'can_user_view',
            )
        datatables_always_serialize = (
                'id',
                'conservation_status_number',
                'group_type',
                'scientific_name',
                'community_name',
                'conservation_list',
                'conservation_category',
                'processing_status',
                'customer_status',
                'can_user_edit',
                'can_user_view',
            )   

    def get_scientific_name(self,obj):
        if obj.species:
            return obj.species.scientific_name.name
        return ''

    def get_community_name(self,obj):
        if obj.community:
            if obj.community.community_name:
                return obj.community.community_name.name
            else:
                return ''
        return ''

    def get_conservation_list(self,obj):
        if obj.conservation_list:
            return obj.conservation_list.code
        return ''

    def get_conservation_category(self,obj):
        if obj.conservation_category:
            return obj.conservation_category.code
        return ''


class ListSpeciesConservationStatusSerializer(serializers.ModelSerializer):
    group_type = serializers.SerializerMethodField()
    species_number = serializers.SerializerMethodField()
    scientific_name = serializers.SerializerMethodField()
    common_name = serializers.SerializerMethodField()
    family = serializers.SerializerMethodField()
    genus = serializers.SerializerMethodField()
    phylogenetic_group = serializers.SerializerMethodField()
    conservation_list = serializers.SerializerMethodField()
    conservation_category = serializers.SerializerMethodField()
    region = serializers.SerializerMethodField()
    district = serializers.SerializerMethodField()
    class Meta:
        model = ConservationStatus
        fields = (
                'id',
                'conservation_status_number',
                'group_type',
                'species_number',
                'scientific_name',
                'common_name',
                'family',
                'genus',
                'phylogenetic_group',
                'region',
                'district',
                'conservation_list',
                'conservation_category',
                'processing_status',
                'customer_status',
                'can_user_edit',
                'can_user_view',
            )
        datatables_always_serialize = (
                'id',
                'conservation_status_number',
                'group_type',
                'species_number',
                'scientific_name',
                'common_name',
                'family',
                'genus',
                'phylogenetic_group',
                'region',
                'district',
                'conservation_list',
                'conservation_category',
                'processing_status',
                'customer_status',
                'can_user_edit',
                'can_user_view',
            )   

    def get_group_type(self,obj):
        if obj.species:
            return obj.species.group_type.name
        else:
            return obj.application_type.name # if user haven't filled up the form yet(ie. species not selected)

    def get_species_number(self,obj):
        if obj.species:
            return obj.species.species_number
        return ''

    def get_scientific_name(self,obj):
        if obj.species:
            return obj.species.scientific_name.name
        return ''

    def get_common_name(self,obj):
        if obj.species:
            return obj.species.common_name
        return ''

    def get_family(self,obj):
        try:
            if obj.species:
                taxonomy = Taxonomy.objects.get(species=obj.species)
                if taxonomy.family:
                    return taxonomy.family.name
        except Taxonomy.DoesNotExist:
            return ''

    def get_genus(self,obj):
        try:
            if obj.species:
                taxonomy = Taxonomy.objects.get(species=obj.species)
                if taxonomy.genus:
                    return taxonomy.genus.name
        except Taxonomy.DoesNotExist:
            return ''

    def get_phylogenetic_group(self,obj):
        try:
            if obj.species:
                taxonomy = Taxonomy.objects.get(species=obj.species)
                if taxonomy.phylogenetic_group:
                    return taxonomy.phylogenetic_group.name
        except Taxonomy.DoesNotExist:
            return ''

    def get_conservation_list(self,obj):
        if obj.conservation_list:
            return obj.conservation_list.code
        return ''

    def get_conservation_category(self,obj):
        if obj.conservation_category:
            return obj.conservation_category.code
        return ''

    def get_region(self,obj):
        if obj.species:
            if obj.species.region:
                return obj.species.region.name
        return ''

    def get_district(self,obj):
        if obj.species:
            if obj.species.district:
                return obj.species.district.name
        return ''


class ListCommunityConservationStatusSerializer(serializers.ModelSerializer):
    group_type = serializers.SerializerMethodField()
    community_number = serializers.SerializerMethodField()
    community_migrated_id = serializers.SerializerMethodField()
    community_name = serializers.SerializerMethodField()
    community_status = serializers.SerializerMethodField()
    #conservation_status = serializers.SerializerMethodField()
    conservation_list = serializers.SerializerMethodField()
    conservation_category = serializers.SerializerMethodField()
    region = serializers.SerializerMethodField()
    district = serializers.SerializerMethodField()
    class Meta:
        model = ConservationStatus
        fields = (
                'id',
                'conservation_status_number',
                'group_type',
                'community_number',
                'community_migrated_id',
                'community_name',
                'community_status',
                #'conservation_status',
                'conservation_list',
                'conservation_category',
                'region',
                'district',
                'processing_status',
                'customer_status',
                'can_user_edit',
                'can_user_view',
            )
        datatables_always_serialize = (
                'id',
                'conservation_status_number',
                'community_number',
                'group_type',
                'community_migrated_id',
                'community_name',
                'community_status',
                #'conservation_status',
                'conservation_list',
                'conservation_category',
                'region',
                'district',
                'processing_status',
                'customer_status',
                'can_user_edit',
                'can_user_view',
            )

    def get_group_type(self,obj):
        if obj.community:
            return obj.community.group_type.name
        else:
            return obj.application_type.name # if user haven't filled up the form yet(ie. species not selected)

    # def get_conservation_status(self,obj):
    #   try:
    #       conservation_status = ConservationStatus.objects.get(community=obj)
    #       return conservation_status.conservation_list.code
    #   except ConservationStatus.DoesNotExist:
    #       return None

    def get_community_number(self,obj):
        if obj.community:
            return obj.community.community_number
        return ''

    def get_community_migrated_id(self,obj):
        if obj.community:
            return obj.community.community_migrated_id
        return ''

    def get_community_name(self,obj):
        if obj.community:
            return obj.community.community_name.name
        return ''

    def get_community_status(self,obj):
        if obj.community:
            return obj.community.community_status
        return ''

    def get_conservation_list(self,obj):
        if obj.conservation_list:
            return obj.conservation_list.code
        return ''

    def get_conservation_category(self,obj):
        if obj.conservation_category:
            return obj.conservation_category.code
        return ''

    def get_region(self,obj):
        if obj.community:
            if obj.community.region:
                return obj.community.region.name
        return ''

    def get_district(self,obj):
        if obj.community:
            if obj.community.district:
                return obj.community.district.name
        return ''


class BaseConservationStatusSerializer(serializers.ModelSerializer):
    readonly = serializers.SerializerMethodField(read_only=True)
    group_type = serializers.SerializerMethodField(read_only=True)
    conservation_criteria = serializers.SerializerMethodField()
    previous_name = serializers.SerializerMethodField()
    allowed_assessors = EmailUserSerializer(many=True)

    class Meta:
        model = ConservationStatus
        fields = (
                'id',
                'group_type',
                'species_id',
                'previous_name',
                'community_id',
                'conservation_status_number',
                'conservation_list_id',
                'conservation_category_id',
                'conservation_criteria',
                'comment',
                'proposed_date',
                'lodgement_date',
                'applicant_type',
                'applicant',
                'submitter',
                'assigned_officer',
                'customer_status',
                'processing_status',
                'review_status',
                'readonly',
                'can_user_edit',
                'can_user_view',
                'reference',
                'applicant_details',
                'assigned_officer',
                'assigned_approver',
                'allowed_assessors',
                )

    def get_readonly(self,obj):
        return False
    
    def get_group_type(self,obj):
        if obj.species:
            return obj.species.group_type.name
        elif obj.community:
            return obj.community.group_type.name
        else:
            return obj.application_type.name

    def get_conservation_criteria(self,obj):
        return [c.id for c in obj.conservation_criteria.all()]

    def get_previous_name(self,obj):
        try:
            if obj.species:
                taxonomy = Taxonomy.objects.get(species=obj.species)
                if taxonomy.previous_name:
                    return taxonomy.previous_name
        except Taxonomy.DoesNotExist:
            return ''

    def get_processing_status(self,obj):
        return obj.get_processing_status_display()

    def get_review_status(self,obj):
        return obj.get_review_status_display()

    def get_customer_status(self,obj):
        return obj.get_customer_status_display()


class ConservationStatusSerializer(BaseConservationStatusSerializer):
    submitter = serializers.SerializerMethodField(read_only=True)
    processing_status = serializers.SerializerMethodField(read_only=True)
    review_status = serializers.SerializerMethodField(read_only=True)
    customer_status = serializers.SerializerMethodField(read_only=True)

    def get_readonly(self,obj):
        return obj.can_user_view

    def get_submitter(self,obj):
        if obj.submitter:
            email_user = retrieve_email_user(obj.submitter)
            return email_user.get_full_name()
        else:
            return None
    

class CreateConservationStatusSerializer(BaseConservationStatusSerializer):
    application_type = serializers.IntegerField(required=False, allow_null=True, write_only= True)
    class Meta:
        model = ConservationStatus
        fields = (
            'id',
            'application_type',
            'submitter',
            )
        read_only_fields = (
            'id',
            'application_type',
            'submitter',
            )


class InternalSpeciesConservationStatusSerializer(BaseConservationStatusSerializer):
    submitter = serializers.SerializerMethodField(read_only=True)
    processing_status = serializers.SerializerMethodField(read_only=True)
    customer_status = serializers.SerializerMethodField(read_only=True)
    current_assessor = serializers.SerializerMethodField()
    allowed_assessors = EmailUserSerializer(many=True)
    assessor_mode = serializers.SerializerMethodField()
    # accessing_user_roles = (
    #     serializers.SerializerMethodField()
    # )

    class Meta:
        model = ConservationStatus
        fields = (
                'id',
                'group_type',
                'species_id',
                'previous_name',
                'conservation_status_number',
                'conservation_list_id',
                'conservation_category_id',
                'conservation_criteria',
                'comment',
                'proposed_date',
                'processing_status',
                'customer_status',
                'readonly',
                'lodgement_date',
                'submitter',
                'applicant_type',
                'assigned_officer',
                'assigned_approver',
                'can_user_edit',
                'can_user_view',
                'current_assessor',
                'allowed_assessors',
                'assessor_mode',
                'accessing_user_roles',
                )

    # def get_accessing_user_roles(self, conservation_status):
    #     request = self.context.get("request")
    #     accessing_user = request.user
    #     roles = []
    #     if (
    #         accessing_user.id
    #         in conservation_status.get_assessor_group().get_system_group_member_ids()
    #     ):
    #         roles.append("assessor")
    #     if (
    #         accessing_user.id
    #         in conservation_status.get_approver_group().get_system_group_member_ids()
    #     ):
    #         roles.append("approver")
    #     referral_ids = list(conservation_status.referrals.values_list("referral", flat=True))
    #     if accessing_user.id in referral_ids:
    #         roles.append("referral")
    #     return roles


    def get_submitter(self, obj):
        if obj.submitter:
            email_user = retrieve_email_user(obj.submitter)
            return EmailUserSerializer(email_user).data
        else:
            return None

    def get_readonly(self,obj):
        return True

    def get_current_assessor(self, obj):
        return {
            "id": self.context["request"].user.id,
            "name": self.context["request"].user.get_full_name(),
            "email": self.context["request"].user.email,
        }

    def get_assessor_mode(self,obj):
        # TODO check if the proposal has been accepted or declined
        request = self.context["request"]
        user = (
            request.user._wrapped if hasattr(request.user, "_wrapped") else request.user
        )
        return {
            "assessor_mode": True,
            "has_assessor_mode": obj.has_assessor_mode(user),
            "assessor_can_assess": obj.can_assess(user),
            "assessor_level": "assessor",
            "assessor_box_view": obj.assessor_comments_view(user),
        }


class SaveSpeciesConservationStatusSerializer(BaseConservationStatusSerializer):
    species_id = serializers.IntegerField(required=False, allow_null=True, write_only= True)
    conservation_list_id = serializers.IntegerField(required=False, allow_null=True, write_only= True)
    conservation_category_id = serializers.IntegerField(required=False, allow_null=True, write_only= True)
    #conservation_criteria = ConservationCriteriaSerializer(read_only = True)

    class Meta:
        model = ConservationStatus
        fields = (
                'id',
                'application_type',
                'species_id',
                'conservation_list_id',
                'conservation_category_id',
                'comment',
                'lodgement_date',
                'applicant_type',
                'submitter',
                'readonly',
                'can_user_edit',
                'can_user_view',
                'reference',
                )
        read_only_fields=('id',)


class CreateSpeciesConservationStatusSerializer(BaseConservationStatusSerializer):
    class Meta:
        model = ConservationStatus
        fields = ('id',
                )
        read_only_fields = (
            'id',
            )


class InternalCommunityConservationStatusSerializer(BaseConservationStatusSerializer):
    submitter = serializers.SerializerMethodField(read_only=True)
    processing_status = serializers.SerializerMethodField(read_only=True)
    customer_status = serializers.SerializerMethodField(read_only=True)
    current_assessor = serializers.SerializerMethodField()
    allowed_assessors = EmailUserSerializer(many=True)
    # accessing_user_roles = (
    #     serializers.SerializerMethodField()
    # )

    class Meta:
        model = ConservationStatus
        fields = (
                'id',
                'group_type',
                'community_id',
                'conservation_status_number',
                'conservation_list_id',
                'conservation_category_id',
                'conservation_criteria',
                'comment',
                'proposed_date',
                'processing_status',
                'customer_status',
                'readonly',
                'lodgement_date',
                'submitter',
                'applicant_type',
                'assigned_officer',
                'assigned_approver',
                'can_user_edit',
                'can_user_view',
                'current_assessor',
                'allowed_assessors',
                'accessing_user_roles',
                )

    # def get_accessing_user_roles(self, conservation_status):
    #     request = self.context.get("request")
    #     accessing_user = request.user
    #     roles = []
    #     if (
    #         accessing_user.id
    #         in conservation_status.get_assessor_group().get_system_group_member_ids()
    #     ):
    #         roles.append("assessor")
    #     if (
    #         accessing_user.id
    #         in conservation_status.get_approver_group().get_system_group_member_ids()
    #     ):
    #         roles.append("approver")
    #     referral_ids = list(conservation_status.referrals.values_list("referral", flat=True))
    #     if accessing_user.id in referral_ids:
    #         roles.append("referral")
    #     return roles

    def get_submitter(self, obj):
        if obj.submitter:
            email_user = retrieve_email_user(obj.submitter)
            return EmailUserSerializer(email_user).data
        else:
            return None

    def get_readonly(self,obj):
        return True

    def get_current_assessor(self, obj):
        return {
            "id": self.context["request"].user.id,
            "name": self.context["request"].user.get_full_name(),
            "email": self.context["request"].user.email,
        }


class SaveCommunityConservationStatusSerializer(BaseConservationStatusSerializer):
    community_id = serializers.IntegerField(required=False, allow_null=True, write_only= True)
    conservation_list_id = serializers.IntegerField(required=False, allow_null=True, write_only= True)
    conservation_category_id = serializers.IntegerField(required=False, allow_null=True, write_only= True)
    #conservation_criteria = ConservationCriteriaSerializer(read_only = True)

    class Meta:
        model = ConservationStatus
        fields = (
                'id',
                'application_type',
                'community_id',
                'conservation_list_id',
                'conservation_category_id',
                'comment',
                'lodgement_date',
                'applicant_type',
                'submitter',
                'readonly',
                'can_user_edit',
                'can_user_view',
                'reference',
                )
        read_only_fields=('id',)


class ConservationStatusUserActionSerializer(serializers.ModelSerializer):
    who = serializers.SerializerMethodField()
    class Meta:
        model = ConservationStatusUserAction
        fields = '__all__'

    def get_who(self, conservation_status_user_action):
        email_user = retrieve_email_user(conservation_status_user_action.who)
        fullname = email_user.get_full_name()
        return fullname


class ConservationStatusLogEntrySerializer(CommunicationLogEntrySerializer):
    documents = serializers.SerializerMethodField()

    class Meta:
        model = ConservationStatusLogEntry
        fields = "__all__"
        read_only_fields = ("customer",)

    def get_documents(self, obj):
        return [[d.name, d._file.url] for d in obj.documents.all()]
