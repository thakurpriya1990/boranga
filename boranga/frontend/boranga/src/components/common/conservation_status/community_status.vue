<template lang="html">
    <div id="communityStatus">
        <FormSection :formCollapse="false" label="Conservation Status" Index="conservation_status">
            <div class="row mb-3">
                <label for="" class="col-sm-4 control-label">Community Name:</label>
                <div class="col-sm-8">
                    <select :disabled="conservation_status_obj.readonly" class="form-select" 
                        v-model="conservation_status_obj.community_id" id="community_name" @change="getCommunityDisplay()">
                        <option v-for="option in community_list" :value="option.id" v-bind:key="option.id">
                            {{ option.name }}                            
                        </option>
                    </select>
                </div>
            </div>
            <div class="row mb-3">
                <label for="" class="col-sm-4 control-label"></label>
                <div class="col-sm-8">
                    <textarea disabled class="form-control" rows="3" id="community_display" v-model="community_display"/>
                </div>
            </div>
            <!-- <div class="row mb-3">
                <label for="" class="col-sm-4 control-label">Previous Name:</label>
                <div class="col-sm-8">
                    <input readonly type="text" class="form-control" id="previous_name" placeholder="" 
                    v-model="conservation_status_obj.previous_name"/>
                </div>
            </div> -->
            <div class="row mb-3">
                <label for="" class="col-sm-4 control-label">Proposed Conservation List:</label>
                <div class="col-sm-8">
                    <select :disabled="conservation_status_obj.readonly" class="form-select" 
                        v-model="conservation_status_obj.conservation_list_id" id="conservation_list" 
                        @change="filterConservationCategoryCriteria($event)">
                        <option v-for="option in conservation_list_values" :value="option.id" v-bind:key="option.id">
                            {{ option.code }}                            
                        </option>
                    </select>
                </div>
            </div>
            <div class="row mb-3">
                <label for="" class="col-sm-4 control-label">Proposed Conservation Category:</label>
                <div class="col-sm-8">
                    <select :disabled="conservation_status_obj.readonly" class="form-select" 
                        v-model="conservation_status_obj.conservation_category_id" 
                        id="conservation_category">
                        <option v-for="option in filtered_conservation_category_list" :value="option.id" v-bind:key="option.id">
                            {{ option.code }}                            
                        </option>
                    </select>
                </div>
            </div>
            <div class="row mb-3">
                <label for="" class="col-sm-4 control-label">Proposed Conservation Criteria:</label>
                <div class="col-sm-8">
                    <select :disabled="conservation_status_obj.readonly" 
                        style="width:100%;" class="form-select input-sm" multiple 
                        ref="conservation_criteria_select" 
                        v-model="conservation_status_obj.conservation_criteria" >
                        <option v-for="c in filtered_conservation_criteria_list" :value="c.id" :key="c.id">
                            {{c.code}}
                        </option>
                    </select>
                </div>
            </div>
            <div class="row mb-3">
                <label for="" class="col-sm-4 control-label">Comment:</label>
                <div class="col-sm-8">
                    <textarea :disabled="conservation_status_obj.readonly" class="form-control" rows="3" id="comment" placeholder=""
                    v-model="conservation_status_obj.comment"/>
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
require("select2/dist/css/select2.min.css");
require("select2-bootstrap-5-theme/dist/select2-bootstrap-5-theme.min.css")

