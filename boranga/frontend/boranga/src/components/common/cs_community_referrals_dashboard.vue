<template id="cs_communities_referrals_dashboard">
    <div>
        <CollapsibleFilters component_title="Filters" ref="collapsible_filters" @created="collapsible_component_mounted" class="mb-2">
            <div class="row">
                <div class="col-md-3">
                    <div class="form-group">
                        <label for="">Community ID:</label>
                        <select class="form-select" v-model="filterCSRefCommunityMigratedId">
                            <option value="all">All</option>
                            <option v-for="community in communities_data_list" :value="community.community_migrated_id">
                                {{community.community_migrated_id}}
                            </option>
                        </select>
                    </div>
                </div>
                <div class="col-md-3">
                    <div class="form-group">
                        <label for="">Community Name:</label>
                        <select class="form-select" v-model="filterCSRefCommunityName">
                            <option value="all">All</option>
                            <option v-for="option in community_name_list" :value="option.id">
                                {{option.name}}
                            </option>
                        </select>
                    </div>
                </div>
                <div class="col-md-3">
                    <div class="form-group">
                        <label for="">Community Status:</label>
                        <select class="form-select" v-model="filterCSRefCommunityStatus">
                            <option value="all">All</option>
                            <option v-for="community in communities_data_list" :value="community.community_status">
                                {{community.community_status}}
                            </option>
                        </select>
                    </div>
                </div>
                <div class="col-md-3">
                    <div class="form-group">
                        <label for="">Conservation List:</label>
                        <select class="form-select" v-model="filterCSRefCommunityConservationList"
                        @change="filterConservationCategory($event)">
                            <option value="all">All</option>
                            <option v-for="list in conservation_list_dict" :value="list.id">{{list.code}}</option>
                        </select>
                    </div>
                </div>
                <div class="col-md-3">
                    <div class="form-group">
                        <label for="">Conservation Category:</label>
                        <select class="form-select" v-model="filterCSRefCommunityConservationCategory">
                            <option value="all">All</option>
                            <option v-for="list in filtered_conservation_category_list" :value="list.id">{{list.code}}</option>
                        </select>
                    </div>
                </div>
                <div class="col-md-3">
                    <div class="form-group">
                        <label for="">Status:</label>
                        <select class="form-select" v-model="filterCSRefCommunityApplicationStatus">
                            <option value="all">All</option>
                            <option v-for="status in proposal_status" :value="status.value">{{ status.name }}</option>
                        </select>
                    </div>
                </div>
                <div class="col-md-3">
                    <div class="form-group">
                        <label for="">Region:</label>
                        <select class="form-select" v-model="filterCSRefCommunityRegion">
                            <option value="all">All</option>
                            <option v-for="region in region_list" :value="region.id">{{region.name}}</option>
                        </select>
                    </div>
                </div>
                <div class="col-md-3">
                    <div class="form-group">
                        <label for="">District:</label>
                        <select class="form-select" v-model="filterCSRefCommunityDistrict">
                            <option value="all">All</option>
                            <option v-for="district in district_list" :value="district.id">{{district.name}}</option>
                        </select>
                    </div>
                </div>
            </div>
        </CollapsibleFilters>
        <div class="row">
            <div class="col-lg-12">
                <datatable
                        ref="cs_communities_ref_datatable"
                        :id="datatable_id"
                        :dtOptions="datatable_options"
                        :dtHeaders="datatable_headers"
                    />
            </div>
        </div>
    </div>
