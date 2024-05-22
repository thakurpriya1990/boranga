<template lang="html">
    <div v-if="conservation_status_obj" class="container" id="internalConservationStatus">
        <div class="row" style="padding-bottom: 50px;">
            <h3><span class="text-capitalize">{{ conservation_status_obj.group_type }}</span> {{
                conservation_status_obj.conservation_status_number }}</h3>
            <div class="col-md-3">
                <CommsLogs :comms_url="comms_url" :logs_url="logs_url" :comms_add_url="comms_add_url"
                    :disable_add_entry="false" />

                <Submission v-if="canSeeSubmission" :submitter_first_name="submitter_first_name"
                    :submitter_last_name="submitter_last_name" :lodgement_date="conservation_status_obj.lodgement_date"
                    :is_new_contributor="conservation_status_obj.is_new_contributor" class="mt-3" />

                <div class="mt-3">
                    <div class="card card-default">
                        <div class="card-header">
                            Workflow
                        </div>
                        <div class="card-body">
                            <strong>Status</strong><br />
                            {{ conservation_status_obj.processing_status }}
                        </div>
                        <div v-if="!isFinalised" class="card-body border-top">
                            <div class="row">
                                <div class="col-sm-12 top-buffer-s">
                                    <strong>Currently assigned to</strong><br />
                                    <div class="form-group">
                                        <template v-if="conservation_status_obj.processing_status == 'With Approver'">
                                            <select ref="assigned_officer" :disabled="!canAction" class="form-control"
                                                v-model="conservation_status_obj.assigned_approver">
                                                <option v-for="member in conservation_status_obj.allowed_assessors"
                                                    :value="member.id">{{ member.first_name }} {{ member.last_name }}
                                                </option>
                                            </select>
                                            <a v-if="canAssess && conservation_status_obj.assigned_approver != conservation_status_obj.current_assessor.id"
                                                @click.prevent="assignRequestUser()" class="actionBtn float-end">Assign
                                                to me</a>
                                        </template>
                                        <template v-else>
                                            <select ref="assigned_officer" :disabled="!canAction" class="form-control"
                                                v-model="conservation_status_obj.assigned_officer">
                                                <option v-for="member in conservation_status_obj.allowed_assessors"
                                                    :value="member.id">{{ member.first_name }} {{ member.last_name }}
                                                </option>
                                            </select>
                                            <a v-if="canAssess && conservation_status_obj.assigned_officer != conservation_status_obj.current_assessor.id"
                                                @click.prevent="assignRequestUser()" class="actionBtn float-end">Assign
                                                to me</a>
                                        </template>
                                    </div>
                                </div>
                            </div>
                        </div>
                        <div v-if="canAction"
                            class="card-body border-top">
                            <div class="row">
                                <div class="col-sm-12 top-buffer-s">
                                    <strong>Referrals</strong><br />
                                    <div class="form-group mb-3">
                                        <select :disabled="!canLimitedAction" ref="department_users"
                                            class="form-control">
                                        </select>
                                        <template v-if='!sendingReferral'>
                                            <template v-if="selected_referral">
                                                <label class="control-label mt-2" for="referral_text">Comments</label>
                                                <textarea class="form-control" name="referral_text" ref="referral_text"
                                                    v-model="referral_text"></textarea>
                                                <a v-if="canLimitedAction" @click.prevent="sendReferral()"
                                                    class="actionBtn float-end">Send</a>
                                            </template>
                                        </template>
                                        <template v-else>
                                            <span v-if="canLimitedAction" @click.prevent="sendReferral()" disabled
                                                class="actionBtn text-primary float-end">
                                                Sending Referral&nbsp;
                                                <i class="fa fa-circle-o-notch fa-spin fa-fw"></i>
                                            </span>
                                        </template>
                                    </div>
                                    <template
                                        v-if="conservation_status_obj.latest_referrals && conservation_status_obj.latest_referrals.length > 0">
                                        <div>
                                            <div class="fw-bold mb-1">
                                                Recent Referrals
                                                <small class="text-secondary fw-lighter">(Showing {{
                                                    conservation_status_obj.latest_referrals.length }} of
                                                    {{ conservation_status_obj.referrals.length }})</small>
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
                                                    <tr v-for="r in conservation_status_obj.latest_referrals">
                                                        <td class="truncate-name">
                                                            {{ r.referral_obj.first_name }} {{
                                                                r.referral_obj.last_name }}
                                                        </td>
                                                        <td>
                                                            {{ r.processing_status }}
                                                        </td>
                                                        <td>
                                                            <template v-if="r.processing_status == 'Awaiting'">
                                                                <a v-if="canLimitedAction" role="button"
                                                                    data-bs-toggle="popover" data-bs-trigger="hover"
                                                                    :data-bs-content="'Send a reminder to ' +
                                                                        r.referral_obj['fullname']
                                                                        " data-bs-placement="bottom"
                                                                    data-bs-container="body"
                                                                    @click.prevent="remindReferral(r)"><i
                                                                        class="fa fa-bell text-warning"
                                                                        aria-hidden="true"></i>
                                                                </a>
                                                                <a role="button" data-bs-toggle="popover"
                                                                    data-bs-trigger="hover" :data-bs-content="'Recall the referral request sent to ' +
                                                                        r.referral_obj['fullname']
                                                                        " data-bs-placement="bottom"
                                                                    data-bs-container="body"
                                                                    @click.prevent="recallReferral(r)"><i
                                                                        class="fa fa-times-circle text-danger"
                                                                        aria-hidden="true"></i>
                                                                </a>
                                                            </template>
                                                            <template v-else>
                                                                <template v-if="canLimitedAction"><a role="button"
                                                                        data-bs-toggle="popover" data-bs-trigger="hover"
                                                                        :data-bs-content="'Resend this referral request to ' +
                                                                            r.referral_obj['fullname']
                                                                            " data-bs-container="body"
                                                                        @click.prevent="resendReferral(r)"><i
                                                                            class="fa fa-envelope text-primary"
                                                                            aria-hidden="true"></i>
                                                                    </a>
                                                                </template>
                                                            </template>
                                                        </td>
                                                    </tr>
                                                </tbody>
                                            </table>
                                            <CSMoreReferrals @refreshFromResponse="refreshFromResponse"
                                                :conservation_status_obj="conservation_status_obj"
                                                :canAction="canLimitedAction" :isFinalised="isFinalised"
                                                :referral_url="referralListURL" />
                                        </div>
                                    </template>
                                </div>
                            </div>
                        </div>
                        <div v-if="!isFinalised && canAction" class="card-body border-top">
                            <div class="row">
                                <div class="col-sm-12 top-buffer-s">
                                    <template
                                        v-if="conservation_status_obj.processing_status == 'With Assessor' || conservation_status_obj.processing_status == 'With Referral'">
                                        <div class="row">
                                            <div class="col-sm-12">
                                                <strong>Action</strong><br />
                                            </div>
                                        </div>
                                        <div class="row">
                                            <div class="col-sm-12">
                                                <button style="width:90%;" class="btn btn-primary top-buffer-s"
                                                    :disabled="!conservation_status_obj.can_user_edit"
                                                    @click.prevent="amendmentRequest()">Request
                                                    Amendment</button><br />
                                            </div>
                                        </div>
                                        <div class="row" v-if="conservation_status_obj.approval_level == 'minister'">
                                            <div class="col-sm-12">
                                                <button style="width:90%;" class="btn btn-primary top-buffer-s"
                                                    :disabled="!conservation_status_obj.can_user_edit"
                                                    @click.prevent="proposedReadyForAgenda()">Propose Ready For
                                                    Agenda</button><br />
                                            </div>
                                        </div>
                                        <div class="row"
                                            v-if="conservation_status_obj.approval_level == 'intermediate'">
                                            <div class="col-sm-12">
                                                <button style="width:90%;" class="btn btn-primary top-buffer-s"
                                                    :disabled="!conservation_status_obj.can_user_edit"
                                                    @click.prevent="declineProposal()">Decline</button><br />
                                            </div>
                                        </div>
                                        <div class="row"
                                            v-if="conservation_status_obj.approval_level == 'intermediate'">
                                            <div class="col-sm-12">
                                                <button style="width:90%;" class="btn btn-primary top-buffer-s"
                                                    :disabled="!conservation_status_obj.can_user_edit"
                                                    @click.prevent="issueProposal()">Approve</button><br />
                                            </div>
                                        </div>
                                    </template>
                                    <template v-if="conservation_status_obj.processing_status == 'Ready For Agenda'">
                                        <div class="row">
                                            <div class="col-sm-12">
                                                <strong>Action</strong><br />
                                            </div>
                                        </div>
                                        <div class="row" v-if="conservation_status_obj.approval_level == 'minister'">
                                            <div class="col-sm-12">
                                                <button style="width:90%;" class="btn btn-primary top-buffer-s"
                                                    :disabled="!conservation_status_obj.can_user_edit"
                                                    @click.prevent="declineProposal()">Decline</button><br />
                                            </div>
                                        </div>
                                        <div class="row" v-if="conservation_status_obj.approval_level == 'minister'">
                                            <div class="col-sm-12">
                                                <button style="width:90%;" class="btn btn-primary top-buffer-s"
                                                    :disabled="!conservation_status_obj.can_user_edit"
                                                    @click.prevent="issueProposal()">Approve</button><br />
                                            </div>
                                        </div>
                                    </template>
                                    <template v-else-if="conservation_status_obj.processing_status == 'With Approver'">
                                        <div class="row">
                                            <div class="col-sm-12">
                                                <strong>Action</strong><br />
                                            </div>
                                        </div>
                                        <div class="row">
                                            <div class="col-sm-12">
                                                <label class="control-label pull-left" for="Name">Approver
                                                    Comments</label>
                                                <textarea class="form-control" name="name"
                                                    v-model="approver_comment"></textarea><br>
                                            </div>
                                        </div>
                                        <div class="row">
                                            <div class="col-sm-12">
                                                <button style="width:90%;" class="btn btn-primary"
                                                    :disabled="conservation_status_obj.can_user_edit"
                                                    @click.prevent="switchStatus('with_assessor')">Back To
                                                    Assessor</button><br />
                                            </div>
                                        </div>
                                        <div class="row">
                                            <div class="col-sm-12">
                                                <button style="width:90%;" class="btn btn-primary top-buffer-s"
                                                    :disabled="conservation_status_obj.can_user_edit"
                                                    @click.prevent="issueProposal()">Approve</button><br />
                                            </div>
                                            <div class="col-sm-12">
                                                <button style="width:90%;" class="btn btn-primary top-buffer-s"
                                                    :disabled="conservation_status_obj.can_user_edit"
                                                    @click.prevent="declineProposal()">Decline</button><br />
                                            </div>
                                        </div>
                                    </template>
                                </div>
                                <template v-if="canDiscard">
                                    <div class="row">
                                        <div class="col-sm-12">
                                            <strong>Action</strong><br />
                                        </div>
                                    </div>
                                    <div class="row">
                                        <div class="col-sm-12">
                                            <button style="width:90%;" class="btn btn-primary top-buffer-s"
                                                @click.prevent="discardCSProposal()">Discard</button><br />
                                        </div>
                                    </div>
                                </template>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
            <div class="col-md-9">
                <div class="row">
                    <template>
                        <div class="">
                            <div class="row">
                                <form :action="species_community_cs_form_url" method="post"
                                    name="new_conservation_status" enctype="multipart/form-data">
                                    <ProposalConservationStatus ref="conservation_status"
                                        :conservation_status_obj="conservation_status_obj"
                                        :canEditStatus="canEditStatus" id="ConservationStatusStart" :is_internal="true">
                                        <!-- TODO add hasAssessorMode props to ProposalConservationStatus -->
                                    </ProposalConservationStatus>
                                    <input type="hidden" name="csrfmiddlewaretoken" :value="csrf_token" />
                                    <input type='hidden' name="conservation_status_id" :value="1" />
                                    <div class="row" style="margin-bottom: 50px">
                                        <div class="navbar fixed-bottom" style="background-color: #f5f5f5;">
                                            <!--the below as internal proposal submission ELSE just saving proposal changes -->
                                            <div v-if="conservation_status_obj.internal_user_edit" class="container">
                                                <div class="col-md-12 text-end">
                                                    <button v-if="savingConservationStatus" class="btn btn-primary me-2"
                                                        style="margin-top:5px;" disabled>Save and Continue&nbsp;
                                                        <i class="fa fa-circle-o-notch fa-spin fa-fw"></i></button>
                                                    <button v-else class="btn btn-primary me-2" style="margin-top:5px;"
                                                        @click.prevent="save()"
                                                        :disabled="saveExitConservationStatus || submitConservationStatus">Save
                                                        and Continue</button>

                                                    <button v-if="saveExitConservationStatus"
                                                        class="btn btn-primary me-2" style="margin-top:5px;"
                                                        disabled>Save and Exit&nbsp;
                                                        <i class="fa fa-circle-o-notch fa-spin fa-fw"></i></button>
                                                    <button v-else class="btn btn-primary me-2" style="margin-top:5px;"
                                                        @click.prevent="save_exit()"
                                                        :disabled="savingConservationStatus || submitConservationStatus">Save
                                                        and Exit</button>

                                                    <button v-if="submitConservationStatus" class="btn btn-primary"
                                                        style="margin-top:5px;" disabled>Submit&nbsp;
                                                        <i class="fa fa-circle-o-notch fa-spin fa-fw"></i></button>
                                                    <button v-else class="btn btn-primary" style="margin-top:5px;"
                                                        @click.prevent="submit()"
                                                        :disbaled="saveExitConservationStatus || savingConservationStatus">Submit</button>
                                                </div>
                                            </div>

                                            <div v-else-if="hasAssessorMode" class="container">
                                                <div class="col-md-12 text-end">
                                                    <button v-if="savingConservationStatus" class="btn btn-primary"
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
                            </div>
                        </div>
                    </template>
                </div>
            </div>
        </div>
        <AmendmentRequest ref="amendment_request" :conservation_status_id="conservation_status_obj.id"
            @refreshFromResponse="refreshFromResponse"></AmendmentRequest>
        <ProposedDecline ref="proposed_decline" :processing_status="conservation_status_obj.processing_status"
            :conservation_status_id="conservation_status_obj.id" @refreshFromResponse="refreshFromResponse">
        </ProposedDecline>
        <ProposedApproval ref="proposed_approval" :processing_status="conservation_status_obj.processing_status"
            :conservation_status_id="conservation_status_obj.id" :isApprovalLevelDocument="isApprovalLevelDocument"
            @refreshFromResponse="refreshFromResponse" />

    </div>
