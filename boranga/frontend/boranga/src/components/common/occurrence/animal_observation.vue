<template lang="html">
    <div id="animal_observation">
        <!-- <FormSection :formCollapse="false" label="Plant Count" :Index="plantCountBody"> -->
            <div class="row mb-3">
                <label for="" class="col-sm-3 control-label">Primary Detection Method:</label>
                <div class="col-sm-9">
                    <select :disabled="isReadOnly" 
                        style="width:100%;" class="form-select input-sm"
                        ref="primary_detection_select" 
                        v-model="animal_observation.primary_detection_method">
                        <option v-for="option in primary_detection_method_list" :value="option.id" :key="option.id">
                            {{option.name}}
                        </option>
                    </select>
                </div>
            </div>
            <div class="row mb-3">
                <label for="" class="col-sm-3 control-label">Secondary Signs:</label>
                <div class="col-sm-9">
                    <select :disabled="isReadOnly" 
                        style="width:100%;" class="form-select input-sm"
                        ref="secondary_sign_select" 
                        v-model="animal_observation.secondary_sign">
                        <option v-for="option in secondary_sign_list" :value="option.id" :key="option.id">
                            {{option.name}}
                        </option>
                    </select>
                </div>
            </div>
            <div class="row mb-3">
                <label for="" class="col-sm-3 control-label">Reproductive Maturity:</label>
                <div class="col-sm-9">
                    <select :disabled="isReadOnly" 
                        style="width:100%;" class="form-select input-sm"
                        ref="reproductive_maturity_select" 
                        v-model="animal_observation.reproductive_maturity">
                        <option v-for="option in reprod_maturity_list" :value="option.id" :key="option.id">
                            {{option.name}}
                        </option>
                    </select>
                </div>
            </div>
            <div class="row mb-3">
                <label for="" class="col-sm-3 control-label">Animal Health:</label>
                <div class="col-sm-9">
                    <select :disabled="isReadOnly" class="form-select" v-model="animal_observation.animal_health_id">
                        <option v-for="option in animal_health_list" :value="option.id" v-bind:key="option.id">
                            {{ option.name }}                            
                        </option>
                    </select>
                </div>
            </div>
            <div class="row mb-3">
                <label for="" class="col-sm-3 control-label">Cause of Death:</label>
                <div class="col-sm-9">
                    <select :disabled="isReadOnly" class="form-select" v-model="animal_observation.death_reason_id">
                        <option v-for="option in death_reason_list" :value="option.id" v-bind:key="option.id">
                            {{ option.name }}                            
                        </option>
                    </select>
                    
                </div>
            </div>

            <div class="row mb-3">
                <label for="" class="col-sm-3 control-label">Distinctive Features :</label>
                <div class="col-sm-9">
                    <textarea :disabled="isReadOnly" type="text" row="2" class="form-control" id="distinct_features" placeholder="" v-model="animal_observation.distinctive_feature"/>
                </div>
            </div>

            <div class="row mb-3">
                <label for="" class="col-sm-3 control-label">Actions Taken :</label>
                <div class="col-sm-9">
                    <textarea :disabled="isReadOnly" type="text" row="2" class="form-control" id="distinct_features" placeholder="" v-model="animal_observation.action_taken"/>
                </div>
            </div>

            <div class="row mb-3">
                <label for="" class="col-sm-3 control-label">Actions Required :</label>
                <div class="col-sm-9">
                    <textarea :disabled="isReadOnly" type="text" row="2" class="form-control" id="distinct_features" placeholder="" v-model="animal_observation.action_required"/>
                </div>
            </div>

            <div class="row mb-3">
                <label for="" class="col-sm-3 control-label">Observation Details :</label>
                <div class="col-sm-9">
                    <textarea :disabled="isReadOnly" type="text" row="2" class="form-control" id="distinct_features" placeholder="" v-model="animal_observation.observation_detail_comment"/>
                </div>
            </div>

            <label for="" class="col-lg-3 control-label fs-5 fw-bold">Animal Count :</label>
            <div class="row mb-3">
                <div class="col-sm-3">
                    
                </div>
                <div class="col-sm-2 fw-bold">
                    Adult
                </div>
                <div class="col-sm-2 fw-bold">
                    Juvenile
                </div>
                <div class="col-sm-2 fw-bold">
                    Pouch Young
                </div>
                <div class="col-sm-2 fw-bold">
                    Unsure
                </div>
            </div>
            <div class="row mb-3">
                <div class="col-sm-3 fw-bold">
                   Alive
                </div>
                <div class="col-sm-2">
                    <input :disabled="isReadOnly" type="number" class="form-control plant_count" id="alive_adult" placeholder="" min="0"
                    v-model="animal_observation.alive_adult"/>
                </div>
                <div class="col-sm-2">
                    <input :disabled="isReadOnly" type="number" class="form-control plant_count" id="alive_juvenile" placeholder="" min="0"
                    v-model="animal_observation.alive_juvenile"/>
                </div>
                <div class="col-sm-2">
                    <input :disabled="isReadOnly" type="number" class="form-control plant_count" id="alive_young" placeholder="" min="0"
                    v-model="animal_observation.alive_pouch_young"/>
                </div>
                <div class="col-sm-2">
                    <input :disabled="isReadOnly" type="number" class="form-control plant_count" id="alive_unsure" placeholder="" min="0"
                    v-model="animal_observation.alive_unsure"/>
                </div>
            </div>
            <div class="row mb-3">
                <div class="col-sm-3 fw-bold">
                   Dead
                </div>
                <div class="col-sm-2">
                    <input :disabled="isReadOnly" type="number" class="form-control plant_count" id="dead_adult" placeholder="" min="0"
                    v-model="animal_observation.dead_adult"/>
                </div>
                <div class="col-sm-2">
                    <input :disabled="isReadOnly" type="number" class="form-control plant_count" id="dead_juvenile" placeholder="" min="0"
                    v-model="animal_observation.dead_juvenile"/>
                </div>
                <div class="col-sm-2">
                    <input :disabled="isReadOnly" type="number" class="form-control plant_count" id="dead_young" placeholder="" min="0"
                    v-model="animal_observation.dead_pouch_young"/>
                </div>
                <div class="col-sm-2">
                    <input :disabled="isReadOnly" type="number" class="form-control plant_count" id="dead_unsure" placeholder="" min="0"
                    v-model="animal_observation.dead_unsure"/>
                </div>
            </div>
            
            <div class="row mb-3">
                <label for="" class="col-sm-3 control-label">Total Number Seen :</label>
                <div class="col-sm-6">
                    <input :disabled="isReadOnly" type="number" class="form-control ocr_number" id="quadrats_surveyed" placeholder="" min="0"
                    v-model="animal_observation.total_count"/>
                </div>
            </div>
            
            <div class="row mb-3">
                <div class="col-sm-12">
                    <!-- <button v-if="!updatingAnimalOnservationDetails" class="pull-right btn btn-primary" @click.prevent="updateDetails()" :disabled="!can_update()">Update</button> -->
                    <button v-if="!updatingAnimalOnservationDetails" :disabled="isReadOnly" class="btn btn-primary btn-sm float-end" @click.prevent="updateAnimalObservationDetails()">Update</button>
                    <button v-else disabled class="float-end btn btn-primary"><i class="fa fa-spin fa-spinner"></i>&nbsp;Updating</button>
                </div>
            </div>
        <!-- </FormSection> -->
    </div>
