import InternalDashboard from '../dashboard.vue'
import Search from '../search.vue'
import User from '../users/manage.vue'
import Proposal from '../proposals/proposal.vue'
import ProposalCompare from '../proposals/proposal_compare.vue'
import Referral from '../referrals/referral.vue'
import ApprovalDash from '../approvals/dashboard.vue'
import ComplianceDash from '../compliances/dashboard.vue'
import Compliance from '../compliances/access.vue'
import Approval from '../approvals/approval.vue'
//import PaymentOrder from '@/components/common/tclass/payment_order.vue'
//import PaymentOrder from '@/components/common/tclass/payment_order.vue'
//import PaymentDash from '@/components/common/payments_dashboard.vue'
//import ParkBookingDash from '@/components/common/parkbookings_dashboard.vue'
import Reports from '@/components/reports/reports.vue'
import ParkEntryFeesDashboard from '../park_entry_fees_dashboard.vue'
import SpeciesCommunitiesDash from '../species_communities/dashboard.vue'
import SpeciesCommunities from '../species_communities/species_communities.vue'
export default
{
    path: '/internal',
    component:
    {
        render(c)
        {
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
            name:"internal-approvals-dash"
        },
        {
            path: 'species-communities',
            component: SpeciesCommunitiesDash,
            name:"internal-species-communities-dash"
        },
        {
            path: 'approval/:approval_id',
            component: Approval,

        },
        {
            path: 'compliances',
            component: ComplianceDash,
            name:"internal-compliances-dash"
        },
        {
            path: 'compliance/:compliance_id',
            component: Compliance,

        },
        {
            path: 'search',
            component: Search,
            name:"internal-search"
        },
        // {
        //     path: 'payment',
        //     component: PaymentDash,
        //     props: { level: 'internal' }
        //     //component: PaymentOrder,
        // },
        // {
        //     path: 'payment',
        //     component: ParkBookingDash,
        //     props: { level: 'internal' }
        // },
        {
            path: 'payment',
            component: ParkEntryFeesDashboard,
        },
       /* {
            path: 'payment_order',
            component: PaymentOrder,
            name:"payment_order"
        },*/
        {
            path:'reports',
            name:'reports',
            component:Reports
        },

        {
            path: 'users',
            component: {
                render(c)
                {
                    return c('router-view')
                }
            },
            children: [
                {
                    path: ':user_id',
                    component: User,
                    name:"internal-user-detail"
                },
            ]
        },
        {
            path: 'proposal',
            component: {
                render(c)
                {
                    return c('router-view')
                }
            },
            children: [
                {
                    path: ':proposal_id',
                    component: {
                        render(c)
                        {
                            return c('router-view')
                        }
                    },
                    children: [
                        {
                            path: '/',
                            component: Proposal,
                            name:"internal-proposal"
                        },
                        {
                            path: 'referral/:referral_id',
                            component: Referral,
                            name:"internal-referral"
                        },
                    ]
                },
            ]
        },
        {
            path: 'species_communities',
            component: {
                render(c)
                {
                    return c('router-view')
                }
            },
            children: [
                {
                    path: ':proposal_id',
                    component: {
                        render(c)
                        {
                            return c('router-view')
                        }
                    },
                    children: [
                        {
                            path: '/',
                            component: SpeciesCommunities,
                            name:"internal-species-communities"
                        },
                        {
                            path: 'referral/:referral_id',
                            component: Referral,
                            name:"internal-species-communities-referral"
                        }
                    ]
                },
            ]
        },


        {
            path: 'proposal_compare',
            component: {
                render(c)
                {
                    return c('router-view')
                }
            },
            children: [
                {
                    path: ':proposal_id',
                    component: {
                        render(c)
                        {
                            return c('router-view')
                        }
                    },
                    children: [
                        {
                            path: '/',
                            component: ProposalCompare,
                            name:"proposal-compare"
                        }
                    ]
                },
            ]
        },
        // {
        //     path: 'district_proposal',
        //     component: {
        //         render(c)
        //         {
        //             return c('router-view')
        //         }
        //     },
        //     children: [
        //         {
        //             path: ':district_proposal_id',
        //             component: {
        //                 render(c)
        //                 {
        //                     return c('router-view')
        //                 }
        //             },
        //             children: [
        //                 {
        //                     path: '/',
        //                     component: DistrictProposal,
        //                     name:"internal-district-proposal"
        //                 },
        //             ]
        //         },
        //     ]
        // },

        /*{
            path: 'proposal',
            component: Proposal,
            name:"new_proposal"
        }*/
    ]
}
