<template lang="html">
    <div id="threat_detail">
        <modal transition="modal fade" @ok="ok()" @cancel="cancel()" :title="title" large>
            <div class="container-fluid">
                <div class="row">
                    <form class="form-horizontal" name="threatForm">
                        <alert :show.sync="showError" type="danger"><strong>{{errorString}}</strong></alert>
                        <div class="col-sm-12">
                            <div class="form-group">
                                <div class="row modal-input-row mb-3">
                                    <div class="col-sm-3">
                                      <label class="control-label pull-left">Category</label>
                                    </div>
                                    <div class="col-sm-9">
                                      <select class="form-select" v-model="threatObj.threat_category">
                                        <option  v-for="category in threat_category_list" :value="category.id" v-bind:key="category.id">
                                          {{ category.name }} 
                                        </option>
                                      </select>
                                    </div>
                                </div>
                                <div class="row mb-3">
                                    <div class="col-sm-3">
                                      <label class="control-label pull-left">Threat Agent</label>
                                    </div>
                                    <div class="col-sm-9">
                                      <input type="text" class="form-control" v-model="threatObj.threat_agent"/>
                                    </div>
                                </div>
                                <div class="row mb-3">
                                    <div class="col-sm-3">
                                      <label class="control-label pull-left">Threat Comments</label>
                                    </div>
                                    <div class="col-sm-9">
                                      <textarea class="form-control" v-model="threatObj.comment">
                                      </textarea>                                
                                    </div>
                                </div>
                                <div class="row mb-3">
                                   <div class="col-sm-3">
                                      <label class="control-label pull-left">Current Impact?</label>
                                    </div>
                                    <div class="col-sm-9">
                                        <div v-for="option in current_impact_list" class="form-check form-check-inline">
                                              <input type="radio" class="form-check-input" :value="option.id" :id="'current_impact_'+option.id" v-bind:key="option.id" 
                                              v-model="threatObj.current_impact"/>
                                               <label :for="'current_impact_'+option.id" >{{ option.name }}</label>
                                        </div>
                                    </div>
                                </div>
                                <div class="row mb-3">
                                    <div class="col-sm-3">
                                      <label class="control-label pull-left">Potential Impact?</label>
                                    </div>
                                    <div class="col-sm-9">
                                        <div v-for="option in potential_impact_list" class="form-check form-check-inline">
                                          <input type="radio" class="form-check-input" :value="option.id" :id="'potential_impact_'+option.id" v-bind:key="option.id" 
                                            v-model="threatObj.potential_impact"/>
                                           <label :for="'potential_impact_'+option.id" >{{ option.name }}</label>
                                        </div>
                                    </div>
                                </div>
                                <div class="row mb-3">
                                    <div class="col-sm-3">
                                      <label class="control-label pull-left">Potential Threat Onset?</label>
                                    </div>
                                    <div class="col-sm-9">
                                        <div v-for="option in potential_threat_onset_list" class="form-check form-check-inline ">
                                          <input type="radio" class="form-check-input" :value="option.id" :id="'potential_threat_onset_'+option.id" v-bind:key="option.id" 
                                                v-model="threatObj.potential_threat_onset"/>
                                           <label :for="'potential_threat_onset_'+option.id" >{{ option.name }}</label>
                                        </div>
                                    </div>
                                </div>
                                <div class="row mb-3">
                                    <div class="col-sm-3">
                                      <label class="control-label pull-left">Threat Source</label>
                                    </div>
                                    <div class="col-sm-9">
                                      <input type="text" class="form-control" readonly v-model="threatObj.source"/>
                                    </div>
                                </div>
                                <div class="row mb-3">
                                    <div class="col-sm-3">
                                        <label for="" class="control-label pull-left">Date observed: </label>
                                    </div>
                                    <div class="col-sm-9">
                                        <input type="date" class="form-control" name="date_observed" 
                                        ref="date_observed" v-model="threatObj.date_observed" />
                                    </div>
                                </div>
                            </div>
                        </div>
                    </form>
                </div>
            </div>
            <div slot="footer">
                <template v-if="threat_id"> 
                    <button type="button" v-if="updatingThreat" disabled class="btn btn-default" @click="ok"><i class="fa fa-spinnner fa-spin"></i> Updating</button>
                    <button type="button" v-else class="btn btn-default" @click="ok">Update</button>
                </template>
                <template v-else>
                    <button type="button" v-if="addingThreat" disabled class="btn btn-default" @click="ok"><i class="fa fa-spinner fa-spin"></i> Adding</button>
                    <button type="button" v-else class="btn btn-default" @click="ok">Add</button>
                </template>
                <button type="button" class="btn btn-default" @click="cancel">Cancel</button>
            </div>
        </modal>
    </div>
