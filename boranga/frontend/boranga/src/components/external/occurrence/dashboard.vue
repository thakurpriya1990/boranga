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
                :url="occurrence_repot_url"
            />
        </FormSection>
    </div>
</template>

<script>
import datatable from '@/utils/vue/datatable.vue'
import FormSection from "@/components/forms/section_toggle.vue"
import OccurrenceReportTable from './occurrence_report_table.vue'
import { api_endpoints, helpers } from '@/utils/hooks'

export default {
    name: 'ExternalOccurrenceReportDashboard',
    data() {
        let vm = this;
        return {
            occurrence_repot_url: api_endpoints.occurrence_report_paginated_external,
        }
    },
    components:{
        FormSection,
        OccurrenceReportTable,
    },
    watch: {

    },
    computed: {
        is_external: function() {
            return this.level == 'external'
        },

    },
    methods: {
    },
    mounted: function () {

    },
    created: function() {

    },
}
</script>
