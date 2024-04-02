<template lang="html">
    <div id="community">
        <FormSection :formCollapse="false" label="Taxonomy" Index="taxonomy">
            <!-- <div class="row mb-3">
                <label for="" class="col-sm-3 control-label">Species:</label>
                <div class="col-sm-9">
                    <select style="width:100%;" class="form-select input-sm" :disabled="isReadOnly" multiple ref="species_select" v-model="species_community.species">
                        <option v-for="s in species_list" :value="s.id" :key="s.id">{{s.id}} - {{s.scientific_name}}</option>
                    </select>
                </div>
            </div> -->
            <!-- <div class="row mb-3">
                <label for="" class="col-sm-3 control-label">Community Name:</label>
                <div class="col-sm-9" :id="select_community_name">
                    <select :disabled="isReadOnly"
                        :id="community_name_lookup"  
                        :name="community_name_lookup"  
                        :ref="community_name_lookup" 
                        class="form-control" />
                </div>
            </div>
            <div class="row mb-3">
                <label for="" class="col-sm-3 control-label"></label>
                <div class="col-sm-9">
                    <textarea disabled class="form-control" rows="3" id="community_name_display" 
                    v-model="community_name_display"/>
                </div>
            </div> -->
            <div class="row mb-3">
                <label for="" class="col-sm-3 control-label">Community Name:</label>
                <div class="col-sm-9">
                    <textarea :disabled="isReadOnly" class="form-control" rows="1" id="community_name" placeholder=""
                    v-model="species_community.taxonomy_details.community_name"/>
                </div>
            </div>
            <div class="row mb-3">
                <label for="" class="col-sm-3 control-label">Community ID:</label>
                <div class="col-sm-9">
                    <input :disabled="isReadOnly" type="text" class="form-control"
                    id="community_migrated_id" placeholder=""
                    v-model="species_community.taxonomy_details.community_migrated_id"/>
                </div>
            </div>
            <div class="row mb-3">
                <label for="" class="col-sm-3 control-label">Community Description:</label>
                <div class="col-sm-9">
                    <textarea :disabled="isReadOnly" class="form-control" rows="2" id="community_description" placeholder=""
                    v-model="species_community.taxonomy_details.community_description"/>
                </div>
            </div>
            <div class="row mb-3">
                <label for="" class="col-sm-3 control-label">Previous Name:</label>
                <div class="col-sm-9">
                    <textarea :disabled="isReadOnly" class="form-control" id="community_previous_name" placeholder=""
                    v-model="species_community.taxonomy_details.previous_name"/>
                </div>
            </div>
            <div class="row mb-3">
                <label for="" class="col-sm-3 control-label">Name Authority:</label>
                <div class="col-sm-9">
                    <textarea :disabled="isReadOnly" rows="1" class="form-control" id="name_authority" placeholder="" 
                    v-model="species_community.taxonomy_details.name_authority"/>
                </div>
            </div>
            <div class="row mb-3">
                <label for="" class="col-sm-3 control-label">Name Comments:</label>
                <div class="col-sm-9">
                    <textarea :disabled="isReadOnly" class="form-control" id="community_comment" placeholder=""
                    v-model="species_community.taxonomy_details.name_comments"/>
                </div>
            </div>
        </FormSection>
        <FormSection :formCollapse="false" label="Distribution" Index="distribution">
            <div class="row mb-3">
                <label for="" class="col-sm-3 control-label">Distribution:</label>
                <div class="col-sm-9">
                    <textarea :disabled="isReadOnly" class="form-control" rows="1" id="distribution" placeholder="" v-model="species_community.distribution.distribution"/>
                </div>
            </div>
            <div class="row mb-3">
                <label for="" class="col-sm-3 control-label">Region:</label>
                <div class="col-sm-9">
                    <select :disabled="isReadOnly" class="form-select" @change="filterDistrict($event)" v-model="species_community.region_id" placeholder="Select Region">
                        <option v-for="option in region_list" :value="option.id" v-bind:key="option.id">
                            {{ option.name }}                            
                        </option>
                    </select>
                </div>
            </div>
            <div class="row mb-3">
                <label for="" class="col-sm-3 control-label">District:</label>
                <div class="col-sm-9">
                    <select :disabled="isReadOnly" class="form-select" v-model="species_community.district_id" placeholder="Select District">
                        <option v-for="option in filtered_district_list" :value="option.id" v-bind:key="option.id">
                            {{ option.name }}                            
                        </option>
                    </select>
                </div>
            </div>
        <!-- </FormSection>
        <FormSection :formCollapse="false" label="Ecological Communities" Index="ecological_communities"> -->
            <div class="row mb-3">
                <label for="" class="col-sm-3 control-label">Number of Occurrences:</label>
                <div class="col-sm-6">
                    <input :disabled="isNOOReadOnly" type="number" class="form-control" id="no_of_occurrences" placeholder="" v-model="species_community.distribution.number_of_occurrences"/>
                </div>
                <div class="col-sm-3">    
                    <input :disabled="isReadOnly" type="radio" value="true" 
                            class="form-check-input" id="noo_auto" @click="switchNOO('true')"
                            v-model="species_community.distribution.noo_auto">
                    <label>auto</label>
                    <input :disabled="isReadOnly" type="radio" value="false" 
                            class="form-check-input" id="noo_manual" @click="switchNOO('false')"
                            v-model="species_community.distribution.noo_auto">
                    <label>manual</label>
                </div>
            </div>
            <div class="row mb-3">
                <label for="" class="col-sm-3 control-label">Extent of Occurrence (km2):</label>
                <div class="col-sm-6">
                    <input :disabled="isEOOReadOnly" type="number" class="form-control" id="extent_of_occurrence" 
                    placeholder="" v-model="species_community.distribution.extent_of_occurrences"/>
                </div>
                 <div class="col-sm-3">    
                    <input :disabled="isReadOnly" type="radio" value="true" 
                            class="form-check-input" id="eoo_auto" @click="switchEOO('true')"
                            v-model="species_community.distribution.eoo_auto">
                    <label>auto</label>
                    <input :disabled="isReadOnly" type="radio" value="false" 
                            class="form-check-input" id="eoo_manual" @click="switchEOO('false')"
                            v-model="species_community.distribution.eoo_auto">
                    <label>manual</label>
                </div>
            </div>
            <div class="row mb-3">
                <label for="" class="col-sm-3 control-label">Area of Occupancy<br>(10km x 10km):</label>
                <div class="col-sm-6">
                    <input :disabled="isAOOReadOnly" type="number" class="form-control" id="area_of_occupany" placeholder="" 
                    v-model="species_community.distribution.area_of_occupancy"/>
                </div>
                 <div class="col-sm-3">    
                    <input :disabled="isReadOnly" type="radio" value="true" 
                            class="form-check-input" id="aoo_auto" @click="switchAOO('true')"
                            v-model="species_community.distribution.aoo_auto">
                    <label>auto</label>
                    <input :disabled="isReadOnly" type="radio" value="false" 
                            class="form-check-input" id="aoo_manual" @click="switchAOO('false')"
                            v-model="species_community.distribution.aoo_auto">
                    <label>manual</label>
                </div>
            </div>
            <div class="row mb-3">
                <label for="" class="col-sm-3 control-label">Area of Occupancy Actual (km2):</label>
                <div class="col-sm-6">
                    <input :disabled="isAOOActualReadOnly" type="number" step="any" class="form-control" id="area_of_occupancy_actual" placeholder="" 
                    v-model="species_community.distribution.area_of_occupancy_actual"/>
                </div>
                <div class="col-sm-3">    
                    <input :disabled="isReadOnly" type="radio" value="true"
                            class="form-check-input" id="aoo_actual_auto" @click="switchAOOActual('true')"
                            v-model="species_community.distribution.aoo_actual_auto">
                    <label>auto</label>
                    <input :disabled="isReadOnly" type="radio" value="false"
                            class="form-check-input" id="aoo_actual_manual" @click="switchAOOActual('false')"
                            v-model="species_community.distribution.aoo_actual_auto">
                    <label>manual</label>
                </div>
            </div>
            <div class="row mb-3">
                <label for="" class="col-sm-3 control-label">Number of IUCN Locations:</label>
                <div class="col-sm-9">
                    <input :disabled="isReadOnly" type="number" class="form-control" id="no_of_iucn_locations"
                    placeholder="" v-model="species_community.distribution.number_of_iucn_locations"/>
                </div>
            </div>
            <div class="row mb-3">
                <label for="" class="col-sm-3 control-label">Community Original Area (ha):</label>
                <div class="col-sm-9">
                    <input :disabled="isReadOnly" type="number" class="form-control" id="community_original_area" placeholder="" v-model="species_community.distribution.community_original_area"/>
                </div>
            </div>
            <div class="row mb-3">
                <label for="" class="col-sm-3 control-label">Community Original Area (+/- ha) Accuracy:</label>
                <div class="col-sm-9">
                    <input :disabled="isReadOnly" type="number" class="form-control" id="community_original_area_accuracy" placeholder=""
                    v-model="species_community.distribution.community_original_area_accuracy"/>
                </div>
            </div>
            <div class="row mb-3">
                <label for="" class="col-sm-3 control-label">Community Original Area (ha) Reference:</label>
                <div class="col-sm-9">
                    <input :disabled="isReadOnly" type="text" class="form-control" id="community_original_area_reference" placeholder=""
                    v-model="species_community.distribution.community_original_area_reference"/>
                </div>
            </div>
        </FormSection>
        <FormSection :formCollapse="false" label="Conservation Attributes" Index="conservation_attributes">
            <!-- <div class="row mb-3">
                <label for="" class="col-sm-3 control-label">Habitat/Growth Form:</label>
                <div class="col-sm-9">
                    <textarea :disabled="isReadOnly" type="text" class="form-control"
                    id="habitat_growth_form" placeholder="" 
                    v-model="species_community.conservation_attributes.habitat_growth_form"/>
                </div>
            </div> -->
            <div class="row mb-3">
                <label for="" class="col-sm-3 control-label">Pollinator Information:</label>
                <div class="col-sm-9">
                    <!-- <select :disabled="isReadOnly" class="form-select"
                        v-model="species_community.conservation_attributes.pollinator_information_id">
                        <option v-for="option in pollinator_info_list" :value="option.id" v-bind:key="option.id">
                            {{ option.name }}                            
                        </option>
                    </select> -->
                    <textarea :disabled="isReadOnly" type="text" class="form-control"
                    id="pollinator_info" placeholder="" 
                    v-model="species_community.conservation_attributes.pollinator_information"/>
                </div>
            </div>
            <div class="row mb-3">
                <label for="" class="col-sm-3 control-label">Minimum Fire Interval:</label>
                <div class="col-sm-3">
                    <input class="form-check-input" type="checkbox" name="minimum_fire_interval_range" id="minimum_fire_interval_range"
                        v-model="minimum_fire_interval_range" :disabled="isReadOnly" @change="handleMinimumFireIntervalRange()" />
                    <label for="" class="control-label">Range</label>
                </div>
                <label for="" class="col-sm-6 control-label" style="color: red;">{{ errors.minimum_fire_interval_error }}</label>
            </div>
            <div class="row mb-3" v-if="!minimum_fire_interval_range">
                <label for="" class="col-sm-3 control-label"></label>
                <div class="col-sm-3 interval-margin">
                    <input :disabled="isReadOnly" type="number" class="form-control" 
                    id="minimum_fire_interval_from" placeholder="" @change="validateMinimumFireIntervalRange()"
                    v-model="species_community.conservation_attributes.minimum_fire_interval_from"/>
                </div>
                <div class="col-sm-2">
                    <select :disabled="isReadOnly" class="form-select" @change="validateMinimumFireIntervalRange()"
                        v-model="species_community.conservation_attributes.minimum_fire_interval_choice">
                        <option v-for="option in interval_choice" :value="option.id" v-bind:key="option.id">
                            {{ option.name }}                            
                        </option>
                    </select>
                </div>
                <div class="col-sm-4">
                    <label for="" class="control-label">{{ minFireIntervalMonthsComputed}}</label>
                </div>
            </div>

            <div class="row mb-3" v-else>
                    <label for="" class="col-sm-3 control-label"></label>
                    <label for="" class="col-sm-2 control-label">From:</label>
                    <div class="col-sm-2 interval-range-true-input">
                        <input :disabled="isReadOnly" type="number" class="form-control" 
                        id="minimum_fire_interval_from" placeholder="" @change="validateMinimumFireIntervalRange()"
                        v-model="species_community.conservation_attributes.minimum_fire_interval_from"/>
                    </div>
                    <label for="" class="col-sm-2 control-label">To:</label>
                    <div class="col-sm-2 interval-range-true-input">
                        <input :disabled="isReadOnly" type="number" class="form-control" 
                        id="minimum_fire_interval_to" placeholder="" @change="validateMinimumFireIntervalRange()"
                        v-model="species_community.conservation_attributes.minimum_fire_interval_to"/>
                    </div>
                    <div class="col-sm-2">
                        <select :disabled="isReadOnly" class="form-select" @change="validateMinimumFireIntervalRange()"
                            v-model="species_community.conservation_attributes.minimum_fire_interval_choice">
                            <option v-for="option in interval_choice" :value="option.id" v-bind:key="option.id">
                                {{ option.name }}                            
                            </option>
                        </select>
                    </div>
            </div>
            <div class="row mb-3">
                <label for="" class="col-sm-3 control-label">Response to Fire:</label>
                <div class="col-sm-9">
                    <textarea :disabled="isReadOnly" type="text" class="form-control" id="response_to_fire" placeholder="" v-model="species_community.conservation_attributes.response_to_fire"/>
                </div>
            </div>
            <div class="row mb-3">
                <label for="" class="col-sm-3 control-label">Post Fire Habitat Interactions:</label>
                <div class="col-sm-9">
                    <select :disabled="isReadOnly" class="form-select"
                        v-model="species_community.conservation_attributes.post_fire_habitat_interaction_id">
                        <option v-for="option in post_fire_habitatat_interactions_list" :value="option.id" v-bind:key="option.id">
                            {{ option.name }}                            
                        </option>
                    </select>
                </div>
            </div>
            <div class="row mb-3">
                <label for="" class="col-sm-3 control-label">Hydrology:</label>
                <div class="col-sm-9">
                    <textarea :disabled="isReadOnly" type="text" class="form-control" id="hydrology" 
                    placeholder="" v-model="species_community.conservation_attributes.hydrology"/>
                </div>
            </div>
            <div class="row mb-3">
                <label for="" class="col-sm-3 control-label">Ecological Community and Biological Information:
                </label>
                <div class="col-sm-9">
                    <textarea :disabled="isReadOnly" type="text" class="form-control" 
                    id="ecological_biological_information" placeholder="" 
                    v-model="species_community.conservation_attributes.ecological_and_biological_information"/>
                </div>
            </div>
            <div class="row mb-3">
                <label for="" class="col-sm-3 control-label">Research Requirements:</label>
                <div class="col-sm-9">
                    <textarea :disabled="isReadOnly" type="text" class="form-control" 
                    id="research_requirements" 
                    placeholder="" v-model="species_community.conservation_attributes.research_requirements"/>
                </div>
            </div>
            <div class="row mb-3">
                <label for="" class="col-sm-3 control-label">Response to Dieback:</label>
                <div class="col-sm-9">
                    <textarea :disabled="isReadOnly" type="text" class="form-control" 
                    id="response_to_dieback" 
                    placeholder="" v-model="species_community.conservation_attributes.response_to_dieback"/>
                </div>
            </div>
            <div class="row mb-3">
                <label for="" class="col-sm-3 control-label">Other relevant diseases:</label>
                <div class="col-sm-9">
                    <textarea :disabled="isReadOnly" type="text" class="form-control" 
                    id="other_relevant_diseases" 
                    placeholder="" v-model="species_community.conservation_attributes.other_relevant_diseases"/>
                </div>
            </div>
        </FormSection>
        <FormSection :formCollapse="false" label="General" Index="general">
            <div class="row mb-3">
                <label for="" class="col-sm-3 control-label">Department File Numbers:</label>
                <div class="col-sm-9">
                    <input :disabled="isReadOnly" type="text" class="form-control" id="department_file_numbers" placeholder="" v-model="species_community.distribution.department_file_numbers"/>
                </div>
            </div>
            <div class="row mb-3">
                <label for="" class="col-sm-3 control-label">Last data curration date: </label>
                <div class="col-sm-9">
                     <input :disabled="isReadOnly" type="date" class="form-control" name="last_data_curration_date" 
                    ref="last_data_curration_date" @change="checkDate()" v-model="species_community.last_data_curration_date" />
                </div>
            </div>
            <div class="row mb-3">
                <label for="" class="col-sm-3 control-label">Comment:</label>
                <div class="col-sm-9">
                    <textarea :disabled="isReadOnly" class="form-control" rows="3" id="comment" placeholder=""
                    v-model="species_community.comment"/>
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
// require("select2/dist/css/select2.min.css");
// require("select2-bootstrap-5-theme/dist/select2-bootstrap-5-theme.min.css")

