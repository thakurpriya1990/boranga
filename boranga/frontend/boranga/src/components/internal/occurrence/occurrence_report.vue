<template lang="html">
    <div v-if="occurrence_report" class="container" id="internal-occurence-report-detail">
        <div class="row">
            <div class="col">
                <h3 class="mb-1">Occurrence Report: {{ occurrence_report.occurrence_report_number }} - <span
                        class="text-capitalize">{{ display_group_type }}</span></h3>
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
            <div class="col-md-3">

                <CommsLogs :comms_url="comms_url" :logs_url="logs_url" :comms_add_url="comms_add_url"
                    :disable_add_entry="false" class="mb-3" />

                <Submission v-if="canSeeSubmission" :submitter_first_name="submitter_first_name"
                    :submitter_last_name="submitter_last_name" :lodgement_date="occurrence_report.lodgement_date"
                    :is_new_contributor="occurrence_report.is_new_contributor"
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
                        <template v-if="with_approver">
                            <select ref="assigned_officer" :disabled="!occurrence_report.can_user_approve"
                                class="form-select mb-2" v-model="occurrence_report.assigned_approver">
                                <option v-for="member in occurrence_report.allowed_assessors" :value="member.id" :selected="member.id==occurrence_report.assigned_approver">
                                    {{ member.first_name }} {{ member.last_name }}</option>
                            </select>
                            <a v-if="with_approver && occurrence_report.assigned_approver != occurrence_report.current_assessor.id"
                                @click.prevent="assignRequestUser()" class="actionBtn float-end" role="button">Assign to
                                me</a>
                        </template>
                        <template v-else>
                            <select ref="assigned_officer" :disabled="!occurrence_report.can_user_assess"
                                class="form-select mb-2" v-model="occurrence_report.assigned_officer">
                                <option v-for="member in occurrence_report.allowed_assessors" :value="member.id" :selected="member.id==occurrence_report.current_assessor.id">
                                    {{ member.first_name }} {{ member.last_name }}</option>
                            </select>
                            <a v-if="(with_assessor || with_referral || unlocked) && occurrence_report.assigned_officer != occurrence_report.current_assessor.id"
                                @click.prevent="assignRequestUser()" class="actionBtn float-end" role="button">Assign to
                                me</a>
                        </template>
                    </div>
                    <div v-if="display_referral_actions" class="card-body border-top">
                        <div class="mb-2"><strong>Referrals</strong></div>
                        <div class="form-group mb-3">
                            <select :disabled="!canAction" ref="department_users" class="form-control">
                            </select>
                            <template v-if='!sendingReferral'>
                                <template v-if="selected_referral">
                                    <label class="control-label mt-3" for="referral_text">Comments</label>
                                    <textarea class="form-control" name="referral_text" ref="referral_text"
                                        v-model="referral_text"></textarea>
                                    <a v-if="canAction" @click.prevent="sendReferral()" class="actionBtn float-end mt-2"
                                        role="button">Send</a>
                                </template>
                            </template>
                            <template v-else>
                                <span v-if="canAction" @click.prevent="sendReferral()" disabled
                                    class="actionBtn text-primary float-end">
                                    Sending Referral&nbsp;
                                    <i class="fa fa-circle-o-notch fa-spin fa-fw"></i>
                                </span>
                            </template>
                        </div>
                    </div>
                    <div v-if="display_referral_actions &&
                        isAssignedOfficer &&
                        occurrence_report.latest_referrals &&
                        occurrence_report.latest_referrals.length > 0
                    " class="card-body border-top">
                        <div>
                            <div class="fw-bold mb-1">
                                Recent Referrals
                                <small class="text-secondary fw-lighter">(Showing {{
                                    occurrence_report.latest_referrals.length }} of
                                    {{ occurrence_report.referrals.length }})</small>
                            </div>
                            <table class="table table-sm table-hover table-referrals">
                                <thead>
                                    <tr>
                                        <th>Referee</th>
                                        <th>Status</th>
                                        <th>Actions</th>
                                    </tr>
                                </thead>
                                <tbody>
                                    <tr v-for="r in occurrence_report.latest_referrals" :key="r.id">
                                        <td class="truncate-name">
                                            {{ r.referral.first_name }}
                                            {{ r.referral.last_name }}
                                        </td>
                                        <td>
                                            {{ r.referral_status }}
                                        </td>
                                        <td class="text-center">
                                            <template v-if="'with_referral' == r.processing_status">
                                                <a v-if="canAction" role="button" data-bs-toggle="popover"
                                                    data-bs-trigger="hover" :data-bs-content="'Send a reminder to ' +
                                                        r.referral['fullname']
                                                        " data-bs-placement="bottom" @click.prevent="
                                                            remindReferral(r)
                                                            "><i class="fa fa-bell text-warning"
                                                        aria-hidden="true"></i>
                                                </a>
                                                <a role="button" data-bs-toggle="popover" data-bs-trigger="hover"
                                                    :data-bs-content="'Recall the referral request sent to ' +
                                                        r.referral['fullname']
                                                        " data-bs-placement="bottom" @click.prevent="
                                                            recallReferral(r)
                                                            "><i class="fa fa-times-circle text-danger"
                                                        aria-hidden="true"></i>
                                                </a>
                                            </template>
                                            <template v-else>
                                                <small v-if="canAction"><a role="button" data-bs-toggle="popover"
                                                        data-bs-trigger="hover" :data-bs-content="'Resend this referral request to ' +
                                                            r.referral['fullname']
                                                            " @click.prevent="
                                                                resendReferral(r)
                                                                "><i class="fa fa-envelope text-primary"
                                                            aria-hidden="true"></i>
                                                    </a></small>
                                            </template>
                                        </td>
                                    </tr>
                                </tbody>
                            </table>
                            <ShowAllReferrals @refreshFromResponse="refreshFromResponse"
                                :occurrence_report_obj="occurrence_report" :canAction="canAction"
                                :isFinalised="occurrence_report.finalised" :referral_url="referralListURL" />
                        </div>
                    </div>
                    <div v-if="canAction" class="card-body border-top">
                        <div class="mb-3">
                            <strong>Actions</strong>
                        </div>
                        <div class="text-center">
                            <button v-if="with_assessor" style="width:80%;" class="btn btn-primary mb-4"
                                @click.prevent="amendmentRequest()">Request
                                Amendment</button>
                            <button v-if="with_approver || unlocked" style="width:80%;" class="btn btn-primary mb-4"
                                @click.prevent="backToAssessor()">Back to Assessor</button>

                            <button v-if="with_assessor" style="width:80%;" class="btn btn-primary mb-2"
                                @click.prevent="proposeApprove">Propose Approve</button>
                            <button v-if="with_assessor" style="width:80%;" class="btn btn-primary mb-4"
                                @click.prevent="proposeDecline">Propose Decline</button>

                            <button v-if="display_approve_button" style="width:80%;" class="btn btn-primary mb-4"
                                @click.prevent="approve()">Approve</button>
                            <button v-if="display_decline_button" style="width:80%;" class="btn btn-primary mb-4"
                                @click.prevent="decline()">Decline</button>

                            <button v-if="with_assessor || with_approver" style="width:80%;" class="btn btn-primary mb-2"
                                @click.prevent="splitSpecies()">Split</button><br />
                            <button v-if="canDiscard" style="width:80%;" class="btn btn-primary mb-2"
                                @click.prevent="discardOCRProposal()">Discard</button>

                            <button v-if="approved" style="width:80%;" class="btn btn-primary mb-4"
                                @click.prevent="unlock()">Unlock</button>
                            <button v-if="unlocked" style="width:80%;" class="btn btn-primary mb-4"
                                @click.prevent="lock()">Lock</button>
                        </div>
                    </div>
                </div>
            </div>
            <div class="col-md-9">
                <template>
                    <form :action="occurrence_report_form_url" method="post" name="occurrence_report"
                        enctype="multipart/form-data">
                        <ProposalOccurrenceReport v-if="occurrence_report" :occurrence_report_obj="occurrence_report"
                            id="OccurrenceReportStart" :canEditStatus="false" :is_external="false" :is_internal="true"
                            ref="occurrence_report" @refreshFromResponse="refreshFromResponse" @refreshOccurrenceReport="refreshOccurrenceReport()">
                        </ProposalOccurrenceReport>

                        <input type="hidden" name="csrfmiddlewaretoken" :value="csrf_token" />
                        <input type='hidden' name="occurrence_report_id" :value="1" />
                        <div class="row" style="margin-bottom: 50px">
                            <div class="navbar fixed-bottom" style="background-color: #f5f5f5;">
                                <div v-if="occurrence_report.internal_application && occurrence_report.can_user_edit" class="container">
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
                                            :disabled="saveExitOccurrenceReport || savingOccurrenceReport">Submit</button>
                                    </div>
                                </div>
                                <div v-else-if="(occurrence_report.assessor_mode.has_assessor_mode || occurrence_report.assessor_mode.has_unlocked_mode)" class="container">
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

        <AmendmentRequest ref="amendment_request" :occurrence_report_id="occurrence_report.id"
            @refreshFromResponse="refreshFromResponse"></AmendmentRequest>
        <BackToAssessor ref="back_to_assessor" :occurrence_report_id="occurrence_report.id"
            :occurrence_report_number="occurrence_report.occurrence_report_number"
            @refreshFromResponse="refreshFromResponse">
        </BackToAssessor>
        <ProposeAppprove ref="propose_approve" :occurrence_report="occurrence_report"
            :occurrence_report_number="occurrence_report.occurrence_report_number" :occurrence="occurrence_report.occurrence"
            :group_type_id="occurrence_report.group_type_id" @refreshFromResponse="refreshFromResponse">
        </ProposeAppprove>
        <ProposeDecline ref="propose_decline" :occurrence_report_id="occurrence_report.id"
            :occurrence_report_number="occurrence_report.occurrence_report_number"
            @refreshFromResponse="refreshFromResponse">
        </ProposeDecline>

        <Decline v-if="display_decline_button" ref="decline" :occurrence_report_id="occurrence_report.id"
            :occurrence_report_number="occurrence_report.occurrence_report_number"
            :declined_details="occurrence_report.declined_details" @refreshFromResponse="refreshFromResponse"></Decline>
        <Approve v-if="display_approve_button && occurrence_report.approval_details" ref="approve"
            :occurrence_report_id="occurrence_report.id"
            :occurrence_report_number="occurrence_report.occurrence_report_number"
            :approval_details="occurrence_report.approval_details" @refreshFromResponse="refreshFromResponse"></Approve>


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
import ShowAllReferrals from '@common-utils/occurrence/ocr_more_referrals.vue'
import ProposalOccurrenceReport from '@/components/form_occurrence_report.vue'
import AmendmentRequest from './amendment_request.vue'
import BackToAssessor from './back_to_assessor.vue'
import ProposeDecline from './ocr_propose_decline.vue'
import ProposeAppprove from './ocr_propose_approve.vue'
import Decline from './ocr_decline.vue'
import Approve from './ocr_approve.vue'

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
            referrals_api_endpoint: api_endpoints.ocr_referrals,
            initialisedSelects: false,
            form: null,
            selected_referral: '',
            referral_text: '',
            sendingReferral: false,
            savingOccurrenceReport: false,
            saveExitOccurrenceReport: false,
            submitOccurrenceReport: false,
            imageURL: '',
            isSaved: false,
            DATE_TIME_FORMAT: 'DD/MM/YYYY HH:mm:ss',
            department_users: null,
        }
    },
    components: {
        datatable,
        CommsLogs,
        Submission,
        Workflow,
        ShowAllReferrals,
        ProposalOccurrenceReport,
        AmendmentRequest,
        BackToAssessor,
        ProposeDecline,
        ProposeAppprove,
        Decline,
        Approve,
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
            return (this.occurrence_report) ? `/api/occurrence_report/${this.occurrence_report.id}/draft.json` : '';
        },
        display_group_type: function () {
            if (this.occurrence_report && this.occurrence_report.group_type) {
                return this.occurrence_report.group_type;
            }
            return '';
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
        display_approve_button: function () {
            return this.with_approver && this.occurrence_report.approval_details
        },
        display_decline_button: function () {
            return this.with_approver && this.occurrence_report.proposed_decline_status && this.occurrence_report.declined_details
        },
        display_referral_actions: function () {
            return this.occurrence_report && ['With Assessor', 'With Referral'].includes(this.occurrence_report.processing_status) && this.isAssignedOfficer
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
        with_assessor: function () {
            return this.occurrence_report && this.occurrence_report.processing_status === 'With Assessor'
        },
        with_referral: function () {
            return this.occurrence_report && this.occurrence_report.processing_status === 'With Referral'
        },
        with_approver: function () {
            return this.occurrence_report && this.occurrence_report.processing_status === 'With Approver'
        },
        approved: function () {
            return this.occurrence_report && this.occurrence_report.processing_status === 'Approved'
        },
        unlocked: function () {
            return this.occurrence_report && this.occurrence_report.processing_status === 'Unlocked'
        },
        canSeeSubmission: function () {
            // TODO define condition
            return true
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
            //return this.occurrence_report && this.occurrence_report.processing_status === "Draft" ? true : false;
            return false; //TODO do we need this here?
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
        referralListURL: function () {
            return this.occurrence_report != null
                ?
                api_endpoints.occurrence_report +
                `/${this.occurrence_report.id}/referrals/`
                : '';
        }
    },
    methods: {
        discardOCRProposal: function () {
            let vm = this;
            swal.fire({
                title: "Discard Report",
                text: "Are you sure you want to discard this report?",
                icon: "warning",
                showCancelButton: true,
                confirmButtonText: 'Discard Application',
                confirmButtonColor: '#d9534f'
            }).then((swalresult) => {
                if (swalresult.isConfirmed) {
                    vm.$http.delete(api_endpoints.discard_ocr_proposal(vm.occurrence_report.id))
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
        unlock: function () {
            let vm = this;
            swal.fire({
                title: "Unlock Report",
                text: "Are you sure you want to unlock this approved report?",
                icon: "warning",
                showCancelButton: true,
                confirmButtonText: 'Unlock Report',
                confirmButtonColor: '#d9534f'
            }).then((swalresult) => {
                if (swalresult.isConfirmed) {
                    vm.$http.post(`/api/occurrence_report/${vm.occurrence_report.id}/unlock_occurrence_report.json`)
                        .then((response) => {
                            swal.fire({
                                title: 'Unlocked',
                                text: 'The approved occurrence report has been unlocked for editing',
                                icon: 'success',
                                confirmButtonColor: '#226fbb',
                            });
                            vm.occurrence_report = response.body;
                        }, (error) => {
                            console.log(error);
                        });
                }
            }, (error) => {

            });
        },
        lock: function () {
            let vm = this;
            swal.fire({
                title: "Lock Report",
                text: "Are you sure you want to lock this approved report?",
                icon: "warning",
                showCancelButton: true,
                confirmButtonText: 'Lock Report',
                confirmButtonColor: '#d9534f'
            }).then((swalresult) => {
                if (swalresult.isConfirmed) {
                    vm.$http.post(`/api/occurrence_report/${vm.occurrence_report.id}/lock_occurrence_report.json`)
                        .then((response) => {
                            swal.fire({
                                title: 'Locked',
                                text: 'The approved occurrence report has been locked from editing',
                                icon: 'success',
                                confirmButtonColor: '#226fbb',
                            });
                            vm.occurrence_report = response.body;
                        }, (error) => {
                            console.log(error);
                        });
                }
            }, (error) => {

            });
        },
        amendmentRequest: function () {
            this.$refs.amendment_request.isModalOpen = true;
        },
        backToAssessor: function () {
            this.$refs.back_to_assessor.isModalOpen = true;
        },
        decline: function () {
            this.$refs.decline.isModalOpen = true;
        },
        approve: function () {
            this.$refs.approve.isModalOpen = true;
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

            // add map geometry to the occurrence_report
            if (vm.$refs.occurrence_report.$refs.ocr_location.$refs.component_map) {
                vm.occurrence_report.ocr_geometry = vm.$refs.occurrence_report.$refs.ocr_location.$refs.component_map.getJSONFeatures();
            }

            let payload = { proposal: vm.occurrence_report };
            await vm.$http.post(vm.occurrence_report_form_url, payload).then(res => {
                swal.fire({
                    title: "Saved",
                    text: "Your changes has been saved",
                    icon: "success",
                    confirmButtonColor: '#226fbb'
                });
                vm.savingOccurrenceReport = false;
                vm.isSaved = true;
                vm.occurrence_report = res.body
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
                        name: 'internal-occurrence-dash'
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

            // add map geometry to the occurrence_report
            if (vm.$refs.occurrence_report.$refs.ocr_location.$refs.component_map) {
                vm.occurrence_report.ocr_geometry = vm.$refs.occurrence_report.$refs.ocr_location.$refs.component_map.getJSONFeatures();
            }

            let payload = { proposal: vm.occurrence_report };
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
                if (vm.occurrence_report.species_id == null || vm.occurrence_report.species_id == '') {
                    blank_fields.push(' Scientific Name is missing')
                }
            }
            else {
                if (vm.occurrence_report.community_id == null || vm.occurrence_report.community_id == '') {
                    blank_fields.push(' Community Name is missing')
                }
            }
            if (check_action == 'submit') {
                //TODO add validation for fields required before submit
                if(!vm.occurrence_report.submitter_information.submitter_category){
                    blank_fields.push(' Please select a submitter category')
                }
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
                text: "Are you sure you want to submit this occurrence report?",
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
                        vm.$http.post(helpers.add_endpoint_json(api_endpoints.occurrence_report, vm.occurrence_report.id + '/submit'), payload).then(res => {
                            vm.occurrence = res.body;
                            // TODO router should push to submit_cs_proposal for internal side
                            vm.$router.push({
                                name: 'internal-occurrence-dash'
                            });
                        }, err => {
                            swal.fire({
                                title: 'Submit Error',
                                text: helpers.apiVueResourceError(err),
                                icon: 'error',
                                confirmButtonColor: '#226fbb'
                            });
                            vm.submitOccurrenceReport = false;
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
                vm.initialiseReferreeSelect();
                vm.initialiseAssignedOfficerSelect();
                vm.initialisedSelects = true;
            }
        },
        sendReferral: function () {
            let vm = this;
            let formData = new FormData(vm.form);
            vm.sendingReferral = true;
            let data = { 'email': vm.selected_referral, 'text': vm.referral_text };
            vm.$http.post(helpers.add_endpoint_json(api_endpoints.occurrence_report, (vm.occurrence_report.id + '/send_referral')), JSON.stringify(data), {
                emulateJSON: true
            }).then((response) => {
                vm.sendingReferral = false;
                vm.original_occurrence_report = helpers.copyObject(response.body);
                vm.occurrence_report = response.body;
                swal.fire({
                    title: 'Referral Sent',
                    text: `The referral has been sent to ${vm.selected_referral}`,
                    icon: 'success',
                    confirmButtonColor: '#226fbb'
                });
                $(vm.$refs.department_users).val(null).trigger("change");
                vm.selected_referral = '';
                vm.referral_text = '';
            }, (error) => {
                console.log(error);
                swal.fire({
                    title: 'Referral Error',
                    text: helpers.apiVueResourceError(error),
                    icon: 'error',
                    confirmButtonColor: '#226fbb'
                });
                vm.sendingReferral = false;
            });
        },
        remindReferral: function (r) {
            let vm = this;
            vm.$http.get(helpers.add_endpoint_json(api_endpoints.ocr_referrals, r.id + '/remind')).then(response => {
                vm.original_occurrence_report = helpers.copyObject(response.body);
                vm.occurrence_report = response.body;
                swal.fire({
                    title: 'Referral Reminder',
                    text: 'A reminder has been sent to ' + vm.department_users.find(d => d.id == r.referral.id).name,
                    icon: 'success',
                    confirmButtonColor: '#226fbb'
                });
            },
                error => {
                    swal.fire({
                        title: 'Referral Reminder Error',
                        text: helpers.apiVueResourceError(error),
                        icon: 'error',
                        confirmButtonColor: '#226fbb'
                    });
                });
        },
        recallReferral: function (r) {
            let vm = this;
            vm.$http.get(helpers.add_endpoint_json(api_endpoints.ocr_referrals, r.id + '/recall')).then(response => {
                vm.original_occurrence_report = helpers.copyObject(response.body);
                vm.occurrence_report = response.body;
                $('.popover').hide();
                vm.enablePopovers();
                swal.fire({
                    title: 'Referral Recall',
                    text: 'The referral has been recalled from ' + vm.department_users.find(d => d.id == r.referral.id).name,
                    icon: 'success',
                    confirmButtonColor: '#226fbb'
                });
            },
                error => {
                    swal.fire({
                        title: 'Referral Recall Error',
                        text: helpers.apiVueResourceError(error),
                        icon: 'error',
                        confirmButtonColor: '#226fbb'
                    });
                });
        },
        resendReferral: function (r) {
            let vm = this;
            vm.$http.get(helpers.add_endpoint_json(api_endpoints.ocr_referrals, r.id + '/resend')).then(response => {
                vm.original_occurrence_report = helpers.copyObject(response.body);
                vm.occurrence_report = response.body;
                $('.popover').hide();
                vm.enablePopovers();
                swal.fire({
                    title: 'Referral Resent',
                    text: 'The referral has been resent to ' + vm.department_users.find(d => d.id == r.referral.id).name,
                    icon: 'success',
                    confirmButtonColor: '#226fbb'
                });
            },
                error => {
                    swal.fire({
                        title: 'Referral Resent Error',
                        text: helpers.apiVueResourceError(error),
                        icon: 'error',
                        confirmButtonColor: '#226fbb'
                    });
                });
        },
        fetchDeparmentUsers: function () {
            let vm = this;
            vm.$http.get(api_endpoints.department_users).then((response) => {
                vm.department_users = response.body
            }, (error) => {
                console.log(error);
            })
        },
        initialiseReferreeSelect: function () {
            let vm = this;
            $(vm.$refs.department_users).select2({
                minimumInputLength: 2,
                "theme": "bootstrap-5",
                allowClear: true,
                placeholder: "Search for Referree",
                ajax: {
                    url: api_endpoints.users_api + '/get_referees/',
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
                    vm.$nextTick(() => {
                        vm.$refs.referral_text.focus();
                    });
                })
                .on("select2:unselect", function (e) {
                    var selected = $(e.currentTarget);
                    vm.selected_referral = null;
                })
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
                    if (vm.with_approver) {
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
                    if (vm.with_approver) {
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
            if (vm.with_approver) {
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
            if (vm.with_approver) {
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
                    vm.$nextTick(() => {
                        vm.initialiseReferreeSelect();
                    });
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
        proposeDecline: function () {
            this.$refs.propose_decline.isModalOpen = true;
        },
        proposeApprove: function () {
            this.$refs.propose_approve.isModalOpen = true;
        },
        enablePopovers: function () {
            this.$nextTick(() => {
                $(function () {
                    $('[data-bs-toggle="popover"]').each(function () {
                        new bootstrap.Popover(this);
                    })
                })
            });
        },
        fetchOccurrenceReport: function (id) {
            let vm = this;
            Vue.http.get(`/api/occurrence_report/${id}/`).then(res => {
                vm.occurrence_report = res.body;
            },
                err => {
                    console.log(err);
                });
        },
        refreshOccurrenceReport: function () {
            this.fetchOccurrenceReport(this.$route.params.occurrence_report_id);
        },
    },
    created: function () {
        if (!this.occurrence_report) {
            this.fetchOccurrenceReport(this.$route.params.occurrence_report_id);
        }
    },
    mounted: function () {
        let vm = this;
        vm.fetchDeparmentUsers();
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
