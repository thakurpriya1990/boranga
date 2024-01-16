<template lang="html">
    <div class="container" >
        <form :action="cs_proposal_form_url" method="post" name="new_cs_proposal" enctype="multipart/form-data">
            <div v-if="!cs_proposal_readonly">
              <div v-if="hasAmendmentRequest" class="row">
                <div class="col-lg-12 pull-right">
                  <!-- <div class="card card-default">
                    <div class="card-header">
                      <h3 class="card-title" style="color:red;">An amendment has been requested for this Application
                        <a class="panelClicker" :href="'#'+pBody" data-toggle="collapse"  data-parent="#userInfo" expanded="true" :aria-controls="pBody">
                              <span class="glyphicon glyphicon-chevron-down pull-right "></span>
                        </a>
                      </h3>
                    </div>
                    <div class="card-body collapse in" :id="pBody">
                      <div v-for="a in amendment_request">
                        <p>Reason: {{a.reason}}</p>
                        <p>Details: <p v-for="t in splitText(a.text)">{{t}}</p></p>
                    </div>
                  </div>
                </div> -->
                <FormSection :formCollapse="true" label="An amendment has been requested for this Application" 
                Index="amendment_request" customColor="red">
                  <div v-for="a in amendment_request">
                    <p>Reason: {{a.reason}}</p>
                    <p>Details: <p v-for="t in splitText(a.text)">{{t}}</p></p>
                  </div>
                </FormSection>
              </div> 
            </div>
          </div>

            <!-- <div id="error" v-if="missing_fields.length > 0" style="margin: 10px; padding: 5px; color: red; border:1px solid red;">
                <b>Please answer the following mandatory question(s):</b>
                <ul>
                    <li v-for="error in missing_fields">
                        {{ error.label }}
                    </li>
                </ul>
            </div> -->

            <div v-if="conservation_status_obj" id="scrollspy-heading" class="col-lg-12" >
                <h4>Conservation list - <!-- {{proposal.application_type}} --> application: {{conservation_status_obj.conservation_status_number}}</h4>
            </div>

            <ProposalConservationStatus 
                v-if="conservation_status_obj"
                :conservation_status_obj="conservation_status_obj" 
                id="ConservationStatusStart" 
                :canEditStatus="canEditStatus"
                :is_external="true"
                ref="conservation_status">
            </ProposalConservationStatus>

            <!-- <ProposalTClass v-if="proposal && proposal_parks && proposal.application_type==application_type_tclass" :proposal="proposal" id="proposalStart"  :canEditActivities="canEditActivities" :is_external="true" :proposal_parks="proposal_parks" ref="proposal_tclass"></ProposalTClass> -->
            
            <div>
                <input type="hidden" name="csrfmiddlewaretoken" :value="csrf_token"/>
                <!-- <input type='hidden' name="schema" :value="JSON.stringify(proposal)" /> -->
                <input type='hidden' name="conservation_status_id" :value="1" />

                <div class="row" style="margin-bottom: 50px">
                        <div  class="container">
                          <div class="row" style="margin-bottom: 50px">
                              <div class="navbar fixed-bottom"  style="background-color: #f5f5f5;">
                                  <div class="navbar-inner-right">
                                    <div v-if="conservation_status_obj && !conservation_status_obj.readonly" class="container">
                                      <p class="pull-right" style="margin-top:5px">
                                        <button v-if="saveExitCSProposal" type="button" class="btn btn-primary me-2" disabled>Save and Exit&nbsp;
                                                <i class="fa fa-circle-o-notch fa-spin fa-fw"></i></button>
                                        <input v-else type="button" @click.prevent="save_exit" class="btn btn-primary me-2" value="Save and Exit" :disabled="savingCSProposal || paySubmitting"/>

                                        <button v-if="savingCSProposal" type="button" class="btn btn-primary me-2" disabled>Save and Continue&nbsp;
                                                <i class="fa fa-circle-o-notch fa-spin fa-fw"></i></button>
                                        <input v-else type="button" @click.prevent="save" class="btn btn-primary me-2" value="Save and Continue" :disabled="saveExitCSProposal || paySubmitting"/>

                                        <button v-if="paySubmitting" type="button" class="btn btn-primary" disabled>{{ submit_text() }}&nbsp;
                                                <i class="fa fa-circle-o-notch fa-spin fa-fw"></i></button>
                                        <input v-else type="button" @click.prevent="submit" class="btn btn-primary" :value="submit_text()" :disabled="saveExitCSProposal || savingCSProposal"/>
                                        <input id="save_and_continue_btn" type="hidden" @click.prevent="save_wo_confirm" class="btn btn-primary" value="Save Without Confirmation"/>
                                      </p>
                                    </div>
                                    <div v-else class="container">
                                      <p class="pull-right" style="margin-top:5px;">
                                        <router-link class="btn btn-primary" :to="{name: 'external-conservation_status-dash'}">Back to Dashboard</router-link>
                                      </p>
                                    </div>
                                  </div>
                                </div>
                            </div>
                        </div>
                </div>
            </div>

        </form>
    </div>
