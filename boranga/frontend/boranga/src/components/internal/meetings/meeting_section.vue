<template lang="html">
    <div id="communityStatus">
        <FormSection :formCollapse="false" label="Meeting" Index="meeting">
            <div class="row mb-3">
                <label for="" class="col-sm-4 control-label">Title:</label>
                <div class="col-sm-8">
                    <input :disabled="isReadOnly" type="text" class="form-control" id="title" placeholder="" 
                    v-model="meeting_obj.title"/>
                </div>
            </div>
            <div class="row mb-3">
                <label for="" class="col-sm-4 control-label">Start Date/ Time:</label>
                <div class="col-sm-8">
                    <!-- <input :disabled="meeting_obj.readonly" type="datetime-local" class="form-control"  id="start_time" v-model="meeting_obj.start_date"> -->
                    <input :disabled="isReadOnly" type="datetime-local" class="form-control" name="start_date" 
                                        ref="start_date" v-model="meeting_obj.start_date" />
                </div>
            </div>
            <div class="row mb-3">
                <label for="" class="col-sm-4 control-label">End Date/ Time:</label>
                <div class="col-sm-8">
                    <input :disabled="isReadOnly" type="datetime-local" class="form-control"  id="end_date" v-model="meeting_obj.end_date">
                </div>
            </div>
            <div class="row mb-3">
                <label for="" class="col-sm-4 control-label">Meeting Type:</label>
                <div class="col-sm-8">
                    <select :disabled="isReadOnly" 
                        style="width:100%;" class="form-select"  
                        ref="meeting_status_select" 
                        v-model="meeting_obj.meeting_type" 
                        @change="toggleAttendees(meeting_obj.meeting_type)">
                        <option v-for="option in meeting_type_list" :value="option.id" :key="option.id">
                            {{option.display_name}}
                        </option>
                    </select>
                </div>
            </div>
            <div v-show="!isCommitteeMeeting" class="row mb-3">
                <label for="" class="col-sm-4 control-label">Attendees:</label>
                <div class="col-sm-8">
                    <input :disabled="isReadOnly" type="text" class="form-control" id="title" placeholder="" 
                    v-model="meeting_obj.attendees"/>
                </div>
            </div>
            <div v-show="isCommitteeMeeting">
                <div class="row mb-3">
                    <label for="" class="col-sm-4 control-label">Committee:</label>
                    <div class="col-sm-8">
                        <select :disabled="isReadOnly" 
                            style="width:100%;" class="form-select"  
                            v-model="meeting_obj.committee_id" @change="renderMembersTable()">
                            <option v-for="option in committee_list" :value="option.id" :key="option.id">
                                {{option.name}}
                            </option>
                        </select>
                    </div>
                </div>
                <div class="row mb-3">
                    <datatable ref="members_datatable" :id="panelBody" :dtOptions="members_options"
                    :dtHeaders="members_headers"/>
                </div>
            </div>
            <div class="row mb-3">
                <label for="" class="col-sm-4 control-label">Location:</label>
                <div class="col-sm-8">
                    <select :disabled="isReadOnly" 
                        style="width:100%;" class="form-select"  
                        v-model="meeting_obj.location_id" >
                        <option v-for="option in location_list" :value="option.id" :key="option.id">
                            {{option.name}}
                        </option>
                    </select>
                </div>
            </div>
            <div class="row mb-3">
                <label for="" class="col-sm-4 control-label">Meeting status:</label>
                <div class="col-sm-8">
                    <select :disabled="isReadOnly" 
                        style="width:100%;" class="form-select"  
                        ref="meeting_status_select" 
                        v-model="meeting_obj.processing_status" >
                        <option v-for="option in status_list" :value="option.id" :key="option.id">
                            {{option.display_name}}
                        </option>
                    </select>
                </div>
            </div>
        </FormSection>
    </div>
</template>

