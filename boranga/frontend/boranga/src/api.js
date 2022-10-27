var site_url = location.origin
var t_class='Commercial operations'
var filming='Filming'
var event='Event'
var flora='flora'
var fauna='fauna'
var community='community'

module.exports = {
    organisations: '/api/organisations.json',
    filtered_organisations: '/api/filtered_organisations',
    organisation_requests: '/api/organisation_requests.json',
    organisation_contacts: '/api/organisation_contacts.json',
    organisation_access_group_members: '/api/organisation_access_group_members',
    users_api: '/api/users',
    users: '/api/users.json',
    profile: '/api/profile',
    department_users: '/api/department_users',
    filtered_users: '/api/filtered_users',
    referral_recipient_groups: '/api/referrals/user_group_list',
    //other
    //countries: "https://restcountries.eu/rest/v1/?fullText=true",
    countries: '/api/countries',
    proposal_type:"/api/proposal_type",
    species:"/api/species",
    community:"/api/community",
    conservation_status:"/api/conservation_status",
    cs_referrals:"/api/cs_referrals.json",
    /*species_conservation_status:"/api/species_conservation_status",
    community_conservation_status:"/api/community_conservation_status",*/
    document_categories: "/api/document_categories.json",
    document_sub_categories: "/api/document_sub_categories.json",
    species_documents:"/api/species_documents.json",
    community_documents:"/api/community_documents.json",
    threat:"/api/threat.json",
    threat_categories: "/api/threat_categories.json",
    current_impact: "/api/current_impact.json",
    potential_impact: "/api/potential_impact.json",
    potential_threat_onset: "/api/potential_threat_onset.json",
    proposals:"/api/proposal.json",
    proposal_park:"/api/proposal_park.json",
    proposal_submit:"/api/proposal_submit.json",
    //list_proposals:"/api/proposal/list_proposal.json",
    approvals:"/api/approvals.json",
    referrals:"/api/referrals.json",
    compliances:"/api/compliances.json",
    proposal_standard_requirements:"/api/proposal_standard_requirements.json",
    proposal_requirements:"/api/proposal_requirements.json",
    amendment_request:"/api/amendment_request.json",
    regions:"/api/regions.json",
    park_treeview:"/api/park_treeview",
    marine_treeview:"/api/marine_treeview",
    tclass_container_land:"/api/tclass_container_land",
    tclass_container_marine:"/api/tclass_container_marine",
    activity_matrix:"/api/activity_matrix.json",
    application_types:"/api/application_types.json",
    access_types:"/api/access_types.json",
    parks:"/api/parks.json",
    trails:"/api/trails.json",
    districts:"/api/districts.json",
    vehicles:"/api/vehicles.json",
    vessels:"/api/vessels.json",
    assessments:"/api/assessments.json",
    event_trail_container:"/api/event_trail_container",
    event_park_container:"/api/event_park_container",
    overdue_invoices:"/api/overdue_invoices.json",
    
    //filming
    proposal_filming_parks:"/api/proposal_filming_parks.json",
    district_proposals:"/api/district_proposals.json",

    //Events
    proposal_events_parks:"/api/proposal_events_parks.json",
    abseiling_climbing_activities:"/api/abseiling_climbing_activities.json",
    proposal_pre_event_parks:"/api/proposal_pre_event_parks.json",
    proposal_events_trails:"/api/proposal_events_trails.json",

    // used in internal and external dashboards
    proposals_paginated_external:   "/api/proposal_paginated/proposals_external/?format=datatables",
    approvals_paginated_external:   "/api/approval_paginated/approvals_external/?format=datatables",
    compliances_paginated_external: "/api/compliance_paginated/compliances_external/?format=datatables",
    proposals_paginated_internal:   "/api/proposal_paginated/proposals_internal/?format=datatables",
    referrals_paginated_internal:   "/api/proposal_paginated/referrals_internal/?format=datatables",
    species_paginated_internal: "/api/species_paginated/species_internal/?format=datatables",
    communities_paginated_internal: "/api/communities_paginated/communities_internal/?format=datatables",
    species_conservation_status_paginated_internal: "/api/species_conservation_status_paginated/species_cs_internal/?format=datatables",
    species_conservation_status_referrals_paginated_internal: "/api/species_conservation_status_paginated/species_cs_referrals_internal/?format=datatables",
    community_conservation_status_paginated_internal: "/api/community_conservation_status_paginated/community_cs_internal/?format=datatables",
    community_conservation_status_referrals_paginated_internal: "/api/community_conservation_status_paginated/community_cs_referrals_internal/?format=datatables",
    conservation_status_paginated_external: "/api/conservation_status_paginated/conservation_status_external?format=datatables",
    filter_lists_species:"/api/filter_lists_species",
    group_types_dict:"/api/group_types_dict",
    community_filter_dict:"/api/community_filter_dict",
    region_district_filter_dict:"/api/region_district_filter_dict",
    scientific_name_lookup:"/api/scientific_name_lookup",

    //conservation Status profile page list of value dict
    cs_profile_dict:"/api/cs_profile_dict",
    conservation_list_dict:"/api/conservation_list_dict",

    //filter_list:                    "/api/proposal_paginated/filter_list.json",
    filter_list:                    "/api/proposal/filter_list.json",
    filter_list_approvals:          "/api/approvals/filter_list.json",
    filter_list_compliances:        "/api/compliances/filter_list.json",
    filter_list_referrals:          "/api/referrals/filter_list.json",
    filter_list_parks:              "/api/parks/filter_list.json",
    filter_list_district_proposals:  "/api/district_proposals/filter_list.json",

    filter_list_cs_referrals:         "/api/cs_referrals/filter_list.json",
    filter_list_cs_referrals_community:"/api/cs_referrals/community_filter_list.json",

    //approvals_paginated:"/api/approvals/user_list_paginated/?format=datatables",
    //compliances_paginated:"/api/compliances/user_list_paginated/?format=datatables",
    //list_proposals:"/api/list_proposal/?format=datatables",
    //list_referrals:"/api/list_proposal/referral_list/?format=datatables",

    discard_cs_proposal:function (id) {
      return `/api/conservation_status/${id}.json`;
    },
    discard_proposal:function (id) {
      return `/api/proposal/${id}.json`;
    },
    discard_vessel:function (id) {
      return `/api/vessels/${id}.json`;
    },
    discard_vehicle:function (id) {
      return `/api/vehicles/${id}.json`;
    },
    discard_abseiling_climbing:function (id) {
      return `/api/abseiling_climbing_activities/${id}.json`;
    },
    discard_pre_event_park:function (id) {
      return `/api/proposal_pre_event_parks/${id}.json`;
    },
    discard_event_park:function (id) {
      return `/api/proposal_events_parks/${id}.json`;
    },
    discard_event_trail:function (id) {
      return `/api/proposal_events_trails/${id}.json`;
    },
    discard_filming_park:function (id) {
      return `/api/proposal_filming_parks/${id}.json`;
    },
    site_url: site_url,
    //dep_name: 'Department of Biodiversity, Conservation and Attractions',
    //dep_name_short: 'DBCA',
    system_name: 'Boranga System',
    //system_name_short: 'DAS',
    payment_help_url: 'https://parks.dpaw.wa.gov.au/for-business/training-accreditation-insurance-fees',
    proposal_type_help_url: ' https://parks.dbca.wa.gov.au/for-business/commercial-operations-licensing',
    t_class: t_class,
    filming: filming,
    event: event,
    group_types:['Fauna', 'Flora', 'Communities']
}
