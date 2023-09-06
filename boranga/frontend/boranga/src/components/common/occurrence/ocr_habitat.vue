<template lang="html">
    <div id="habitat">
        <FormSection :formCollapse="false" label="Habitat Composition" :Index="habitatCompositionBody">
            <div class="row mb-3">
                <label for="" class="col-sm-3 control-label">Land Form:</label>
                <div class="col-sm-9">
                    <select :disabled="isReadOnly" 
                        style="width:100%;" class="form-select input-sm" multiple 
                        v-model="occurrence_report_obj.habitat_composition.land_form" >
                        <option v-for="option in land_form_list" :value="option.id" :key="option.id">
                            {{option.name}}
                        </option>
                    </select>
                </div>
            </div>
            <div class="row mb-3">
                <label for="" class="col-sm-3 control-label">Rock Type:</label>
                <div class="col-sm-9">
                    <select :disabled="isReadOnly" class="form-select" v-model="occurrence_report_obj.habitat_composition.rock_type_id">
                        <option v-for="option in rock_type_list" :value="option.id" v-bind:key="option.id">
                            {{ option.name }}                            
                        </option>
                    </select>

                </div>
            </div>
            <div class="row mb-3">
                <label for="" class="col-sm-3 control-label">Loose Rock % :</label>
                <div class="col-sm-6">
                    <input :disabled="isReadOnly" type="number" class="form-control" id="loose_rock_per" placeholder="" min="0" max="100"
                    v-model="occurrence_report_obj.habitat_composition.loose_rock_percent"/>
                </div>
            </div>
            <div class="row mb-3">
                <label for="" class="col-sm-3 control-label">Soil Type:</label>
                <div class="col-sm-9">
                    <select :disabled="isReadOnly" class="form-select" v-model="occurrence_report_obj.habitat_composition.soil_type_id">
                        <option v-for="option in soil_type_list" :value="option.id" v-bind:key="option.id">
                            {{ option.name }}                            
                        </option>
                    </select>

                </div>
            </div>
            <div class="row mb-3">
                <label for="" class="col-sm-3 control-label">Soil Colour:</label>
                <div class="col-sm-9">
                    <select :disabled="isReadOnly" class="form-select" v-model="occurrence_report_obj.habitat_composition.soil_colour_id">
                        <option v-for="option in soil_colour_list" :value="option.id" v-bind:key="option.id">
                            {{ option.name }}                            
                        </option>
                    </select>

                </div>
            </div>
            <div class="row mb-3">
                <label for="" class="col-sm-3 control-label">Soil Condition:</label>
                <div class="col-sm-9">
                    <select :disabled="isReadOnly" class="form-select" v-model="occurrence_report_obj.habitat_composition.soil_condition_id">
                        <option v-for="option in soil_condition_list" :value="option.id" v-bind:key="option.id">
                            {{ option.name }}                            
                        </option>
                    </select>

                </div>
            </div>
            <div class="row mb-3">
                <label for="" class="col-sm-3 control-label">Drainage:</label>
                <div class="col-sm-9">
                    <select :disabled="isReadOnly" class="form-select" v-model="occurrence_report_obj.habitat_composition.drainage_id">
                        <option v-for="option in drainage_list" :value="option.id" v-bind:key="option.id">
                            {{ option.name }}                            
                        </option>
                    </select>

                </div>
            </div>
            <div class="row mb-3">
                <label for="" class="col-sm-3 control-label">Water Quality:</label>
                <div class="col-sm-9">
                    <textarea :disabled="isReadOnly" type="text" class="form-control" placeholder="" 
                    v-model="occurrence_report_obj.habitat_composition.water_quality"/>
                </div>
            </div>
            <div class="row mb-3">
                <label for="" class="col-sm-3 control-label">Habitat Notes:</label>
                <div class="col-sm-9">
                    <textarea :disabled="isReadOnly" type="text" class="form-control" placeholder="" 
                    v-model="occurrence_report_obj.habitat_composition.habitat_notes"/>
                </div>
            </div>
            <div class="row mb-3">
                <div class="col-sm-12">
                    <!-- <button v-if="!updatingHabitatCompositionDetails" class="pull-right btn btn-primary" @click.prevent="updateDetails()" :disabled="!can_update()">Update</button> -->
                    <button v-if="!updatingHabitatCompositionDetails" class="btn btn-primary btn-sm float-end" @click.prevent="updateHabitatCompositionDetails()">Update</button>
                    <button v-else disabled class="float-end btn btn-primary"><i class="fa fa-spin fa-spinner"></i>&nbsp;Updating</button>
                </div>
            </div>
        </FormSection>
        <FormSection :formCollapse="false" label="Habitat Condition" :Index="habitatConditionBody">
            <label for="" class="col-lg-3 control-label fs-5 fw-bold">Keiry Scale</label>
            <div class="row mb-3">
                <label for="" class="col-sm-3 control-label">Pristine %:</label>
                <div class="col-sm-6">
                    <input :disabled="isReadOnly" type="number" class="form-control ocr_number" id="pristine" placeholder="" min="0" max="100"
                    v-model="occurrence_report_obj.habitat_condition.pristine" @change.prevent="calcKeiryTotal()"/>
                </div>
            </div>
            <div class="row mb-3">
                <label for="" class="col-sm-3 control-label">Excellent %:</label>
                <div class="col-sm-6">
                    <input :disabled="isReadOnly" type="number" class="form-control ocr_number" id="excellent" placeholder="" min="0" max="100"
                    v-model="occurrence_report_obj.habitat_condition.excellent" @change.prevent="calcKeiryTotal()"/>
                </div>
            </div>
            <div class="row mb-3">
                <label for="" class="col-sm-3 control-label">Very Good %:</label>
                <div class="col-sm-6">
                    <input :disabled="isReadOnly" type="number" class="form-control ocr_number" id="very_good" placeholder="" min="0" max="100"
                    v-model="occurrence_report_obj.habitat_condition.very_good" @change.prevent="calcKeiryTotal()"/>
                </div>
            </div>
            <div class="row mb-3">
                <label for="" class="col-sm-3 control-label">Good %:</label>
                <div class="col-sm-6">
                    <input :disabled="isReadOnly" type="number" class="form-control ocr_number" id="good" placeholder="" min="0" max="100"
                    v-model="occurrence_report_obj.habitat_condition.good" @change.prevent="calcKeiryTotal()"/>
                </div>
            </div>
            <div class="row mb-3">
                <label for="" class="col-sm-3 control-label">Degraded %:</label>
                <div class="col-sm-6">
                    <input :disabled="isReadOnly" type="number" class="form-control ocr_number" id="degraded" placeholder="" min="0" max="100"
                    v-model="occurrence_report_obj.habitat_condition.degraded" @change.prevent="calcKeiryTotal()"/>
                </div>
            </div>
            <div class="row mb-3">
                <label for="" class="col-sm-3 control-label">Completely Degraded %:</label>
                <div class="col-sm-6">
                    <input :disabled="isReadOnly" type="number" class="form-control ocr_number" id="completely_degraded" placeholder="" min="0" max="100"
                    v-model="occurrence_report_obj.habitat_condition.completely_degraded" @change.prevent="calcKeiryTotal()"/>
                </div>
            </div>
            <div class="row mb-3">
                <label for="" class="col-sm-3 control-label"></label>
                <div class="col-sm-6">
                    <input readonly type="text" class="form-control ocr_number" id="habitat_cond_sum" placeholder="" v-model="habitat_cond_sum"/>
                </div>
            </div>
            <div class="row mb-3">
                <div class="col-sm-12">
                    <button v-if="!updatingHabitatConditionDetails" class="btn btn-primary btn-sm float-end" @click.prevent="updateHabitatConditionDetails()">Update</button>
                    <button v-else disabled class="float-end btn btn-primary"><i class="fa fa-spin fa-spinner"></i>&nbsp;Updating</button>
                </div>
            </div>
        </FormSection>
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
        name: 'Species',
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
                scientific_name_lookup: 'scientific_name_lookup' + vm._uid,
                select_scientific_name: "select_scientific_name"+ vm._uid,
                select_flowering_period: "select_flowering_period"+ vm._uid,
                habitatCompositionBody: 'habitatCompositionBody' + vm._uid,
                habitatConditionBody: 'habitatConditionBody' + vm._uid,
                //---to show fields related to Fauna
                isFauna: vm.occurrence_report_obj.group_type==="fauna"?true:false,
                //----list of values dictionary
                listOfValuesDict: {},
                //scientific_name_list: [],
                rock_type_list: [],
                soil_type_list: [],
                soil_colour_list: [],
                soil_condition_list: [],
                land_form_list: [],
                drainage_list: [],
                habitat_cond_sum: 0,
                updatingHabitatCompositionDetails: false,
                updatingHabitatConditionDetails: false,
            }
        },
        components: {
            FormSection,
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
            // "occurrence_report_obj.distribution.noo_auto": function(newVal) {
            //     let vm=this;
            //     var selectedValue = newVal;
            //         if(selectedValue === "true"){
            //             vm.occurrence_report_obj.distribution.number_of_occurrences=vm.occurrence_report_obj.distribution.cal_number_of_occurrences;
            //         }
            //         else{
            //             vm.occurrence_report_obj.distribution.number_of_occurrences=null;
            //         }
            // },
        },
        methods:{
            eventListeners:function (){
                let vm = this;
                $(vm.$refs.flowering_period_select).select2({
                    "theme": "bootstrap-5",
                    allowClear: true,
                    placeholder:"Select Flowering Period",
                    multiple: true,
                }).
                on("select2:select",function (e) {
                    var selected = $(e.currentTarget);
                    vm.occurrence_report_obj.conservation_attributes.flowering_period = selected.val();
                }).
                on("select2:unselect",function (e) {
                    var selected = $(e.currentTarget);
                    vm.occurrence_report_obj.conservation_attributes.flowering_period = selected.val();
                });
            },
            updateHabitatCompositionDetails: function() {
                let vm = this;
                vm.updatingHabitatCompositionDetails = true;
                vm.$http.post(helpers.add_endpoint_json(api_endpoints.occurrence_report,(vm.occurrence_report_obj.id+'/update_habitat_composition_details')),JSON.stringify(vm.occurrence_report_obj.habitat_composition),{
                    emulateJSON:true
                }).then((response) => {
                    vm.updatingHabitatCompositionDetails = false;
                    vm.occurrence_report_obj.habitat_composition = response.body;
                    swal.fire({
                        title: 'Saved',
                        text: 'Habitat Composition details have been saved',
                        icon: 'success',
                        confirmButtonColor:'#226fbb',

                    });
                }, (error) => {
                    var text= helpers.apiVueResourceError(error);
                    swal.fire({
                        title: 'Error', 
                        text: 'Habitat Composition details have cannot be saved because of the following error: '+text,
                        icon: 'error',
                        confirmButtonColor:'#226fbb',
                    });
                    vm.updatingHabitatCompositionDetails = false;
                });
            },
            updateHabitatConditionDetails: function() {
                let vm = this;
                var valKeiryTotal=vm.calcKeiryTotal();
                if(valKeiryTotal){
                    vm.updatingHabitatConditionDetails = true;
                    vm.$http.post(helpers.add_endpoint_json(api_endpoints.occurrence_report,(vm.occurrence_report_obj.id+'/update_habitat_condition_details')),JSON.stringify(vm.occurrence_report_obj.habitat_condition),{
                        emulateJSON:true
                    }).then((response) => {
                        vm.updatingHabitatConditionDetails = false;
                        vm.occurrence_report_obj.habitat_condition = response.body;
                        swal.fire({
                            title: 'Saved',
                            text: 'Habitat Condition details have been saved',
                            icon: 'success',
                            confirmButtonColor:'#226fbb',
                        });
                    }, (error) => {
                        var text= helpers.apiVueResourceError(error);
                        swal.fire({
                            title: 'Error', 
                            text: 'Habitat Condition details have cannot be saved because of the following error: '+text,
                            icon: 'error',
                            confirmButtonColor:'#226fbb',
                        });
                        vm.updatingHabitatConditionDetails = false;
                    });
                }
            },
            calcKeiryTotal: function(){
                let vm=this;
                let total=0;
                let a = parseInt(vm.occurrence_report_obj.habitat_condition.pristine);
                let b = parseInt(vm.occurrence_report_obj.habitat_condition.excellent);
                let c = parseInt(vm.occurrence_report_obj.habitat_condition.very_good);
                let d = parseInt(vm.occurrence_report_obj.habitat_condition.good);
                let e = parseInt(vm.occurrence_report_obj.habitat_condition.degraded);
                let f = parseInt(vm.occurrence_report_obj.habitat_condition.completely_degraded);
                total = a+b+c+d+e+f;
                vm.habitat_cond_sum = total;
                if(total>100){
                    swal.fire({
                        title: 'warning', 
                        text: 'The total Kiery Scale should not exceed 100% ',
                        icon: 'warning',
                        confirmButtonColor:'#226fbb',
                    });
                    return false;
                }
                else{
                    return true;
                }

            }
        },
        created: async function() {
            let vm=this;
            //------fetch list of values
            const res = await Vue.http.get('/api/occurrence_report/list_of_values.json');
            vm.listOfValuesDict = res.body;
            vm.land_form_list = vm.listOfValuesDict.land_form_list;
            vm.land_form_list.splice(0,0,
                {
                    id: '',
                    name: '',
                });
            vm.rock_type_list = vm.listOfValuesDict.rock_type_list;
            vm.rock_type_list.splice(0,0,
                {
                    id: null,
                    name: null,
                });
            vm.soil_type_list = vm.listOfValuesDict.soil_type_list;
            vm.soil_type_list.splice(0,0,
                {
                    id: null,
                    name: null,
                });
            vm.soil_colour_list = vm.listOfValuesDict.soil_colour_list;
            vm.soil_colour_list.splice(0,0,
                {
                    id: null,
                    name: null,
                });
            vm.soil_condition_list = vm.listOfValuesDict.soil_condition_list;
            vm.soil_condition_list.splice(0,0,
                {
                    id: null,
                    name: null,
                });
            vm.drainage_list = vm.listOfValuesDict.drainage_list;
            vm.drainage_list.splice(0,0,
                {
                    id: null,
                    name: null,
                });
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
    #habitat_cond_sum{
        color: red;
    }
</style>

