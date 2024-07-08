from django.contrib.gis import admin

from boranga.admin import DeleteProtectedModelAdmin
from boranga.components.species_and_communities.models import (
    ClassificationSystem,
    CurrentImpact,
    District,
    DocumentCategory,
    DocumentSubCategory,
    FloraRecruitmentType,
    GroupType,
    InformalGroup,
    Kingdom,
    PostFireHabitatInteraction,
    PotentialImpact,
    PotentialThreatOnset,
    Region,
    RootMorphology,
    Species,
    Taxonomy,
    TaxonomyRank,
    TaxonPreviousName,
    TaxonVernacular,
    ThreatAgent,
    ThreatCategory,
)


@admin.register(DocumentSubCategory)
class DocumentSubCategoryAdmin(DeleteProtectedModelAdmin):
    list_display = ["document_sub_category_name", "document_category"]


# Each of the following models will be available to Django Admin.
admin.site.register(GroupType)
admin.site.register(Region)
admin.site.register(District)
admin.site.register(DocumentCategory, DeleteProtectedModelAdmin)
admin.site.register(ThreatCategory, DeleteProtectedModelAdmin)
admin.site.register(FloraRecruitmentType, DeleteProtectedModelAdmin)
admin.site.register(RootMorphology, DeleteProtectedModelAdmin)
admin.site.register(PostFireHabitatInteraction, DeleteProtectedModelAdmin)
admin.site.register(CurrentImpact, DeleteProtectedModelAdmin)
admin.site.register(PotentialImpact, DeleteProtectedModelAdmin)
admin.site.register(PotentialThreatOnset, DeleteProtectedModelAdmin)
admin.site.register(ThreatAgent, DeleteProtectedModelAdmin)


@admin.register(Kingdom)
class KingdomAdmin(admin.ModelAdmin):
    list_display = ["id", "kingdom_id", "kingdom_name", "grouptype"]
    readonly_fields = ("kingdom_id", "kingdom_name")

    def has_delete_permission(self, request, obj=None):
        return False

    def has_add_permission(self, request):
        return False


class TaxonVernacularInline(admin.TabularInline):
    model = TaxonVernacular
    list_display = ("id", "vernacular_id", "vernacular_name")
    ordering = ("-id",)
    extra = 0

    def has_add_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False


class TaxonPreviousNameInline(admin.TabularInline):
    model = TaxonPreviousName
    list_display = ("id", "previous_name_id", "previous_scientific_name")
    ordering = ("-id",)
    extra = 0

    def has_add_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False


class InformalGroupInline(admin.TabularInline):
    model = InformalGroup
    list_display = ("id", "classification_system_id", "classification_system_fk")
    ordering = ("-id",)
    extra = 0

    def has_add_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False


@admin.register(Taxonomy)
class TaxonomyAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "taxon_name_id",
        "scientific_name",
        "kingdom_name",
        "grouptype__name",
    )
    list_filter = ["kingdom_fk__kingdom_name", "kingdom_fk__grouptype__name"]
    inlines = [TaxonVernacularInline, TaxonPreviousNameInline, InformalGroupInline]
    search_fields = ("taxon_name_id", "scientific_name")
    actions = None

    def get_readonly_fields(self, request, obj=None):
        return [f.name for f in obj._meta.fields]

    def has_delete_permission(self, request, obj=None):
        return False

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None, **kwargs):
        return False

    def grouptype__name(self, obj):
        if obj.kingdom_fk.grouptype is None:
            return ""
        else:
            return obj.kingdom_fk.grouptype.name


@admin.register(TaxonomyRank)
class TaxonomyRankAdmin(admin.ModelAdmin):
    list_display = ["id", "taxon_rank_id", "rank_name", "kingdom_fk"]
    actions = None

    def get_readonly_fields(self, request, obj=None):
        return [f.name for f in obj._meta.fields]

    def has_delete_permission(self, request, obj=None):
        return False

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None, **kwargs):
        return False


@admin.register(ClassificationSystem)
class ClassificationSystemAdmin(admin.ModelAdmin):
    list_display = ["id", "classification_system_id", "class_desc"]
    actions = None

    def get_readonly_fields(self, request, obj=None):
        return [f.name for f in obj._meta.fields]

    def has_delete_permission(self, request, obj=None):
        return False

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None, **kwargs):
        return False


@admin.register(Species)
class SpeciesAdmin(admin.ModelAdmin):
    list_display = [
        "id",
        "species_number",
        "group_type",
        "taxonomy",
        "processing_status",
    ]
    actions = None

    def get_readonly_fields(self, request, obj=None):
        return [f.name for f in obj._meta.fields]

    def has_delete_permission(self, request, obj=None):
        return False

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None, **kwargs):
        return False
