<template lang="html">
    <div id="occurrenceCombineContacts">
        <datatable
            :id="panelBody"
            ref="contacts_datatable"
            :dt-options="contacts_options"
            :dt-headers="contacts_headers"
        />
    </div>
</template>

<script>
import datatable from '@vue-utils/datatable.vue';
import { constants, helpers } from '@/utils/hooks';

export default {
    name: 'OccurrenceCombineContacts',
    components: {
        datatable,
    },
    props: {
        selectedKeyContacts: {
            type: Array,
            required: true,
        },
        combineKeyContactIds: {
            type: Array,
            required: true,
        },
        mainOccurrenceId: {
            type: Number,
            required: true,
        },
    },
    data: function () {
        let vm = this;
        return {
            panelBody: 'contact-combine-select-' + vm._uid,
            checkedContactNames: [],
            contacts_headers: [
                'Occurrence',
                'Name',
                'Role',
                'Contact Details',
                'Organisation',
                'Notes',
                'Action',
            ],
            contacts_options: {
                autowidth: true,
                language: {
                    processing: constants.DATATABLE_PROCESSING_HTML,
                },
                paging: true,
                responsive: true,
                columnDefs: [
                    { responsivePriority: 1, targets: 0 },
                    { responsivePriority: 2, targets: -1 },
                ],
                data: vm.selectedKeyContacts,
                order: [],
                buttons: [],
                searching: true,
                dom:
                    "<'d-flex align-items-center'<'me-auto'l>fB>" +
                    "<'row'<'col-sm-12'tr>>" +
                    "<'d-flex align-items-center'<'me-auto'i>p>",
                columns: [
                    {
                        data: 'occurrence__occurrence_number',
                        orderable: true,
                        searchable: true,
                    },
                    {
                        data: 'contact_name',
                        orderable: true,
                        searchable: true,
                    },
                    {
                        data: 'role',
                    },
                    {
                        data: 'contact',
                        mRender: function (data, type, full) {
                            let value = full.contact;
                            let result = helpers.dtPopover(value, 30, 'hover');
                            return type == 'export' ? value : result;
                        },
                    },
                    {
                        data: 'organisation',
                    },
                    {
                        data: 'notes',
                        mRender: function (data, type, full) {
                            let value = full.notes;
                            let result = helpers.dtPopover(value, 30, 'hover');
                            return type == 'export' ? value : result;
                        },
                    },
                    {
                        data: 'id',
                        mRender: function (data, type, full) {
                            if (vm.combineKeyContactIds.includes(full.id)) {
                                if (
                                    full.occurrence__id == vm.mainOccurrenceId
                                ) {
                                    return `<input id='${full.id}' data-contact-checkbox='${full.id}' contact-name='${full.contact_name}' type='checkbox' checked disabled/>`;
                                } else {
                                    return `<input id='${full.id}' data-contact-checkbox='${full.id}' contact-name='${full.contact_name}' type='checkbox' checked/>`;
                                }
                            } else {
                                //console.log(vm.checkedContactNames)
                                if (
                                    vm.checkedContactNames.includes(
                                        full.contact_name
                                    )
                                ) {
                                    return `<input id='${full.id}' data-contact-checkbox='${full.id}' contact-name='${full.contact_name}' type='checkbox' disabled/>`;
                                } else {
                                    return `<input id='${full.id}' data-contact-checkbox='${full.id}' contact-name='${full.contact_name}' type='checkbox'/>`;
                                }
                            }
                        },
                    },
                ],
            },
            drawCallback: function () {
                setTimeout(function () {
                    vm.adjust_table_width();
                }, 100);
            },
            initComplete: function () {
                // another option to fix the responsive table overflow css on tab switch
                setTimeout(function () {
                    vm.adjust_table_width();
                }, 100);
            },
        };
    },
    created: function () {
        let vm = this;
        vm.getSelectedContactNames();
    },
    mounted: function () {
        let vm = this;
        this.$nextTick(() => {
            vm.addEventListeners();
        });
    },
    methods: {
        getSelectedContactNames: function () {
            let vm = this;
            let names = [];
            vm.selectedKeyContacts.forEach((contact) => {
                if (
                    vm.combineKeyContactIds.includes(contact.id) &&
                    !names.includes(contact.contact_name)
                ) {
                    names.push(contact.contact_name);
                }
            });
            vm.checkedContactNames = names;
        },
        adjust_table_width: function () {
            if (this.$refs.contacts_datatable !== undefined) {
                this.$refs.contacts_datatable.vmDataTable.columns
                    .adjust()
                    .responsive.recalc();
            }
            helpers.enablePopovers();
        },
        removeContact: function (id) {
            let vm = this;
            vm.combineKeyContactIds.splice(
                vm.combineKeyContactIds.indexOf(id),
                1
            );
            vm.getSelectedContactNames();
        },
        addContact: function (id) {
            let vm = this;
            vm.combineKeyContactIds.push(id);
            vm.getSelectedContactNames();
        },
        addEventListeners: function () {
            let vm = this;
            vm.$refs.contacts_datatable.vmDataTable.on(
                'change',
                'input[data-contact-checkbox]',
                function (e) {
                    e.preventDefault();
                    var id = parseInt($(this).attr('data-contact-checkbox'));
                    if ($(this).prop('checked')) {
                        vm.addContact(id);
                        vm.selectedKeyContacts.forEach((contact) => {
                            let checkbox =
                                vm.$refs.contacts_datatable.vmDataTable.$(
                                    '#' + contact.id
                                );
                            if (
                                id != checkbox.attr('data-contact-checkbox') &&
                                checkbox.attr('contact-name') ==
                                    $(this).attr('contact-name')
                            ) {
                                checkbox.prop('disabled', true);
                            }
                        });
                    } else {
                        vm.removeContact(id);
                        vm.selectedKeyContacts.forEach((contact) => {
                            let checkbox =
                                vm.$refs.contacts_datatable.vmDataTable.$(
                                    '#' + contact.id
                                );
                            if (
                                id != checkbox.attr('data-contact-checkbox') &&
                                checkbox.attr('contact-name') ==
                                    $(this).attr('contact-name')
                            ) {
                                checkbox.prop('disabled', false);
                            }
                        });
                    }
                }
            );
            vm.$refs.contacts_datatable.vmDataTable.on('draw', function (e) {
                helpers.enablePopovers();
            });
            vm.$refs.contacts_datatable.vmDataTable.on(
                'childRow.dt',
                function (e, settings) {
                    helpers.enablePopovers();
                }
            );
        },
    },
};
</script>
