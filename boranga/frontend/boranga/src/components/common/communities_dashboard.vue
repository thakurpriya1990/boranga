<template id="communities_dashboard">
    <div>
        <CollapsibleFilters component_title="Filters" ref="collapsible_filters" @created="collapsible_component_mounted" class="mb-2">
            <div class="row">
                <div class="col-md-3">
                    <div class="form-group">
                        <label for="">Community ID:</label>
                        <select class="form-select" v-model="filterCommunityMigratedId">
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
                        <select class="form-select" v-model="filterCommunityName">
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
                        <select class="form-select" v-model="filterCommunityStatus">
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
                        <select class="form-select" v-model="filterCommunityConservationList"
                        @change="filterConservationCategory($event)">
                            <option value="all">All</option>
                            <option v-for="list in conservation_list_dict" :value="list.id">{{list.code}}</option>
                        </select>
                    </div>
                </div>
                <div class="col-md-3">
                    <div class="form-group">
                        <label for="">Conservation Category:</label>
                        <select class="form-select" v-model="filterCommunityConservationCategory">
                            <option value="all">All</option>
                            <option v-for="list in filtered_conservation_category_list" :value="list.id">{{list.code}}</option>
                        </select>
                    </div>
                </div>
                <div class="col-md-3">
                    <div class="form-group">
                        <label for="">Workflow Status:</label>
                        <select class="form-select">
                            <option value="all">All</option>
                        </select>
                    </div>
                </div>
                <div class="col-md-3">
                    <div class="form-group">
                        <label for="">Region:</label>
                        <select class="form-select" v-model="filterCommunityRegion">
                            <option value="all">All</option>
                            <option v-for="region in region_list" :value="region.id">{{region.name}}</option>
                        </select>
                    </div>
                </div>
                <div class="col-md-3">
                    <div class="form-group">
                        <label for="">District:</label>
                        <select class="form-select" v-model="filterCommunityDistrict">
                            <option value="all">All</option>
                            <option v-for="district in district_list" :value="district.id">{{district.name}}</option>
                        </select>
                    </div>
                </div>
            </div>
        </CollapsibleFilters>

        <div v-if="newCommunityVisibility" class="col-md-12">
            <div class="text-end">
                <button type="button" class="btn btn-primary mb-2 " @click.prevent="createCommunity"><i class="fa-solid fa-circle-plus"></i> New Community </button>
            </div>
        </div>

        <div class="row">
            <div class="col-lg-12">
                <datatable
                        ref="communities_datatable"
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
    name: 'CommunitiesTable',
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
        filterCommunityMigratedId_cache: {
            type: String,
            required: false,
            default: 'filterCommunityMigratedId',
        },
        filterCommunityName_cache: {
            type: String,
            required: false,
            default: 'filterCommunityName',
        },
        filterCommunityStatus_cache: {
            type: String,
            required: false,
            default: 'filterCommunityStatus',
        },
        filterCommunityConservationList_cache: {
            type: String,
            required: false,
            default: 'filterCommunityConservationList',
        },
        filterCommunityConservationCategory_cache: {
            type: String,
            required: false,
            default: 'filterCommunityConservationCategory',
        },
        filterCommunityRegion_cache: {
            type: String,
            required: false,
            default: 'filterCommunityRegion',
        },
        filterCommunityDistrict_cache: {
            type: String,
            required: false,
            default: 'filterCommunityDistrict',
        },
    },
    data() {
        let vm = this;
        return {
            datatable_id: 'communities-datatable-'+vm._uid,
     
            //Profile to check if user has access to process Proposal
            profile: {},
            is_payment_admin: false,
            
            // selected values for filtering
            filterCommunityMigratedId: sessionStorage.getItem(this.filterCommunityMigratedId_cache) ? 
                                sessionStorage.getItem(this.filterCommunityMigratedId_cache) : 'all',

            filterCommunityName: sessionStorage.getItem(this.filterCommunityName_cache) ? 
                                    sessionStorage.getItem(this.filterCommunityName_cache) : 'all',

            filterCommunityStatus: sessionStorage.getItem(this.filterCommunityStatus_cache) ? 
                                    sessionStorage.getItem(this.filterCommunityStatus_cache) : 'all',

            filterCommunityConservationList: sessionStorage.getItem(this.filterCommunityConservationList_cache) ? 
                                    sessionStorage.getItem(this.filterCommunityConservationList_cache) : 'all',

            filterCommunityConservationCategory: sessionStorage.getItem(this.filterCommunityConservationCategory_cache) ? 
                                    sessionStorage.getItem(this.filterCommunityConservationCategory_cache) : 'all',

            filterCommunityRegion: sessionStorage.getItem(this.filterCommunityRegion_cache) ? 
                                    sessionStorage.getItem(this.filterCommunityRegion_cache) : 'all',

            filterCommunityDistrict: sessionStorage.getItem(this.filterCommunityDistrict_cache) ? 
                                        sessionStorage.getItem(this.filterCommunityDistrict_cache) : 'all',

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
        filterCommunityMigratedId: function(){
            let vm = this;
            vm.$refs.communities_datatable.vmDataTable.ajax.reload(); // This calls ajax() backend call.  
            sessionStorage.setItem(vm.filterCommunityMigratedId_cache, vm.filterCommunityMigratedId);
        },
        filterCommunityName: function() {
            let vm = this;
            vm.$refs.communities_datatable.vmDataTable.ajax.reload(); // This calls ajax() backend call.  
            sessionStorage.setItem(vm.filterCommunityName_cache, vm.filterCommunityName);
        },
        filterCommunityStatus: function() {
            let vm = this;
            vm.$refs.communities_datatable.vmDataTable.ajax.reload(); // This calls ajax() backend call.  
            sessionStorage.setItem(vm.filterCommunityStatus_cache, vm.filterCommunityStatus);
        },
        filterCommunityConservationList: function() {
            let vm = this;
            vm.$refs.communities_datatable.vmDataTable.ajax.reload(); // This calls ajax() backend call.  
            sessionStorage.setItem(vm.filterCommunityConservationList_cache, vm.filterCommunityConservationList);
        },
        filterCommunityConservationCategory: function() {
            let vm = this;
            vm.$refs.communities_datatable.vmDataTable.ajax.reload(); // This calls ajax() backend call.  
            sessionStorage.setItem(vm.filterCommunityConservationCategory_cache, vm.filterCommunityConservationCategory);
        },
        filterCommunityRegion: function(){
            let vm = this;
            vm.$refs.communities_datatable.vmDataTable.ajax.reload(); // This calls ajax() backend call.
            sessionStorage.setItem(vm.filterCommunityRegion_cache, vm.filterCommunityRegion);
        },
        filterCommunityDistrict: function(){
            let vm = this;
            vm.$refs.communities_datatable.vmDataTable.ajax.reload(); // This calls ajax() backend call.
            sessionStorage.setItem(vm.filterCommunityDistrict_cache, vm.filterCommunityDistrict);
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
            if(this.filterCommunityMigratedId === 'all' && 
                this.filterCommunityName === 'all' && 
                this.filterCommunityStatus === 'all' && 
                this.filterCommunityConservationList === 'all' && 
                this.filterCommunityConservationCategory === 'all' && 
                this.filterCommunityRegion === 'all' && 
                this.filterCommunityDistrict === 'all'){
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
        newCommunityVisibility: function() {
            let visibility = false;
            if (this.is_internal) {
                visibility = true;
            }
            return visibility;
        },
        datatable_headers: function(){
            if (this.is_external){
                return ['Id','Number', 'Community Id' ,'Community Name', 'Community Status', 'Conservation List' ,  
                            'Conservation Category', 'Action', 'Workflow Status', 'Region', 'District']
            }
            if (this.is_internal){
                return ['Id','Number', 'Community Id' ,'Community Name', 'Community Status', 'Conservation List',  
                            'Conservation Category', 'Action', 'Workflow Status', 'Region', 'District']
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
                data: "community_number",
                orderable: true,
                searchable: true,
                visible: true,
                'render': function(data, type, full){
                    return full.community_number
                },
                name: "id",
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
                name: "community_migrated_id",
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
                name: "community_name__name",
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
                name: "community_status",
            }
        },
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
                name: "community_status",
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
                name: "region__name",
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
                name: "district__name",
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
                                links +=  `<a href='/internal/species_communities/${full.id}?group_type_name=${full.group_type}'>Process</a><br/>`;
                        }
                        else{
                            links +=  `<a href='/internal/species_communities/${full.id}?group_type_name=${full.group_type}'>View</a><br/>`;
                        }
                    }
                    else{
                        if (full.can_user_edit) {
                            links +=  `<a href='/external/species_communities/${full.id}?group_type_name=${full.group_type}'>Continue</a><br/>`;
                            links +=  `<a href='#${full.id}' data-discard-proposal='${full.id}?group_type_name=${full.group_type}'>Discard</a><br/>`;
                        }
                        else if (full.can_user_view) {
                            links +=  `<a href='/external/species_communities/${full.id}?group_type_name=${full.group_type}'>View</a>`;
                        }
                    }

                    links +=  `<a href='/internal/species_communities/${full.id}?group_type_name=${full.group_type}'>Edit</a><br/>`; // Dummy addition for Boranaga demo

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
                    vm.column_id,
                    vm.column_number,
                    vm.column_community_id,
                    vm.column_community_name,
                    vm.column_community_status,
                    vm.column_conservation_list,
                    vm.column_conservation_category,
                    vm.column_action,
                    vm.column_workflow_status,
                    vm.column_region,
                    vm.column_district,
                ]
                search = false
                buttons = []
            }
            if(vm.is_internal){
                columns = [
                    vm.column_id,
                    vm.column_number,
                    vm.column_community_id,
                    vm.column_community_name,
                    vm.column_community_status,
                    vm.column_conservation_list,
                    vm.column_conservation_category,
                    vm.column_action,
                    vm.column_workflow_status,
                    vm.column_region,
                    vm.column_district,
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
                ajax: {
                    "url": this.url,
                    "dataSrc": 'data',

                    // adding extra GET params for Custom filtering
                    "data": function ( d ) {
                        d.filter_community_migrated_id = vm.filterCommunityMigratedId;
                        d.filter_community_name = vm.filterCommunityName;
                        d.filter_community_status = vm.filterCommunityStatus;
                        d.filter_conservation_list = vm.filterCommunityConservationList;
                        d.filter_conservation_category = vm.filterCommunityConservationCategory;
                        d.filter_group_type = vm.group_type_name;
                        d.filter_region = vm.filterCommunityRegion;
                        d.filter_district = vm.filterCommunityDistrict;
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
                      this.filterCommunityConservationCategory='all'; //-----to remove the previous selection
                    }
                    this.filtered_conservation_category_list=[];
                    //---filter conservation_categories as per cons_list selected
                    for(let choice of this.conservation_category_list){
                        if(choice.conservation_list_id.toString() === this.filterCommunityConservationList.toString())
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
                    vm.$refs.communities_datatable.vmDataTable.ajax.reload();
                }, (error) => {
                    console.log(error);
                });
            },(error) => {

            });
        },
        addEventListeners: function(){
            let vm = this;
            // External Discard listener
            vm.$refs.communities_datatable.vmDataTable.on('click', 'a[data-discard-proposal]', function(e) {
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
            vm.$refs.communities_datatable.table.dataTableExt.afnFiltering.push(
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
