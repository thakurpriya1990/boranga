<template lang="html">
    <div id="related_items">
        <FormSection :formCollapse="false" label="Related Items" Index="related_items">
            <CollapsibleFilters component_title="Filters" ref="collapsible_filters"
                @created="collapsible_component_mounted" class="mb-2">
                <div class="row">
                    <div class="col-md-3">
                        <div class="form-group">
                            <label for="">Related Type:</label>
                            <select class="form-select" v-model="filterRelatedType">
                                <option value="all">All</option>
                                <option v-for="option in related_type_filter_list" :value="option[0]">{{ option[1] }}
                                </option>
                            </select>
                        </div>
                    </div>
                </div>
            </CollapsibleFilters>
            <div>
                <datatable ref="related_items_datatable" :id="datatable_id" :dtOptions="datatable_options"
                    :dtHeaders="datatable_headers" />
            </div>
        </FormSection>
    </div>
</template>

<script>
import { v4 as uuid } from 'uuid'
import { constants, helpers } from '@/utils/hooks'
import datatable from '@/utils/vue/datatable.vue'
import FormSection from '@/components/forms/section_toggle.vue';
import CollapsibleFilters from '@/components/forms/collapsible_component.vue'
export default {
    name: 'TableRelatedItems',
    components: {
        datatable,
        FormSection,
        CollapsibleFilters,
    },
    props: {
        ajax_url: {
            type: String,
            required: true,
        },
        filter_list_url: {
            type: String,
            required: true,
        },
    },
    data() {
        return {
            datatable_id: uuid(),
            related_type_filter_list: [],
            filterRelatedType: 'all',
        }
    },
    computed: {
        column_lodgement_number: function () {
            return {
                data: 'identifier',
                orderable: false,
                searchable: true,
                visible: true,
            }
        },
        column_type: function () {
            return {
                data: 'model_name',
                orderable: false,
                searchable: false,
                visible: true,
            }
        },
        column_description: function () {
            return {
                data: 'descriptor',
                orderable: false,
                searchable: true,
                visible: true,
                'render': function (value, type) {
                    let result = helpers.dtPopover(value, 30, 'hover');
                    return type == 'export' ? value : result;
                },
            }
        },
        column_status: function () {
            return {
                data: 'status',
                orderable: false,
                searchable: false,
                visible: true,
            }
        },
        column_action: function () {
            return {
                data: 'action_url',
                orderable: false,
                searchable: false,
                visible: true,
            }
        },
        datatable_options: function () {
            let vm = this
            let columns = [
                vm.column_lodgement_number,
                vm.column_type,
                vm.column_description,
                vm.column_status,
                vm.column_action,
            ]
            return {
                autoWidth: false,
                language: {
                    processing: constants.DATATABLE_PROCESSING_HTML
                },
                responsive: true,
                searching: true,
                ordering: true,
                order: [[0, 'desc']],
                ajax: {
                    "url": vm.ajax_url,
                    "dataSrc": "",
                    "data": function (d) {
                        d.related_filter_type = vm.filterRelatedType
                    }
                },
                dom: 'lBfrtip',
                buttons: [],
                columns: columns,
                processing: true,
                drawCallback: function () {
                    helpers.enablePopovers();
                },
                initComplete: function () {
                    helpers.enablePopovers();
                },
            }
        },
        datatable_headers: function () {
            return [
                'Number',
                'Type',
                'Description',
                'Status',
                'Action',
            ]
        },
        filterApplied: function () {
            if (this.filterRelatedType === 'all') {
                return false
            } else {
                return true
            }
        },
    },
    watch: {
        filterRelatedType: function () {
            let vm = this;
            vm.$refs.related_items_datatable.vmDataTable.ajax.reload();
        },
        filterApplied: function () {
            if (this.$refs.collapsible_filters) {
                // Collapsible component exists
                this.$refs.collapsible_filters.show_warning_icon(this.filterApplied)
            }
        },
    },
    methods: {
        collapsible_component_mounted: function () {
            this.$refs.collapsible_filters.show_warning_icon(this.filterApplied)
        },
        fetchFilterList: function () {
            let vm = this;
            //large FilterList of Species Values object
            vm.$http.get(vm.filter_list_url).then((response) => {
                vm.related_type_filter_list = response.body;
            }, (error) => {
                console.log(error);
            })
        },
    },
    mounted: function () {
        let vm = this;
        vm.fetchFilterList();
        vm.$nextTick(() => {
            vm.$refs.related_items_datatable.vmDataTable.on('childRow.dt', function (e, settings) {
                helpers.enablePopovers();
            });
        });
    }
}
</script>
