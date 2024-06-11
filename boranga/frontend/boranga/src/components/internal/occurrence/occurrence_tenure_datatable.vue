<template id="occurrence_tenure_datatable_template">
    <div>
        <datatable
            :id="datatable_id"
            ref="occurrence_tenure_datatable"
            :dt-options="options"
            :dt-headers="headers"
        />
    </div>
</template>

<script>
import { api_endpoints, constants } from '@/utils/hooks';
import datatable from '@/utils/vue/datatable.vue';
import { v4 as uuid } from 'uuid';

export default {
    name: 'OccurrenceTenureDatatable',
    components: {
        datatable,
    },
    props: {
        occurrenceId: {
            type: Number,
            required: false,
            default: null,
        },
    },
    data: function () {
        return {
            uuid: uuid(),
            datatable_id: 'occurrence-tenure-datatable-' + uuid(),
            url: api_endpoints.occurrence_tenure_paginated_internal,
            headers: [
                'Feature ID',
                // 'Tenure Area ID',
                "Owner's Name",
                // 'Owner Count',
                'Vesting',
                'Purpose',
                'Comments',
                'Significant to OCC',
                'Status',
                'Action',
            ],
        };
    },
    computed: {
        column_featureid: function () {
            return {
                data: 'featureid',
                orderable: true,
                searchable: true,
                visible: true,
            };
        },
        column_tenure_area_id: function () {
            return {
                data: 'tenure_area_id',
                orderable: true,
                searchable: true,
                visible: true,
            };
        },
        column_owner_name: function () {
            return {
                data: 'owner_name',
                orderable: true,
                searchable: true,
                visible: true,
            };
        },
        column_vesting: function () {
            return {
                data: 'vesting',
                orderable: true,
                searchable: true,
                visible: true,
            };
        },
        column_purpose: function () {
            return {
                data: 'purpose',
                orderable: true,
                searchable: true,
                visible: true,
            };
        },
        column_comments: function () {
            return {
                data: 'comments',
                orderable: true,
                searchable: true,
                visible: true,
            };
        },
        column_significant_to_occurrence: function () {
            return {
                data: 'significant_to_occurrence',
                orderable: true,
                searchable: true,
                visible: true,
            };
        },
        column_status: function () {
            return {
                data: 'status',
                orderable: true,
                searchable: true,
                visible: true,
            };
        },
        column_action: function () {
            return {
                data: 'id',
                orderable: false,
                searchable: false,
                visible: true,
                // eslint-disable-next-line no-unused-vars
                render: function (data, type, row) {
                    let html = `<button class="btn btn-primary" @click="highlightOnMap(${data})">Highlight on Map</button>`;
                    html += `<br><button class="btn btn-primary" @click="editTenureDetails(${data})">Edit Tenure Details</button>`;
                    return html;
                },
            };
        },
        options: function () {
            let columns = [
                this.column_featureid,
                // this.column_tenure_area_id,
                this.column_owner_name,
                // this.column_owner_count,
                this.column_vesting,
                this.column_purpose,
                this.column_comments,
                this.column_significant_to_occurrence,
                this.column_status,
                this.column_action,
            ];
            let url = this.url;
            if (this.occurrenceId) {
                url = `${this.url}&occurrence_id=${this.occurrenceId}`;
            }
            return {
                autoWidth: false,
                language: {
                    processing: constants.DATATABLE_PROCESSING_HTML,
                },
                responsive: true,
                //serverSide: true,
                searching: true,
                ordering: true,
                order: [[7, 'asc'], [0, 'desc']],
                ajax: {
                    url: url,
                    dataSrc: 'data',
                    // eslint-disable-next-line no-unused-vars
                    data: function (d) {
                        // d.filter_xyz = this.xyz
                    },
                },
                dom: 'lBfrtip',
                buttons: [],
                columns: columns,
                processing: true,
                // eslint-disable-next-line no-unused-vars
                initComplete: function (settings, json) {
                    //
                },
            };
        },
    },
};
</script>
