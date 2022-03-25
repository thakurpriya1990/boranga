<template lang="html">
    <div id="species">
        <FormSection label="Taxonomy" Index="taxonomy">
            <div class="row form-group">
                <label for="" class="col-sm-3 control-label">Previous Name:</label>
                <div class="col-sm-9">
                    <input :disabled="proposal.readonly" type="text" class="form-control" id="previous_name" placeholder="" 
                    v-model="species.previous_name"/>
                </div>
            </div>
            <div class="row form-group">
                <label for="" class="col-sm-3 control-label">Family:</label>
                <div class="col-sm-9">
                    <input :disabled="proposal.readonly" type="text" class="form-control" id="family" placeholder="" 
                    v-model="species.family"/>
                </div>
            </div>
            <div class="row form-group">
                <label for="" class="col-sm-3 control-label">Genus:</label>
                <div class="col-sm-9">
                    <input :disabled="proposal.readonly" type="text" class="form-control" id="genus" placeholder="" 
                    v-model="species.genus"/>
                </div>
            </div>
            <div class="row form-group">
                <label for="" class="col-sm-3 control-label">Phylogenetic Group:</label>
                <div class="col-sm-9">
                    <input :disabled="proposal.readonly" type="text" class="form-control" id="phylogenetic_group" placeholder="" v-model="species.phylogenetic_group"/>
                </div>
            </div>
            <div class="row form-group">
                <label for="" class="col-sm-3 control-label">Name Authority:</label>
                <div class="col-sm-9">
                    <input :disabled="proposal.readonly" type="text" class="form-control" id="name_authority" placeholder="" 
                    v-model="species.name_authority"/>
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
                    v-model="species.taxonomy"/>
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
        <FormSection label="Distribution" Index="distribution">
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
        <FormSection label="Conservation Attributes" Index="conservation_attributes">
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
        <FormSection label="" Index="">
            <div class="row form-group">
                <label for="" class="col-sm-3 control-label">Department File Numbers:</label>
                <div class="col-sm-9">
                    <input :disabled="proposal.readonly" type="text" class="form-control" id="department_file_numbers" placeholder="" v-model="species.distribution.department_file_numbers"/>
                </div>
            </div>
            <div class="row form-group">
                <label for="" class="col-sm-3 control-label">Last data curation date: </label>
                <div class="col-sm-9">
                    <input :disabled="proposal.readonly" type="text" class="form-control" id="department_file_numbers" placeholder="" />
                </div>
            </div>
        </FormSection>
        <FormSection label="Conservation Status" Index="conservation_status">
            <div class="row form-group">
                <ConservationStatusDatatable :disabled="proposal.readonly" :species="species">
                </ConservationStatusDatatable>
            </div>
        </FormSection>
    </div>
</template>

