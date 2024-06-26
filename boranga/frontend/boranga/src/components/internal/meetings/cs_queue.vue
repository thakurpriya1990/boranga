<template lang="html">
    <div id="cs_queue">
        <FormSection :formCollapse="false" label="Agenda" :Index="csQueueBody">
            <div v-if="meeting_obj.can_user_edit" class="col-sm-12">
                <div class="text-end">
                    <button :disabled="isReadOnly" type="button" class="btn btn-primary mb-2 "
                        @click.prevent="addConservationStatus">
                        <i class="fa-solid fa-circle-plus"></i>
                        Add Conservation Status
                    </button>
                </div>
            </div>
            <datatable ref="cs_queue_datatable" :id="datatable_id" :dtOptions="cs_queue_options"
                :dtHeaders="cs_queue_headers" />
        </FormSection>
        <AgendaModal ref="agenda_modal" :meeting_obj="meeting_obj" :is_internal="true"></AgendaModal>
    </div>
</template>
<script>
import {
    api_endpoints,
    constants,
    helpers
}
    from '@/utils/hooks'
import Vue from 'vue'
import "babel-polyfill"
import datatable from '@/utils/vue/datatable.vue'
import FormSection from '@/components/forms/section_toggle.vue';
import AgendaModal from './agenda_datatable.vue';

