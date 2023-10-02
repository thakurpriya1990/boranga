<template lang="html">
    <div id="ocrLocation">
        <FormSection :formCollapse="false" label="Location" Index="occurrence_report" :isShowComment="isShowComment" :has_comment_value="has_comment_value" v-on:toggleComment="toggleComment($event)" :displayCommentSection="!is_external">
            <div v-if="!is_external">
                <div v-show="isShowComment">
                    <!-- Assessor Deficiencies and comment box -->
                    <div class="row mb-3" v-if="deficiencyVisibility">
                        <label for="" class="col-sm-4 control-label">Deficiencies:</label>
                        <div class="col-sm-8">
                            <textarea :disabled="deficiency_readonly" class="form-control" rows="3" id="assessor_deficiencies" placeholder=""
                            v-model="occurrence_report_obj.deficiency_data"/>
                        </div>
                    </div>
                    <div class="row mb-3" v-if="assessorCommentVisibility">
                        <label for="" class="col-sm-4 control-label">Assessor:</label>
                        <div class="col-sm-8">
                            <textarea :disabled="assessor_comment_readonly" class="form-control" rows="3" id="assessor_comment" placeholder=""
                            v-model="occurrence_report_obj.assessor_data"/>
                        </div>
                    </div>
                    <!-- --- -->

                    <!-- Assessor Deficiencies and comment box -->
                    <div v-if="referral_comments_boxes.length >0">
                        <div v-for="ref in referral_comments_boxes">
                            <div class="row mb-3" v-if="ref.box_view">
                                <label for="" class="col-sm-4 control-label">{{ref.label}}:</label>
                                <div class="col-sm-8">
                                    <textarea v-if='!ref.readonly'
                                        :disabled="ref.readonly" 
                                        :name="ref.name" 
                                        class="form-control" 
                                        rows="3" 
                                        placeholder="" 
                                        v-model="referral.referral_comment"
                                        />
                                    <textarea v-else
                                        :disabled="ref.readonly" 
                                        :name="ref.name" 
                                        :value="ref.value" 
                                        class="form-control" 
                                        rows="" 
                                        placeholder="" 
                                        />
                                </div>
                            </div> 
                        </div>
                    </div>
                </div>
            </div>
            <!--  -->

            <div class="row mb-3">
                <label for="" class="col-sm-3 control-label">Scientific Name:</label>
                <div class="col-sm-9" :id="select_scientific_name">
                    <select :disabled="isReadOnly"
                        :id="scientific_name_lookup"  
                        :name="scientific_name_lookup"  
                        :ref="scientific_name_lookup" 
                        class="form-control" />
                </div>
            </div>
            <div class="row mb-3">
                <label for="" class="col-sm-3 control-label"></label>
                <div class="col-sm-9">
                    <textarea disabled class="form-control" rows="2" id="species_display" v-model="species_display"/>
                </div>
            </div>
            <div class="row mb-3">
                <label for="" class="col-sm-3 control-label">Previous Name:</label>
                <div class="col-sm-9">
                    <input readonly type="text" class="form-control" id="previous_name" placeholder="" 
                    v-model="taxon_previous_name"/>
                </div>
            </div>
            <div class="row mb-3">
                <label for="" class="col-sm-3 control-label">Observation Date:</label>
                <div class="col-sm-9">
                    <input :disabled="isReadOnly" type="datetime-local" class="form-control" name="start_date" v-model="occurrence_report_obj.location.observation_date"/>
                </div>
            </div>
            <!-- ------------Observer Detail section -->
            
            <ObserverDatatable ref="observer_datatable" :occurrence_report_obj="occurrence_report_obj" :is_external="is_external" :isReadOnly="isReadOnly"></ObserverDatatable>

            <!-- -------------------------------- -->
            <div class="row mb-3">
                <label for="" class="col-sm-3 control-label">Location Description:</label>
                <div class="col-sm-9">
                    <textarea :disabled="isReadOnly" class="form-control" rows="2" id="loc_description" placeholder=""
                    v-model="occurrence_report_obj.location.location_description"/>
                </div>
            </div>
            <div class="row mb-3">
                <label for="" class="col-sm-3 control-label">Boundary Description:</label>
                <div class="col-sm-9">
                    <textarea :disabled="isReadOnly" class="form-control" rows="2" id="boundary_descr" placeholder=""
                    v-model="occurrence_report_obj.location.boundary_description"/>
                </div>
            </div>
            <div class="row mb-3">
                <label class="col-sm-3 control-label">New Occurrence</label>
                <div class="col-sm-1">
                    <input :disabled="isReadOnly" id="newOccurrenceYes" type="radio" v-model="occurrence_report_obj.location.new_occurrence" value="true">&nbsp;
                    <label for="newOccurrenceYes">Yes</label>
                </div>
                <div class="col-sm-1">
                    <input :disabled="isReadOnly" id="newOccurrenceNo" type="radio" v-model="occurrence_report_obj.location.new_occurrence" value="false">&nbsp;
                    <label for="newOccurrenceNo">No</label>
                </div>
            </div>
            <div class="row mb-3">
                <label for="" class="col-sm-3 control-label">Boundary(m) :</label>
                <div class="col-sm-6">
                    <input :disabled="isReadOnly" type="number" class="form-control ocr_number" id="boundary" placeholder="" min="0"
                    v-model="occurrence_report_obj.location.boundary"/>
                </div>
            </div>
            <div class="row mb-3">
                <label class="col-sm-3 control-label">Mapped Boundary</label>
                <div class="col-sm-1">
                    <input :disabled="isReadOnly" id="mapBoundaryYes" type="radio" v-model="occurrence_report_obj.location.mapped_boundary" value="true">&nbsp;
                    <label for="mapBoundaryYes">Yes</label>
                </div>
                <div class="col-sm-1">
                    <input :disabled="isReadOnly" id="mapBoundaryNo" type="radio" v-model="occurrence_report_obj.location.mapped_boundary" value="false">&nbsp;
                    <label for="mapBoundaryNo">No</label>
                </div>
            </div>
            <div class="row mb-3">
                <label for="" class="col-sm-3 control-label">Buffer Radius(m) :</label>
                <div class="col-sm-6">
                    <input :disabled="isReadOnly" type="number" class="form-control ocr_number" id="buffer_radius" placeholder="" min="0"
                    v-model="occurrence_report_obj.location.buffer_radius"/>
                </div>
            </div>
            <div class="row mb-3">
                <label for="" class="col-sm-3 control-label">Datum:</label>
                <div class="col-sm-9">
                    <select :disabled="isReadOnly" class="form-select" v-model="occurrence_report_obj.location.datum_id">
                        <option v-for="option in datum_list" :value="option.id" v-bind:key="option.id">
                            {{ option.name }}                            
                        </option>
                    </select>
                </div>
            </div>
            <div class="row mb-3">
                <label for="" class="col-sm-3 control-label">Coordination Source:</label>
                <div class="col-sm-9">
                    <select :disabled="isReadOnly" class="form-select" v-model="occurrence_report_obj.location.coordination_source_id">
                        <option v-for="option in coordination_source_list" :value="option.id" v-bind:key="option.id">
                            {{ option.name }}                            
                        </option>
                    </select>
                </div>
            </div>
            <div class="row mb-3">
                <label for="" class="col-sm-3 control-label">Location Accuracy/Certainty:</label>
                <div class="col-sm-9">
                    <select :disabled="isReadOnly" class="form-select" v-model="occurrence_report_obj.location.location_accuracy_id">
                        <option v-for="option in location_accuracy_list" :value="option.id" v-bind:key="option.id">
                            {{ option.name }}                            
                        </option>
                    </select>
                </div>
            </div>

            <div class="row mb-3">
                <div class="col-sm-12">
                    <!-- <button v-if="!updatingLocationDetails" class="pull-right btn btn-primary" @click.prevent="updateDetails()" :disabled="!can_update()">Update</button> -->
                    <button v-if="!updatingLocationDetails" class="btn btn-primary btn-sm float-end" @click.prevent="updateLocationDetails()">Update</button>
                    <button v-else disabled class="float-end btn btn-primary"><i class="fa fa-spin fa-spinner"></i>&nbsp;Updating</button>
                </div>
            </div>
        </FormSection>
    </div>
