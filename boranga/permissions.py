import json
import logging
import json

from rest_framework import permissions,serializers
from rest_framework.permissions import BasePermission

from boranga.components.conservation_status.models import (
    ConservationStatus,
    ConservationStatusReferral,
)
from boranga.components.occurrence.models import (
    OccurrenceReport,
    Occurrence,
)
from boranga.components.occurrence.models import OccurrenceReportReferral
from ledger_api_client.ledger_models import EmailUserRO as EmailUser
from boranga.helpers import (
    is_conservation_status_approver,
    is_conservation_status_assessor,
    is_conservation_status_referee,
    is_contributor,
    is_django_admin,
    is_external_contributor,
    is_internal,
    is_internal_contributor,
    is_occurrence_approver,
    is_occurrence_assessor,
    is_occurrence_report_referee,
    is_readonly_user,
    is_species_communities_approver,
)

logger = logging.getLogger(__name__)


class IsExternalContributor(BasePermission):
    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False

        if request.user.is_superuser:
            return True

        return is_external_contributor(request)


class IsInternalContributor(BasePermission):
    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False

        if request.user.is_superuser:
            return True

        return is_internal_contributor(request)


class IsReadOnlyUser(BasePermission):
    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False

        if request.user.is_superuser:
            return True

        return is_readonly_user(request)


class IsOccurrenceAssessor(BasePermission):
    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False

        if request.user.is_superuser:
            return True

        return is_occurrence_assessor(request)


class IsOccurrenceApprover(BasePermission):
    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False

        if request.user.is_superuser:
            return True

        return is_occurrence_approver(request)


class IsSpeciesCommunitiesApprover(BasePermission):
    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False

        if request.user.is_superuser:
            return True

        return is_species_communities_approver(request)


class IsConservationStatusAssessor(BasePermission):
    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False

        if request.user.is_superuser:
            return True

        return is_conservation_status_assessor(request)


class IsConservationStatusApprover(BasePermission):
    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False

        if request.user.is_superuser:
            return True

        return is_conservation_status_approver(request)


class IsConservationStatusReferee(BasePermission):
    def has_permission(self, request, view):
        return is_conservation_status_referee(request)

    def has_object_permission(self, request, view, obj):
        return (
            obj.referrals.filter(referral=request.user.id)
            .exclude(
                processing_status=ConservationStatusReferral.PROCESSING_STATUS_RECALLED
            )
            .exists()
        )


class IsOccurrenceReportReferee(BasePermission):
    def has_permission(self, request, view):
        return is_occurrence_report_referee(request)

    def has_object_permission(self, request, view, obj):

        if obj._meta.model_name == "occurrencereport":
            
            if (obj.referrals.filter(referral=request.user.id)
                .exclude(
                    processing_status=OccurrenceReportReferral.PROCESSING_STATUS_RECALLED
                )
                .exists()):
                return True
            #TODO edge case, consider not using POST for process_shapefile_document if possible
            elif hasattr(view, "action") and view.action == "process_shapefile_document":
                return (obj.referrals.filter(referral=request.user.id).exists())
            
        else:
            return obj.referral == request.user.id


class IsInternal(BasePermission):
    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False

        if request.user.is_superuser:
            return True

        return is_internal(request)


class IsDjangoAdmin(BasePermission):
    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False

        if request.user.is_superuser:
            return True

        return is_django_admin(request)


class IsAssessor(BasePermission):
    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False

        if request.user.is_superuser:
            return True

        return is_conservation_status_assessor(request) or is_occurrence_assessor(
            request
        )


class IsApprover(BasePermission):
    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False

        if request.user.is_superuser:
            return True

        return (
            is_species_communities_approver(request)
            or is_conservation_status_approver(request)
            or is_occurrence_approver(request)
        )


class MeetingPermission(BasePermission):
    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False

        if request.user.is_superuser:
            return True

        if hasattr(view, "action") and view.action == "create":
            return is_conservation_status_approver(request)

        return (
            is_readonly_user(request)
            or is_conservation_status_assessor(request)
            or is_conservation_status_approver(request)
        )

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True

        return is_conservation_status_approver(request)


class ConservationStatusPermission(BasePermission):
    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False

        if request.user.is_superuser:
            return True

        if hasattr(view, "action") and view.action == "create":
            return is_contributor(request)

        return (
            is_readonly_user(request)
            or is_conservation_status_assessor(request)
            or is_conservation_status_approver(request)
            or is_species_communities_approver(request)
            or is_occurrence_assessor(request)
            or is_occurrence_approver(request)
            or is_contributor(request)
            or is_conservation_status_referee(request)
        )

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True

        if obj.submitter == request.user.id:
            return is_contributor(request)

        return is_conservation_status_assessor(
            request
        ) or is_conservation_status_approver(request)


