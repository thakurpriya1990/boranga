from django.contrib.gis import admin
from django.db.models import Q
from boranga.components.meetings import models
from boranga.components.meetings.models import (
    MeetingRoom,
)

@admin.register(models.MeetingRoom)
class MeetingRoomAdmin(admin.ModelAdmin):
    list_display = ['id','room_name']