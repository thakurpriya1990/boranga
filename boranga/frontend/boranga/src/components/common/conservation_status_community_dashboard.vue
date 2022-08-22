<template id="cs_communities_dashboard">
    <div>
        <CollapsibleFilters component_title="Filters" ref="collapsible_filters" @created="collapsible_component_mounted" class="mb-2">
            <div class="row">
                <div class="col-md-3">
                    <div class="form-group">
                        <label for="">Community ID:</label>
                        <select class="form-select" v-model="filterCSCommunityMigratedId">
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
                        <select class="form-select" v-model="filterCSCommunityName">
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
                        <select class="form-select" v-model="filterCSCommunityStatus">
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
                        <select class="form-select" v-model="filterCSCommunityConservationList"
                        @change="filterConservationCategory($event)">
                            <option value="all">All</option>
                            <option v-for="list in conservation_list_dict" :value="list.id">{{list.code}}</option>
                        </select>
                    </div>
                </div>
                <div class="col-md-3">
                    <div class="form-group">
                        <label for="">Conservation Category:</label>
                        <select class="form-select" v-model="filterCSCommunityConservationCategory">
                            <option value="all">All</option>
                            <option v-for="list in filtered_conservation_category_list" :value="list.id">{{list.code}}</option>
                        </select>
                    </div>
                </div>
                <div class="col-md-3">
                    <div class="form-group">
                        <label for="">Workflow Status:</label>
                        <select class="form-control">
                            <option value="all">All</option>
                        </select>
                    </div>
                </div>
                <div class="col-md-3">
                    <div class="form-group">
                        <label for="">Region:</label>
                        <select class="form-select" v-model="filterCSCommunityRegion">
                            <option value="all">All</option>
                            <option v-for="region in region_list" :value="region.id">{{region.name}}</option>
                        </select>
                    </div>
                </div>
                <div class="col-md-3">
                    <div class="form-group">
                        <label for="">District:</label>
                        <select class="form-select" v-model="filterCSCommunityDistrict">
                            <option value="all">All</option>
                            <option v-for="district in district_list" :value="district.id">{{district.name}}</option>
                        </select>
                    </div>
                </div>
            </div>
        </CollapsibleFilters>

        <div v-if="addCommunityCSVisibility" class="col-md-12">
            <div class="text-end">
                <button type="button" class="btn btn-primary mb-2 " @click.prevent="createCommunity"><i class="fa-solid fa-circle-plus"></i> Add Conservation Satus</button>
            </div>
        </div>

        <div class="row">
            <div class="col-lg-12">
                <datatable
                        ref="cs_communities_datatable"
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
    name: 'ConservationStatusCommunityTable',
    props: {
        level:{
            type: String,
            required: true,
            validator:function(val) {
                let options = ['internal','referral','external'];
                return options.indexOf(val) != -1 ? true: false;
            }
        },
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
        filterCSCommunityMigratedId_cache: {
            type: String,
            required: false,
            default: 'filterCSCommunityMigratedId',
        },
        filterCSCommunityName_cache: {
            type: String,
            required: false,
            default: 'filterCSCommunityName',
        },
        filterCSCommunityStatus_cache: {
            type: String,
            required: false,
            default: 'filterCSCommunityStatus',
        },
        filterCSCommunityConservationList_cache: {
            type: String,
            required: false,
            default: 'filterCSCommunityConservationList',
        },
        filterCSCommunityConservationCategory_cache: {
            type: String,
            required: false,
            default: 'filterCSCommunityConservationCategory',
        },
        filterCSCommunityRegion_cache: {
            type: String,
            required: false,
            default: 'filterCSCommunityRegion',
        },
        filterCSCommunityDistrict_cache: {
            type: String,
            required: false,
            default: 'filterCSCommunityDistrict',
        },
    },
    data() {
        let vm = this;
        return {
            datatable_id: 'cs-communities-datatable-'+vm._uid,
     
            //Profile to check if user has access to process Proposal
            profile: {},
            is_payment_admin: false,
            
            // selected values for filtering
            filterCSCommunityMigratedId: sessionStorage.getItem(this.filterCSCommunityMigratedId_cache) ? 
                                sessionStorage.getItem(this.filterCSCommunityMigratedId_cache) : 'all',

            filterCSCommunityName: sessionStorage.getItem(this.filterCSCommunityName_cache) ? 
                                    sessionStorage.getItem(this.filterCSCommunityName_cache) : 'all',

            filterCSCommunityStatus: sessionStorage.getItem(this.filterCSCommunityStatus_cache) ? 
                                    sessionStorage.getItem(this.filterCSCommunityStatus_cache) : 'all',

            filterCSCommunityConservationList: sessionStorage.getItem(this.filterCSCommunityConservationList_cache) ? 
                                    sessionStorage.getItem(this.filterCSCommunityConservationList_cache) : 'all',

            filterCSCommunityConservationCategory: sessionStorage.getItem(this.filterCSCommunityConservationCategory_cache)                     ? sessionStorage.getItem(this.filterCSCommunityConservationCategory_cache) : 'all',

            filterCSCommunityRegion: sessionStorage.getItem(this.filterCSCommunityRegion_cache) ? 
                                    sessionStorage.getItem(this.filterCSCommunityRegion_cache) : 'all',

            filterCSCommunityDistrict: sessionStorage.getItem(this.filterCSCommunityDistrict_cache) ? 
                                        sessionStorage.getItem(this.filterCSCommunityDistrict_cache) : 'all',

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
            
            // filtering options
            external_status:[
                {value: 'draft', name: 'Draft'},
                {value: 'with_assessor', name: 'Under Review'},
                {value: 'approved', name: 'Approved'},
                {value: 'declined', name: 'Declined'},
                {value: 'discarded', name: 'Discarded'},
                {value: 'awaiting_payment', name: 'Awaiting Payment'},
            ],
            internal_status:[
                {value: 'draft', name: 'Draft'},
                {value: 'with_assessor', name: 'With Assessor'},
                {value: 'on_hold', name: 'On Hold'},
                {value: 'with_qa_officer', name: 'With QA Officer'},
                {value: 'with_referral', name: 'With Referral'},
                {value: 'with_assessor_requirements', name: 'With Assessor (Requirements)'},
                {value: 'with_approver', name: 'With Approver'},
                {value: 'approved', name: 'Approved'},
                {value: 'declined', name: 'Declined'},
                {value: 'discarded', name: 'Discarded'},
                {value: 'awaiting_payment', name: 'Awaiting Payment'},
            ],
            
            proposal_status: [],

        }
    },
    components:{
        datatable,
        CollapsibleFilters,
        FormSection,
    },
    watch:{
        filterCSCommunityMigratedId: function(){
            let vm = this;
            vm.$refs.cs_communities_datatable.vmDataTable.ajax.reload(); // This calls ajax() backend call.  
            sessionStorage.setItem(vm.filterCSCommunityMigratedId_cache, vm.filterCSCommunityMigratedId);
        },
        filterCSCommunityName: function() {
            let vm = this;
            vm.$refs.cs_communities_datatable.vmDataTable.ajax.reload(); // This calls ajax() backend call.  
            sessionStorage.setItem(vm.filterCSCommunityName_cache, vm.filterCSCommunityName);
        },
        filterCSCommunityStatus: function() {
            let vm = this;
            vm.$refs.cs_communities_datatable.vmDataTable.ajax.reload(); // This calls ajax() backend call.  
            sessionStorage.setItem(vm.filterCSCommunityStatus_cache, vm.filterCSCommunityStatus);
        },
        filterCSCommunityConservationList: function() {
            let vm = this;
            vm.$refs.cs_communities_datatable.vmDataTable.ajax.reload(); // This calls ajax() backend call.  
            sessionStorage.setItem(vm.filterCSCommunityConservationList_cache, vm.filterCSCommunityConservationList);
        },
        filterCSCommunityConservationCategory: function() {
            let vm = this;
            vm.$refs.cs_communities_datatable.vmDataTable.ajax.reload(); // This calls ajax() backend call.  
            sessionStorage.setItem(vm.filterCSCommunityConservationCategory_cache, 
                vm.filterCSCommunityConservationCategory);
        },
        filterCSCommunityRegion: function(){
            let vm = this;
            vm.$refs.cs_communities_datatable.vmDataTable.ajax.reload(); // This calls ajax() backend call.
            sessionStorage.setItem(vm.filterCSCommunityRegion_cache, vm.filterCommunityRegion);
        },
        filterCSCommunityDistrict: function(){
            let vm = this;
            vm.$refs.cs_communities_datatable.vmDataTable.ajax.reload(); // This calls ajax() backend call.
            sessionStorage.setItem(vm.filterCSCommunityDistrict_cache, vm.filterCSCommunityDistrict);
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
            if(this.filterCSCommunityMigratedId === 'all' && 
                this.filterCSCommunityName === 'all' && 
                this.filterCSCommunityStatus === 'all' && 
                this.filterCSCommunityConservationList === 'all' && 
                this.filterCSCommunityConservationCategory === 'all' && 
                this.filterCSCommunityRegion === 'all' && 
                this.filterCSCommunityDistrict === 'all'){
                return false
            } else {
                return true
            }
        },
        is_external: function(){
            return this.level == 'external';
        },
        is_internal: function() {
            return this.level == 'internal'
        },
        is_referral: function(){
            return this.level == 'referral';
        },
        addCommunityCSVisibility: function() {
            let visibility = false;
            if (this.is_internal) {
                visibility = true;
            }
            return visibility;
        },
        datatable_headers: function(){
            if (this.is_external){
                return ['Number', 'Community','Community Id' ,'Community Name', 'Community Status', 
                    'Conservation List' , 'Conservation Category', 'Region', 'District', 'Workflow Status', 'Action']
            }
            if (this.is_internal){
                return ['Number', 'Community','Community Id' ,'Community Name', 'Community Status', 
                        'Conservation List', 'Conservation Category', 'Region', 'District', 'Workflow Status', 'Action']
            }
        },
        column_id: function(){
            return {
                data: "id",
                orderable: true,
                searchable: false,
                visible: false,
                'render': function(data, type, full){
                    return full.id
                },
                name: "id",
            }
        },
        column_number: function(){
            return {
                data: "conservation_status_number",
                orderable: true,
                searchable: true,
                visible: true,
                'render': function(data, type, full){
                    return full.conservation_status_number
                },
                name: "id",
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
                name: "community__community_number",
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
                name: "community__community_migrated_id",
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
                name: "community__community_name__name",
            }
        },
        column_community_status: function(){
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
                name: "community__community_status",
            }
        },
        column_conservation_list: function(){
            return {
                data: "current_conservation_list",
                orderable: true,
                searchable: true,
                visible: true,
                'render': function(value, type){
                    let result = helpers.dtPopover(value, 30, 'hover');
                    return type=='export' ? value : result;
                },
                //'createdCell': helpers.dtPopoverCellFn,
                name: "current_conservation_list__code",
            }
        },
        column_conservation_category: function(){
            return {
                data: "current_conservation_category",
                orderable: true,
                searchable: true,
                visible: true,
                'render': function(value, type){
                    let result = helpers.dtPopover(value, 30, 'hover');
                    return type=='export' ? value : result;
                },
                //'createdCell': helpers.dtPopoverCellFn,
                name: "current_conservation_category__code",
            }
        },
        column_workflow_status: function(){
            return {
                data: "community_status",
                orderable: true,
                searchable: true,
                visible: true,
                'render': function(data, type, full){
                    if (full.community_status){
                        return full.community_status;
                    }
                    // Should not reach here
                    return ''
                },
                name: "community__community_status",
            }
        },
        column_region: function(){
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
                name: "community__region__name",
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
                name: "community__district__name",
            }
        },
        column_action: function(){
            let vm = this
            return {
                // 9. Action
                data: "id",
                orderable: false,
                searchable: false,
                visible: true,
                'render': function(data, type, full){
                    let links = "";
                    if (!vm.is_external){
                        /*if(vm.check_assessor(full) && full.can_officer_process)*/
                        if(full.assessor_process){   
                                links +=  `<a href='/internal/conservation_status/${full.id}?group_type_name=${full.group_type}'>Process</a><br/>`;
                        }
                        else{
                            links +=  `<a href='/internal/conservation_status/${full.id}?group_type_name=${full.group_type}'>View</a><br/>`;
                        }
                    }
                    else{
                        if (full.can_user_edit) {
                            links +=  `<a href='/external/conservation_status/${full.id}?group_type_name=${full.group_type}'>Continue</a><br/>`;
                            links +=  `<a href='#${full.id}' data-discard-proposal='${full.id}?group_type_name=${full.group_type}'>Discard</a><br/>`;
                        }
                        else if (full.can_user_view) {
                            links +=  `<a href='/external/conservation_status/${full.id}?group_type_name=${full.group_type}'>View</a>`;
                        }
                    }

                    links +=  `<a href='/internal/conservation_status/${full.id}?group_type_name=${full.group_type}'>Edit</a><br/>`; // Dummy addition for Boranaga demo

                    return links;
                }
            }
        },
        datatable_options: function(){
            let vm = this

            let columns = []
            let search = null
            let buttons = []
            if(vm.is_external){
                columns = [
                    vm.column_number,
                    vm.column_community_number,
                    vm.column_community_id,
                    vm.column_community_name,
                    vm.column_community_status,
                    vm.column_conservation_list,
                    vm.column_conservation_category,
                    vm.column_region,
                    vm.column_district,
                    vm.column_workflow_status,
                    vm.column_action,
                ]
                search = false
                buttons = []
            }
            if(vm.is_internal){
                columns = [
                    vm.column_number,
                    vm.column_community_number,
                    vm.column_community_id,
                    vm.column_community_name,
                    vm.column_community_status,
                    vm.column_conservation_list,
                    vm.column_conservation_category,
                    vm.column_region,
                    vm.column_district,
                    vm.column_workflow_status,
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
                            orthogonal: 'export' 
                        }
                    },
                ]

            }

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
                        d.filter_community_migrated_id = vm.filterCSCommunityMigratedId;
                        d.filter_community_name = vm.filterCSCommunityName;
                        d.filter_community_status = vm.filterCSCommunityStatus;
                        d.filter_conservation_list = vm.filterCSCommunityConservationList;
                        d.filter_conservation_category = vm.filterCSCommunityConservationCategory;
                        d.filter_group_type = vm.group_type_name;
                        d.filter_region = vm.filterCSCommunityRegion;
                        d.filter_district = vm.filterCSCommunityDistrict;
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

            vm.$http.get(api_endpoints.community_filter_dict+ '?group_type_name=' + vm.group_type_name).then((response) => {
                vm.filterListsCommunities= response.body;
                vm.communities_data_list= vm.filterListsCommunities.community_data_list;
                vm.community_name_list = vm.filterListsCommunities.community_name_list;
                vm.conservation_list_dict = vm.filterListsCommunities.conservation_list_dict;
                vm.conservation_category_list = vm.filterListsCommunities.conservation_category_list;
                vm.filterConservationCategory();
                //vm.proposal_status = vm.level == 'internal' ? response.body.processing_status_choices: response.body.customer_status_choices;
                //vm.proposal_status = vm.level == 'internal' ? vm.internal_status: vm.external_status;
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
                      this.filterCSCommunityConservationCategory='all'; //-----to remove the previous selection
                    }
                    this.filtered_conservation_category_list=[];
                    //---filter conservation_categories as per cons_list selected
                    for(let choice of this.conservation_category_list){
                        if(choice.conservation_list_id.toString() === this.filterCSCommunityConservationList.toString())
                        {
                          this.filtered_conservation_category_list.push(choice);
                        }
                    }
                });
        },
        createCommunity: async function () {
            let newCommunityId = null
            try {
                    const createUrl = api_endpoints.community+"/";
                    let payload = new Object();
                    payload.group_type_id = this.group_type_id
                    let savedCommunity = await Vue.http.post(createUrl, payload);
                    if (savedCommunity) {
                        newCommunityId = savedCommunity.body.id;
                    }
                }
            catch (err) {
                console.log(err);
                if (this.is_internal) {
                    return err;
                }
            }
            this.$router.push({
                name: 'internal-species-communities',
                params: {species_community_id: newCommunityId},
                query: {group_type_name: this.group_type_name},
                });
        },

        discardProposal:function (proposal_id) {
            let vm = this;
            swal({
                title: "Discard Application",
                text: "Are you sure you want to discard this proposal?",
                type: "warning",
                showCancelButton: true,
                confirmButtonText: 'Discard Application',
                confirmButtonColor:'#d9534f'
            }).then(() => {
                vm.$http.delete(api_endpoints.discard_proposal(proposal_id))
                .then((response) => {
                    swal(
                        'Discarded',
                        'Your proposal has been discarded',
                        'success'
                    )
                    vm.$refs.cs_communities_datatable.vmDataTable.ajax.reload();
                }, (error) => {
                    console.log(error);
                });
            },(error) => {

            });
        },
        addEventListeners: function(){
            let vm = this;
            // External Discard listener
            vm.$refs.cs_communities_datatable.vmDataTable.on('click', 'a[data-discard-proposal]', function(e) {
                e.preventDefault();
                var id = $(this).attr('data-discard-proposal');
                vm.discardProposal(id);
            });
        },
        initialiseSearch:function(){
            this.submitterSearch();
        },
        submitterSearch:function(){
            let vm = this;
            vm.$refs.cs_communities_datatable.table.dataTableExt.afnFiltering.push(
                function(settings,data,dataIndex,original){
                    let filtered_submitter = vm.filterProposalSubmitter;
                    if (filtered_submitter == 'All'){ return true; } 
                    return filtered_submitter == original.submitter.email;
                }
            );
        },
        fetchProfile: function(){
            let vm = this;
            /*Vue.http.get(api_endpoints.profile).then((response) => {
                vm.profile = response.body;
                vm.is_payment_admin=response.body.is_payment_admin;
                              
            },(error) => {
                console.log(error);
                
            })*/
        },

        check_assessor: function(proposal){
            let vm = this;
            if (proposal.assigned_officer)
                {
                    { if(proposal.assigned_officer== vm.profile.full_name)
                        return true;
                    else
                        return false;
                }
            }
            else{
                 var assessor = proposal.allowed_assessors.filter(function(elem){
                    return(elem.id=vm.profile.id)
                });
                
                if (assessor.length > 0)
                    return true;
                else
                    return false;
              
            }
            
        },
    },


    mounted: function(){
        this.fetchFilterLists();
        this.fetchProfile();
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
