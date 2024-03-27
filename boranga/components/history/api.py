from django.apps import apps
from rest_framework.response import Response
from rest_framework.exceptions import PermissionDenied
from rest_framework.mixins import ListModelMixin
from rest_framework import views
from reversion.models import Version
from boranga.helpers import is_internal
from rest_framework_datatables.pagination import PageNumberPagination
import json

class InternalAuthorizationView(views.APIView):
    """ This ViewSet adds authorization that only allows internal users to
        return data.
    """
    def get(self, request):
        """ Deny access to the version history for external users """
        #TODO utilise model specific permissions
        if not is_internal(self.request):
            raise PermissionDenied()
        
class GetPaginatedVersionsView(InternalAuthorizationView):
    paginator = PageNumberPagination()
    paginator.page_size = 10

    """ A View to return all unique (no duplicated) versions of a model as .json """
    def get(self, request, app_label, component_name, model_name, pk, reference_id_field):
        """ Returns all versions for any model object

            api/history/app_label/component_name/model_name/pk/

            Example:

            api/history/boranga/species_communities/SpeciesDocument/729
        """
        super().get(self)

        model = apps.get_model(app_label=app_label, model_name=model_name)
        instance = model.objects.get(pk=int(pk))

        #revision_comment_filter = request.GET.get('revision_comment_filter')
#
        #if revision_comment_filter:
        #    versions = Version.objects.get_for_object(instance).select_related('revision')\
        #    .filter(revision__comment__contains=revision_comment_filter).get_unique()
        #else:
        versions = Version.objects.get_for_object(instance)#.select_related('revision')\
        #.get_unique()

        #print(versions.count())
        versions = self.paginator.paginate_queryset(versions,request, view=self)

        #replace this with a serializer
        # Build the list of versions
        versions_list = []
        for index, version in enumerate(versions):
            ref_number = f'{getattr(instance, reference_id_field)}-{version.revision_id}'
            versions_list.append({
                'ref_number': ref_number,
                'date_created': version.revision.date_created,
                'data': json.loads(version.serialized_data)
                }
            )

        return self.paginator.get_paginated_response(versions_list)