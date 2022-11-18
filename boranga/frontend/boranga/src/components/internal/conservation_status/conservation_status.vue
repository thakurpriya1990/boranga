<template lang="html">
    <div v-if="conservation_status_obj" class="container" id="internalConservationStatus">
      <div class="row" style="padding-bottom: 50px;">
        <h3>{{ display_number }} - {{display_name }}</h3>
        
        <div v-if="!comparing" class="col-md-3">
           <!-- TODO -->

           <CommsLogs
                :comms_url="comms_url"
                :logs_url="logs_url"
                :comms_add_url="comms_add_url"
                :disable_add_entry="false"
            />

            <Submission v-if="canSeeSubmission"
                :submitter_first_name="submitter_first_name"
                :submitter_last_name="submitter_last_name"
                :lodgement_date="conservation_status_obj.lodgement_date"
                class="mt-2"
            />
            
            <div class="top-buffer-s">
                <div class="card card-default">
                    <div class="card-header">
                        Workflow 
                    </div>
                     <div class="card-body card-collapse">
                        <div class="row">
                            <div class="col-sm-12">
                                <strong>Status</strong><br/>
                                {{ conservation_status_obj.processing_status }}
                            </div>
                            <div class="col-sm-12">
                                <div class="separator"></div>
                            </div>
                            <template v-if="conservation_status_obj.processing_status == 'With Assessor' || conservation_status_obj.processing_status == 'With Referral'">
                                <div class="col-sm-12 top-buffer-s">
                                    <strong>Referrals</strong><br/>
                                    <div class="form-group">

                                        <select :disabled="!canLimitedAction" ref="department_users" class="form-control">
                                            <option value="null"></option>
                                            <!-- <option v-for="user in department_users" :value="user.email" :key="user.id">{{user.name}}</option> -->
                                        </select>

                                        <template v-if='!sendingReferral'>
                                            <template v-if="selected_referral">
                                                <label class="control-label pull-left"  for="Name">Comments</label>
                                                <textarea class="form-control" name="name" v-model="referral_text"></textarea>
                                                <a v-if="canLimitedAction" @click.prevent="sendReferral()" class="actionBtn pull-right">Send</a>
                                            </template>
                                        </template>
                                        <template v-else>
                                            <span v-if="canLimitedAction" @click.prevent="sendReferral()" disabled class="actionBtn text-primary pull-right">
                                                Sending Referral&nbsp;
                                                <i class="fa fa-circle-o-notch fa-spin fa-fw"></i>
                                            </span>
                                        </template>
                                    </div>
                                    <table class="table small-table">
                                        <tr>
                                            <th>Referral</th>
                                            <th>Status/Action</th>
                                        </tr>
                                        <tr v-for="r in conservation_status_obj.latest_referrals">
                                            <td>
                                                <small><strong>{{r.referral_obj.first_name}} {{ r.referral_obj.last_name }}</strong></small><br/>
                                                <small><strong>{{r.lodged_on | formatDate}}</strong></small>
                                            </td>
                                            <td>
                                                <small><strong>{{r.processing_status}}</strong></small><br/>
                                                <template v-if="r.processing_status == 'Awaiting'">
                                                    <small v-if="canLimitedAction"><a @click.prevent="remindReferral(r)" href="#">Remind</a> / <a @click.prevent="recallReferral(r)"href="#">Recall</a></small>
                                                </template>
                                                <template v-else>
                                                    <small v-if="canLimitedAction"><a @click.prevent="resendReferral(r)" href="#">Resend</a></small>
                                                </template>
                                            </td>
                                        </tr>
                                    </table>
                                    <template>
                                            
                                    </template>
                                    <CSMoreReferrals @refreshFromResponse="refreshFromResponse" :conservation_status_obj="conservation_status_obj" :canAction="canLimitedAction" :isFinalised="isFinalised" :referral_url="referralListURL"/>
                                </div>
                                <div class="col-sm-12">
                                    <div class="separator"></div>
                                </div>
                            </template>
                            <div v-if="!isFinalised" class="col-sm-12 top-buffer-s">
                                <strong>Currently assigned to</strong><br/>
                                <div class="form-group">
                                    <template v-if="conservation_status_obj.processing_status == 'With Approver'">
                                        <select ref="assigned_officer" :disabled="!canAction" class="form-control" v-model="conservation_status_obj.assigned_approver">
                                            <option v-for="member in conservation_status_obj.allowed_assessors" :value="member.id">{{member.first_name}} {{member.last_name}}</option>
                                        </select>
                                        <a v-if="canAssess && conservation_status_obj.assigned_approver != conservation_status_obj.current_assessor.id" @click.prevent="assignRequestUser()" class="actionBtn pull-right">Assign to me</a>
                                    </template>
                                    <template v-else>
                                        <select ref="assigned_officer" :disabled="!canAction" class="form-control" v-model="conservation_status_obj.assigned_officer">
                                            <option v-for="member in conservation_status_obj.allowed_assessors" :value="member.id">{{member.first_name}} {{member.last_name}}</option>
                                        </select>
                                        <a v-if="canAssess && conservation_status_obj.assigned_officer != conservation_status_obj.current_assessor.id" @click.prevent="assignRequestUser()" class="actionBtn pull-right">Assign to me</a>
                                    </template>
                                </div>
                            </div>
                            <div class="col-sm-12">
                                <div class="separator"></div>
                            </div>
                            <div class="col-sm-12 top-buffer-s" v-if="!isFinalised && canAction">
                                <template v-if="conservation_status_obj.processing_status == 'With Assessor' || conservation_status_obj.processing_status == 'With Referral'">
                                    <div class="row">
                                        <div class="col-sm-12">
                                            <strong>Action</strong><br/>
                                        </div>
                                    </div>
                                    <div class="row">
                                        <div class="col-sm-12">
                                            <button style="width:80%;" class="btn btn-primary top-buffer-s" :disabled="conservation_status_obj.can_user_edit" @click.prevent="amendmentRequest()">Request Amendment</button><br/>
                                        </div>
                                    </div>
                                    <div class="row">
                                        <div class="col-sm-12">
                                            <button style="width:80%;" class="btn btn-primary top-buffer-s" :disabled="conservation_status_obj.can_user_edit" @click.prevent="proposedDecline()">Propose to Decline</button>
                                        </div>
                                    </div>
                                    <div class="row">
                                        <div class="col-sm-12">
                                            <button style="width:80%;" class="btn btn-primary top-buffer-s" :disabled="conservation_status_obj.can_user_edit" @click.prevent="proposedApproval()">Propose to Approve</button><br/>
                                        </div>
                                    </div>
                                </template>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
            
           
        </div>

            
        <div v-if="!comparing" class="col-md-1"></div>
        <!--<div class="col-md-8">-->
        <div :class="class_ncols">
            <div class="row">
                <template>
                    <div class="">
                        <div class="row">
                            <form :action="species_community_cs_form_url" method="post" name="new_conservation_status" enctype="multipart/form-data">
                                <ProposalConservationStatus 
                                    ref="conservation_status" 
                                    :conservation_status_obj="conservation_status_obj" 
                                    :canEditStatus="canEditStatus"
                                    id="ConservationStatusStart" 
                                    :is_internal="true">
                                    <!-- TODO add hasAssessorMode props to ProposalConservationStatus -->
                                </ProposalConservationStatus>
                                <input type="hidden" name="csrfmiddlewaretoken" :value="csrf_token"/>
                                <input type='hidden' name="conservation_status_id" :value="1" />
                                <div class="row" style="margin-bottom: 50px">
                                    <div class="navbar fixed-bottom" style="background-color: #f5f5f5;">
                                        <!-- commented the below as internal is no proposal submission just saving proposal changes -->
                                        <!-- <div v-if="hasAssessorMode" class="container">
                                            <div class="col-md-12 text-end">
                                                <button v-if="savingConservationStatus" class="btn btn-primary pull-right" style="margin-top:5px;" disabled >Save and Continue&nbsp;
                                                <i class="fa fa-circle-o-notch fa-spin fa-fw"></i></button>
                                                <button v-else class="btn btn-primary pull-right" style="margin-top:5px;" 
                                                @click.prevent="save()" :disabled="saveExitConservationStatus || submitConservationStatus">Save and Continue</button>
                                                
                                                <button v-if="saveExitConservationStatus" class="btn btn-primary pull-right" style="margin-top:5px;" disabled >Save and Exit&nbsp;
                                                <i class="fa fa-circle-o-notch fa-spin fa-fw"></i></button>
                                                <button v-else class="btn btn-primary pull-right" style="margin-top:5px;" 
                                                @click.prevent="save_exit()" :disabled="savingConservationStatus || submitConservationStatus">Save and Exit</button>

                                                <button v-if="submitConservationStatus" class="btn btn-primary pull-right" style="margin-top:5px;" disabled >Submit&nbsp;
                                                <i class="fa fa-circle-o-notch fa-spin fa-fw"></i></button>
                                                <button v-else class="btn btn-primary pull-right" style="margin-top:5px;" 
                                                @click.prevent="submit()" :disbaled="saveExitConservationStatus || savingConservationStatus">Submit</button>
                                            </div>
                                        </div> -->

                                        <div v-if="hasAssessorMode" class="container">
                                            <div class="col-md-12 text-end">
                                                <button v-if="savingConservationStatus" class="btn btn-primary pull-right" style="margin-top:5px;" disabled >Save Changes&nbsp;
                                                <i class="fa fa-circle-o-notch fa-spin fa-fw"></i></button>
                                                <button v-else class="btn btn-primary pull-right" style="margin-top:5px;" @click.prevent="save()">Save Changes</button>
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
        <AmendmentRequest ref="amendment_request" :conservation_status_id="conservation_status_obj.id" @refreshFromResponse="refreshFromResponse"></AmendmentRequest>
        <ProposedDecline ref="proposed_decline" :processing_status="conservation_status_obj.processing_status" :conservation_status_id="conservation_status_obj.id" @refreshFromResponse="refreshFromResponse"></ProposedDecline>
        
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

