var site_url = location.origin
var t_class='Commercial operations'
var filming='Filming'
var event='Event'

module.exports = {
    organisations: '/api/organisations.json',
    filtered_organisations: '/api/filtered_organisations',
    organisation_requests: '/api/organisation_requests.json',
    organisation_contacts: '/api/organisation_contacts.json',
    organisation_access_group_members: '/api/organisation_access_group_members',
    users: '/api/users.json',
    profile: '/api/profile',
    department_users: '/api/department_users',
    filtered_users: '/api/filtered_users',
    referral_recipient_groups: '/api/referrals/user_group_list',

    // Other
    countries: '/api/countries',
    proposal_type:"/api/proposal_type",
    proposals:"/api/proposal.json",
    proposal_submit:"/api/proposal_submit.json",
    approvals:"/api/approvals.json",
    referrals:"/api/referrals.json",
    proposal_standard_requirements:"/api/proposal_standard_requirements.json",
    proposal_requirements:"/api/proposal_requirements.json",
    amendment_request:"/api/amendment_request.json",
    regions:"/api/regions.json",

    // Used in internal and external dashboards
    // proposals_paginated_internal:   "/api/proposal_paginated/proposals_internal/?format=datatables",
    // referrals_paginated_internal:   "/api/proposal_paginated/referrals_internal/?format=datatables",
    species_paginated_internal: "/api/species_paginated/species_internal/?format=datatables",
    communities_paginated_internal: "/api/communities_paginated/communities_internal/?format=datatables",
    species_documents_paginated_internal: "/api/species_documents_paginated/species_documents_internal/?format=datatables",
    
    filter_lists_species:"/api/filter_lists_species",
    group_types_dict:"/api/group_types_dict",
    community_filter_dict:"/api/community_filter_dict",
    region_district_filter_dict:"/api/region_district_filter_dict",

    filter_list:                    "/api/proposal/filter_list.json",
    filter_list_approvals:          "/api/approvals/filter_list.json",
    filter_list_compliances:        "/api/compliances/filter_list.json",
    filter_list_referrals:          "/api/referrals/filter_list.json",

    site_url: site_url,
    system_name: 'Boranga System',
    proposal_type_help_url: ' https://parks.dbca.wa.gov.au/for-business/commercial-operations-licensing',
    group_types:['Fauna', 'Flora', 'Communities']
}
