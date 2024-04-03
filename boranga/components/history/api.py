from django.apps import apps
from rest_framework.response import Response
from rest_framework.exceptions import PermissionDenied
from rest_framework.mixins import ListModelMixin
from rest_framework import views
from reversion.models import Version
from boranga.helpers import is_internal
from rest_framework_datatables.pagination import PageNumberPagination, DatatablesPageNumberPagination
import json
from django.db.models import JSONField
from django.db.models.functions import Cast
from rest_framework_datatables.filters import DatatablesFilterBackend
from django.db.models import F

#keeping it as an APIView to control how its handled
class InternalAuthorizationView(views.APIView):
    """ This ViewSet adds authorization that only allows internal users to
        return data.
    """
    def get(self, request):
        """ Deny access to the version history for external users """
        #TODO utilise model specific permissions
        if not is_internal(self.request):
            raise PermissionDenied()
        
class VersionsFilterBackend(DatatablesFilterBackend):

    def filter_queryset(self, request, queryset, view):
        total_count = queryset.count()

        queryset = queryset.annotate(data=Cast('serialized_data', JSONField()))
        fields = self.get_fields(request)
 
        #TODO search function here
        
        ordering = []
        ordering_values = []
        for field, dir_ in self.get_ordering_fields(request, view, fields):
            ordering.append(
                '-' if dir_ == 'desc' else ''
            )
            ordering_values.append(field['name'][0])
        final_ordering_values = []
        for i in range(0,len(ordering)):

            #handle revision date and id 
            if ordering_values[i] == 'revision_id':
                final_ordering_values.append(ordering[i]+"revision")
            elif ordering_values[i] == 'revision_date':
                final_ordering_values.append(ordering[i]+"revision__date_created")
            else:
                queryset = queryset.annotate(**{'order_field'+str(i):F("data__0__fields__"+ordering_values[i])})
                final_ordering_values.append(ordering[i]+"order_field"+str(i))

        queryset = queryset.order_by(*final_ordering_values)

        return queryset

class GetPaginatedVersionsView(InternalAuthorizationView):
    filter_backend = VersionsFilterBackend
    paginator = DatatablesPageNumberPagination()
    #paginator.page_size = 2

    def get(self, request, app_label, component_name, model_name, pk):
        """ Returns all versions for any model object

            api/history/app_label/component_name/model_name/pk/

            Example:

            api/history/boranga/species_communities/SpeciesDocument/729
        """
        super().get(self)

        model = apps.get_model(app_label=app_label, model_name=model_name)
        instance = model.objects.get(pk=int(pk))

        queryset = Version.objects.get_for_object(instance)
        queryset = self.filter_backend().filter_queryset(self.request, queryset, self)

        if not self.paginator.page_size:
            self.paginator.page_size = 10

        queryset = self.paginator.paginate_queryset(queryset, request, view=self)

        # Build the list of versions
        versions_list = []
        related_versions = Version.objects.annotate(data=Cast('serialized_data', JSONField()))

        for version in queryset:
            #ref_number = f'{getattr(instance, reference_id_field)}-{version.revision_id}'

            #TODO add other versioned models in the same revision (consider transforming in to dict)
            revision_versions = related_versions.filter(revision_id=version.revision_id)
            data = {}
            for related_version in revision_versions:
                data[related_version.content_type.model] = related_version.data[0]

            versions_list.append({
               'revision_id': version.revision_id,
               'date_created': version.revision.date_created,
               'data': data,
               }
            )

        return self.paginator.get_paginated_response(list(versions_list))