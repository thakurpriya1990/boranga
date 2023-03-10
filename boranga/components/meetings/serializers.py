import logging

from django.conf import settings
from ledger_api_client.ledger_models import EmailUserRO as EmailUser, Address
from boranga.components.meetings.models import(
        Meeting,
    )
from boranga.ledger_api_utils import retrieve_email_user
from rest_framework import serializers
from django.db.models import Q


class ListMeetingSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Meeting
        fields = (
                'id',
                'start_date',
                'end_date',
                'scientific_name',
                'location',
                'title',
                
            )
        datatables_always_serialize = (
                'id',
                'start_date',
                'end_date',
                'scientific_name',
                'location',
                'title',
            )  