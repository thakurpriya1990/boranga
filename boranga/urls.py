import sys

from django import conf, urls
from django.conf import settings
from django.conf.urls import include, url
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views
from django.urls import path, re_path
from ledger_api_client.urls import urlpatterns as ledger_patterns
from rest_framework import routers

from boranga import views
from boranga.admin import admin
from boranga.components.conservation_status import api as conservation_status_api
from boranga.components.history import api as history_api
from boranga.components.main import api as main_api
from boranga.components.meetings import api as meeting_api
from boranga.components.occurrence import api as occurrence_api
from boranga.components.spatial import api as spatial_api
from boranga.components.spatial import views as spatial_views
from boranga.components.species_and_communities import api as species_communities_api
from boranga.components.users import api as users_api
from boranga.management.default_data_manager import DefaultDataManager


def are_migrations_running():
    """
    Checks whether the app was launched with the migration-specific params
    """
    # return sys.argv and ('migrate' in sys.argv or 'makemigrations' in sys.argv)
    return sys.argv and (
        "migrate" in sys.argv
        or "makemigrations" in sys.argv
        or "showmigrations" in sys.argv
        or "sqlmigrate" in sys.argv
    )


# To test sentry
def trigger_error(request):
    division_by_zero = 1 / 0  # noqa


# API patterns
router = routers.DefaultRouter()
if settings.DEBUG is not True:
    router.include_root_view = False


router.register(
    r"external_species",
    species_communities_api.ExternalSpeciesViewSet,
    "external_species",
)

router.register(
    r"external_community",
    species_communities_api.ExternalCommunityViewSet,
    "external_community",
)
router.register(r"species", species_communities_api.SpeciesViewSet, "species")
router.register(r"community", species_communities_api.CommunityViewSet, "community")
router.register(
    r"taxonomy", species_communities_api.TaxonomyViewSet
)  # not used on species_profile
router.register(
    r"community_taxonomy", species_communities_api.CommunityTaxonomyViewSet
)  # not used on community_profile
router.register(
    r"species_paginated",
    species_communities_api.SpeciesPaginatedViewSet,
    "species_paginated",
)
router.register(
    r"communities_paginated",
    species_communities_api.CommunitiesPaginatedViewSet,
    "communities_paginated",
)
router.register(r"species_documents", species_communities_api.SpeciesDocumentViewSet)
router.register(
    r"community_documents", species_communities_api.CommunityDocumentViewSet
)
router.register(r"threat", species_communities_api.ConservationThreatViewSet)
router.register(
    r"species_conservation_status_paginated",
    conservation_status_api.SpeciesConservationStatusPaginatedViewSet,
    "species_conservation_status_paginated",
)
router.register(
    r"community_conservation_status_paginated",
    conservation_status_api.CommunityConservationStatusPaginatedViewSet,
    "community_conservation_status_paginated",
)
router.register(
    r"conservation_status_paginated",
    conservation_status_api.ConservationStatusPaginatedViewSet,
    "conservation_status_paginated",
)
router.register(
    r"conservation_status_documents",
    conservation_status_api.ConservationStatusDocumentViewSet,
)
router.register(
    r"cs_referrals", conservation_status_api.ConservationStatusReferralViewSet
)
router.register(
    r"cs_amendment_request",
    conservation_status_api.ConservationStatusAmendmentRequestViewSet,
    "cs_amendment_request",
)
router.register(
    r"ocr_amendment_request",
    occurrence_api.OccurrenceReportAmendmentRequestViewSet,
    "ocr_amendment_request",
)
router.register(r"ocr_referrals", occurrence_api.OccurrenceReportReferralViewSet)
router.register(r"meeting", meeting_api.MeetingViewSet, "meeting")
router.register(
    r"meeting_paginated", meeting_api.MeetingPaginatedViewSet, "meeting_paginated"
)
router.register(r"minutes", meeting_api.MinutesViewSet)
router.register(r"committee", meeting_api.CommitteeViewSet)
router.register(r"meeting_agenda_items", meeting_api.AgendaItemViewSet)
router.register(
    r"conservation_status", conservation_status_api.ConservationStatusViewSet
)
router.register(
    r"occurrence_report", occurrence_api.OccurrenceReportViewSet, "occurrence_report"
)
router.register(
    r"occurrence_report_referrals",
    occurrence_api.OccurrenceReportReferralViewSet,
    "occurrence_report_referrals",
)
router.register(
    r"occurrence_paginated",
    occurrence_api.OccurrencePaginatedViewSet,
    "occurrence_paginated",
)
router.register(
    r"occurrence",
    occurrence_api.OccurrenceViewSet,
    "occurrence",
)
router.register(r"occurrence_documents", occurrence_api.OccurrenceDocumentViewSet)
router.register(
    r"occurrence_report_paginated",
    occurrence_api.OccurrenceReportPaginatedViewSet,
    "occurrence_report_paginated",
)
router.register(r"observer_detail", occurrence_api.ObserverDetailViewSet)
router.register(
    r"occurrence_report_documents", occurrence_api.OccurrenceReportDocumentViewSet
)
router.register(r"ocr_threat", occurrence_api.OCRConservationThreatViewSet)
router.register(r"occ_threat", occurrence_api.OCCConservationThreatViewSet)