</template>
<script>
//import Proposal from '../form.vue'
import Vue from 'vue' 
import ProposalConservationStatus from '@/components/form_conservation_status.vue'
import FormSection from '@/components/forms/section_toggle.vue';
import {
  api_endpoints,
  helpers
}
from '@/utils/hooks'
export default {
  name: 'ExternalConservationStatusProposal',
  data: function() {
    return {
      "proposal": null,
      "conservation_status_obj": null,
      "loading": [],
      form: null,
      amendment_request: [],
      //isDataSaved: false,
      saveError: false,
      proposal_readonly: true,
      cs_proposal_readonly: true,
      hasAmendmentRequest: false,
      submitting: false,
      saveExitCSProposal: false,
      savingCSProposal:false,
      paySubmitting:false,
      newText: "",
      pBody: 'pBody',
      missing_fields: [],
      proposal_parks:null,
    }
  },
  components: {
    ProposalConservationStatus,
    FormSection,
  },
  computed: {
    isLoading: function() {
      return this.loading.length > 0
    },
    csrf_token: function() {
      return helpers.getCookie('csrftoken')
    },
    cs_proposal_form_url: function() {
      return (this.conservation_status_obj) ? `/api/conservation_status/${this.conservation_status_obj.id}/draft.json` : '';
    },
    application_fee_url: function() {
      return (this.proposal) ? `/application_fee/${this.proposal.id}/` : '';
    },
    proposal_submit_url: function() {
      return (this.proposal) ? `/api/proposal/${this.proposal.id}/submit.json` : '';
      //return this.submit();
    },
    canEditActivities: function(){
      return this.conservation_status_obj ? this.conservation_status_obj.can_user_edit: 'false';
    },
    canEditStatus: function(){
      return this.conservation_status_obj ? this.conservation_status_obj.can_user_edit: 'false';
    },
    canEditPeriod: function(){
      return this.proposal ? this.conservation_status_obj.can_user_edit: 'false';
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
    proposal_refs:function(){
      let vm=this;
      if(vm.proposal.application_type == vm.application_type_tclass) {
          return vm.$refs.proposal_tclass;
      } else if(vm.proposal.application_type == vm.application_type_filming) {
          return vm.$refs.proposal_filming;
      } else if(vm.proposal.application_type == vm.application_type_event) {
          return vm.$refs.proposal_event;
      }
    },

    submit_text: function() {
      let vm = this;
      return 'Submit';
    },

    set_formData: function(e) {
      let vm = this;
      //vm.form=document.forms.new_cs_proposal;
      let formData = new FormData(vm.form);

      //console.log('land activities', vm.proposal.selected_parks_activities);
      formData.append('selected_parks_activities', JSON.stringify(vm.proposal.selected_parks_activities))
      formData.append('selected_trails_activities', JSON.stringify(vm.proposal.selected_trails_activities))
      formData.append('marine_parks_activities', JSON.stringify(vm.proposal.marine_parks_activities))

      return formData;
    },
    save: function(e) {
      let vm = this;
      vm.savingCSProposal=true;

      let payload = new Object();
      Object.assign(payload, vm.conservation_status_obj);
      vm.$http.post(vm.cs_proposal_form_url,payload).then(res=>{
          swal.fire({
            title: 'Saved',
            text: 'Your application has been saved',
            icon: 'success',
            confirmButtonColor:'#226fbb'
          });;
          vm.savingCSProposal=false;
      },err=>{
        var errorText=helpers.apiVueResourceError(err); 
                  swal.fire({
                      title: 'Save Error',
                      text: errorText,
                      icon: 'error',
                      confirmButtonColor:'#226fbb'
                  });
        vm.savingCSProposal=false;
      });
    },
    save_exit: function(e) {
      let vm = this;
      this.submitting = true;
      this.saveExitCSProposal=true;
      this.save(e);
      this.saveExitCSProposal=false;
      // redirect back to dashboard
      vm.$router.push({
        name: 'external-conservation_status-dash'
      });
    },

    save_wo_confirm: function(e) {
      let vm = this;
      let formData = vm.set_formData()

      vm.$http.post(vm.cs_proposal_form_url,formData);
    },
    save_before_submit: async function(e) {
      //console.log('save before submit');
      let vm = this;
      vm.saveError=false;

      let payload = new Object();
      Object.assign(payload, vm.conservation_status_obj);
      const result = await vm.$http.post(vm.cs_proposal_form_url,payload).then(res=>{
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
                  vm.paySubmitting=false;
                  vm.saveError=true;
        //return false;
      });
      return result;
    },

    setdata: function(readonly){
      this.cs_proposal_readonly = readonly;
    },

    setAmendmentData: function(amendment_request){
      this.amendment_request = amendment_request;
      
      if (amendment_request.length > 0)
        this.hasAmendmentRequest = true;
        
    },

    splitText: function(aText){
      let newText = '';
      newText = aText.split("\n");
      return newText;

    },

    leaving: function(e) {
      let vm = this;
      var dialogText = 'You have some unsaved changes.';
      if (!vm.cs_proposal_readonly && !vm.submitting){
        e.returnValue = dialogText;
        return dialogText;
      }
      else{
        return null;
      }
    },
    
    highlight_missing_fields: function(){
        let vm = this;
        for (var missing_field of vm.missing_fields) {
            $("#" + missing_field.id).css("color", 'red');
        }
    },

    validate: function(){
        let vm = this;

        // reset default colour
        for (var field of vm.missing_fields) {
            $("#" + field.id).css("color", '#515151');
        }
        vm.missing_fields = [];

        // get all required fields, that are not hidden in the DOM
        //var hidden_fields = $('input[type=text]:hidden, textarea:hidden, input[type=checkbox]:hidden, input[type=radio]:hidden, input[type=file]:hidden');
        //hidden_fields.prop('required', null);
        //var required_fields = $('select:required').not(':hidden');
        var required_fields = $('input[type=text]:required, textarea:required, input[type=checkbox]:required, input[type=radio]:required, input[type=file]:required, select:required').not(':hidden');

        // loop through all (non-hidden) required fields, and check data has been entered
        required_fields.each(function() {
            //console.log('type: ' + this.type + ' ' + this.name)
            var id = 'id_' + this.name
            if (this.type == 'radio') {
                //if (this.type == 'radio' && !$("input[name="+this.name+"]").is(':checked')) {
                if (!$("input[name="+this.name+"]").is(':checked')) {
                    var text = $('#'+id).text()
                    console.log('radio not checked: ' + this.type + ' ' + text)
                    vm.missing_fields.push({id: id, label: text});
                }
            }

            if (this.type == 'checkbox') {
                //if (this.type == 'radio' && !$("input[name="+this.name+"]").is(':checked')) {
                var id = 'id_' + this.classList['value']
                if ($("[class="+this.classList['value']+"]:checked").length == 0) {
                    var text = $('#'+id).text()
                    console.log('checkbox not checked: ' + this.type + ' ' + text)
                    vm.missing_fields.push({id: id, label: text});
                }
            }

            if (this.type == 'select-one') {
                if ($(this).val() == '') {
                    var text = $('#'+id).text()  // this is the (question) label
                    var id = 'id_' + $(this).prop('name'); // the label id
                    console.log('selector not selected: ' + this.type + ' ' + text)
                    vm.missing_fields.push({id: id, label: text});
                }
            }

            if (this.type == 'file') {
                var num_files = $('#'+id).attr('num_files')
                if (num_files == "0") {
                    var text = $('#'+id).text()
                    console.log('file not uploaded: ' + this.type + ' ' + this.name)
                    vm.missing_fields.push({id: id, label: text});
                }
            }

            if (this.type == 'text') {
                if (this.value == '') {
                    var text = $('#'+id).text()
                    console.log('text not provided: ' + this.type + ' ' + this.name)
                    vm.missing_fields.push({id: id, label: text});
                }
            }

            if (this.type == 'textarea') {
                if (this.value == '') {
                    var text = $('#'+id).text()
                    console.log('textarea not provided: ' + this.type + ' ' + this.name)
                    vm.missing_fields.push({id: id, label: text});
                }
            }

            /*
            if (this.type == 'select') {
                if (this.value == '') {
                    var text = $('#'+id).text()
                    console.log('select not provided: ' + this.type + ' ' + this.name)
                    vm.missing_fields.push({id: id, label: text});
                }
            }

            if (this.type == 'multi-select') {
                if (this.value == '') {
                    var text = $('#'+id).text()
                    console.log('multi-select not provided: ' + this.type + ' ' + this.name)
                    vm.missing_fields.push({id: id, label: text});
                }
            }
            */



        });

        return vm.missing_fields.length
    },

    can_submit: function(){
      let vm=this;
      let blank_fields=[]
      // TODO check blank 
      /*if (vm.conservation_status_obj.application_type==vm.application_type_tclass) {
      } 
      else if (vm.conservation_status_obj.application_type==vm.application_type_event) {
          blank_fields=vm.can_submit_event();
      }*/
      blank_fields=vm.can_submit_conservation_status();
      
      if(blank_fields.length==0){
        return true;
      }
      else{
        return blank_fields;
      }

    },
    can_submit_conservation_status: function(){
      let vm=this;
      let blank_fields=[]
      if (vm.conservation_status_obj.group_type == 'flora' || vm.conservation_status_obj.group_type == 'fauna'){
        if (vm.conservation_status_obj.species_id == null || vm.conservation_status_obj.species_id == ''){
            blank_fields.push(' Species is missing')
        }
      }
      else{
        if (vm.conservation_status_obj.community_id == null || vm.conservation_status_obj.community_id == ''){
            blank_fields.push(' Community is missing')
        }
      }
      if (vm.conservation_status_obj.conservation_list_id == null || vm.conservation_status_obj.conservation_list_id == ''){
          blank_fields.push(' Conservation List is missing')
      }
      if (vm.conservation_status_obj.conservation_category_id == null || vm.conservation_status_obj.conservation_category_id == ''){
          blank_fields.push(' Conservation Category is missing')
      }
      return blank_fields
    },
    submit: function(){
        let vm = this;

        var missing_data= vm.can_submit();
        if(missing_data!=true){
          swal.fire({
              title: "Please fix following errors before submitting",
              text: missing_data,
              icon:'error',
              confirmButtonColor:'#226fbb'
          })
          //vm.paySubmitting=false;
          return false;
        }

        // remove the confirm prompt when navigating away from window (on button 'Submit' click)
        vm.submitting = true;
        vm.paySubmitting=true;

        swal.fire({
            title: vm.submit_text() + " Application",
            text: "Are you sure you want to " + vm.submit_text().toLowerCase()+ " this application?",
            icon: "question",
            showCancelButton: true,
            confirmButtonText: vm.submit_text(),
            confirmButtonColor:'#226fbb'
        }).then(async (result) => {
            if(result.isConfirmed){
              /* just save and submit - no payment required (probably application was pushed back by assessor for amendment */
              // var saved=true;
              //vm.save_wo_confirm()
              let result = await vm.save_before_submit()
              if(!vm.saveError){
                let payload = new Object();
                Object.assign(payload, vm.conservation_status_obj);
                vm.$http.post(helpers.add_endpoint_json(api_endpoints.conservation_status,vm.conservation_status_obj.id+'/submit'),payload).then(res=>{
                    vm.conservation_status_obj = res.body;
                    vm.$router.push({
                        name: 'submit_cs_proposal',
                        params: { conservation_status_obj: vm.conservation_status_obj}
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
          vm.paySubmitting=false;
        });
        //vm.paySubmitting=false;
    },

  },

  mounted: function() {
    let vm = this;
    vm.form = document.forms.new_cs_proposal;
    window.addEventListener('beforeunload', vm.leaving);
    window.addEventListener('onblur', vm.leaving);
  },
  

  beforeRouteEnter: function(to, from, next) {
    if (to.params.conservation_status_id) {
      let vm = this;
      Vue.http.get(`/api/conservation_status/${to.params.conservation_status_id}.json`).then(res => {
          next(vm => {
            vm.loading.push('conservation status proposal')
            vm.conservation_status_obj = res.body;
            vm.loading.splice('fetching conservation status proposal', 1);
            vm.setdata(vm.conservation_status_obj.readonly);
            
            Vue.http.get(helpers.add_endpoint_json(api_endpoints.conservation_status,to.params.conservation_status_id+'/amendment_request')).then((res) => {
                     
                      vm.setAmendmentData(res.body);
                  
                },
              err => { 
                        console.log(err);
                  });
              });
          },
        err => {
          console.log(err);
        });    
    }
    else {
      Vue.http.post('/api/conservation_status.json').then(res => {
          next(vm => {
            vm.loading.push('fetching conservation status proposal')
            vm.conservation_status_obj = res.body;
            vm.loading.splice('fetching conservation status proposal', 1);
          });
        },
        err => {
          console.log(err);
        });
    }
  }
}
</script>

<style lang="css" scoped>
</style>
