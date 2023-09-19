<template lang="html">
    <div id="observation">
        <FormSection :formCollapse="false" label="Observation Details" :Index="observationDetailBody">
            <div class="row mb-3">
                <label for="" class="col-sm-3 control-label">Observation Method:</label>
                <div class="col-sm-9">
                    <select :disabled="isReadOnly" class="form-select" v-model="occurrence_report_obj.observation_detail.observation_method_id">
                        <option v-for="option in observation_method_list" :value="option.id" v-bind:key="option.id">
                            {{ option.name }}                            
                        </option>
                    </select>
                    
                </div>
            </div>
            <div class="row mb-3">
                <label for="" class="col-sm-3 control-label">Area Surveyed(m<sup>2</sup>) :</label>
                <div class="col-sm-6">
                    <input :disabled="isReadOnly" type="number" class="form-control ocr_number" id="area_surveyed" placeholder="" min="0"
                    v-model="occurrence_report_obj.observation_detail.area_surveyed"/>
                </div>
            </div>
            <div class="row mb-3">
                <label for="" class="col-sm-3 control-label">Survey Duration(mins) :</label>
                <div class="col-sm-6">
                    <input :disabled="isReadOnly" type="number" class="form-control ocr_number" id="survey_duration" placeholder="" min="0"
                    v-model="occurrence_report_obj.observation_detail.survey_duration"/>
                </div>
            </div>
            <div class="row mb-3">
                <div class="col-sm-12">
                    <!-- <button v-if="!updatingHabitatCompositionDetails" class="pull-right btn btn-primary" @click.prevent="updateDetails()" :disabled="!can_update()">Update</button> -->
                    <button v-if="!updatingObservationDetails" class="btn btn-primary btn-sm float-end" @click.prevent="updateObservationDetails()">Update</button>
                    <button v-else disabled class="float-end btn btn-primary"><i class="fa fa-spin fa-spinner"></i>&nbsp;Updating</button>
                </div>
            </div>
        </FormSection>
        
        <FormSection :formCollapse="false" label="Plant Count" :Index="plantCountBody" v-if="!isFauna">
            <PlantCount
                v-if="!isFauna"
                :occurrence_report_obj="occurrence_report_obj" 
                id="plantCountDetail" 
                :is_external="is_external"
                :isReadOnly="isReadOnly"
                ref="plantCountDetail">
            </PlantCount>
        </FormSection>

        <FormSection :formCollapse="false" label="Animal Observation" :Index="animalObsBody" v-if="isFauna">
            <AnimalObservation
                v-if="isFauna"
                :occurrence_report_obj="occurrence_report_obj" 
                id="animalObservationDetail" 
                :is_external="is_external"
                :isReadOnly="isReadOnly"
                ref="animalObservationDetail">
            </AnimalObservation>
        </FormSection>
   </div>
</template>