class ExternalConservationStatusPermission(BasePermission):
    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False

        if request.user.is_superuser:
            return True

        return is_external_contributor(request)

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True

        if obj.submitter == request.user.id:
            return is_external_contributor(request)


class ConservationStatusReferralPermission(BasePermission):
    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False

        if request.user.is_superuser:
            return True

        return (
            is_readonly_user(request)
            or is_conservation_status_assessor(request)
            or is_conservation_status_approver(request)
            or is_species_communities_approver(request)
            or is_occurrence_assessor(request)
            or is_occurrence_approver(request)
            # The following group has access to the conservation status referral
            # however the queryset is filtered to only include the conservation status referrals
            # they are assigned to
            or is_conservation_status_referee(request)
        )

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True

        if obj.referral == request.user.id and obj.processing_status not in [
            ConservationStatusReferral.PROCESSING_STATUS_RECALLED
        ]:
            return is_conservation_status_referee(request)

        return is_conservation_status_assessor(request)


class ConservationStatusAmendmentRequestPermission(BasePermission):
    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False

        if request.user.is_superuser:
            return True

        if hasattr(view, "action") and view.action == "create":
            return is_conservation_status_assessor(request)

        return (
            is_readonly_user(request)
            or is_conservation_status_assessor(request)
            or is_conservation_status_approver(request)
            or is_species_communities_approver(request)
            or is_occurrence_assessor(request)
            or is_occurrence_approver(request)
            or is_contributor(request)
        )

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True

        return is_conservation_status_assessor(request)


class ConservationStatusDocumentPermission(BasePermission):
    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False

        if request.user.is_superuser:
            return True

        if (
            hasattr(view, "action")
            and view.action in ["create"]
            and request.method == "POST"
        ):
            if is_conservation_status_assessor(
                request
            ) or is_conservation_status_approver(request):
                return True

            data_str = request.data.get("data", None)

            if not data_str:
                return False

            try:
                data = json.loads(data_str)
            except json.JSONDecodeError:
                return False

            conservation_status_id = data.get("conservation_status", None)

            if not conservation_status_id:
                return False
            try:
                conservation_status = ConservationStatus.objects.get(
                    id=conservation_status_id
                )
            except ConservationStatus.DoesNotExist:
                return False

            return conservation_status.submitter == request.user.id and is_contributor(
                request
            )

        return (
            is_readonly_user(request)
            or is_conservation_status_assessor(request)
            or is_conservation_status_approver(request)
            or is_species_communities_approver(request)
            or is_occurrence_assessor(request)
            or is_occurrence_approver(request)
            or is_contributor(request)
            or is_conservation_status_referee(request)
        )

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True

        if obj.conservation_status.submitter == request.user.id:
            if view.action in ["update", "discard", "reinstate"]:
                return is_internal_contributor(request) or is_external_contributor(
                    request
                )

        return is_conservation_status_assessor(request)