</template>
<script>
import "babel-polyfill"
import datatable from '@/utils/vue/datatable.vue'
import CollapsibleFilters from '@/components/forms/collapsible_component.vue'
import FormSection from '@/components/forms/section_toggle.vue'
import Vue from 'vue'
import {
    api_endpoints,
    helpers
}from '@/utils/hooks'
export default {
    name: 'CSReferralsCommunityTable',
    props: {
        group_type_name:{
            type: String,
            required: true
        },
        group_type_id:{
            type: Number,
            required: true,
            default: 0
        },
        url:{
            type: String,
            required: true
        },
        filterCSRefCommunityMigratedId_cache: {
            type: String,
            required: false,
            default: 'filterCSRefCommunityMigratedId',
        },
        filterCSRefCommunityName_cache: {
            type: String,
            required: false,
            default: 'filterCSRefCommunityName',
        },
        filterCSRefCommunityStatus_cache: {
            type: String,
            required: false,
            default: 'filterCSRefCommunityStatus',
        },
        filterCSRefCommunityConservationList_cache: {
            type: String,
            required: false,
            default: 'filterCSRefCommunityConservationList',
        },
        filterCSRefCommunityConservationCategory_cache: {
            type: String,
            required: false,
            default: 'filterCSRefCommunityConservationCategory',
        },
        filterCSRefCommunityRegion_cache: {
            type: String,
            required: false,
            default: 'filterCSRefCommunityRegion',
        },
        filterCSRefCommunityDistrict_cache: {
            type: String,
            required: false,
            default: 'filterCSRefCommunityDistrict',
        },
        filterCSRefCommunityApplicationStatus_cache: {
            type: String,
            required: false,
            default: 'filterCSRefCommunityApplicationStatus',
        },
    },
    data() {
        let vm = this;
        return {
            datatable_id: 'cs-communities-ref-datatable-'+vm._uid,
     
            // selected values for filtering
            filterCSRefCommunityMigratedId: sessionStorage.getItem(this.filterCSRefCommunityMigratedId_cache) ? 
                                sessionStorage.getItem(this.filterCSRefCommunityMigratedId_cache) : 'all',

            filterCSRefCommunityName: sessionStorage.getItem(this.filterCSRefCommunityName_cache) ? 
                                    sessionStorage.getItem(this.filterCSRefCommunityName_cache) : 'all',

            filterCSRefCommunityStatus: sessionStorage.getItem(this.filterCSRefCommunityStatus_cache) ? 
                                    sessionStorage.getItem(this.filterCSRefCommunityStatus_cache) : 'all',

            filterCSRefCommunityConservationList: sessionStorage.getItem(this.filterCSRefCommunityConservationList_cache) ?sessionStorage.getItem(this.filterCSRefCommunityConservationList_cache) : 'all',

            filterCSRefCommunityConservationCategory: 
                sessionStorage.getItem(this.filterCSRefCommunityRefConservationCategory_cache) ? 
                sessionStorage.getItem(this.filterCSRefCommunityRefConservationCategory_cache) : 'all',

            filterCSRefCommunityRegion: sessionStorage.getItem(this.filterCSRefCommunityRegion_cache) ? 
                                    sessionStorage.getItem(this.filterCSRefCommunityRegion_cache) : 'all',

            filterCSRefCommunityDistrict: sessionStorage.getItem(this.filterCSRefCommunityDistrict_cache) ? 
                                        sessionStorage.getItem(this.filterCSRefCommunityDistrict_cache) : 'all',

            filterCSRefCommunityApplicationStatus: 
                    sessionStorage.getItem(this.filterCSRefCommunityApplicationStatus_cache) ?
                    sessionStorage.getItem(this.filterCSRefCommunityApplicationStatus_cache) : 'all',

            //Filter list for Community select box
            filterListsCommunities: {},
            communities_data_list: [],
            community_name_list: [],
            conservation_list_dict: [],
            conservation_category_list: [],
            filtered_conservation_category_list: [],
            filterRegionDistrict: {},
            region_list: [],
            district_list: [],
            proposal_status: [],

        }
    },
    components:{
        datatable,
        CollapsibleFilters,
        FormSection,
    },
    watch:{
        filterCSRefCommunityMigratedId: function(){
            let vm = this;
            vm.$refs.cs_communities_ref_datatable.vmDataTable.ajax.reload(); // This calls ajax() backend call.  
            sessionStorage.setItem(vm.filterCSRefCommunityMigratedId_cache, vm.filterCSRefCommunityMigratedId);
        },
        filterCSRefCommunityName: function() {
            let vm = this;
            vm.$refs.cs_communities_ref_datatable.vmDataTable.ajax.reload(); // This calls ajax() backend call.  
            sessionStorage.setItem(vm.filterCSRefCommunityName_cache, vm.filterCSRefCommunityName);
        },
        filterCSRefCommunityStatus: function() {
            let vm = this;
            vm.$refs.cs_communities_ref_datatable.vmDataTable.ajax.reload(); // This calls ajax() backend call.  
            sessionStorage.setItem(vm.filterCSRefCommunityStatus_cache, vm.filterCSRefCommunityStatus);
        },
        filterCSRefCommunityConservationList: function() {
            let vm = this;
            vm.$refs.cs_communities_ref_datatable.vmDataTable.ajax.reload(); // This calls ajax() backend call.  
            sessionStorage.setItem(vm.filterCSRefCommunityConservationList_cache, vm.filterCSRefCommunityConservationList);
        },
        filterCSRefCommunityConservationCategory: function() {
            let vm = this;
            vm.$refs.cs_communities_ref_datatable.vmDataTable.ajax.reload(); // This calls ajax() backend call.  
            sessionStorage.setItem(vm.filterCSRefCommunityConservationCategory_cache, 
                vm.filterCSRefCommunityConservationCategory);
        },
        filterCSRefCommunityRegion: function(){
            let vm = this;
            vm.$refs.cs_communities_ref_datatable.vmDataTable.ajax.reload(); // This calls ajax() backend call.
            sessionStorage.setItem(vm.filterCSRefCommunityRegion_cache, vm.filterCSRefCommunityRegion);
        },
        filterCSRefCommunityDistrict: function(){
            let vm = this;
            vm.$refs.cs_communities_ref_datatable.vmDataTable.ajax.reload(); // This calls ajax() backend call.
            sessionStorage.setItem(vm.filterCSRefCommunityDistrict_cache, vm.filterCSRefCommunityDistrict);
        },
        filterCSRefCommunityApplicationStatus: function() {
            let vm = this;
            vm.$refs.cs_communities_ref_datatable.vmDataTable.ajax.reload(); // This calls ajax() backend call.  
            sessionStorage.setItem(
                vm.filterCSRefCommunityApplicationStatus_cache, vm.filterCSRefCommunityApplicationStatus
                );
        },
        filterApplied: function(){
            if (this.$refs.collapsible_filters){
                // Collapsible component exists
                this.$refs.collapsible_filters.show_warning_icon(this.filterApplied)
            }
        },
    },
    computed: {
        filterApplied: function(){
            if(this.filterCSRefCommunityMigratedId === 'all' && 
                this.filterCSRefCommunityName === 'all' && 
                this.filterCSRefCommunityStatus === 'all' && 
                this.filterCSRefCommunityConservationList === 'all' && 
                this.filterCSRefCommunityConservationCategory === 'all' && 
                this.filterCSRefCommunityRegion === 'all' && 
                this.filterCSRefCommunityDistrict === 'all' && 
                this.filterCSRefCommunityApplicationStatus === 'all'){
                return false
            } else {
                return true
            }
        },
        datatable_headers: function(){
           return ['Number', 'Community','Community Id' ,'Community Name', 'Conservation List' , 'Conservation Category',      /*'Region', 'District',*/ 'Status', 'Action']
        },
        column_number: function(){
            return {
                data: "conservation_status_number",
                orderable: true,
                searchable: true,
                visible: true,
                'render': function(data, type, full){
                    let tick='';
                            if (full.can_be_processed){
                                tick = "<i class='fa fa-exclamation-circle' style='color:#FFBF00'></i>";
                            }
                            else
                            {
                                tick = "<i class='fa fa-check-circle' style='color:green'></i>";
                            }
                    return full.conservation_status_number+tick;
                },
                name: "conservation_status__id, conservation_status__conservation_status_number",
            }
        },
        column_community_number: function(){
            return {
                data: "community_number",
                orderable: true,
                searchable: true,
                visible: true,
                'render': function(data, type, full){
                    return full.community_number
                },
                name: "conservation_status__community__community_number",
            }
        },
        column_community_id: function(){
            return {
                data: "community_migrated_id",
                orderable: true,
                searchable: true,
                visible: true,
                'render': function(value, type){
                    let result = helpers.dtPopover(value, 30, 'hover');
                    return type=='export' ? value : result;
                },
                name: "conservation_status__community__community_migrated_id",
            }
        },
        column_community_name: function(){
            return {
                data: "community_name",
                orderable: true,
                searchable: true,
                visible: true,
                'render': function(value, type){
                    let result = helpers.dtPopover(value, 30, 'hover');
                    return type=='export' ? value : result;
                },
                //'createdCell': helpers.dtPopoverCellFn,
                name: "conservation_status__community__community_name__name",
            }
        },
        /*column_community_status: function(){
            return {
                data: "community_status",
                orderable: true,
                searchable: true,
                visible: true,
                'render': function(value, type){
                    let result = helpers.dtPopover(value, 30, 'hover');
                    return type=='export' ? value : result;
                },
                //'createdCell': helpers.dtPopoverCellFn,
                name: "conservation_status__community__community_status",
            }
        },*/
        column_conservation_list: function(){
            return {
                data: "conservation_list",
                orderable: true,
                searchable: true,
                visible: true,
                'render': function(value, type){
                    let result = helpers.dtPopover(value, 30, 'hover');
                    return type=='export' ? value : result;
                },
                //'createdCell': helpers.dtPopoverCellFn,
                name: "conservation_status__conservation_list__code",
            }
        },
        column_conservation_category: function(){
            return {
                data: "conservation_category",
                orderable: true,
                searchable: true,
                visible: true,
                'render': function(value, type){
                    let result = helpers.dtPopover(value, 30, 'hover');
                    return type=='export' ? value : result;
                },
                //'createdCell': helpers.dtPopoverCellFn,
                name: "conservation_status__conservation_category__code",
            }
        },
        column_status: function(){
            return {
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
                name: "conservation_status__processing_status",
            }
        },
        /*column_region: function(){
            return {
                data: "region",
                orderable: true,
                searchable: false,
                visible: true,
                'render': function(data, type, full){
                    if(full.region){
                        return full.region;
                    }
                    // Should not reach here
                    return ''
                },
                name: "conservation_status__community__region__name",
            }
        },
        column_district: function(){
            return {
                data: "district",
                orderable: true,
                searchable: false, // handles by filter_queryset override method - class ProposalFilterBackend
                visible: true,
                'render': function(data, type, full){
                    if (full.district){
                        return full.district
                    }
                    // Should not reach here
                    return ''
                },
                name: "conservation_status__community__district__name",
            }
        },*/
        column_action: function(){
            let vm = this
            return {
                // 9. Action
                data: "id",
                orderable: false,
                searchable: false,
                visible: true,
                'render': function(data, type, full){
                    let links = '';
                    links +=  full.can_user_process ? `<a href='/internal/conservation_status/${full.conservation_status}/referral/${full.id}'>Process</a><br/>`: `<a href='/internal/conservation_status/${full.conservation_status}/referral/${full.id}'>View</a><br/>`;
                    return links;
                }
            }
        },
        datatable_options: function(){
            let vm = this

            let columns = [
                vm.column_number,
                vm.column_community_number,
                vm.column_community_id,
                vm.column_community_name,
                /*vm.column_community_status,*/
                vm.column_conservation_list,
                vm.column_conservation_category,
                /*vm.column_region,
                vm.column_district,*/
                vm.column_status,
                vm.column_action,
            ]
            let search = false
            let buttons = [
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
                        d.filter_community_migrated_id = vm.filterCSRefCommunityMigratedId;
                        d.filter_community_name = vm.filterCSRefCommunityName;
                        d.filter_community_status = vm.filterCSRefCommunityStatus;
                        d.filter_conservation_list = vm.filterCSRefCommunityConservationList;
                        d.filter_conservation_category = vm.filterCSRefCommunityConservationCategory;
                        d.filter_group_type = vm.group_type_name;
                        d.filter_region = vm.filterCSRefCommunityRegion;
                        d.filter_district = vm.filterCSRefCommunityDistrict;
                        d.filter_application_status = vm.filterCSRefCommunityApplicationStatus;
                        d.is_internal = vm.is_internal;
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
        }
    
    },
    methods:{
        collapsible_component_mounted: function(){
            this.$refs.collapsible_filters.show_warning_icon(this.filterApplied)
        },

        fetchFilterLists: function(){
            let vm = this;

            vm.$http.get(api_endpoints.filter_list_cs_referrals_community+ '?group_type_name=' + vm.group_type_name).then((response) => {
                vm.filterListsCommunities= response.body;
                vm.communities_data_list= vm.filterListsCommunities.community_data_list;
                vm.community_name_list = vm.filterListsCommunities.community_name_list;
                vm.conservation_list_dict = vm.filterListsCommunities.conservation_list_dict;
                vm.conservation_category_list = vm.filterListsCommunities.conservation_category_list;
                vm.filterConservationCategory();
                vm.proposal_status = vm.filterListsCommunities.processing_status_list
            },(error) => {
                console.log(error);
            })
            vm.$http.get(api_endpoints.region_district_filter_dict).then((response) => {
                vm.filterRegionDistrict= response.body;
                vm.region_list= vm.filterRegionDistrict.region_list;
                vm.district_list= vm.filterRegionDistrict.district_list;
            },(error) => {
                console.log(error);
            })
        },
        //-------filter category dropdown dependent on conservation_list selected
        filterConservationCategory: function(event) {
                this.$nextTick(() => {
                    if(event){
                      this.filterCSRefCommunityConservationCategory='all'; //-----to remove the previous selection
                    }
                    this.filtered_conservation_category_list=[];
                    //---filter conservation_categories as per cons_list selected
                    for(let choice of this.conservation_category_list){
                        if(choice.conservation_list_id.toString() === this.filterCSRefCommunityConservationList.toString())
                        {
                          this.filtered_conservation_category_list.push(choice);
                        }
                    }
                });
        },
        addEventListeners: function(){
            let vm = this;
        },
        initialiseSearch:function(){
            this.submitterSearch();
        },
        submitterSearch:function(){
            let vm = this;
            vm.$refs.cs_communities_ref_datatable.table.dataTableExt.afnFiltering.push(
                function(settings,data,dataIndex,original){
                    let filtered_submitter = vm.filterProposalSubmitter;
                    if (filtered_submitter == 'All'){ return true; } 
                    return filtered_submitter == original.submitter.email;
                }
            );
        },
    },


    mounted: function(){
        this.fetchFilterLists();
        let vm = this;
        $( 'a[data-toggle="collapse"]' ).on( 'click', function () {
            var chev = $( this ).children()[ 0 ];
            window.setTimeout( function () {
                $( chev ).toggleClass( "glyphicon-chevron-down glyphicon-chevron-up" );
            }, 100 );
        });
        this.$nextTick(() => {
            vm.initialiseSearch();
            vm.addEventListeners();
        });
    }
}
</script>
<style scoped>
.dt-buttons{
    float: right;
}
</style>
