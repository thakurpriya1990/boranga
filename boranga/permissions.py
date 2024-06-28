import logging

from rest_framework import permissions
from rest_framework.permissions import BasePermission

from boranga.components.conservation_status.models import ConservationStatusReferral
from boranga.components.occurrence.models import OccurrenceReportReferral
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
        return (
            obj.referrals.filter(referral=request.user.id)
            .exclude(
                processing_status=OccurrenceReportReferral.PROCESSING_STATUS_RECALLED
            )
            .exists()
        )


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

        if hasattr(view, "action") and view.action in ["create"]:
            return (
                is_conservation_status_assessor(request)
                or is_conservation_status_approver(request)
                or is_contributor(request)
            )

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

        if obj.conservation_status.submitter == request.user.id:
            if view.action in ["update", "discard", "reinstate"]:
                return is_internal_contributor(request) or is_external_contributor(
                    request
                )

        return is_conservation_status_assessor(request)