class OccurrenceReportPermission(BasePermission):
    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False

        if request.user.is_superuser:
            return True

        return (
            is_readonly_user(request)
            or is_conservation_status_assessor(request)
            or is_conservation_status_approver(request)
            or is_species_communities_approver(request)
            or is_occurrence_assessor(request)
            or is_occurrence_approver(request)
            or is_internal_contributor(request)
            or is_conservation_status_referee(request)
        )

    def is_authorised_to_update(self,request,obj):
        return ((
                obj.can_user_edit
                and (
                    request.user.id
                    == obj.submitter
                    or request.user.is_superuser
                )
            )
            or (obj.has_assessor_mode(request))
            or (obj.has_unlocked_mode(request)))
    
    def is_authorised_to_approve(self,request,obj):
        return obj.has_approver_mode(request)
    
    def is_authorised_to_assess(self,request,obj):
        return obj.has_assessor_mode(request)
    
    def is_authorised_to_assign(self, obj, assigner, assignee=None):
        # To assign a report:
        # - the report must be under assessment, the assigner must be in the assessment group,
        # and the assignee must be in the assessment group or
        # - the report must be under approval, the assigner must be in the approver group,
        # and the assignee must be in the approval group
        # AND the Assignee must be the proposed assignee, or already assigned
        in_assessor_group = assignee and (is_occurrence_assessor(self.request) or self.request.user.is_superuser)
        in_approver_group = assignee and (is_occurrence_approver(self.request) or self.request.user.is_superuser)

        self_assigning = assigner == assignee

        assigner_assigned = obj.assigned_officer == assigner.id
        assigner_approver = obj.assigned_approver == assigner.id

        return (((
            obj.processing_status
            in [
                OccurrenceReport.PROCESSING_STATUS_WITH_REFERRAL,
                OccurrenceReport.PROCESSING_STATUS_WITH_ASSESSOR,
                OccurrenceReport.PROCESSING_STATUS_UNLOCKED,
            ]
            ) and (
                (self_assigning and (in_assessor_group or in_approver_group))
                or (
                    not (assignee)
                    and assigner_assigned
                    and obj.has_assessor_mode(self.request)
                )
                or (
                    (in_assessor_group or in_approver_group)
                    and assigner_assigned
                    and obj.has_assessor_mode(self.request)
                )
            )) or ((
            obj.processing_status
            in [
                OccurrenceReport.PROCESSING_STATUS_WITH_APPROVER,
            ]
            ) and (
                (self_assigning and in_approver_group)
                or (
                    not (assignee)
                    and assigner_approver
                    and obj.has_approver_mode(self.request)
                )
                or (
                    (in_approver_group)
                    and assigner_assigned
                    and obj.has_assessor_mode(self.request)
                )
            )))
    
    def is_authorised_to_change_lock(self, request, obj):
        return obj.can_change_lock(request)

    def is_authorised_to_update_show_on_map(self, request, obj):
        if not obj.occurrence:
            return False
        return (
            (is_occurrence_approver(request) or request.user.is_superuser)
            and obj.processing_status
            in [
                OccurrenceReport.PROCESSING_STATUS_WITH_REFERRAL,
                OccurrenceReport.PROCESSING_STATUS_WITH_ASSESSOR,
                OccurrenceReport.PROCESSING_STATUS_UNLOCKED,
                OccurrenceReport.PROCESSING_STATUS_APPROVED,
            ]
            and obj.occurrence.processing_status
            in [Occurrence.PROCESSING_STATUS_ACTIVE]
        )

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS or view.action == "process_shapefile_document":
            return True
        
        if view.action in ["propose_decline","propose_approve","send_referral"]:
            return self.is_authorised_to_assess(request,obj)

        if ((view.action == "back_to_assessor" and obj.processing_status
            == OccurrenceReport.PROCESSING_STATUS_WITH_APPROVER)
            or view.action in ["decline","approve"]
            ):
            return self.is_authorised_to_approve(request,obj)
        
        if view.action == "assign_request_user":
            self.is_authorised_to_assign(obj, request.user, request.user)

        if view.action == "assign_to":
            try:
                user_id = request.data.get("assessor_id", None)
                user = EmailUser.objects.get(id=user_id)
            except EmailUser.DoesNotExist:
                raise serializers.ValidationError(
                    "A user with the id passed in does not exist"
                )
            self.is_authorised_to_assign(obj, request.user, user)

        if view.action == "unassign":
            self.is_authorised_to_assign(obj, request.user)

        if view.action in ["lock_occurrence_report","unlock_occurrence_report"]:
            return self.is_authorised_to_change_lock(request,obj)
        
        if hasattr(view, "action") and view.action == "update_show_on_map":
            return self.is_authorised_to_update_show_on_map(request, obj)

        return self.is_authorised_to_update(request,obj) 


class ExternalOccurrenceReportPermission(BasePermission):
    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False

        if request.user.is_superuser:
            return True

        return is_external_contributor(request)

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS or view.action == "process_shapefile_document":
            return True

        if obj.submitter == request.user.id and (obj.can_user_edit
            or (hasattr(view, "action") and view.action == "process_shapefile_document")):
            return is_external_contributor(request)
        

#accounts for objects that belong to an occurrence report
#only works if the object has an assigned occurrence report
class OccurrenceReportObjectPermission(BasePermission):
    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False

        if hasattr(view, "action") and view.action == "create":
            try:
                data = json.loads(request.data.get("data"))
                occurrence_report = OccurrenceReport.objects.get(id=int(data["occurrence_report"]))

                if view.basename == "ocr_amendment_request":
                    if not occurrence_report.has_assessor_mode(request):
                        return False
                elif not self.is_authorised_to_update(request, occurrence_report):
                    return False
            except:
                return False
        
        if request.user.is_superuser:
            return True

        return (
            is_readonly_user(request)
            or is_conservation_status_assessor(request)
            or is_conservation_status_approver(request)
            or is_species_communities_approver(request)
            or is_occurrence_assessor(request)
            or is_occurrence_approver(request)
            or is_internal_contributor(request)
            or is_conservation_status_referee(request)
        )
    
    def is_authorised_to_update(self, request, occurrence_report):
        user = request.user
        return (
            (
                occurrence_report.can_user_edit
                and (
                    user.id
                    == occurrence_report.submitter
                    or request.user.is_superuser
                )
            )
            or (occurrence_report.has_assessor_mode(request))
            or (occurrence_report.has_unlocked_mode(request))
            )
    
    def has_object_permission(self, request, view, obj):
        
        occurrence_report = obj.occurrence_report

        if obj._meta.model_name == "occurrencereportamendmentrequest" and occurrence_report:
            occurrence_report = obj.occurrence_report
            return occurrence_report.has_assessor_mode(request)

        if occurrence_report:
            return self.is_authorised_to_update(request,occurrence_report) 

