import User from '../users/manage.vue'
import SpeciesCommunitiesDash from '../species_communities/dashboard.vue'
import SpeciesCommunities from '../species_communities/species_communities.vue'
import ConservationStatusDash from '../conservation_status/dashboard.vue'
import ConservationStatus from '../conservation_status/conservation_status.vue'
import ConservationStatusReferral from '../conservation_status/referral.vue'
import MeetingsDash from '../meetings/dashboard.vue'
import Meeting from '../meetings/meeting.vue'
import OccurrenceDash from '../occurrence/dashboard.vue'
import Occurrence from '../occurrence/occurrence.vue'
import OccurrenceReport from '../occurrence/occurrence_report.vue'
import OccurrenceReportReferral from '../occurrence/referral.vue'

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
                component: SpeciesCommunitiesDash,
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
                path: 'occurrence',
                component: OccurrenceDash,
                name: "internal-occurrence-dash"
            },
            {
                path: 'occurrence/:occurrence_id',
                component: Occurrence,
                name: "internal-occurrence-detail"
            },
            {
                path: 'occurrence_report',
                component: {
                    render(c) {
                        return c('router-view')
                    },
                },
                children: [
                    {
                        path: ':occurrence_report_id',
                        component: {
                            render(c) {
                                return c('router-view')
                            },
                        },
                        children: [
                            {
                                path: '/',
                                component: OccurrenceReport,
                                name: "internal-occurrence-report-detail",
                            },
                            {
                                path: 'referral/:referral_id',
                                component: OccurrenceReportReferral,
                                name: "internal-occurrence-report-referral"
                            }
                        ]
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
            }
        ]
    }
