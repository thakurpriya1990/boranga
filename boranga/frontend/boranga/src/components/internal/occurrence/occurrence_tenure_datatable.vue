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
    emit: ['highlight-on-map', 'edit-tenure-details'],
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
                'Status',
                'Vesting',
                'Purpose',
                'Comments',
                'Signif. to OCC',
                "Owner's Name",
                // 'Owner Count',
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
                data: 'status_display',
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
                    const coordinates = row.tenure_area_centroid
                        ? row.tenure_area_centroid.coordinates
                        : null;
                    let html = `<a class="btn btn-primary btn-sm mb-1" data-highlight-on-map-coordinates="${coordinates}">Highlight on Map</a>`;
                    html += `<br><a class="btn btn-primary btn-sm" data-edit-tenure-details="${data}">Edit Tenure Details</a>`;
                    return html;
                },
            };
        },
        options: function () {
            let columns = [
                this.column_featureid,
                // this.column_tenure_area_id,
                this.column_status,
                this.column_vesting,
                this.column_purpose,
                this.column_comments,
                this.column_significant_to_occurrence,
                this.column_owner_name,
                // this.column_owner_count,
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
                searching: true,
                ordering: true,
                order: [
                    [1, 'asc'],
                    [0, 'desc'],
                ],
                fixedColumns: {
                    start: 1,
                    end: 1,
                },
                paging: true,
                scrollCollapse: true,
                scrollX: true,
                scrollY: false,
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
    mounted: function () {
        this.$nextTick(() => {
            this.addEventListeners();
        });
    },
    methods: {
        addEventListeners: function () {
            this.$refs.occurrence_tenure_datatable.vmDataTable.on(
                'click',
                'a[data-highlight-on-map-coordinates]',
                function (e) {
                    e.preventDefault();
                    const coordinates = $(this).attr(
                        'data-highlight-on-map-coordinates'
                    );
                    console.log(coordinates);
                    this.highlightOnMap(coordinates);
                }
            );
            this.$refs.occurrence_tenure_datatable.vmDataTable.on(
                'click',
                'a[data-edit-tenure-details]',
                function (e) {
                    e.preventDefault();
                    const id = $(this).attr('data-edit-tenure-details');
                    this.editTenureDetails(id);
                    console.log(id);
                }
            );
        },
        highlightOnMap: function (coordinates) {
            this.$emit('highlight-on-map', coordinates);
        },
        editTenureDetails: function (id) {
            this.$emit('edit-tenure-details', id);
        },
    },
};
</script>