<script>
import Vue from 'vue' ;
import FormSection from '@/components/forms/section_toggle.vue';
import PlantCount from './plant_count.vue'
import AnimalObservation from './animal_observation.vue'
import {
  api_endpoints,
  helpers
}
from '@/utils/hooks'
export default {
        name: 'OCRObservation',
        props:{
            occurrence_report_obj:{
                type: Object,
                required:true
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
        },
        data:function () {
            let vm = this;
            return{
                observationDetailBody: 'observationDetailBody' + vm._uid,
                plantCountBody: 'plantCountBody' + vm._uid,
                animalObsBody: 'animalObsBody' + vm._uid,
                //---to show fields related to Fauna
                isFauna: vm.occurrence_report_obj.group_type==="fauna"?true:false,
                //----list of values dictionary
                listOfValuesDict: {},
                //scientific_name_list: [],
                observation_method_list: [],
                updatingObservationDetails: false,
            }
        },
        components: {
            FormSection,
            PlantCount,
            AnimalObservation,
        },
        computed: {
            isReadOnly: function(){
                let action = this.$route.query.action;
                if(action === "edit" && this.occurrence_report_obj && this.occurrence_report_obj.assessor_mode.has_assessor_mode){
                    return false;
                }
                else{
                    return this.occurrence_report_obj.readonly;
                }
            },
        },
        watch:{
        },
        methods:{
            eventListeners:function (){
            },
            updateObservationDetails: function() {
                let vm = this;
                vm.updatingObservationDetails = true;
                vm.$http.post(helpers.add_endpoint_json(api_endpoints.occurrence_report,(vm.occurrence_report_obj.id+'/update_observation_details')),JSON.stringify(vm.occurrence_report_obj.observation_detail),{
                    emulateJSON:true
                }).then((response) => {
                    vm.updatingObservationDetails = false;
                    vm.occurrence_report_obj.observation_detail = response.body;
                    swal.fire({
                        title: 'Saved',
                        text: 'Observation details have been saved',
                        icon: 'success',
                        confirmButtonColor:'#226fbb',

                    });
                }, (error) => {
                    var text= helpers.apiVueResourceError(error);
                    swal.fire({
                        title: 'Error', 
                        text: 'Observation details cannot be saved because of the following error: '+text,
                        icon: 'error',
                        confirmButtonColor:'#226fbb',
                    });
                    vm.updatingObservationDetails = false;
                });
            },
        },
        created: async function() {
            let vm=this;
            //------fetch list of values
            const res = await Vue.http.get('/api/occurrence_report/observation_list_of_values.json');
            vm.listOfValuesDict = res.body;
            vm.observation_method_list = vm.listOfValuesDict.observation_method_list;
            vm.observation_method_list.splice(0,0,
                {
                    id: null,
                    name:null,
                });
            if(!this.isFauna){
                // using child refs to assign the list values to avoid calling the above api again in plantCount component
                vm.$refs.plantCountDetail.plant_count_method_list = vm.listOfValuesDict.plant_count_method_list;
                vm.$refs.plantCountDetail.plant_count_method_list.splice(0,0,
                    {
                        id: null,
                        name:null,
                    });
                vm.$refs.plantCountDetail.plant_count_accuracy_list = vm.listOfValuesDict.plant_count_accuracy_list;
                vm.$refs.plantCountDetail.plant_count_accuracy_list.splice(0,0,
                    {
                        id: null,
                        name: null,
                    });
                vm.$refs.plantCountDetail.plant_condition_list = vm.listOfValuesDict.plant_condition_list;
                vm.$refs.plantCountDetail.plant_condition_list.splice(0,0,
                    {
                        id: null,
                        name: null,
                    });
                vm.$refs.plantCountDetail.counted_subject_list = vm.listOfValuesDict.counted_subject_list;
                vm.$refs.plantCountDetail.counted_subject_list.splice(0,0,
                    {
                        id: null,
                        name: null,
                    });
            }
            else if(this.isFauna){
                // using child refs to assign the list values to avoid calling the above api again in AnimalObservation component
                vm.$refs.animalObservationDetail.primary_detection_method_list = vm.listOfValuesDict.primary_detection_method_list;
                vm.$refs.animalObservationDetail.primary_detection_method_list.splice(0,0,
                    {
                        id: '',
                        name: '',
                    });
                vm.$refs.animalObservationDetail.secondary_sign_list = vm.listOfValuesDict.secondary_sign_list;
                vm.$refs.animalObservationDetail.secondary_sign_list.splice(0,0,
                    {
                        id: '',
                        name: '',
                    });
                vm.$refs.animalObservationDetail.reprod_maturity_list = vm.listOfValuesDict.reprod_maturity_list;
                vm.$refs.animalObservationDetail.reprod_maturity_list.splice(0,0,
                    {
                        id: '',
                        name: '',
                    });
                vm.$refs.animalObservationDetail.death_reason_list = vm.listOfValuesDict.death_reason_list;
                vm.$refs.animalObservationDetail.death_reason_list.splice(0,0,
                    {
                        id: null,
                        name: null,
                    });
                vm.$refs.animalObservationDetail.animal_health_list = vm.listOfValuesDict.animal_health_list;
                vm.$refs.animalObservationDetail.animal_health_list.splice(0,0,
                    {
                        id: null,
                        name: null,
                    });
            }
        },
        mounted: function(){
            let vm = this;
            vm.eventListeners();
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
    input.ocr_number{
        width: 20%;
    }
    input.plant_count{
        width: 63%;
    }
</style>

