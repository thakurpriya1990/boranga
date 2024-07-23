from django.contrib.gis import admin

from boranga.admin import ArchivableModelAdminMixin, DeleteProtectedModelAdmin
from boranga.components.meetings import models
from boranga.components.meetings.models import CommitteeMembers


class MeetingRoomAdmin(ArchivableModelAdminMixin, DeleteProtectedModelAdmin):
    list_display = ["id", "room_name"]


class CommitteeMembersInline(admin.TabularInline):
    model = CommitteeMembers
    extra = 0
    verbose_name = "Committee Member"
    # raw_id_fields = ('email',)


class CommitteeMembersAdmin(DeleteProtectedModelAdmin):
    list_display = ["email", "id", "first_name", "last_name", "committee"]


class CommitteeAdmin(ArchivableModelAdminMixin, DeleteProtectedModelAdmin):
    list_display = ["name", "id"]
    inlines = [CommitteeMembersInline]


admin.site.register(models.MeetingRoom, MeetingRoomAdmin)
admin.site.register(models.Committee, CommitteeAdmin)
admin.site.register(models.CommitteeMembers, CommitteeMembersAdmin)
