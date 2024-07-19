from rest_framework.permissions import BasePermission

from boranga.helpers import (
    is_external_contributor,
    is_internal_contributor,
)

class TileLayerPermission(BasePermission):
    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False

        return any(
            [
                p(request)
                for p in [is_external_contributor, is_internal_contributor]
            ]
        )
