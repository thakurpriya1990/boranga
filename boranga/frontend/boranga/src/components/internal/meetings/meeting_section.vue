<template lang="html">
    <div id="communityStatus">
        <FormSection :formCollapse="false" label="Meeting" Index="meeting">
            <alert type="danger" v-if="!isMeetingDateValid"><strong>Please select End Date that is later than Start
                    Date</strong></alert>
            <div class="row mb-3">
                <label for="" class="col-sm-4 control-label fw-bold">Title: <span class="text-danger">*</span></label>
                <div class="col-sm-8">
                    <input :disabled="isReadOnly" type="text" class="form-control" id="title" ref="title" placeholder=""
                        v-model="meeting_obj.title" autofocus />
                </div>
            </div>
            <!-- <div class="row mb-3">
                <label for="" class="col-sm-4 control-label fw-bold">Start Date/ Time: <span class="text-danger">*</span></label>
                <div class="col-sm-8">

                    <input :disabled="isReadOnly" type="datetime-local" class="form-control" name="start_date"
                        ref="start_date" v-model="meeting_obj.start_date" @change="validateMeetingDate()" />
                </div>
            </div> -->
            <div class="row mb-3">
                <label for="" class="col-sm-4 control-label fw-bold">Start Date/ Time: <span
                        class="text-danger">*</span></label>
                <div class="col-sm-8">

                    <input :disabled="isReadOnly" type="datetime-local" class="form-control" name="start_date"
                        ref="start_date" v-model="start_date" @change="validateMeetingDate()" />
                </div>
            </div>
            <!-- <div class="row mb-3">
                <label for="" class="col-sm-4 control-label fw-bold">End Date/ Time: <span class="text-danger">*</span></label>
                <div class="col-sm-8">
                    <input :disabled="isReadOnly" type="datetime-local" class="form-control" id="end_date"
                        v-model="meeting_obj.end_date" @change="validateMeetingDate()" />
                </div>
            </div> -->
            <div class="row mb-3">
                <label for="" class="col-sm-4 control-label fw-bold">End Date/ Time: <span
                        class="text-danger">*</span></label>
                <div class="col-sm-8">
                    <input :disabled="isReadOnly" type="datetime-local" class="form-control" id="end_date"
                        v-model="end_date" @change="validateMeetingDate()" />
                </div>
            </div>
            <div class="row mb-3">
                <label for="" class="col-sm-4 control-label fw-bold">Meeting Type: <span
                        class="text-danger">*</span></label>
                <div class="col-sm-8">
                    <select :disabled="isReadOnly" style="width:100%;" class="form-select"
                        v-model="meeting_obj.meeting_type" @change="toggleAttendees(meeting_obj.meeting_type)">
                        <option v-for="option in meeting_type_list" :value="option.id" :key="option.id">
                            {{ option.display_name }}
                        </option>
                    </select>
                </div>
            </div>
            <div v-show="!isCommitteeMeeting" class="row mb-3">
                <label for="" class="col-sm-4 control-label fw-bold">Attendees: <span
                        class="text-danger">*</span></label>
                <div class="col-sm-8">
                    <input :disabled="isReadOnly" type="text" class="form-control" id="title" placeholder=""
                        v-model="meeting_obj.attendees" />
                </div>
            </div>
            <div v-show="isCommitteeMeeting">
                <div class="row mb-3">
                    <label for="" class="col-sm-4 control-label fw-bold">Committee: <span
                            class="text-danger">*</span></label>
                    <div class="col-sm-8">
                        <template v-if="!isReadOnly">
                            <template
                                v-if="committee_list && committee_list.length > 0 && meeting_obj.committee_id && !committee_list.map((d) => d.id).includes(meeting_obj.committee_id)">
                                <input type="text" v-if="meeting_obj.committee" class="form-control mb-3"
                                    :value="meeting_obj.committee + ' (Now Archived)'" disabled />
                                <div class="mb-3 text-muted">
                                    Change committee to:
                                </div>
                            </template>
                            <select class="form-select" v-model="meeting_obj.committee_id">
                                <option v-for="committee in committee_list" :value="committee.id" :key="committee.id">
                                    {{ committee.name }}
                                </option>
                            </select>
                        </template>
                        <template v-else>
                            <input class="form-control" type="text" :disabled="isReadOnly"
                                v-model="meeting_obj.committee" />
                        </template>
                    </div>
                </div>
                <div class="row mb-3">
                    <datatable ref="members_datatable" :id="panelBody" :dtOptions="members_options"
                        :dtHeaders="members_headers" />
                </div>
            </div>
            <div class="row mb-3">
                <label for="" class="col-sm-4 control-label fw-bold">Location: <span
                        class="text-danger">*</span></label>
                <div class="col-sm-8">
                    <select v-if="!isReadOnly" class="form-select" v-model="meeting_obj.location_id">
                        <option v-for="option in location_list" :value="option.id" :key="option.id">
                            {{ option.name }}
                        </option>
                    </select>
                    <input v-else type="text" readonly class="form-control" id="location" placeholder=""
                        v-model="meeting_obj.location" />
                </div>
            </div>
            <!-- <div class="row mb-3" v-if="meetingStatusEditable">
                <label for="" class="col-sm-4 control-label fw-bold">Meeting status: <span class="text-danger">*</span></label>
                <div class="col-sm-8">
                    <select :disabled="isReadOnly" style="width:100%;" class="form-select"
                        v-model="meeting_obj.processing_status">
                        <option v-for="option in status_list" :value="option.id" :key="option.id">
                            {{ option.display_name }}
                        </option>
                    </select>
                </div>
            </div> -->
        </FormSection>
    </div>