#accounts for objects that belong to an occurrence report and can be managed externally
#only works if the object has an assigned occurrence report
class ExternalOccurrenceReportObjectPermission(BasePermission):
    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False
           
        if hasattr(view, "action") and view.action == "create":
            try:
                data = json.loads(request.data.get("data"))
                occurrence_report = OccurrenceReport.objects.get(id=int(data["occurrence_report"]))
                if not (occurrence_report and 
                        (occurrence_report.submitter == request.user.id or request.user.is_superuser) 
                        and occurrence_report.can_user_edit):
                    return False
            except:
                return False
            
        if request.user.is_superuser:
            return True
        
        return is_external_contributor(request)
    
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True

        occurrence_report = obj.occurrence_report

        if occurrence_report and occurrence_report.submitter == request.user.id and occurrence_report.can_user_edit:
            return is_external_contributor(request)

class OccurrencePermission(BasePermission):
    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False

        if request.user.is_superuser:
            return True
        
        if hasattr(view, "action") and view.action == "create":
            return is_occurrence_approver(request)

        return (
            is_readonly_user(request)
            or is_conservation_status_assessor(request)
            or is_conservation_status_approver(request)
            or is_species_communities_approver(request)
            or is_occurrence_assessor(request)
            or is_occurrence_approver(request)
            or is_conservation_status_referee(request)
        )

    def is_authorised_to_update(self,request,obj):
        return (
            (is_occurrence_approver(request) or request.user.is_superuser)
            and (
                obj.processing_status == Occurrence.PROCESSING_STATUS_ACTIVE
                or obj.processing_status == Occurrence.PROCESSING_STATUS_DRAFT
            )
        )
    
    def is_authorised_to_reopen(self,request,obj):
        return (
            (is_occurrence_approver(request) or request.user.is_superuser)
            and (
                obj.processing_status == Occurrence.PROCESSING_STATUS_HISTORICAL
            )
        )
    
    def is_authorised_to_unlock(self,request,obj):
        return (
            (is_occurrence_approver(request) or request.user.is_superuser)
            and (
                obj.processing_status == Occurrence.PROCESSING_STATUS_LOCKED
            )
        )

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True

        if hasattr(view, "action") and view.action == "unlock_occurrence":
            return self.is_authorised_to_unlock(request, obj)
        if hasattr(view, "action") and view.action == "update_show_on_map":
            return self.is_authorised_to_update_show_on_map(request, obj)
        if hasattr(view, "action") and view.action == "reopen_occurrence":
            return self.is_authorised_to_reopen(request, obj)

        return self.is_authorised_to_update(request, obj)


class OccurrenceObjectPermission(BasePermission):
    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False
        
        if hasattr(view, "action") and view.action == "create":
            try:
                data = json.loads(request.data.get("data"))
                occurrence = Occurrence.objects.get(id=int(data["occurrence"]))
                if not self.is_authorised_to_update(request, occurrence):
                    return False
            except:
                return False

        if request.user.is_superuser:
            return True

        return (
            is_readonly_user(request)
            or is_conservation_status_assessor(request)
            or is_conservation_status_approver(request)
            or is_species_communities_approver(request)
            or is_occurrence_assessor(request)
            or is_occurrence_approver(request)
            or is_conservation_status_referee(request)
        )

    def is_authorised_to_update(self,request,occurrence):
        return (
            (is_occurrence_approver(request) or request.user.is_superuser)
            and (
                occurrence.processing_status == Occurrence.PROCESSING_STATUS_ACTIVE
                or occurrence.processing_status == Occurrence.PROCESSING_STATUS_DRAFT
            )
        )

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True

        occurrence = obj.occurrence

        if occurrence:
            return self.is_authorised_to_update(request,occurrence) 
