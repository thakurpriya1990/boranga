<template lang="html">
    <div id="plant_count">
        <!-- <FormSection :formCollapse="false" label="Plant Count" :Index="plantCountBody"> -->
            <div class="row mb-3">
                <label for="" class="col-sm-3 control-label">Plant Count Method:</label>
                <div class="col-sm-9">
                    <select :disabled="isReadOnly" class="form-select" v-model="plant_count.plant_count_method_id">
                        <option v-for="option in plant_count_method_list" :value="option.id" v-bind:key="option.id">
                            {{ option.name }}                            
                        </option>
                    </select>
                    
                </div>
            </div>
            <div class="row mb-3">
                <label for="" class="col-sm-3 control-label">Plant Count Accuracy:</label>
                <div class="col-sm-9">
                    <select :disabled="isReadOnly" class="form-select" v-model="plant_count.plant_count_accuracy_id">
                        <option v-for="option in plant_count_accuracy_list" :value="option.id" v-bind:key="option.id">
                            {{ option.name }}                            
                        </option>
                    </select>
                    
                </div>
            </div>
            <div class="row mb-3">
                <label for="" class="col-sm-3 control-label">Counted Subject:</label>
                <div class="col-sm-9">
                    <select :disabled="isReadOnly" class="form-select" v-model="plant_count.counted_subject_id">
                        <option v-for="option in counted_subject_list" :value="option.id" v-bind:key="option.id">
                            {{ option.name }}                            
                        </option>
                    </select>
                    
                </div>
            </div>
            <div class="row mb-3">
                <label for="" class="col-sm-3 control-label">Estimated Population Area(m<sup>2</sup>) :</label>
                <div class="col-sm-6">
                    <input :disabled="isReadOnly" type="number" class="form-control ocr_number" id="est_population_area" placeholder="" min="0"
                    v-model="plant_count.estimated_population_area"/>
                </div>
            </div>
            <div class="row mb-3">
                <label for="" class="col-sm-3 control-label">Plant Condition:</label>
                <div class="col-sm-9">
                    <select :disabled="isReadOnly" class="form-select" v-model="plant_count.plant_condition_id">
                        <option v-for="option in plant_condition_list" :value="option.id" v-bind:key="option.id">
                            {{ option.name }}                            
                        </option>
                    </select>
                    
                </div>
            </div>

            <label for="" class="col-lg-3 control-label fs-5 fw-bold">Plant Count - Detailed</label>
            <div class="row mb-3">
                <div class="col-sm-3">
                    
                </div>
                <div class="col-sm-2 fw-bold">
                    Mature
                </div>
                <div class="col-sm-2 fw-bold">
                    Juvenile
                </div>
                <div class="col-sm-2 fw-bold">
                    Seedling
                </div>
                <div class="col-sm-2 fw-bold">
                    Unknown
                </div>
            </div>
            <div class="row mb-3">
                <div class="col-sm-3 fw-bold">
                   Alive
                </div>
                <div class="col-sm-2">
                    <input :disabled="isReadOnly" type="number" class="form-control plant_count" id="alive_mature" placeholder="" min="0"
                    v-model="plant_count.detailed_alive_mature"/>
                </div>
                <div class="col-sm-2">
                    <input :disabled="isReadOnly" type="number" class="form-control plant_count" id="plant_alive_juvenile" placeholder="" min="0"
                    v-model="plant_count.detailed_alive_juvenile"/>
                </div>
                <div class="col-sm-2">
                    <input :disabled="isReadOnly" type="number" class="form-control plant_count" id="alive_seedling" placeholder="" min="0"
                    v-model="plant_count.detailed_alive_seedling"/>
                </div>
                <div class="col-sm-2">
                    <input :disabled="isReadOnly" type="number" class="form-control plant_count" id="alive_unknown" placeholder="" min="0"
                    v-model="plant_count.detailed_alive_unknown"/>
                </div>
            </div>
            <div class="row mb-3">
                <div class="col-sm-3 fw-bold">
                   Dead
                </div>
                <div class="col-sm-2">
                    <input :disabled="isReadOnly" type="number" class="form-control plant_count" id="dead_mature" placeholder="" min="0"
                    v-model="plant_count.detailed_dead_mature"/>
                </div>
                <div class="col-sm-2">
                    <input :disabled="isReadOnly" type="number" class="form-control plant_count" id="plant_dead_juvenile" placeholder="" min="0"
                    v-model="plant_count.detailed_dead_juvenile"/>
                </div>
                <div class="col-sm-2">
                    <input :disabled="isReadOnly" type="number" class="form-control plant_count" id="dead_seedling" placeholder="" min="0"
                    v-model="plant_count.detailed_dead_seedling"/>
                </div>
                <div class="col-sm-2">
                    <input :disabled="isReadOnly" type="number" class="form-control plant_count" id="dead_unknown" placeholder="" min="0"
                    v-model="plant_count.detailed_dead_unknown"/>
                </div>
            </div>
            
            <label for="" class="col-lg-3 control-label fs-5 fw-bold">Plant Count - Simple</label>
            <div class="row mb-3">
                <label for="" class="col-sm-3 control-label">Number alive :</label>
                <div class="col-sm-6">
                    <input :disabled="isReadOnly" type="number" class="form-control ocr_number" id="simple_alive" placeholder="" min="0"
                    v-model="plant_count.simple_alive"/>
                </div>
            </div>
            <div class="row mb-3">
                <label for="" class="col-sm-3 control-label">Number dead :</label>
                <div class="col-sm-6">
                    <input :disabled="isReadOnly" type="number" class="form-control ocr_number" id="simple_dead" placeholder="" min="0"
                    v-model="plant_count.simple_dead"/>
                </div>
            </div>


            <label for="" class="col-lg-3 control-label fs-5 fw-bold">Quadrats</label>
            <div class="row mb-3">
                <label class="col-sm-3 control-label">Quadrats Present?</label>
                <div class="col-sm-1">
                    <input :disabled="isReadOnly" id="quadratsPresentYes" type="radio" v-model="plant_count.quadrats_present" value="true">&nbsp;
                    <label for="quadratsPresentYes">Yes</label>
                </div>
                <div class="col-sm-1">
                    <input :disabled="isReadOnly" id="quadratsPresentNo" type="radio" v-model="plant_count.quadrats_present" value="false">&nbsp;
                    <label for="quadratsPresentNo">No</label>
                </div>
            </div>
            <div class="row mb-3">
                <label class="col-sm-3 control-label">Quadrats Data attached?</label>
                <div class="col-sm-1">
                    <input :disabled="isReadOnly" id="quadratsDataYes" type="radio" v-model="plant_count.quadrats_data_attached" value="true">&nbsp;
                    <label for="quadratsDataYes">Yes</label>
                </div>
                <div class="col-sm-1">
                    <input :disabled="isReadOnly" id="quadratsDataNo" type="radio" v-model="plant_count.quadrats_data_attached" value="false">&nbsp;
                    <label for="quadratsDataNo">No</label>
                </div>
            </div>
            <div class="row mb-3">
                <label for="" class="col-sm-3 control-label">Number of quadrats surveyed :</label>
                <div class="col-sm-6">
                    <input :disabled="isReadOnly" type="number" class="form-control ocr_number" id="quadrats_surveyed" placeholder="" min="0"
                    v-model="plant_count.quadrats_surveyed"/>
                </div>
            </div>
            <div class="row mb-3">
                <label for="" class="col-sm-3 control-label">Individual quadrat area (m<sup>2</sup>) :</label>
                <div class="col-sm-6">
                    <input :disabled="isReadOnly" type="number" class="form-control ocr_number" id="ind_quadrat_area" placeholder="" min="0"
                    v-model="plant_count.individual_quadrat_area"/>
                </div>
            </div>
            <div class="row mb-3">
                <label for="" class="col-sm-3 control-label">Total quadrat area (m<sup>2</sup>) :</label>
                <div class="col-sm-6">
                    <input :disabled="isReadOnly" type="number" class="form-control ocr_number" id="tot_quadrat_area" placeholder="" min="0"
                    v-model="plant_count.total_quadrat_area"/>
                </div>
            </div>
            <div class="row mb-3">
                <label for="" class="col-sm-3 control-label">Flowering plants % :</label>
                <div class="col-sm-6">
                    <input :disabled="isReadOnly" type="number" class="form-control ocr_number" id="flow_plant_per" placeholder="" min="0" max="100"
                    v-model="plant_count.flowering_plants_per"/>
                </div>
            </div>

            <label for="" class="col-lg-3 control-label fs-5 fw-bold"></label>
            <div class="row mb-3">
                <label class="col-sm-3 control-label">Clonal Reproduction present?</label>
                <div class="col-sm-1">
                    <input :disabled="isReadOnly" id="reprodPresentYes" type="radio" v-model="plant_count.clonal_reproduction_present" value="true">&nbsp;
                    <label for="reprodPresentYes">Yes</label>
                </div>
                <div class="col-sm-1">
                    <input :disabled="isReadOnly" id="reprodPresentNo" type="radio" v-model="plant_count.clonal_reproduction_present" value="false">&nbsp;
                    <label for="reprodPresentNo">No</label>
                </div>
            </div>
            <div class="row mb-3">
                <label class="col-sm-3 control-label">Vegetative State present?</label>
                <div class="col-sm-1">
                    <input :disabled="isReadOnly" id="vegStatePresentYes" type="radio" v-model="plant_count.vegetative_state_present" value="true">&nbsp;
                    <label for="vegStatePresentYes">Yes</label>
                </div>
                <div class="col-sm-1">
                    <input :disabled="isReadOnly" id="vegStatePresentNo" type="radio" v-model="plant_count.vegetative_state_present" value="false">&nbsp;
                    <label for="vegStatePresentNo">No</label>
                </div>
            </div>
            <div class="row mb-3">
                <label class="col-sm-3 control-label">Flower Buds present?</label>
                <div class="col-sm-1">
                    <input :disabled="isReadOnly" id="flowerBudsPresentYes" type="radio" v-model="plant_count.flower_bud_present" value="true">&nbsp;
                    <label for="flowerBudsPresentYes">Yes</label>
                </div>
                <div class="col-sm-1">
                    <input :disabled="isReadOnly" id="flowerBudsPresentNo" type="radio" v-model="plant_count.flower_bud_present" value="false">&nbsp;
                    <label for="flowerBudsPresentNo">No</label>
                </div>
            </div>
            <div class="row mb-3">
                <label class="col-sm-3 control-label">Flowers present?</label>
                <div class="col-sm-1">
                    <input :disabled="isReadOnly" id="flowerPresentYes" type="radio" v-model="plant_count.flower_present" value="true">&nbsp;
                    <label for="flowerPresentYes">Yes</label>
                </div>
                <div class="col-sm-1">
                    <input :disabled="isReadOnly" id="flowerPresentNo" type="radio" v-model="plant_count.flower_present" value="false">&nbsp;
                    <label for="flowerPresentNo">No</label>
                </div>
            </div>
            <div class="row mb-3">
                <label class="col-sm-3 control-label">Immature Fruit present?</label>
                <div class="col-sm-1">
                    <input :disabled="isReadOnly" id="immFruitPresentYes" type="radio" v-model="plant_count.immature_fruit_present" value="true">&nbsp;
                    <label for="immFruitPresentYes">Yes</label>
                </div>
                <div class="col-sm-1">
                    <input :disabled="isReadOnly" id="immFruitPresentNo" type="radio" v-model="plant_count.immature_fruit_present" value="false">&nbsp;
                    <label for="immFruitPresentNo">No</label>
                </div>
            </div>
            <div class="row mb-3">
                <label class="col-sm-3 control-label">Ripe Fruit present?</label>
                <div class="col-sm-1">
                    <input :disabled="isReadOnly" id="ripeFruitPresentYes" type="radio" v-model="plant_count.immature_fruit_present" value="true">&nbsp;
                    <label for="ripeFruitPresentYes">Yes</label>
                </div>
                <div class="col-sm-1">
                    <input :disabled="isReadOnly" id="ripeFruitPresentNo" type="radio" v-model="plant_count.ripe_fruit_present" value="false">&nbsp;
                    <label for="ripeFruitPresentNo">No</label>
                </div>
            </div>
            <div class="row mb-3">
                <label class="col-sm-3 control-label">Dehisced Fruit present?</label>
                <div class="col-sm-1">
                    <input :disabled="isReadOnly" id="dehFruitPresentYes" type="radio" v-model="plant_count.dehisced_fruit_present" value="true">&nbsp;
                    <label for="dehFruitPresentYes">Yes</label>
                </div>
                <div class="col-sm-1">
                    <input :disabled="isReadOnly" id="dehFruitPresentNo" type="radio" v-model="plant_count.dehisced_fruit_present" value="false">&nbsp;
                    <label for="dehFruitPresentNo">No</label>
                </div>
            </div>
            <div class="row mb-3">
                <label for="" class="col-sm-3 control-label">Pollinator Observations :</label>
                <div class="col-sm-9">
                    <textarea :disabled="isReadOnly" type="text" row="2" class="form-control" id="pollinator_obs" placeholder="" v-model="plant_count.pollinator_observation"/>
                </div>
            </div>
            <div class="row mb-3">
                <label for="" class="col-sm-3 control-label">Plant Count Comments :</label>
                <div class="col-sm-9">
                    <textarea :disabled="isReadOnly" type="text" row="2" class="form-control" id="plant_count_comment" placeholder="" v-model="plant_count.comment"/>
                </div>
            </div>

            <div class="row mb-3">
                <div class="col-sm-12">
                    <!-- <button v-if="!updatingHabitatCompositionDetails" class="pull-right btn btn-primary" @click.prevent="updateDetails()" :disabled="!can_update()">Update</button> -->
                    <button v-if="!updatingPlantCountDetails" :disabled="isReadOnly" class="btn btn-primary btn-sm float-end" @click.prevent="updatePlantCountDetails()">Update</button>
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
        name: 'PlantCount',
        props:{
            plant_count:{
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
                plant_count_method_list: [],
                plant_count_accuracy_list: [],
                plant_condition_list: [],
                counted_subject_list: [],
                updatingPlantCountDetails: false,
            }
        },
        components: {
            FormSection,
        },
        computed: {
        },
        watch:{
        },
        methods:{
            eventListeners:function (){
            },
            updatePlantCountDetails: function() {
                let vm = this;
                vm.updatingPlantCountDetails = true;
                let endpoint = api_endpoints.occurrence;
                if (is_report) {
                    endpoint = api_endpoints.occurrence_report;
                }
                vm.$http.post(helpers.add_endpoint_json(endpoint,(vm.occurrence_id+'/update_plant_count_details')),JSON.stringify(vm.plant_count),{
                    emulateJSON:true
                }).then((response) => {
                    vm.updatingPlantCountDetails = false;
                    vm.plant_count = response.body;
                    swal.fire({
                        title: 'Saved',
                        text: 'Plant Count details have been saved',
                        icon: 'success',
                        confirmButtonColor:'#226fbb',

                    });
                }, (error) => {
                    var text= helpers.apiVueResourceError(error);
                    swal.fire({
                        title: 'Error', 
                        text: 'Plant Count details cannot be saved because of the following error: '+text,
                        icon: 'error',
                        confirmButtonColor:'#226fbb',
                    });
                    vm.updatingPlantCountDetails = false;
                });
            },
        },
        created: async function() {
            let vm=this;
        },
        mounted: function(){
            let vm = this;
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