</template>

<script>
import Vue from 'vue' ;
// import datatable from '@vue-utils/datatable.vue';
import FormSection from '@/components/forms/section_toggle.vue';
import ObserverDatatable from './observer_datatable.vue'
import {
  api_endpoints,
  helpers
}
from '@/utils/hooks'
// require("select2/dist/css/select2.min.css");
// require("select2-bootstrap-5-theme/dist/select2-bootstrap-5-theme.min.css")

export default {
        name: 'OCRLocation',
        props:{
            occurrence_report_obj:{
                type: Object,
                required:true
            },
            referral:{
                type: Object,
                required:false
            },
            is_external:{
              type: Boolean,
              default: false
            },
            canEditStatus:{
              type: Boolean,
              default: true
            },
        },
        data:function () {
            let vm = this;
            return{
                scientific_name_lookup: 'scientific_name_lookup' + vm.occurrence_report_obj.id,
                select_scientific_name: "select_scientific_name"+ vm.occurrence_report_obj.id,
                isShowComment: false,
                //---to show fields related to Fauna
                isFauna: vm.occurrence_report_obj.group_type==="fauna"?true:false,
                //----list of values dictionary
                cs_profile_dict: {},
                species_list: [],
                referral_comments_boxes: [],
                // to display the species selected 
                species_display: '',
                taxon_previous_name:'',
                //---Comment box attributes

                deficiency_readonly : !this.is_external && !this.occurrence_report_obj.can_user_edit && this.occurrence_report_obj.assessor_mode.assessor_level == 'assessor' && this.occurrence_report_obj.assessor_mode.has_assessor_mode && !this.occurrence_report_obj.assessor_mode.status_without_assessor? false : true,
                assessor_comment_readonly: !this.is_external && !this.occurrence_report_obj.can_user_edit && this.occurrence_report_obj.assessor_mode.assessor_level == 'assessor' && this.occurrence_report_obj.assessor_mode.has_assessor_mode && !this.occurrence_report_obj.assessor_mode.status_without_assessor? false : true,

                updatingLocationDetails: false,
                listOfValuesDict: {},
                datum_list: [],
                coordination_source_list: [],
                location_accuracy_list:[],
            }
        },
        components: {
            FormSection,
            ObserverDatatable,
        },
        computed: {
            deficiencyVisibility: function(){
                return this.occurrence_report_obj.assessor_mode.assessor_box_view;
            },
            assessorCommentVisibility: function(){
                return this.occurrence_report_obj.assessor_mode.assessor_box_view;
            },
            has_comment_value:function () {
                let has_value=false;
                // TODO need to add assessor comment value as well
                for(var i=0; i<this.referral_comments_boxes.length; i++){
                    if(this.referral_comments_boxes[i].hasOwnProperty('value')){
                        if(this.referral_comments_boxes[i].value!=null && this.referral_comments_boxes[i].value!=undefined && this.referral_comments_boxes[i].value!= '' ){
                            has_value=true;
                        }
                    } 
                }
                return has_value;
            },
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
            initialiseScientificNameLookup: function(){
                let vm = this;
                $(vm.$refs[vm.scientific_name_lookup]).select2({
                    minimumInputLength: 2,
                    dropdownParent: $("#"+vm.select_scientific_name),
                    "theme": "bootstrap-5",
                    allowClear: true,
                    placeholder:"Select Scientific Name",
                    ajax: {
                        url: api_endpoints.scientific_name_lookup,
                        dataType: 'json',
                        data: function(params) {
                            var query = {
                                term: params.term,
                                type: 'public',
                                group_type_id: vm.occurrence_report_obj.group_type_id,
                                cs_species: true,
                                cs_species_status: vm.occurrence_report_obj.processing_status,
                            }
                            return query;
                        },
                        // results: function (data, page) { // parse the results into the format expected by Select2.
                        //     // since we are using custom formatting functions we do not need to alter remote JSON data
                        //     return {results: data};
                        // },
                    },
                }).
                on("select2:select", function (e) {
                    var selected = $(e.currentTarget);
                    let data = e.params.data.id;
                    vm.occurrence_report_obj.species_id = data
                    vm.species_display = e.params.data.text;
                    vm.taxon_previous_name = e.params.data.taxon_previous_name;
                }).
                on("select2:unselect",function (e) {
                    var selected = $(e.currentTarget);
                    vm.occurrence_report_obj.species_id = ''
                    vm.species_display = '';
                    vm.taxon_previous_name = '';
                }).
                on("select2:open",function (e) {
                    const searchField = $('[aria-controls="select2-'+vm.scientific_name_lookup+'-results"]')
                    // move focus to select2 field
                    searchField[0].focus();
                });
            },
            getSpeciesDisplay: function(){
                let vm = this;
                for(let choice of vm.species_list){
                        if(choice.id === vm.occurrence_report_obj.species_id)
                        {
                            var newOption = new Option(choice.name, choice.id, false, true);
                            $('#'+ vm.scientific_name_lookup).append(newOption);
                            vm.species_display = choice.name;
                            vm.taxon_previous_name = choice.taxon_previous_name;
                        }
                    }
            },
            generateReferralCommentBoxes: function(){
                var box_visibility = this.occurrence_report_obj.assessor_mode.assessor_box_view
                var assessor_mode = this.occurrence_report_obj.assessor_mode.assessor_level
                if (!this.occurrence_report_obj.can_user_edit){
                    var current_referral_present = false;
                    $.each(this.occurrence_report_obj.latest_referrals,(i,v)=> {
                        var referral_name = `comment-field-Referral-${v.referral_obj.email}`; 
                        var referral_visibility =  assessor_mode == 'referral' && this.occurrence_report_obj.assessor_mode.assessor_can_assess && this.referral.referral == v.referral_obj.id ? false : true ;
                        var referral_label = `${v.referral_obj.fullname}`;
                        var referral_comment_val = `${v.referral_comment}`;
                        this.referral_comments_boxes.push(
                            {
                                "box_view": box_visibility,
                                "name": referral_name,
                                "label": referral_label,
                                "readonly": referral_visibility,
                                "value": referral_comment_val,
                            }
                        )
                    });
                }
            },
            eventListeners:function (){
                let vm = this;
            },
            toggleComment:function(updatedShowComment) {
                //this.isShowComment = ! this.isShowComment;
                this.isShowComment = updatedShowComment;
            },
            updateLocationDetails: function() {
                let vm = this;
                vm.updatingLocationDetails = true;
                vm.$http.post(helpers.add_endpoint_json(api_endpoints.occurrence_report,(vm.occurrence_report_obj.id+'/update_location_details')),JSON.stringify(vm.occurrence_report_obj.location),{
                    emulateJSON:true
                }).then((response) => {
                    vm.updatingLocationDetails = false;
                    vm.occurrence_report_obj.location = response.body;
                    swal.fire({
                        title: 'Saved',
                        text: 'Location details have been saved',
                        icon: 'success',
                        confirmButtonColor:'#226fbb',

                    });
                }, (error) => {
                    var text= helpers.apiVueResourceError(error);
                    swal.fire({
                        title: 'Error', 
                        text: 'Location details cannot be saved because of the following error: '+text,
                        icon: 'error',
                        confirmButtonColor:'#226fbb',
                    });
                    vm.updatingLocationDetails = false;
                });
            },
        },
        created: async function() {
            let vm=this;
            //------fetch list of values according to action
            let action = this.$route.query.action;
            let dict_url= action == "view"? api_endpoints.cs_profile_dict+ '?group_type=' + vm.occurrence_report_obj.group_type+ '&action=' + action : 
                                            api_endpoints.cs_profile_dict+ '?group_type=' + vm.occurrence_report_obj.group_type
            vm.$http.get(dict_url).then((response) => {
                vm.cs_profile_dict = response.body;
                vm.species_list = vm.cs_profile_dict.species_list;
                this.getSpeciesDisplay();
                if(!vm.is_external){
                    this.generateReferralCommentBoxes();
                }
            },(error) => {
                console.log(error);
            })
            //------fetch list of values
            const res = await Vue.http.get('/api/occurrence_report/location_list_of_values.json');
            vm.listOfValuesDict = res.body;
            vm.datum_list = vm.listOfValuesDict.datum_list;
            vm.datum_list.splice(0,0,
            {
                id: null,
                name:null,
            });
            vm.coordination_source_list = vm.listOfValuesDict.coordination_source_list;
            vm.coordination_source_list.splice(0,0,
            {
                id: null,
                name:null,
            });
            vm.location_accuracy_list = vm.listOfValuesDict.location_accuracy_list;
            vm.location_accuracy_list.splice(0,0,
            {
                id: null,
                name:null,
            });
        },
        mounted: function(){
            let vm = this;
            this.$nextTick(()=>{
                vm.eventListeners();
                vm.initialiseScientificNameLookup();
            });
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
    input[type=number] {
        width: 50%;
    }
    input.ocr_number{
        width: 20%;
    }
</style>

