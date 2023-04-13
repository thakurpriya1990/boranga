<template lang="html">
    <div v-if="meeting_obj" class="container" id="internalMeeting">
      <div class="row" style="padding-bottom: 50px;">
        <h3>Meeting ID# - {{meeting_obj.id }}</h3>
        
        <div v-if="!comparing" class="col-md-3">
           <!-- TODO -->

           <!-- <CommsLogs
                :comms_url="comms_url"
                :logs_url="logs_url"
                :comms_add_url="comms_add_url"
                :disable_add_entry="false"
            />

            <Submission v-if="canSeeSubmission"
                :submitter_first_name="submitter_first_name"
                :submitter_last_name="submitter_last_name"
                :lodgement_date="meeting_obj.lodgement_date"
                class="mt-2"
            /> -->
            
            <div class="top-buffer-s">
                <div class="card card-default">
                    <div class="card-header">
                        Workflow 
                    </div>
                     <div class="card-body card-collapse">
                        <div class="row">
                            <div class="col-sm-12">
                                <strong>Status</strong><br/>
                                {{ meeting_obj.processing_status }}
                            </div>
                            <div class="col-sm-12">
                                <div class="separator"></div>
                            </div>
                            <template>
                                
                                <div class="col-sm-12">
                                    <div class="separator"></div>
                                </div>
                            </template>
                            
                            
                            <div class="col-sm-12 top-buffer-s" v-if="!isFinalised && canAction">
                                <div class="col-sm-12">
                                    <div class="separator"></div>
                                </div>
                                <template v-if="meeting_obj.processing_status == 'With Assessor' || meeting_obj.processing_status == 'With Referral'">
                                    <div class="row">
                                        <div class="col-sm-12">
                                            <strong>Action</strong><br/>
                                        </div>
                                    </div>
                                    
                                </template>
                                <template v-else-if="meeting_obj.processing_status == 'With Approver'">
                                    <div class="row">
                                        <div class="col-sm-12">
                                            <strong>Action</strong><br/>
                                        </div>
                                    </div>

                                    <div class="row">
                                        <div class="col-sm-12">
                                            <!-- <label class="control-label pull-left"  for="Name">Approver Comments</label>
                                            <textarea class="form-control" name="name" v-model="approver_comment"></textarea><br> -->
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
                            <form :action="meeting_form_url" method="post" name="new_meeting" enctype="multipart/form-data">
                                <MeetingSection
                                    ref="meeting" 
                                    :meeting_obj="meeting_obj" 
                                    :canEditStatus="canEditStatus"
                                    id="MeetingStart" 
                                    :is_internal="true">
                                    <!-- TODO add hasAssessorMode props to ProposalMeeting -->
                                </MeetingSection>
                                <input type="hidden" name="csrfmiddlewaretoken" :value="csrf_token"/>
                                <input type='hidden' name="meeting_id" :value="1" />
                                <div class="row" style="margin-bottom: 50px">
                                    <div class="navbar fixed-bottom" style="background-color: #f5f5f5;">
                                        <!--the below as internal proposal submission ELSE just saving proposal changes -->
                                        <div v-if="meeting_obj.internal_user_edit" class="container">
                                            <div class="col-md-12 text-end">
                                                <button v-if="savingMeeting" class="btn btn-primary pull-right" style="margin-top:5px;" disabled >Save and Continue&nbsp;
                                                <i class="fa fa-circle-o-notch fa-spin fa-fw"></i></button>
                                                <button v-else class="btn btn-primary pull-right" style="margin-top:5px;" 
                                                @click.prevent="save()" :disabled="saveExitMeeting || submitMeeting">Save and Continue</button>
                                                
                                                <button v-if="saveExitMeeting" class="btn btn-primary pull-right" style="margin-top:5px;" disabled >Save and Exit&nbsp;
                                                <i class="fa fa-circle-o-notch fa-spin fa-fw"></i></button>
                                                <button v-else class="btn btn-primary pull-right" style="margin-top:5px;" 
                                                @click.prevent="save_exit()" :disabled="savingMeeting || submitMeeting">Save and Exit</button>

                                                <button v-if="submitMeeting" class="btn btn-primary pull-right" style="margin-top:5px;" disabled >Submit&nbsp;
                                                <i class="fa fa-circle-o-notch fa-spin fa-fw"></i></button>
                                                <button v-else class="btn btn-primary pull-right" style="margin-top:5px;" 
                                                @click.prevent="submit()" :disbaled="saveExitMeeting || savingMeeting">Submit</button>
                                            </div>
                                        </div>

                                        <div v-else-if="hasAssessorMode" class="container">
                                            <div class="col-md-12 text-end">
                                                <button v-if="savingMeeting" class="btn btn-primary pull-right" style="margin-top:5px;" disabled >Save Changes&nbsp;
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
        
        
    </div>
