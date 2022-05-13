<template lang="html">
    <div id="community">
        <FormSection :formCollapse="false" label="Taxonomy" Index="taxonomy">
            <div class="row form-group">
                <label for="" class="col-sm-3 control-label">Community Id:</label>
                <div class="col-sm-9">
                    <input :disabled="species_community.readonly" type="text" class="form-control" id="community_id" placeholder="" 
                    v-model="species_community.community_id"/>
                </div>
            </div>
            <div class="row form-group">
                <label for="" class="col-sm-3 control-label">Community Name:</label>
                <div class="col-sm-9">
                    <input :disabled="species_community.readonly" type="text" class="form-control" id="community_name" placeholder="" 
                    v-model="species_community.community_name"/>
                </div>
            </div>
            <div class="row form-group">
                <label for="" class="col-sm-3 control-label">Community Status:</label>
                <div class="col-sm-9">
                    <textarea :disabled="species_community.readonly" class="form-control" id="community_status" placeholder=""
                    v-model="species_community.community_status"/>
                </div>
            </div>
        </FormSection>
        <FormSection :formCollapse="false" label="Distribution" Index="distribution">
            <div class="row form-group">
                <label for="" class="col-sm-3 control-label">Region:</label>
                <div class="col-sm-9">
                    <input :disabled="species_community.readonly" type="text" class="form-control" id="region" placeholder="" 
                    v-model="species_community.region"/>
                </div>
            </div>
            <div class="row form-group">
                <label for="" class="col-sm-3 control-label">District:</label>
                <div class="col-sm-9">
                    <input :disabled="species_community.readonly" type="text" class="form-control" id="district" placeholder="" 
                    v-model="species_community.district"/>
                </div>
            </div>
        </FormSection>
        <FormSection :formCollapse="false" label="Ecological Communities" Index="ecological_communities">
            <!-- <div class="row form-group">
                <label for="" class="col-sm-3 control-label">General Management Advice:</label>
                <div class="col-sm-9">
                    <input :disabled="species_community.readonly" type="text" class="form-control" id="general_management_advice" placeholder=""v-model="species_community.conservation_attributes.general_management_advice"/>
                </div>
            </div>
            <div class="row form-group">
                <label for="" class="col-sm-3 control-label">Biological Attributes:</label>
                <div class="col-sm-9">
                    <input :disabled="species_community.readonly" type="text" class="form-control" id="biological_attributes" placeholder=""
                    v-model="species_community.conservation_attributes.biological_attributes"/>
                </div>
            </div>
            <div class="row form-group">
                <label for="" class="col-sm-3 control-label">Specific Survey Advice:</label>
                <div class="col-sm-9">
                    <input :disabled="species_community.readonly" type="text" class="form-control" id="specific_survey_advice" placeholder=""
                    v-model="species_community.conservation_attributes.specific_survey_advice"/>
                </div>
            </div> -->
        </FormSection>
        <FormSection :formCollapse="false" label="Conservation Status" Index="conservation_status">
            <div class="row form-group">
                <div class="col-sm-12">
                    <ConservationStatusDatatable :disabled="species_community.readonly" :species_community="species_community">
                    </ConservationStatusDatatable>
            </div>
            </div>
        </FormSection>
        <FormSection :formCollapse="false" label="" Index="">
            <!-- <div class="row form-group">
                <label for="" class="col-sm-3 control-label">Department File Numbers:</label>
                <div class="col-sm-9">
                    <input :disabled="species_community.readonly" type="text" class="form-control" id="department_file_numbers" placeholder="" v-model="species_community.distribution.department_file_numbers"/>
                </div>
            </div> -->
            <!-- TODO get the all data curation date -->
            <!-- <div class="row form-group">
                <label for="" class="col-sm-3 control-label">Last data curation date: </label>
                <div class="col-sm-9 input-groyp date" ref="dataCurationDatePicker">
                    <input :disabled="species_community.readonly" type="text" class="form-control" id="data_curation_date" 
                    placeholder="DD/MM/YYYY" />
                    <span class="input-group-addon">
                        <span class="glyphicon glyphicon-calendar"></span>
                    </span>
                </div>
            </div> -->
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
        name: 'Community',
        props:{
            proposal:{
                type: Object,
                required:true
            },
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