<script>
import Vue from 'vue' 
import FormSection from '@/components/forms/section_toggle.vue'
import ConservationStatusDatatable from '@/components/common/species_communities/species_conservation_status_datatable.vue'
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
                values:null,
                accreditation_choices:[],
                accreditation_type:[],
                selected_accreditations:[],
                licence_period_choices:[],
                mooring: [''],
                global_settings:[],
                //mooring:[{'value':''}],
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
            deed_poll_url: function(){
                let vm=this;
                if(vm.global_settings){
                    for(var i=0; i<vm.global_settings.length; i++){
                        if(vm.global_settings[i].key=='deed_poll'){
                            return vm.global_settings[i].value;
                        }
                    }
                }
                return '';
            },
            credit_facility_link: function(){
                let vm=this;
                if(vm.global_settings){
                    for(var i=0; i<vm.global_settings.length; i++){
                        if(vm.global_settings[i].key=='credit_facility_link'){
                            return vm.global_settings[i].value;
                        }
                    }
                }
                return '';
            }
        },
        watch:{
            
            accreditation_type: function(){
                this.proposal.other_details.accreditation_type=this.accreditation_type.key;
            },
        },
        methods:{
            handleRadioChange: function(e){
                    if(e.target.value=="true"){
                        console.log(e.target.value);
                        $('#show_docket').removeClass('hidden')
                    }
                    else{
                        $('#show_docket').addClass('hidden')
                    }
                
            },
            handleSelectionChange: function(e){
                    if(e.target.value=="true"){
                        console.log(e.target.value);
                        $('#show_credit_link').removeClass('hidden')
                    }
                    else{
                        $('#show_credit_link').addClass('hidden')
                    }
                
            },
            showDockteNumber: function(){
                let vm=this;
                if(vm.proposal && vm.proposal.other_details.credit_docket_books){
                    var input = this.$refs.docket_books_yes;
                    var e = document.createEvent('HTMLEvents');
                    e.initEvent('change', true, true);
                    var disabledStatus = input.disabled;
                    try {
                        /* Firefox will not fire events for disabled widgets, so (temporarily) enabling them */
                        if(disabledStatus) {
                            input.disabled = false;
                        }
                        input.dispatchEvent(e);
                    } finally {
                        if(disabledStatus) {
                            input.disabled = true;
                        }
                    }
                }
            },
            showCreditFacilityLink: function(){
                let vm=this;
                if(vm.proposal && vm.proposal.other_details.credit_fees){
                    var input = this.$refs.credit_fees_yes;
                    var e = document.createEvent('HTMLEvents');
                    e.initEvent('change', true, true);
                    var disabledStatus = input.disabled;
                    try {
                        /* Firefox will not fire events for disabled widgets, so (temporarily) enabling them */
                        if(disabledStatus) {
                            input.disabled = false;
                        }
                        input.dispatchEvent(e);
                    } finally {
                        if(disabledStatus) {
                            input.disabled = true;
                        }
                    }
                }
            },
            addMooring: function(){
                let vm=this;
                //var new_mooring= helpers.copyObject(vm.mooring)
                var new_mooring= helpers.copyObject(vm.proposal.other_details.mooring)
                new_mooring.push('');
                vm.proposal.other_details.mooring=new_mooring;
                console.log(vm.proposal.other_details.mooring);
            },
            fetchAccreditationChoices: function(){
                let vm = this;
                vm.$http.get('/api/accreditation_choices.json').then((response) => {
                    vm.accreditation_choices = response.body;
                    if(vm.proposal.other_details.accreditation_type
                        ){
                        for(var i=0; i<vm.accreditation_choices.length; i++){
                            if(vm.accreditation_choices[i].key==vm.proposal.other_details.accreditation_type){
                                vm.accreditation_type=vm.accreditation_choices[i]
                            }
                        }
                    }
                    
                },(error) => {
                    console.log(error);
                } );
            },
            fetchLicencePeriodChoices: function(){
                let vm = this;
                vm.$http.get('/api/licence_period_choices.json').then((response) => {
                    vm.licence_period_choices = response.body;
                    
                },(error) => {
                    console.log(error);
                } );
            },
            fetchGlobalSettings: function(){
                let vm = this;
                vm.$http.get('/api/global_settings.json').then((response) => {
                    vm.global_settings = response.body;
                    
                },(error) => {
                    console.log(error);
                } );
            },
            checkProposalAccreditation: function(){
                let vm= this;
                if(vm.proposal && vm.proposal.other_details){
                    for(var i=0; i<vm.proposal.other_details.accreditations.length; i++){
                        vm.proposal.other_details.accreditations[i].is_deleted=false;
                        vm.selected_accreditations.push(vm.proposal.other_details.accreditations[i].accreditation_type);
                    }
                }
            },
            selectAccreditation: function(e, accreditation_type){
                let vm=this;
                if(e.target.checked){
                    var found=false;
                    for(var i=0;i<vm.proposal.other_details.accreditations.length; i++){
                        if(vm.proposal.other_details.accreditations[i].accreditation_type==accreditation_type.key){
                            found=true;
                            vm.proposal.other_details.accreditations[i].is_deleted=false;
                        }
                    }
                    if(found==false){
                    var data={
                        'accreditation_type': accreditation_type.key,
                        'accreditation_expiry':null,
                        'comments':'',
                        'proposal_other_details': vm.proposal.other_details.id,
                        'is_deleted': false,
                        'accreditation_type_value': accreditation_type.value
                    }
                    var acc=helpers.copyObject(vm.proposal.other_details.accreditations);
                    acc.push(data);
                    vm.proposal.other_details.accreditations=acc;
                    }
                }
                else{
                    for(var i=0;i<vm.proposal.other_details.accreditations.length; i++)
                    {

                        if(vm.proposal.other_details.accreditations[i].accreditation_type==accreditation_type.key)
                        {
                            if(vm.proposal.other_details.accreditations[i].id){
                                //console.log('yes')
                                var acc=helpers.copyObject(vm.proposal.other_details.accreditations);
                                acc[i].is_deleted=true;
                                vm.proposal.other_details.accreditations=acc;
                            }
                            else{
                                var acc=helpers.copyObject(vm.proposal.other_details.accreditations);
                                acc.splice(i,1);
                                vm.proposal.other_details.accreditations=acc;
                            }
                        }
                    }
                }
            },
            eventListeners:function (){
                let vm=this;

                var date= new Date()
                var today= new Date(date.getFullYear(), date.getMonth(), date.getDate());

                $(vm.$refs.accreditation_expiry).datetimepicker(vm.datepickerOptions);
                $(vm.$refs.accreditation_expiry).on('dp.change', function(e){
                    if ($(vm.$refs.accreditation_expiry).data('DateTimePicker').date()) {
                        

                        vm.proposal.other_details.accreditation_expiry =  e.date.format('DD/MM/YYYY');
                    }
                    else if ($(vm.$refs.accreditation_expiry).data('date') === "") {
                        vm.proposal.other_details.accreditation_expiry = "";
                    }
                 });
                //Nominated start date listener
                $(vm.$refs.nominated_start_date).datetimepicker(vm.datepickerOptions);
                //Set minimum date on datetimepicker so that nominated
                //start date cannot be selected prior to today
                $(vm.$refs.nominated_start_date).data("DateTimePicker").minDate(today);
                $(vm.$refs.nominated_start_date).on('dp.change', function(e){
                    if ($(vm.$refs.nominated_start_date).data('DateTimePicker').date()) {
                        

                        vm.proposal.other_details.nominated_start_date =  e.date.format('DD/MM/YYYY');
                    }
                    else if ($(vm.$refs.nominated_start_date).data('date') === "") {
                        vm.proposal.other_details.nominated_start_date = "";
                    }
                 });
                //Insurance expiry date listener
                $(vm.$refs.insurance_expiry).datetimepicker(vm.datepickerOptions);
                //Set minimum date on datetimepicker so that
                //insurance expiry date cannot be selected prior to today
                $(vm.$refs.insurance_expiry).data("DateTimePicker").minDate(today);
                $(vm.$refs.insurance_expiry).on('dp.change', function(e){
                    if ($(vm.$refs.insurance_expiry).data('DateTimePicker').date()) {                       

                        vm.proposal.other_details.insurance_expiry =  e.date.format('DD/MM/YYYY');
                    }
                    else if ($(vm.$refs.insurance_expiry).data('date') === "") {
                        vm.proposal.other_details.insurance_expiry = "";
                    }
                 });
                // Intialise select2
                $(vm.$refs.preferred_licence_period).select2({
                    "theme": "bootstrap",
                    allowClear: true,
                    placeholder:"Select preferred licence term"
                }).
                on("select2:select",function (e) {
                    var selected = $(e.currentTarget);
                    vm.proposal.other_details.preferred_licence_period = selected.val();
                    vm.proposal.other_details.preferred_licence_period_id = selected.val();
                }).
                on("select2:unselect",function (e) {
                    var selected = $(e.currentTarget);
                    vm.proposal.other_details.preferred_licence_period = selected.val();
                    vm.proposal.other_details.preferred_licence_period_id = selected.val();
                });
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