</template>
<script>
import Vue from 'vue'
import datatable from '@vue-utils/datatable.vue'
import CommsLogs from '@common-utils/comms_logs.vue'
import Submission from '@common-utils/submission.vue'
import Workflow from '@common-utils/workflow.vue'
import AmendmentRequest from './amendment_request.vue'
import ProposedDecline from './proposal_proposed_decline'
import ProposedApproval from './proposed_issuance.vue'

import CSMoreReferrals from '@common-utils/conservation_status/cs_more_referrals.vue'
import ProposalConservationStatus from '@/components/form_conservation_status.vue'
import {
    api_endpoints,
    helpers
}
    from '@/utils/hooks'
export default {
    name: 'InternalConservationStatus',
    data: function () {
        let vm = this;
        return {
            "conservation_status_obj": null,
            "original_conservation_status_obj": null,
            "loading": [],
            form: null,
            savingConservationStatus: false,
            saveExitConservationStatus: false,
            submitConservationStatus: false,
            submitting: false,
            saveExitCSProposal: false,
            savingCSProposal: false,
            department_users: [],
            selected_referral: '',
            referral_text: '',
            approver_comment: '',
            sendingReferral: false,
            changingStatus: false,
            proposeReadyForAgenda: false,

            DATE_TIME_FORMAT: 'DD/MM/YYYY HH:mm:ss',
            comms_url: helpers.add_endpoint_json(api_endpoints.conservation_status, vm.$route.params.conservation_status_id + '/comms_log'),
            comms_add_url: helpers.add_endpoint_json(api_endpoints.conservation_status, vm.$route.params.conservation_status_id + '/add_comms_log'),
            logs_url: helpers.add_endpoint_json(api_endpoints.conservation_status, vm.$route.params.conservation_status_id + '/action_log'),
            initialisedSelects: false,
            cs_proposal_readonly: true,
            isSaved: false,
        }
    },
    components: {
        datatable,
        CommsLogs,
        Submission,
        Workflow,
        ProposalConservationStatus,
        AmendmentRequest,
        CSMoreReferrals,
        ProposedDecline,
        ProposedApproval,
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
        referralListURL: function () {
            return this.conservation_status_obj != null ? helpers.add_endpoint_json(api_endpoints.cs_referrals, 'datatable_list') + '?conservation_status=' + this.conservation_status_obj.id : '';
        },
        species_community_cs_form_url: function () {
            if (this.$route.query.action == 'edit') {
                return `/api/conservation_status/${this.conservation_status_obj.id}/conservation_status_edit.json`;
            }
            else {
                return `/api/conservation_status/${this.conservation_status_obj.id}/conservation_status_save.json`;
            }
        },
        submitter_first_name: function () {
            if (this.conservation_status_obj.submitter) {
                return this.conservation_status_obj.submitter.first_name
            } else {
                return ''
            }
        },
        submitter_last_name: function () {
            if (this.conservation_status_obj.submitter) {
                return this.conservation_status_obj.submitter.last_name
            } else {
                return ''
            }
        },
        submitter_id: function () {
            if (this.conservation_status_obj.submitter) {
                return this.conservation_status_obj.submitter.id
            } else {
                //eturn this.conservation_status_obj.applicant_obj.id
            }
        },
        submitter_email: function () {
            if (this.conservation_status_obj.submitter) {
                return this.conservation_status_obj.submitter.email
            } else {
                //return this.conservation_status_obj.applicant_obj.email
            }
        },
        canSeeSubmission: function () {
            return true; // TODO the Processing Status based value
        },
        canEditStatus: function () {
            return this.conservation_status_obj ? this.conservation_status_obj.can_user_edit : 'false';
        },
        isFinalised: function () {
            return this.conservation_status_obj.processing_status == 'Declined' || this.conservation_status_obj.processing_status == 'Approved';
        },
        canLimitedAction: function () {
            return this.conservation_status_obj
                && (
                    this.conservation_status_obj.processing_status == 'With Assessor'
                    || this.conservation_status_obj.processing_status == 'With Referral'
                )
                && !this.isFinalised
                && this.conservation_status_obj.can_user_edit
                && (
                    this.conservation_status_obj.current_assessor.id == this.conservation_status_obj.assigned_officer
                    || this.conservation_status_obj.assigned_officer == null
                )
                && this.conservation_status_obj.assessor_mode.assessor_can_assess ? true : false;
        },
        canAction: function () {
            if (this.conservation_status_obj.processing_status == 'With Approver') {
                return this.conservation_status_obj
                    && !this.isFinalised
                    && this.conservation_status_obj.can_user_edit
                    && (
                        this.conservation_status_obj.current_assessor.id == this.conservation_status_obj.assigned_approver
                        || this.conservation_status_obj.assigned_approver == null
                    )
                    && this.conservation_status_obj.assessor_mode.assessor_can_assess ? true : false;
            }
            else if ( ['With Assessor', 'Ready For Agenda', 'With Referral'].includes(this.conservation_status_obj.processing_status)) {
                return this.conservation_status_obj
                    && !this.isFinalised &&
                    this.conservation_status_obj.can_user_edit
                    && (
                        this.conservation_status_obj.current_assessor.id == this.conservation_status_obj.assigned_officer                    )
                    && this.conservation_status_obj.assessor_mode.assessor_can_assess ? true : false;
            } else {
                return this.conservation_status_obj
                    && this.conservation_status_obj.processing_status == 'Draft'
                    && this.conservation_status_obj.internal_application
                    && this.conservation_status_obj.internal_user_edit
            }
        },
        canAssess: function () {
            return this.conservation_status_obj && this.conservation_status_obj.assessor_mode.assessor_can_assess ? true : false;
        },
        hasAssessorMode: function () {
            // Need to check for approved status as to show 'Save changes' button only when edit and not while view
            if (this.conservation_status_obj.processing_status == 'Approved') {
                if (this.$route.query.action == 'edit') {
                    return this.conservation_status_obj && this.conservation_status_obj.assessor_mode.has_assessor_mode ? true : false;
                }
                else {
                    return false;
                }
            }
            else {
                return this.conservation_status_obj && this.conservation_status_obj.assessor_mode.has_assessor_mode ? true : false;
            }
        },
        isApprovalLevelDocument: function () {
            return false;
        },
        canDiscard: function () {
            return this.conservation_status_obj.internal_user_edit;
        },
    },
    methods: {
        commaToNewline(s) {
            return s.replace(/[,;]/g, '\n');
        },
        discardCSProposal: function () {
            let vm = this;
            swal.fire({
                title: "Discard Application",
                text: "Are you sure you want to discard this proposal?",
                icon: "warning",
                showCancelButton: true,
                confirmButtonText: 'Discard Application',
                confirmButtonColor: '#d9534f'
            }).then((result) => {
                if (result.isConfirmed) {
                    vm.$http.delete(api_endpoints.discard_cs_proposal(vm.conservation_status_obj.id))
                        .then((response) => {
                            swal.fire({
                                title: 'Discarded',
                                text: 'Your proposal has been discarded',
                                icon: 'success',
                                confirmButtonColor: '#226fbb',
                            });
                            vm.$router.push({
                                name: 'internal-conservation_status-dash'
                            });
                        }, (error) => {
                            console.log(error);
                        });
                }
            });
        },
        amendmentRequest: function () {
            let value = '';
            value = $('#assessor_deficiencies').val();
            this.$refs.amendment_request.amendment.text = value;
            this.$refs.amendment_request.isModalOpen = true;
        },
        proposedReadyForAgenda: function () {
            let vm = this;
            vm.proposeReadyForAgenda = true;
            vm.$http.post(helpers.add_endpoint_json(api_endpoints.conservation_status, vm.conservation_status_obj.id + '/proposed_ready_for_agenda')).then((response) => {
                vm.proposeReadyForAgenda = false;
                vm.$router.push({ path: '/internal/conservation-status/' }); //Navigate to dashboard page after Propose issue.
            }, (error) => {
                vm.errors = true;
                vm.proposeReadyForAgenda = false;
                vm.errorString = helpers.apiVueResourceError(error);
            });
        },
        proposedApproval: function () {
            this.$refs.proposed_approval.approval = this.conservation_status_obj.conservationstatusissuanceapprovaldetails != null ? helpers.copyObject(this.conservation_status_obj.conservationstatusissuanceapprovaldetails) : {};
            this.$refs.proposed_approval.isModalOpen = true;
        },
        issueProposal: function () {
            this.$refs.proposed_approval.approval = this.conservation_status_obj.conservationstatusissuanceapprovaldetails != null ? helpers.copyObject(this.conservation_status_obj.conservationstatusissuanceapprovaldetails) : {};
            this.$refs.proposed_approval.state = 'final_approval';
            this.$refs.proposed_approval.isApprovalLevelDocument = this.isApprovalLevelDocument;
            this.$refs.proposed_approval.isModalOpen = true;
        },
        proposedDecline: function () {
            this.save_wo();
            this.$refs.proposed_decline.decline = this.conservation_status_obj.conservationstatusdeclineddetails != null ? helpers.copyObject(this.conservation_status_obj.conservationstatusdeclineddetails) : {};
            this.$refs.proposed_decline.isModalOpen = true;
        },
        declineProposal: function () {
            this.$refs.proposed_decline.decline = this.conservation_status_obj.conservationstatusdeclineddetails != null ? helpers.copyObject(this.conservation_status_obj.conservationstatusdeclineddetails) : {};
            this.$refs.proposed_decline.isModalOpen = true;
        },
        save: async function (e) {
            let vm = this;
            var missing_data = vm.can_submit("");
            if (missing_data != true) {
                swal.fire({
                    title: "Please fix following errors before saving",
                    text: missing_data,
                    icon: 'error',
                    confirmButtonColor: '#226fbb'
                })
                return false;
            }
            vm.isSaved = false;
            vm.savingConservationStatus = true;
            let payload = new Object();
            Object.assign(payload, vm.conservation_status_obj);
            await vm.$http.post(vm.species_community_cs_form_url, payload).then(res => {
                swal.fire({
                    title: 'Saved',
                    text: 'Your changes has been saved',
                    icon: 'success',
                    confirmButtonColor: '#226fbb',
                });
                vm.savingConservationStatus = false;
                vm.isSaved = true;
            }, err => {
                var errorText = helpers.apiVueResourceError(err);
                swal.fire({
                    title: 'Save Error',
                    text: errorText,
                    icon: 'error',
                    confirmButtonColor: '#226fbb'
                });
                vm.savingConservationStatus = false;
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
                return false;
            }
            vm.saveExitConservationStatus = true;
            await this.save(e).then(() => {
                if (vm.isSaved === true) {
                    vm.$router.push({
                        name: 'internal-conservation_status-dash'
                    });
                } else {
                    vm.saveExitConservationStatus = false;
                }
            });
        },
        save_before_submit: async function (e) {
            let vm = this;
            vm.saveError = false;

            let payload = new Object();
            Object.assign(payload, vm.conservation_status_obj);
            const result = await vm.$http.post(vm.species_community_cs_form_url, payload).then(res => {
                //return true;
            }, err => {
                var errorText = helpers.apiVueResourceError(err);
                swal.fire({
                    title: 'Submit Error',
                    text: errorText,
                    icon: 'error',
                    confirmButtonColor: '#226fbb'
                });
                vm.submitConservationStatus = false;
                vm.saveError = true;
            });
            return result;
        },
        can_submit: function (check_action) {
            let vm = this;
            let blank_fields = []
            // TODO check blank
            blank_fields = vm.can_submit_conservation_status(check_action);

            if (blank_fields.length == 0) {
                return true;
            }
            else {
                return blank_fields;
            }
        },
        can_submit_conservation_status: function (check_action) {
            let vm = this;
            let blank_fields = []
            if (vm.conservation_status_obj.group_type == 'flora' || vm.conservation_status_obj.group_type == 'fauna') {
                if (vm.conservation_status_obj.species_id == null || vm.conservation_status_obj.species_id == '') {
                    blank_fields.push(' Scientific Name is missing')
                }
            }
            else {
                if (vm.conservation_status_obj.community_id == null || vm.conservation_status_obj.community_id == '') {
                    blank_fields.push(' Community Name is missing')
                }
            }
            if (check_action == "submit") {
                // TODO: Check for required conservation list / category fields
            }
            return blank_fields
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
                return false;
            }
            vm.submitConservationStatus = true;
            swal.fire({
                title: "Submit New Conservation Status Application",
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
                        Object.assign(payload, vm.conservation_status_obj);
                        vm.$http.post(helpers.add_endpoint_json(api_endpoints.conservation_status, vm.conservation_status_obj.id + '/submit'), payload).then(res => {
                            vm.conservation_status_obj = res.body;
                            // TODO router should push to submit_cs_proposal for internal side
                            vm.$router.push({
                                name: 'internal-conservation_status-dash'
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
                vm.submitConservationStatus = false;
            });
        },
        save_wo: function () {
            let vm = this;
            let payload = new Object();
            Object.assign(payload, vm.conservation_status_obj);
            vm.$http.post(vm.species_community_cs_form_url, payload).then(res => {
            }, err => {
            });
        },
        refreshFromResponse: function (response) {
            let vm = this;
            vm.original_conservation_status_obj = helpers.copyObject(response.body);
            vm.conservation_status_obj = helpers.copyObject(response.body);
            vm.$nextTick(() => {
                vm.initialiseAssignedOfficerSelect(true);
                vm.updateAssignedOfficerSelect();
            });
        },
        assignTo: function () {
            let vm = this;
            let unassign = true;
            let data = {};
            if (vm.conservation_status_obj.processing_status == 'With Approver') {
                unassign = vm.conservation_status_obj.assigned_approver != null && vm.conservation_status_obj.assigned_approver != 'undefined' ? false : true;
                data = { 'assessor_id': vm.conservation_status_obj.assigned_approver };
            }
            else {
                unassign = vm.conservation_status_obj.assigned_officer != null && vm.conservation_status_obj.assigned_officer != 'undefined' ? false : true;
                data = { 'assessor_id': vm.conservation_status_obj.assigned_officer };
            }
            if (!unassign) {
                vm.$http.post(helpers.add_endpoint_json(api_endpoints.conservation_status, (vm.conservation_status_obj.id + '/assign_to')), JSON.stringify(data), {
                    emulateJSON: true
                }).then((response) => {
                    vm.conservation_status_obj = response.body;
                    vm.original_conservation_status_obj = helpers.copyObject(response.body);
                    vm.updateAssignedOfficerSelect();
                }, (error) => {
                    vm.conservation_status_obj = helpers.copyObject(vm.original_conservation_status_obj)
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
                vm.$http.get(helpers.add_endpoint_json(api_endpoints.conservation_status, (vm.conservation_status_obj.id + '/unassign')))
                    .then((response) => {
                        vm.conservation_status_obj = response.body;
                        vm.original_conservation_status_obj = helpers.copyObject(response.body);
                        vm.updateAssignedOfficerSelect();
                    }, (error) => {
                        vm.conservation_status_obj = helpers.copyObject(vm.original_conservation_status_obj)

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
        updateAssignedOfficerSelect: function () {
            let vm = this;
            if (vm.conservation_status_obj.processing_status == 'With Approver') {
                $(vm.$refs.assigned_officer).val(vm.conservation_status_obj.assigned_approver);
                $(vm.$refs.assigned_officer).trigger('change');
            }
            else {
                $(vm.$refs.assigned_officer).val(vm.conservation_status_obj.assigned_officer);
                $(vm.$refs.assigned_officer).trigger('change');
            }
        },
        assignRequestUser: function () {
            let vm = this;
            vm.$http.get(helpers.add_endpoint_json(api_endpoints.conservation_status, (vm.conservation_status_obj.id + '/assign_request_user')))
                .then((response) => {
                    vm.conservation_status_obj = response.body;
                    vm.original_conservation_status_obj = helpers.copyObject(response.body);
                    vm.updateAssignedOfficerSelect();

                }, (error) => {
                    vm.conservation_status_obj = helpers.copyObject(vm.original_conservation_status_obj)
                    vm.updateAssignedOfficerSelect();
                    swal.fire({
                        title: 'Application Error',
                        text: helpers.apiVueResourceError(error),
                        icon: 'error',
                        confirmButtonColor: '#226fbb'
                    });
                });
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
                placeholder: "Select Officer"
            }).
                on("select2:select", function (e) {
                    var selected = $(e.currentTarget);
                    if (vm.conservation_status_obj.processing_status == 'With Approver') {
                        vm.conservation_status_obj.assigned_approver = selected.val();
                    }
                    else {
                        vm.conservation_status_obj.assigned_officer = selected.val();
                    }
                    vm.assignTo();
                }).on("select2:unselecting", function (e) {
                    var self = $(this);
                    setTimeout(() => {
                        self.select2('close');
                    }, 0);
                }).on("select2:unselect", function (e) {
                    var selected = $(e.currentTarget);
                    if (vm.conservation_status_obj.processing_status == 'With Approver') {
                        vm.conservation_status_obj.assigned_approver = null;
                    }
                    else {
                        vm.conservation_status_obj.assigned_officer = null;
                    }
                    vm.assignTo();
                });
        },
        fetchDeparmentUsers: function () {
            let vm = this;
            vm.loading.push('Loading Department Users');
            vm.$http.get(api_endpoints.department_users).then((response) => {
                vm.department_users = response.body
                vm.loading.splice('Loading Department Users', 1);
            }, (error) => {
                console.log(error);
                vm.loading.splice('Loading Department Users', 1);
            })
        },
        initialiseSelects: function () {
            let vm = this;
            if (!vm.initialisedSelects) {
                $(vm.$refs.department_users).select2({
                    minimumInputLength: 2,
                    "theme": "bootstrap-5",
                    allowClear: true,
                    placeholder: "Search for a Referree",
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
                        vm.$nextTick(() => {
                            vm.$refs.referral_text.focus();
                        });
                    })
                    .on("select2:unselect", function (e) {
                        var selected = $(e.currentTarget);
                        vm.selected_referral = null;
                    })
                vm.initialiseAssignedOfficerSelect();
                vm.initialisedSelects = true;
            }
        },
        sendReferral: function () {
            let vm = this;
            let formData = new FormData(vm.form);
            vm.sendingReferral = true;
            let payload = new Object();
            Object.assign(payload, vm.conservation_status_obj);
            vm.$http.post(vm.species_community_cs_form_url, payload).then(res => {
                let data = { 'email': vm.selected_referral, 'text': vm.referral_text };
                vm.$http.post(helpers.add_endpoint_json(api_endpoints.conservation_status, (vm.conservation_status_obj.id + '/assesor_send_referral')), JSON.stringify(data), {
                    emulateJSON: true
                }).then((response) => {
                    vm.sendingReferral = false;
                    vm.original_conservation_status_obj = helpers.copyObject(response.body);
                    vm.conservation_status_obj = response.body;
                    swal.fire({
                        title: 'Referral Sent',
                        text: 'The referral has been sent to ' + vm.department_users.find(d => d.email == vm.selected_referral).name,
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
            });
        },
        remindReferral: function (r) {
            let vm = this;
            vm.$http.get(helpers.add_endpoint_json(api_endpoints.cs_referrals, r.id + '/remind')).then(response => {
                vm.original_conservation_status_obj = helpers.copyObject(response.body);
                vm.conservation_status_obj = response.body;
                swal.fire({
                    title: 'Referral Reminder',
                    text: 'A reminder has been sent to ' + vm.department_users.find(d => d.id == r.referral).name,
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
            vm.$http.get(helpers.add_endpoint_json(api_endpoints.cs_referrals, r.id + '/recall')).then(response => {
                vm.original_conservation_status_obj = helpers.copyObject(response.body);
                vm.conservation_status_obj = response.body;
                $(".popover").hide()
                vm.enablePopovers();
                swal.fire({
                    title: 'Referral Recall',
                    text: 'The referral has been recalled from ' + vm.department_users.find(d => d.id == r.referral).name,
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

            vm.$http.get(helpers.add_endpoint_json(api_endpoints.cs_referrals, r.id + '/resend')).then(response => {
                vm.original_conservation_status_obj = helpers.copyObject(response.body);
                vm.conservation_status_obj = response.body;
                $(".popover").hide()
                vm.enablePopovers();
                swal.fire({
                    title: 'Referral Resent',
                    text: 'The referral has been resent to ' + vm.department_users.find(d => d.id == r.referral).name,
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
        switchStatus: function (status) {
            let vm = this;
            if (vm.conservation_status_obj.processing_status == 'With Approver' && status == 'with_assessor') {
                let data = { 'status': status, 'approver_comment': vm.approver_comment }
                vm.$http.post(helpers.add_endpoint_json(api_endpoints.conservation_status, (vm.conservation_status_obj.id + '/switch_status')), JSON.stringify(data), {
                    emulateJSON: true,
                })
                    .then((response) => {
                        vm.conservation_status_obj = response.body;
                        vm.original_conservation_status_obj = helpers.copyObject(response.body);
                        vm.approver_comment = '';
                        vm.$nextTick(() => {
                            vm.initialiseAssignedOfficerSelect(true);
                            vm.updateAssignedOfficerSelect();
                        });
                        vm.$router.push({ path: '/internal/conservation-status/' });
                    }, (error) => {
                        vm.conservation_status_obj = helpers.copyObject(vm.original_conservation_status_obj)
                        swal.fire({
                            title: 'Application Error',
                            text: helpers.apiVueResourceError(error),
                            icon: 'error',
                            confirmButtonColor: '#226fbb'
                        });
                    });
            }
            else {
                let data = { 'status': status, 'approver_comment': vm.approver_comment }
                vm.changingStatus = true;
                vm.$http.post(helpers.add_endpoint_json(api_endpoints.conservation_status, (vm.conservation_status_obj.id + '/switch_status')), JSON.stringify(data), {
                    emulateJSON: true,
                })
                    .then((response) => {
                        vm.conservation_status_obj = response.body;
                        vm.original_conservation_status_obj = helpers.copyObject(response.body);
                        vm.approver_comment = '';
                        vm.$nextTick(() => {
                            vm.initialiseAssignedOfficerSelect(true);
                            vm.updateAssignedOfficerSelect();
                        });
                        vm.changingStatus = false;
                    }, (error) => {
                        vm.conservation_status_obj = helpers.copyObject(vm.original_conservation_status_obj)
                        swal.fire({
                            title: 'Application Error',
                            text: helpers.apiVueResourceError(error),
                            icon: 'error',
                            confirmButtonColor: '#226fbb'
                        });
                        vm.changingStatus = false;
                    });
            }
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
    },
    mounted: function () {
        let vm = this;
        vm.fetchDeparmentUsers();
    },
    created: function () {
        if (!this.conservation_status_obj) {
            this.$http.get('/api/conservation_status/' + this.$route.params.conservation_status_id + '/internal_conservation_status.json').then(res => {
                this.conservation_status_obj = res.body.conservation_status_obj;
            },
                err => {
                    console.log(err);
                });
        }
    },
    updated: function () {
        let vm = this;
        this.$nextTick(() => {
            vm.initialiseSelects();
            vm.form = document.forms.new_conservation_status;
        });
    },
    beforeRouteEnter: function (to, from, next) {
        Vue.http.get(`/api/conservation_status/${to.params.conservation_status_id}/internal_conservation_status.json`).then(res => {
            next(vm => {
                vm.conservation_status_obj = res.body.conservation_status_obj;
            });
        },
            err => {
                console.log(err);
            });
    },
}
</script>
<style scoped>
.top-buffer-s {
    margin-top: 10px;
}

.actionBtn {
    cursor: pointer;
}

.hidePopover {
    display: none;
}

.separator {
    border: 1px solid;
    margin-top: 15px;
    margin-bottom: 10px;
    width: 100%;
}
</style>
