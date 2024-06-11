<template id="occurrence_tenure_datatable_template">
    <div>
        Hello
        <datatable
            :id="datatable_id"
            ref="occurrence_tenure_datatable"
            :dtOptions="conservation_status_options"
            :dtHeaders="conservation_status_headers"/>
    </div>
</template>

<script>
import {
    api_endpoints,
    helpers
} from '@/utils/hooks';
import datatable from '@/utils/vue/datatable.vue';
import { v4 as uuid } from 'uuid';

export default {
    name: 'OccurrenceTenureDatatable',
    components: {
        datatable,
    },
    props: {
        occurrenceTenure: {
            type: Object,
            required: true,
        },
    },
    data: function () {
        let vm = this;
        return {
            datatable_id: 'occurrence-tenure-datatable-' + uuid(),
            conservation_status_headers: [
                'Tenure Type',
                'Tenure Status',
                'Tenure Start Date',
                'Tenure End Date',
            ],
            conservation_status_options: {},
        };
    },
};
</script>
