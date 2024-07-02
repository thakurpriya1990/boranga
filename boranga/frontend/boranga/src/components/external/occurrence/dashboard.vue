<template>
    <div class="container" id="externalOCRDash">
        <FormSection
            :formCollapse="false"
            label="Occurrence Report"
            subtitle="- submit and view your reported occurrences"
            Index="applications"
        >
            <OccurrenceReportTable
                level="external"
                :url="occurrence_report_url"
            />
        </FormSection>
        <FormSection
            :formCollapse="false"
            label="Occurrence Reports Referred to Me"
            Index="ocr_referred_to_me"
        >
            <OccurrenceReportExternalReferralsDashboard
                level="external"
                :url="ocr_external_referrals_url"
            />
        </FormSection>
    </div>
</template>

<script>
import FormSection from "@/components/forms/section_toggle.vue"
import OccurrenceReportTable from './occurrence_report_table.vue'
import OccurrenceReportExternalReferralsDashboard from '@common-utils/ocr_external_referrals_dashboard.vue'

import { api_endpoints } from '@/utils/hooks'

export default {
    name: 'ExternalOccurrenceReportDashboard',
    data() {
        return {
            occurrence_report_url: api_endpoints.occurrence_report_paginated_external,
            ocr_external_referrals_url: api_endpoints.occurrence_report_paginated_referred_to_me,
        }
    },
    components:{
        FormSection,
        OccurrenceReportTable,
        OccurrenceReportExternalReferralsDashboard,
    },
    computed: {
        is_external: function() {
            return this.level == 'external'
        },
    },
}
</script>
