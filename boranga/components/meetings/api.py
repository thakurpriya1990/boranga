import traceback
import pytz
import json
from django.db.models import Q
from django.db import transaction
from django.core.exceptions import ValidationError
from rest_framework import viewsets, serializers, status, views
from rest_framework.decorators import action as detail_route, renderer_classes
from rest_framework.decorators import action as list_route
from rest_framework.response import Response
from rest_framework.renderers import JSONRenderer
from datetime import datetime
from ledger_api_client.settings_base import TIME_ZONE
from boranga import settings
from boranga import exceptions
from django.core.cache import cache
from django.http import HttpResponse
from django.urls import reverse
from django.shortcuts import redirect
from boranga.helpers import is_customer, is_internal
from rest_framework_datatables.pagination import DatatablesPageNumberPagination
from rest_framework_datatables.filters import DatatablesFilterBackend
from rest_framework_datatables.renderers import DatatablesRenderer
from copy import deepcopy
from django.shortcuts import render, redirect, get_object_or_404

from boranga.components.meetings.models import( 
    Meeting,
    
)

from boranga.components.meetings.serializers import(
    ListMeetingSerializer,
    MeetingSerializer,
    EditMeetingSerializer,
)


class MeetingFilterBackend(DatatablesFilterBackend):
    def filter_queryset(self, request, queryset, view):
        total_count = queryset.count()

        # filter_group_type
        filter_meeting_type = request.GET.get('meeting_status')
        if queryset.model is Meeting:
            if filter_meeting_type:
                #queryset = queryset.filter(species__group_type__name=filter_group_type)
                #changed to application_type (ie group_type)
                queryset = queryset

        filter_start_date = request.GET.get('filter_start_date')
        filter_end_date = request.GET.get('filter_end_date')
        if queryset.model is Meeting:
            if filter_start_date:
                queryset = queryset.filter(start_date=filter_start_date)

            if filter_end_date:
                queryset = queryset.filter(end_date=filter_end_date)
        
        getter = request.query_params.get
        fields = self.get_fields(getter)
        ordering = self.get_ordering(getter, fields)
        queryset = queryset.order_by(*ordering)
        if len(ordering):
            queryset = queryset.order_by(*ordering)

        try:
            queryset = super(MeetingFilterBackend, self).filter_queryset(request, queryset, view)
        except Exception as e:
            print(e)
        setattr(view, '_datatables_total_count', total_count)
        return queryset

class MeetingRenderer(DatatablesRenderer):
    def render(self, data, accepted_media_type=None, renderer_context=None):
        if 'view' in renderer_context and hasattr(renderer_context['view'], '_datatables_total_count'):
            data['recordsTotal'] = renderer_context['view']._datatables_total_count
        return super(MeetingRenderer, self).render(data, accepted_media_type, renderer_context)
    

class MeetingPaginatedViewSet(viewsets.ModelViewSet):
    filter_backends = (MeetingFilterBackend,)
    pagination_class = DatatablesPageNumberPagination
    renderer_classes = (MeetingRenderer,)
    queryset = Meeting.objects.none()
    serializer_class = ListMeetingSerializer
    page_size = 10

    def get_queryset(self):
        #request_user = self.request.user
        qs = Meeting.objects.none()

        if is_internal(self.request):
            qs = Meeting.objects.all()

        return qs
    
class MeetingViewSet(viewsets.ModelViewSet):
    queryset = Meeting.objects.all()
    serializer_class = MeetingSerializer

    def create(self, request, *args, **kwargs):
        try:
            meeting_type=request.data.get('meeting_type')
            data = {
                'meeting_type': meeting_type,                
            }
            serializer = self.get_serializer(data= request.data)
            #serializer = self.get_serializer(data=data)
            serializer.is_valid(raise_exception = True)
            instance = serializer.save()
            serializer = self.get_serializer(instance)
            return Response(serializer.data)
        except serializers.ValidationError:
            print(traceback.print_exc())
            raise
        except ValidationError as e:
            if hasattr(e,'error_dict'):
                raise serializers.ValidationError(repr(e.error_dict))
            else:
                if hasattr(e,'message'):
                    raise serializers.ValidationError(e.message)
        except Exception as e:
            print(traceback.print_exc())
            raise serializers.ValidationError(str(e))
        
    @detail_route(methods=['GET',], detail=True)
    def internal_meeting(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            serializer = self.get_serializer(instance)        
            return Response(serializer.data)
        except serializers.ValidationError:
            print(traceback.print_exc())
            raise
        except ValidationError as e:
            if hasattr(e,'error_dict'):
                    raise serializers.ValidationError(repr(e.error_dict))
            else:
                if hasattr(e,'message'):
                    raise serializers.ValidationError(e.message)
        except Exception as e:
            print(traceback.print_exc())
            raise serializers.ValidationError(str(e))
        
    @detail_route(methods=['post'], detail=True)
    def edit_meeting(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            # serializer_class = self.get_serializer()
            # serializer = serializer_class(instance,context={'request':request})
            serializer = self.get_serializer(instance)
            # serializer.is_valid(raise_exception = True)
            serializer = EditMeetingSerializer(instance, data= request.data)
            serializer.is_valid(raise_exception = True)
            serializer.save()        
            return Response(serializer.data)
        except serializers.ValidationError:
            print(traceback.print_exc())
            raise
        except ValidationError as e:
            if hasattr(e,'error_dict'):
                    raise serializers.ValidationError(repr(e.error_dict))
            else:
                if hasattr(e,'message'):
                    raise serializers.ValidationError(e.message)
        except Exception as e:
            print(traceback.print_exc())
            raise serializers.ValidationError(str(e))
        
class GetMeetingDict(views.APIView):
    
    def get(self, request, format=None):
        status_list=[]
        status_choices= Meeting.PROCESSING_STATUS_CHOICES
        for choice in status_choices:
            status_list.append({
                'id': choice[0],
                'display_name': choice[1]
            })
        res_json = {
        "status_list":status_list,
        }
        res_json = json.dumps(res_json)
        return HttpResponse(res_json, content_type='application/json')
