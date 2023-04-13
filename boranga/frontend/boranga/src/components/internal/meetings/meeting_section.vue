<template lang="html">
    <div id="communityStatus">
        <FormSection :formCollapse="false" label="Meeting" Index="meeting" :isShowComment="isShowComment" :has_comment_value="has_comment_value" v-on:toggleComment="toggleComment($event)" :displayCommentSection="!is_external">
            <div v-if="!is_external">
                
            </div>
            <!--  -->

            
            
            <div class="row mb-3">
                <label for="" class="col-sm-4 control-label">Start Date/ Time:</label>
                <div class="col-sm-8">
                    <!-- <input :disabled="meeting_obj.readonly" type="datetime-local" class="form-control"  id="start_time" v-model="meeting_obj.start_date"> -->
                    <input type="datetime-local" class="form-control" name="start_date" 
                                        ref="start_date" v-model="meeting_obj.start_date" />
                </div>
            </div>
             <div class="row mb-3">
                <label for="" class="col-sm-4 control-label">End Date/ Time:</label>
                <div class="col-sm-8">
                    <input :disabled="meeting_obj.readonly" type="datetime-local" class="form-control"  id="end_date" v-model="meeting_obj.end_date">
                </div>
            </div>
            <div class="row mb-3">
                <label for="" class="col-sm-4 control-label">Title:</label>
                <div class="col-sm-8">
                    <input type="text" class="form-control" id="title" placeholder="" 
                    v-model="meeting_obj.title"/>
                </div>
            </div>
            <div class="row mb-3">
                <label for="" class="col-sm-4 control-label">Meeting status:</label>
                <div class="col-sm-8">
                    <select :disabled="isReadOnly" 
                        style="width:100%;" class="form-select input-sm"  
                        ref="meeting_status_select" 
                        v-model="meeting_obj.processing_status" >
                        <option v-for="c in status_list" :value="c.id" :key="c.id">
                            {{c.display_name}}
                        </option>
                    </select>
                </div>
            </div>
            
            
            
            <!-- TODO Do we need to show the effective dates and approval document to external user -->
            
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
require("select2/dist/css/select2.min.css");
require("select2-bootstrap-5-theme/dist/select2-bootstrap-5-theme.min.css")

