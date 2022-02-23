from django.contrib.gis import admin
from boranga.components.main import models

from django.contrib.admin import AdminSite
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import Group
from import_export.admin import ImportExportMixin

from django.db.models import Q

#from ledger.accounts.models import EmailUser
from ledger_api_client.ledger_models import EmailUserRO as EmailUser
from django.http import HttpResponse

from copy import deepcopy

from boranga.components.species_and_communities.models import ConservationCategory, ConservationCriteria, ConservationList, DocumentCategory, NameAuthority, RegionDistrict, Source, ThreatCategory

admin.site.index_template = 'admin-index.html'
admin.autodiscover()

class ConservationListAdmin(ImportExportMixin, admin.ModelAdmin):
    list_display = ['code', 'label']
admin.site.register(ConservationList, ConservationListAdmin)

class ConservationCategoryAdmin(ImportExportMixin, admin.ModelAdmin):
    list_display = ['code', 'label']
admin.site.register(ConservationCategory, ConservationCategoryAdmin)

class ConservationCriteriaAdmin(ImportExportMixin, admin.ModelAdmin):
    list_display = ['code']
admin.site.register(ConservationCriteria, ConservationCriteriaAdmin)

admin.site.register(RegionDistrict)
admin.site.register(NameAuthority)
admin.site.register(Source)
admin.site.register(DocumentCategory)
admin.site.register(ThreatCategory)

@admin.register(models.EmailUser)
class EmailUserAdmin(admin.ModelAdmin):
    list_display = ('email','first_name','last_name','is_staff','is_active',)
    ordering = ('email',)
    search_fields = ('id','email','first_name','last_name')

    def has_change_permission(self, request, obj=None):
        if obj is None: # and obj.status > 1:
            return True
        return None 
    def has_delete_permission(self, request, obj=None):
        return None