router.register(r"users", users_api.UserViewSet)
router.register(r"global_settings", main_api.GlobalSettingsViewSet)

router.register(r"tile_layer", spatial_api.TileLayerViewSet, "tile_layer")

api_patterns = [
    url(r"^api/profile$", users_api.GetProfile.as_view(), name="get-profile"),
    url(
        r"^api/save_submitter_information$",
        users_api.SaveSubmitterInformation.as_view(),
        name="save-submitter-information",
    ),
    url(r"^api/countries$", users_api.GetCountries.as_view(), name="get-countries"),
    url(
        r"^api/submitter_categories$",
        users_api.GetSubmitterCategories.as_view(),
        name="get-submitter-categories",
    ),
    url(
        r"^api/department_users$",
        users_api.DepartmentUserList.as_view(),
        name="department-users-list",
    ),
    url(
        r"^api/filtered_users$",
        users_api.UserListFilterView.as_view(),
        name="filtered_users",
    ),
    url(r"^api/", include(router.urls)),
    url(
        r"^api/filter_lists_species",
        species_communities_api.GetSpeciesFilterDict.as_view(),
        name="get-filter_lists_species",
    ),
    url(
        r"^api/group_types_dict",
        species_communities_api.GetGroupTypeDict.as_view(),
        name="get-group-types-dict",
    ),
    url(
        r"^api/community_filter_dict",
        species_communities_api.GetCommunityFilterDict.as_view(),
        name="get-community-filter-dict",
    ),
    url(
        r"^api/region_district_filter_dict",
        species_communities_api.GetRegionDistrictFilterDict.as_view(),
        name="get-region_district_filter_dict",
    ),
    url(
        r"^api/species_profile_dict",
        species_communities_api.GetSpeciesProfileDict.as_view(),
        name="get-species-profile-dict",
    ),
    url(
        r"^api/community_profile_dict",
        species_communities_api.GetCommunityProfileDict.as_view(),
        name="get-community-profile-dict",
    ),
    url(
        r"^api/species_lookup$",
        species_communities_api.GetSpecies.as_view(),
        name="get-species",
    ),
    url(
        r"^api/communities_lookup$",
        species_communities_api.GetCommunities.as_view(),
        name="get-communities",
    ),
    url(
        r"^api/scientific_name_lookup$",
        species_communities_api.GetScientificName.as_view(),
        name="get-scientific-name",
    ),
    url(
        r"^api/scientific_name_lookup_by_groupname$",
        species_communities_api.GetScientificNameByGroup.as_view(),
        name="get-scientific-name-by-groupname",
    ),
    url(
        r"^api/common_name_lookup$",
        species_communities_api.GetCommonName.as_view(),
        name="get-common-name",
    ),
    url(
        r"^api/family_lookup$",
        species_communities_api.GetFamily.as_view(),
        name="get-family",
    ),
    url(
        r"^api/genera_lookup$",
        species_communities_api.GetGenera.as_view(),
        name="get-genera",
    ),
    url(
        r"^api/phylo_group_lookup$",
        species_communities_api.GetPhyloGroup.as_view(),
        name="get-phylo-group",
    ),
    url(
        r"^api/community_id_lookup$",
        species_communities_api.GetCommunityId.as_view(),
        name="get-community_id",
    ),
    url(
        r"^api/community_name_lookup$",
        species_communities_api.GetCommunityName.as_view(),
        name="get-community_name",
    ),
    url(
        r"^api/wild_status_lookup$",
        occurrence_api.GetWildStatus.as_view(),
        name="get-wild_status",
    ),
    url(
        r"^api/occurrence_source_lookup$",
        occurrence_api.GetOccurrenceSource.as_view(),
        name="get-occurrence_source_lookup",
    ),
    url(
        r"^api/species_display$",
        conservation_status_api.GetSpeciesDisplay.as_view(),
        name="get-cs-profile-dict",
    ),
    url(
        r"^api/community_display$",
        conservation_status_api.GetCommunityDisplay.as_view(),
        name="get-community-display",
    ),
    url(
        r"^api/cs_profile_dict$",
        conservation_status_api.GetCSProfileDict.as_view(),
        name="get-cs-profile-dict",
    ),
    url(
        r"^api/conservation_list_dict",
        conservation_status_api.GetConservationListDict.as_view(),
        name="get-conservation-list-dict",
    ),
    url(
        r"^api/proposal_amendment_request_reason_choices",
        conservation_status_api.AmendmentRequestReasonChoicesView.as_view(),
        name="amendment_request_reason_choices",
    ),
    url(
        r"^api/meeting_dict$",
        meeting_api.GetMeetingDict.as_view(),
        name="get-meeting-dict",
    ),
    url(
        r"^api/document_categories_dict$",
        species_communities_api.GetDocumentCategoriesDict.as_view(),
        name="get-document-categories-dict",
    ),
    url(
        r"^api/occ_profile_dict$",
        occurrence_api.GetOCCProfileDict.as_view(),
        name="get-occ-profile-dict",
    ),
    url(
        r"^api/history/(?P<app_label>[\w-]+)/(?P<component_name>[\w-]+)/(?P<model_name>[\w-]+)/(?P<pk>\d+)/$",
        history_api.GetPaginatedVersionsView.as_view(),
        name="get-versions",
    ),
    url(
        r"^api/history/(?P<app_label>[\w-]+)/(?P<model_name>[\w-]+)/(?P<revision_id>\d+)/$",
        history_api.GetRevisionVersionsView.as_view(),
        name="get-revision",
    ),
]