</template>

<script>
import Vue from 'vue' ;
import FormSection from '@/components/forms/section_toggle.vue';
import {
  api_endpoints,
  helpers
}
from '@/utils/hooks'
export default {
        name: 'AnimalObservation',
        props:{
            animal_observation:{
                type: Object,
                required:true
            },
            is_report:{
                type: Boolean,
                required:true
            },
            occurrence_id:{
                type: Number,
                required:true
            },
            processing_status:{
                type: String,
                required:false
            },
            // this prop is only send from split species form to make the original species readonly
            is_readonly:{
              type: Boolean,
              default: false
            },
            is_external:{
              type: Boolean,
              default: false
            },
            isReadOnly:{
              type: Boolean,
              default: false
            },
        },
        data:function () {
            let vm = this;
            return{
                //----list of values dictionary
                primary_detection_method_list: [],
                secondary_sign_list: [],
                reprod_maturity_list: [],
                death_reason_list: [],
                animal_health_list: [],
                updatingAnimalOnservationDetails: false,
            }
        },
        components: {
            FormSection,
        },
        computed: {
        },
        watch:{
            animal_observation: function (){
                let vm = this;
                $(vm.$refs.primary_detection_select).val(vm.animal_observation.primary_detection_method).trigger('change.select2');
                $(vm.$refs.secondary_sign_select).val(vm.animal_observation.secondary_sign).trigger('change.select2');
                $(vm.$refs.reproductive_maturity_select).val(vm.animal_observation.reproductive_maturity).trigger('change.select2');
            }
        },
        methods:{
            eventListeners:function (){
            },
            initialisePrimaryDetectionSelect: function(){
                let vm = this;
                // Initialise select2 for proposed Conservation Criteria
                $(vm.$refs.primary_detection_select).select2({
                    "theme": "bootstrap-5",
                    allowClear: true,
                    multiple: true,
                    placeholder:"Select Primary Detection Method",
                }).
                on("select2:select",function (e) {
                    var selected = $(e.currentTarget);
                    vm.animal_observation.primary_detection_method = selected.val();
                }).
                on("select2:unselect",function (e) {
                    var selected = $(e.currentTarget);
                    vm.animal_observation.primary_detection_method = selected.val();
                });
            },
            initialiseSecondarySignSelect: function(){
                let vm = this;
                // Initialise select2 for proposed Conservation Criteria
                $(vm.$refs.secondary_sign_select).select2({
                    "theme": "bootstrap-5",
                    allowClear: true,
                    multiple: true,
                    placeholder:"Select Secondary Signs",
                }).
                on("select2:select",function (e) {
                    var selected = $(e.currentTarget);
                    vm.animal_observation.secondary_sign = selected.val();
                }).
                on("select2:unselect",function (e) {
                    var selected = $(e.currentTarget);
                    vm.animal_observation.secondary_sign = selected.val();
                });
            },
            initialiseReprodMaturitySelect: function(){
                let vm = this;
                // Initialise select2 for proposed Conservation Criteria
                $(vm.$refs.reproductive_maturity_select).select2({
                    "theme": "bootstrap-5",
                    allowClear: true,
                    multiple: true,
                    placeholder:"Select Reproductive Maturity",
                }).
                on("select2:select",function (e) {
                    var selected = $(e.currentTarget);
                    vm.animal_observation.reproductive_maturity = selected.val();
                }).
                on("select2:unselect",function (e) {
                    var selected = $(e.currentTarget);
                    vm.animal_observation.reproductive_maturity = selected.val();
                });
            },
            updateAnimalObservationDetails: function() {
                let vm = this;
                vm.updatingAnimalOnservationDetails = true;
                let endpoint = api_endpoints.occurrence;
                if (vm.is_report) {
                    endpoint = api_endpoints.occurrence_report;
                }
                vm.$http.post(helpers.add_endpoint_json(endpoint,(vm.occurrence_id+'/update_animal_observation_details')),JSON.stringify(vm.animal_observation),{
                    emulateJSON:true
                }).then((response) => {
                    vm.updatingAnimalOnservationDetails = false;
                    //vm.animal_observation = response.body;
                    swal.fire({
                        title: 'Saved',
                        text: 'Animal Observation details have been saved',
                        icon: 'success',
                        confirmButtonColor:'#226fbb',

                    }).then((result) => {
                        if (vm.processing_status == "Unlocked") {
                            vm.$router.go();
                        }
                    });
                }, (error) => {
                    var text= helpers.apiVueResourceError(error);
                    swal.fire({
                        title: 'Error', 
                        text: 'Animal Observation details cannot be saved because of the following error: '+text,
                        icon: 'error',
                        confirmButtonColor:'#226fbb',
                    });
                    vm.updatingAnimalOnservationDetails = false;
                });
            },
        },
        created: async function() {
            let vm=this;
        },
        mounted: function(){
            let vm = this;
            vm.initialisePrimaryDetectionSelect();
            vm.initialiseSecondarySignSelect();
            vm.initialiseReprodMaturitySelect();
        },
    }
</script>

<style lang="css" scoped>
    /*ul, li {
        zoom:1;
        display: inline;
    }*/
    fieldset.scheduler-border {
    border: 1px groove #ddd !important;
    padding: 0 1.4em 1.4em 1.4em !important;
    margin: 0 0 1.5em 0 !important;
    -webkit-box-shadow:  0px 0px 0px 0px #000;
            box-shadow:  0px 0px 0px 0px #000;
    }
    legend.scheduler-border {
    width:inherit; /* Or auto */
    padding:0 10px; /* To give a bit of padding on the left and right */
    border-bottom:none;
    }
    input[type=text], select {
        width: 100%;
        padding: 0.375rem 2.25rem 0.375rem 0.75rem;
    }
    input[type=number]{
        width: 50%;
    }
    input.plant_count{
        width: 63%;
    }
    input.ocr_number{
        width: 20%;
    }
</style>