</template>
<script>
import Vue from 'vue'
import datatable from '@vue-utils/datatable.vue'
import CommsLogs from '@common-utils/comms_logs.vue'
import Submission from '@common-utils/submission.vue'
import Workflow from '@common-utils/workflow.vue'


import ResponsiveDatatablesHelper from "@/utils/responsive_datatable_helper.js"
import MeetingSection from './meeting_section.vue'
import {
    api_endpoints,
    helpers
}
from '@/utils/hooks'
export default {
    name: 'InternalMeeting',
    data: function() {
        let vm = this;
        return {
            "meeting_obj":null,
            "original_meeting_obj": null,
            "loading": [],
            form: null,
            savingMeeting:false,
            saveExitMeeting: false,
            submitMeeting: false,
            submitting: false,
            saveExitCSProposal: false,
            savingCSProposal:false,
            department_users : [],
            selected_referral: '',
            referral_text: '',
            approver_comment: '',
            sendingReferral: false,
            changingStatus:false,
            
            DATE_TIME_FORMAT: 'DD/MM/YYYY HH:mm:ss',
            comms_url: helpers.add_endpoint_json(api_endpoints.meeting,vm.$route.params.meeting_id+'/comms_log'),
            comms_add_url: helpers.add_endpoint_json(api_endpoints.meeting,vm.$route.params.meeting_id+'/add_comms_log'),
            logs_url: helpers.add_endpoint_json(api_endpoints.meeting,vm.$route.params.meeting_id+'/action_log'),
            comparing: false,
            initialisedSelects: false,
        }
    },
    components: {
        datatable,
        CommsLogs,
        Submission,
        Workflow,
        MeetingSection,
        
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
        meeting_form_url: function(){
            if(this.meeting_obj.id){
                return `/api/meeting/${this.meeting_obj.id}/edit_meeting.json`;
            }
            else{
                return `/api/meeting.json`;
            }
        },
        
        class_ncols: function(){
            return this.comparing ? 'col-md-12' : 'col-md-8';
        },
        submitter_first_name: function(){
            if (this.meeting_obj.submitter){
                return this.meeting_obj.submitter.first_name
            } else {
                return ''
            }
        },
        submitter_last_name: function(){
            if (this.meeting_obj.submitter){
                return this.meeting_obj.submitter.last_name
            } else {
                return ''
            }
        },
        submitter_id: function(){
            if (this.meeting_obj.submitter){
                return this.meeting_obj.submitter.id
            } else {
                //eturn this.meeting_obj.applicant_obj.id
            }
        },
        submitter_email: function(){
            if (this.meeting_obj.submitter){
                return this.meeting_obj.submitter.email
            } else {
                //return this.meeting_obj.applicant_obj.email
            }
        },
        canSeeSubmission: function(){
            /*return this.proposal && (this.proposal.processing_status != 'With Assessor (Requirements)' && this.proposal.processing_status != 'With Approver' && !this.isFinalised)*/

            return true; // TODO the Processing Status based value
        },
        canEditStatus: function(){
            return this.meeting_obj ? this.meeting_obj.can_user_edit: 'false';
        },
        isFinalised: function(){
            return this.meeting_obj.processing_status == 'Declined' || this.meeting_obj.processing_status == 'Approved';
        },
        canLimitedAction: function(){
            if (this.meeting_obj.processing_status == 'With Approver'){
                return this.meeting_obj && (this.meeting_obj.processing_status == 'With Assessor' || this.meeting_obj.processing_status == 'With Referral') && !this.isFinalised && !this.meeting_obj.can_user_edit && (this.meeting_obj.current_assessor.id == this.meeting_obj.assigned_approver || this.meeting_obj.assigned_approver == null ) && this.meeting_obj.assessor_mode.assessor_can_assess? true : false;
            }
            else{
                return this.meeting_obj && (this.meeting_obj.processing_status == 'With Assessor' || this.meeting_obj.processing_status == 'With Referral') && !this.isFinalised && !this.meeting_obj.can_user_edit && (this.meeting_obj.current_assessor.id == this.meeting_obj.assigned_officer || this.meeting_obj.assigned_officer == null ) && this.meeting_obj.assessor_mode.assessor_can_assess? true : false;
            }
        },
        canAction: function(){
            if (this.meeting_obj.processing_status == 'With Approver'){
                return this.meeting_obj && (this.meeting_obj.processing_status == 'With Approver' || this.meeting_obj.processing_status == 'With Assessor') && !this.isFinalised && !this.meeting_obj.can_user_edit && (this.meeting_obj.current_assessor.id == this.meeting_obj.assigned_approver || this.meeting_obj.assigned_approver == null ) && this.meeting_obj.assessor_mode.assessor_can_assess? true : false;
            }
            else{
                return this.meeting_obj && (this.meeting_obj.processing_status == 'With Approver' || this.meeting_obj.processing_status == 'With Assessor') && !this.isFinalised && !this.meeting_obj.can_user_edit && (this.meeting_obj.current_assessor.id == this.meeting_obj.assigned_officer || this.meeting_obj.assigned_officer == null ) && this.meeting_obj.assessor_mode.assessor_can_assess? true : false;
            }
        },
        // canAssess: function(){
        //     return this.meeting_obj && this.meeting_obj.assessor_mode.assessor_can_assess ? true : false;
        // },
        hasAssessorMode:function(){
            // Need to check for approved status as to show 'Save changes' button only when edit and not while view
           return true;
        },
        isApprovalLevelDocument: function(){
            //return this.meeting_obj && this.meeting_obj.processing_status == 'With Approver' && this.meeting_obj.approval_level != null && this.meeting_obj.approval_level_document == null ? true : false;
            return false;
        },
    },
    methods: {
        commaToNewline(s){
            return s.replace(/[,;]/g, '\n');
        },
       
        save: async function(e) {
            let vm = this;
            vm.savingMeeting=true;
            let payload = new Object();
            Object.assign(payload, vm.meeting_obj);
            vm.$http.post(vm.meeting_form_url,payload).then(res=>{
              swal(
                'Saved',
                'Your changes has been saved',
                'success'
              )
              vm.savingMeeting=false;
          },err=>{
            var errorText=helpers.apiVueResourceError(err); 
                  swal(
                          'Save Error',
                          errorText,
                          'error'
                      )
            vm.savingMeeting=false;
          });
        },
        save_exit: async function(e){
            let vm = this;
            vm.saveExitMeeting=true;
            this.save(e);
            vm.saveExitMeeting=false;
            // redirect back to dashboard
            vm.$router.push({
                    name: 'internal-meeting-dash'
                });
        },
        save_before_submit: async function(e) {
            //console.log('save before submit');
            let vm = this;
            vm.saveError=false;

            let payload = new Object();
            Object.assign(payload, vm.meeting_obj);
            const result = await vm.$http.post(vm.species_community_cs_form_url,payload).then(res=>{
                //return true;
            },err=>{
                        var errorText=helpers.apiVueResourceError(err); 
                        swal(
                                'Submit Error',
                                //helpers.apiVueResourceError(err),
                                errorText,
                                'error'
                            )
                        vm.submitMeeting=false;
                        vm.saveError=true;
                //return false;
            });
            return result;
        },
        can_submit: function(){
            let vm=this;
            let blank_fields=[]
            // TODO check blank 
            /*if (vm.meeting_obj.application_type==vm.application_type_tclass) {
            } 
            else if (vm.meeting_obj.application_type==vm.application_type_event) {
                blank_fields=vm.can_submit_event();
            }*/
            blank_fields=vm.can_submit_meeting();
            
            if(blank_fields.length==0){
                return true;
            }
            else{
                return blank_fields;
            }
        },
        can_submit_meeting: function(){
            let vm=this;
            let blank_fields=[]
            if (vm.meeting_obj.group_type == 'flora' || vm.meeting_obj.group_type == 'fauna'){
                if (vm.meeting_obj.species_id == null || vm.meeting_obj.species_id == ''){
                    blank_fields.push(' Species is missing')
                }
            }
            else{
                if (vm.meeting_obj.community_id == null || vm.meeting_obj.community_id == ''){
                    blank_fields.push(' Community is missing')
                }
            }
            if (vm.meeting_obj.conservation_list_id == null || vm.meeting_obj.conservation_list_id == ''){
                blank_fields.push(' Conservation List is missing')
            }
            if (vm.meeting_obj.conservation_category_id == null || vm.meeting_obj.conservation_category_id == ''){
                blank_fields.push(' Conservation Category is missing')
            }
            if (vm.meeting_obj.conservation_criteria.length == 0){
                blank_fields.push(' Conservation criteria is missing')
            }
            if (vm.meeting_obj.comment == null || vm.meeting_obj.comment == ''){
                blank_fields.push(' Conservation comment is missing')
            }
            /*if(vm.$refs.proposal_filming.$refs.filming_other_details.$refs.deed_poll_doc.documents.length==0){
                blank_fields.push(' Deed poll document is missing')
            }*/
            return blank_fields
        },
        submit: async function(){
            let vm = this;

            var missing_data= vm.can_submit();
            if(missing_data!=true){
                swal({
                    title: "Please fix following errors before submitting",
                    text: missing_data,
                    type:'error'
                })
                //vm.paySubmitting=false;
                return false;
            }
            vm.submitMeeting=true;
            swal({
                title: "Submit New Conservation Status Application",
                text: "Are you sure you want to submit this application?",
                type: "question",
                showCancelButton: true,
                confirmButtonText: "submit"
            }).then(async () => {
            
                let result = await vm.save_before_submit()
                if(!vm.saveError){
                    let payload = new Object();
                    Object.assign(payload, vm.meeting_obj);
                    vm.$http.post(helpers.add_endpoint_json(api_endpoints.meeting,vm.meeting_obj.id+'/submit'),payload).then(res=>{
                        vm.meeting_obj = res.body;
                        // vm.$router.push({
                        //     name: 'submit_cs_proposal',
                        //     params: { meeting_obj: vm.meeting_obj}
                        // });
                    // TODO router should push to submit_cs_proposal for internal side 
                        vm.$router.push({
                            name: 'internal-meeting-dash'
                        });
                    },err=>{
                        swal(
                            'Submit Error',
                            helpers.apiVueResourceError(err),
                            'error'
                        )
                    });
                }
                
            },(error) => {
                vm.submitMeeting=false;
            });
        },
        save_wo: function() {
            let vm = this;
            let payload = new Object();
            Object.assign(payload, vm.meeting_obj);
            vm.$http.post(vm.species_community_cs_form_url,payload).then(res=>{
                },err=>{
            });
        },
        initialiseAssignedOfficerSelect:function(reinit=false){
            let vm=this;
        },
        refreshFromResponse:function(response){
            let vm = this;
            vm.original_meeting_obj = helpers.copyObject(response.body);
            vm.meeting_obj = helpers.copyObject(response.body);
            // vm.proposal.org_applicant.address = vm.proposal.org_applicant.address != null ? vm.proposal.org_applicant.address : {};
            vm.$nextTick(() => {
                vm.initialiseAssignedOfficerSelect(true);
                vm.updateAssignedOfficerSelect();
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
            Object.assign(payload, vm.meeting_obj);
            vm.$http.post(vm.species_community_cs_form_url,payload).then(res=>{

            let data = {'email':vm.selected_referral, 'text': vm.referral_text};
            vm.$http.post(helpers.add_endpoint_json(api_endpoints.meeting,(vm.meeting_obj.id+'/assesor_send_referral')),JSON.stringify(data),{
                emulateJSON:true
            }).then((response) => {
                vm.sendingReferral = false;
                vm.original_meeting_obj = helpers.copyObject(response.body);
                vm.meeting_obj = response.body;
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
                vm.original_meeting_obj = helpers.copyObject(response.body);
                vm.meeting_obj = response.body;
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
                vm.original_meeting_obj = helpers.copyObject(response.body);
                vm.meeting_obj = response.body;
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
                vm.original_meeting_obj = helpers.copyObject(response.body);
                vm.meeting_obj = response.body;
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
        switchStatus: function(status){
            let vm = this;
            //vm.save_wo();
            //let vm = this;
            //if approver is pushing back proposal to Assessor then navigate the approver back to dashboard page
            if(vm.meeting_obj.processing_status == 'With Approver' && status=='with_assessor') {
                let data = {'status': status, 'approver_comment': vm.approver_comment}
                vm.$http.post(helpers.add_endpoint_json(api_endpoints.meeting,(vm.meeting_obj.id+'/switch_status')),JSON.stringify(data),{
                    emulateJSON:true,
                })
                .then((response) => {
                    vm.meeting_obj = response.body;
                    vm.original_meeting_obj = helpers.copyObject(response.body);
                    vm.approver_comment='';
                    vm.$nextTick(() => {
                        vm.initialiseAssignedOfficerSelect(true);
                        vm.updateAssignedOfficerSelect();
                    });
                    vm.$router.push({ path: '/internal/conservation-status/' });
                }, (error) => {
                    vm.meeting_obj = helpers.copyObject(vm.original_meeting_obj)
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
                vm.$http.post(helpers.add_endpoint_json(api_endpoints.meeting,(vm.meeting_obj.id+'/switch_status')),JSON.stringify(data),{
                    emulateJSON:true,
                })
                .then((response) => {
                    vm.meeting_obj = response.body;
                    vm.original_meeting_obj = helpers.copyObject(response.body);
                    vm.approver_comment='';
                    vm.$nextTick(() => {
                        vm.initialiseAssignedOfficerSelect(true);
                        vm.updateAssignedOfficerSelect();
                    });
                    vm.changingStatus=false;
                }, (error) => {
                    vm.meeting_obj = helpers.copyObject(vm.original_meeting_obj)
                    swal(
                        'Application Error',
                        helpers.apiVueResourceError(error),
                        'error'
                    )
                    vm.changingStatus=false;
                });
            }
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
            vm.form = document.forms.new_meeting;
        });
    },
    beforeRouteEnter: function(to, from, next) {
        //-------------get species_meeting object if received species id
        /*if(to.query.group_type_name === 'flora' || to.query.group_type_name === "fauna"){
            Vue.http.get(`/api/species_meeting/${to.params.meeting_id}/internal_species_meeting.json`).then(res => {
              next(vm => {
                vm.meeting_obj = res.body.species_meeting_obj; //--temp species_obj
              });
            },
            err => {
              console.log(err);
            });
        }
        //------get community_conservations_status object if received community id
        else{
            Vue.http.get(`/api/community_meeting/${to.params.meeting_id}/internal_community_meeting.json`).then(res => {
              next(vm => {
                vm.meeting_obj = res.body.community_meeting_obj; //--temp community_obj
              });
            },
            err => {
              console.log(err);
            });
        }*/
        Vue.http.get(`/api/meeting/${to.params.meeting_id}/internal_meeting.json`).then(res => {
              next(vm => {
                vm.meeting_obj = res.body;
              });
            },
            err => {
              console.log(err);
            });
    },
    /*beforeRouteUpdate: function(to, from, next) {
          Vue.http.get(`/api/proposal/${to.params.meeting_id}.json`).then(res => {
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


</style>
