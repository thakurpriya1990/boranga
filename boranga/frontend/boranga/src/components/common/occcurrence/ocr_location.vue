<template lang="html">
    <div id="ocrLocation">
        <FormSection :formCollapse="false" label="Location" Index="occurrence_report" :isShowComment="isShowComment" :has_comment_value="has_comment_value" v-on:toggleComment="toggleComment($event)" :displayCommentSection="!is_external">
             <!-- <template v-if="!isShowComment">
                <a v-if="has_comment_value" href="" @click.prevent="toggleComment"><i style="color:red" class="far fa-comment">&nbsp;</i></a>
                <a v-else href="" @click.prevent="toggleComment"><i class="far fa-comment">&nbsp;</i></a>
            </template>
            <a href="" v-else @click.prevent="toggleComment"><i class="fa fa-ban">&nbsp;</i></a> -->
            
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
                <label for="" class="col-sm-4 control-label">Scientific Name:</label>
                <div class="col-sm-8" :id="select_scientific_name">
                    <select :disabled="occurrence_report_obj.readonly"
                        :id="scientific_name_lookup"  
                        :name="scientific_name_lookup"  
                        :ref="scientific_name_lookup" 
                        class="form-control" />
                </div>
            </div>
            <div class="row mb-3">
                <label for="" class="col-sm-4 control-label"></label>
                <div class="col-sm-8">
                    <textarea disabled class="form-control" rows="3" id="species_display" v-model="species_display"/>
                </div>
            </div>
            <div class="row mb-3">
                <label for="" class="col-sm-4 control-label">Previous Name:</label>
                <div class="col-sm-8">
                    <input readonly type="text" class="form-control" id="previous_name" placeholder="" 
                    v-model="taxon_previous_name"/>
                </div>
            </div>
            <!-- <div class="row mb-3">
                <label for="" class="col-sm-4 control-label">Comment:</label>
                <div class="col-sm-8">
                    <textarea :disabled="isReadOnly" class="form-control" rows="3" id="comment" placeholder=""
                    v-model="occurrence_report_obj.comment"/>
                </div>
            </div> -->
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
        name: 'SpeciesStatus',
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
                
            }
        },
        components: {
            FormSection,
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
            filterConservationCategoryCriteria: function(event){
                this.$nextTick(() => {
                    if(event){
                        this.occurrence_report_obj.conservation_category_id=null;
                        this.occurrence_report_obj.conservation_criteria=[];
                    }
                    this.filtered_conservation_category_list=[];
                    this.filtered_conservation_category_list=[{
                          id:null,
                          code:"",
                          conservation_list_id:null,
                        }];
                    this.filtered_conservation_criteria_list=[];
                    for(let choice of this.conservation_category_list){
                            if(choice.conservation_list_id === this.occurrence_report_obj.conservation_list_id)
                            {
                              this.filtered_conservation_category_list.push(choice);
                            }
                        }
                    for(let choice of this.conservation_criteria_list){
                            if(choice.conservation_list_id === this.occurrence_report_obj.conservation_list_id)
                            {
                              this.filtered_conservation_criteria_list.push(choice);
                            }
                        }
                });
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
                // Initialise select2 for proposed Conservation Criteria
                $(vm.$refs.conservation_criteria_select).select2({
                    "theme": "bootstrap-5",
                    allowClear: true,
                    placeholder:"Select Criteria",
                    multiple: true,
                }).
                on("select2:select",function (e) {
                    var selected = $(e.currentTarget);
                    vm.selected_criteria = selected.val();
                    vm.occurrence_report_obj.conservation_criteria = selected.val();
                }).
                on("select2:unselect",function (e) {
                    var selected = $(e.currentTarget);
                    vm.occurrence_report_obj.conservation_criteria = selected.val();
                });
            },
            toggleComment:function(updatedShowComment) {
                //this.isShowComment = ! this.isShowComment;
                this.isShowComment = updatedShowComment;
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
</style>

