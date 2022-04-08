<template lang="html">
    <div v-if="species" class="container" id="internalSpecies">
      <div class="row" style="padding-bottom: 50px;">
        <h3>{{ species.id }} - {{species.scientific_name }}</h3>
        <h4>{{species.conservation_category }}</h4>

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
                    :lodgement_date="proposal.lodgement_date"
                    class="mt-2"
                />
                <!-- ----- -->

                <!-- TODO
                <Workflow
                    ref='workflow'
                    :proposal="proposal"
                    :isFinalised="isFinalised"
                    :canAction="canAction"
                    :canAssess="canAssess"
                    :can_user_edit="proposal.can_user_edit"
                    @toggleProposal="toggleProposal"
                    @toggleRequirements="toggleRequirements"
                    @switchStatus="switchStatus"
                    @completeReferral="completeReferral"
                    @amendmentRequest="amendmentRequest"
                    @proposedDecline="proposedDecline"
                    @proposedApproval="proposedApproval"
                    @issueProposal="issueProposal"
                    @declineProposal="declineProposal"
                    @assignRequestUser="assignRequestUser"
                    @assignTo="assignTo"
                    class="mt-2"
                />
                -->
            </div>

            
        <div v-if="!comparing" class="col-md-1"></div>
        <!--<div class="col-md-8">-->
        <div :class="class_ncols">
            <div class="row">
                <template>
                    <div class="">
                        <div class="row">
                            <form :action="species_form_url" method="post" name="new_species" enctype="multipart/form-data">
                                <ProposalSpeciesCommunities 
                                    ref="species_communities" 
                                    :proposal="proposal" 
                                    :species="species" 
                                    id="speciesStart" 
                                    :canEditActivities="canEditActivities"  
                                    :is_internal="true">
                                </ProposalSpeciesCommunities>
                                    <input type="hidden" name="csrfmiddlewaretoken" :value="csrf_token"/>
                                    <input type='hidden' name="species_id" :value="1" />
                                    <div class="row" style="margin-bottom: 50px">
                                      <div class="navbar navbar-fixed-bottom" style="background-color: #f5f5f5;">
                                        <div class="navbar-inner">
                                            <p class="pull-right">
                                                <!-- <button v-if="savingProposal" class="btn btn-primary pull-right" style="margin-top:5px;" disabled >Save Changes&nbsp;
                                                <i class="fa fa-circle-o-notch fa-spin fa-fw"></i></button>
                                                 --><button class="btn btn-primary pull-right" style="margin-top:5px;" @click.prevent="save()">Submit</button>
                                            </p>
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
    </div>
</template>
<script>
//import Proposal from '../../form.vue'
import Vue from 'vue'
/*import ProposedDecline from './proposal_proposed_decline.vue'
import AmendmentRequest from './amendment_request.vue'
import Requirements from './proposal_requirements.vue'
import ProposedApproval from './proposed_issuance.vue'
import ApprovalScreen from './proposal_approval.vue'*/
import datatable from '@vue-utils/datatable.vue'
import CommsLogs from '@common-utils/comms_logs.vue'
import Submission from '@common-utils/submission.vue'
import Workflow from '@common-utils/workflow.vue'

