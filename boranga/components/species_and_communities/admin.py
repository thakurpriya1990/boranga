from django.contrib.gis import admin
from import_export.admin import ImportExportMixin
from django.db.models import Q
from boranga.components.species_and_communities.models import (
    District, 
    DocumentCategory, 
    NameAuthority, 
    Region, 
    Source, 
    ThreatCategory, 
    DocumentSubCategory,
    Family,
    PhylogeneticGroup,
    Genus,
    )


# The following allow Import/Export of large lists from file.
# class ConservationListAdmin(ImportExportMixin, admin.ModelAdmin):
#     list_display = ['code', 'label']
# admin.site.register(ConservationList, ConservationListAdmin)

# class ConservationCategoryAdmin(ImportExportMixin, admin.ModelAdmin):
#     list_display = ['code', 'label']
# admin.site.register(ConservationCategory, ConservationCategoryAdmin)

# class ConservationCriteriaAdmin(ImportExportMixin, admin.ModelAdmin):
#     list_display = ['code']
# admin.site.register(ConservationCriteria, ConservationCriteriaAdmin)

@admin.register(DocumentSubCategory)
class DocumentSubCategoryAdmin(admin.ModelAdmin):
    list_display = ['document_sub_category_name', 'document_category']

# Each of the following models will be available to Django Admin.
admin.site.register(Region)
admin.site.register(District)
admin.site.register(NameAuthority)
admin.site.register(Source)
admin.site.register(DocumentCategory)
admin.site.register(ThreatCategory)
admin.site.register(Family)
admin.site.register(PhylogeneticGroup)
admin.site.register(Genus)
