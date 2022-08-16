<template lang="html">
    <div id="species">
        <FormSection :formCollapse="false" label="Taxonomy" Index="taxonomy">
            <div class="row mb-3">
                <label for="" class="col-sm-3 control-label">Scientific Name:</label>
                <div class="col-sm-9">
                    <select :disabled="species_community.readonly" class="form-select" 
                        v-model="species_community.scientific_name_id" id="scientific_name" @change="getSpeciesDisplay()">
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
            <div class="row mb-3">
                <label for="" class="col-sm-3 control-label">Common Name:</label>
                <div class="col-sm-9">
                    <input :disabled="species_community.readonly" type="text" class="form-control" id="common_name" placeholder="" 
                    v-model="species_community.common_name"/>
                </div>
            </div>
            <div class="row mb-3">
                <label for="" class="col-sm-3 control-label">Taxon ID:</label>
                <div class="col-sm-9">
                    <input :disabled="species_community.readonly" type="text" class="form-control" id="taxon_id" placeholder="" 
                    v-model="species_community.taxonomy_details.taxon_id"/>
                </div>
            </div>
            <div class="row mb-3">
                <label for="" class="col-sm-3 control-label">Previous Name:</label>
                <div class="col-sm-9">
                    <input :disabled="species_community.readonly" type="text" class="form-control" id="previous_name" placeholder="" 
                    v-model="species_community.taxonomy_details.previous_name"/>
                </div>
            </div>
            <div class="row mb-3" v-show="isFauna">
                <label for="" class="col-sm-3 control-label">Phylogenetic Group:</label>
                <div class="col-sm-9">
                    <select :disabled="species_community.readonly" class="form-select" v-model="species_community.taxonomy_details.phylogenetic_group_id" id="phylogenetic_group">
                        <option v-for="option in phylo_group_list" :value="option.id" v-bind:key="option.id">
                            {{ option.name }}                            
                        </option>
                    </select>
                </div>
            </div>
            <div class="row mb-3">
                <label for="" class="col-sm-3 control-label">Family:</label>
                <div class="col-sm-9">
                    <select :disabled="species_community.readonly" class="form-select" v-model="species_community.taxonomy_details.family_id" id="family">
                        <option v-for="option in family_list" :value="option.id" v-bind:key="option.id">
                            {{ option.name }}                            
                        </option>
                    </select>
                </div>
            </div>
            <div class="row mb-3">
                <label for="" class="col-sm-3 control-label">Genus:</label>
                <div class="col-sm-9">
                    <select :disabled="species_community.readonly" class="form-select" v-model="species_community.taxonomy_details.genus_id" id="genus">
                        <option v-for="option in genus_list" :value="option.id" v-bind:key="option.id">
                            {{ option.name }}                            
                        </option>
                    </select>
                </div>
            </div>
            <div class="row mb-3">
                <label for="" class="col-sm-3 control-label">Name Authority:</label>
                <div class="col-sm-9">
                    <select :disabled="species_community.readonly" class="form-select" v-model="species_community.taxonomy_details.name_authority_id">
                        <option v-for="option in name_authority_list" :value="option.id" v-bind:key="option.id">
                            {{ option.name }}                            
                        </option>
                    </select>
                </div>
            </div>
            <div class="row mb-3">
                <label for="" class="col-sm-3 control-label">Name Comments:</label>
                <div class="col-sm-9">
                    <textarea :disabled="species_community.readonly" class="form-control" rows="3" id="comment" placeholder=""
                    v-model="species_community.taxonomy_details.name_comments"/>
                </div>
            </div>
        </FormSection>
        <FormSection :formCollapse="false" label="Distribution" Index="distribution">
            <div class="row mb-3">
                <label for="" class="col-sm-3 control-label">Region:</label>
                <div class="col-sm-9">
                    <select :disabled="species_community.readonly" class="form-select" @change="filterDistrict($event)" v-model="species_community.region_id">
                        <option v-for="option in region_list" :value="option.id" v-bind:key="option.id">
                            {{ option.name }}                            
                        </option>
                    </select>
                </div>
            </div>
            <div class="row mb-3">
                <label for="" class="col-sm-3 control-label">District:</label>
                <div class="col-sm-9">
                    <select :disabled="species_community.readonly" class="form-select" v-model="species_community.district_id">
                        <option v-for="option in filtered_district_list" :value="option.id" v-bind:key="option.id">
                            {{ option.name }}                            
                        </option>
                    </select>

                </div>
            </div>
            <div class="row mb-3">
                <label for="" class="col-sm-3 control-label">Number of Occurrences:</label>
                <div class="col-sm-6">
                    <input :disabled="species_community.readonly" type="number" class="form-control" id="no_of_occurrences" placeholder="" v-model="species_community.distribution.number_of_occurrences"/>
                </div>
                <div class="col-sm-3">    
                    <input :disabled="species_community.readonly" type="radio" value="true" 
                            class="noo_auto form-check-input" name="noo_auto" 
                            v-model="species_community.distribution.noo_auto">
                    <label>auto</label>
                    <input :disabled="species_community.readonly" type="radio" value="false" 
                            class="noo_auto form-check-input" name="noo_auto" 
                            v-model="species_community.distribution.noo_auto">
                    <label>manual</label>
                </div>
            </div>
            <div class="row mb-3">
                <label for="" class="col-sm-3 control-label">Extent of Occurrence:</label>
                <div class="col-sm-6">
                    <input :disabled="species_community.readonly" type="number" class="form-control" id="extent_of_occurrence" 
                    placeholder="" v-model="species_community.distribution.extent_of_occurrences"/>
                </div>
                <div class="col-sm-3">    
                    <input :disabled="species_community.readonly" type="radio" value="true" 
                            class="eoo_auto form-check-input" name="eoo_auto" 
                            v-model="species_community.distribution.eoo_auto">
                    <label>auto</label>
                    <input :disabled="species_community.readonly" type="radio" value="false" 
                            class="eoo_auto form-check-input" name="eoo_auto" 
                            v-model="species_community.distribution.eoo_auto">
                    <label>manual</label>
                </div>
            </div>
            <div class="row mb-3">
                <label for="" class="col-sm-3 control-label">Area of Occupancy<br>(Actual):</label>
                <div class="col-sm-6">
                    <input :disabled="species_community.readonly" type="number" class="form-control" id="area_of_occupancy_actual" placeholder="" 
                    v-model="species_community.distribution.area_of_occupancy_actual"/>
                </div>
                <div class="col-sm-3">    
                    <input :disabled="species_community.readonly" type="radio" value="true" 
                            class="aoo_actual_auto form-check-input" name="aoo_actual_auto" 
                            v-model="species_community.distribution.aoo_actual_auto">
                    <label>auto</label>
                    <input :disabled="species_community.readonly" type="radio" value="false" 
                            class="aoo_actual_auto form-check-input" name="aoo_actual_auto" 
                            v-model="species_community.distribution.aoo_actual_auto">
                    <label>manual</label>
                </div>
            </div>
            <div class="row mb-3">
                <label for="" class="col-sm-3 control-label">Area of Occupancy<br>(2km x 2km):</label>
                <div class="col-sm-6">
                    <input :disabled="species_community.readonly" type="number" class="form-control" id="area_of_occupany" placeholder="" 
                    v-model="species_community.distribution.area_of_occupancy"/>
                </div>
                <div class="col-sm-3">    
                    <input :disabled="species_community.readonly" type="radio" value="true" 
                            class="aoo_auto form-check-input" name="aoo_auto" v-model="species_community.distribution.aoo_auto">
                    <label>auto</label>
                    <input :disabled="species_community.readonly" type="radio" value="false" 
                            class="aoo_auto form-check-input" name="aoo_auto" v-model="species_community.distribution.aoo_auto">
                    <label>manual</label>
                </div>
            </div>
            <div class="row mb-3">
                <label for="" class="col-sm-3 control-label">Number of IUCN Locations:</label>
                <div class="col-sm-9">
                    <input :disabled="species_community.readonly" type="number" class="form-control" id="no_of_iucn_locations" 
                    placeholder="" v-model="species_community.distribution.number_of_iucn_locations"/>
                </div>
            </div>
        </FormSection>
        <FormSection :formCollapse="false" label="Conservation Attributes" Index="conservation_attributes">
            <div class="row mb-3">
                <label for="" class="col-sm-3 control-label">Habitat/Growth Form:</label>
                <div class="col-sm-9">
                    <textarea :disabled="species_community.readonly" type="text" class="form-control" 
                    id="habitat_growth_form" placeholder="" 
                    v-model="species_community.conservation_attributes.habitat_growth_form"/>
                </div>
            </div>
            <div class="row mb-3" v-show="!isFauna">
                <label for="" class="col-sm-3 control-label">Flowering Period:</label>
                <div class="col-sm-9">
                    <select :disabled="species_community.readonly" class="form-select" 
                        v-model="species_community.conservation_attributes.flowering_period_id">
                        <option v-for="option in flowering_period_list" :value="option.id" v-bind:key="option.id">
                            {{ option.name }}                            
                        </option>
                    </select>
                </div>
            </div>
            <div class="row mb-3" v-show="!isFauna">
                <label for="" class="col-sm-3 control-label">Fruiting Period:</label>
                <div class="col-sm-9">
                    <select :disabled="species_community.readonly" class="form-select" 
                        v-model="species_community.conservation_attributes.fruiting_period_id">
                        <option v-for="option in fruiting_period_list" :value="option.id" v-bind:key="option.id">
                            {{ option.name }}                            
                        </option>
                    </select>
                </div>
            </div>
            <div class="row mb-3" v-show="!isFauna">
                <label for="" class="col-sm-3 control-label">Flora Recruitment Type:</label>
                <div class="col-sm-9">
                    <select :disabled="species_community.readonly" class="form-select" 
                        v-model="species_community.conservation_attributes.flora_recruitment_type_id">
                        <option v-for="option in flora_recruitment_type_list" :value="option.id" v-bind:key="option.id">
                            {{ option.name }}                            
                        </option>
                    </select>
                </div>
            </div>
            <div class="row mb-3" v-show="!isFauna">
                <label for="" class="col-sm-3 control-label">Seed Viability and Germination Info:</label>
                <div class="col-sm-9">
                    <select :disabled="species_community.readonly" class="form-select" 
                        v-model="species_community.conservation_attributes.seed_viability_germination_info_id">
                        <option v-for="option in seed_viability_germination_info_list" :value="option.id" v-bind:key="option.id">
                            {{ option.name }}                            
                        </option>
                    </select>
                </div>
            </div>
            <div class="row mb-3" v-show="!isFauna">
                <label for="" class="col-sm-3 control-label">Root Morphology:</label>
                <div class="col-sm-9">
                    <select :disabled="species_community.readonly" class="form-select" 
                        v-model="species_community.conservation_attributes.root_morphology_id">
                        <option v-for="option in root_morphology_list" :value="option.id" v-bind:key="option.id">
                            {{ option.name }}                            
                        </option>
                    </select>
                </div>
            </div>
            <div class="row mb-3" v-show="!isFauna">
                <label for="" class="col-sm-3 control-label">Pollinator Information:</label>
                <div class="col-sm-9">
                    <select :disabled="species_community.readonly" class="form-select" 
                        v-model="species_community.conservation_attributes.pollinator_information_id">
                        <option v-for="option in pollinator_info_list" :value="option.id" v-bind:key="option.id">
                            {{ option.name }}                            
                        </option>
                    </select>
                </div>
            </div>
            <div class="row mb-3" v-show="isFauna">
                <label for="" class="col-sm-3 control-label">Breeding Period:</label>
                <div class="col-sm-9">
                    <select :disabled="species_community.readonly" class="form-select" 
                        v-model="species_community.conservation_attributes.breeding_period_id">
                        <option v-for="option in breeding_period_list" :value="option.id" v-bind:key="option.id">
                            {{ option.name }}                            
                        </option>
                    </select>
                </div>
            </div>
            <div class="row mb-3" v-show="isFauna">
                <label for="" class="col-sm-3 control-label">Fauna Breeding:</label>
                <div class="col-sm-9">
                    <div v-for="option in fauna_breeding_list">
                        <input :disabled="species_community.readonly" type="radio" v-bind:value="option.id" 
                            :id="'breeding_type_'+option.id" 
                            v-model="species_community.conservation_attributes.fauna_breeding_id">
                        <label :for="'breeding_type_'+option.id">{{ option.name }}</label>
                    </div>
                </div>
            </div>
            <div class="row mb-3" v-show="isFauna">
                <label for="" class="col-sm-3 control-label">Fauna Reproductive capacity:</label>
                <div class="col-sm-9">
                    <input :disabled="species_community.readonly" type="number" class="form-control" 
                    id="fauna_reproductive_capacity" placeholder="" 
                    v-model="species_community.conservation_attributes.fauna_reproductive_capacity"/>
                </div>
            </div>
            <div class="row mb-3">
                <label for="" class="col-sm-3 control-label">Time to Maturity:</label>
                <div class="col-sm-9">
                    <input :disabled="species_community.readonly" type="number" class="form-control" 
                    id="time_to_maturity" placeholder="" 
                    v-model="species_community.conservation_attributes.time_to_maturity"/>
                </div>
            </div>
            <div class="row mb-3">
                <label for="" class="col-sm-3 control-label">Generation Length:</label>
                <div class="col-sm-9">
                    <input :disabled="species_community.readonly" type="number" class="form-control" 
                    id="generation_length" placeholder="" 
                    v-model="species_community.conservation_attributes.generation_length"/>
                </div>
            </div>
            <div class="row mb-3">
                <label for="" class="col-sm-3 control-label">Average Lifespan:</label>
                <div class="col-sm-9">
                    <input :disabled="species_community.readonly" type="number" class="form-control" 
                    id="average_lifespan" placeholder="" 
                    v-model="species_community.conservation_attributes.average_lifespan"/>
                </div>
            </div>
            <div class="row mb-3">
                <label for="" class="col-sm-3 control-label">Minimum Fire Interval:</label>
                <div class="col-sm-9">
                    <input :disabled="species_community.readonly" type="text" class="form-control" 
                    id="minimum_fire_interval" placeholder="" 
                    v-model="species_community.conservation_attributes.minimum_fire_interval"/>
                </div>
            </div>
            <div class="row mb-3">
                <label for="" class="col-sm-3 control-label">Response to Fire:</label>
                <div class="col-sm-9">
                    <input :disabled="species_community.readonly" type="text" class="form-control" id="response_to_fire" placeholder="" v-model="species_community.conservation_attributes.response_to_fire"/>
                </div>
            </div>
            <div class="row mb-3">
                <label for="" class="col-sm-3 control-label">Post Fire Habitat Interactions:</label>
                <div class="col-sm-9">
                    <select :disabled="species_community.readonly" class="form-select" 
                        v-model="species_community.conservation_attributes.post_fire_habitat_interaction_id">
                        <option v-for="option in post_fire_habitatat_interactions_list" :value="option.id" v-bind:key="option.id">
                            {{ option.name }}                            
                        </option>
                    </select>
                </div>
            </div>
            <div class="row mb-3">
                <label for="" class="col-sm-3 control-label">Response to Disturbance:</label>
                <div class="col-sm-9">
                    <input :disabled="species_community.readonly" type="text" class="form-control" 
                    id="response_to_disturbance" placeholder="" 
                    v-model="species_community.conservation_attributes.response_to_disturbance"/>
                </div>
            </div>
            <div class="row mb-3">
                <label for="" class="col-sm-3 control-label">Habitat:</label>
                <div class="col-sm-9">
                    <input :disabled="species_community.readonly" type="text" class="form-control" id="habitat" 
                    placeholder="" v-model="species_community.conservation_attributes.habitat"/>
                </div>
            </div>
            <div class="row mb-3" v-show="!isFauna">
                <label for="" class="col-sm-3 control-label">Hydrology:</label>
                <div class="col-sm-9">
                    <input :disabled="species_community.readonly" type="text" class="form-control" id="hydrology" 
                    placeholder="" v-model="species_community.conservation_attributes.hydrology"/>
                </div>
            </div>
            <div class="row mb-3" v-show="isFauna">
                <label for="" class="col-sm-3 control-label">Diet and Food Source:</label>
                <div class="col-sm-9">
                    <input :disabled="species_community.readonly" type="text" class="form-control" id="diet_food_source" 
                    placeholder="" v-model="species_community.conservation_attributes.diet_and_food_source"/>
                </div>
            </div>
            <div class="row mb-3" v-show="isFauna">
                <label for="" class="col-sm-3 control-label">Home Range:</label>
                <div class="col-sm-9">
                    <input :disabled="species_community.readonly" type="text" class="form-control" id="home_range" 
                    placeholder="" v-model="species_community.conservation_attributes.home_range"/>
                </div>
            </div>
            <div class="row mb-3">
                <label for="" class="col-sm-3 control-label">Research Requirements:</label>
                <div class="col-sm-9">
                    <input :disabled="species_community.readonly" type="text" class="form-control" 
                    id="research_requirements" 
                    placeholder="" v-model="species_community.conservation_attributes.research_requirements"/>
                </div>
            </div>
            <div class="row mb-3" v-show="!isFauna">
                <label for="" class="col-sm-3 control-label">Response to Dieback:</label>
                <div class="col-sm-9">
                    <input :disabled="species_community.readonly" type="text" class="form-control" 
                    id="response_to_dieback" 
                    placeholder="" v-model="species_community.conservation_attributes.response_to_dieback"/>
                </div>
            </div>
            <div class="row mb-3">
                <label for="" class="col-sm-3 control-label">Other relevant diseases:</label>
                <div class="col-sm-9">
                    <textarea :disabled="species_community.readonly" type="text" class="form-control" 
                    id="other_relevant_diseases" 
                    placeholder="" v-model="species_community.conservation_attributes.other_relevant_diseases"/>
                </div>
            </div>
        </FormSection>
        <!-- TODO Conservation status needed to be in the related items Tab -->
        <!-- <FormSection :formCollapse="false" label="Conservation Status" Index="conservation_status">
            <div class="row form-group">
                <div class="col-sm-12">
                    <ConservationStatusDatatable :disabled="species_community.readonly" :species_community="species_community">
                    </ConservationStatusDatatable>
            </div>
            </div>
        </FormSection> -->
        <FormSection :formCollapse="false" label="General" Index="general">
            <div class="row mb-3">
                <label for="" class="col-sm-3 control-label">Department File Numbers:</label>
                <div class="col-sm-9">
                    <input :disabled="species_community .readonly" type="text" class="form-control" id="department_file_numbers" placeholder="" v-model="species_community.distribution.department_file_numbers"/>
                </div>
            </div>
            <div class="row mb-3">
                <label for="" class="col-sm-3 control-label">Last data curration date: </label>
                <div class="col-sm-9">
                    <input :disabled="species_community.readonly" type="date" class="form-control" name="last_data_curration_date" 
                    ref="last_data_curration_date" @change="checkDate()" v-model="species_community.last_data_curration_date" />
                </div>
            </div>
        </FormSection>
    </div>
