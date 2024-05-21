<template lang="html">
    <div id="communityStatus">
        <FormSection :formCollapse="false" label="Conservation Status" Index="conservation_status" :isShowComment="isShowComment" :has_comment_value="has_comment_value" v-on:toggleComment="toggleComment($event)" :displayCommentSection="!is_external">
            <div v-if="!is_external">
                <div v-show="isShowComment">
                    <!-- Assessor Deficiencies and comment box -->
                    <div class="row mb-3" v-if="deficiencyVisibility">
                        <label for="" class="col-sm-4 control-label">Deficiencies:</label>
                        <div class="col-sm-8">
                            <textarea :disabled="deficiency_readonly" class="form-control" rows="3" id="assessor_deficiencies" placeholder=""
                            v-model="conservation_status_obj.deficiency_data"/>
                        </div>
                    </div>
                    <div class="row mb-3" v-if="assessorCommentVisibility">
                        <label for="" class="col-sm-4 control-label">Assessor:</label>
                        <div class="col-sm-8">
                            <textarea :disabled="assessor_comment_readonly" class="form-control" rows="3" id="assessor_comment" placeholder=""
                            v-model="conservation_status_obj.assessor_data"/>
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
                <label for="" class="col-sm-4 control-label">Community Name:</label>
                <div class="col-sm-8" :id="select_community_name">
                    <!-- <select :disabled="conservation_status_obj.readonly" class="form-select"
                        v-model="conservation_status_obj.community_id" id="community_name" @change="getCommunityDisplay()">
                        <option v-for="option in community_list" :value="option.id" v-bind:key="option.id">
                            {{ option.name }}
                        </option>
                    </select> -->
                    <select :disabled="conservation_status_obj.readonly"
                        :id="community_name_lookup"
                        :name="community_name_lookup"
                        :ref="community_name_lookup"
                        class="form-control" />
                </div>
            </div>
            <div class="row mb-3">
                <label for="" class="col-sm-4 control-label"></label>
                <div class="col-sm-8">
                    <textarea disabled class="form-control" rows="3" id="community_display" v-model="community_display"/>
                </div>
            </div>
            <!-- TODO: Add new conservation list / category fields in here -->
            <div class="row mb-3">
                <label for="" class="col-sm-4 control-label">{{ conservation_criteria_label }}:</label>
                <div class="col-sm-8">
                    <input :disabled="isReadOnly" type="text" class="form-control" id="conservation_criteria" placeholder=""
                        v-model="conservation_status_obj.conservation_criteria"/>
                </div>
            </div>
            <div class="row mb-3" v-show="canViewCurrentList">
                <label for="" class="col-sm-4 control-label">Current Conservation List:</label>
                <div class="col-sm-8">
                    <input readonly type="text" class="form-control" id="curr_cons_list" placeholder=""
                    v-model="conservation_status_obj.curr_conservation_list"/>
                </div>
            </div>
            <div class="row mb-3" v-show="canViewCurrentList">
                <label for="" class="col-sm-4 control-label">Current Conservation Category:</label>
                <div class="col-sm-8">
                    <input readonly type="text" class="form-control" id="curr_cons_category" placeholder=""
                    v-model="conservation_status_obj.curr_conservation_category"/>
                </div>
            </div>
            <div class="row mb-3" v-show="canViewCurrentList">
                <label for="" class="col-sm-4 control-label">Current Conservation Criteria:</label>
                <div class="col-sm-8">
                    <input readonly type="text" class="form-control" id="curr_cons_criteria" placeholder=""
                    v-model="conservation_status_obj.curr_conservation_criteria"/>
                </div>
            </div>
            <div class="row mb-3" v-show="conservation_status_obj.can_view_recommended">
                <label for="" class="col-sm-4 control-label">Recommended Conservation Criteria:</label>
                <div class="col-sm-8">
                    <input :disabled="!conservation_status_obj.can_edit_recommended" type="text" class="form-control" id="rec_conservation_criteria" placeholder=""
                        v-model="conservation_status_obj.recommended_conservation_criteria"/>
                </div>
            </div>

            <div class="row mb-3">
                <label for="" class="col-sm-4 control-label">Comment:</label>
                <div class="col-sm-8">
                    <textarea :disabled="isReadOnly" class="form-control" rows="3" id="comment" placeholder=""
                    v-model="conservation_status_obj.comment"/>
                </div>
            </div>
            <!-- TODO Do we need to show the effective dates and approval document to external user -->
            <div class="row mb-3" v-if="isStatusApproved && is_external==false">
                <label for="" class="col-sm-4 control-label">Effective From Date:</label>
                <div class="col-sm-8">
                    <input :disabled="conservation_status_obj.readonly" type="date" class="form-control" placeholder="DD/MM/YYYY" id="effective_from_date" v-model="conservation_status_obj.conservationstatusissuanceapprovaldetails.effective_from_date">
                </div>
            </div>
            <div class="row mb-3" v-if="isStatusApproved && is_external==false">
                <label for="" class="col-sm-4 control-label">Effective To Date:</label>
                <div class="col-sm-8">
                   <input :disabled="conservation_status_obj.readonly" type="date" class="form-control" placeholder="DD/MM/YYYY" id="effective_to_date" v-model="conservation_status_obj.conservationstatusissuanceapprovaldetails.effective_to_date">
                </div>
            </div>
            <div class="row mb-3" v-if="isStatusApproved && is_external==false">
                <label for="" class="col-sm-4 control-label">Approval document:</label>
                <div class="col-sm-8">
                    <p v-if="conservation_status_obj.conservation_status_approval_document">
                        <strong><a :href="conservation_status_obj.conservation_status_approval_document[1]" target="_blank">{{conservation_status_obj.conservation_status_approval_document[0]}}</a></strong>
                    </p>
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
        name: 'CommunityStatus',
        props:{
            conservation_status_obj:{
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
                community_name_lookup: 'community_name_lookup' + vm._uid,
                select_community_name: "select_community_name"+ vm._uid,
                isShowComment: false,
                //----list of values dictionary
                cs_community_profile_dict: {},
                community_list: [],
                referral_comments_boxes: [],
                // to display the species selected
                community_display: '',
                //---Comment box attributes
                deficiency_readonly : !this.is_external && !this.conservation_status_obj.can_user_edit && this.conservation_status_obj.assessor_mode.assessor_level == 'assessor' && this.conservation_status_obj.assessor_mode.has_assessor_mode && !this.conservation_status_obj.assessor_mode.status_without_assessor? false : true,
                assessor_comment_readonly: !this.is_external && !this.conservation_status_obj.can_user_edit && this.conservation_status_obj.assessor_mode.assessor_level == 'assessor' && this.conservation_status_obj.assessor_mode.has_assessor_mode && !this.conservation_status_obj.assessor_mode.status_without_assessor? false : true,
            }
        },
        components: {
            FormSection,
        },
        computed: {
             deficiencyVisibility: function(){
                return this.conservation_status_obj.assessor_mode.assessor_box_view;
            },
            assessorCommentVisibility: function(){
                return this.conservation_status_obj.assessor_mode.assessor_box_view;
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
                return this.conservation_status_obj.processing_status=="Approved" ? true : false;
            },
            isReadOnly: function(){
                let action = this.$route.query.action;
                if(action === "edit" && this.conservation_status_obj && this.conservation_status_obj.assessor_mode.has_assessor_mode){
                    return false;
                }
                else{
                    return this.conservation_status_obj.readonly;
                }
            },
            conservation_list_label: function(){
                if(this.conservation_status_obj.processing_status == "Approved" || this.conservation_status_obj.processing_status == "DeListed"){
                    return "Conservation List";
                }
                else{
                    if(this.conservation_status_obj.processing_status == "Draft"){
                        return "Propose Conservation List";
                    }
                    else{
                        return "Proposed Conservation List";
                    }
                }
            },
            conservation_category_label: function(){
                // return (this.conservation_status_obj.processing_status == "Approved" || this.conservation_status_obj.processing_status == "DeListed") ? "Conservation Category" : "Proposed Conservation Category";
                if(this.conservation_status_obj.processing_status == "Approved" || this.conservation_status_obj.processing_status == "DeListed"){
                    return "Conservation Category";
                }
                else{
                    if(this.conservation_status_obj.processing_status == "Draft"){
                        return "Propose Conservation Category";
                    }
                    else{
                        return "Proposed Conservation Category";
                    }
                }
            },
            conservation_criteria_label: function(){
                //return (this.conservation_status_obj.processing_status == "Approved" || this.conservation_status_obj.processing_status == "DeListed") ? "Conservation Criteria" : "Proposed Conservation Criteria";
                if(this.conservation_status_obj.processing_status == "Approved" || this.conservation_status_obj.processing_status == "DeListed"){
                    return "Conservation Criteria";
                }
                else{
                    if(this.conservation_status_obj.processing_status == "Draft"){
                        return "Propose Conservation Criteria";
                    }
                    else{
                        return "Proposed Conservation Criteria";
                    }
                }
            },
            canViewCurrentList: function (){
                return (this.conservation_status_obj.processing_status == "Approved" || this.conservation_status_obj.processing_status == "DeListed") ? false:true;
            }
        },
        watch:{
        },
        methods:{
            initialiseCommunityNameLookup: function(){
                let vm = this;
                $(vm.$refs[vm.community_name_lookup]).select2({
                    minimumInputLength: 2,
                    dropdownParent: $("#"+vm.select_community_name),
                    "theme": "bootstrap-5",
                    allowClear: true,
                    placeholder:"Select Community Name",
                    ajax: {
                        url: api_endpoints.community_name_lookup,
                        dataType: 'json',
                        data: function(params) {
                            var query = {
                                term: params.term,
                                type: 'public',
                                cs_community: true,
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
                    vm.conservation_status_obj.community_id = data
                    vm.community_display = e.params.data.text;
                }).
                on("select2:unselect",function (e) {
                    var selected = $(e.currentTarget);
                    vm.conservation_status_obj.community_id = null
                    vm.community_display = '';
                }).
                on("select2:open",function (e) {
                    const searchField = $('[aria-controls="select2-'+vm.community_name_lookup+'-results"]')
                    // move focus to select2 field
                    searchField[0].focus();
                });
            },
            getCommunityDisplay: function(){
                for(let choice of this.community_list){
                        if(choice.id === this.conservation_status_obj.community_id)
                        {
                            var newOption = new Option(choice.name, choice.id, false, true);
                            $('#'+ this.community_name_lookup).append(newOption);
                            this.community_display = choice.name;
                        }
                    }
            },
            generateReferralCommentBoxes: function(){
                var box_visibility = this.conservation_status_obj.assessor_mode.assessor_box_view
                var assessor_mode = this.conservation_status_obj.assessor_mode.assessor_level
                if (!this.conservation_status_obj.can_user_edit){
                    var current_referral_present = false;
                    $.each(this.conservation_status_obj.latest_referrals,(i,v)=> {
                        var referral_name = `comment-field-Referral-${v.referral_obj.email}`;
                        var referral_visibility =  assessor_mode == 'referral' && this.conservation_status_obj.assessor_mode.assessor_can_assess && this.referral.referral == v.referral_obj.id ? false : true ;
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
                // $(vm.$refs.conservation_criteria_select).select2({
                //     "theme": "bootstrap-5",
                //     allowClear: true,
                //     placeholder:"Select Criteria",
                //     multiple: true,
                // }).
                // on("select2:select",function (e) {
                //     var selected = $(e.currentTarget);
                //     vm.selected_criteria = selected.val();
                //     vm.conservation_status_obj.conservation_criteria = selected.val();
                // }).
                // on("select2:unselect",function (e) {
                //     var selected = $(e.currentTarget);
                //     vm.conservation_status_obj.conservation_criteria = selected.val();
                // });

                // Initialise select2 for recommended Conservation Criteria
                // $(vm.$refs.recom_conservation_criteria_select).select2({
                //     "theme": "bootstrap-5",
                //     allowClear: true,
                //     placeholder:"Select Criteria",
                //     multiple: true,
                // }).
                // on("select2:select",function (e) {
                //     var selected = $(e.currentTarget);
                //     vm.conservation_status_obj.recommended_conservation_criteria = selected.val();
                // }).
                // on("select2:unselect",function (e) {
                //     var selected = $(e.currentTarget);
                //     vm.conservation_status_obj.recommended_conservation_criteria = selected.val();
                // });
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
            let dict_url= action == "view"? api_endpoints.cs_profile_dict+ '?group_type=' + vm.conservation_status_obj.group_type+ '&action=' + action :
                                            api_endpoints.cs_profile_dict+ '?group_type=' + vm.conservation_status_obj.group_type
            vm.$http.get(dict_url).then((response) => {
                vm.cs_profile_dict = response.body;
                vm.community_list = vm.cs_profile_dict.community_list;
                this.getCommunityDisplay();
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
                vm.initialiseCommunityNameLookup();
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
        padding: 0.375rem 2.25rem 0.375rem 0.75rem;
    }
</style>
