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
    </div>
</template>

<script>

import FormSection from "@/components/forms/section_toggle.vue"
import ConservationStatusTable from './conservation_status_proposal_table.vue'
import { api_endpoints } from '@/utils/hooks'

export default {
    name: 'ExternalConservationStatusDashboard',
    data() {
        let vm = this;
        return {
            conservation_status_url: api_endpoints.conservation_status_paginated_external,
        }
    },
    components:{
        FormSection,
        ConservationStatusTable,
    },
    computed: {
        is_external: function() {
            return this.level == 'external'
        },
    },
}
</script>