export default {
    name: 'CSQueueDatatable',
    props: {
        meeting_obj: {
            type: Object,
            required: true
        },
    },
    data: function () {
        let vm = this;
        return {
            csQueueBody: "csQueueBody" + vm._uid,
            datatable_id: 'cs-queue-datatable-' + vm._uid,
            cs_queue_headers: [
                "Order",
                "Number",
                "Type",
                "Scientific Name",
                "CS Number",
                "Action",
            ],
            cs_queue_options: {
                autoWidth: false,
                lengthMenu: [[10, 25, 50, -1], [10, 25, 50, "All"]],
                language: {
                    processing: constants.DATATABLE_PROCESSING_HTML
                },
                responsive: true,
                ajax: {
                    "url": helpers.add_endpoint_json(api_endpoints.meeting, vm.meeting_obj.id + '/fetch_agenda_items'),
                    "dataSrc": ''
                },
                order: [],
                dom: "<'d-flex align-items-center'<'me-auto'l>fB>" +
                    "<'row'<'col-sm-12'tr>>" +
                    "<'d-flex align-items-center'<'me-auto'i>p>",
                buttons: [
                    {
                        text: '<i class="fa-solid fa-download"></i> Excel',
                        className: 'btn btn-primary me-2 rounded',
                        action: function (e, dt, node, config) {
                            vm.exportData("excel");
                        }
                    },
                    {
                        text: '<i class="fa-solid fa-download"></i> CSV',
                        className: 'btn btn-primary rounded',
                        action: function (e, dt, node, config) {
                            vm.exportData("csv");
                        }
                    }
                ],
                columns: [
                    {
                        data: "id",
                        mRender: function (data, type, full) {
                            let links = '';
                            if (!vm.isReadOnly) {
                                links += `<a class="dtMoveUp" data-id="${full.id}" href='#'><i class="bi bi-caret-up-fill"></i></a><br/>`;
                                links += `<a class="dtMoveDown" data-id="${full.id}" href='#'><i class="bi bi-caret-down-fill"></i></a><br/>`;
                            }
                            return links;
                        },
                        orderable: false
                    },
                    {
                        data: null,
                    },
                    {
                        data: "group_type",
                        searchable: true,
                        mRender: function (data, type, full) {
                            if (full.group_type) {
                                return full.group_type;
                            }
                        },
                        orderable: false
                    },
                    {
                        data: "scientific_name",
                        searchable: true,
                        'render': function (value, type, full) {
                            let result = helpers.dtPopover(value, 30, 'hover');
                            return type == 'export' ? value : result;
                        },
                        orderable: false
                    },
                    {
                        data: "conservation_status_number",
                        searchable: true,
                        mRender: function (data, type, full) {
                            if (full.conservation_status_number) {
                                return full.conservation_status_number;
                            }
                        },
                        orderable: false
                    },
                    {
                        data: "conservation_status_id",
                        mRender: function (data, type, full) {
                            let links = '';
                            if (!vm.isReadOnly) {
                                links += `<a href='#${full.conservation_status_id}' data-remove-agenda-item='${full.conservation_status_id}'>Remove</a><br/>`
                            }
                            links += `<a target="_blank" href='/internal/conservation_status/${full.conservation_status_id}?action=view'>View <i class="bi bi-arrow-up-right-square"></i></a><br/>`;
                            return links;

                        },
                        orderable: false
                    },
                ],
                columnDefs: [
                    {
                        "orderable": false,
                        "targets": 1 // target means the column no.
                    },
                ],
                "order": [
                    [1, "desc"]
                ],
                searching: true,
                processing: true,
                drawCallback: function () {
                    helpers.enablePopovers();
                },
                initComplete: function () {
                    helpers.enablePopovers();
                    vm.addTableListeners();
                },
            },
            updateModal: false, // used to load the datatable in the modal when open to fix the css
            agenda_items: [],
        }
    },
    components: {
        datatable,
        FormSection,
        AgendaModal,
    },
    computed: {
        isReadOnly: function () {
            let action = this.$route.query.action;
            if (action === "edit" && this.meeting_obj && this.meeting_obj.user_edit_mode) {
                return false;
            }
            else {
                return this.meeting_obj.readonly;
            }
        },
    },
    methods: {
        updateAgendaItems() {
            let vm = this;
            vm.$refs.cs_queue_datatable.vmDataTable.ajax.reload(vm.addTableListeners, false);
        },
        // This function was used to call api and then add row to datatable manually on ANY ACTION
        constructCSQueueTable: function () {
            let vm = this;
            Vue.http.get(`/api/meeting/${vm.meeting_obj.id}/fetch_agenda_items.json`).then(res => {
                vm.agenda_items = res.body;
                vm.$refs.cs_queue_datatable.vmDataTable.clear()
                vm.$refs.cs_queue_datatable.vmDataTable.rows.add(vm.agenda_items);
                vm.$refs.cs_queue_datatable.vmDataTable.draw();
            },
                err => {
                    console.log(err);
                });
        },
        addConservationStatus: async function () {
            this.updateModal = true;
            this.$refs.agenda_modal.isModalOpen = true;
        },
        addEventListeners: function () {
            let vm = this;
            // internal Discard listener
            vm.$refs.cs_queue_datatable.vmDataTable.on('click', 'a[data-remove-agenda-item]', function (e) {
                e.preventDefault();
                var id = $(this).attr('data-remove-agenda-item');
                vm.removeAgendaItem(id);
            });
            // to add the incremental row number column to the table
            vm.$refs.cs_queue_datatable.vmDataTable.on('order.dt search.dt', function () {
                vm.$refs.cs_queue_datatable.vmDataTable.column(1, {
                    search: 'applied',
                }).nodes().each(function (cell, i) {
                    cell.innerHTML = i + 1;
                });
            }).draw();

            // Bind clicks to functions
            vm.$refs.cs_queue_datatable.vmDataTable.on('click', '.dtMoveUp', function (e) {
                e.preventDefault();
                var tr = $(e.target).parents('tr');
                var id = $(this).attr('data-id');
                vm.moveUp(id, tr);
            });
            vm.$refs.cs_queue_datatable.vmDataTable.on('click', '.dtMoveDown', function (e) {
                e.preventDefault();
                var tr = $(e.target).parents('tr');
                var id = $(this).attr('data-id');
                vm.moveDown(id, tr);
            });

            vm.$refs.cs_queue_datatable.vmDataTable.on('childRow.dt', function (e, settings) {
                helpers.enablePopovers();
            });
        },
        removeAgendaItem: function (conservation_status_id) {
            let vm = this;
            swal.fire({
                title: "Remove Agenda Item",
                text: "Are you sure you want to remove this agenda item?",
                icon: "question",
                showCancelButton: true,
                confirmButtonText: 'Remove Agenda Item',
                customClass: {
                    confirmButton: 'btn btn-primary',
                    cancelButton: 'btn btn-secondary me-2',
                },
                reverseButtons: true,
            }).then((result) => {
                if (result.isConfirmed) {
                    let payload = new Object();
                    payload.conservation_status_id = conservation_status_id;
                    Vue.http.post(`/api/meeting/${vm.meeting_obj.id}/remove_agenda_item.json`, payload)
                        .then((res) => {
                            swal.fire({
                                title: 'Removed',
                                text: 'Your agenda item is removed',
                                icon: 'success',
                                customClass: {
                                    confirmButton: 'btn btn-primary',
                                },
                            });
                            vm.meeting_obj.agenda_items_arr = res.body;
                            vm.$refs.cs_queue_datatable.vmDataTable.ajax.reload(vm.addTableListeners, false);
                        }, (error) => {
                            console.log(error);
                        });
                }
            }, (error) => {

            });
        },
        addTableListeners: function (e) {
            let vm = this;
            // for "...more" tooltip to work after reload
            helpers.enablePopovers();
            // to remove the down arrow from last row
            $(vm.$refs.cs_queue_datatable.table).find('tr:last .dtMoveDown').remove();
            // to remove the up arroiw from first row
            $(vm.$refs.cs_queue_datatable.table).children('tbody').find('tr:first .dtMoveUp').remove();
            // Remove previous binding before adding it
            $('.dtMoveUp').off('click');
            $('.dtMoveDown').off('click');

        },
        async sendDirection(req, direction) {
            let vm = this;
            let movement = direction == 'down' ? 'move_down' : 'move_up';
            try {
                const res = await fetch(helpers.add_endpoint_json(api_endpoints.meeting_agenda_items, req + '/' + movement))
                this.$parent.uuid++;
            } catch (error) {
                console.log(error);
            }
        },
        moveUp(id, tr) {
            // Move the row up
            this.moveRow(tr, 'up');
            this.sendDirection(id, 'up');
        },
        moveDown(id, tr) {
            // Move the row down
            this.moveRow(tr, 'down');
            this.sendDirection(id, 'down');
        },
        moveRow(row, direction) {
            let vm = this;
            // Move up or down (depending...)
            var table = this.$refs.cs_queue_datatable.vmDataTable;
            var index = table.row(row).index();

            var order = -1;
            if (direction === 'down') {
                order = 1;
            }

            var data1 = table.row(index).data();
            data1.order += order;

            var data2 = table.row(index + order).data();
            data2.order += -order;

            table.row(index).data(data2);
            table.row(index + order).data(data1);

            table.page(0).draw(false);

            // to remove the down arrow from last row
            $(vm.$refs.cs_queue_datatable.table).find('tr:last .dtMoveDown').remove();
            // to remove the up arroiw from first row
            $(vm.$refs.cs_queue_datatable.table).children('tbody').find('tr:first .dtMoveUp').remove();
        },
        exportData: function (format) {
            let vm = this;

            const url = api_endpoints.meeting + '/' + vm.meeting_obj.id + '/export_agenda_items?export_format=' + format;
            try {
                if (format === "excel") {
                    $.ajax({
                        type: "GET",
                        url: url,
                        contentType: "application/vnd.ms-excel",
                        dataType: "binary",
                        xhrFields: {
                            responseType: 'blob'
                        },

                        success: function (response, status, request) {
                            var contentDispositionHeader = request.getResponseHeader('Content-Disposition');
                            var filename = contentDispositionHeader.split('filename=')[1];
                            window.URL = window.URL || window.webkitURL;
                            var blob = new Blob([response], { type: "application/vnd.ms-excel" });
                            var downloadUrl = window.URL.createObjectURL(blob);
                            var a = document.createElement("a");
                            a.href = downloadUrl;
                            a.download = filename;
                            document.body.appendChild(a);
                            a.click();
                            document.body.removeChild(a);
                        },
                        error: function (xhr, status, error) {
                            console.log(error);
                        },
                    });
                }
                else if (format === "csv") {
                    $.ajax({
                        type: "GET",
                        url: url,
                        success: function (response, status, request) {
                            var contentDispositionHeader = request.getResponseHeader('Content-Disposition');
                            var filename = contentDispositionHeader.split('filename=')[1];
                            window.URL = window.URL || window.webkitURL;
                            var blob = new Blob([response], { type: "text/csv" });

                            var downloadUrl = window.URL.createObjectURL(blob);
                            var a = document.createElement("a");
                            a.href = downloadUrl;
                            a.download = filename;
                            document.body.appendChild(a);
                            a.click();
                            document.body.removeChild(a);
                        },
                        error: function (xhr, status, error) {
                            console.log(error);
                        },
                    });
                }
            }
            catch (err) {
                console.log(err);
                if (vm.is_internal) {
                    return err;
                }
            }
        },
        hideOrderColumn: function () {
            // this method is used to hide the order colmn when processing_status is completed
            let vm = this;
            if (vm.isReadOnly == true) {
                vm.$refs.cs_queue_datatable.vmDataTable.column([0]).visible(false);
            }
        },
    },
    mounted: function () {
        let vm = this;
        this.$nextTick(() => {
            vm.addEventListeners();
            vm.hideOrderColumn();
        });
    },
}
</script>