</template>

<script>

import datatable from '@vue-utils/datatable.vue';
import alert from '@vue-utils/alert.vue'
import FormSection from '@/components/forms/section_toggle.vue';


import {
    constants,
    api_endpoints,
    helpers,
}
    from '@/utils/hooks'
import { meeting } from '../../../api';
const calculateDefaultDate = () => {
    const now = new Date();
    now.setHours(9, 0, 0, 0);  // Set time to 9:00 AM

    const year = now.getFullYear();
    const month = String(now.getMonth() + 1).padStart(2, '0'); // Months are zero-indexed
    const day = String(now.getDate()).padStart(2, '0');
    const hours = String(now.getHours()).padStart(2, '0');
    const minutes = String(now.getMinutes()).padStart(2, '0');

    return `${year}-${month}-${day}T${hours}:${minutes}`;
};
const calculateDefaultEndDate = () => {
    const now = new Date();
    now.setHours(17, 0, 0, 0);  // Set time to 9:00 AM

    const year = now.getFullYear();
    const month = String(now.getMonth() + 1).padStart(2, '0'); // Months are zero-indexed
    const day = String(now.getDate()).padStart(2, '0');
    const hours = String(now.getHours()).padStart(2, '0');
    const minutes = String(now.getMinutes()).padStart(2, '0');

    return `${year}-${month}-${day}T${hours}:${minutes}`;
};
export default {
    name: 'MeetingSection',
    props: {
        meeting_obj: {
            type: Object,
            required: true
        },
        is_external: {
            type: Boolean,
            default: false
        },
        userCanEdit: {
            type: Boolean,
            default: true
        },
    },
    data: function () {
        let vm = this;
        return {
            datepickerOptions: {
                format: 'DD/MM/YYYY',
                showClear: true,
                useCurrent: false,
                keepInvalid: true,
                allowInputToggle: true,
            },
            start_date: calculateDefaultDate(),
            end_date: calculateDefaultEndDate(),
            isMeetingDateValid: true,
            isShowComment: false,
            isCommitteeMeeting: false,
            meetingStatusEditable: true,

            //----list of values dictionary
            meeting_dict: {},
            location_list: [],
            meeting_type_list: [],
            status_list: [],
            committee_list: [],
            committee_mem_arr: [],
            results: [],
            panelBody: "committee_members" + vm._uid,
            members_headers: ['id', 'First Name', 'Last Name', 'Email', 'Action'],
            members_options: {
                autowidth: true,
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
                order: [],
                dom: "<'d-flex align-items-center'<'me-auto'l>fB>" +
                    "<'row'<'col-sm-12'tr>>" +
                    "<'d-flex align-items-center'<'me-auto'i>p>",
                buttons: [
                ],
                columns: [
                    {
                        data: "id",
                        orderable: true,
                        searchable: true,
                        visible: false,
                        mRender: function (data, type, full) {
                            return full.id;
                        },

                    },
                    {
                        data: "first_name",
                        orderable: true,
                        searchable: true,
                        mRender: function (data, type, full) {
                            return full.first_name;
                        },

                    },
                    {
                        data: "last_name",
                        orderable: true,
                        searchable: true,
                        mRender: function (data, type, full) {
                            return full.last_name;
                        },
                    },
                    {
                        data: "email",
                        orderable: true,
                        searchable: true,
                        'render': function (value, type, full) {
                            let result = helpers.dtPopover(value, 30, 'hover');
                            return type == 'export' ? value : result;
                        },
                    },
                    {
                        data: "id",
                        mRender: function (data, type, full) {
                            let links = '';
                            if (vm.meeting_obj.sel_committee_members_arr && vm.meeting_obj.sel_committee_members_arr.includes(full.id)) {
                                return `<a href='#${full.id}' data-remove-member='${full.id}'>Remove</a><br/>`;
                            }
                            else {
                                return `<a href='#${full.id}' data-add-member='${full.id}'>Add</a><br/>`;
                            }
                        }
                    },
                ],
                processing: true,
                drawCallback: function () {
                    helpers.enablePopovers();
                },
                initComplete: function () {
                    helpers.enablePopovers();
                },
            }
        }
    },
    components: {
        FormSection,
        datatable,
        alert
    },
    computed: {
        isStatusDraft: function () {
            return this.meeting_obj.processing_status == "draft" ? true : false;
        },
        isReadOnly: function () {
            return !this.userCanEdit;
        },
    },
    watch: {
        // to fix the dateformat error when select to clear the date (ie. "") string value
        // "meeting_obj.start_date": function (newVal) {
        //     let vm = this;
        //     var selectedValue = newVal;
        //     if (selectedValue === "") {
        //         vm.meeting_obj.start_date = null;
        //     }
        // },
        // "meeting_obj.end_date": function (newVal) {
        //     let vm = this;
        //     var selectedValue = newVal;
        //     if (selectedValue === "") {
        //         vm.meeting_obj.end_date = null;
        //     }
        // },
        start_date: function (newVal) {
            let vm = this;
            console.log(newVal, vm.meeting_obj.start_date)
            var selectedValue = newVal;
            if (selectedValue === "") {
                vm.meeting_obj.start_date = null;
            }
            else {
                vm.meeting_obj.start_date = vm.start_date;
                // if(vm.meeting_obj.end_date=='' || vm.meeting_obj.end_date==null ){
                //     vm.end_date=vm.start_date;
                // }
                vm.end_date = vm.start_date;
            }
        },
        end_date: function (newVal) {
            let vm = this;
            var selectedValue = newVal;
            if (selectedValue === "") {
                vm.meeting_obj.end_date = null;
            }
            else {
                vm.meeting_obj.end_date = vm.end_date;
            }
        },
    },
    methods: {
        eventListeners: function () {
            let vm = this;
            vm.$refs.members_datatable.vmDataTable.on('childRow.dt', function (e, settings) {
                helpers.enablePopovers();
            });
        },
        //  render only once onload if meeting_obj.selected_committee_members>0 i.e previous sumbitted members
        renderExistsSelectedMembersTable: function () {
            let vm = this;
            vm.$http.get(`/api/committee/${vm.meeting_obj.committee_id}/committee_members`).then(res => {
                vm.results = res.body;
                if (vm.meeting_obj.selected_committee_members.length > 0) {
                    vm.meeting_obj.sel_committee_members_arr = [];
                    vm.meeting_obj.sel_committee_members_arr = vm.meeting_obj.selected_committee_members;
                }
                vm.$refs.members_datatable.vmDataTable.clear()
                vm.$refs.members_datatable.vmDataTable.rows.add(vm.results);
                vm.$refs.members_datatable.vmDataTable.draw();
            },
                err => {
                    console.log(err);
                });
        },
        // render on change of comittee and also on new meeting form
        renderMembersTable: function (add) {
            let vm = this;
            let committee_id = vm.meeting_obj.committee_id;
            if (committee_id === null) {
                vm.meeting_obj.sel_committee_members_arr = [];
                vm.$refs.members_datatable.vmDataTable.clear()
                vm.$refs.members_datatable.vmDataTable.draw();
            }
            else {
                vm.$http.get(`/api/committee/${vm.meeting_obj.committee_id}/committee_members`).then(res => {
                    vm.results = res.body;
                    //-- only get members onchange of committee and not when only one member added by add btn
                    if (add === undefined) {
                        // empty the previous selection
                        vm.meeting_obj.sel_committee_members_arr = [];
                        //to store all members of committee in array for further use
                        for (var i = 0; i < vm.results.length; i++) {
                            vm.meeting_obj.sel_committee_members_arr.push(vm.results[i].id);
                        }
                    }
                    vm.$refs.members_datatable.vmDataTable.clear()
                    vm.$refs.members_datatable.vmDataTable.rows.add(vm.results);
                    vm.$refs.members_datatable.vmDataTable.draw();
                },
                    err => {
                        console.log(err);
                    });
            }
        },
        toggleAttendees: function (id) {
            let vm = this;
            if (id === 'committee_meeting') {
                vm.isCommitteeMeeting = true;
            }
            else {
                vm.meeting_obj.committee_id = null;
                vm.meeting_obj.sel_committee_members_arr = [];
                vm.isCommitteeMeeting = false;
            }
        },
        eventListeners: function () {
            let vm = this;
            vm.$refs.members_datatable.vmDataTable.on('click', 'a[data-remove-member]', function (e) {
                e.preventDefault();
                let id = $(this).attr('data-remove-member');
                let mem_arr = vm.meeting_obj.sel_committee_members_arr;
                //---remove document id from array (for this arr.splice is used)
                let index = mem_arr.indexOf(parseInt(id)); // need to parse the id to int as the array is integer array
                vm.meeting_obj.sel_committee_members_arr.splice(index, 1);
                vm.$refs.members_datatable.vmDataTable.row($(this).parents('tr')).remove().draw();
            });
            vm.$refs.members_datatable.vmDataTable.on('click', 'a[data-add-member]', function (e) {
                e.preventDefault();
                let id = $(this).attr('data-add-member');
                if (!vm.meeting_obj.sel_committee_members_arr) {
                    vm.meeting_obj.sel_committee_members_arr = [];
                }
                vm.meeting_obj.sel_committee_members_arr.push(parseInt(id));
                //--to add only the requested memvbr to the sel_committee_members_arr
                vm.renderMembersTable('add');
            });
        },
        validateMeetingDate: function () {
            if (this.meeting_obj.start_date && this.meeting_obj.end_date) {
                const startDate = new Date(this.meeting_obj.start_date);
                const endDate = new Date(this.meeting_obj.end_date);
                this.isMeetingDateValid = startDate <= endDate;
            }
            else {
                this.isMeetingDateValid = true;
            }
        },
        hideActionColumn: function () {
            // this method is used to hide the action colmn whem processing_status is completed
            let vm = this;
            if (vm.isReadOnly == true) {
                vm.$refs.members_datatable.vmDataTable.column([4]).visible(false);
            }
        },
        setMeetingDates: function () {
            let vm = this;
            if (vm.meeting_obj.start_date) {
                vm.start_date = vm.meeting_obj.start_date;
            }
            if (vm.meeting_obj.end_date) {
                vm.end_date = vm.meeting_obj.end_date;
            }
        },
    },
    created: async function () {
        let vm = this;
        //------fetch list of values
        vm.$http.get(api_endpoints.meeting_dict).then((response) => {
            vm.meeting_dict = response.body;
            if (vm.meeting_obj.processing_status == 'completed') {
                vm.meetingStatusEditable = false;
            }
            //--meeting room list
            vm.location_list = vm.meeting_dict.location_list;
            vm.location_list.splice(0, 0,
                {
                    id: null,
                    name: null,
                });
            vm.committee_list = vm.meeting_dict.committee_list;
            vm.committee_list.splice(0, 0,
                {
                    id: null,
                    name: null,
                });
            //--meeting type list
            vm.meeting_type_list = vm.meeting_dict.meeting_type_list;
            //--status choices list
            vm.status_list = vm.meeting_dict.status_list;
            vm.toggleAttendees(vm.meeting_obj.meeting_type)
            if (vm.meeting_obj.committee_id != null) {
                vm.renderExistsSelectedMembersTable();
            }
            else {
                vm.renderMembersTable();
            }
        }, (error) => {
            console.log(error);
        })
    },
    mounted: function () {
        let vm = this;

        this.$nextTick(() => {
            vm.eventListeners();
            vm.hideActionColumn();
        });
        vm.setMeetingDates();
    }
}
</script>
