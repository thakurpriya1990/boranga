<template lang="html">
    <div v-if="meeting_obj" class="container" id="internalMeeting">
      <div class="row" style="padding-bottom: 50px;">
        <h3>Meeting ID# - {{meeting_obj.meeting_number }}</h3>
        
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
                :lodgement_date="meeting_obj.lodgement_date"
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
                                {{ meeting_obj.processing_status_display }}
                            </div>
                            <div class="col-sm-12">
                                <div class="separator"></div>
                            </div>
                            <!-- <div class="col-sm-12 top-buffer-s" v-if="!isFinalised && canAction"> -->
                            <div class="col-sm-12 top-buffer-s">
                                <!-- <template v-if="hasUserEditMode">
                                    <div class="row">
                                        <div class="col-sm-12">
                                            <strong>Action</strong><br/>
                                        </div>
                                    </div>
                                    <div class="row">
                                        <div class="col-sm-12">
                                            <button style="width:80%;" class="btn btn-primary top-buffer-s" @click.prevent="splitSpecies()">Split</button><br/>
                                        </div>
                                        <div class="col-sm-12">
                                            <button style="width:80%;" class="btn btn-primary top-buffer-s" @click.prevent="combineSpecies()">Combine</button><br/>
                                        </div>
                                        <div class="col-sm-12">
                                            <button style="width:80%;" class="btn btn-primary top-buffer-s" @click.prevent="renameSpecies()">Rename</button><br/>
                                        </div>
                                    </div>
                                </template> -->
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
                                <CSQueue
                                    ref="cs_queue" 
                                    :meeting_obj="meeting_obj" 
                                    id="CSQueue" 
                                    :is_internal="true">
                                    <!-- TODO add hasAssessorMode props to ProposalMeeting -->
                                </CSQueue>
                                <Minutes
                                    ref="minutes" 
                                    :meeting_obj="meeting_obj" 
                                    id="Minutes" 
                                    :is_internal="true">
                                    <!-- TODO add hasAssessorMode props to ProposalMeeting -->
                                </Minutes>
                                <input type="hidden" name="csrfmiddlewaretoken" :value="csrf_token"/>
                                <input type='hidden' name="meeting_id" :value="1" />
                                <div class="row" style="margin-bottom: 50px">
                                    <div class="navbar fixed-bottom" style="background-color: #f5f5f5;">
                                        <!--the below as internal proposal submission ELSE just saving proposal changes -->
                                        <div v-if="meeting_obj.can_user_edit" class="container">
                                            <div class="col-md-12 text-end">
                                                <button v-if="savingMeeting" class="btn btn-primary me-2 pull-right" style="margin-top:5px;" disabled >Save and Continue&nbsp;
                                                <i class="fa fa-circle-o-notch fa-spin fa-fw"></i></button>
                                                <button v-else class="btn btn-primary me-2 pull-right" style="margin-top:5px;" 
                                                @click.prevent="save()" :disabled="saveExitMeeting || submitMeeting">Save and Continue</button>
                                                
                                                <button v-if="saveExitMeeting" class="btn btn-primary me-2 pull-right" style="margin-top:5px;" disabled >Save and Exit&nbsp;
                                                <i class="fa fa-circle-o-notch fa-spin fa-fw"></i></button>
                                                <button v-else class="btn btn-primary me-2 pull-right" style="margin-top:5px;" 
                                                @click.prevent="save_exit()" :disabled="savingMeeting || submitMeeting">Save and Exit</button>

                                                <button v-if="submitMeeting" class="btn btn-primary pull-right" style="margin-top:5px;" disabled >Submit&nbsp;
                                                <i class="fa fa-circle-o-notch fa-spin fa-fw"></i></button>
                                                <button v-else class="btn btn-primary pull-right" style="margin-top:5px;" 
                                                @click.prevent="submit()" :disbaled="saveExitMeeting || savingMeeting">Submit</button>
                                            </div>
                                        </div>

                                        <div v-else-if="hasUserEditMode" class="container">
                                            <div class="col-md-12 text-end">
                                                <button v-if="savingMeeting" class="btn btn-primary pull-right" style="margin-top:5px;" disabled >Save Changes&nbsp;
                                                <i class="fa fa-circle-o-notch fa-spin fa-fw"></i></button>
                                                <button v-else class="btn btn-primary pull-right" style="margin-top:5px;" @click.prevent="save_exit()">Save Changes</button>
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


