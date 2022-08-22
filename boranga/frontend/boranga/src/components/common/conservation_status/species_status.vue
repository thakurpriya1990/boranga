<template lang="html">
    <div id="speciesStatus">
        <FormSection :formCollapse="false" label="Taxonomy" Index="taxonomy">
            <div class="row mb-3">
                <label for="" class="col-sm-3 control-label">Scientific Name:</label>
                <div class="col-sm-9">
                    <select :disabled="conservation_status_obj.readonly" class="form-select" 
                        v-model="conservation_status_obj.species_id" id="scientific_name" @change="getSpeciesDisplay()">
                        <option v-for="option in scientific_name_list" :value="option.id" v-bind:key="option.id">
                            {{ option.name }}                            
                        </option>
                    </select>
                </div>
            </div>
            <div class="row mb-3">
                <label for="" class="col-sm-3 control-label"></label>
                <div class="col-sm-9">
                    <textarea disabled class="form-control" rows="3" id="species_display" v-model="species_display"/>
                </div>
            </div>
            <!-- <div class="row mb-3">
                <label for="" class="col-sm-3 control-label">Common Name:</label>
                <div class="col-sm-9">
                    <input :disabled="conservation_status_obj.readonly" type="text" class="form-control" id="common_name" placeholder="" 
                    v-model="conservation_status_obj.common_name"/>
                </div>
            </div>
            <div class="row mb-3">
                <label for="" class="col-sm-3 control-label">Taxon ID:</label>
                <div class="col-sm-9">
                    <input :disabled="conservation_status_obj.readonly" type="text" class="form-control" id="taxon_id" placeholder="" 
                    v-model="conservation_status_obj.taxonomy_details.taxon_id"/>
                </div>
            </div>
            <div class="row mb-3">
                <label for="" class="col-sm-3 control-label">Previous Name:</label>
                <div class="col-sm-9">
                    <input :disabled="conservation_status_obj.readonly" type="text" class="form-control" id="previous_name" placeholder="" 
                    v-model="conservation_status_obj.taxonomy_details.previous_name"/>
                </div>
            </div> -->
            <div class="row mb-3">
                <label for="" class="col-sm-3 control-label">Name Comments:</label>
                <div class="col-sm-9">
                    <textarea :disabled="conservation_status_obj.readonly" class="form-control" rows="3" id="comment" placeholder=""
                    v-model="conservation_status_obj.comment"/>
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
        name: 'SpeciesStatus',
        props:{
            conservation_status_obj:{
                type: Object,
                required:true
            },
        },
        data:function () {
            let vm = this;
            return{
                datepickerOptions:{
                    format: 'DD/MM/YYYY',
                    showClear:true,
                    useCurrent:false,
                    keepInvalid:true,
                    allowInputToggle:true,
                },
                //---to show fields related to Fauna
                isFauna: vm.conservation_status_obj.group_type==="fauna"?true:false,
                //----list of values dictionary
                species_profile_dict: {},
                scientific_name_list: [],
                // to display the species selected 
                species_display: '',
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
            /*checkDate: function(){
                let vm=this;
                if(vm.$refs.last_data_curration_date.value){
                    vm.conservation_status_obj.last_data_curration_date = vm.$refs.last_data_curration_date.value;
                }
                else{
                    vm.conservation_status_obj.last_data_curration_date=null;
                }
            },*/
            getSpeciesDisplay: function(){
                for(let choice of this.scientific_name_list){
                        if(choice.id === this.conservation_status_obj.scientific_name_id)
                        {
                          this.species_display = choice.name;
                        }
                    }
            },
            eventListeners:function (){
            },
        },
        created: async function() {
            let vm=this;
            //------fetch list of values
            const res = await Vue.http.get('/api/species_profile_dict/');
            vm.species_profile_dict = res.body;
            vm.scientific_name_list = vm.species_profile_dict.scientific_name_list;
            vm.scientific_name_list.splice(0,0,
                {
                    id: null,
                    name: null,
                });
            this.getSpeciesDisplay();
        },
        mounted: function(){
            let vm = this;
            //vm.eventListeners();
        }
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
    }
    input[type=number],{
        width: 50%;
    }
</style>

