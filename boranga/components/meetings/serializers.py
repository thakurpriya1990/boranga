import logging

from django.conf import settings
from ledger_api_client.ledger_models import EmailUserRO as EmailUser, Address
from boranga.components.meetings.models import(
        Meeting,
        MeetingLogEntry,
	    MeetingUserAction,
        Minutes,
    )
from boranga.components.main.serializers import CommunicationLogEntrySerializer, EmailUserSerializer
from boranga.ledger_api_utils import retrieve_email_user
from rest_framework import serializers
from django.db.models import Q


class ListMeetingSerializer(serializers.ModelSerializer):
    location = serializers.SerializerMethodField()
    processing_status = serializers.CharField(source='get_processing_status_display')

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
    processing_status_display = serializers.SerializerMethodField(read_only=True)
    submitter = serializers.SerializerMethodField(read_only=True)
    start_date= serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S")
    end_date= serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S")

    class Meta:
        model = Meeting
        fields = (
                'id',
                'meeting_number',
                'start_date',
                'end_date',
                'location_id',
                'title',
                'meeting_type',
                'processing_status',
                'processing_status_display',
                'can_user_edit',
                'lodgement_date',
                'submitter',
            )
    
    def get_processing_status_display(self,obj):
        return obj.get_processing_status_display()
    
    def get_submitter(self, obj):
        if obj.submitter:
            email_user = retrieve_email_user(obj.submitter)
            return EmailUserSerializer(email_user).data
        else:
            return None


class SaveMeetingSerializer(serializers.ModelSerializer):
    location_id = serializers.IntegerField(required=False, allow_null=True, write_only= True)
    start_date = serializers.DateTimeField(required=False,allow_null=True)
    end_date = serializers.DateTimeField(required=False,allow_null=True)
    class Meta:
        model = Meeting
        fields = ('id',
                'title',
                'start_date',
                'end_date',
                'meeting_type',
			    'location_id',
                'processing_status',
				'submitter',
                'can_user_edit',
                )
        read_only_fields=('id',)

    
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


class MinutesSerializer(serializers.ModelSerializer):
	document_category_name = serializers.SerializerMethodField()
	document_sub_category_name = serializers.SerializerMethodField()
	class Meta:
		model = Minutes
		fields = (
			'id',
			'minutes_number',
			'meeting',
			'name',
			'_file',
			'description',
			'input_name',
			'uploaded_date',
			'document_category',
			'document_category_name',
			'document_sub_category',
			'document_sub_category_name',
			'visible',
		)
		read_only_fields = ('id','minutes_number')

	def get_document_category_name(self,obj):
		if obj.document_category:
			return obj.document_category.document_category_name

	def get_document_sub_category_name(self,obj):
		if obj.document_sub_category:
			return obj.document_sub_category.document_sub_category_name


class SaveMinutesSerializer(serializers.ModelSerializer):
	class Meta:
		model = Minutes
		fields = (
			'id',
			'meeting',
			'name',
			'description',
			'input_name',
			'uploaded_date',
			'document_category',
			'document_sub_category',
			)