import CSMoreReferrals from '@common-utils/conservation_status/cs_more_referrals.vue'
import ResponsiveDatatablesHelper from "@/utils/responsive_datatable_helper.js"
import ProposalConservationStatus from '@/components/form_conservation_status.vue'
import {
    api_endpoints,
    helpers
}
from '@/utils/hooks'
export default {
    name: 'InternalConservationStatus',
    data: function() {
        let vm = this;
        return {
            "conservation_status_obj":null,
            "original_conservation_status_obj": null,
            "loading": [],
            form: null,
            savingConservationStatus:false,
            /*saveExitConservationStatus: false,
            submitConservationStatus: false,*/
            department_users : [],
            selected_referral: '',
            referral_text: '',
            sendingReferral: false,
            
            DATE_TIME_FORMAT: 'DD/MM/YYYY HH:mm:ss',
            comms_url: helpers.add_endpoint_json(api_endpoints.conservation_status,vm.$route.params.conservation_status_id+'/comms_log'),
            comms_add_url: helpers.add_endpoint_json(api_endpoints.conservation_status,vm.$route.params.conservation_status_id+'/add_comms_log'),
            logs_url: helpers.add_endpoint_json(api_endpoints.conservation_status,vm.$route.params.conservation_status_id+'/action_log'),
            comparing: false,
            initialisedSelects: false,
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
    },
    filters: {
        formatDate: function(data){
            return data ? moment(data).format('DD/MM/YYYY HH:mm:ss'): '';
        }
    },
    watch: {
    },
    computed: {
        csrf_token: function() {
          return helpers.getCookie('csrftoken')
        },
        referralListURL: function(){
            return this.conservation_status_obj!= null ? helpers.add_endpoint_json(api_endpoints.cs_referrals,'datatable_list')+'?conservation_status='+this.conservation_status_obj.id : '';
        },
        species_community_cs_form_url: function() {
          /*return (this.conservation_status_obj.group_type === "community") ? 
                  `/api/community/${this.conservation_status_obj.id}/community_save.json`: 
                  `/api/species_conservation_status/${this.conservation_status_obj.id}/species_conservation_status_save.json`;*/
            return `/api/conservation_status/${this.conservation_status_obj.id}/conservation_status_save.json`;
        },
        display_number: function() {
            return this.conservation_status_obj.conservation_status_number;
        },
        display_name: function() {
            return (this.conservation_status_obj.group_type === "community") ? 
                    this.conservation_status_obj.conservation_status_number : 
                    this.conservation_status_obj.conservation_status_number;
        },
        class_ncols: function(){
            return this.comparing ? 'col-md-12' : 'col-md-8';
        },
        submitter_first_name: function(){
            if (this.conservation_status_obj.submitter){
                return this.conservation_status_obj.submitter.first_name
            } else {
                return ''
            }
        },
        submitter_last_name: function(){
            if (this.conservation_status_obj.submitter){
                return this.conservation_status_obj.submitter.last_name
            } else {
                return ''
            }
        },
        submitter_id: function(){
            if (this.conservation_status_obj.submitter){
                return this.conservation_status_obj.submitter.id
            } else {
                //eturn this.conservation_status_obj.applicant_obj.id
            }
        },
        submitter_email: function(){
            if (this.conservation_status_obj.submitter){
                return this.conservation_status_obj.submitter.email
            } else {
                //return this.conservation_status_obj.applicant_obj.email
            }
        },
        canSeeSubmission: function(){
            /*return this.proposal && (this.proposal.processing_status != 'With Assessor (Requirements)' && this.proposal.processing_status != 'With Approver' && !this.isFinalised)*/

            return true; // TODO the Processing Status based value
        },
        canEditStatus: function(){
            return this.conservation_status_obj ? this.conservation_status_obj.can_user_edit: 'false';
        },
        isFinalised: function(){
            return this.conservation_status_obj.processing_status == 'Declined' || this.conservation_status_obj.processing_status == 'Approved';
        },
        canLimitedAction: function(){
            if (this.conservation_status_obj.processing_status == 'With Approver'){
                return this.conservation_status_obj && (this.conservation_status_obj.processing_status == 'With Assessor' || this.conservation_status_obj.processing_status == 'With Referral') && !this.isFinalised && !this.conservation_status_obj.can_user_edit && (this.conservation_status_obj.current_assessor.id == this.conservation_status_obj.assigned_approver || this.conservation_status_obj.assigned_approver == null ) && this.conservation_status_obj.assessor_mode.assessor_can_assess? true : false;
            }
            else{
                return this.conservation_status_obj && (this.conservation_status_obj.processing_status == 'With Assessor' || this.conservation_status_obj.processing_status == 'With Referral') && !this.isFinalised && !this.conservation_status_obj.can_user_edit && (this.conservation_status_obj.current_assessor.id == this.conservation_status_obj.assigned_officer || this.conservation_status_obj.assigned_officer == null ) && this.conservation_status_obj.assessor_mode.assessor_can_assess? true : false;
            }
        },
        canAction: function(){
            if (this.conservation_status_obj.processing_status == 'With Approver'){
                return this.conservation_status_obj && (this.conservation_status_obj.processing_status == 'With Approver' || this.conservation_status_obj.processing_status == 'With Assessor') && !this.isFinalised && !this.conservation_status_obj.can_user_edit && (this.conservation_status_obj.current_assessor.id == this.conservation_status_obj.assigned_approver || this.conservation_status_obj.assigned_approver == null ) && this.conservation_status_obj.assessor_mode.assessor_can_assess? true : false;
            }
            else{
                return this.conservation_status_obj && (this.conservation_status_obj.processing_status == 'With Approver' || this.conservation_status_obj.processing_status == 'With Assessor') && !this.isFinalised && !this.conservation_status_obj.can_user_edit && (this.conservation_status_obj.current_assessor.id == this.conservation_status_obj.assigned_officer || this.conservation_status_obj.assigned_officer == null ) && this.conservation_status_obj.assessor_mode.assessor_can_assess? true : false;
            }
        },
        canAssess: function(){
            return this.conservation_status_obj && this.conservation_status_obj.assessor_mode.assessor_can_assess ? true : false;
        },
        hasAssessorMode:function(){
            return this.conservation_status_obj && this.conservation_status_obj.assessor_mode.has_assessor_mode ? true : false;
        },
    },
    methods: {
        commaToNewline(s){
            return s.replace(/[,;]/g, '\n');
        },
        amendmentRequest: function(){
            //this.save_wo();
            let value = '';
            value = $('#assessor_deficiencies').val();
            /*$('#assessor_deficiencies').each((i,d) => {
                values +=  $(d).val() != '' ? `Question - ${$(d).data('question')}\nDeficiency - ${$(d).val()}\n\n`: '';
            }); */
            this.$refs.amendment_request.amendment.text = value;
            
            this.$refs.amendment_request.isModalOpen = true;
        },
        proposedDecline: function(){
            this.save_wo();
            //this.$refs.proposed_decline.decline = this.conservation_status_obj.proposaldeclineddetails != null ? helpers.copyObject(this.conservation_status_obj.proposaldeclineddetails): {};
            this.$refs.proposed_decline.isModalOpen = true;
        },
        save: async function() {
            let vm = this;
            vm.savingConservationStatus=true;
            let payload = new Object();
            Object.assign(payload, vm.conservation_status_obj);
            vm.$http.post(vm.species_community_cs_form_url,payload).then(res=>{
              swal(
                'Saved',
                'Your changes has been saved',
                'success'
              )
              vm.savingConservationStatus=false;
          },err=>{
            vm.savingConservationStatus=false;
          });
        },
        /*save_exit: async function(){
            let vm = this;
            vm.saveExitConservationStatus=true;
            const res = await this.save();
            vm.saveExitConservationStatus=false;
            // redirect back to dashboard
            if (res.ok) {
                vm.$router.push({
                    name: 'internal-conservation_status-dash'
                });
            }
        },*/
        /*submit: async function(){
            let vm = this
            vm.submitConservationStatus=true;
            try {
                await swal({
                    title:"Edit Conservation Status",
                    text: "Are you sure you want to submit the changes",
                    type: "question",
                    showCancelButton: true,
                    confirmButtonText: "submit"
                })
            } catch (cancel) {
                vm.submitConservationStatus = false;
                return;
            }

            if(vm.submitConservationStatus){
                try {
                    const res = await this.save();
                    if (res.ok) {
                        vm.$router.push({
                          name: 'internal-conservation_status-dash'
                        });
                    }
                } catch(err) {
                    console.log(err)
                    console.log(typeof(err.body))
                    await swal({
                        title: 'Submit Error',
                        html: helpers.formatError(err),
                        type: "error",
                    })
                    vm.submitConservationStatus=false;
                    //this.submitting = false;
                }
            }
        },*/
        save_wo: function() {
            let vm = this;
            let payload = new Object();
            Object.assign(payload, vm.conservation_status_obj);
            vm.$http.post(vm.species_community_cs_form_url,payload).then(res=>{
                },err=>{
            });
        },
        refreshFromResponse:function(response){
            let vm = this;
            vm.original_conservation_status_obj = helpers.copyObject(response.body);
            vm.conservation_status_obj = helpers.copyObject(response.body);
            // vm.proposal.org_applicant.address = vm.proposal.org_applicant.address != null ? vm.proposal.org_applicant.address : {};
            vm.$nextTick(() => {
                vm.initialiseAssignedOfficerSelect(true);
                vm.updateAssignedOfficerSelect();
            });
        },
        assignTo: function(){
            let vm = this;
            let unassign = true;
            let data = {};
            if (vm.conservation_status_obj.processing_status == 'With Approver'){
                unassign = vm.conservation_status_obj.assigned_approver != null && vm.conservation_status_obj.assigned_approver != 'undefined' ? false: true;
                data = {'assessor_id': vm.conservation_status_obj.assigned_approver};
            }
            else{
                unassign = vm.conservation_status_obj.assigned_officer != null && vm.conservation_status_obj.assigned_officer != 'undefined' ? false: true;
                data = {'assessor_id': vm.conservation_status_obj.assigned_officer};
            }
            if (!unassign){
                vm.$http.post(helpers.add_endpoint_json(api_endpoints.conservation_status,(vm.conservation_status_obj.id+'/assign_to')),JSON.stringify(data),{
                    emulateJSON:true
                }).then((response) => {
                    vm.conservation_status_obj = response.body;
                    vm.original_conservation_status_obj = helpers.copyObject(response.body);
                    
                    // vm.proposal.org_applicant.address = vm.proposal.org_applicant.address != null ? vm.proposal.org_applicant.address : {};
                    vm.updateAssignedOfficerSelect();
                    //vm.fetchProposalParks(vm.proposal.id);
                }, (error) => {
                    vm.conservation_status_obj = helpers.copyObject(vm.original_conservation_status_obj)
                   /* vm.conservation_status_obj.org_applicant.address = vm.conservation_status_obj.org_applicant.address != null ? vm.conservation_status_obj.org_applicant.address : {};*/
                    
                    vm.updateAssignedOfficerSelect();
                    //vm.fetchProposalParks(vm.proposal.id);
                    swal(
                        'Application Error',
                        helpers.apiVueResourceError(error),
                        'error'
                    )
                });
            }
            else{
                vm.$http.get(helpers.add_endpoint_json(api_endpoints.conservation_status,(vm.conservation_status_obj.id+'/unassign')))
                .then((response) => {
                    vm.conservation_status_obj = response.body;
                    vm.original_conservation_status_obj = helpers.copyObject(response.body);
                    
                    // vm.proposal.org_applicant.address = vm.proposal.org_applicant.address != null ? vm.proposal.org_applicant.address : {};
                    vm.updateAssignedOfficerSelect();
                    //vm.fetchProposalParks(vm.proposal.id);
                }, (error) => {
                    vm.conservation_status_obj = helpers.copyObject(vm.original_conservation_status_obj)
                    /*vm.conservation_status_obj.org_applicant.address = vm.conservation_status_obj.org_applicant.address != null ? vm.conservation_status_obj.org_applicant.address : {};*/
                    
                    vm.updateAssignedOfficerSelect();
                    //vm.fetchProposalParks(vm.proposal.id);
                    swal(
                        'Application Error',
                        helpers.apiVueResourceError(error),
                        'error'
                    )
                });
            }
        },
        updateAssignedOfficerSelect:function(){
            let vm = this;
            if (vm.conservation_status_obj.processing_status == 'With Approver'){
                $(vm.$refs.assigned_officer).val(vm.conservation_status_obj.assigned_approver);
                $(vm.$refs.assigned_officer).trigger('change');
            }
            else{
                $(vm.$refs.assigned_officer).val(vm.conservation_status_obj.assigned_officer);
                $(vm.$refs.assigned_officer).trigger('change');
            }
        },
        assignRequestUser: function(){
            let vm = this;
            vm.$http.get(helpers.add_endpoint_json(api_endpoints.conservation_status,(vm.conservation_status_obj.id+'/assign_request_user')))
            .then((response) => {
                vm.conservation_status_obj = response.body;
                //vm.fetchProposalParks(vm.proposal.id);
                vm.original_conservation_status_obj = helpers.copyObject(response.body);
                // vm.proposal.org_applicant.address = vm.proposal.org_applicant.address != null ? vm.proposal.org_applicant.address : {};
                vm.updateAssignedOfficerSelect();

            }, (error) => {
                vm.conservation_status_obj = helpers.copyObject(vm.original_conservation_status_obj)
                // vm.proposal.org_applicant.address = vm.proposal.org_applicant.address != null ? vm.proposal.org_applicant.address : {};
                vm.updateAssignedOfficerSelect();
                swal(
                    'Application Error',
                    helpers.apiVueResourceError(error),
                    'error'
                )
            });
        },
        initialiseAssignedOfficerSelect:function(reinit=false){
            let vm = this;
            if (reinit){
                $(vm.$refs.assigned_officer).data('select2') ? $(vm.$refs.assigned_officer).select2('destroy'): '';
            }
            // Assigned officer select
            $(vm.$refs.assigned_officer).select2({
                "theme": "bootstrap-5",
                allowClear: true,
                placeholder:"Select Officer"
            }).
            on("select2:select",function (e) {
                var selected = $(e.currentTarget);
                if (vm.conservation_status_obj.processing_status == 'With Approver'){
                    vm.conservation_status_obj.assigned_approver = selected.val();
                }
                else{
                    vm.conservation_status_obj.assigned_officer = selected.val();
                }
                vm.assignTo();
            }).on("select2:unselecting", function(e) {
                var self = $(this);
                setTimeout(() => {
                    self.select2('close');
                }, 0);
            }).on("select2:unselect",function (e) {
                var selected = $(e.currentTarget);
                if (vm.conservation_status_obj.processing_status == 'With Approver'){
                    vm.conservation_status_obj.assigned_approver = null;
                }
                else{
                    vm.conservation_status_obj.assigned_officer = null;
                }
                vm.assignTo();
            });
        },
        fetchDeparmentUsers: function(){
            let vm = this;
            vm.loading.push('Loading Department Users');
            vm.$http.get(api_endpoints.department_users).then((response) => {
                vm.department_users = response.body
                vm.loading.splice('Loading Department Users',1);
            },(error) => {
                console.log(error);
                vm.loading.splice('Loading Department Users',1);
            })
        },
        initialiseSelects: function(){
            let vm = this;
            if (!vm.initialisedSelects){
                $(vm.$refs.department_users).select2({
                minimumInputLength: 2,
                "theme": "bootstrap-5",
                allowClear: true,
                placeholder:"Select Referrer",
                ajax: {
                    url: api_endpoints.users_api + '/get_department_users/',
                    dataType: 'json',
                    data: function(params) {
                        var query = {
                            term: params.term,
                            type: 'public',
                        }
                        return query;
                    },
                },
                })
                .on("select2:select", function (e) {
                    //var selected = $(e.currentTarget);
                    //vm.selected_referral = selected.val();
                    let data = e.params.data.id;
                    vm.selected_referral = data;
                })
                .on("select2:unselect",function (e) {
                    var selected = $(e.currentTarget);
                    vm.selected_referral = null;
                })
                vm.initialiseAssignedOfficerSelect();
                vm.initialisedSelects = true;
            }
        },
        sendReferral: function(){
            let vm = this;
            //vm.save_wo();
            //TODO in boranga below checkAssessorData()
            //vm.checkAssessorData();
            let formData = new FormData(vm.form);
            vm.sendingReferral = true;
            let payload = new Object();
            Object.assign(payload, vm.conservation_status_obj);
            vm.$http.post(vm.species_community_cs_form_url,payload).then(res=>{

            let data = {'email':vm.selected_referral, 'text': vm.referral_text};
            vm.$http.post(helpers.add_endpoint_json(api_endpoints.conservation_status,(vm.conservation_status_obj.id+'/assesor_send_referral')),JSON.stringify(data),{
                emulateJSON:true
            }).then((response) => {
                vm.sendingReferral = false;
                vm.original_conservation_status_obj = helpers.copyObject(response.body);
                vm.conservation_status_obj = response.body;
                swal(
                    'Referral Sent',
                    'The referral has been sent to '+vm.department_users.find(d => d.email == vm.selected_referral).name,
                    'success'
                )
                $(vm.$refs.department_users).val(null).trigger("change");
                vm.selected_referral = '';
                vm.referral_text = '';
            }, (error) => {
                console.log(error);
                swal(
                    'Referral Error',
                    helpers.apiVueResourceError(error),
                    'error'
                )
                vm.sendingReferral = false;
            });


          },err=>{
          });
        },
        remindReferral:function(r){
            let vm = this;

            vm.$http.get(helpers.add_endpoint_json(api_endpoints.cs_referrals,r.id+'/remind')).then(response => {
                vm.original_conservation_status_obj = helpers.copyObject(response.body);
                vm.conservation_status_obj = response.body;
                //vm.proposal.applicant.address = vm.proposal.applicant.address != null ? vm.proposal.applicant.address : {};
                swal(
                    'Referral Reminder',
                    'A reminder has been sent to '+vm.department_users.find(d => d.id == r.referral).name,
                    'success'
                )
            },
            error => {
                swal(
                    'Proposal Error',
                    helpers.apiVueResourceError(error),
                    'error'
                )
            });
        },
        recallReferral:function(r){
            let vm = this;
            swal({
                    title: "Loading...",
                    //text: "Loading...",
                    allowOutsideClick: false,
                    allowEscapeKey:false,
                    onOpen: () =>{
                        swal.showLoading()
                    }
            })

            vm.$http.get(helpers.add_endpoint_json(api_endpoints.cs_referrals,r.id+'/recall')).then(response => {
                swal.hideLoading();
                swal.close();
                vm.original_conservation_status_obj = helpers.copyObject(response.body);
                vm.conservation_status_obj = response.body;
                //vm.proposal.applicant.address = vm.proposal.applicant.address != null ? vm.proposal.applicant.address : {};
                swal(
                    'Referral Recall',
                    'The referall has been recalled from '+vm.department_users.find(d => d.id == r.referral).name,
                    'success'
                )
            },
            error => {
                swal(
                    'Proposal Error',
                    helpers.apiVueResourceError(error),
                    'error'
                )
            });
        },
        resendReferral:function(r){
            let vm = this;

            vm.$http.get(helpers.add_endpoint_json(api_endpoints.cs_referrals,r.id+'/resend')).then(response => {
                vm.original_conservation_status_obj = helpers.copyObject(response.body);
                vm.conservation_status_obj = response.body;
                //vm.proposal.applicant.address = vm.proposal.applicant.address != null ? vm.proposal.applicant.address : {};
                swal(
                    'Referral Resent',
                    'The referral has been resent to '+vm.department_users.find(d => d.id == r.referral).name,
                    'success'
                )
            },
            error => {
                swal(
                    'Proposal Error',
                    helpers.apiVueResourceError(error),
                    'error'
                )
            });
        },
    },
    mounted: function() {
        let vm = this;
        vm.fetchDeparmentUsers();
    },
    updated: function(){
        let vm = this;
        this.$nextTick(() => {
            vm.initialiseSelects();
            vm.form = document.forms.new_conservation_status;
        });
    },
    beforeRouteEnter: function(to, from, next) {
        //-------------get species_conservation_status object if received species id
        /*if(to.query.group_type_name === 'flora' || to.query.group_type_name === "fauna"){
            Vue.http.get(`/api/species_conservation_status/${to.params.conservation_status_id}/internal_species_conservation_status.json`).then(res => {
              next(vm => {
                vm.conservation_status_obj = res.body.species_conservation_status_obj; //--temp species_obj
              });
            },
            err => {
              console.log(err);
            });
        }
        //------get community_conservations_status object if received community id
        else{
            Vue.http.get(`/api/community_conservation_status/${to.params.conservation_status_id}/internal_community_conservation_status.json`).then(res => {
              next(vm => {
                vm.conservation_status_obj = res.body.community_conservation_status_obj; //--temp community_obj
              });
            },
            err => {
              console.log(err);
            });
        }*/
        Vue.http.get(`/api/conservation_status/${to.params.conservation_status_id}/internal_conservation_status.json`).then(res => {
              next(vm => {
                vm.conservation_status_obj = res.body.conservation_status_obj;
              });
            },
            err => {
              console.log(err);
            });
    },
    /*beforeRouteUpdate: function(to, from, next) {
          Vue.http.get(`/api/proposal/${to.params.conservation_status_id}.json`).then(res => {
              next(vm => {
                vm.proposal = res.body;
                vm.original_proposal = helpers.copyObject(res.body);
                
              });
            },
            err => {
              console.log(err);
            });
    }*/
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

.p-3 {
  padding: $spacer !important;
}
</style>
