<template id="occurrence_tenure_datatable_template">
    <div>
        <CollapsibleFilters
            ref="collapsible_filters"
            component_title="Filters"
            @created="collapsible_component_mounted"
        >
            <div class="row">
                <div class="col-md-3">
                    <div class="form-group">
                        <label for="cs_ref_tenure_type_lookup"
                            >Tenure Type:</label
                        >
                        <select
                            id="cs_ref_tenure_type_lookup"
                            ref="cs_ref_tenure_type_lookup"
                            name="cs_ref_tenure_type_lookup"
                            class="form-control"
                        />
                    </div>
                </div>
                <div class="col-md-3">
                    <div class="form-group">
                        <label for="cs_ref_area_id_lookup">Area ID:</label>
                        <select
                            id="cs_ref_area_id_lookup"
                            ref="cs_ref_area_id_lookup"
                            name="cs_ref_area_id_lookup"
                            class="form-control"
                        />
                    </div>
                </div>
                <div class="col-md-3">
                    <div class="form-group">
                        <label
                            for="cs_linked_with_occurrence_lookup"
                            class="text-nowrap"
                            >Linked with Occurrence:</label
                        >
                        <select
                            ref="cs_linked_with_occurrence_lookup"
                            v-model="filterCSRefCommunityApplicationStatus"
                            class="form-select"
                        >
                            <option value="all">All</option>
                            <option
                                v-for="status in tenure_statuses"
                                :key="status.value"
                                :value="status.value"
                            >
                                {{ status.name }}
                            </option>
                        </select>
                    </div>
                </div>
            </div>
        </CollapsibleFilters>
        <datatable
            :id="datatable_id"
            ref="occurrence_tenure_datatable"
            :dt-options="options"
            :dt-headers="headers"
        />
    </div>
</template>

<script>
import { api_endpoints, constants, helpers } from '@/utils/hooks';
import datatable from '@/utils/vue/datatable.vue';
import { v4 as uuid } from 'uuid';
import CollapsibleFilters from '@/components/forms/collapsible_component.vue';

export default {
    name: 'OccurrenceTenureDatatable',
    components: {
        datatable,
        CollapsibleFilters,
    },
    emit: ['highlight-on-map', 'edit-tenure-details'],
    props: {
        occurrenceId: {
            type: Number,
            required: false,
            default: null,
        },
        hrefContainerId: {
            type: String,
            required: false,
            default: '',
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
            tenure_statuses: [
                { value: 'current', name: 'Current' },
                { value: 'historical', name: 'Historical' },
            ],
            filterCSRefCommunityApplicationStatus: sessionStorage.getItem(
                this.filterCSRefCommunityApplicationStatus_cache
            )
                ? sessionStorage.getItem(
                      this.filterCSRefCommunityApplicationStatus_cache
                  )
                : 'all',
        };
    },
    computed: {
        filterApplied: function () {
            if (
                // this.filterCSRefCommunityMigratedId === 'all' &&
                this.filterCSRefCommunityApplicationStatus === 'all'
            ) {
                return false;
            } else {
                return true;
            }
        },
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
            const vm = this;
            return {
                data: 'id',
                orderable: false,
                searchable: false,
                visible: true,
                // eslint-disable-next-line no-unused-vars
                render: function (data, type, row) {
                    const coordinates = row.tenure_area_centroid
                        ? JSON.stringify(row.tenure_area_centroid.coordinates)
                        : '';
                    let html = `<a href="#${vm.hrefContainerId}" class="btn btn-primary btn-sm mb-1" data-highlight-on-map-coordinates="${coordinates}">Highlight on Map</a>`;
                    html += `<br><a href="#" class="btn btn-primary btn-sm" data-edit-tenure-details="${data}">Edit Tenure Details</a>`;
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
    watch: {
        filterCSRefCommunityApplicationStatus: function () {
            this.$refs.occurrence_tenure_datatable.vmDataTable.ajax.reload(
                helpers.enablePopovers,
                false
            );
            sessionStorage.setItem(
                this.filterCSRefCommunityApplicationStatus_cache,
                this.filterCSRefCommunityApplicationStatus
            );
        },
        filterApplied: function () {
            if (this.$refs.collapsible_filters) {
                this.$refs.collapsible_filters.show_warning_icon(
                    this.filterApplied
                );
            }
        },
    },
    mounted: function () {
        this.$nextTick(() => {
            this.addEventListeners();
        });
    },
    methods: {
        addEventListeners: function () {
            const vm = this;
            this.$refs.occurrence_tenure_datatable.vmDataTable.on(
                'click',
                'a[data-highlight-on-map-coordinates]',
                function (e) {
                    let coordinates = $(this).attr(
                        'data-highlight-on-map-coordinates'
                    );
                    coordinates = coordinates || null;
                    if (!coordinates) {
                        e.preventDefault();
                    }
                    vm.highlightOnMap(coordinates);
                }
            );
            this.$refs.occurrence_tenure_datatable.vmDataTable.on(
                'click',
                'a[data-edit-tenure-details]',
                function (e) {
                    e.preventDefault();
                    const id = $(this).attr('data-edit-tenure-details');
                    vm.editTenureDetails(id);
                    console.log(id);
                }
            );
        },
        highlightOnMap: function (coordinates = null) {
            this.$emit('highlight-on-map', JSON.parse(coordinates));
        },
        editTenureDetails: function (id) {
            this.$emit('edit-tenure-details', id);
        },
        collapsible_component_mounted: function () {
            this.$refs.collapsible_filters.show_warning_icon(
                this.filterApplied
            );
        },
    },
};
</script>
