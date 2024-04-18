<template lang="html">
    <div v-if="occurrence_report" class="container" id="internal-occurence-report-detail">
        <div class="row">
            <div class="col">
                <h3 class="mb-1">Occurrence Report: {{ occurrence_report.occurrence_report_number }}</h3>
                <h4 class="text-muted mb-3">
                    Occurrence:
                    <template v-if="occurrence_report.occurrence">
                        {{ occurrence_report.occurrence.occurrence_number }} <small><a
                                :href="`/internal/occurrence/${occurrence_report.occurrence.id}?group_type_name=${occurrence_report.group_type}&action=view`"
                                target="_blank"><i class="bi bi-box-arrow-up-right"></i></a></small>
                    </template>
                    <template v-else>
                        NOT SET
                    </template>
                </h4>
            </div>
        </div>
        <div class="row pb-4">
            <div v-if="!comparing" class="col-md-3">

                <CommsLogs :comms_url="comms_url" :logs_url="logs_url" :comms_add_url="comms_add_url"
                    :disable_add_entry="false" class="mb-3" />

                <Submission v-if="canSeeSubmission" :submitter_first_name="submitter_first_name"
                    :submitter_last_name="submitter_last_name" :lodgement_date="occurrence_report.lodgement_date"
                    class="mb-3" />

                <div class="card card-default sticky-top">
                    <div class="card-header">
                        Workflow
                    </div>
                    <div class="card-body border-bottom">
                        <strong>Status</strong><br />
                        {{ occurrence_report.processing_status }}
                    </div>
                    <div class="card-body">
                        <div class="mb-2"><strong>Currently assigned to</strong></div>
                        <template v-if="occurrence_report.processing_status == 'With Approver'">
                            <select ref="assigned_officer" :disabled="!hasUserEditMode" class="form-select mb-2"
                                v-model="occurrence_report.assigned_approver">
                                <option v-for="member in occurrence_report.allowed_assessors" :value="member.id">
                                    {{ member.first_name }} {{ member.last_name }}</option>
                            </select>
                            <a v-if="occurrence_report.processing_status == 'With Approver' && occurrence_report.assigned_approver != occurrence_report.current_assessor.id"
                                @click.prevent="assignRequestUser()" class="actionBtn float-end">Assign to me</a>
                        </template>
                        <template v-else>
                            <select ref="assigned_officer" :disabled="!hasUserEditMode" class="form-select mb-2"
                                v-model="occurrence_report.assigned_officer">
                                <option v-for="member in occurrence_report.allowed_assessors" :value="member.id">
                                    {{ member.first_name }} {{ member.last_name }}</option>
                            </select>
                            <a v-if="occurrence_report.processing_status == 'With Assessor' && occurrence_report.assigned_officer != occurrence_report.current_assessor.id"
                                @click.prevent="assignRequestUser()" class="actionBtn float-end" role="button">Assign to
                                me</a>
                        </template>
                    </div>
                    <div v-if="isAssignedOfficer" class="card-body border-top">
                        <div class="mb-2"><strong>Referrals</strong></div>
                        <select class="form-select mb-2" placeholder="Select a referee">
                            <option value="">Unassigned</option>
                            <option value="1">User 1</option>
                        </select>
                        <a href="">Show referrals</a>
                    </div>
                    <div v-if="canAction" class="card-body border-top">
                        <div class="mb-3">
                            <strong>Actions</strong>
                        </div>
                        <div class="text-center">
                            <button style="width:80%;" class="btn btn-primary mb-2"
                                @click.prevent="">Approve</button><br />
                            <button style="width:80%;" class="btn btn-primary mb-2" @click.prevent="amendmentRequest()">Request
                                Amendment</button><br />
                            <button style="width:80%;" class="btn btn-primary mb-2"
                                @click.prevent="splitSpecies()">Split</button><br />
                            <button style="width:80%;" class="btn btn-primary mb-2"
                                @click.prevent="discardSpeciesProposal()">Discard</button>
                        </div>
                    </div>
                </div>
            </div>
            <div class="col-md-9">
                <template>
                    <form :action="occurrence_report_form_url" method="post" name="occurrence_report"
                        enctype="multipart/form-data">
                        <ProposalOccurrenceReport v-if="occurrence_report" :occurrence_report_obj="occurrence_report"
                            id="OccurrenceReportStart" :canEditStatus="false" :is_external="true"
                            ref="occurrence_report" @refreshFromResponse="refreshFromResponse">
                        </ProposalOccurrenceReport>

                        <input type="hidden" name="csrfmiddlewaretoken" :value="csrf_token" />
                        <input type='hidden' name="occurrence_report_id" :value="1" />
                        <div class="row" style="margin-bottom: 50px">
                            <div class="navbar fixed-bottom" style="background-color: #f5f5f5;">
                                <div v-if="hasUserEditMode" class="container">
                                    <div class="col-md-12 text-end">
                                        <button v-if="savingOccurrenceReport" class="btn btn-primary me-2"
                                            style="margin-top:5px;" disabled>Save and Continue&nbsp;
                                            <i class="fa fa-circle-o-notch fa-spin fa-fw"></i></button>
                                        <button v-else class="btn btn-primary me-2" style="margin-top:5px;"
                                            @click.prevent="save()"
                                            :disabled="saveExitOccurrenceReport || submitOccurrenceReport">Save
                                            and Continue</button>

                                        <button v-if="saveExitOccurrenceReport" class="btn btn-primary me-2"
                                            style="margin-top:5px;" disabled>Save and Exit&nbsp;
                                            <i class="fa fa-circle-o-notch fa-spin fa-fw"></i></button>
                                        <button v-else class="btn btn-primary me-2" style="margin-top:5px;"
                                            @click.prevent="save_exit()"
                                            :disabled="savingOccurrenceReport || submitOccurrenceReport">Save
                                            and Exit</button>

                                        <button v-if="submitOccurrenceReport" class="btn btn-primary"
                                            style="margin-top:5px;" disabled>Submit&nbsp;
                                            <i class="fa fa-circle-o-notch fa-spin fa-fw"></i></button>
                                        <button v-else class="btn btn-primary" style="margin-top:5px;"
                                            @click.prevent="submit()"
                                            :disbaled="saveExitOccurrenceReport || savingOccurrenceReport">Submit</button>
                                    </div>
                                </div>
                                <div v-else-if="hasUserEditMode" class="container">
                                    <div class="col-md-12 text-end">
                                        <button v-if="savingOccurrenceReport" class="btn btn-primary"
                                            style="margin-top:5px;" disabled>Save Changes&nbsp;
                                            <i class="fa fa-circle-o-notch fa-spin fa-fw"></i></button>
                                        <button v-else class="btn btn-primary" style="margin-top:5px;"
                                            @click.prevent="save()">Save
                                            Changes</button>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </form>
                </template>
            </div>
        </div>

        <AmendmentRequest ref="amendment_request" :occurrence_report_id="occurrence_report.id" @refreshFromResponse="refreshFromResponse"></AmendmentRequest>
    </div>
    <!-- <SpeciesSplit ref="species_split" :occurrence_report="occurrence_report" :is_internal="true"
            @refreshFromResponse="refreshFromResponse" />
        <SpeciesCombine ref="species_combine" :occurrence_report="occurrence_report" :is_internal="true"
            @refreshFromResponse="refreshFromResponse" />
        <SpeciesRename ref="species_rename" :occurrence_report_original="occurrence_report" :is_internal="true"
            @refreshFromResponse="refreshFromResponse" /> -->

