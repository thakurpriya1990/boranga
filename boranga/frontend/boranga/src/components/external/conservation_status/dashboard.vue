<template>
    <div class="container" id="externalCSDash">
        <FormSection
            :formCollapse="false"
            label="Conservation Status"
            subtitle="- submit and view your proposed conservation status listings"
            Index="applications"
        >
            <ConservationStatusTable
                level="external"
                :url="conservation_status_url"
            />
        </FormSection>
        <FormSection
            :formCollapse="false"
            label="Conservation Status Proposals Referred to Me"
            Index="cs_referred_to_me"
        >
            <ConservationStatusExternalReferralsDashboard
                level="external"
                :url="cs_external_referrals_url"
            />
        </FormSection>
    </div>
</template>

<script>

import FormSection from "@/components/forms/section_toggle.vue"
import ConservationStatusTable from './conservation_status_proposal_table.vue'
import ConservationStatusExternalReferralsDashboard from '@common-utils/cs_external_referrals_dashboard.vue'
import { api_endpoints } from '@/utils/hooks'

export default {
    name: 'ExternalConservationStatusDashboard',
    data() {
        let vm = this;
        return {
            conservation_status_url: api_endpoints.conservation_status_paginated_external,
            cs_external_referrals_url: api_endpoints.conservation_status_referred_to_me,
        }
    },
    components:{
        FormSection,
        ConservationStatusTable,
        ConservationStatusExternalReferralsDashboard,
    },
    computed: {
        is_external: function() {
            return this.level == 'external'
        },
    },
}
</script>
