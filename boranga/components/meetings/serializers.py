import logging

from django.conf import settings
from ledger_api_client.ledger_models import EmailUserRO as EmailUser, Address
from boranga.components.meetings.models import(
        Meeting,
        MeetingLogEntry,
	    MeetingUserAction,
    )
from boranga.components.main.serializers import CommunicationLogEntrySerializer, EmailUserSerializer
from boranga.ledger_api_utils import retrieve_email_user
from rest_framework import serializers
from django.db.models import Q


class ListMeetingSerializer(serializers.ModelSerializer):
    location = serializers.SerializerMethodField()

    class Meta:
        model = Meeting
        fields = (
                'id',
                'meeting_number',
                'start_date',
                'end_date',
                'location',
                'title',
                'processing_status',
                'can_user_edit',
            )
        datatables_always_serialize = (
                'id',
                'meeting_number',
                'start_date',
                'end_date',
                'location',
                'title',
                'processing_status',
                'can_user_edit',
            )

    def get_location(self,obj):
        if obj.location:
            return obj.location.room_name
        return ''
        
class CreateMeetingSerializer(serializers.ModelSerializer):
	class Meta:
		model = Meeting
		fields = ('id',
			    )
		read_only_fields = (
            'id',
            )


class MeetingSerializer(serializers.ModelSerializer):
    #processing_status = serializers.SerializerMethodField(read_only=True)
    start_date= serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S")
    end_date= serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S")

    class Meta:
        model = Meeting
        fields = (
                'id',
                'meeting_number',
                'start_date',
                'end_date',
                'location',
                'title',
                'meeting_type',
                'processing_status',
                'can_user_edit',
            )
        
    def get_processing_status(self,obj):
        return obj.get_processing_status_display()
    
class EditMeetingSerializer(serializers.ModelSerializer):

    class Meta:
        model = Meeting
        fields = (
                'id',
                'meeting_number',
                'start_date',
                'end_date',
                'location',
                'title',
                'meeting_type',
                'processing_status',
                'can_user_edit',
            )


class MeetingLogEntrySerializer(CommunicationLogEntrySerializer):
    documents = serializers.SerializerMethodField()
    class Meta:
        model = MeetingLogEntry
        fields = '__all__'
        read_only_fields = (
            'customer',
        )

    def get_documents(self,obj):
        return [[d.name,d._file.url] for d in obj.documents.all()]

class MeetingUserActionSerializer(serializers.ModelSerializer):
	who = serializers.SerializerMethodField()
	class Meta:
		model = MeetingUserAction
		fields = '__all__'

	def get_who(self, meeting_user_action):
		email_user = retrieve_email_user(meeting_user_action.who)
		fullname = email_user.get_full_name()
		return fullname