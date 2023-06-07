<template id="meetings_datatable">
    <div>
        <CollapsibleFilters component_title="Filters" ref="collapsible_filters" @created="collapsible_component_mounted" class="mb-2">
            <div class="row">
                <div class="col-md-3">
                    <div class="form-group">
                        <label for="">Start Date:</label>
                        <input type="datetime-local" class="form-control" placeholder="DD/MM/YYYY" id="start_date" v-model="filterMeetingStartDate">
                    </div>
                </div>
                <div class="col-md-3">
                    <div class="form-group">
                        <label for="">End Date:</label>
                        <input type="datetime-local" class="form-control" placeholder="DD/MM/YYYY" id="end_date" v-model="filterMeetingEndDate">
                    </div>
                </div>
                <div class="col-md-3">
                    <div class="form-group">
                        <label for="">Status:</label>
                        <select class="form-select" v-model="filterMeetingStatus">
                            <option value="all">All</option>
                            <option v-for="status in meeting_status" :value="status.value">{{ status.name }}</option>
                        </select>
                    </div>
                </div>
            </div>
        </CollapsibleFilters>
        <div class="col-md-12">
            <div class="text-end">
                <button type="button" class="btn btn-primary mb-2 " @click.prevent="createMeeting"><i class="fa-solid fa-circle-plus"></i> Add Meeting</button>
            </div>
        </div>
        <div class="row">
            <div class="col-lg-12">
                <datatable 
                ref="meetings_datatable" 
                :id="datatable_id" 
                :dtOptions="datatable_options" 
                :dtHeaders="datatable_headers"/>
            </div>

        </div>
    </div>
</template>
<script>
import {
    api_endpoints,
    helpers
}
from '@/utils/hooks'
import "babel-polyfill"
import datatable from '@/utils/vue/datatable.vue'
import CollapsibleFilters from '@/components/forms/collapsible_component.vue'
import moment from 'moment'
import Vue from 'vue'