export default {
        name: 'MeetingSection',
        props:{
            meeting_obj:{
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
                datepickerOptions:{
                    format: 'DD/MM/YYYY',
                    showClear:true,
                    useCurrent:false,
                    keepInvalid:true,
                    allowInputToggle:true,
                },
                isShowComment: false,
                //----list of values dictionary
                meeting_dict: {},
                status_list: [],
                conservation_list_values: [],
                conservation_category_list: [],
                conservation_criteria_list: [],
                filtered_prop_conservation_category_list: [],
                filtered_prop_conservation_criteria_list: [],
                filtered_conservation_category_list: [],
                filtered_conservation_criteria_list: [],
                referral_comments_boxes: [],
                // to display the species selected 
                community_display: '',
                //---Comment box attributes
                //deficiency_readonly : !this.is_external && !this.meeting_obj.can_user_edit && this.meeting_obj.assessor_mode.assessor_level == 'assessor' && this.meeting_obj.assessor_mode.has_assessor_mode && !this.meeting_obj.assessor_mode.status_without_assessor? false : true,
                //assessor_comment_readonly: !this.is_external && !this.meeting_obj.can_user_edit && this.meeting_obj.assessor_mode.assessor_level == 'assessor' && this.meeting_obj.assessor_mode.has_assessor_mode && !this.meeting_obj.assessor_mode.status_without_assessor? false : true,
            }
        },
        components: {
            FormSection,
        },
        computed: {
             deficiencyVisibility: function(){
                return this.meeting_obj.assessor_mode.assessor_box_view;
            },
            assessorCommentVisibility: function(){
                return this.meeting_obj.assessor_mode.assessor_box_view;
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
            isStatusApproved: function(){
                return this.meeting_obj.processing_status=="Approved" ? true : false;
            },
            isReadOnly: function(){
                let action = this.$route.query.action;
                if(action === "edit" && this.meeting_obj && this.meeting_obj.assessor_mode.has_assessor_mode){
                    return false;
                }
                else{
                    return this.meeting_obj.readonly;
                }
            },
        },
        watch:{
        },
        methods:{
            /*checkDate: function(){
                let vm=this;
                if(vm.$refs.last_data_curration_date.value){
                    vm.meeting_obj.last_data_curration_date = vm.$refs.last_data_curration_date.value;
                }
                else{
                    vm.meeting_obj.last_data_curration_date=null;
                }
            },*/
            getCommunityDisplay: function(){
                for(let choice of this.community_list){
                        if(choice.id === this.meeting_obj.community_id)
                        {
                          this.community_display = choice.name;
                        }
                    }
            },
            /*filterProposedConservationCategoryCriteria: function(event){
                this.$nextTick(() => {
                    if(event){
                        this.meeting_obj.proposed_conservation_category_id=null;
                        this.meeting_obj.proposed_conservation_criteria=[];
                    }
                    this.filtered_prop_conservation_category_list=[];
                    this.filtered_prop_conservation_category_list=[{
                          id:null,
                          code:"",
                          conservation_list_id:null,
                        }];
                    this.filtered_prop_conservation_criteria_list=[];
                    for(let choice of this.conservation_category_list){
                            if(choice.conservation_list_id === this.meeting_obj.proposed_conservation_list_id)
                            {
                              this.filtered_prop_conservation_category_list.push(choice);
                            }
                        }
                    for(let choice of this.conservation_criteria_list){
                            if(choice.conservation_list_id === this.meeting_obj.proposed_conservation_list_id)
                            {
                              this.filtered_prop_conservation_criteria_list.push(choice);
                            }
                        }
                });
            },*/
            filterConservationCategoryCriteria: function(event){
                this.$nextTick(() => {
                    if(event){
                        this.meeting_obj.conservation_category_id=null;
                        this.meeting_obj.conservation_criteria=[];
                    }
                    this.filtered_conservation_category_list=[];
                    this.filtered_conservation_category_list=[{
                          id:null,
                          code:"",
                          conservation_list_id:null,
                        }];
                    this.filtered_conservation_criteria_list=[];
                    for(let choice of this.conservation_category_list){
                            if(choice.conservation_list_id === this.meeting_obj.conservation_list_id)
                            {
                              this.filtered_conservation_category_list.push(choice);
                            }
                        }
                    for(let choice of this.conservation_criteria_list){
                            if(choice.conservation_list_id === this.meeting_obj.conservation_list_id)
                            {
                              this.filtered_conservation_criteria_list.push(choice);
                            }
                        }
                });
            },
            generateReferralCommentBoxes: function(){
                var box_visibility = this.meeting_obj.assessor_mode.assessor_box_view
                var assessor_mode = this.meeting_obj.assessor_mode.assessor_level
                if (!this.meeting_obj.can_user_edit){
                    var current_referral_present = false;
                    $.each(this.meeting_obj.latest_referrals,(i,v)=> {
                        var referral_name = `comment-field-Referral-${v.referral_obj.email}`; 
                        var referral_visibility =  assessor_mode == 'referral' && this.meeting_obj.assessor_mode.assessor_can_assess && this.referral.referral == v.referral_obj.id ? false : true ;
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
                    vm.meeting_obj.conservation_criteria = selected.val();
                }).
                on("select2:unselect",function (e) {
                    var selected = $(e.currentTarget);
                    vm.meeting_obj.conservation_criteria = selected.val();
                });

                // Initialise select2 for Proposed Conservation Criteria
                /*$(vm.$refs.prop_conservation_criteria_select).select2({
                    "theme": "bootstrap-5",
                    allowClear: true,
                    placeholder:"Select Criteria",
                    multiple: true,
                }).
                on("select2:select",function (e) {
                    var selected = $(e.currentTarget);
                    vm.meeting_obj.proposed_conservation_criteria = selected.val();
                }).
                on("select2:unselect",function (e) {
                    var selected = $(e.currentTarget);
                    vm.meeting_obj.proposed_conservation_criteria = selected.val();
                });*/
            },
            toggleComment:function(updatedShowComment) {
                //this.isShowComment = ! this.isShowComment;
                this.isShowComment = updatedShowComment;
            },
        },
        created: async function() {
            let vm=this;
            //------fetch list of values
            vm.$http.get(api_endpoints.meeting_dict).then((response) => {
                vm.meeting_dict = response.body;
                vm.status_list = vm.meeting_dict.status_list;
                
            },(error) => {
                console.log(error);
            })
        },
        mounted: function(){
            let vm = this;
            this.$nextTick(()=>{
                vm.eventListeners();
            });
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

