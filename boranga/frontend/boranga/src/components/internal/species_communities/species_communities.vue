<template lang="html">
    <div v-if="species_community" class="container" id="internalSpeciesCommunity">
      <div class="row" style="padding-bottom: 50px;">
        <h3>{{ display_number }} - {{display_name }}</h3>
        <h4>{{species_community.conservation_status.conservation_category }}</h4>

            <div v-if="!comparing" class="col-md-3">
               <!-- TODO -->

               <!-- <CommsLogs
                    :comms_url="comms_url"
                    :logs_url="logs_url"
                    :comms_add_url="comms_add_url"
                    :disable_add_entry="false"
                /> -->

               <!--  <Submission v-if="canSeeSubmission"
                    :submitter_first_name="submitter_first_name"
                    :submitter_last_name="submitter_last_name"
                    :lodgement_date="proposal.lodgement_date"
                    class="mt-2"
                /> -->
                
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
                            <form :action="species_community_form_url" method="post" name="new_species" enctype="multipart/form-data">
                                <ProposalSpeciesCommunities 
                                    ref="species_communities" 
                                    :species_community="species_community" 
                                    id="speciesCommunityStart" 
                                    :is_internal="true">
                                </ProposalSpeciesCommunities>
                                <input type="hidden" name="csrfmiddlewaretoken" :value="csrf_token"/>
                                <input type='hidden' name="species_community_id" :value="1" />
                                <div class="row" style="margin-bottom: 50px">
                                    <div class="navbar fixed-bottom" style="background-color: #f5f5f5;">
                                        <div class="container">
                                            <div class="col-md-12 text-end">
                                                <button v-if="savingSpeciesCommunity" class="btn btn-primary pull-right" style="margin-top:5px;" disabled >Save and Continue&nbsp;
                                                <i class="fa fa-circle-o-notch fa-spin fa-fw"></i></button>
                                                <button v-else class="btn btn-primary pull-right" style="margin-top:5px;" 
                                                @click.prevent="save()" :disabled="saveExitSpeciesCommunity || submitSpeciesCommunity">Save and Continue</button>
                                                
                                                <button v-if="saveExitSpeciesCommunity" class="btn btn-primary pull-right" style="margin-top:5px;" disabled >Save and Exit&nbsp;
                                                <i class="fa fa-circle-o-notch fa-spin fa-fw"></i></button>
                                                <button v-else class="btn btn-primary pull-right" style="margin-top:5px;" 
                                                @click.prevent="save_exit()" :disabled="savingSpeciesCommunity || submitSpeciesCommunity">Save and Exit</button>

                                                <button v-if="submitSpeciesCommunity" class="btn btn-primary pull-right" style="margin-top:5px;" disabled >Submit&nbsp;
                                                <i class="fa fa-circle-o-notch fa-spin fa-fw"></i></button>
                                                <button v-else class="btn btn-primary pull-right" style="margin-top:5px;" 
                                                @click.prevent="submit()" :disbaled="saveExitSpeciesCommunity || savingSpeciesCommunity">Submit</button>
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

//import MoreReferrals from '@common-utils/more_referrals.vue'
import ResponsiveDatatablesHelper from "@/utils/responsive_datatable_helper.js"
import ProposalSpeciesCommunities from '@/components/form_species_communities.vue'
import {
    api_endpoints,
    helpers
}
from '@/utils/hooks'
export default {
    name: 'InternalSpeciesCommunity',
    data: function() {
        let vm = this;
        return {
            "species_community":null,
            form: null,
            savingSpeciesCommunity:false,
            saveExitSpeciesCommunity: false,
            submitSpeciesCommunity: false,
            
            DATE_TIME_FORMAT: 'DD/MM/YYYY HH:mm:ss',
            comms_url: helpers.add_endpoint_json(api_endpoints.species,vm.$route.params.species_community_id+'/comms_log'),
            comms_add_url: helpers.add_endpoint_json(api_endpoints.species,vm.$route.params.species_community_id+'/add_comms_log'),
            //logs_url: helpers.add_endpoint_json(api_endpoints.proposals,vm.$route.params.species_community_id+'/action_log'),
            comparing: false,
        }
    },
    components: {
        datatable,
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
        species_community_form_url: function() {
          return (this.species_community.group_type === "community") ? 
                  `/api/community/${this.species_community.id}/community_save.json`: 
                  `/api/species/${this.species_community.id}/species_save.json`;
        },
        display_number: function() {
            return (this.species_community.group_type === "community") ? 
                    this.species_community.community_number : 
                    this.species_community.species_number;
        },
        display_name: function() {
            return (this.species_community.group_type === "community") ? 
                    this.species_community.community_migrated_id : 
                    this.species_community.common_name;
        },
        class_ncols: function(){
            return this.comparing ? 'col-md-12' : 'col-md-8';
        },
    },
    methods: {
        commaToNewline(s){
            return s.replace(/[,;]/g, '\n');
        },
        save: async function() {
            let vm = this;
            vm.savingSpeciesCommunity=true;
            let payload = new Object();
            Object.assign(payload, vm.species_community);
            const res = await vm.$http.post(vm.species_community_form_url,payload);
            if(res.ok){
                swal(
                    'Saved',
                    'Your changes has been saved',
                    'success'
                )
                vm.savingSpeciesCommunity=false;
                return res;
            }
            else{
                swal({
                    title: "Please fix following errors before saving",
                    text: err.bodyText,
                    type:'error'
                });
                vm.savingSpeciesCommunity=false;
            }
        },
        save_exit: async function(){
            let vm = this;
            vm.saveExitSpeciesCommunity=true;
            const res = await this.save();
            vm.saveExitSpeciesCommunity=false;
            // redirect back to dashboard
            if (res.ok) {
                vm.$router.push({
                    name: 'internal-species-communities-dash'
                });
            }
        },
        submit: async function(){
            let vm = this
            vm.submitSpeciesCommunity=true;
            try {
                await swal({
                    title:"Edit Species",
                    text: "Are you sure you want to submit the changes",
                    type: "question",
                    showCancelButton: true,
                    confirmButtonText: "submit"
                })
            } catch (cancel) {
                vm.submitSpeciesCommunity = false;
                return;
            }

            if(vm.submitSpeciesCommunity){
                try {
                    const res = await this.save();
                    if (res.ok) {
                        vm.$router.push({
                          name: 'internal-species-communities-dash'
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
                    vm.submitSpeciesCommunity=false;
                    //this.submitting = false;
                }
            }
        },
        save_wo: function() {
            let vm = this;
            let formData = new FormData(vm.form);
            vm.$http.post(vm.proposal_form_url,formData).then(res=>{
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
            vm.form = document.forms.new_species;
        });
    },
    beforeRouteEnter: function(to, from, next) {
        //-------------get species object if received species id
        if(to.query.group_type_name === 'flora' || to.query.group_type_name === "fauna"){
            Vue.http.get(`/api/species/${to.params.species_community_id}/internal_species.json`).then(res => {
              next(vm => {
                vm.species_community = res.body.species_obj; //--temp species_obj
              });
            },
            err => {
              console.log(err);
            });
        }
        //------get community object if received community id
        else{
            Vue.http.get(`/api/community/${to.params.species_community_id}/internal_community.json`).then(res => {
              next(vm => {
                vm.species_community = res.body.community_obj; //--temp community_obj
              });
            },
            err => {
              console.log(err);
            });
        }
    },
    /*beforeRouteUpdate: function(to, from, next) {
          Vue.http.get(`/api/proposal/${to.params.species_community_id}.json`).then(res => {
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
