from django.apps import apps
from rest_framework.response import Response
from rest_framework.exceptions import PermissionDenied
from rest_framework import views
from django.db import models
from reversion.models import Version
from reversion import is_registered
from rest_framework_datatables.pagination import DatatablesPageNumberPagination
from django.db.models import JSONField
from django.db.models.functions import Cast
from rest_framework_datatables.filters import DatatablesFilterBackend
from django.db.models import F
from rest_framework_datatables.utils import get_param
from boranga.helpers import (is_internal, is_customer,
is_boranga_admin, is_django_admin, is_assessor, is_approver,
is_species_processor, is_community_processor,
is_conservation_status_editor)
from django.db.models.fields.json import KeyTransform

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

class GetLookUpValues():

    lookup_fields = []
    lookup_values = {}

    def getModelLookupFields(self,model):
        """
        Get look up fields for a model

        Returns all one to many fields that are not reversion registered
        """
        #get all foreign fields of model
        #model = apps.get_model(app_label=app_label, model_name=model_name)
        lookup_fields = []
        #reversion_fields = ContentType.objects.values_list(,flat=True)
        for i in model._meta.get_fields():
            #check if field foreign
            #print(i,i.__class__)
            if isinstance(i,models.ForeignKey) and not is_registered(i.related_model):
                #check if reversion has been applied
                #if not, treat it as a lookup field
                #print(i.name)
                lookup_fields.append(i.name)
        return lookup_fields

    def getLookUpFieldValues(self,versions,model,lookup_field):
        """
        Get a set of look up field values for a given set of model instance versions

        Requires a versions queryset, the model the versions queryset pertains to, and a lookup field

        """
        field = model._meta.get_field(lookup_field)
        lookup_model = field.related_model

        instance_field_occurrences = list(set(list(versions \
        .annotate(data=Cast('serialized_data', JSONField()))\
        .annotate(lookup=KeyTransform(lookup_field, "data__0__fields")) \
        .values_list("lookup",flat=True))))

        #get queryset of the lookup_field values where the id is among the found unique instances
        lookup_values = list(lookup_model.objects.filter(pk__in=instance_field_occurrences).values())
        lookup_dict = {}
        primary_key = lookup_model._meta.pk.name
        for i in lookup_values:
            lookup_dict[i[primary_key]] = dict(i)

        return lookup_dict
    
    def getVersionModelLookUpFieldValues(self,versions,model):
        """ 
        returns a list of lookup fields, and a dictionary of fields values

        this can be used to track fields not registered by reversion to provide appropriate context

        best suited for lookup fields such as category, that are not expected to change often and/or retain their meaning even after some change
        """
        self.lookup_fields = self.getModelLookupFields(model)
        for i in self.lookup_fields:
            self.lookup_values[i] = self.getLookUpFieldValues(versions,model,i)

class GetPaginatedVersionsView(InternalAuthorizationView):
    filter_backend = VersionsFilterBackend
    paginator = DatatablesPageNumberPagination()
    #paginator.page_size = 2
    lookup_getter = GetLookUpValues()

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

        queryset_list = self.paginator.paginate_queryset(queryset, request, view=self)

        # Build the list of versions
        versions_list = []
        related_versions = Version.objects.annotate(data=Cast('serialized_data', JSONField()))

        paginated_queryset = Version.objects.filter(id__in=list(map(lambda i:i.pk,queryset_list)))
        self.lookup_getter.getVersionModelLookUpFieldValues(paginated_queryset,model)

        for version in queryset_list:
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

            #get lookup fields (for main model only)
            if model._meta.model_name in data:       
                for i in self.lookup_getter.lookup_fields:
                    if i in data[model._meta.model_name]["fields"] and data[model._meta.model_name]["fields"][i] != None:
                        data[model._meta.model_name]["fields"][i] = self.lookup_getter.lookup_values[i][data[model._meta.model_name]["fields"][i]]

            versions_list.append({
               'revision_id': version.revision_id,
               'revision_sequence': id_sequence_index.index(version.revision_id),
               'date_created': version.revision.date_created.strftime("%Y-%m-%d %H:%M:%S"),
               'data': data,
               }
            )

        return self.paginator.get_paginated_response(list(versions_list))
    
class GetRevisionVersionsView(InternalAuthorizationView):

    lookup_getter = GetLookUpValues()

    def get(self, request, app_label, model_name, revision_id):
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

        model = apps.get_model(app_label=app_label,model_name=model_name)
        self.lookup_getter.getVersionModelLookUpFieldValues(primary_version,model)

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
                    for i in self.lookup_getter.lookup_fields:
                        if i in data["fields"] and data["fields"][i] != None:
                            data["fields"][i] = self.lookup_getter.lookup_values[i][data["fields"][i]]
                    data["model_display_name"] = primary_version_sub.content_type.name
                    version_data[primary_version[0].content_type.model.lower()].append(data)
        else:
            if primary_version[0].data:
                data = primary_version[0].data[0]
                for i in self.lookup_getter.lookup_fields:
                    if i in data["fields"] and data["fields"][i] != None:
                        data["fields"][i] = self.lookup_getter.lookup_values[i][data["fields"][i]]
                version_data[primary_version[0].content_type.model.lower()] = data
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


