from django.apps import apps
from rest_framework.response import Response
from rest_framework.exceptions import PermissionDenied
from rest_framework.mixins import ListModelMixin
from rest_framework import views
from reversion.models import Version
from rest_framework_datatables.pagination import PageNumberPagination, DatatablesPageNumberPagination
import json
from django.db.models import JSONField
from django.db.models.functions import Cast
from rest_framework_datatables.filters import DatatablesFilterBackend
from django.db.models import F
from rest_framework_datatables.utils import get_param
from boranga.helpers import (is_internal, is_customer,
is_boranga_admin, is_django_admin, is_assessor, is_approver,
is_species_processor, is_community_processor,
is_conservation_status_editor)
from django.db.models.expressions import Window
from django.db.models.functions import RowNumber

#keeping it as an APIView to control how its handled
class InternalAuthorizationView(views.APIView):
    """ This ViewSet adds authorization that only allows internal users to
        return data.
    """
    django_admin_models = ["Species","SpeciesDocument",
                       "Community","CommunityDocument",
                       "ConservationStatus","ConservationStatusDocument",
                       "Occurrence", "OccurrenceReport"]
    assessor_models = ["Species","SpeciesDocument",
                       "Community","CommunityDocument",
                       "ConservationStatus","ConservationStatusDocument",
                       "Occurrence", "OccurrenceReport"]
    approver_models = ["Species","SpeciesDocument",
                       "Community","CommunityDocument",
                       "ConservationStatus","ConservationStatusDocument",
                       "Occurrence", "OccurrenceReport"]
    species_processor_models = ["Species","SpeciesDocument"]
    community_processor_models = [ "Community","CommunityDocument"]
    conservation_status_editor_models = ["ConservationStatus","ConservationStatusDocument"]

    #TODO other models to consider - Meetings, Minutes, and any Occurence Document Models

    def check_auth_by_model(self, request, model_name):
        if (request.user.is_superuser or
            is_boranga_admin(request)):
            return True
        else:
            #go through each list, if model is in it run function for user
            #return the result if true, otherwise run other checks until all possibilities exhausted
            if model_name in self.django_admin_models and is_assessor(request):
                return True
            if model_name in self.assessor_models and is_assessor(request):
                return True
            if model_name in self.approver_models and is_approver(request):
                return True
            if model_name in self.species_processor_models and is_species_processor(request):
                return True
            if model_name in self.community_processor_models and is_community_processor(request):
                return True
            if model_name in self.conservation_status_editor_models and is_conservation_status_editor(request):
                return True

            return False

    def get(self, request, model_name):
        """ Deny access to the version history for external users """
        if not is_internal(self.request) or not self.check_auth_by_model(request, model_name):
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
            qs_revision_id = all_versions.none()
            if "revision_id" in search_fields:
                qs_revision_id = all_versions
                qs_revision_id = qs_revision_id.filter(revision__id__icontains=search_value)
            
            qs_revision_date = all_versions.none()
            #revision date
            if "revision_date" in search_fields:
                qs_revision_date = all_versions
                qs_revision_date = qs_revision_date.filter(revision__date_created__icontains=search_value)

            qs_revision_data = all_versions.none()
            #otherwise, json data fields (regex?)
            if search_fields_regex:
                qs_revision_data = all_versions
                qs_revision_data = qs_revision_data.filter(serialized_data__iregex=filter_regex)

            #union resulting querysets
            all_versions = qs_revision_data.union(qs_revision_date).union(qs_revision_id)

            #get remaining revision ids, apply to main queryset for result
            try:
                remaining_revision_ids = list(set(all_versions.values_list("revision_id",flat=True)))
                queryset = queryset.filter(revision_id__in=remaining_revision_ids)
            except Exception as e:
                print(e)
                print("Invalid search term")
        
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
            elif ordering_values[i] == 'revision_sequence':
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
        super().get(request,model_name)

        model = apps.get_model(app_label=app_label, model_name=model_name)
        instance = model.objects.get(pk=int(pk))

        queryset = Version.objects.get_for_object(instance)

        id_sequence_index = list(queryset.order_by("revision_id").values_list("revision_id",flat=True))

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
                #if multiple records are of the same model, convert the dict in to a list
                if related_version.content_type.model in data:
                    if not isinstance(data[related_version.content_type.model],list):
                        data[related_version.content_type.model] = [data[related_version.content_type.model]]
                    data[related_version.content_type.model].append(related_version.data[0])
                else:
                    data[related_version.content_type.model] = related_version.data[0]

            versions_list.append({
               'revision_id': version.revision_id,
               'revision_sequence': id_sequence_index.index(version.revision_id),
               'date_created': version.revision.date_created.strftime("%Y-%m-%d %H:%M:%S"),
               'data': data,
               }
            )

        return self.paginator.get_paginated_response(list(versions_list))
    
class GetRevisionVersionsView(InternalAuthorizationView):

    def get(self, request, model_name, revision_id):
        """ Returns all versions for a revision id, oriented by a primary model

            api/history/model_name/revision_id/

            Example:

            api/history/SpeciesDocument/112/
        """
        super().get(request,model_name)

        queryset = Version.objects.filter(revision_id=revision_id).annotate(data=Cast('serialized_data', JSONField()))

        # Build the list of versions
        primary_version = queryset.filter(content_type__model__iexact=model_name)
        if primary_version.count() < 1:
            return Response()

        revision_dict = {
            'revision_id': primary_version[0].revision_id,
            'date_created': primary_version[0].revision.date_created.strftime("%Y-%m-%d %H:%M:%S"),
        }
        version_data = {}

        if primary_version.count() > 1:
            version_data[primary_version[0].content_type.model.lower()] = []
            for primary_version_sub in primary_version:
                if primary_version_sub.data:
                    data = primary_version_sub.data[0]
                    data["model_display_name"] = primary_version_sub.content_type.name
                    version_data[primary_version[0].content_type.model.lower()].append(data)
        else:
            if primary_version[0].data:
                version_data[primary_version[0].content_type.model.lower()] = primary_version[0].data[0]
                version_data[primary_version[0].content_type.model.lower()]["model_display_name"] = primary_version[0].content_type.name

        for version in queryset:
            if not version.content_type.model.lower() == model_name.lower() and version.data:
                if version.content_type.model in version_data:
                    if not isinstance(version_data[version.content_type.model],list):
                        version_data[version.content_type.model] = [version_data[version.content_type.model]]
                    version.data[0]["model_display_name"] = version.content_type.name
                    version_data[version.content_type.model].append(version.data[0])
                else:
                    version.data[0]["model_display_name"] = version.content_type.name
                    version_data[version.content_type.model] = version.data[0]

        revision_dict["version_data"] = version_data
        
        return Response(revision_dict)
