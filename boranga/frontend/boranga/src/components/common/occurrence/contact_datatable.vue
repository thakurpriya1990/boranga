<template lang="html">
    <div id="contactTable">
        <div class="row mb-3">
            <label for="" class="col-sm-3 control-label fw-bold">Key Contacts:</label>
            <div class="col-sm-9 text-end">
                <button :disabled="isReadOnly" type="button" class="btn btn-primary mb-2 "
                    @click.prevent="newContactDetail">
                    <i class="fa-solid fa-circle-plus"></i>
                    Add Contact
                </button>
            </div>
        </div>
        <div class="row mb-3">
            <datatable ref="contact_detail_datatable" id="contactDetailTable" :dtOptions="contact_detail_options"
                :dtHeaders="contact_detail_headers" />
        </div>
        <ContactDetail v-if="occurrence_obj" ref="contact_detail" @refreshFromResponse="refreshFromResponse"
            :url="contact_detail_url" :occurrence="occurrence_obj">
        </ContactDetail>
    </div>
</template>
<script>
import Vue from 'vue';
import datatable from '@vue-utils/datatable.vue';
import ContactDetail from './add_contact_detail.vue'
import {
    constants,
    api_endpoints,
    helpers,
}
    from '@/utils/hooks'

export default {
    name: 'ContactTable',
    props: {
        occurrence_obj: {
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
            contact_detail_url: api_endpoints.contact_detail,
            contact_detail_headers: ['Contact Name', 'Contact Role', 'Contact Details', 'Organisation', 'Notes', 'Action'],
            contact_detail_options: {
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
                    "url": helpers.add_endpoint_json(api_endpoints.occurrence, vm.occurrence_obj.id + '/contact_details'),
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
                        data: "contact_name",
                        orderable: true,
                        searchable: true,
                        mRender: function (data, type, full) {
                            if (full.visible) {
                                return full.contact_name;
                            } else {
                                return '<s>' + full.contact_name + '</s>'
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
                                return full.contact;
                            } else {
                                return '<s>' + full.contact + '</s>'
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
                        data: "notes",
                        orderable: true,
                        searchable: true,
                        mRender: function (data, type, full) {
                            let value = full.notes;
                            let result = helpers.dtPopover(value, 60, 'hover');
                            if(full.visible){
                                return result;
                            }
                            else{
                                return '<s>' + result + '</s>';
                            }
                        },
                    },
                    {
                        data: "id",
                        mRender: function (data, type, full) {
                            let links = '';
                            if (full.visible) {
                                if (!vm.isReadOnly) {
                                    links += `<a href='#${full.id}' data-edit-contact_det='${full.id}'>Edit</a><br/>`;
                                    links += `<a href='#' data-delete-contact_det='${full.id}'>Discard</a><br>`;
                                } else {
                                    links += `<a href='#${full.id}' data-view-contact_det='${full.id}'>View</a><br/>`;
                                }
                            } else if (!vm.isReadOnly) {
                                links += `<a href='#' data-reinstate-contact_det='${full.id}'>Reinstate</a><br>`;
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
        ContactDetail,
    },
    watch: {
        isReadOnly: function (newVal, oldVal) {
            this.$refs.contact_detail_datatable.vmDataTable.ajax.reload();
        }
    },
    methods: {
        eventListeners: function () {
            let vm = this;
            vm.$refs.contact_detail_datatable.vmDataTable.on('click', 'a[data-edit-contact_det]', function (e) {
                e.preventDefault();
                var id = $(this).attr('data-edit-contact_det');
                vm.editContactDetail(id);
            });
            vm.$refs.contact_detail_datatable.vmDataTable.on('click', 'a[data-view-contact_det]', function (e) {
                e.preventDefault();
                var id = $(this).attr('data-view-contact_det');
                vm.viewContactDetail(id);
            });
            // External Discard listener
            vm.$refs.contact_detail_datatable.vmDataTable.on('click', 'a[data-delete-contact_det]', function (e) {
                e.preventDefault();
                var id = $(this).attr('data-delete-contact_det');
                vm.deleteContactDetail(id);
            });
            vm.$refs.contact_detail_datatable.vmDataTable.on('click', 'a[data-reinstate-contact_det]', function (e) {
                e.preventDefault();
                var id = $(this).attr('data-reinstate-contact_det');
                vm.reinstateContactDetail(id);
            });
            vm.$refs.contact_detail_datatable.vmDataTable.on('childRow.dt', function (e, settings) {
                helpers.enablePopovers();
            });
        },
        refreshFromResponse: function () {
            let vm = this;
            vm.$refs.contact_detail_datatable.vmDataTable.ajax.reload();
        },
        adjust_table_width: function () {
            let vm = this;
            if (vm.$refs.contact_detail_datatable !== undefined) { vm.$refs.contact_detail_datatable.vmDataTable.columns.adjust().responsive.recalc(); }
        },
        newContactDetail: function () {
            let vm = this;
            this.$refs.contact_detail.contact_detail_id = '';
            //----for adding new contact
            var new_contact_detail = {
                occurrence: vm.occurrence_obj.id,
                contact_name: '',
                role: '',
                contact: '',
                organisation: '',
                notes: '',
            }
            this.$refs.contact_detail.contactObj = new_contact_detail;
            this.$refs.contact_detail.contact_detail_action = 'add';
            this.$refs.contact_detail.isModalOpen = true;
        },
        editContactDetail: function (id) {
            let vm = this;
            this.$refs.contact_detail.contact_detail_id = id;
            this.$refs.contact_detail.contact_detail_action = 'edit';
            Vue.http.get(helpers.add_endpoint_json(api_endpoints.contact_detail, id)).then((response) => {
                this.$refs.contact_detail.contactObj = response.body;
            },
                err => {
                    console.log(err);
                });
            this.$refs.contact_detail.isModalOpen = true;
        },
        viewContactDetail: function (id) {
            let vm = this;
            this.$refs.contact_detail.contact_detail_id = id;
            this.$refs.contact_detail.contact_detail_action = 'view';
            Vue.http.get(helpers.add_endpoint_json(api_endpoints.contact_detail, id)).then((response) => {
                this.$refs.contact_detail.contactObj = response.body;
            },
                err => {
                    console.log(err);
                });
            this.$refs.contact_detail.isModalOpen = true;
        },
        deleteContactDetail: function (id) {
            let vm = this;
            swal.fire({
                title: "Discard Contact",
                text: "Are you sure you want to discard this Contact?",
                icon: "warning",
                showCancelButton: true,
                confirmButtonText: 'Discard Contact',
                confirmButtonColor: '#d9534f'
            }).then((result) => {
                if (result.isConfirmed) {
                    vm.$http.post(helpers.add_endpoint_json(api_endpoints.contact_detail, id + '/discard'))
                        .then((response) => {
                            swal.fire({
                                title: 'Discarded',
                                text: 'The Contact has been discarded',
                                icon: 'success',
                                confirmButtonColor: '#226fbb',
                            }).then((result) => {
                                vm.$refs.contact_detail_datatable.vmDataTable.ajax.reload();
                                vm.$emit('refreshOccurrenceReport');
                                if (vm.occurrence_obj.processing_status == "Unlocked") {
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
        reinstateContactDetail: function (id) {
            let vm = this;
            vm.$http.post(helpers.add_endpoint_json(api_endpoints.contact_detail, id + '/reinstate'))
                .then((response) => {
                    swal.fire({
                        title: 'Reinstated',
                        text: 'The Contact has been reinstated',
                        icon: 'success',
                        confirmButtonColor: '#226fbb',
                    }).then((result) => {
                        vm.$refs.contact_detail_datatable.vmDataTable.ajax.reload();
                        vm.$emit('refreshOccurrenceReport');
                        if (vm.occurrence_obj.processing_status == "Unlocked") {
                            vm.$router.go();
                        }
                    });
                }, (error) => {
                    console.log(error);
                });
        },
        updatedContactDetails() {
            let vm = this;
            this.$refs.contact_detail_datatable.vmDataTable.ajax.reload();
            vm.$emit('refreshOccurrenceReport');
            if (vm.occurrence_obj.processing_status == "Unlocked") {
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