<script>
import Vue from 'vue' ;
import datatable from '@vue-utils/datatable.vue';
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
                isCommitteeMeeting:false,
                //----list of values dictionary
                meeting_dict: {},
                location_list: [],
                meeting_type_list: [],
                status_list:[],
                committee_list:[],
                committee_mem_arr:[],
                results: [],
                panelBody: "committee_members"+vm._uid,
                members_headers:['id','First Name', 'Last Name', 'Email', 'Action'],
                members_options:{
                    autowidth: true,
                    language:{
                        processing: "<i class='fa fa-4x fa-spinner'></i>"
                    },
                    responsive: true,
                    searching: true,
                     //  to show the "workflow Status","Action" columns always in the last position
                    columnDefs: [
                        { responsivePriority: 1, targets: 0 },
                        { responsivePriority: 2, targets: -1 },
                    ],
                    // ajax:{
                    //     "url": helpers.add_endpoint_json(api_endpoints.committee,vm.meeting_obj.committee_id+'/committee_members'),
                    //     "dataSrc": ''
                    // },
                    order: [],
                    dom: "<'d-flex align-items-center'<'me-auto'l>fB>" +
                         "<'row'<'col-sm-12'tr>>" +
                         "<'d-flex align-items-center'<'me-auto'i>p>",
                    buttons:[
                        {
                            extend: 'excel',
                            text: '<i class="fa-solid fa-download"></i> Excel',
                            className: 'btn btn-primary ml-2',
                            exportOptions: {
                                orthogonal: 'export' 
                            }
                        },
                        {
                            extend: 'csv',
                            text: '<i class="fa-solid fa-download"></i> CSV',
                            className: 'btn btn-primary',
                            exportOptions: {
                                orthogonal: 'export' 
                            }
                        },
                    ],
                    columns: [
                        {
                            data: "id",
                            orderable: true,
                            searchable: true,
                            visible: false,
                            mRender: function(data,type,full){
                                return full.id;
                            },

                        },
                        {
                            data: "first_name",
                            orderable: true,
                            searchable: true,
                            mRender: function(data,type,full){
                                return full.first_name;
                            },

                        },
                        {
                            data: "last_name",
                            orderable: true,
                            searchable: true,
                            mRender: function(data,type,full){
                                return full.last_name;
                            },

                        },
                        {
                            data: "email",
                            orderable: true,
                            searchable: true,
                            'render': function(value, type, full){
                                let result = helpers.dtPopover(value, 30, 'hover');
                                return type=='export' ? value : result;
                            },
                        },
                        {
                            data: "id",
                            mRender:function (data,type,full){
                                let links = '';
                                if(vm.meeting_obj.sel_committee_members_arr.includes(full.id)){
                                    return `<a href='#${full.id}' data-remove-member='${full.id}'>Remove</a><br/>`;
                                }
                                else{
                                    return `<a href='#${full.id}' data-add-member='${full.id}'>Add</a><br/>`;
                                }
                                //links +=  `<a href='#${full.id}' data-remove-member='${full.id}'>Remove</a><br/>`;
                                //return links;
                            }
                        },
                    ],
                    processing:true,
                    initComplete: function() {
                        helpers.enablePopovers();
                    }, 
                }
            }
        },
        components: {
            FormSection,
            datatable,
        },
        computed: {
            isStatusApproved: function(){
                return this.meeting_obj.processing_status=="scheduled" ? true : false;
            },
            isReadOnly: function(){
                let action = this.$route.query.action;
                // if(action === "edit" && this.meeting && this.meeting.user_edit_mode){
                    //     return false;
                    // }
                    // else{
                        //     return this.meeting.readonly;
                        // }
                //  TODO add the appropriate logic as above
                if(action === "view" && this.meeting_obj){
                    return true;
                }
                else{
                    return false;
                }
            },
        },
        watch:{
        },
        methods:{
            eventListeners:function (){
                let vm = this;
            },
            //  render only once onload if meeting_obj.selected_committee_members>0 i.e previous sumbitted members
            renderExistsSelectedMembersTable: function(){
                let vm = this;
                vm.$http.get(`/api/committee/${vm.meeting_obj.committee_id}/committee_members`).then(res => {
                    vm.results = res.body;
                    if(vm.meeting_obj.selected_committee_members.length>0){
                        vm.meeting_obj.sel_committee_members_arr=[];
                        vm.meeting_obj.sel_committee_members_arr=vm.meeting_obj.selected_committee_members;
                    }
                    vm.$refs.members_datatable.vmDataTable.clear()
                    vm.$refs.members_datatable.vmDataTable.rows.add(vm.results);
                    vm.$refs.members_datatable.vmDataTable.draw();
                },
                err => {
                console.log(err);
                });
            },
            // render on change of comittee and also on new meeting form
            //TODO this function can be centralised and the sel_committee_members_arr to be sent to the function
            renderMembersTable: function(add){
                let vm = this;
                let committee_id=vm.meeting_obj.committee_id;
                if(committee_id===null){
                    vm.meeting_obj.sel_committee_members_arr=[];
                    vm.$refs.members_datatable.vmDataTable.clear()
                    vm.$refs.members_datatable.vmDataTable.draw();
                }
                else{
                    vm.$http.get(`/api/committee/${vm.meeting_obj.committee_id}/committee_members`).then(res => {
                        vm.results = res.body;
                        //-- only get members onchange of committee and not when only one member added by add btn
                        if(add===undefined){
                            // empty the previous selection
                            vm.meeting_obj.sel_committee_members_arr=[];
                            //to store all members of committee in array for further use
                            for(var i=0; i<vm.results.length; i++){
                                vm.meeting_obj.sel_committee_members_arr.push(vm.results[i].id);
                            }
                        }
                        vm.$refs.members_datatable.vmDataTable.clear()
                        vm.$refs.members_datatable.vmDataTable.rows.add(vm.results);
                        vm.$refs.members_datatable.vmDataTable.draw();
                    },
                    err => {
                    console.log(err);
                    });
                }
            },
            toggleAttendees: function(id){
                let vm=this;
                if(id==='committee_meeting'){
                    vm.isCommitteeMeeting=true;
                }
                else{
                    vm.meeting_obj.committee_id=null;
                    vm.meeting_obj.sel_committee_members_arr=[];
                    vm.isCommitteeMeeting=false;
                }
            },
            eventListeners: function(){
                let vm = this;
                vm.$refs.members_datatable.vmDataTable.on('click', 'a[data-remove-member]', function(e) {
                    e.preventDefault();
                    let id = $(this).attr('data-remove-member');
                    let mem_arr=vm.meeting_obj.sel_committee_members_arr;
                    //---remove document id from array (for this arr.splice is used)
                    let index = mem_arr.indexOf(parseInt(id)); // need to parse the id to int as the array is integer array
                    vm.meeting_obj.sel_committee_members_arr.splice(index,1);
                    vm.$refs.members_datatable.vmDataTable.row( $(this).parents('tr') ).remove().draw();
                });
                vm.$refs.members_datatable.vmDataTable.on('click', 'a[data-add-member]', function(e) {
                    e.preventDefault();
                    let id = $(this).attr('data-add-member');
                    vm.meeting_obj.sel_committee_members_arr.push(parseInt(id));
                    //--to add only the requested memvbr to the sel_committee_members_arr
                    vm.renderMembersTable('add');
                });
            },
        },
        created: async function() {
            let vm=this;
            //------fetch list of values
            vm.$http.get(api_endpoints.meeting_dict).then((response) => {
                vm.meeting_dict = response.body;
                //--meeting room list
                vm.location_list = vm.meeting_dict.location_list;
                vm.location_list.splice(0,0,
                {
                    id: null,
                    name: null,
                });
                vm.committee_list = vm.meeting_dict.committee_list;
                vm.committee_list.splice(0,0,
                {
                    id: null,
                    name: null,
                });
                //--meeting type list
                vm.meeting_type_list = vm.meeting_dict.meeting_type_list;
                //--status choices list
                vm.status_list = vm.meeting_dict.status_list;
                vm.toggleAttendees(vm.meeting_obj.meeting_type)
                if(vm.meeting_obj.committee_id!=null){
                    vm.renderExistsSelectedMembersTable();
                }
                else{
                    vm.renderMembersTable();
                }
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

