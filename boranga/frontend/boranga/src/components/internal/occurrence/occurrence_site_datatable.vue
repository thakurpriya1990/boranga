<template id="occurrence_site_datatable_template">
    <div>
        <datatable
            :id="datatable_id"
            ref="occurrence_site_datatable"
            :dt-options="options"
            :dt-headers="headers"
        />
    </div>
</template>

<script>
import { api_endpoints, constants, helpers } from '@/utils/hooks';
import datatable from '@/utils/vue/datatable.vue';
import { v4 as uuid } from 'uuid';

export default {
    name: 'OccurrenceSiteDatatable',
    components: {
        datatable,
    },
    props: {
        occurrence_obj: {
            type: Object,
            required: true,
        },
    },
    data: function () {
        return {
            uuid: uuid(),
            datatable_id: 'occurrence-site-datatable-' + uuid(),
            headers: [
                'Site Number',
                'Action',
            ],
        };
    },
    computed: {
        column_site_number: function () {
            return {
                data: "site_number",
            }
        },
        column_action: function () {
            return {
                data: "id",
            }
        },
        options: function () {
            let vm = this;
            let columns = [
                this.column_site_number,
                this.column_action,
            ];
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
                columnDefs: [
                    { responsivePriority: 1, targets: 0 },
                    { responsivePriority: 2, targets: -1 },
                ],
                paging: true,
                scrollCollapse: true,
                scrollX: true,
                scrollY: false,
                ajax: {
                    "url": helpers.add_endpoint_json(api_endpoints.occurrence, vm.occurrence_obj.id + '/sites'),
                    "dataSrc": ''
                },
                dom: "<'d-flex align-items-center'<'me-auto'l>fB>" +
                    "<'row'<'col-sm-12'tr>>" +
                    "<'d-flex align-items-center'<'me-auto'i>p>",
                buttons: [],
                columns: columns,
                processing: true,
                initComplete: function (settings, json) {
                    helpers.enablePopovers();
                    // another option to fix the responsive table overflow css on tab switch
                    setTimeout(function () {
                        vm.adjust_table_width();
                    }, 100);
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
        adjust_table_width: function () {
            let vm = this;
            if (vm.$refs.occurrence_site_datatable !== undefined) { vm.$refs.occurrence_site_datatable.vmDataTable.columns.adjust().responsive.recalc(); }
        },
        editSiteDetails: function () {

        },
        addEventListeners: function () {
            const vm = this;
            this.$refs.occurrence_site_datatable.vmDataTable.on(
                'click',
                'a[data-edit-site-details]',
                function (e) {
                    e.preventDefault();
                    const id = $(this).attr('data-edit-site-details');
                    vm.editSiteDetails(id);
                }
            );
        },
    },
};
</script>
