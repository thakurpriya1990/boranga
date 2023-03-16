<template id="meetings_datatable">
    <div>
        <CollapsibleFilters component_title="Filters" ref="collapsible_filters" @created="collapsible_component_mounted" class="mb-2">
            <div class="row">
                <div class="col-md-3">
                    <div class="form-group">
                        <label for="">Start Date:</label>
                        <input type="datetime-local" class="form-control" placeholder="DD/MM/YYYY" id="start_date" v-model="filterStartDate">
                    </div>
                </div>
                <div class="col-md-3">
                    <div class="form-group">
                        <label for="">End Date:</label>
                        <input type="datetime-local" class="form-control" placeholder="DD/MM/YYYY" id="end_date" v-model="filterEndDate">
                    </div>
                </div>
            </div>
        </CollapsibleFilters>
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

export default {
    name: 'MeetingsDatatable',
    props: {
        url:{
            type: String,
            required: true
        },
        filterStartDate_cache: {
            type: String,
            required: false,
            default: 'filterStartDate',
        },
        filterEndDate_cache: {
            type: String,
            required: false,
            default: 'filterEndDate',
        },
    },
    data: function() {
        let vm = this;
        return {

            datatable_id: 'meetings-datatable-'+vm._uid,
            dateFormat: 'DD/MM/YYYY',
            timeFormat: 'h:mm:ss a',
            filterStartDate: sessionStorage.getItem(this.filterStartDate_cache) ?
            sessionStorage.getItem(this.filterStartDate_cache) : '',

            filterEndDate: sessionStorage.getItem(this.filterEndDate_cache) ?
            sessionStorage.getItem(this.filterEndDate_cache) : '',
            
        }
    },
    components:{
        datatable,
        CollapsibleFilters,
    },
    watch:{
        filterStartDate: function(){
            let vm = this;
            vm.$refs.meetings_datatable.vmDataTable.ajax.reload(); // This calls ajax() backend call.
            sessionStorage.setItem(vm.filterStartDate_cache, vm.filterStartDate);
        },
        filterEndDate: function(){
            let vm = this;
            vm.$refs.meetings_datatable.vmDataTable.ajax.reload(); // This calls ajax() backend call.
            sessionStorage.setItem(vm.filterEndDate_cache, vm.filterEndDate);
        },
    },
    computed:{
        filterApplied: function(){
            if(
                this.filterStartDate === '' &&
                this.filterEndDate === ''){
                return false
            } else {
                return true
            }
        },
        datatable_headers: function(){
            return ['Number','Location','Title', 'Start Date', 'End date', 'Action']
            
        },
        column_id: function(){
            return {
                data: "id",
                orderable: true,
                searchable: false,
                visible: true,
                'render': function(data, type, full){
                    return full.id
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
                    links +=  `<a href='/internal/meetings/${full.id}'>Continue</a><br/>`;
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
                vm.column_location,
                vm.column_title,
                vm.column_start_date,
                vm.column_end_date,
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
                        d.filter_start_date = vm.filterStartDate;
                        d.filter_end_date = vm.filterEndDate;
                        // d.filter_group_type = vm.group_type_name;
                        // d.filter_scientific_name = vm.filterCSFaunaScientificName;
                        // d.filter_common_name = vm.filterCSFaunaCommonName;
                        // d.filter_phylogenetic_group = vm.filterCSFaunaPhylogeneticGroup;
                        // d.filter_family = vm.filterCSFaunaFamily;
                        // d.filter_genus = vm.filterCSFaunaGenus;
                        // d.filter_conservation_list = vm.filterCSFaunaConservationList;
                        // d.filter_conservation_category = vm.filterCSFaunaConservationCategory;
                        // d.filter_region = vm.filterCSFaunaRegion;
                        // d.filter_district = vm.filterCSFaunaDistrict;
                        // d.filter_application_status = vm.filterCSFaunaApplicationStatus;
                        // d.filter_effective_from_date = vm.filterCSFaunaEffectiveFromDate;
                        // d.filter_effective_to_date = vm.filterCSFaunaEffectiveToDate;
                        // d.is_internal = vm.is_internal;
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
            // if(this.species_community.conservation_status){
            //     for(let i=0; i<this.species_community.conservation_status.length; i++){
            //         this.addConservationStatusToTable(this.species_community.conservation_status[i]);
            //     }
            // }
        },
        addConservationStatusToTable: function(conservationStatus){
            this.$refs.conservation_status_datatable.vmDataTable.row.add({
                conservation_list: conservationStatus,
                conservation_category: conservationStatus,
                conservation_criteria: conservationStatus,
                conservation_list_id: conservationStatus,
                effective_status_date: conservationStatus,
            }).draw();
        }
    },
    created: function() {
        this.$nextTick(() => {
            this.constructMeetingsTable();
            // if(this.species_community.conservation_status){
            //     this.constructConservationStatusTable();
            // }
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
