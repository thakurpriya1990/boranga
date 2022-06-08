<template lang="html">
    <div id="species">
        <FormSection :formCollapse="false" label="Taxonomy" Index="taxonomy">
            <div class="row form-group">
                <label for="" class="col-sm-3 control-label">Previous Name:</label>
                <div class="col-sm-9">
                    <input :disabled="species_community.readonly" type="text" class="form-control" id="previous_name" placeholder="" 
                    v-model="species_community.taxonomy_details.previous_name"/>
                </div>
            </div>
            <div class="row form-group">
                <label for="" class="col-sm-3 control-label">Family:</label>
                <div class="col-sm-9">
                    <input :disabled="species_community.readonly" type="text" class="form-control" id="family" placeholder="" 
                    v-model="species_community.taxonomy_details.family"/>
                </div>
            </div>
            <div class="row form-group">
                <label for="" class="col-sm-3 control-label">Genus:</label>
                <div class="col-sm-9">
                    <input :disabled="species_community.readonly" type="text" class="form-control" id="genus" placeholder="" 
                    v-model="species_community.taxonomy_details.genus"/>
                </div>
            </div>
            <div class="row form-group">
                <label for="" class="col-sm-3 control-label">Phylogenetic Group:</label>
                <div class="col-sm-9">
                    <input :disabled="species_community.readonly" type="text" class="form-control" id="phylogenetic_group" placeholder="" v-model="species_community.taxonomy_details.phylogenetic_group"/>
                </div>
            </div>
            <div class="row form-group">
                <label for="" class="col-sm-3 control-label">Name Authority:</label>
                <div class="col-sm-9">
                    <select :disabled="species_community.readonly" class="form-control" v-model="species_community.taxonomy_details.name_authority_id">
                        <option v-for="option in name_authority_list" :value="option.id" v-bind:key="option.id">
                            {{ option.name }}                            
                        </option>
                    </select>
                </div>
            </div>
            <div class="row form-group">
                <label for="" class="col-sm-3 control-label">Common Name:</label>
                <div class="col-sm-9">
                    <input :disabled="species_community.readonly" type="text" class="form-control" id="common_name" placeholder="" 
                    v-model="species_community.common_name"/>
                </div>
            </div>
            <div class="row form-group">
                <label for="" class="col-sm-3 control-label">Taxon Id:</label>
                <div class="col-sm-9">
                    <input :disabled="species_community.readonly" type="text" class="form-control" id="taxon_id" placeholder="" 
                    v-model="species_community.taxonomy_details.taxon_id"/>
                </div>
            </div>
            <div class="row form-group">
                <label for="" class="col-sm-3 control-label">Comments:</label>
                <div class="col-sm-9">
                    <textarea :disabled="species_community.readonly" class="form-control" id="comment" placeholder=""
                    v-model="species_community.conservation_attributes.comments"/>
                </div>
            </div>
        </FormSection>
        <FormSection :formCollapse="false" label="Distribution" Index="distribution">
            <div class="row form-group">
                <label for="" class="col-sm-3 control-label">Region:</label>
                <div class="col-sm-9">
                    <select :disabled="species_community.readonly" class="form-control" @change="filterDistrict($event)" v-model="species_community.region_id">
                        <option v-for="option in region_list" :value="option.id" v-bind:key="option.id">
                            {{ option.name }}                            
                        </option>
                    </select>
                </div>
            </div>
            <div class="row form-group">
                <label for="" class="col-sm-3 control-label">District:</label>
                <div class="col-sm-9">
                    <select :disabled="species_community.readonly" class="form-control" v-model="species_community.district_id">
                        <option v-for="option in filtered_district_list" :value="option.id" v-bind:key="option.id">
                            {{ option.name }}                            
                        </option>
                    </select>
                </div>
            </div>
            <div class="row form-group">
                <label for="" class="col-sm-3 control-label">Number of Occurrences:</label>
                <div class="col-sm-9">
                    <input :disabled="species_community.readonly" type="number" class="form-control" id="no_of_occurrences" placeholder="" v-model="species_community.distribution.number_of_occurrences"/>
                </div>
            </div>
            <div class="row form-group">
                <label for="" class="col-sm-3 control-label">Extent of Occurrence:</label>
                <div class="col-sm-9">
                    <input :disabled="species_community.readonly" type="number" class="form-control" id="extent_of_occurrence" 
                    placeholder="" v-model="species_community.distribution.extent_of_occurrences"/>
                </div>
            </div>
            <div class="row form-group">
                <label for="" class="col-sm-3 control-label">Area of Occupancy<br>(Actual):</label>
                <div class="col-sm-9">
                    <input :disabled="species_community.readonly" type="number" class="form-control" id="area_of_occupancy_actual" placeholder="" v-model="species_community.distribution.area_of_occupancy"/>
                </div>
            </div>
            <div class="row form-group">
                <label for="" class="col-sm-3 control-label">Area of Occupancy<br>(2km x 2km):</label>
                <div class="col-sm-9">
                    <input :disabled="species_community.readonly" type="number" class="form-control" id="area_of_occupany" placeholder="" 
                    v-model="species_community.distribution.area_of_occupancy"/>
                </div>
            </div>
            <div class="row form-group">
                <label for="" class="col-sm-3 control-label">Number of IUCN Locations:</label>
                <div class="col-sm-9">
                    <input :disabled="species_community.readonly" type="number" class="form-control" id="no_of_iucn_locations" 
                    placeholder="" v-model="species_community.distribution.number_of_iucn_locations"/>
                </div>
            </div>
        </FormSection>
        <FormSection :formCollapse="false" label="Conservation Attributes" Index="conservation_attributes">
            <div class="row form-group">
                <label for="" class="col-sm-3 control-label">General Management Advice:</label>
                <div class="col-sm-9">
                    <input :disabled="species_community.readonly" type="text" class="form-control" id="general_management_advice" placeholder=""v-model="species_community.conservation_attributes.general_management_advice"/>
                </div>
            </div>
            <div class="row form-group">
                <label for="" class="col-sm-3 control-label">Biological Attributes:</label>
                <div class="col-sm-9">
                    <input :disabled="species_community.readonly" type="text" class="form-control" id="biological_attributes" placeholder="" v-model="species_community.conservation_attributes.biological_attributes"/>
                </div>
            </div>
            <div class="row form-group">
                <label for="" class="col-sm-3 control-label">Specific Survey Advice:</label>
                <div class="col-sm-9">
                    <input :disabled="species_community.readonly" type="text" class="form-control" id="specific_survey_advice" placeholder="" v-model="species_community.conservation_attributes.specific_survey_advice"/>
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
        <FormSection :formCollapse="false" label="" Index="">
            <div class="row form-group">
                <label for="" class="col-sm-3 control-label">Department File Numbers:</label>
                <div class="col-sm-9">
                    <input :disabled="species_community .readonly" type="text" class="form-control" id="department_file_numbers" placeholder="" v-model="species_community.distribution.department_file_numbers"/>
                </div>
            </div>
            <div class="row form-group">
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
                name_authority_list: [],
                region_list: [],
                district_list: [],
                filtered_district_list: [],
            }
        },
        components: {
            FormSection,
            ConservationStatusDatatable,
        },
        computed: {
        },
        watch:{
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
        },
        created: async function() {
            let vm=this;
            const nameAuthorityResponse = await Vue.http.get('/api/name_authority_list/');
            vm.name_authority_list = nameAuthorityResponse.body;
            vm.name_authority_list.splice(0,0,
                {
                    id: "",
                    name: "",
                });
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
        },
        mounted: function(){
            let vm = this;

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
</style>