</template>
<script>
import Vue from 'vue'
import datatable from '@vue-utils/datatable.vue'
import CommsLogs from '@common-utils/comms_logs.vue'
import Submission from '@common-utils/submission.vue'
import Workflow from '@common-utils/workflow.vue'
import ProposalOccurrenceReport from '@/components/form_occurrence_report.vue'
import AmendmentRequest from './amendment_request.vue'

// import SpeciesSplit from './species_split.vue'
// import SpeciesCombine from './species_combine.vue'
// import SpeciesRename from './species_rename.vue'

import {
    api_endpoints,
    helpers
}
    from '@/utils/hooks'
export default {
    name: 'InternalOccurrenceReportDetail',
    data: function () {
        let vm = this;
        return {
            occurrence_report: null,
            original_occurrence_report: null,
            initialisedSelects: false,
            form: null,
            savingOccurrenceReport: false,
            saveExitOccurrenceReport: false,
            submitOccurrenceReport: false,
            imageURL: '',
            isSaved: false,
            DATE_TIME_FORMAT: 'DD/MM/YYYY HH:mm:ss',
            comparing: false,
        }
    },
    components: {
        datatable,
        CommsLogs,
        Submission,
        Workflow,
        ProposalOccurrenceReport,
        AmendmentRequest,
        // SpeciesSplit,
        // SpeciesCombine,
        // SpeciesRename,
    },
    filters: {
        formatDate: function (data) {
            return data ? moment(data).format('DD/MM/YYYY HH:mm:ss') : '';
        }
    },
    computed: {
        csrf_token: function () {
            return helpers.getCookie('csrftoken')
        },
        isCommunity: function () {
            return this.occurrence_report && this.occurrence_report.group_type === "community"
        },
        occurrence_report_form_url: function () {
            return (this.occurrence_report.group_type === "community") ?
                `/api/community/${this.occurrence_report.id}/community_save.json` :
                `/api/species/${this.occurrence_report.id}/species_save.json`;
        },
        occurrence_report_submit_url: function () {
            return (this.occurrence_report.group_type === "community") ?
                `community` :
                `species`;
        },
        display_group_type: function () {
            let group_type_string = this.occurrence_report.group_type
            // to Capitalize only first character
            return group_type_string.charAt(0).toUpperCase() + group_type_string.slice(1);
        },
        display_number: function () {
            return (this.occurrence_report.group_type === "community") ?
                this.occurrence_report.community_number :
                this.occurrence_report.species_number;
        },
        display_name: function () {
            return (this.occurrence_report.group_type === "community") ?
                (this.occurrence_report.taxonomy_details != null) ? this.occurrence_report.taxonomy_details.community_migrated_id : '' :
                (this.occurrence_report.taxonomy_details != null) ? this.occurrence_report.taxonomy_details.scientific_name + " (" + this.occurrence_report.taxonomy_details.taxon_name_id + ")" : '';
        },
        submitter_first_name: function () {
            if (this.occurrence_report && this.occurrence_report.submitter) {
                return this.occurrence_report.submitter.first_name
            } else {
                return ''
            }
        },
        submitter_last_name: function () {
            if (this.occurrence_report && this.occurrence_report.submitter) {
                return this.occurrence_report.submitter.last_name
            } else {
                return ''
            }
        },
        canSeeSubmission: function () {
            //return this.proposal && (this.proposal.processing_status != 'With Assessor (Requirements)' && this.proposal.processing_status != 'With Approver' && !this.isFinalised)
            //return this.proposal && (this.proposal.processing_status != 'With Assessor (Requirements)')
            return true
        },
        hasUserEditMode: function () {
            // Need to check for approved status as to show 'Save changes' button only when edit and not while view
            if (['process'].includes(this.$route.query.action)) {
                return this.occurrence_report && this.occurrence_report.can_user_edit;
            }
            else {
                return false;
            }
        },
        isAssignedOfficer: function () {
            return this.occurrence_report && this.occurrence_report.assigned_officer == this.occurrence_report.current_assessor.id;
        },
        isAssignedApprover: function () {
            return this.occurrence_report && this.occurrence_report.assigned_approver == this.occurrence_report.current_assessor.id;
        },
        canAction: function () {
            return this.occurrence_report && this.occurrence_report.can_user_action;
        },
        canDiscard: function () {
            return this.occurrence_report && this.occurrence_report.processing_status === "Draft" ? true : false;
        },
        comms_url: function () {
            return helpers.add_endpoint_json(api_endpoints.occurrence_report, this.$route.params.occurrence_report_id + '/comms_log')
        },
        comms_add_url: function () {
            return helpers.add_endpoint_json(api_endpoints.occurrence_report, this.$route.params.occurrence_report_id + '/add_comms_log')
        },
        logs_url: function () {
            return helpers.add_endpoint_json(api_endpoints.occurrence_report, this.$route.params.occurrence_report_id + '/action_log')
        },
    },
    methods: {
        discardSpeciesProposal: function () {
            let vm = this;
            swal.fire({
                title: "Discard Application",
                text: "Are you sure you want to discard this proposal?",
                icon: "warning",
                showCancelButton: true,
                confirmButtonText: 'Discard Application',
                confirmButtonColor: '#d9534f'
            }).then((swalresult) => {
                if (swalresult.isConfirmed) {
                    vm.$http.delete(api_endpoints.discard_species_proposal(vm.occurrence_report.id))
                        .then((response) => {
                            swal.fire({
                                title: 'Discarded',
                                text: 'Your proposal has been discarded',
                                icon: 'success',
                                confirmButtonColor: '#226fbb',
                            });
                            vm.$router.push({
                                name: 'internal-species-communities-dash'
                            });
                        }, (error) => {
                            console.log(error);
                        });
                }
            }, (error) => {

            });
        },
        amendmentRequest: function(){
            this.$refs.amendment_request.isModalOpen = true;
        },
        save: async function () {
            let vm = this;
            var missing_data = vm.can_submit("");
            vm.isSaved = false;
            if (missing_data != true) {
                swal.fire({
                    title: "Please fix following errors before saving",
                    text: missing_data,
                    icon: 'error',
                    confirmButtonColor: '#226fbb'
                })
                return false;
            }
            vm.savingOccurrenceReport = true;
            let payload = new Object();
            Object.assign(payload, vm.occurrence_report);
            await vm.$http.post(vm.occurrence_report_form_url, payload).then(res => {
                swal.fire({
                    title: "Saved",
                    text: "Your changes has been saved",
                    icon: "success",
                    confirmButtonColor: '#226fbb'
                });
                vm.savingOccurrenceReport = false;
                vm.isSaved = true;
            }, err => {
                var errorText = helpers.apiVueResourceError(err);
                swal.fire({
                    title: 'Save Error',
                    text: errorText,
                    icon: 'error',
                    confirmButtonColor: '#226fbb'
                });
                vm.savingOccurrenceReport = false;
                vm.isSaved = false;
            });
        },
        save_exit: async function (e) {
            let vm = this;
            var missing_data = vm.can_submit("");
            if (missing_data != true) {
                swal.fire({
                    title: "Please fix following errors before saving",
                    text: missing_data,
                    icon: 'error',
                    confirmButtonColor: '#226fbb'
                })
                //vm.paySubmitting=false;
                return false;
            }
            vm.saveExitOccurrenceReport = true;
            await vm.save().then(() => {
                if (vm.isSaved === true) {
                    vm.$router.push({
                        name: 'internal-species-communities-dash'
                    });
                }
                else {
                    vm.saveExitOccurrenceReport = false;
                }
            });
        },
        save_before_submit: async function (e) {
            //console.log('save before submit');
            let vm = this;
            vm.saveError = false;

            let payload = new Object();
            Object.assign(payload, vm.occurrence_report);
            const result = await vm.$http.post(vm.occurrence_report_form_url, payload).then(res => {
                //return true;
            }, err => {
                var errorText = helpers.apiVueResourceError(err);
                swal.fire({
                    title: 'Submit Error',
                    //helpers.apiVueResourceError(err),
                    text: errorText,
                    icon: 'error',
                    confirmButtonColor: '#226fbb'
                })
                vm.submitOccurrenceReport = false;
                vm.saveError = true;
                //return false;
            });
            return result;
        },
        can_submit: function (check_action) {
            let vm = this;
            let blank_fields = []
            if (vm.occurrence_report.group_type == 'flora' || vm.occurrence_report.group_type == 'fauna') {
                if (vm.occurrence_report.taxonomy_id == null || vm.occurrence_report.taxonomy_id == '') {
                    blank_fields.push('Scientific Name is missing')
                }
            }
            else {
                if (vm.occurrence_report.taxonomy_details.community_name == null || vm.occurrence_report.taxonomy_details.community_name == '') {
                    blank_fields.push('Community Name is missing')
                }
            }
            if (check_action == 'submit') {
                //TODO add validation for fields required before submit
            }
            if (blank_fields.length == 0) {
                return true;
            }
            else {
                return blank_fields;
            }
        },
        submit: async function () {
            let vm = this;

            var missing_data = vm.can_submit("submit");
            if (missing_data != true) {
                swal.fire({
                    title: "Please fix following errors before submitting",
                    text: missing_data,
                    icon: 'error',
                    confirmButtonColor: '#226fbb'
                })
                //vm.paySubmitting=false;
                return false;
            }

            vm.submitOccurrenceReport = true;
            swal.fire({
                title: "Submit",
                text: "Are you sure you want to submit this application?",
                icon: "question",
                showCancelButton: true,
                confirmButtonText: "submit",
                confirmButtonColor: '#226fbb'
            }).then(async (swalresult) => {
                if (swalresult.isConfirmed) {
                    let result = await vm.save_before_submit()
                    if (!vm.saveError) {
                        let payload = new Object();
                        Object.assign(payload, vm.occurrence_report);
                        let submit_url = this.occurrence_report.group_type === "community" ?
                            helpers.add_endpoint_json(api_endpoints.community, vm.occurrence_report.id + '/submit') :
                            helpers.add_endpoint_json(api_endpoints.species, vm.occurrence_report.id + '/submit')
                        vm.$http.post(submit_url, payload).then(res => {
                            vm.occurrence = res.body;
                            // vm.$router.push({
                            //     name: 'submit_cs_proposal',
                            //     params: { occurrence_report: vm.occurrence_report}
                            // });
                            // TODO router should push to submit_cs_proposal for internal side
                            vm.$router.push({
                                name: 'internal-species-communities-dash'
                            });
                        }, err => {
                            swal.fire({
                                title: 'Submit Error',
                                text: helpers.apiVueResourceError(err),
                                icon: 'error',
                                confirmButtonColor: '#226fbb'
                            });
                        });
                    }
                }
            }, (error) => {
                vm.submitOccurrenceReport = false;
            });
        },
        refreshFromResponse: function (response) {
            let vm = this;
            vm.original_occurrence = helpers.copyObject(response.body);
            vm.occurrence_report = helpers.copyObject(response.body);
        },
        splitSpecies: async function () {
            this.$refs.species_split.occurrence_original = this.occurrence_report;
            let newSpeciesId1 = null
            try {
                const createUrl = api_endpoints.species + "/";
                let payload = new Object();
                payload.group_type_id = this.occurrence_report.group_type_id;
                let savedSpecies = await Vue.http.post(createUrl, payload);
                if (savedSpecies) {
                    newSpeciesId1 = savedSpecies.body.id;
                    Vue.http.get(`/api/species/${newSpeciesId1}/internal_species.json`).then(res => {
                        let species_obj = res.body.species_obj;
                        //--- to add empty documents array
                        species_obj.documents = []
                        //---empty threats array added to store the select threat ids in from the child component
                        species_obj.threats = []
                        this.$refs.species_split.occurrence_list.push(species_obj); //--temp species_obj
                    },
                        err => {
                            console.log(err);
                        });
                }
            }
            catch (err) {
                console.log(err);
                if (this.is_internal) {
                    return err;
                }
            }
            let newSpeciesId2 = null
            try {
                const createUrl = api_endpoints.species + "/";
                let payload = new Object();
                payload.group_type_id = this.occurrence_report.group_type_id
                let savedSpecies = await Vue.http.post(createUrl, payload);
                if (savedSpecies) {
                    newSpeciesId2 = savedSpecies.body.id;
                    Vue.http.get(`/api/species/${newSpeciesId2}/internal_species.json`).then(res => {
                        let species_obj = res.body.species_obj;
                        // to add documents id array from original species
                        species_obj.documents = []
                        //---empty threats array added to store the select threat ids in from the child component
                        species_obj.threats = []
                        this.$refs.species_split.occurrence_list.push(species_obj); //--temp species_obj
                    },
                        err => {
                            console.log(err);
                        });
                }
            }
            catch (err) {
                console.log(err);
                if (this.is_internal) {
                    return err;
                }
            }
            this.$refs.species_split.isModalOpen = true;
        },
        combineSpecies: async function () {
            this.$refs.species_combine.original_species_combine_list.push(this.occurrence_report); //--push current original into the array
            let newSpeciesId = null
            try {
                const createUrl = api_endpoints.species + "/";
                let payload = new Object();
                payload.group_type_id = this.occurrence_report.group_type_id;
                let savedSpecies = await Vue.http.post(createUrl, payload);
                if (savedSpecies) {
                    newSpeciesId = savedSpecies.body.id;
                    Vue.http.get(`/api/species/${newSpeciesId}/internal_species.json`).then(res => {
                        let species_obj = res.body.species_obj;
                        //--- to add empty documents array
                        species_obj.documents = []
                        //---empty threats array added to store the selected threat ids in from the child component
                        species_obj.threats = []
                        this.$refs.species_combine.new_combine_species = species_obj; //---assign the new created species to the modal obj
                    },
                        err => {
                            console.log(err);
                        });
                }

            }
            catch (err) {
                console.log(err);
                if (this.is_internal) {
                    return err;
                }
            }
            this.$refs.species_combine.isModalOpen = true;
        },
        renameSpecies: async function () {
            let rename_species_obj = null;
            let newRenameSpecies = await Vue.http.get(`/api/species/${this.occurrence_report.id}/rename_deep_copy.json`)
            if (newRenameSpecies) {
                rename_species_obj = newRenameSpecies.body.species_obj;
                this.$refs.species_rename.new_rename_species = rename_species_obj;
                this.$refs.species_rename.isModalOpen = true;
            }
        },
        initialiseSelects: function () {
            let vm = this;
            if (!vm.initialisedSelects) {
                $(vm.$refs.department_users).select2({
                    minimumInputLength: 2,
                    "theme": "bootstrap-5",
                    allowClear: true,
                    placeholder: "Select Referrer",
                    ajax: {
                        url: api_endpoints.users_api + '/get_department_users/',
                        dataType: 'json',
                        data: function (params) {
                            var query = {
                                term: params.term,
                                type: 'public',
                            }
                            return query;
                        },
                    },
                })
                    .on("select2:select", function (e) {
                        let data = e.params.data.id;
                        vm.selected_referral = data;
                    })
                    .on("select2:unselect", function (e) {
                        var selected = $(e.currentTarget);
                        vm.selected_referral = null;
                    })
                vm.initialiseAssignedOfficerSelect();
                vm.initialisedSelects = true;
            }
        },
        initialiseAssignedOfficerSelect: function (reinit = false) {
            let vm = this;
            if (reinit) {
                $(vm.$refs.assigned_officer).data('select2') ? $(vm.$refs.assigned_officer).select2('destroy') : '';
            }
            // Assigned officer select
            $(vm.$refs.assigned_officer).select2({
                "theme": "bootstrap-5",
                allowClear: true,
                placeholder: "Unassigned"
            }).
                on("select2:select", function (e) {
                    var selected = $(e.currentTarget);
                    if (vm.occurrence_report.processing_status == 'With Approver') {
                        vm.occurrence_report.assigned_approver = selected.val();
                    }
                    else {
                        vm.occurrence_report.assigned_officer = selected.val();
                    }
                    vm.assignTo();
                }).on("select2:unselecting", function (e) {
                    var self = $(this);
                    setTimeout(() => {
                        self.select2('close');
                    }, 0);
                }).on("select2:unselect", function (e) {
                    var selected = $(e.currentTarget);
                    if (vm.occurrence_report.processing_status == 'With Approver') {
                        vm.occurrence_report.assigned_approver = null;
                    }
                    else {
                        vm.occurrence_report.assigned_officer = null;
                    }
                    vm.assignTo();
                });
        },
        updateAssignedOfficerSelect: function () {
            let vm = this;
            if (vm.occurrence_report.processing_status == 'With Approver') {
                $(vm.$refs.assigned_officer).val(vm.occurrence_report.assigned_approver);
                $(vm.$refs.assigned_officer).trigger('change');
            }
            else {
                $(vm.$refs.assigned_officer).val(vm.occurrence_report.assigned_officer);
                $(vm.$refs.assigned_officer).trigger('change');
            }
        },
        assignTo: function () {
            let vm = this;
            let unassign = true;
            let data = {};
            if (vm.occurrence_report.processing_status == 'With Approver') {
                unassign = vm.occurrence_report.assigned_approver != null && vm.occurrence_report.assigned_approver != 'undefined' ? false : true;
                data = { 'assessor_id': vm.occurrence_report.assigned_approver };
            }
            else {
                unassign = vm.occurrence_report.assigned_officer != null && vm.occurrence_report.assigned_officer != 'undefined' ? false : true;
                data = { 'assessor_id': vm.occurrence_report.assigned_officer };
            }
            if (!unassign) {
                vm.$http.post(helpers.add_endpoint_json(api_endpoints.occurrence_report, (vm.occurrence_report.id + '/assign_to')), JSON.stringify(data), {
                    emulateJSON: true
                }).then((response) => {
                    vm.occurrence_report = response.body;
                    vm.original_occurrence_report = helpers.copyObject(response.body);
                    vm.updateAssignedOfficerSelect();
                }, (error) => {
                    vm.occurrence_report = helpers.copyObject(vm.original_occurrence_report)
                    vm.updateAssignedOfficerSelect();
                    swal.fire({
                        title: 'Application Error',
                        text: helpers.apiVueResourceError(error),
                        icon: 'error',
                        confirmButtonColor: '#226fbb'
                    });
                });
            }
            else {
                vm.$http.get(helpers.add_endpoint_json(api_endpoints.occurrence_report, (vm.occurrence_report.id + '/unassign')))
                    .then((response) => {
                        vm.occurrence_report = response.body;
                        vm.original_occurrence_report = helpers.copyObject(response.body);
                        vm.updateAssignedOfficerSelect();
                    }, (error) => {
                        vm.occurrence_report = helpers.copyObject(vm.original_occurrence_report)
                        vm.updateAssignedOfficerSelect();
                        swal.fire({
                            title: 'Application Error',
                            text: helpers.apiVueResourceError(error),
                            icon: 'error',
                            confirmButtonColor: '#226fbb'
                        });
                    });
            }
        },
        assignRequestUser: function () {
            let vm = this;
            vm.$http.get(helpers.add_endpoint_json(api_endpoints.occurrence_report, (vm.occurrence_report.id + '/assign_request_user')))
                .then((response) => {
                    vm.occurrence_report = response.body;
                    vm.original_occurrence_report = helpers.copyObject(response.body);
                    vm.updateAssignedOfficerSelect();

                }, (error) => {
                    vm.occurrence_report = helpers.copyObject(vm.original_occurrence_report)
                    vm.updateAssignedOfficerSelect();
                    swal.fire({
                        title: 'Application Error',
                        text: helpers.apiVueResourceError(error),
                        icon: 'error',
                        confirmButtonColor: '#226fbb'
                    });
                });
        },
    },
    updated: function () {
        let vm = this;
        this.$nextTick(() => {
            vm.initialiseSelects();
            vm.form = document.forms.occurrence_report;
        });
    },
    beforeRouteEnter: function (to, from, next) {
            Vue.http.get(`/api/occurrence_report/${to.params.occurrence_report_id}/`).then(res => {
                next(vm => {
                    vm.occurrence_report = res.body;
                });
            },
                err => {
                    console.log(err);
                });
    },
}
</script>
