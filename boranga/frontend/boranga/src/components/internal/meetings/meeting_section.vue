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
            <div class="row mb-3">
                <label for="" class="col-sm-4 control-label fw-bold">Start Date/ Time: <span
                        class="text-danger">*</span></label>
                <div class="col-sm-8">
                    <input :disabled="isReadOnly" type="datetime-local" class="form-control" name="start_date"
                        ref="start_date" v-model="start_date" @change="validateMeetingDate()" />
                </div>
            </div>
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
                            <select class="form-select" v-model="meeting_obj.committee_id"
                                @change="committeeChanged">
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
                <div v-if="meeting_obj.committee_id && committee_members" class="row mb-3">
                    <label for="" class="col-sm-4 control-label fw-bold">Members Attending: <span
                            class="text-danger">*</span></label>
                    <div class="col-sm-8">
                        <template v-if="committee_members.length > 0">
                            <div class="border-bottom pb-2 mb-2">
                                <input id="all-members-attending" class="form-check-input me-2"
                                    v-model="all_members_attending" type="checkbox" :value="true"
                                    @click="toggleAllMembersAttending" />
                                <label class="form-check-label" for="all-members-attending"><i
                                        class="bi bi-people-fill h5"
                                        :class="all_members_attending ? 'text-primary' : 'text-secondary'"></i> All
                                    Members are
                                    Attending</label>
                            </div>
                            <div v-for="committee_member in committee_members" class="fs-6 mb-2">
                                <input :id="'member-' + committee_member.id" class="form-check-input me-2"
                                    type="checkbox" :value="committee_member.id"
                                    v-model="meeting_obj.selected_committee_members"
                                    @change="updateAllMembersAttending" />
                                <label class="form-check-label"
                                    :class="meeting_obj.selected_committee_members.includes(committee_member.id) ? '' : 'text-secondary'"
                                    :for="'member-' + committee_member.id"><i class="bi h5"
                                        :class="meeting_obj.selected_committee_members.includes(committee_member.id) ? 'bi-person-fill-check text-success' : 'bi-person-fill-dash text-secondary'"></i>
                                    {{
                                        committee_member.first_name
                                    }} {{
                                        committee_member.last_name }}</label>
                            </div>
                        </template>
                        <template v-else>
                            <div class="text-muted">No members found for this committee</div>
                        </template>
                    </div>
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
            isCommitteeMeeting: false,
            meetingStatusEditable: true,

            //----list of values dictionary
            meeting_dict: {},
            location_list: [],
            meeting_type_list: [],
            status_list: [],
            committee_list: [],
            committee_members: [],
            all_members_attending: false,
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
        start_date: function (newVal) {
            let vm = this;
            console.log(newVal, vm.meeting_obj.start_date)
            var selectedValue = newVal;
            if (selectedValue === "") {
                vm.meeting_obj.start_date = null;
            }
            else {
                vm.meeting_obj.start_date = vm.start_date;
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
        toggleAttendees: function (id) {
            let vm = this;
            if (id === 'committee_meeting') {
                vm.isCommitteeMeeting = true;
                vm.fetchCommitteeMembers()
            }
            else {
                vm.meeting_obj.committee_id = null;
                vm.isCommitteeMeeting = false;
                vm.committee_members = [];
                vm.meeting_obj.selected_committee_members = [];
            }
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
        setMeetingDates: function () {
            let vm = this;
            if (vm.meeting_obj.start_date) {
                vm.start_date = vm.meeting_obj.start_date;
            }
            if (vm.meeting_obj.end_date) {
                vm.end_date = vm.meeting_obj.end_date;
            }
        },
        fetchCommitteeMembers: function () {
            let vm = this;
            if (vm.meeting_obj.committee_id) {
                vm.$http.get(api_endpoints.committee_members(vm.meeting_obj.committee_id)).then((response) => {
                    vm.committee_members = response.body;
                    if (vm.meeting_obj.selected_committee_members.length === vm.committee_members.length) {
                        vm.all_members_attending = true;
                    }
                }, (error) => {
                    console.log(error);
                })
            }
        },
        toggleAllMembersAttending: function () {
            let vm = this;
            if (vm.meeting_obj.selected_committee_members.length === vm.committee_members.length) {
                vm.meeting_obj.selected_committee_members = [];
            }
            else {
                vm.meeting_obj.selected_committee_members = vm.committee_members.map((d) => d.id);
            }
        },
        updateAllMembersAttending: function () {
            let vm = this;
            if (vm.meeting_obj.selected_committee_members.length === vm.committee_members.length) {
                vm.all_members_attending = true;
            }
            else {
                vm.all_members_attending = false;
            }
        },
        committeeChanged: function () {
            let vm = this;
            vm.meeting_obj.selected_committee_members = [];
            vm.all_members_attending = false;
            vm.fetchCommitteeMembers();
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
                    name: 'Select the Location for the Meeting',
                });
            vm.committee_list = vm.meeting_dict.committee_list;
            vm.committee_list.splice(0, 0,
                {
                    id: null,
                    name: 'Select the Committee for the Meeting',
                });
            //--meeting type list
            vm.meeting_type_list = vm.meeting_dict.meeting_type_list;
            //--status choices list
            vm.status_list = vm.meeting_dict.status_list;
            vm.toggleAttendees(vm.meeting_obj.meeting_type)
        }, (error) => {
            console.log(error);
        })
    },
    mounted: function () {
        let vm = this;
        vm.setMeetingDates();
    }
}
</script>
