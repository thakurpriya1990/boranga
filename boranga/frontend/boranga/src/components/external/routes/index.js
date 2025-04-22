import { RouterView } from 'vue-router';

import SpeciesCommunitiesDash from '../species_communities/dashboard.vue';
import ExternalConservationStatusDash from '../conservation_status/dashboard.vue';

import ExternalSpeciesCommunity from '../species_communities/species_communities.vue';

import ConservationStatusProposal from '../conservation_status/conservation_status_proposal.vue';
import ConservationStatusProposalSubmit from '../conservation_status/conservation_status_proposal_submit.vue';
import ConservationStatusReferral from '../../internal/conservation_status/referral.vue';

import ExternalOccurrenceReportDash from '../occurrence/dashboard.vue';
import OccurrenceReportProposal from '../occurrence/occurrence_report_proposal.vue';
import OccurrenceReportReferral from '../../internal/occurrence/referral.vue';

import OCRProposalSubmit from '../occurrence/ocr_proposal_submit.vue';

export default {
    path: '/external',
    component: RouterView,
    children: [
        {
            path: 'species-communities',
            component: SpeciesCommunitiesDash,
            name: 'external-species-communities-dash',
        },
        {
            path: 'species-communities',
            component: RouterView,
            children: [
                {
                    path: ':species_community_id',
                    name: 'external-species-communities',
                    component: ExternalSpeciesCommunity,
                },
            ],
        },
        {
            path: 'occurrence-report',
            component: ExternalOccurrenceReportDash,
            name: 'external-occurrence-report-dash',
        },
        {
            path: 'occurrence-report',
            component: RouterView,
            children: [
                {
                    path: ':occurrence_report_id',
                    component: OccurrenceReportProposal,
                    name: 'draft_ocr_proposal',
                },
                {
                    path: 'submit',
                    component: OCRProposalSubmit,
                    name: 'submit_ocr_proposal',
                },
                {
                    path: ':occurrence_report_id/referral/:referral_id',
                    component: OccurrenceReportReferral,
                    name: 'occurrence-report-referral',
                },
            ],
        },
        {
            path: 'conservation-status',
            component: ExternalConservationStatusDash,
            name: 'external-conservation-status-dash',
        },
        {
            path: 'conservation-status',
            component: RouterView,
            children: [
                {
                    path: ':conservation_status_id',
                    component: ConservationStatusProposal,
                    name: 'draft_cs_proposal',
                },
                {
                    path: 'submit',
                    component: ConservationStatusProposalSubmit,
                    name: 'submit_cs_proposal',
                },
                {
                    path: ':conservation_status_id/referral/:referral_id',
                    component: ConservationStatusReferral,
                    name: 'conservation-status-referral',
                },
            ],
        },
    ],
};
