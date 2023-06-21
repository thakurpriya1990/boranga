import traceback
import pytz
import json
from django.utils import timezone
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
    MeetingRoom,
    MeetingUserAction,
    Minutes,
    Committee,
    CommitteeMembers,
    AgendaItem,
)

from boranga.components.meetings.serializers import(
    ListMeetingSerializer,
    CreateMeetingSerializer,
    MeetingSerializer,
    EditMeetingSerializer,
    MeetingLogEntrySerializer,
    MeetingUserActionSerializer,
    SaveMeetingSerializer,
    MinutesSerializer,
    SaveMinutesSerializer,
    CommitteeMembersSerializer,
    ListAgendaItemSerializer,
    AgendaItemSerializer,
)

from boranga.components.conservation_status.models import ConservationStatus


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
        # import ipdb; ipdb.set_trace()
        if queryset.model is Meeting:
            if filter_start_date:
                queryset = queryset.filter(start_date__gte=filter_start_date)

            if filter_end_date:
                queryset = queryset.filter(end_date__lte=filter_end_date)

        filter_meeting_status = request.GET.get('filter_meeting_status')
        if filter_meeting_status and not filter_meeting_status.lower() == 'all':
            if queryset.model is Meeting:
                queryset = queryset.filter(processing_status=filter_meeting_status)
        
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
            serializer = CreateMeetingSerializer(data= request.data)
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
    @renderer_classes((JSONRenderer,))
    def meeting_save(self, request, *args, **kwargs):
        try:
            with transaction.atomic():
                instance = self.get_object()
                request_data = request.data
                # to resolve error for serializer submitter id as object is received in request
                if request_data['submitter']:
                    request.data['submitter'] = u'{}'.format(request_data['submitter'].get('id'))
                serializer=SaveMeetingSerializer(instance, data = request_data, partial=True)

                serializer.is_valid(raise_exception=True)
                if serializer.is_valid():
                    saved_instance = serializer.save()
                    # add the committee selected members to the meeting
                    saved_instance.selected_committee_members.set(request_data.get('sel_committee_members_arr'))

                    instance.log_user_action(MeetingUserAction.ACTION_SAVE_MEETING.format(instance.meeting_number), request)

            return redirect(reverse('internal'))

        except serializers.ValidationError:
            print(traceback.print_exc())
            raise
        except ValidationError as e:
            raise serializers.ValidationError(repr(e.error_dict))
        except Exception as e:
            print(traceback.print_exc())
            raise serializers.ValidationError(str(e))

    @detail_route(methods=['post'], detail=True)
    @renderer_classes((JSONRenderer,))
    def submit(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            instance.submit(request,self)
            instance.save()
            serializer = self.get_serializer(instance)
            return Response(serializer.data)
            # return redirect(reverse('internal'))
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
    
    # used form the meeting Queue section datatable to show the agenda items for the meeting
    @detail_route(methods=['GET',], detail=True)
    def fetch_agenda_items(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            qs = instance.agenda_items.all()
            serializer = ListAgendaItemSerializer(qs,many=True)
            return Response(serializer.data)
        except serializers.ValidationError:
            print(traceback.print_exc())
            raise
        except ValidationError as e:
            print(traceback.print_exc())
            raise serializers.ValidationError(repr(e.error_dict))
        except Exception as e:
            print(traceback.print_exc())
            raise serializers.ValidationError(str(e))
    
    # used to add the conservation status to the meeting agenda  items
    @detail_route(methods=['post'], detail=True)
    @renderer_classes((JSONRenderer,))
    def add_agenda_item(self, request, *args, **kwargs):
        try:
            with transaction.atomic():
                instance = self.get_object()
                request_data = request.data
                if request_data['conservation_status_id']:
                    cs = ConservationStatus.objects.get(id=request_data['conservation_status_id'])
                    instance.agenda_items.create(conservation_status=cs)
                agenda_items = [cs.conservation_status_id for cs in instance.agenda_items.all()]
            return Response(agenda_items)

        except serializers.ValidationError:
            print(traceback.print_exc())
            raise
        except ValidationError as e:
            raise serializers.ValidationError(repr(e.error_dict))
        except Exception as e:
            print(traceback.print_exc())
            raise serializers.ValidationError(str(e))
    
    # used to remove the conservation status from the meeting agenda  items
    @detail_route(methods=['post'], detail=True)
    @renderer_classes((JSONRenderer,))
    def remove_agenda_item(self, request, *args, **kwargs):
        try:
            with transaction.atomic():
                instance = self.get_object()
                request_data = request.data
                if request_data['conservation_status_id']:
                    cs = ConservationStatus.objects.get(id=request_data['conservation_status_id'])
                    agenda_item = AgendaItem.objects.get(meeting=instance, conservation_status=cs)
                    agenda_item.delete()
                agenda_items = [cs.conservation_status_id for cs in instance.agenda_items.all()]
            return Response(agenda_items)

        except serializers.ValidationError:
            print(traceback.print_exc())
            raise
        except ValidationError as e:
            raise serializers.ValidationError(repr(e.error_dict))
        except Exception as e:
            print(traceback.print_exc())
            raise serializers.ValidationError(str(e))
    
    @detail_route(methods=['GET',], detail=True)
    def minutes(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            qs = instance.meeting_minutes.all()
            qs = qs.order_by('-uploaded_date')
            serializer = MinutesSerializer(qs,many=True, context={'request':request})
            return Response(serializer.data)
        except serializers.ValidationError:
            print(traceback.print_exc())
            raise
        except ValidationError as e:
            print(traceback.print_exc())
            raise serializers.ValidationError(repr(e.error_dict))
        except Exception as e:
            print(traceback.print_exc())
            raise serializers.ValidationError(str(e))
    
    @detail_route(methods=['GET',], detail=True)
    def comms_log(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            qs = instance.comms_logs.all()
            serializer = MeetingLogEntrySerializer(qs,many=True)
            return Response(serializer.data)
        except serializers.ValidationError:
            print(traceback.print_exc())
            raise
        except ValidationError as e:
            print(traceback.print_exc())
            raise serializers.ValidationError(repr(e.error_dict))
        except Exception as e:
            print(traceback.print_exc())
            raise serializers.ValidationError(str(e))

    @detail_route(methods=['POST',], detail=True)
    @renderer_classes((JSONRenderer,))
    def add_comms_log(self, request, *args, **kwargs):
        try:
            with transaction.atomic():
                instance = self.get_object()
                mutable=request.data._mutable
                request.data._mutable=True
                request.data['meeting'] = u'{}'.format(instance.id)
                request.data['staff'] = u'{}'.format(request.user.id)
                request.data._mutable=mutable
                serializer = MeetingLogEntrySerializer(data=request.data)
                serializer.is_valid(raise_exception=True)
                comms = serializer.save()
                # Save the files
                for f in request.FILES:
                    document = comms.documents.create()
                    document.name = str(request.FILES[f])
                    document._file = request.FILES[f]
                    document.save()
                # End Save Documents

                return Response(serializer.data)
        except serializers.ValidationError:
            print(traceback.print_exc())
            raise
        except ValidationError as e:
            print(traceback.print_exc())
            raise serializers.ValidationError(repr(e.error_dict))
        except Exception as e:
            print(traceback.print_exc())
            raise serializers.ValidationError(str(e))

    @detail_route(methods=['GET',], detail=True)
    def action_log(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            qs = instance.action_logs.all()
            serializer = MeetingUserActionSerializer(qs,many=True)
            return Response(serializer.data)
        except serializers.ValidationError:
            print(traceback.print_exc())
            raise
        except ValidationError as e:
            print(traceback.print_exc())
            raise serializers.ValidationError(repr(e.error_dict))
        except Exception as e:
            print(traceback.print_exc())
            raise serializers.ValidationError(str(e))


class GetMeetingDict(views.APIView):
    
    def get(self, request, format=None):
        location_list = []
        locations = MeetingRoom.objects.all()
        if locations:
            for option in locations:
                location_list.append({'id': option.id,
                    'name':option.room_name,
                    });
        meeting_type_list = []
        meeting_type_choices= Meeting.MEETING_TYPE_CHOICES
        for choice in meeting_type_choices:
            meeting_type_list.append({
                'id': choice[0],
                'display_name': choice[1]
            })
        status_list = []
        status_choices= Meeting.PROCESSING_STATUS_CHOICES
        for choice in status_choices:
            status_list.append({
                'id': choice[0],
                'display_name': choice[1]
            })
        committee_list = []
        committees= Committee.objects.all()
        for option in committees:
            committee_list.append({
                'id': option.id,
                'name': option.name
            })
        res_json = {
        "location_list":location_list,
        "meeting_type_list":meeting_type_list,
        "status_list":status_list,
        "committee_list":committee_list,
        }
        res_json = json.dumps(res_json)
        return HttpResponse(res_json, content_type='application/json')


class MinutesViewSet(viewsets.ModelViewSet):
    queryset = Minutes.objects.all().order_by('id')
    serializer_class = MinutesSerializer

    @detail_route(methods=['GET',], detail=True)
    def discard(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            instance.visible = False
            instance.save()
            instance.meeting.log_user_action(MeetingUserAction.ACTION_DISCARD_MINUTE.format(instance.minutes_number,instance.meeting.meeting_number),request)
            serializer = self.get_serializer(instance)
            return Response(serializer.data)
        except serializers.ValidationError:
            print(traceback.print_exc())
            raise
        except ValidationError as e:
            print(traceback.print_exc())
            raise serializers.ValidationError(repr(e.error_dict))
        except Exception as e:
            print(traceback.print_exc())
            raise serializers.ValidationError(str(e))

    @detail_route(methods=['GET',], detail=True)
    def reinstate(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            instance.visible = True
            instance.save()
            serializer = self.get_serializer(instance)
            instance.meeting.log_user_action(MeetingUserAction.ACTION_REINSTATE_MINUTE.format(instance.minutes_number,instance.meeting.meeting_number),request)
            return Response(serializer.data)
        except serializers.ValidationError:
            print(traceback.print_exc())
            raise
        except ValidationError as e:
            print(traceback.print_exc())
            raise serializers.ValidationError(repr(e.error_dict))
        except Exception as e:
            print(traceback.print_exc())
            raise serializers.ValidationError(str(e))

    def update(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            serializer = SaveMinutesSerializer(instance, data=json.loads(request.data.get('data')))
            serializer.is_valid(raise_exception=True)
            serializer.save()
            instance.add_minutes_documents(request)
            instance.meeting.log_user_action(MeetingUserAction.ACTION_UPDATE_MINUTE.format(instance.minutes_number,instance.meeting.meeting_number),request)
            return Response(serializer.data)
        except Exception as e:
            print(traceback.print_exc())
            raise serializers.ValidationError(str(e))


    def create(self, request, *args, **kwargs):
        try:
            serializer = SaveMinutesSerializer(data= json.loads(request.data.get('data')))
            serializer.is_valid(raise_exception = True)
            instance = serializer.save()
            instance.add_minutes_documents(request)
            instance.meeting.log_user_action(MeetingUserAction.ACTION_ADD_MINUTE.format(instance.minutes_number,instance.meeting.meeting_number),request)
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


class CommitteeViewSet(viewsets.ModelViewSet):
    queryset = Committee.objects.all()
    serializer_class = None
    
    @detail_route(methods=['GET',], detail=True)
    def committee_members(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            qs = instance.members.all()
            qs = qs.order_by('-first_name')
            serializer = CommitteeMembersSerializer(qs,many=True, context={'request':request})
            return Response(serializer.data)
        except serializers.ValidationError:
            print(traceback.print_exc())
            raise
        except ValidationError as e:
            print(traceback.print_exc())
            raise serializers.ValidationError(repr(e.error_dict))
        except Exception as e:
            print(traceback.print_exc())
            raise serializers.ValidationError(str(e))


class AgendaItemViewSet(viewsets.ModelViewSet):
    #queryset = ProposalRequirement.objects.all()
    queryset = AgendaItem.objects.none()
    serializer_class = AgendaItemSerializer

    def get_queryset(self):
        qs = AgendaItem.objects.all()
        return qs

    @detail_route(methods=['GET',], detail=True)
    def move_up(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            instance.up()
            instance.save()
            serializer = self.get_serializer(instance)
            return Response(serializer.data)
        except serializers.ValidationError:
            print(traceback.print_exc())
            raise
        except ValidationError as e:
            print(traceback.print_exc())
            raise serializers.ValidationError(repr(e.error_dict))
        except Exception as e:
            print(traceback.print_exc())
            raise serializers.ValidationError(str(e))

    @detail_route(methods=['GET',], detail=True)
    def move_down(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            instance.down()
            instance.save()
            serializer = self.get_serializer(instance)
            return Response(serializer.data)
        except serializers.ValidationError:
            print(traceback.print_exc())
            raise
        except ValidationError as e:
            print(traceback.print_exc())
            raise serializers.ValidationError(repr(e.error_dict))
        except Exception as e:
            print(traceback.print_exc())
            raise serializers.ValidationError(str(e))