</template>

<script>
import Vue from 'vue' ;
import FormSection from '@/components/forms/section_toggle.vue';
import ConservationStatusDatatable from '@/components/common/species_communities/species_conservation_status_datatable.vue';
import {
  api_endpoints,
  helpers
}
from '@/utils/hooks'
export default {
        name: 'Species',
        props:{
            species_community:{
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
                isFauna: vm.species_community.group_type==="fauna"?true:false,
                //----list of values dictionary
                species_profile_dict: {},
                scientific_name_list: [],
                name_authority_list: [],
                family_list: [],
                genus_list: [],
                phylo_group_list: [],
                region_list: [],
                district_list: [],
                filtered_district_list: [],
                //---conservatiuon attributes field lists
                flowering_period_list: [],
                fruiting_period_list: [],
                flora_recruitment_type_list: [],
                seed_viability_germination_info_list: [],
                root_morphology_list: [],
                pollinator_info_list: [],
                post_fire_habitatat_interactions_list: [],
                breeding_period_list: [],
                fauna_breeding_list: [],
                // to display the species selected 
                species_display: '',
            }
        },
        components: {
            FormSection,
            ConservationStatusDatatable,
        },
        computed: {
        },
        watch:{
            "species_community.distribution.noo_auto": function(newVal) {
                let vm=this;
                var selectedValue = newVal;
                    if(selectedValue === "true"){
                        vm.species_community.distribution.number_of_occurrences=vm.species_community.distribution.cal_number_of_occurrences;
                    }
                    else{
                        vm.species_community.distribution.number_of_occurrences=null;
                    }
            },
            "species_community.distribution.eoo_auto": function(newVal) {
                let vm=this;
                var selectedValue = newVal;
                    if(selectedValue === "true"){
                        vm.species_community.distribution.extent_of_occurrences=vm.species_community.distribution.cal_extent_of_occurrences;
                    }
                    else{
                        vm.species_community.distribution.extent_of_occurrences=null;
                    }
            },
            "species_community.distribution.aoo_actual_auto": function(newVal) {
                let vm=this;
                var selectedValue = newVal;
                    if(selectedValue === "true"){
                        vm.species_community.distribution.area_of_occupancy_actual=vm.species_community.distribution.cal_area_of_occupancy_actual;
                    }
                    else{
                        vm.species_community.distribution.area_of_occupancy_actual=null;
                    }
            },
            "species_community.distribution.aoo_auto": function(newVal) {
                let vm=this;
                var selectedValue = newVal;
                    if(selectedValue === "true"){
                        vm.species_community.distribution.area_of_occupancy=vm.species_community.distribution.cal_area_of_occupancy;
                    }
                    else{
                        vm.species_community.distribution.area_of_occupancy=null;
                    }
            },
        },
        methods:{
            filterDistrict: function(event) {
                this.$nextTick(() => {
                    if(event){
                      this.species_community.district_id=null; //-----to remove the previous selection
                    }
                    this.filtered_district_list=[];
                    this.filtered_district_list=[{
                      id:null,
                      name:"",
                      region_id:null,
                    }];
                    //---filter districts as per region selected
                    for(let choice of this.district_list){
                        if(choice.region_id === this.species_community.region_id)
                        {
                          this.filtered_district_list.push(choice);
                        }
                    }
                });
            },
            checkDate: function(){
                let vm=this;
                if(vm.$refs.last_data_curration_date.value){
                    vm.species_community.last_data_curration_date = vm.$refs.last_data_curration_date.value;
                }
                else{
                    vm.species_community.last_data_curration_date=null;
                }
            },
            getSpeciesDisplay: function(){
                for(let choice of this.scientific_name_list){
                        if(choice.id === this.species_community.scientific_name_id)
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
            //----set the distribution field values if auto onload
            if(vm.species_community.distribution.noo_auto == true){
                vm.species_community.distribution.number_of_occurrences=vm.species_community.distribution.cal_number_of_occurrences;
            }
            if(vm.species_community.distribution.eoo_auto == true){
                vm.species_community.distribution.extent_of_occurrences=vm.species_community.distribution.cal_extent_of_occurrences;
            }
            if(vm.species_community.distribution.aoo_actual_auto == true){
                vm.species_community.distribution.area_of_occupancy_actual=vm.species_community.distribution.cal_area_of_occupancy_actual;
            }
            if(vm.species_community.distribution.aoo_auto == true){
                vm.species_community.distribution.area_of_occupancy=vm.species_community.distribution.cal_area_of_occupancy;
            }
            //------fetch list of values
            const res = await Vue.http.get('/api/species_profile_dict/');
            vm.species_profile_dict = res.body;
            vm.scientific_name_list = vm.species_profile_dict.scientific_name_list;
            vm.scientific_name_list.splice(0,0,
                {
                    id: null,
                    name: null,
                });
            vm.name_authority_list = vm.species_profile_dict.name_authority_list;
            vm.name_authority_list.splice(0,0,
                {
                    id: null,
                    name: null,
                });
            vm.family_list = vm.species_profile_dict.family_list;
            vm.family_list.splice(0,0,
                {
                    id: null,
                    name: null,
                });
            vm.genus_list = vm.species_profile_dict.genus_list;
            vm.genus_list.splice(0,0,
                {
                    id: null,
                    name: null,
                });
            vm.phylo_group_list = vm.species_profile_dict.phylo_group_list;
            vm.phylo_group_list.splice(0,0,
                {
                    id: null,
                    name: null,
                });
            vm.flowering_period_list = vm.species_profile_dict.flowering_period_list;
            vm.flowering_period_list.splice(0,0,
                {
                    id: null,
                    name: null,
                });
            vm.fruiting_period_list = vm.species_profile_dict.fruiting_period_list;
            vm.fruiting_period_list.splice(0,0,
                {
                    id: null,
                    name: null,
                });
            vm.flora_recruitment_type_list = vm.species_profile_dict.flora_recruitment_type_list;
            vm.flora_recruitment_type_list.splice(0,0,
                {
                    id: null,
                    name: null,
                });
            vm.seed_viability_germination_info_list = vm.species_profile_dict.seed_viability_germination_info_list;
            vm.seed_viability_germination_info_list.splice(0,0,
                {
                    id: null,
                    name: null,
                });
            vm.root_morphology_list = vm.species_profile_dict.root_morphology_list;
            vm.root_morphology_list.splice(0,0,
                {
                    id: null,
                    name: null,
                });
            vm.pollinator_info_list = vm.species_profile_dict.pollinator_info_list;
            vm.pollinator_info_list.splice(0,0,
                {
                    id: null,
                    name: null,
                });
            vm.post_fire_habitatat_interactions_list = vm.species_profile_dict.post_fire_habitatat_interactions_list;
            vm.post_fire_habitatat_interactions_list.splice(0,0,
                {
                    id: null,
                    name: null,
                });
            vm.breeding_period_list = vm.species_profile_dict.breeding_period_list;
            vm.breeding_period_list.splice(0,0,
                {
                    id: null,
                    name: null,
                });
            vm.fauna_breeding_list = vm.species_profile_dict.fauna_breeding_list;
            const response = await Vue.http.get('/api/region_district_filter_dict/');
            vm.filterRegionDistrict= response.body;
            vm.region_list= vm.filterRegionDistrict.region_list;
            vm.district_list= vm.filterRegionDistrict.district_list;
            vm.region_list.splice(0,0,
            {
                id: null,
                name: null,
            });
            this.filterDistrict();
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