</template>

<script>
//import $ from 'jquery'
//import FileField from '@/components/forms/file.vue'
import Vue from 'vue'
import modal from '@vue-utils/bootstrap-modal.vue'
import alert from '@vue-utils/alert.vue'
import {helpers,api_endpoints} from "@/utils/hooks.js"
export default {
    name:'Threat-Detail',
    components:{
        modal,
        alert
    },
    props: {
        url:{
            type: String,
            required: true
        },
    },
    data:function () {
        let vm = this;
        return {
            isModalOpen:false,
            form:null,
            threat_id: String,
            threat_action: String,
            threatObj: Object,
            threat_category_list: [],
            current_impact_list: [],
            potential_impact_list: [],
            potential_threat_onset_list: [],
            addingThreat: false,
            updatingThreat: false,
            validation_form: null,
            type: '1',
            errors: false,
            errorString: '',
            successString: '',
            success:false,
            validDate: false,
        }
    },
    computed: {
        showError: function() {
            var vm = this;
            return vm.errors;
        },
        title: function(){
            return this.threat_action == 'add' ? 'Add Threat' : 'Edit Threat';
        },

    },
    watch: {

    },
    methods:{
        ok:function () {
            let vm =this;
            if($(vm.form).valid()){
                vm.sendData();
            }
        },
        cancel:function () {
            this.close()
        },
        close:function () {
            this.isModalOpen = false;
            this.threatObj = {};
            this.errors = false;
            $('.has-error').removeClass('has-error');
            //this.documentForm.resetForm();
        },
        sendData:function(){
            let vm = this;
            vm.errors = false;
            let threatObj = JSON.parse(JSON.stringify(vm.threatObj));
            let formData = new FormData()

            if (vm.threatObj.id){
                vm.updatingThreat = true;
                formData.append('data', JSON.stringify(threatObj));
                vm.$http.put(helpers.add_endpoint_json(vm.url,threatObj.id), formData,{
                        emulateJSON:true,
                    }).then((response)=>{
                        vm.updatingThreat = false;
                        vm.$parent.updatedThreats();
                        vm.close();
                    },(error)=>{
                        vm.errors = true;
                        vm.errorString = helpers.apiVueResourceError(error);
                        vm.updatingThreat = false;
                    });
            } else {
                vm.addingThreat = true;
                formData.append('data', JSON.stringify(threatObj));
                vm.$http.post(vm.url, formData,{
                        emulateJSON:true,
                    }).then((response)=>{
                        vm.addingThreat = false;
                        vm.close();
                        vm.$parent.updatedThreats();
                    },(error)=>{
                        vm.errors = true;
                        vm.addingThreat = false;
                        vm.errorString = helpers.apiVueResourceError(error);
                    });
            }
        },
       eventListeners:function () {
            let vm = this;
        }
   },
   created: async function () {
        // documentCategories
        let category_res = await this.$http.get('/api/threat_categories/threat_category_choices/');
        Object.assign(this.threat_category_list, category_res.body);
        // blank entry allows user to clear selection
        this.threat_category_list.splice(0, 0, 
            {
              id: "", 
              name: "",
            });
        //----fetch current_impact list
        let current_impact_res = await this.$http.get('/api/current_impact/current_impact_choices/');
        Object.assign(this.current_impact_list, current_impact_res.body);

        //----fetch potential_impact list
        let potential_impact_res = await this.$http.get('/api/potential_impact/potential_impact_choices/');
        Object.assign(this.potential_impact_list, potential_impact_res.body);

        //----fetch potential_threat_onset list
        let potential_threat_onset_re = await this.$http.get('/api/potential_threat_onset/potential_threat_onset_choices/');
        Object.assign(this.potential_threat_onset_list, potential_threat_onset_re.body);
   },
   mounted:function () {
        let vm =this;
        vm.form = document.forms.threatForm;
        this.$nextTick(()=>{
            vm.eventListeners();
        });
   }
}
</script>

<style lang="css">
    .modal-input-row {
        margin-bottom: 20px;
    }
</style>