import InternalDashboard from '../dashboard.vue'
import Search from '../search.vue'
import OrgAccessTable from '../organisations/dashboard.vue'
import OrgAccess from '../organisations/access.vue'
import Organisation from '../organisations/manage.vue'
import User from '../users/manage.vue'
import Proposal from '../proposals/proposal.vue'
import ProposalCompare from '../proposals/proposal_compare.vue'
import Referral from '../referrals/referral.vue'
import ApprovalDash from '../approvals/dashboard.vue'
import ComplianceDash from '../compliances/dashboard.vue'
import Compliance from '../compliances/access.vue'
import Approval from '../approvals/approval.vue'
import Reports from '@/components/reports/reports.vue'
import ParkEntryFeesDashboard from '../park_entry_fees_dashboard.vue'
import DistrictProposal from '../district_proposals/district_proposal.vue'
import SpeciesCommunitiesDash from '../species_communities/dashboard.vue'
import SpeciesCommunities from '../species_communities/species_communities.vue'
import ConservationStatusDash from '../conservation_status/dashboard.vue'
import ConservationStatus from '../conservation_status/conservation_status.vue'
import ConservationStatusReferral from '../conservation_status/referral.vue'
import MeetingsDash from '../meetings/dashboard.vue'
import Meeting from '../meetings/meeting.vue'
import ConservationPlansDash from '../conservation_plans/dashboard.vue'
import OccurrenceDash from '../occurrence/dashboard.vue'
import Occurrence from '../occurrence/occurrence.vue'
export default
    {
        path: '/internal',
        component:
        {
            render(c) {
                return c('router-view')
            }
        },
        children: [
            {
                path: '/',
                //component: InternalDashboard
                component: SpeciesCommunitiesDash,
            },
            {
                path: 'approvals',
                component: ApprovalDash,
                name: "internal-approvals-dash"
            },
            {
                path: 'species-communities',
                component: SpeciesCommunitiesDash,
                name: "internal-species-communities-dash"
            },
            {
                path: 'conservation-status',
                component: ConservationStatusDash,
                name: "internal-conservation_status-dash"
            },
            {
                path: 'meetings',
                component: MeetingsDash,
                name: "internal-meetings-dash"
            },
            {
                path: 'meetings/:meeting_id',
                component: Meeting,
                name: "internal-meetings"

            },
            {
                path: 'conservation-plans',
                component: ConservationPlansDash,
                name: "internal-conservation_plan-dash"
            },
            {
                path: 'occurrence',
                component: OccurrenceDash,
                name: "occurrence-dashboard"
            },
            {
                path: 'occurrence/:occurrence_id',
                component: Occurrence,
                name: "internal-occurrence-detail"
            },
            {
                path: 'approval/:approval_id',
                component: Approval,

            },
            {
                path: 'compliances',
                component: ComplianceDash,
                name: "internal-compliances-dash"
            },
            {
                path: 'compliance/:compliance_id',
                component: Compliance,

            },
            {
                path: 'search',
                component: Search,
                name: "internal-search"
            },
            {
                path: 'conservation-plans',
                component: ConservationPlansDash,
                name: "internal-conservation-plans-dash"
            },
            {
                path: 'payment',
                component: ParkEntryFeesDashboard,
            },
            {
                path: 'reports',
                name: 'reports',
                component: Reports
            },

            {
                path: 'organisations',
                component: {
                    render(c) {
                        return c('router-view')
                    }
                },
                children: [
                    {
                        path: 'access',
                        component: OrgAccessTable,
                        name: "org-access-dash"
                    },
                    {
                        path: 'access/:access_id',
                        component: OrgAccess,
                        name: "org-access"
                    },
                    {
                        path: ':org_id',
                        component: Organisation,
                        name: "internal-org-detail"
                    },

                ]
            },
            {
                path: 'users',
                component: {
                    render(c) {
                        return c('router-view')
                    }
                },
                children: [
                    {
                        path: ':user_id',
                        component: User,
                        name: "internal-user-detail"
                    },
                ]
            },
            {
                path: 'proposal',
                component: {
                    render(c) {
                        return c('router-view')
                    }
                },
                children: [
                    {
                        path: ':proposal_id',
                        component: {
                            render(c) {
                                return c('router-view')
                            }
                        },
                        children: [
                            {
                                path: '/',
                                component: Proposal,
                                name: "internal-proposal"
                            },
                            {
                                path: 'referral/:referral_id',
                                component: Referral,
                                name: "internal-referral"
                            },
                            {
                                path: 'district_proposal/:district_proposal_id',
                                component: DistrictProposal,
                                name: "internal-district-proposal"
                            },
                        ]
                    },
                ]
            },
            {
                path: 'species_communities',
                component: {
                    render(c) {
                        return c('router-view')
                    },
                },
                children: [
                    {
                        path: ':species_community_id',
                        component: {
                            render(c) {
                                return c('router-view')
                            },
                        },
                        children: [
                            {
                                path: '/',
                                component: SpeciesCommunities,
                                name: "internal-species-communities"
                            },
                        ]
                    },
                ]
            },
            {
                path: 'conservation_status',
                component: {
                    render(c) {
                        return c('router-view')
                    },
                },
                children: [
                    {
                        path: ':conservation_status_id',
                        component: {
                            render(c) {
                                return c('router-view')
                            },
                        },
                        children: [
                            {
                                path: '/',
                                component: ConservationStatus,
                                name: "internal-conservation_status"
                            },
                            {
                                path: 'referral/:referral_id',
                                component: ConservationStatusReferral,
                                name: "internal-conservation_status-referral"
                            }
                        ]
                    },
                ]
            },
            {
                path: 'proposal_compare',
                component: {
                    render(c) {
                        return c('router-view')
                    }
                },
                children: [
                    {
                        path: ':proposal_id',
                        component: {
                            render(c) {
                                return c('router-view')
                            }
                        },
                        children: [
                            {
                                path: '/',
                                component: ProposalCompare,
                                name: "proposal-compare"
                            }
                        ]
                    },
                ]
            }
        ]
    }