export default {
        name: 'CommunityStatus',
        props:{
            conservation_status_obj:{
                type: Object,
                required:true
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
                //----list of values dictionary
                cs_community_profile_dict: {},
                community_list: [],
                conservation_list_values: [],
                conservation_category_list: [],
                conservation_criteria_list: [],
                filtered_prop_conservation_category_list: [],
                filtered_prop_conservation_criteria_list: [],
                filtered_conservation_category_list: [],
                filtered_conservation_criteria_list: [],
                // to display the species selected 
                community_display: '',
            }
        },
        components: {
            FormSection,
        },
        computed: {
        },
        watch:{
        },
        methods:{
            /*checkDate: function(){
                let vm=this;
                if(vm.$refs.last_data_curration_date.value){
                    vm.conservation_status_obj.last_data_curration_date = vm.$refs.last_data_curration_date.value;
                }
                else{
                    vm.conservation_status_obj.last_data_curration_date=null;
                }
            },*/
            getCommunityDisplay: function(){
                for(let choice of this.community_list){
                        if(choice.id === this.conservation_status_obj.community_id)
                        {
                          this.community_display = choice.name;
                        }
                    }
            },
            /*filterProposedConservationCategoryCriteria: function(event){
                this.$nextTick(() => {
                    if(event){
                        this.conservation_status_obj.proposed_conservation_category_id=null;
                        this.conservation_status_obj.proposed_conservation_criteria=[];
                    }
                    this.filtered_prop_conservation_category_list=[];
                    this.filtered_prop_conservation_category_list=[{
                          id:null,
                          code:"",
                          conservation_list_id:null,
                        }];
                    this.filtered_prop_conservation_criteria_list=[];
                    for(let choice of this.conservation_category_list){
                            if(choice.conservation_list_id === this.conservation_status_obj.proposed_conservation_list_id)
                            {
                              this.filtered_prop_conservation_category_list.push(choice);
                            }
                        }
                    for(let choice of this.conservation_criteria_list){
                            if(choice.conservation_list_id === this.conservation_status_obj.proposed_conservation_list_id)
                            {
                              this.filtered_prop_conservation_criteria_list.push(choice);
                            }
                        }
                });
            },*/
            filterConservationCategoryCriteria: function(event){
                this.$nextTick(() => {
                    if(event){
                        this.conservation_status_obj.conservation_category_id=null;
                        this.conservation_status_obj.conservation_criteria=[];
                    }
                    this.filtered_conservation_category_list=[];
                    this.filtered_conservation_category_list=[{
                          id:null,
                          code:"",
                          conservation_list_id:null,
                        }];
                    this.filtered_conservation_criteria_list=[];
                    for(let choice of this.conservation_category_list){
                            if(choice.conservation_list_id === this.conservation_status_obj.conservation_list_id)
                            {
                              this.filtered_conservation_category_list.push(choice);
                            }
                        }
                    for(let choice of this.conservation_criteria_list){
                            if(choice.conservation_list_id === this.conservation_status_obj.conservation_list_id)
                            {
                              this.filtered_conservation_criteria_list.push(choice);
                            }
                        }
                });
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
                    vm.conservation_status_obj.conservation_criteria = selected.val();
                }).
                on("select2:unselect",function (e) {
                    var selected = $(e.currentTarget);
                    vm.conservation_status_obj.conservation_criteria = selected.val();
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
                    vm.conservation_status_obj.proposed_conservation_criteria = selected.val();
                }).
                on("select2:unselect",function (e) {
                    var selected = $(e.currentTarget);
                    vm.conservation_status_obj.proposed_conservation_criteria = selected.val();
                });*/
            },
        },
        created: async function() {
            let vm=this;
            //------fetch list of values
            vm.$http.get(api_endpoints.cs_profile_dict+ '?group_type=' + vm.conservation_status_obj.group_type).then((response) => {
                vm.cs_profile_dict = response.body;
                vm.community_list = vm.cs_profile_dict.community_list;
                vm.community_list.splice(0,0,
                {
                    id: null,
                    name: null,
                });
                vm.conservation_list_values = vm.cs_profile_dict.conservation_list_values;
                vm.conservation_list_values.splice(0,0,
                {
                    id: null,
                    code: null,
                });
                vm.conservation_category_list = vm.cs_profile_dict.conservation_category_list;
                vm.conservation_criteria_list = vm.cs_profile_dict.conservation_criteria_list;
                this.getCommunityDisplay();
                this.filterConservationCategoryCriteria();
                //this.filterProposedConservationCategoryCriteria();
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