//import MoreReferrals from '@common-utils/more_referrals.vue'
import ResponsiveDatatablesHelper from "@/utils/responsive_datatable_helper.js"
import ProposalSpeciesCommunities from '@/components/form_species_communities.vue'
import {
    api_endpoints,
    helpers
}
from '@/utils/hooks'
export default {
    name: 'InternalSpecies',
    data: function() {
        let vm = this;
        return {
            "proposal": null,
            "species":null,
            "original_proposal": null,
            "loading": [],
            selected_referral: '',
            approver_comment: '',
            form: null,
            proposal_parks:null,
            department_users : [],
            referral_recipient_groups : [],
            initialisedSelects: false,
            showingProposal:false,
            showingRequirements:false,
            savingProposal:false,
            changingStatus:false,
            requirementsComplete:true,
            
            DATE_TIME_FORMAT: 'DD/MM/YYYY HH:mm:ss',
            comms_url: helpers.add_endpoint_json(api_endpoints.proposals,vm.$route.params.species_id+'/comms_log'),
            comms_add_url: helpers.add_endpoint_json(api_endpoints.proposals,vm.$route.params.species_id+'/add_comms_log'),
            logs_url: helpers.add_endpoint_json(api_endpoints.proposals,vm.$route.params.species_id+'/action_log'),
            district_proposals_url: helpers.add_endpoint_json(api_endpoints.proposals,vm.$route.params.species_id+'/district_proposals'),
            comparing: false,
        }
    },
    components: {
        //Proposal,
        datatable,
        /*ProposedDecline,
        AmendmentRequest,
        Requirements,
        ProposedApproval,
        MoreReferrals,
        ApprovalScreen,*/
        CommsLogs,
        Submission,
        Workflow,
        ProposalSpeciesCommunities,
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
        species_form_url: function() {
          return (this.species) ? `/api/species/${this.species.id}/species_save.json` : '';
        },
        proposal_form_url: function() {
          return (this.proposal) ? `/api/proposal/${this.proposal.id}/assessor_save.json` : '';
        },
        isFinalised: function(){
            return this.proposal.processing_status == 'Declined' || this.proposal.processing_status == 'Approved' || this.proposal.processing_status == 'Awaiting Payment';
        },
        canAssess: function(){
            return this.proposal && this.proposal.assessor_mode.assessor_can_assess ? true : false;
        },
        hasAssessorMode:function(){
            return this.proposal && this.proposal.assessor_mode.has_assessor_mode ? true : false;
        },
        canEditActivities: function(){
            return this.proposal && this.proposal.assessor_mode && this.proposal.assessor_mode.assessor_mode && this.proposal.can_edit_activities;
        },
        canAction: function(){
            if (this.proposal.processing_status == 'With Approver'){
                return this.proposal && (this.proposal.processing_status == 'With Approver' || this.proposal.processing_status == 'With Assessor' || this.proposal.processing_status == 'With Assessor (Requirements)') && !this.isFinalised && !this.proposal.can_user_edit && (this.proposal.current_assessor.id == this.proposal.assigned_approver || this.proposal.assigned_approver == null ) && this.proposal.assessor_mode.assessor_can_assess? true : false;
            }
            else{
                return this.proposal && (this.proposal.processing_status == 'With QA Officer' || this.proposal.processing_status == 'On Hold' || this.proposal.processing_status == 'With Approver' || this.proposal.processing_status == 'With Assessor' || this.proposal.processing_status == 'With Assessor (Requirements)') && !this.isFinalised && !this.proposal.can_user_edit && (this.proposal.current_assessor.id == this.proposal.assigned_officer || this.proposal.assigned_officer == null ) && this.proposal.assessor_mode.assessor_can_assess? true : false;
            }
        },
        canSeeSubmission: function(){
            return this.proposal && (this.proposal.processing_status != 'With Assessor (Requirements)' && this.proposal.processing_status != 'With Approver' && !this.isFinalised)
        },
        isApprovalLevelDocument: function(){
            return this.proposal && this.proposal.processing_status == 'With Approver' && this.proposal.approval_level != null && this.proposal.approval_level_document == null ? true : false;
        },
        class_ncols: function(){
            return this.comparing ? 'col-md-12' : 'col-md-8';
        },
        application_type_tclass: function(){
          return api_endpoints.t_class;
        },
        application_type_filming: function(){
          return api_endpoints.filming;
        },
        application_type_event: function(){
          return api_endpoints.event;
        },
    },
    methods: {
        commaToNewline(s){
            return s.replace(/[,;]/g, '\n');
        },
        proposedDecline: function(){
            this.save_wo();
            this.$refs.proposed_decline.decline = this.proposal.proposaldeclineddetails != null ? helpers.copyObject(this.proposal.proposaldeclineddetails): {};
            this.$refs.proposed_decline.isModalOpen = true;
        },
        proposedApproval: function(){
            this.$refs.proposed_approval.approval = this.proposal.proposed_issuance_approval != null ? helpers.copyObject(this.proposal.proposed_issuance_approval) : {};
            if(this.proposal.application_type==this.application_type_tclass){
                if((this.proposal.proposed_issuance_approval==null || this.proposal.proposed_issuance_approval.expiry_date==null) && this.proposal.other_details.proposed_end_date!=null){
                    // this.$refs.proposed_approval.expiry_date=this.proposal.other_details.proposed_end_date;
                    var test_approval={
                        'start_date': this.proposal.other_details.nominated_start_date,
                        'expiry_date': this.proposal.other_details.proposed_end_date
                    };
                    this.$refs.proposed_approval.approval= helpers.copyObject(test_approval);
                }
                //this.$refs.proposed_approval.approval= helpers.copyObject(test_approval);
            }
            if(this.proposal.application_type==this.application_type_filming){
                if((this.proposal.proposed_issuance_approval==null || this.proposal.proposed_issuance_approval.expiry_date==null) && this.proposal.filming_activity.completion_date!=null && this.proposal.filming_activity.commencement_date!=null){
                    // this.$refs.proposed_approval.expiry_date=this.proposal.other_details.proposed_end_date;
                    var test_approval={
                        'start_date': this.proposal.filming_activity.commencement_date,
                        'expiry_date': this.proposal.filming_activity.completion_date
                    };
                    this.$refs.proposed_approval.approval= helpers.copyObject(test_approval);

                }
                //console.logt(test_approval)
                //this.$refs.proposed_approval.approval= helpers.copyObject(test_approval);
            }
            if(this.proposal.application_type==this.application_type_event){
                if((this.proposal.proposed_issuance_approval==null || this.proposal.proposed_issuance_approval.expiry_date==null) && this.proposal.event_activity.completion_date!=null && this.proposal.event_activity.commencement_date!=null){
                    // this.$refs.proposed_approval.expiry_date=this.proposal.other_details.proposed_end_date;
                    var test_approval={
                        'start_date': this.proposal.event_activity.commencement_date,
                        'expiry_date': this.proposal.event_activity.completion_date
                    };
                    this.$refs.proposed_approval.approval= helpers.copyObject(test_approval);

                }
                //console.logt(test_approval)
                //this.$refs.proposed_approval.approval= helpers.copyObject(test_approval);
            }

            this.$refs.proposed_approval.isModalOpen = true;
        },
        issueProposal:function(){
            //this.$refs.proposed_approval.approval = helpers.copyObject(this.proposal.proposed_issuance_approval);
            this.$refs.proposed_approval.approval = this.proposal.proposed_issuance_approval != null ? helpers.copyObject(this.proposal.proposed_issuance_approval) : {};
            this.$refs.proposed_approval.state = 'final_approval';
            this.$refs.proposed_approval.isApprovalLevelDocument = this.isApprovalLevelDocument;
            this.$refs.proposed_approval.isModalOpen = true;
        },
        declineProposal:function(){
            this.$refs.proposed_decline.decline = this.proposal.proposaldeclineddetails != null ? helpers.copyObject(this.proposal.proposaldeclineddetails): {};
            this.$refs.proposed_decline.isModalOpen = true;
        },
        amendmentRequest: function(){
            this.save_wo();
            let values = '';
            $('.deficiency').each((i,d) => {
                values +=  $(d).val() != '' ? `Question - ${$(d).data('question')}\nDeficiency - ${$(d).val()}\n\n`: '';
            }); 
            this.$refs.amendment_request.amendment.text = values;
            
            this.$refs.amendment_request.isModalOpen = true;
        },
        save: function(e) {
            let vm = this;
            vm.savingProposal=true;
            let payload = new Object();
            Object.assign(payload, vm.species);
            vm.$http.post(vm.species_form_url,payload).then(res=>{
                swal(
                'Saved',
                'Your changes has been saved',
                'success'
                )
                vm.savingProposal=false;
            },err=>{
                vm.savingProposal=false;
            });
        },
        save_wo: function() {
            let vm = this;
            let formData = new FormData(vm.form);
            vm.$http.post(vm.proposal_form_url,formData).then(res=>{
                },err=>{
            });
        },

        toggleProposal:function(){
            this.showingProposal = !this.showingProposal;
        },
        toggleRequirements:function(){
            this.showingRequirements = !this.showingRequirements;
        },
        updateAssignedOfficerSelect:function(){
            let vm = this;
            if (vm.proposal.processing_status == 'With Approver'){
                $(vm.$refs.assigned_officer).val(vm.proposal.assigned_approver);
                $(vm.$refs.assigned_officer).trigger('change');
            }
            else{
                $(vm.$refs.assigned_officer).val(vm.proposal.assigned_officer);
                $(vm.$refs.assigned_officer).trigger('change');
            }
        },
        assignRequestUser: function(){
            let vm = this;

            vm.$http.get(helpers.add_endpoint_json(api_endpoints.proposals,(vm.proposal.id+'/assign_request_user')))
            .then((response) => {
                vm.proposal = response.body;
                vm.fetchProposalParks(vm.proposal.id);
                vm.original_proposal = helpers.copyObject(response.body);
                // vm.proposal.org_applicant.address = vm.proposal.org_applicant.address != null ? vm.proposal.org_applicant.address : {};
                vm.updateAssignedOfficerSelect();

            }, (error) => {
                vm.proposal = helpers.copyObject(vm.original_proposal)
                // vm.proposal.org_applicant.address = vm.proposal.org_applicant.address != null ? vm.proposal.org_applicant.address : {};
                vm.updateAssignedOfficerSelect();
                swal(
                    'Application Error',
                    helpers.apiVueResourceError(error),
                    'error'
                )
            });
        },
        refreshFromResponse:function(response){
            let vm = this;
            vm.original_proposal = helpers.copyObject(response.body);
            vm.proposal = helpers.copyObject(response.body);
            vm.fetchProposalParks(vm.proposal.id);
            // vm.proposal.org_applicant.address = vm.proposal.org_applicant.address != null ? vm.proposal.org_applicant.address : {};
            vm.$nextTick(() => {
                vm.initialiseAssignedOfficerSelect(true);
                vm.updateAssignedOfficerSelect();
            });
        },
        refreshRequirements: function(bool){
              let vm=this;
              //vm.proposal.requirements_completed=bool;
              //console.log('here', bool);
              vm.requirementsComplete=bool;
          },
        assignTo: function(){
            let vm = this;
            let unassign = true;
            let data = {};
            if (vm.proposal.processing_status == 'With Approver'){
                unassign = vm.proposal.assigned_approver != null && vm.proposal.assigned_approver != 'undefined' ? false: true;
                data = {'assessor_id': vm.proposal.assigned_approver};
            }
            else{
                unassign = vm.proposal.assigned_officer != null && vm.proposal.assigned_officer != 'undefined' ? false: true;
                data = {'assessor_id': vm.proposal.assigned_officer};
            }
            if (!unassign){
                vm.$http.post(helpers.add_endpoint_json(api_endpoints.proposals,(vm.proposal.id+'/assign_to')),JSON.stringify(data),{
                    emulateJSON:true
                }).then((response) => {
                    vm.proposal = response.body;
                    vm.original_proposal = helpers.copyObject(response.body);
                    
                    // vm.proposal.org_applicant.address = vm.proposal.org_applicant.address != null ? vm.proposal.org_applicant.address : {};
                    vm.updateAssignedOfficerSelect();
                    vm.fetchProposalParks(vm.proposal.id);
                }, (error) => {
                    vm.proposal = helpers.copyObject(vm.original_proposal)
                    vm.proposal.org_applicant.address = vm.proposal.org_applicant.address != null ? vm.proposal.org_applicant.address : {};
                    
                    vm.updateAssignedOfficerSelect();
                    vm.fetchProposalParks(vm.proposal.id);
                    swal(
                        'Application Error',
                        helpers.apiVueResourceError(error),
                        'error'
                    )
                });
            }
            else{
                vm.$http.get(helpers.add_endpoint_json(api_endpoints.proposals,(vm.proposal.id+'/unassign')))
                .then((response) => {
                    vm.proposal = response.body;
                    vm.original_proposal = helpers.copyObject(response.body);
                    
                    // vm.proposal.org_applicant.address = vm.proposal.org_applicant.address != null ? vm.proposal.org_applicant.address : {};
                    vm.updateAssignedOfficerSelect();
                    vm.fetchProposalParks(vm.proposal.id);
                }, (error) => {
                    vm.proposal = helpers.copyObject(vm.original_proposal)
                    vm.proposal.org_applicant.address = vm.proposal.org_applicant.address != null ? vm.proposal.org_applicant.address : {};
                    
                    vm.updateAssignedOfficerSelect();
                    vm.fetchProposalParks(vm.proposal.id);
                    swal(
                        'Application Error',
                        helpers.apiVueResourceError(error),
                        'error'
                    )
                });
            }
        },
        switchStatus: function(status){
            let vm = this;
            //vm.save_wo();
            //let vm = this;
            if(vm.proposal.processing_status == 'With Assessor' && status == 'with_assessor_requirements'){
                vm.changingStatus=true;
            let formData = new FormData(vm.form);
            vm.$http.post(vm.proposal_form_url,formData).then(res=>{ //save Proposal before changing status so that unsaved assessor data is saved.
            
            let data = {'status': status, 'approver_comment': vm.approver_comment}
            vm.$http.post(helpers.add_endpoint_json(api_endpoints.proposals,(vm.proposal.id+'/switch_status')),JSON.stringify(data),{
                emulateJSON:true,
            })
            .then((response) => {
                vm.proposal = response.body;
                vm.original_proposal = helpers.copyObject(response.body);
                vm.fetchProposalParks(vm.proposal.id);
                // vm.proposal.org_applicant.address = vm.proposal.org_applicant.address != null ? vm.proposal.org_applicant.address : {};
                vm.approver_comment='';
                vm.$nextTick(() => {
                    vm.initialiseAssignedOfficerSelect(true);
                    vm.updateAssignedOfficerSelect();
                });

            }, (error) => {
                vm.proposal = helpers.copyObject(vm.original_proposal)
                vm.proposal.org_applicant.address = vm.proposal.org_applicant.address != null ? vm.proposal.org_applicant.address : {};
                vm.fetchProposalParks(vm.proposal.id);
                swal(
                    'Application Error',
                    helpers.apiVueResourceError(error),
                    'error'
                )
            });
              vm.changingStatus=false;
          },err=>{
            vm.changingStatus=false;
          });
            //vm.changingStatus=false;
        }
        //vm.changingStatus=false;
        //if approver is pushing back proposal to Assessor then navigate the approver back to dashboard page
        if(vm.proposal.processing_status == 'With Approver' && (status == 'with_assessor_requirements' || status=='with_assessor')) {
            let data = {'status': status, 'approver_comment': vm.approver_comment}
            vm.$http.post(helpers.add_endpoint_json(api_endpoints.proposals,(vm.proposal.id+'/switch_status')),JSON.stringify(data),{
                emulateJSON:true,
            })
            .then((response) => {
                vm.proposal = response.body;
                vm.original_proposal = helpers.copyObject(response.body);
                vm.fetchProposalParks(vm.proposal.id);
                // vm.proposal.org_applicant.address = vm.proposal.org_applicant.address != null ? vm.proposal.org_applicant.address : {};
                vm.approver_comment='';
                vm.$nextTick(() => {
                    vm.initialiseAssignedOfficerSelect(true);
                    vm.updateAssignedOfficerSelect();
                });
                vm.$router.push({ path: '/internal' });
            }, (error) => {
                vm.proposal = helpers.copyObject(vm.original_proposal)
                // vm.proposal.org_applicant.address = vm.proposal.org_applicant.address != null ? vm.proposal.org_applicant.address : {};
                swal(
                    'Application Error',
                    helpers.apiVueResourceError(error),
                    'error'
                )
            });

        }

        else{


         let data = {'status': status, 'approver_comment': vm.approver_comment}
         vm.changingStatus=true;
            vm.$http.post(helpers.add_endpoint_json(api_endpoints.proposals,(vm.proposal.id+'/switch_status')),JSON.stringify(data),{
                emulateJSON:true,
            })
            .then((response) => {
                vm.proposal = response.body;
                vm.original_proposal = helpers.copyObject(response.body);
                vm.fetchProposalParks(vm.proposal.id);
                // vm.proposal.org_applicant.address = vm.proposal.org_applicant.address != null ? vm.proposal.org_applicant.address : {};
                vm.approver_comment='';
                vm.$nextTick(() => {
                    vm.initialiseAssignedOfficerSelect(true);
                    vm.updateAssignedOfficerSelect();
                });
                vm.changingStatus=false;
            }, (error) => {
                vm.proposal = helpers.copyObject(vm.original_proposal)
                vm.fetchProposalParks(vm.proposal.id);
                // vm.proposal.org_applicant.address = vm.proposal.org_applicant.address != null ? vm.proposal.org_applicant.address : {};
                swal(
                    'Application Error',
                    helpers.apiVueResourceError(error),
                    'error'
                )
                vm.changingStatus=false;
            });
            }
        },
        fetchProposalParks: function(proposal_id){
          let vm=this;
          vm.$http.get(helpers.add_endpoint_json(api_endpoints.proposals,proposal_id+'/parks_and_trails')).then(response => {
                    vm.proposal_parks = helpers.copyObject(response.body);
                    //console.log(vm.proposal_parks)
                },
                  error => {
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
        fetchReferralRecipientGroups: function(){
            let vm = this;
            vm.loading.push('Loading Referral Recipient Groups');
            vm.$http.get(api_endpoints.referral_recipient_groups).then((response) => {
                vm.referral_recipient_groups = response.body
                vm.loading.splice('Loading Referral Recipient Groups',1);
            },(error) => {
                console.log(error);
                vm.loading.splice('Loading Referral Recipient Groups',1);
            })
        },


        initialiseAssignedOfficerSelect:function(reinit=false){
            let vm = this;
            if (reinit){
                $(vm.$refs.assigned_officer).data('select2') ? $(vm.$refs.assigned_officer).select2('destroy'): '';
            }
            // Assigned officer select
            $(vm.$refs.assigned_officer).select2({
                "theme": "bootstrap",
                allowClear: true,
                placeholder:"Select Officer"
            }).
            on("select2:select",function (e) {
                var selected = $(e.currentTarget);
                if (vm.proposal.processing_status == 'With Approver'){
                    vm.proposal.assigned_approver = selected.val();
                }
                else{
                    vm.proposal.assigned_officer = selected.val();
                }
                vm.assignTo();
            }).on("select2:unselecting", function(e) {
                var self = $(this);
                setTimeout(() => {
                    self.select2('close');
                }, 0);
            }).on("select2:unselect",function (e) {
                var selected = $(e.currentTarget);
                if (vm.proposal.processing_status == 'With Approver'){
                    vm.proposal.assigned_approver = null;
                }
                else{
                    vm.proposal.assigned_officer = null;
                }
                vm.assignTo();
            });
        },
        initialiseSelects: function(){
            let vm = this;
            if (!vm.initialisedSelects){
                //$(vm.$refs.department_users).select2({
                $(vm.$refs.referral_recipient_groups).select2({
                    "theme": "bootstrap",
                    allowClear: true,
                    placeholder:"Select Referral"
                }).
                on("select2:select",function (e) {
                    var selected = $(e.currentTarget);
                    vm.selected_referral = selected.val();
                }).
                on("select2:unselect",function (e) {
                    var selected = $(e.currentTarget);
                    vm.selected_referral = '' 
                });
                vm.initialiseAssignedOfficerSelect();
                vm.initialisedSelects = true;
            }
        },
        remindReferral:function(r){
            let vm = this;
            
            vm.$http.get(helpers.add_endpoint_json(api_endpoints.referrals,r.id+'/remind')).then(response => {
                vm.original_proposal = helpers.copyObject(response.body);
                vm.proposal = response.body;
                vm.fetchProposalParks(vm.proposal.id);
                // vm.proposal.org_applicant.address = vm.proposal.org_applicant.address != null ? vm.proposal.org_applicant.address : {};
                swal(
                    'Referral Reminder',
                    'A reminder has been sent to '+r.referral,
                    'success'
                )
            },
            error => {
                swal(
                    'Application Error',
                    helpers.apiVueResourceError(error),
                    'error'
                )
            });
        },
    },
    mounted: function() {
        let vm = this;
        //vm.fetchDeparmentUsers();
        //vm.fetchReferralRecipientGroups();
        
    },
    updated: function(){
        let vm = this;
        this.$nextTick(() => {
            //vm.initialiseSelects();

            vm.form = document.forms.new_species;
        });
    },
    beforeRouteEnter: function(to, from, next) {
          Vue.http.get(`/api/species/${to.params.species_id}/internal_species.json`).then(res => {
              next(vm => {
                vm.proposal = res.body.proposal_obj;  //--temp proposal_obj
                vm.species = res.body.species_obj; //--temp species_obj
                vm.original_proposal = helpers.copyObject(res.body.proposal_obj);  //--temp proposal_obj
                vm.proposal.org_applicant.address = vm.proposal.org_applicant.address != null ? vm.proposal.org_applicant.address : {};
              });
            },
            err => {
              console.log(err);
            });
    },
    beforeRouteUpdate: function(to, from, next) {
          Vue.http.get(`/api/proposal/${to.params.species_id}.json`).then(res => {
              next(vm => {
                vm.proposal = res.body;
                vm.original_proposal = helpers.copyObject(res.body);
                
              });
            },
            err => {
              console.log(err);
            });
    }
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