# URL Patterns
urlpatterns = [
    path(r"admin/", admin.site.urls),
    url(r"", include(api_patterns)),
    url(r"^$", views.BorangaRoutingView.as_view(), name="home"),
    url(r"^contact/", views.BorangaContactView.as_view(), name="ds_contact"),
    url(
        r"^further_info/",
        views.BorangaFurtherInformationView.as_view(),
        name="ds_further_info",
    ),
    url(r"^internal/", views.InternalView.as_view(), name="internal"),
    url(
        r"^external/species-communities$",
        views.PublicView.as_view(),
        name="species-communities",
    ),
    url(
        r"^external/species_communities/(?P<species_proposal_pk>\d+)",
        views.SpeciesView.as_view(),
        name="external-species-detail",
    ),
    url(r"^external/", views.ExternalView.as_view(), name="external"),
    url(r"^account/$", views.ExternalView.as_view(), name="manage-account"),
    url(r"^profiles/", views.ExternalView.as_view(), name="manage-profiles"),
    url(
        r"^mgt-commands/$", views.ManagementCommandsView.as_view(), name="mgt-commands"
    ),
    url(r"^private-media/", views.getPrivateFile, name="view_private_file"),
    # following url is defined so that to include url path when sending Proposal amendment request to user.
    url(
        r"^external/conservation_status/(?P<cs_proposal_pk>\d+)/$",
        views.ExternalConservationStatusView.as_view(),
        name="external-conservation-status-detail",
    ),
    url(
        r"^internal/conservation_status/(?P<cs_proposal_pk>\d+)/$",
        views.InternalConservationStatusView.as_view(),
        name="internal-conservation-status-detail",
    ),
    url(
        r"^internal/conservation-status/",
        views.InternalConservationStatusDashboardView.as_view(),
        name="internal-conservation-status-dashboard",
    ),
    url(
        r"^internal/conservation_status/(?P<cs_proposal_pk>\d+)/cs_referral/(?P<referral_pk>\d+)/$",
        views.ConservationStatusReferralView.as_view(),
        name="internal-conservation-status-referral-detail",
    ),
    url(
        r"^internal/species_communities/(?P<species_proposal_pk>\d+)/$",
        views.InternalSpeciesView.as_view(),
        name="internal-species-detail",
    ),
    url(
        r"^internal/species_communities/(?P<community_proposal_pk>\d+)/$",
        views.InternalCommunityView.as_view(),
        name="internal-community-detail",
    ),
    url(
        r"^internal/meetings/",
        views.InternalMeetingDashboardView.as_view(),
        name="internal-meeting-dashboard",
    ),
    url(
        r"^external/occurrence-report/(?P<occurrence_report_pk>\d+)/$",
        views.ExternalOccurrenceReportView.as_view(),
        name="external-occurrence-report-detail",
    ),
    url(
        r"^internal/occurrence_report/(?P<occurrence_report_pk>\d+)/$",
        views.InternalOccurrenceReportView.as_view(),
        name="internal-occurrence-report-detail",
    ),
    url(
        r"^internal/occurrence_report/(?P<occurrence_report_pk>\d+)/ocr_referral/(?P<referral_pk>\d+)/$",
        views.InternalOccurrenceReportReferralView.as_view(),
        name="internal-occurrence-report-referral-detail",
    ),
    # url(f"{settings.BASIC_AUTH_PROXY_PREFIX}(?P<request_path>.*)", spatial_views.mapProxyView),
    re_path(
        "geoproxy/(?P<request_path>[A-Za-z0-9-]+)/(?P<path>.*)",
        spatial_views.mapProxyView,
    ),
    urls.path("sentry-debug/", trigger_error),
] + ledger_patterns

if settings.DEBUG:  # Serve media locally in development.
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

    if "debug_toolbar" in settings.INSTALLED_APPS and settings.SHOW_DEBUG_TOOLBAR:
        urlpatterns += [
            # ...
            path("__debug__/", include("debug_toolbar.urls")),
        ]

# DBCA Template URLs
urlpatterns.append(
    urls.path(
        "logout/", auth_views.LogoutView.as_view(), {"next_page": "/"}, name="logout"
    )
)
if conf.settings.ENABLE_DJANGO_LOGIN:
    urlpatterns.append(
        urls.re_path(r"^ssologin/", auth_views.LoginView.as_view(), name="ssologin")
    )

if not are_migrations_running():
    DefaultDataManager()