export default {
    name: 'MeetingsDatatable',
    props: {
        url:{
            type: String,
            required: true
        },
        filterMeetingStartDate_cache: {
            type: String,
            required: false,
            default: 'filterMeetingStartDate',
        },
        filterMeetingEndDate_cache: {
            type: String,
            required: false,
            default: 'filterMeetingEndDate',
        },
        filterMeetingStatus_cache: {
            type: String,
            required: false,
            default: 'filterMeetingStatus',
        },
    },
    data: function() {
        let vm = this;
        return {

            datatable_id: 'meetings-datatable-'+vm._uid,
            
            filterMeetingStartDate: sessionStorage.getItem(this.filterMeetingStartDate_cache) ?sessionStorage.getItem(this.filterMeetingStartDate_cache) : '',

            filterMeetingEndDate: sessionStorage.getItem(this.filterMeetingEndDate_cache) ?sessionStorage.getItem(this.filterMeetingEndDate_cache) : '',

            filterMeetingStatus: sessionStorage.getItem(this.filterMeetingStatus_cache) ?sessionStorage.getItem(this.filterMeetingStatus_cache) : 'all',

            internal_status:[
                {value: 'draft', name: 'Draft'},
                {value: 'scheduled', name: 'Scheduled'},
            ],
            
            meeting_status: [],
            
        }
    },
    components:{
        datatable,
        CollapsibleFilters,
    },
    watch:{
        filterMeetingStartDate: function(){
            let vm = this;
            vm.$refs.meetings_datatable.vmDataTable.ajax.reload(); // This calls ajax() backend call.
            sessionStorage.setItem(vm.filterMeetingStartDate_cache, vm.filterMeetingStartDate);
        },
        filterMeetingEndDate: function(){
            let vm = this;
            vm.$refs.meetings_datatable.vmDataTable.ajax.reload(); // This calls ajax() backend call.
            sessionStorage.setItem(vm.filterMeetingEndDate_cache, vm.filterMeetingEndDate);
        },
        filterMeetingStatus: function() {
            let vm = this;
            vm.$refs.meetings_datatable.vmDataTable.ajax.reload(); // This calls ajax() backend call.  
            sessionStorage.setItem(vm.filterMeetingStatus_cache, vm.filterMeetingStatus);
        },
        filterApplied: function(){
            if (this.$refs.collapsible_filters){
                this.$refs.collapsible_filters.show_warning_icon(this.filterApplied)
            }
        },
    },
    computed:{
        filterApplied: function(){
            if(this.filterMeetingStartDate === '' && 
                this.filterMeetingEndDate === '' && 
                this.filterMeetingStatus === 'all'){
                return false
            } else {
                return true
            }
        },
        datatable_headers: function(){
            return ['Number', 'Title', 'Location', 'Start Date', 'End date', 'Status' , 'Action']
            
        },
        column_id: function(){
            return {
                data: "meeting_number",
                orderable: true,
                searchable: false,
                visible: true,
                'render': function(data, type, full){
                    return full.meeting_number
                },
                name: "id",
            }
        },
        column_location: function(){
            return {
                data: "location",
                orderable: true,
                searchable: true,
                visible: true,
                'render': function(data, type, full){
                    return full.location
                },
                name: "location",
            }
        },
        column_title: function(){
            return {
                data: "title",
                orderable: true,
                searchable: true,
                visible: true,
                'render': function(data, type, full){
                    return full.title
                },
                name: "title",
            }
        },
        column_start_date: function(){
            return {
                data: "start_date",
                orderable: true,
                searchable: true, // handles by filter_queryset override method
                visible: true,
                'render': function(data, type, full){
                    if (full.start_date){
                        //return full.start_date
                        return moment(full.start_date).format('DD/MM/YYYY') + moment(full.start_date).format(' h:mm:ss a')
                    }
                    // Should not reach here
                    return ''
                },
                name: "start_date",
            }
        },
        column_end_date: function(){
            return {
                data: "end_date",
                orderable: true,
                searchable: true, // handles by filter_queryset override method
                visible: true,
                'render': function(data, type, full){
                    if (full.end_date){
                        //return full.end_date
                        return moment(full.end_date).format('DD/MM/YYYY') + moment(full.end_date).format(' h:mm:ss a')
                    }
                    // Should not reach here
                    return ''
                },
                name: "end_date",
            }
        },
        column_status: function(){
            return {
                // 9. Workflow Status
                data: "processing_status",
                orderable: true,
                searchable: true,
                visible: true,
                'render': function(data, type, full){
                    if (full.processing_status){
                        return full.processing_status;
                    }
                    // Should not reach here
                    return ''
                },
                name: "processing_status",
            }
        },
        column_action: function(){
            let vm = this
            return {
                // 10. Action
                data: "id",
                orderable: false,
                searchable: false,
                visible: true,
                'render': function(data, type, full){
                    let links = "";
                    if (full.can_user_edit) {
                            links +=  `<a href='/internal/meetings/${full.id}'>Continue</a><br/>`;
                            links +=  `<a href='#${full.id}' data-discard-meeting='${full.id}'>Discard</a><br/>`;
                        }
                    else{
                            //if(full.user_process){   
                                links +=  `<a href='/internal/meetings/${full.id}?action=edit'>Edit</a><br/>`;    
                            //}
                            links +=  `<a href='/internal/meetings/${full.id}?action=view'>View</a><br/>`;
                        }
                    return links;
                }
            }
        },
        datatable_options: function(){
            let vm = this

            let columns = []
            let search = null
            let buttons = []
            
            
            columns = [
                vm.column_id,
                vm.column_title,
                vm.column_location,
                vm.column_start_date,
                vm.column_end_date,
                vm.column_status,
                vm.column_action,
            ]
            search = true
            buttons = [ 
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
                        orthogonal: 'export',
                    } 
                }, 
            ]

            

            return {
                autoWidth: false,
                language: {
                    processing: "<i class='fa fa-4x fa-spinner fa-spin'></i>"
                },
                order: [
                    [0, 'desc']
                ],
                lengthMenu: [ [10, 25, 50, 100, -1], [10, 25, 50, 100, "All"] ],
                responsive: true,
                serverSide: true,
                searching: search,
                 //  to show the "workflow Status","Action" columns always in the last position
                columnDefs: [
                    { responsivePriority: 1, targets: 0 },
                    { responsivePriority: 3, targets: -1 },
                    { responsivePriority: 2, targets: -2 }
                ],
                ajax: {
                    "url": this.url,
                    "dataSrc": 'data',

                    // adding extra GET params for Custom filtering
                    "data": function ( d ) {
                        d.filter_start_date = vm.filterMeetingStartDate;
                        d.filter_end_date = vm.filterMeetingEndDate;
                        d.filter_meeting_status = vm.filterMeetingStatus;
                        // d.filter_group_type = vm.group_type_name;
                    }
                },
                //dom: 'lBfrtip',
                dom: "<'d-flex align-items-center'<'me-auto'l>fB>" +
                     "<'row'<'col-sm-12'tr>>" +
                     "<'d-flex align-items-center'<'me-auto'i>p>",
                buttons: buttons,

                columns: columns,
                processing: true,
                initComplete: function() {
                    helpers.enablePopovers();
                },
            }
        },
    },
    methods:{
        collapsible_component_mounted: function(){
            this.$refs.collapsible_filters.show_warning_icon(this.filterApplied)
        },

        constructMeetingsTable: function(){
            this.$refs.meetings_datatable.vmDataTable.clear().draw();
        },
        createMeeting: async function () {
            let newMeetingId = null
            try {
                    const createUrl = api_endpoints.meeting+"/";
                    let payload = new Object();
                    payload.meeting_type = 'meeting';
                    let savedMeeting = await Vue.http.post(createUrl, payload);
                    if (savedMeeting) {
                        newMeetingId = savedMeeting.body.id;
                    }
                }
            catch (err) {
                console.log(err);
                if (this.is_internal) {
                    return err;
                }
            }
            this.$router.push({
                name: 'internal-meetings',
                params: {meeting_id: newMeetingId},
                });
        },
        fetchFilterLists: function () {
            let vm = this;
            vm.meeting_status = vm.internal_status;

        },
        discardMeeting:function (meeting_id) {
            let vm = this;
            swal({
                title: "Discard Meeting",
                text: "Are you sure you want to discard this meeting?",
                type: "warning",
                showCancelButton: true,
                confirmButtonText: 'Discard Meeting',
                confirmButtonColor:'#d9534f'
            }).then(() => {
                vm.$http.delete(api_endpoints.discard_meeting(meeting_id))
                .then((response) => {
                    swal(
                        'Discarded',
                        'Your meeting has been discarded',
                        'success'
                    )
                    vm.$refs.meetings_datatable.vmDataTable.ajax.reload();
                }, (error) => {
                    console.log(error);
                });
            },(error) => {

            });
        },
        addEventListeners: function(){
            let vm = this;
            // External Discard listener
            vm.$refs.meetings_datatable.vmDataTable.on('click', 'a[data-discard-meeting]', function(e) {
                e.preventDefault();
                var id = $(this).attr('data-discard-meeting');
                vm.discardMeeting(id);
            });
        },
    },
    mounted: function() {
        let vm = this;
        vm.fetchFilterLists();
    },
    created: function() {
        let vm = this;
        this.$nextTick(() => {
            //vm.constructMeetingsTable();
            vm.addEventListeners();
        });
    },
}
</script>
<style scoped>
.dt-buttons{
    float: right;
}
.collapse-icon {
    cursor: pointer;
}
.collapse-icon::before {
    top: 5px;
    left: 4px;
    height: 14px;
    width: 14px;
    border-radius: 14px;
    line-height: 14px;
    border: 2px solid white;
    line-height: 14px;
    content: '-';
    color: white;
    background-color: #d33333;
    display: inline-block;
    box-shadow: 0px 0px 3px #444;
    box-sizing: content-box;
    text-align: center;
    text-indent: 0 !important;
    font-family: 'Courier New', Courier monospace;
    margin: 5px;
}
.expand-icon {
    cursor: pointer;
}
.expand-icon::before {
    top: 5px;
    left: 4px;
    height: 14px;
    width: 14px;
    border-radius: 14px;
    line-height: 14px;
    border: 2px solid white;
    line-height: 14px;
    content: '+';
    color: white;
    background-color: #337ab7;
    display: inline-block;
    box-shadow: 0px 0px 3px #444;
    box-sizing: content-box;
    text-align: center;
    text-indent: 0 !important;
    font-family: 'Courier New', Courier monospace;
    margin: 5px;
}

</style>
