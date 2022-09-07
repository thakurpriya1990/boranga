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
import datatable from '@/utils/vue/datatable.vue'
import FormSection from "@/components/forms/section_toggle.vue"
import ConservationStatusTable from './conservation_status_proposal_table.vue'
import { api_endpoints, helpers } from '@/utils/hooks'

export default {
    name: 'ExternalConservationStatusDashboard',
    data() {
        let vm = this;
        return {
            empty_list: '/api/empty_list',
            
            //conservation_status_url: api_endpoints.proposals_paginated_external,
            //conservation_status_url
            conservation_status_url: api_endpoints.conservation_status_paginated_external,
            //system_name: api_endpoints.system_name,
        }
    },
    components:{
        FormSection,
        ConservationStatusTable,
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
