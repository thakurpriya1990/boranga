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
from rest_framework_datatables.utils import get_param

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

    def search_versions(self, request, queryset, view):

        search_value = get_param(request, 'search[value]')
        if (search_value):
            #get all revision ids in existing queryset
            revision_ids = queryset.distinct("revision_id").order_by("revision_id").values_list("revision_id",flat=True)
            #get all versions with those revision ids
            all_versions = Version.objects.filter(revision_id__in=revision_ids)
            #get all search fields
            fields = self.get_fields(request)
            search_fields = []
            search_fields_regex = ""
            for i in fields:
                if i['searchable']:
                    search_fields.append(i['name'][0])
                    if i['name'][0] != "revision_id" and i['name'][0] != "revision_date":
                        search_fields_regex = search_fields_regex + i['name'][0] + "|"
            if search_fields_regex:
                search_fields_regex = search_fields_regex[:-1]
            
            filter_regex = ".*\"(?:"+search_fields_regex+")\":\s\"?[\sa-zA-Z0-9-]*(?:"+search_value+")[\sa-zA-Z0-9-]*\"?.*"

            #apply search term to all searchable fields
            #revision id
            qs_revision_id = all_versions
            if "revision_id" in search_fields:
                qs_revision_id = qs_revision_id.filter(revision__id__icontains=search_value)
            
            qs_revision_date = all_versions
            #revision date
            if "revision_date" in search_fields:
                qs_revision_date = qs_revision_date.filter(revision__date_created__icontains=search_value)

            qs_revision_data = all_versions
            #otherwise, json data fields (regex?)
            if search_fields_regex:
                qs_revision_data = qs_revision_data.filter(serialized_data__iregex=filter_regex)

            #union resulting querysets
            all_versions = qs_revision_data.union(qs_revision_date).union(qs_revision_id)

            #get remaining revision ids, apply to main queryset for result
            remaining_revision_ids = list(set(all_versions.values_list("revision_id",flat=True)))
            queryset = queryset.filter(revision_id__in=remaining_revision_ids)
        
        return queryset

    def filter_queryset(self, request, queryset, view):
        total_count = queryset.count()

        queryset = queryset.annotate(data=Cast('serialized_data', JSONField()))
        fields = self.get_fields(request)
 
        #search function
        queryset = self.search_versions(request, queryset, view)
        
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
            #add other versioned models in the same revision
            revision_versions = related_versions.filter(revision_id=version.revision_id)
            data = {}
            for related_version in revision_versions:
                data[related_version.content_type.model] = related_version.data[0]

            versions_list.append({
               'revision_id': version.revision_id,
               'date_created': version.revision.date_created.strftime("%Y-%m-%d %H:%M:%S"),
               'data': data,
               }
            )

        return self.paginator.get_paginated_response(list(versions_list))