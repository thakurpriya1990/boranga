var site_url = location.origin
var t_class = 'Commercial operations'
var filming = 'Filming'
var event = 'Event'
var group_type_flora = 'flora'
var group_type_fauna = 'fauna'
var group_type_community = 'community'

module.exports = {
    access_types: "/api/access_types.json",
    activity_matrix: "/api/activity_matrix.json",
    amendment_request: "/api/amendment_request.json",
    application_types: "/api/application_types.json",
    approvals: "/api/approvals.json",
    assessments: "/api/assessments.json",
    community_documents: "/api/community_documents.json",
    community_taxonomy: "/api/community_taxonomy",
    community: "/api/community",
    compliances: "/api/compliances.json",
    conservation_status_documents: "/api/conservation_status_documents.json",
    conservation_status: "/api/conservation_status",
    countries: '/api/countries',
    cs_referrals: "/api/cs_referrals.json",
    department_users: '/api/department_users',
    districts: "/api/districts.json",
    document_categories_dict: "/api/document_categories_dict",
    event_park_container: "/api/event_park_container",
    event_trail_container: "/api/event_trail_container",
    filtered_organisations: '/api/filtered_organisations',
    filtered_users: '/api/filtered_users',
    marine_treeview: "/api/marine_treeview",
    organisation_access_group_members: '/api/organisation_access_group_members',
    organisation_contacts: '/api/organisation_contacts.json',
    organisation_requests: '/api/organisation_requests.json',
    organisations: '/api/organisations.json',
    overdue_invoices: "/api/overdue_invoices.json",
    park_treeview: "/api/park_treeview",
    parks: "/api/parks.json",
    profile: '/api/profile',
    proposal_park: "/api/proposal_park.json",
    proposal_requirements: "/api/proposal_requirements.json",
    proposal_standard_requirements: "/api/proposal_standard_requirements.json",
    proposal_submit: "/api/proposal_submit.json",
    proposal_type: "/api/proposal_type",
    proposals: "/api/proposal.json",
    referral_recipient_groups: '/api/referrals/user_group_list',
    referrals: "/api/referrals.json",
    regions: "/api/regions.json",
    species_documents: "/api/species_documents.json",
    species: "/api/species",
    taxonomy: "/api/taxonomy",
    tclass_container_land: "/api/tclass_container_land",
    tclass_container_marine: "/api/tclass_container_marine",
    threat: "/api/threat.json",
    trails: "/api/trails.json",
    users_api: '/api/users',
    users: '/api/users.json',
    vehicles: "/api/vehicles.json",
    vessels: "/api/vessels.json",

    //filming
    proposal_filming_parks: "/api/proposal_filming_parks.json",
    district_proposals: "/api/district_proposals.json",

    //Events
    proposal_events_parks: "/api/proposal_events_parks.json",
    abseiling_climbing_activities: "/api/abseiling_climbing_activities.json",
    proposal_pre_event_parks: "/api/proposal_pre_event_parks.json",
    proposal_events_trails: "/api/proposal_events_trails.json",

    // used in internal and external dashboards
    approvals_paginated_external: "/api/approval_paginated/approvals_external/?format=datatables",
    common_name_lookup: "/api/common_name_lookup",
    communities_internal_export: "/api/communities_paginated/communities_internal_export",
    communities_lookup: "/api/communities_lookup",
    communities_paginated_internal: "/api/communities_paginated/communities_internal/?format=datatables",
    community_agenda_conservation_status_paginated_internal: "/api/community_conservation_status_paginated/agenda_cs_internal/?format=datatables",
    community_conservation_plans_paginated_internal: "/api/community_conservation_plans_paginated/community_cp_internal/?format=datatables",
    community_conservation_status_paginated_internal: "/api/community_conservation_status_paginated/community_cs_internal/?format=datatables",
    community_conservation_status_referrals_paginated_internal: "/api/community_conservation_status_paginated/community_cs_referrals_internal/?format=datatables",
    community_cs_internal_export: "/api/community_conservation_status_paginated/community_cs_internal_export",
    community_cs_referrals_internal_export: "/api/community_conservation_status_paginated/community_cs_referrals_internal_export",
    community_filter_dict: "/api/community_filter_dict",
    community_id_lookup: "/api/community_id_lookup",
    community_name_lookup: "/api/community_name_lookup",
    compliances_paginated_external: "/api/compliance_paginated/compliances_external/?format=datatables",
    conservation_status_paginated_external: "/api/conservation_status_paginated/conservation_status_external?format=datatables",
    family_lookup: "/api/family_lookup",
    filter_lists_species: "/api/filter_lists_species",
    genera_lookup: "/api/genera_lookup",
    group_types_dict: "/api/group_types_dict",
    meeting_agenda_items: "/api/meeting_agenda_items.json",
    meetings_paginated: "/api/meeting_paginated/?format=datatables",
    occurrence_lookup: "/api/occurrence_paginated/occurrence_lookup",
    occurrence_internal_export: "/api/occurrence_paginated/occurrence_internal_export",
    occurrence_paginated_internal: "/api/occurrence_paginated/occurrence_internal?format=datatables",
    occurrence_report_external_export: "/api/occurrence_report_paginated/occurrence_report_external_export",
    occurrence_report_internal_export: "/api/occurrence_report_paginated/occurrence_report_internal_export",
    community_occurrence_report_internal_export: "/api/occurrence_report_paginated/community_occurrence_report_internal_export",
    occurrence_report_paginated_external: "/api/occurrence_report_paginated/occurrence_report_external?format=datatables",
    occurrence_report_paginated_internal: "/api/occurrence_report_paginated/occurrence_report_internal?format=datatables",
    occurrence: "/api/occurrence_paginated/",
    phylo_group_lookup: "/api/phylo_group_lookup",
    proposals_paginated_external: "/api/proposal_paginated/proposals_external/?format=datatables",
    proposals_paginated_internal: "/api/proposal_paginated/proposals_internal/?format=datatables",
    referrals_paginated_internal: "/api/proposal_paginated/referrals_internal/?format=datatables",
    region_district_filter_dict: "/api/region_district_filter_dict",
    scientific_name_lookup_by_groupname: "/api/scientific_name_lookup_by_groupname",
    scientific_name_lookup: "/api/scientific_name_lookup",
    species_agenda_conservation_status_paginated_internal: "/api/species_conservation_status_paginated/agenda_cs_internal/?format=datatables",
    species_conservation_plans_paginated_internal: "/api/species_conservation_plans_paginated/species_cp_internal/?format=datatables",
    species_conservation_status_paginated_internal: "/api/species_conservation_status_paginated/species_cs_internal/?format=datatables",
    meeting_export: "/api/meeting_paginated/meeting_export",
    species_conservation_status_referrals_paginated_internal: "/api/species_conservation_status_paginated/species_cs_referrals_internal/?format=datatables",
    species_cs_internal_export: "/api/species_conservation_status_paginated/species_cs_internal_export",
    species_cs_referrals_internal_export: "/api/species_conservation_status_paginated/species_cs_referrals_internal_export",
    species_internal_export: "/api/species_paginated/species_internal_export",
    species_lookup: "/api/species_lookup",
    species_paginated_internal: "/api/species_paginated/species_internal/?format=datatables",

    // Pending - need to create viewsets for the below when working on search filters for OR dashboard
    or_status_lookup: "/api/or_status_lookup",
    or_submitted_from_lookup: "/api/or_submitted_from_lookup",

    //conservation Status profile page list of value dict
    cs_profile_dict: "/api/cs_profile_dict",
    conservation_list_dict: "/api/conservation_list_dict",

    filter_list: "/api/proposal/filter_list.json",
    filter_list_approvals: "/api/approvals/filter_list.json",
    filter_list_compliances: "/api/compliances/filter_list.json",
    filter_list_referrals: "/api/referrals/filter_list.json",
    filter_list_parks: "/api/parks/filter_list.json",
    filter_list_district_proposals: "/api/district_proposals/filter_list.json",

    filter_list_cs_referrals: "/api/cs_referrals/filter_list.json",
    filter_list_cs_referrals_community: "/api/cs_referrals/community_filter_list.json",

    meeting: "/api/meeting",
    meeting_dict: "/api/meeting_dict",
    minutes: "/api/minutes.json",
    committee: "/api/committee",

    occurrence_report: "/api/occurrence_report",
    observer_detail: "/api/observer_detail.json",
    occurrence_report_documents: "/api/occurrence_report_documents.json",
    ocr_threat: "/api/ocr_threat.json",

    discard_cs_proposal: function (id) {
        return `/api/conservation_status/${id}.json`;
    },
    discard_community_proposal: function (id) {
        return `/api/community/${id}.json`;
    },
    discard_species_proposal: function (id) {
        return `/api/species/${id}.json`;
    },
    discard_meeting: function (id) {
        return `/api/meeting/${id}.json`;
    },
    discard_ocr_proposal: function (id) {
        return `/api/occurrence_report/${id}.json`;
    },
    discard_observer_detail: function (id) {
        return `/api/observer_detail/${id}.json`;
    },
    discard_vessel: function (id) {
        return `/api/vessels/${id}.json`;
    },
    discard_vehicle: function (id) {
        return `/api/vehicles/${id}.json`;
    },
    discard_abseiling_climbing: function (id) {
        return `/api/abseiling_climbing_activities/${id}.json`;
    },
    discard_pre_event_park: function (id) {
        return `/api/proposal_pre_event_parks/${id}.json`;
    },
    discard_event_park: function (id) {
        return `/api/proposal_events_parks/${id}.json`;
    },
    discard_event_trail: function (id) {
        return `/api/proposal_events_trails/${id}.json`;
    },
    discard_filming_park: function (id) {
        return `/api/proposal_filming_parks/${id}.json`;
    },

    lookup_history_species_document: function (id) {
      return `/api/history/boranga/species_communities/SpeciesDocument/${id}/`;
    },
    lookup_history_species: function (id) {
      return `/api/history/boranga/species_communities/Species/${id}/`;
    },
    lookup_history_community_document: function (id) {
      return `/api/history/boranga/species_communities/CommunityDocument/${id}/`;
    },
    lookup_history_community: function (id) {
      return `/api/history/boranga/species_communities/Community/${id}/`;
    },

    lookup_history_conservation_status_document: function (id) {
      return `/api/history/boranga/conservation_status/ConservationStatusDocument/${id}/`;
    },
    lookup_history_conservation_status: function (id) {
      return `/api/history/boranga/conservation_status/ConservationStatus/${id}/`;
    },

    lookup_history_occurrence_report_document: function (id) {
      return `/api/history/boranga/occurrence/OccurrenceReportDocument/${id}/`;
    },
    lookup_history_occurrence_report: function (id) {
      return `/api/history/boranga/occurrence/OccurrenceReport/${id}/`;
    },

    lookup_history_occurrence: function (id) {
      return `/api/history/boranga/occurrence/Occurrence/${id}/`;
    },

    lookup_history_conservation_threat: function (id) {
      return `/api/history/boranga/species_communities/ConservationThreat/${id}/`;
    },

    lookup_history_ocr_conservation_threat: function (id) {
      return `/api/history/boranga/occurrence/OcrConservationThreat/${id}/`;
    },

    lookup_history_minutes: function (id) {
      return `/api/history/boranga/meeting/Minutes/${id}/`;
    },

    lookup_revision_versions: function (model,id) {
      return `/api/history/boranga/${model}/${id}/`;
    },

    event: event,
    filming: filming,
    group_type_community: group_type_community,
    group_type_fauna: group_type_fauna,
    group_type_flora: group_type_flora,
    group_types: ['Fauna', 'Flora', 'Communities'],
    payment_help_url: 'https://parks.dpaw.wa.gov.au/for-business/training-accreditation-insurance-fees',
    proposal_type_help_url: ' https://parks.dbca.wa.gov.au/for-business/commercial-operations-licensing',
    site_url: site_url,
    system_name: 'Boranga System',
    t_class: t_class,
}
