from django.contrib.gis import admin

from boranga.components.conservation_status import models


@admin.register(models.ProposalAmendmentReason)
class ProposalAmendmentReasonAdmin(admin.ModelAdmin):
    list_display = ["reason"]


class AbstractListAdmin(admin.ModelAdmin):
    list_display = ["code", "label"]


class WAPriorityListAdmin(AbstractListAdmin):
    pass


class WAPriorityCategoryAdmin(AbstractListAdmin):
    filter_horizontal = ("wa_priority_lists",)


class WALegislativeListAdmin(AbstractListAdmin):
    pass


class WALegislativeCategoryAdmin(AbstractListAdmin):
    filter_horizontal = ("wa_legislative_lists",)


class CommonwealthConservationListAdmin(AbstractListAdmin):
    pass


class ConservationChangeCodeAdmin(admin.ModelAdmin):
    list_display = ["code", "label"]


admin.site.register(models.WAPriorityList, WAPriorityListAdmin)
admin.site.register(models.WAPriorityCategory, WAPriorityCategoryAdmin)
admin.site.register(models.WALegislativeList, WALegislativeListAdmin)
admin.site.register(models.WALegislativeCategory, WALegislativeCategoryAdmin)
admin.site.register(
    models.CommonwealthConservationList, CommonwealthConservationListAdmin
)
admin.site.register(models.ConservationChangeCode, ConservationChangeCodeAdmin)
