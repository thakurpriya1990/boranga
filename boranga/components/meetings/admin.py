from django.contrib.gis import admin
from django.db.models import Q
from boranga.components.meetings import models
from boranga.components.meetings.models import (
    MeetingRoom,
    Committee,
    CommitteeMembers,
)

@admin.register(models.MeetingRoom)
class MeetingRoomAdmin(admin.ModelAdmin):
    list_display = ['id','room_name']

class CommitteeMembersInline(admin.TabularInline):
    model = CommitteeMembers
    extra = 0
    # raw_id_fields = ('email',)

@admin.register(models.CommitteeMembers)
class CommitteeMembersAdmin(admin.ModelAdmin):
    list_display = ['email','id','first_name','last_name','committee']

@admin.register(models.Committee)
class CommitteeAdmin(admin.ModelAdmin):
    list_display = ['name','id']
    inlines = [CommitteeMembersInline]