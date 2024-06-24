<template lang="html">
    <div id="observerTable">
        <div class="row mb-3">
            <label for="" class="col-sm-3 control-label fw-bold">Observation Details:</label>
            <div class="col-sm-9 text-end">
                <button :disabled="isReadOnly" type="button" class="btn btn-primary mb-2 "
                    @click.prevent="newObserverDetail">
                    <i class="fa-solid fa-circle-plus"></i>
                    Add Observer
                </button>
            </div>
        </div>
        <div class="row mb-3">
            <datatable ref="observer_detail_datatable" id="observerDetailTable" :dtOptions="observer_detail_options"
                :dtHeaders="observer_detail_headers" />
        </div>
        <ObserverDetail v-if="occurrence_report_obj" ref="observer_detail" @refreshFromResponse="refreshFromResponse"
            :url="observer_detail_url" :occurrence_report="occurrence_report_obj">
        </ObserverDetail>
    </div>
</template>
<script>
import Vue from 'vue';
import datatable from '@vue-utils/datatable.vue';
import ObserverDetail from './add_observer_detail.vue'
import {
    constants,
    api_endpoints,
    helpers,
}
    from '@/utils/hooks'

export default {
    name: 'ObserverTable',
    props: {
        occurrence_report_obj: {
            type: Object,
            required: true
        },
        is_external: {
            type: Boolean,
            default: false
        },
        isReadOnly: {
            type: Boolean,
            default: true
        },
    },
    emits: ['refreshOccurrenceReport'],
    data: function () {
        let vm = this;
        return {
            observer_detail_url: api_endpoints.observer_detail,
            observer_detail_headers: ['Contact Name', 'Observer Role', 'Contact Detail', 'Organisation', 'Main Observer', 'Action'],
            observer_detail_options: {
                autowidth: false,
                language: {
                    processing: constants.DATATABLE_PROCESSING_HTML
                },
                responsive: true,
                searching: true,
                //  to show the "workflow Status","Action" columns always in the last position
                columnDefs: [
                    { responsivePriority: 1, targets: 0 },
                    { responsivePriority: 2, targets: -1 },
                ],
                ajax: {
                    "url": helpers.add_endpoint_json(api_endpoints.occurrence_report, vm.occurrence_report_obj.id + '/observer_details'),
                    "dataSrc": ''
                },
                order: [],
                dom: "<'d-flex align-items-center'<'me-auto'l>fB>" +
                    "<'row'<'col-sm-12'tr>>" +
                    "<'d-flex align-items-center'<'me-auto'i>p>",
                buttons: [
                    {
                        extend: 'excel',
                        text: '<i class="fa-solid fa-download"></i> Excel',
                        className: 'btn btn-primary me-2 rounded',
                        exportOptions: {
                            orthogonal: 'export'
                        }
                    },
                    {
                        extend: 'csv',
                        text: '<i class="fa-solid fa-download"></i> CSV',
                        className: 'btn btn-primary rounded',
                        exportOptions: {
                            orthogonal: 'export'
                        }
                    },
                ],
                columns: [
                    {
                        data: "observer_name",
                        orderable: true,
                        searchable: true,
                        mRender: function (data, type, full) {
                            if (full.visible) {
                                return full.observer_name;
                            } else {
                                return '<s>' + full.observer_name + '</s>'
                            }
                        },
                    },
                    {
                        data: "role",
                        orderable: true,
                        searchable: true,
                        mRender: function (data, type, full) {
                            if (full.visible) {
                                return full.role;
                            } else {
                                return '<s>' + full.role + '</s>'
                            }
                        },
                    },
                    {
                        data: "contact",
                        orderable: true,
                        searchable: true,
                        mRender: function (data, type, full) {
                            if (full.visible) {
                                let value = full.contact;
                                let result = helpers.dtPopover(value, 30, 'hover');
                                return type == 'export' ? value : result;
                            } else {
                                let value = full.contact;
                                let result = helpers.dtPopover(value, 30, 'hover');
                                return '<s>' + type == 'export' ? value : result + '</s>'
                            }
                        },
                    },
                    {
                        data: "organisation",
                        orderable: true,
                        searchable: true,
                        mRender: function (data, type, full) {
                            if (full.visible) {
                                return full.organisation;
                            } else {
                                return '<s>' + full.organisation + '</s>'
                            }
                        },
                    },
                    {
                        data: "main_observer",
                        orderable: true,
                        searchable: true,
                        mRender: function (data, type, full) {
                            if (full.visible) {
                                return full.main_observer;
                            } else {
                                return '<s>' + full.main_observer; + '</s>'
                            }
                        },
                    },
                    {
                        data: "id",
                        mRender: function (data, type, full) {
                            let links = '';
                            if (full.visible) {
                                if (!vm.isReadOnly) {
                                    links += `<a href='#${full.id}' data-edit-observer_det='${full.id}'>Edit</a><br/>`;
                                    links += `<a href='#' data-delete-observer_det='${full.id}'>Discard</a><br>`;
                                } else {
                                    links += `<a href='#${full.id}' data-view-observer_det='${full.id}'>View</a><br/>`;
                                }
                            } else if (!vm.isReadOnly) {
                                links += `<a href='#' data-reinstate-observer_det='${full.id}'>Reinstate</a><br>`;
                            }
                            return links;
                        }
                    },
                ],
                processing: true,
                drawCallback: function () {
                    helpers.enablePopovers();
                },
                initComplete: function () {
                    helpers.enablePopovers();
                    // another option to fix the responsive table overflow css on tab switch
                    setTimeout(function () {
                        vm.adjust_table_width();
                    }, 100);
                },
            }
        }
    },
    components: {
        datatable,
        ObserverDetail,
    },
    watch: {
        isReadOnly: function (newVal, oldVal) {
            this.$refs.observer_detail_datatable.vmDataTable.ajax.reload();
        }
    },
    methods: {
        eventListeners: function () {
            let vm = this;
            vm.$refs.observer_detail_datatable.vmDataTable.on('click', 'a[data-edit-observer_det]', function (e) {
                e.preventDefault();
                var id = $(this).attr('data-edit-observer_det');
                vm.editObserverDetail(id);
            });
            vm.$refs.observer_detail_datatable.vmDataTable.on('click', 'a[data-view-observer_det]', function (e) {
                e.preventDefault();
                var id = $(this).attr('data-view-observer_det');
                vm.viewObserverDetail(id);
            });
            // External Discard listener
            vm.$refs.observer_detail_datatable.vmDataTable.on('click', 'a[data-delete-observer_det]', function (e) {
                e.preventDefault();
                var id = $(this).attr('data-delete-observer_det');
                vm.deleteObserverDetail(id);
            });
            vm.$refs.observer_detail_datatable.vmDataTable.on('click', 'a[data-reinstate-observer_det]', function (e) {
                e.preventDefault();
                var id = $(this).attr('data-reinstate-observer_det');
                vm.reinstateObserverDetail(id);
            });
            vm.$refs.observer_detail_datatable.vmDataTable.on('childRow.dt', function (e, settings) {
                helpers.enablePopovers();
            });
        },
        refreshFromResponse: function () {
            let vm = this;
            vm.$refs.observer_detail_datatable.vmDataTable.ajax.reload();
        },
        adjust_table_width: function () {
            let vm = this;
            if (vm.$refs.observer_detail_datatable !== undefined) { vm.$refs.observer_detail_datatable.vmDataTable.columns.adjust().responsive.recalc(); }
        },
        newObserverDetail: function () {
            let vm = this;
            this.$refs.observer_detail.observer_detail_id = '';
            //----for adding new observer
            var new_observer_detail = {
                occurrence_report: vm.occurrence_report_obj.id,
                observer_name: '',
                role: '',
                contact: '',
                organisation: '',
                main_observer: null,
            }
            this.$refs.observer_detail.observerObj = new_observer_detail;
            this.$refs.observer_detail.observer_detail_action = 'add';
            this.$refs.observer_detail.isModalOpen = true;
        },
        editObserverDetail: function (id) {
            let vm = this;
            this.$refs.observer_detail.observer_detail_id = id;
            this.$refs.observer_detail.observer_detail_action = 'edit';
            Vue.http.get(helpers.add_endpoint_json(api_endpoints.observer_detail, id)).then((response) => {
                this.$refs.observer_detail.observerObj = response.body;
            },
                err => {
                    console.log(err);
                });
            this.$refs.observer_detail.isModalOpen = true;
        },
        viewObserverDetail: function (id) {
            let vm = this;
            this.$refs.observer_detail.observer_detail_id = id;
            this.$refs.observer_detail.observer_detail_action = 'view';
            Vue.http.get(helpers.add_endpoint_json(api_endpoints.observer_detail, id)).then((response) => {
                this.$refs.observer_detail.observerObj = response.body;
            },
                err => {
                    console.log(err);
                });
            this.$refs.observer_detail.isModalOpen = true;
        },
        deleteObserverDetail: function (id) {
            let vm = this;
            swal.fire({
                title: "Discard Observer",
                text: "Are you sure you want to discard this Observer?",
                icon: "question",
                showCancelButton: true,
                confirmButtonText: 'Discard Observer',
                customClass: {
                    confirmButton: 'btn btn-primary',
                    cancelButton: 'btn btn-secondary me-2',
                },
                reverseButtons: true,
            }).then((result) => {
                if (result.isConfirmed) {
                    vm.$http.post(helpers.add_endpoint_json(api_endpoints.observer_detail, id + '/discard'))
                        .then((response) => {
                            swal.fire({
                                title: 'Discarded',
                                text: 'The Observer has been discarded',
                                icon: 'success',
                                customClass: {
                                    confirmButton: 'btn btn-primary',
                                },
                            }).then((result) => {
                                vm.$refs.observer_detail_datatable.vmDataTable.ajax.reload();
                                vm.$emit('refreshOccurrenceReport');
                                if (vm.occurrence_report_obj.processing_status == "Unlocked") {
                                    vm.$router.go();
                                }
                            });
                        }, (error) => {
                            console.log(error);
                        });
                }
            }, (error) => {

            });
        },
        reinstateObserverDetail: function (id) {
            let vm = this;
            vm.$http.post(helpers.add_endpoint_json(api_endpoints.observer_detail, id + '/reinstate'))
                .then((response) => {
                    swal.fire({
                        title: 'Reinstated',
                        text: 'The Observer has been reinstated',
                        icon: 'success',
                        customClass: {
                            confirmButton: 'btn btn-primary',
                        },
                    }).then((result) => {
                        vm.$refs.observer_detail_datatable.vmDataTable.ajax.reload();
                        vm.$emit('refreshOccurrenceReport');
                        if (vm.occurrence_report_obj.processing_status == "Unlocked") {
                            vm.$router.go();
                        }
                    });
                }, (error) => {
                    console.log(error);
                });
        },
        updatedObserverDetails() {
            let vm = this;
            this.$refs.observer_detail_datatable.vmDataTable.ajax.reload();
            vm.$emit('refreshOccurrenceReport');
            if (vm.occurrence_report_obj.processing_status == "Unlocked") {
                vm.$router.go();
            }
        },
    },
    mounted: function () {
        let vm = this;
        this.$nextTick(() => {
            vm.eventListeners();
        });
    },
}
</script>