import MeetingSection from './meeting_section.vue'
import Minutes from './minutes.vue'
import CSQueue from './cs_queue.vue';
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
        Minutes,
        CSQueue,
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
                return `/api/meeting/${this.meeting_obj.id}/meeting_save.json`;
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
            //return this.proposal && (this.proposal.processing_status != 'With Assessor (Requirements)' && this.proposal.processing_status != 'With Approver' && !this.isFinalised)
            //return this.proposal && (this.proposal.processing_status != 'With Assessor (Requirements)')
            return true
        },
        canEditStatus: function(){
            return this.meeting_obj ? this.meeting_obj.can_user_edit: 'false';
        },
        hasUserEditMode:function(){
            // Need to check for approved status as to show 'Save changes' button only when edit and not while view
            if(this.$route.query.action == 'edit'){
                //return this.meeting && this.meeting.user_edit_mode ? true : false;
                return true;
            }
            else{
                return false;
            }
        },
        // isFinalised: function(){
        //     return this.meeting_obj.processing_status == 'Declined' || this.meeting_obj.processing_status == 'Approved';
        // },
        // canLimitedAction: function(){
        //     if (this.meeting_obj.processing_status == 'With Approver'){
        //         return this.meeting_obj && (this.meeting_obj.processing_status == 'With Assessor' || this.meeting_obj.processing_status == 'With Referral') && !this.isFinalised && !this.meeting_obj.can_user_edit && (this.meeting_obj.current_assessor.id == this.meeting_obj.assigned_approver || this.meeting_obj.assigned_approver == null ) && this.meeting_obj.assessor_mode.assessor_can_assess? true : false;
        //     }
        //     else{
        //         return this.meeting_obj && (this.meeting_obj.processing_status == 'With Assessor' || this.meeting_obj.processing_status == 'With Referral') && !this.isFinalised && !this.meeting_obj.can_user_edit && (this.meeting_obj.current_assessor.id == this.meeting_obj.assigned_officer || this.meeting_obj.assigned_officer == null ) && this.meeting_obj.assessor_mode.assessor_can_assess? true : false;
        //     }
        // },
        // canAction: function(){
        //     if (this.meeting_obj.processing_status == 'With Approver'){
        //         return this.meeting_obj && (this.meeting_obj.processing_status == 'With Approver' || this.meeting_obj.processing_status == 'With Assessor') && !this.isFinalised && !this.meeting_obj.can_user_edit && (this.meeting_obj.current_assessor.id == this.meeting_obj.assigned_approver || this.meeting_obj.assigned_approver == null ) && this.meeting_obj.assessor_mode.assessor_can_assess? true : false;
        //     }
        //     else{
        //         return this.meeting_obj && (this.meeting_obj.processing_status == 'With Approver' || this.meeting_obj.processing_status == 'With Assessor') && !this.isFinalised && !this.meeting_obj.can_user_edit && (this.meeting_obj.current_assessor.id == this.meeting_obj.assigned_officer || this.meeting_obj.assigned_officer == null ) && this.meeting_obj.assessor_mode.assessor_can_assess? true : false;
        //     }
        // },
        // // canAssess: function(){
        // //     return this.meeting_obj && this.meeting_obj.assessor_mode.assessor_can_assess ? true : false;
        // // },
        // hasAssessorMode:function(){
        //     // Need to check for approved status as to show 'Save changes' button only when edit and not while view
        //    return true;
        // },
        // isApprovalLevelDocument: function(){
        //     //return this.meeting_obj && this.meeting_obj.processing_status == 'With Approver' && this.meeting_obj.approval_level != null && this.meeting_obj.approval_level_document == null ? true : false;
        //     return false;
        // },
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
                swal.fire({
                    title: 'Saved',
                    text: 'Your changes has been saved',
                    icon: 'success',
                    confirmButtonColor:'#226fbb'
                });
              vm.savingMeeting=false;
            },err=>{
                var errorText=helpers.apiVueResourceError(err); 
                swal.fire({
                    title: 'Save Error',
                    text: errorText,
                    icon: 'error',
                    confirmButtonColor:'#226fbb'
                });
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
                    name: 'internal-meetings-dash'
                    
                });
        },
        save_before_submit: async function(e) {
            //console.log('save before submit');
            let vm = this;
            vm.saveError=false;

            let payload = new Object();
            Object.assign(payload, vm.meeting_obj);
            const result = await vm.$http.post(vm.meeting_form_url,payload).then(res=>{
                //return true;
            },err=>{
                var errorText=helpers.apiVueResourceError(err); 
                swal.fire({
                    title: 'Submit Error',
                    //helpers.apiVueResourceError(err),
                    text: errorText,
                    icon: 'error',
                    confirmButtonColor:'#226fbb'
                });
                vm.submitMeeting=false;
                vm.saveError=true;
                //return false;
            });
            return result;
        },
        can_submit: function(){
            let vm=this;
            let blank_fields=[]
            
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
            if (vm.meeting_obj.title == null || vm.meeting_obj.title == ''){
                    blank_fields.push(' Title is missing')
                }
            else{
                if (vm.meeting_obj.meeting_type == null || vm.meeting_obj.meeting_type == ''){
                    blank_fields.push(' Please select meeting type')
                }
            }
            
            return blank_fields
        },
        submit: async function(){
            let vm = this;

            var missing_data= vm.can_submit();
            if(missing_data!=true){
                swal.fire({
                    title: "Please fix following errors before submitting",
                    text: missing_data,
                    icon:'error',
                    confirmButtonColor:'#226fbb'
                })
                return false;
            }
            vm.submitMeeting=true;
            swal.fire({
                title: "Submit New Meeting",
                text: "Are you sure you want to submit this meeting?",
                icon: "question",
                showCancelButton: true,
                confirmButtonText: "submit",
                confirmButtonColor:'#226fbb'
            }).then(async (swalresult) => {
                if(swalresult.isConfirmed){
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
                                name: 'internal-meetings-dash'
                            });
                        },err=>{
                            swal.fire({
                                title: 'Submit Error',
                                text: helpers.apiVueResourceError(err),
                                icon: 'error',
                                confirmButtonColor:'#226fbb'
                            });
                        });
                    }
                }
            },(error) => {
                vm.submitMeeting=false;
            });
        },
        save_wo: function() {
            let vm = this;
            let payload = new Object();
            Object.assign(payload, vm.meeting_obj);
            vm.$http.post(vm.meeting_form_url,payload).then(res=>{
                },err=>{
            });
        },
    },
    mounted: function() {
        let vm = this;
    },
    updated: function(){
        let vm = this;
        this.$nextTick(() => {
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
                vm.meeting_obj.sel_committee_members_arr=[];
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
