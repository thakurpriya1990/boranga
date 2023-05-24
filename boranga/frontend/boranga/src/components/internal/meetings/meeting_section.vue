<template lang="html">
    <div id="communityStatus">
        <FormSection :formCollapse="false" label="Meeting" Index="meeting">
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
                        <option v-for="c in status_list" :value="c.value" :key="c.value">
                            {{c.name}}
                        </option>
                    </select>
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
        name: 'MeetingSection',
        props:{
            meeting_obj:{
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
                isShowComment: false,
                //----list of values dictionary
                meeting_dict: {},
                status_list:[
                {value: 'draft', name: 'Draft'},
                {value: 'scheduled', name: 'Scheduled'},
            ],
            }
        },
        components: {
            FormSection,
        },
        computed: {
            isStatusApproved: function(){
                return this.meeting_obj.processing_status=="scheduled" ? true : false;
            },
            isReadOnly: function(){
                // let action = this.$route.query.action;
                // if(action === "edit" && this.meeting_obj && this.meeting_obj.assessor_mode.has_assessor_mode){
                //     return false;
                // }
                // else{
                //     return this.meeting_obj.readonly;
                // }
                return false;
            },
        },
        watch:{
        },
        methods:{
            eventListeners:function (){
                let vm = this;
            },
        },
        created: async function() {
            let vm=this;
            // //------fetch list of values
            // vm.$http.get(api_endpoints.meeting_dict).then((response) => {
            //     vm.meeting_dict = response.body;
            //     vm.status_list = vm.meeting_dict.status_list;
                
            // },(error) => {
            //     console.log(error);
            // })
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

