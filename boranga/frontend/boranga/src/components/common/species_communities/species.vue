<template lang="html">
    <div id="species">
        <FormSection :formCollapse="false" label="Taxonomy" Index="taxonomy">
            <div class="row form-group">
                <label for="" class="col-sm-3 control-label">Previous Name:</label>
                <div class="col-sm-9">
                    <input :disabled="proposal.readonly" type="text" class="form-control" id="previous_name" placeholder="" 
                    v-model="species.taxonomy_details.previous_name"/>
                </div>
            </div>
            <div class="row form-group">
                <label for="" class="col-sm-3 control-label">Family:</label>
                <div class="col-sm-9">
                    <input :disabled="proposal.readonly" type="text" class="form-control" id="family" placeholder="" 
                    v-model="species.taxonomy_details.family"/>
                </div>
            </div>
            <div class="row form-group">
                <label for="" class="col-sm-3 control-label">Genus:</label>
                <div class="col-sm-9">
                    <input :disabled="proposal.readonly" type="text" class="form-control" id="genus" placeholder="" 
                    v-model="species.taxonomy_details.genus"/>
                </div>
            </div>
            <div class="row form-group">
                <label for="" class="col-sm-3 control-label">Phylogenetic Group:</label>
                <div class="col-sm-9">
                    <input :disabled="proposal.readonly" type="text" class="form-control" id="phylogenetic_group" placeholder="" v-model="species.taxonomy_details.phylogenetic_group"/>
                </div>
            </div>
            <div class="row form-group">
                <label for="" class="col-sm-3 control-label">Name Authority:</label>
                <div class="col-sm-9">
                    <input :disabled="proposal.readonly" type="text" class="form-control" id="name_authority" placeholder="" 
                    v-model="species.taxonomy_details.name_authority_details.name"/>
                </div>
            </div>
            <div class="row form-group">
                <label for="" class="col-sm-3 control-label">Common Name:</label>
                <div class="col-sm-9">
                    <input :disabled="proposal.readonly" type="text" class="form-control" id="common_name" placeholder="" 
                    v-model="species.common_name"/>
                </div>
            </div>
            <div class="row form-group">
                <label for="" class="col-sm-3 control-label">Taxon Id:</label>
                <div class="col-sm-9">
                    <input :disabled="proposal.readonly" type="text" class="form-control" id="taxon_id" placeholder="" 
                    v-model="species.taxonomy_details.taxon_id"/>
                </div>
            </div>
            <div class="row form-group">
                <label for="" class="col-sm-3 control-label">Comments:</label>
                <div class="col-sm-9">
                    <textarea :disabled="proposal.readonly" class="form-control" id="comment" placeholder=""
                    v-model="species.conservation_attributes.comments"/>
                </div>
            </div>
        </FormSection>
        <FormSection :formCollapse="false" label="Distribution" Index="distribution">
            <div class="row form-group">
                <label for="" class="col-sm-3 control-label">Region:</label>
                <div class="col-sm-9">
                    <input :disabled="proposal.readonly" type="text" class="form-control" id="region" placeholder="" 
                    v-model="species.region"/>
                </div>
            </div>
            <div class="row form-group">
                <label for="" class="col-sm-3 control-label">District:</label>
                <div class="col-sm-9">
                    <input :disabled="proposal.readonly" type="text" class="form-control" id="district" placeholder="" 
                    v-model="species.district"/>
                </div>
            </div>
            <div class="row form-group">
                <label for="" class="col-sm-3 control-label">Number of Occurrences:</label>
                <div class="col-sm-9">
                    <input :disabled="proposal.readonly" type="text" class="form-control" id="no_of_occurrences" placeholder="" 
                    v-model="species.distribution.number_of_occurrences"/>
                </div>
            </div>
            <div class="row form-group">
                <label for="" class="col-sm-3 control-label">Extent of Occurrence:</label>
                <div class="col-sm-9">
                    <input :disabled="proposal.readonly" type="text" class="form-control" id="extent_of_occurrence" placeholder="" 
                    v-model="species.distribution.extent_of_occurrences"/>
                </div>
            </div>
            <div class="row form-group">
                <label for="" class="col-sm-3 control-label">Area of Occupancy<br>(Actual):</label>
                <div class="col-sm-9">
                    <input :disabled="proposal.readonly" type="text" class="form-control" id="area_of_occupancy_actual" placeholder="" 
                    v-model="species.distribution.area_of_occupancy"/>
                </div>
            </div>
            <div class="row form-group">
                <label for="" class="col-sm-3 control-label">Area of Occupancy<br>(2km x 2km):</label>
                <div class="col-sm-9">
                    <input :disabled="proposal.readonly" type="text" class="form-control" id="area_of_occupany" placeholder="" 
                    v-model="species.distribution.area_of_occupancy"/>
                </div>
            </div>
            <div class="row form-group">
                <label for="" class="col-sm-3 control-label">Number of IUCN Locations:</label>
                <div class="col-sm-9">
                    <input :disabled="proposal.readonly" type="text" class="form-control" id="no_of_iucn_locations" placeholder="" 
                    v-model="species.distribution.number_of_iucn_locations"/>
                </div>
            </div>
        </FormSection>
        <FormSection :formCollapse="false" label="Conservation Attributes" Index="conservation_attributes">
            <div class="row form-group">
                <label for="" class="col-sm-3 control-label">General Management Advice:</label>
                <div class="col-sm-9">
                    <input :disabled="proposal.readonly" type="text" class="form-control" id="general_management_advice" placeholder=""v-model="species.conservation_attributes.general_management_advice"/>
                </div>
            </div>
            <div class="row form-group">
                <label for="" class="col-sm-3 control-label">Biological Attributes:</label>
                <div class="col-sm-9">
                    <input :disabled="proposal.readonly" type="text" class="form-control" id="biological_attributes" placeholder=""
                    v-model="species.conservation_attributes.biological_attributes"/>
                </div>
            </div>
            <div class="row form-group">
                <label for="" class="col-sm-3 control-label">Specific Survey Advice:</label>
                <div class="col-sm-9">
                    <input :disabled="proposal.readonly" type="text" class="form-control" id="specific_survey_advice" placeholder=""
                    v-model="species.conservation_attributes.specific_survey_advice"/>
                </div>
            </div>
        </FormSection>
        <FormSection :formCollapse="false" label="Conservation Status" Index="conservation_status">
            <div class="row form-group">
                <div class="col-sm-12">
                    <ConservationStatusDatatable :disabled="proposal.readonly" :species="species">
                    </ConservationStatusDatatable>
            </div>
            </div>
        </FormSection>
        <FormSection :formCollapse="false" label="" Index="">
            <div class="row form-group">
                <label for="" class="col-sm-3 control-label">Department File Numbers:</label>
                <div class="col-sm-9">
                    <input :disabled="proposal.readonly" type="text" class="form-control" id="department_file_numbers" placeholder="" v-model="species.distribution.department_file_numbers"/>
                </div>
            </div>
            <!-- TODO get the all data curation date -->
            <div class="row form-group">
                <label for="" class="col-sm-3 control-label">Last data curation date: </label>
                <div class="col-sm-9 input-groyp date" ref="dataCurationDatePicker">
                    <input :disabled="proposal.readonly" type="text" class="form-control" id="data_curation_date" 
                    placeholder="DD/MM/YYYY" />
                    <span class="input-group-addon">
                        <span class="glyphicon glyphicon-calendar"></span>
                    </span>
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
        props:{
            proposal:{
                type: Object,
                required:true
            },
            species:{
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
            eventListeners:function (){
                let vm=this;

                var date= new Date()
                var today= new Date(date.getFullYear(), date.getMonth(), date.getDate());

                //$(vm.$refs.accreditation_expiry).datetimepicker(vm.datepickerOptions);
                },
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

