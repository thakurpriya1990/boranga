import logging

from rest_framework.permissions import BasePermission

from boranga.helpers import (
    is_approver,
    is_assessor,
    is_species_processor,
    is_conservation_status_editor,
    is_customer,
    is_conservation_status_referee,
    is_internal,
)

logger = logging.getLogger(__name__)

class IsAssessor(BasePermission):
    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False

        if request.user.is_superuser:
            return True

        return is_assessor(request.user)


class IsApprover(BasePermission):
    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False

        if request.user.is_superuser:
            return True

        return is_approver(request.user)
    

class IsConservationStatusEditor(BasePermission):
    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False

        if request.user.is_superuser:
            return True

        return is_conservation_status_editor(request.user)


class IsConservationStatusReferee(BasePermission):
    def has_permission(self, request, view):
        return is_conservation_status_referee(request)