export default {
        name: 'Community',
        props:{
            species_community:{
                type: Object,
                required:true
            },
        },
        data:function () {
            let vm = this;
            return{
                // community_name_lookup: 'community_name_lookup' + vm._uid,
                // select_community_name: "select_community_name"+ vm._uid,
                species_list: [],
                // taxon_names: [],
                community_profile_dict: {},
                post_fire_habitatat_interactions_list: [],
                region_list: [],
                district_list: [],
                filtered_district_list: [],
                minimum_fire_interval_range: false,
                interval_choice: [{id: 1, name: 'year/s'},
                {id: 2, name: 'month/s'}
                ],
                errors:{
                    minimum_fire_interval_error:null
                },
                // community_name_display:'',
                // community_migrated_id: null,
                // community_description: null,
                // previous_name:null,
                // name_authority: null,
                // name_comments: null,
            }
        },
        components: {
            FormSection,
        },
        computed: {
            isReadOnly: function(){
                let action = this.$route.query.action;
                if(action === "edit" && this.species_community && this.species_community.user_edit_mode){
                    return false;
                }
                else{
                    return this.species_community.readonly;
                }
            },
            isNOOReadOnly: function(){
                let vm = this;
                if(vm.species_community.distribution.noo_auto === true){
                    return true;
                }
                else{
                    return vm.isReadOnly;
                }
            },
            isEOOReadOnly: function(){
                let vm = this;
                if(vm.species_community.distribution.eoo_auto === true){
                    return true;
                }
                else{
                    return vm.isReadOnly;
                }
            },
            isAOOReadOnly: function(){
                let vm = this;
                if(vm.species_community.distribution.aoo_auto === true){
                    return true;
                }
                else{
                    return vm.isReadOnly;
                }
            },
            isAOOActualReadOnly: function(){
                let vm = this;
                if(vm.species_community.distribution.aoo_actual_auto === true){
                    return true;
                }
                else{
                    return vm.isReadOnly;
                }
            },
            minFireIntervalMonthsComputed: function(){

                const totalMonths = parseInt(this.species_community.conservation_attributes.minimum_fire_interval_from);
                const intervalChoice = this.species_community.conservation_attributes.minimum_fire_interval_choice;

                if(totalMonths > 12 && intervalChoice == 2){
                    const years = Math.floor(totalMonths / 12);
                    const months = totalMonths % 12;
                    return years + " year/s " + months + " month/s";
                }
                else{
                    return ""
                }
            }
        },
        watch:{
            "species_community.distribution.number_of_iucn_locations": function(newVal) {
                let vm=this;
                if(newVal == ""){
                        vm.species_community.distribution.number_of_iucn_locations=null;
                    }
            },
            "species_community.distribution.community_original_area": function(newVal) {
                let vm=this;
                if(newVal == ""){
                        vm.species_community.distribution.community_original_area=null;
                    }
            },
            "species_community.distribution.community_original_area_accuracy": function(newVal) {
                let vm=this;
                if(newVal == ""){
                        vm.species_community.distribution.community_original_area_accuracy=null;
                    }
            },
            "species_community.distribution.community_original_area_reference": function(newVal) {
                let vm=this;
                if(newVal == ""){
                        vm.species_community.distribution.community_original_area_reference=null;
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
            eventListeners:function (){
                let vm=this;

                var date= new Date()
                var today= new Date(date.getFullYear(), date.getMonth(), date.getDate());
            },
            handleMinimumFireIntervalRange: function (e){
                if(this.minimum_fire_interval_range == false){
                    this.species_community.conservation_attributes.minimum_fire_interval_to = null;
                }
            },
            validateMinimumFireIntervalRange: function(){
                const rangeFrom = parseInt(this.species_community.conservation_attributes.minimum_fire_interval_from);
                const rangeTo = parseInt(this.species_community.conservation_attributes.minimum_fire_interval_to);
                const intervalChoice = this.species_community.conservation_attributes.minimum_fire_interval_choice;
                if ((rangeFrom != null || rangeTo!= null) && intervalChoice == null){
                    this.errors.minimum_fire_interval_error = "Please select years/months";
                }
                else if(rangeFrom >= rangeTo){
                    this.errors.minimum_fire_interval_error = "Please enter a valid range";
                }
                else{
                    this.errors.minimum_fire_interval_error = "";
                }
            },
            switchNOO: function(value){
                let vm=this;
                var selectedValue = value;
                if(selectedValue === "true"){
                    swal.fire({
                        title: "Warning",
                        text: "Selection of 'auto' will overwrite the existing data. Are you sure you want to select 'auto'?",
                        icon: "warning",
                        showCancelButton: true,
                        confirmButtonText: 'ok',
                        confirmButtonColor:'#d9534f'
                    }).then((swalresult) => {
                        if(swalresult.isConfirmed){
                            vm.species_community.distribution.number_of_occurrences=vm.species_community.distribution.cal_number_of_occurrences;
                            document.getElementById("noo_auto").checked = true;
                            document.getElementById("noo_manual").checked = false;
                            vm.species_community.distribution.noo_auto= true
                        }else if (swalresult.dismiss === swal.DismissReason.cancel){
                            document.getElementById("noo_manual").checked = true;
                            document.getElementById("noo_auto").checked = false;
                            vm.species_community.distribution.noo_auto= false
                            vm.species_community.distribution.number_of_occurrences=vm.species_community.distribution.number_of_occurrences;
                        }

                    },(error) => {
                        console.error('Error:', error);
                    });
                }
                else{
                    vm.species_community.distribution.number_of_occurrences=null;
                    document.getElementById("noo_manual").checked = true;
                    document.getElementById("noo_auto").checked = false;
                    vm.species_community.distribution.noo_auto= false
                }
            },
            switchEOO: function(value){
                let vm=this;
                var selectedValue = value;
                if(selectedValue === "true"){
                    swal.fire({
                        title: "Warning",
                        text: "Selection of 'auto' will overwrite the existing data. Are you sure you want to select 'auto'?",
                        icon: "warning",
                        showCancelButton: true,
                        confirmButtonText: 'ok',
                        confirmButtonColor:'#d9534f'
                    }).then((swalresult) => {
                        if(swalresult.isConfirmed){
                            // set EOO field to calculted_EOO vale
                            vm.species_community.distribution.extent_of_occurrences=vm.species_community.distribution.cal_extent_of_occurrences;
                            document.getElementById("eoo_auto").checked = true;
                            document.getElementById("eoo_manual").checked = false;
                            // set eoo to true to fire the change of value so the EOO input box readonly
                            vm.species_community.distribution.eoo_auto= true;
                        }else if (swalresult.dismiss === swal.DismissReason.cancel){
                            document.getElementById("eoo_manual").checked = true;
                            document.getElementById("eoo_auto").checked = false;
                            // set eoo to false to fire the change of value so the EOO input box will be editable
                            vm.species_community.distribution.eoo_auto= false;
                            //Otherwise revert back to its manual value if swal cancelled 
                            vm.species_community.distribution.extent_of_occurrences=vm.species_community.distribution.extent_of_occurrences;
                        }

                    },(error) => {
                        console.error('Error:', error);
                    });
                }
                else{
                    // set EOO value to null if manual selected
                    vm.species_community.distribution.extent_of_occurrences=null;
                    document.getElementById("eoo_manual").checked = true;
                    document.getElementById("eoo_auto").checked = false;
                    // set eoo to false to fire the change of value so the EOO input box will be editable
                    vm.species_community.distribution.eoo_auto= false;
                }
            },
            switchAOO: function(value){
                let vm=this;
                var selectedValue = value;
                if(selectedValue === "true"){
                    swal.fire({
                        title: "Warning",
                        text: "Selection of 'auto' will overwrite the existing data. Are you sure you want to select 'auto'?",
                        icon: "warning",
                        showCancelButton: true,
                        confirmButtonText: 'ok',
                        confirmButtonColor:'#d9534f'
                    }).then((swalresult) => {
                        if(swalresult.isConfirmed){
                            // set AOO field to calculated_AOO value
                            vm.species_community.distribution.area_of_occupancy = vm.species_community.distribution.cal_area_of_occupancy;
                            document.getElementById("aoo_auto").checked = true;
                            document.getElementById("aoo_manual").checked = false;
                            // set aoo to true to fire the change of value so the AOO input box readonly
                            vm.species_community.distribution.aoo_auto= true;
                        }else if (swalresult.dismiss === swal.DismissReason.cancel){
                            document.getElementById("aoo_manual").checked = true;
                            document.getElementById("aoo_auto").checked = false;
                            // set aoo to false to fire the change of value so the AOO input box will be editable
                            vm.species_community.distribution.aoo_auto = false;
                            //Otherwise revert back to its manual value if swal cancelled 
                            vm.species_community.distribution.area_of_occupancy = vm.species_community.distribution.area_of_occupancy;
                        }

                    },(error) => {
                        console.error('Error:', error);
                    });
                }
                else{
                    // set EOO value to null if manual selected
                    vm.species_community.distribution.area_of_occupancy=null;
                    document.getElementById("aoo_manual").checked = true;
                    document.getElementById("aoo_auto").checked = false;
                    // set aoo to false to fire the change of value so the AOO input box will be editable
                    vm.species_community.distribution.aoo_auto= false;
                }
            },
            switchAOOActual: function(value){
                let vm=this;
                var selectedValue = value;
                if(selectedValue === "true"){
                    swal.fire({
                        title: "Warning",
                        text: "Selection of 'auto' will overwrite the existing data. Are you sure you want to select 'auto'?",
                        icon: "warning",
                        showCancelButton: true,
                        confirmButtonText: 'ok',
                        confirmButtonColor:'#d9534f'
                    }).then((swalresult) => {
                        if(swalresult.isConfirmed){
                            // set AOOActual field to calculted_AOOActual vale
                            vm.species_community.distribution.area_of_occupancy_actual=vm.species_community.distribution.cal_area_of_occupancy_actual;
                            document.getElementById("aoo_actual_auto").checked = true;
                            document.getElementById("aoo_actual_manual").checked = false;
                            // set aoo_actual to true to fire the change of value so the AOOActual input box readonly
                            vm.species_community.distribution.aoo_actual_auto= true;
                        }else if (swalresult.dismiss === swal.DismissReason.cancel){
                            document.getElementById("aoo_actual_manual").checked = true;
                            document.getElementById("aoo_actual_auto").checked = false;
                            // set eoo to false to fire the change of value so the EOO input box will be editable
                            vm.species_community.distribution.aoo_actual_auto= false;
                            //Otherwise revert back to its manual value if swal cancelled 
                            vm.species_community.distribution.area_of_occupancy_actual=vm.species_community.distribution.area_of_occupancy_actual;
                        }

                    },(error) => {
                        console.error('Error:', error);
                    });
                }
                else{
                    // set AOOActual value to null if manual selected
                    vm.species_community.distribution.area_of_occupancy_actual=null;
                    document.getElementById("aoo_actual_manual").checked = true;
                    document.getElementById("aoo_actual_auto").checked = false;
                    // set aoo_actual to false to fire the change of value so the AOOActual input box will be editable
                    vm.species_community.distribution.aoo_actual_auto= false;
                }
            },
        },
        created: async function() {
            let vm = this;
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
            if(vm.species_community.conservation_attributes.minimum_fire_interval_to != null && 
                vm.species_community.conservation_attributes.minimum_fire_interval_to != "" && 
                    vm.species_community.conservation_attributes.minimum_fire_interval_to != undefined)
            {
                vm.minimum_fire_interval_range = true;
            }
            //-----fetch species_list
            // const res = await Vue.http.get('/api/species/species_list.json');
            // vm.species_list= res.body.data;
            //--------get api taxon_names
            // vm.$http.get(api_endpoints.community_taxonomy+'/taxon_names.json').then((response) => {
            //     vm.taxon_names = response.body;
            // });
            //------fetch list of values
            const res_obj = await Vue.http.get('/api/community_profile_dict/');
            vm.community_profile_dict = res_obj.body;
            vm.post_fire_habitatat_interactions_list = vm.community_profile_dict.post_fire_habitatat_interactions_list;
            vm.post_fire_habitatat_interactions_list.splice(0,0,
                {
                    id: null,
                    name: null,
                });
            const response = await Vue.http.get('/api/region_district_filter_dict/');
            vm.filterRegionDistrict= response.body;
            vm.region_list = vm.filterRegionDistrict.region_list;
            vm.district_list= vm.filterRegionDistrict.district_list;
            vm.region_list.splice(0,0,
            {
                id: null,
                name: null,
            });
            this.filterDistrict();
            // this.loadTaxonomydetails();
        },
        mounted: function(){
            let vm = this;
            // vm.initialiseCommunityNameLookup();
            // vm.loadTaxonomydetails();
            // Initialise select2 for Species
            // $(vm.$refs.species_select).select2({
            //     "theme": "bootstrap-5",
            //     allowClear: true,
            //     placeholder:"Select Species",
            //     multiple: true,
            // }).
            // on("select2:select",function (e) {
            //     var selected = $(e.currentTarget);
            //     vm.species_community.species = selected.val();
            // }).
            // on("select2:unselect",function (e) {
            //     var selected = $(e.currentTarget);
            //     vm.species_community.species = selected.val();
            // });
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
        padding: 0.375rem 2.25rem 0.375rem 0.75rem;
    }
    .interval-margin{
        width: 20%;
    }
    .interval-range-true-input{
        margin-left: -70px;
    }
</style>

