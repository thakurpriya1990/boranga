<template id="species_flora_cp_dashboard">
    <div>
        <CollapsibleFilters component_title="Filters" ref="collapsible_filters" @created="collapsible_component_mounted" class="mb-2">
            <div class="row">
                <!-- <div class="col-md-3">
                    <div class="form-group">
                        <label for="cp_non_current_name_lookup">Non-current Name:</label>
                        <select
                            id="cp_non_current_name_lookup"
                            name="cp_non_current_name_lookup"
                            ref="cp_non_current_name_lookup"
                            class="form-control" />
                    </div>
                </div> -->
                <div class="col-md-3">
                    <div class="form-group">
                        <label for="">Status:</label>
                        <select class="form-select" v-model="filterCPFloraApplicationStatus">
                            <option value="all">All</option>
                            <option v-for="status in proposal_status" :value="status.value">{{ status.name }}</option>
                        </select>
                    </div>
                </div>
                <div class="col-md-3">
                    <div class="form-group">
                        <label for="cp_type">Type:</label>
                        <select
                            id="cp_type"
                            name="cp_type"
                            ref="cp_type"
                            class="form-control" />
                    </div>
                </div>
                <div class="col-md-3">
                    <div class="form-group">
                        <label for="">Region:</label>
                        <select class="form-select" v-model="filterCPFloraRegion"
                        @change="filterDistrict($event)">
                            <option value="all">All</option>
                            <option v-for="region in region_list" :value="region.id" v-bind:key="region.id">{{region.name}}</option>
                        </select>
                    </div>
                </div>
                <div class="col-md-3">
                    <div class="form-group">
                        <label for="">District:</label>
                        <select class="form-select" v-model="filterCPFloraDistrict">
                            <option value="all">All</option>
                            <option v-for="district in filtered_district_list" :value="district.id">{{district.name}}</option>
                        </select>
                    </div>
                </div>
                <!-- <div class="col-md-3">
                    <div class="form-group">
                        <label for="cp_approval_status">Approval Status:</label>
                        <select
                            id="cp_approval_status"
                            name="cp_approval_status"
                            ref="cp_approval_status"
                            class="form-control" />
                    </div>
                </div>
                <div class="col-md-3">
                    <div class="form-group">
                        <label for="cp_commonwealth_status">Commonwealth Status:</label>
                        <select
                            id="cp_commonwealth_status"
                            name="cp_commonwealth_status"
                            ref="cp_commonwealth_status"
                            class="form-control" />
                    </div>
                </div>
                <div class="col-md-3">
                    <div class="form-group">
                        <label for="cp_wa_status">Western Australia Status:</label>
                        <select
                            id="cp_wa_status"
                            name="cp_wa_status"
                            ref="cp_wa_status"
                            class="form-control" />
                    </div>
                </div> -->
                <div class="col-md-3">
                    <div class="form-group">
                        <label for="">Effective From Date:</label>
                        <input type="date" class="form-control" placeholder="DD/MM/YYYY" id="effective_from_date" v-model="filterCPFloraEffectiveFromDate">
                    </div>
                </div>
                <div class="col-md-3">
                    <div class="form-group">
                        <label for="">Effective To Date:</label>
                        <input type="date" class="form-control" placeholder="DD/MM/YYYY" id="effective_from_date" v-model="filterCPFloraEffectiveToDate">
                    </div>
                </div>
                <div class="col-md-3">
                    <div class="form-group">
                        <label for="">Review Date:</label>
                        <input type="date" class="form-control" placeholder="DD/MM/YYYY" id="review_date" v-model="filterCPFloraReviewDate">
                    </div>
                </div>
                <!-- <div class="col-md-3">
                    <div class="form-group">
                        <label for="">Review Date To:</label>
                        <input type="date" class="form-control" placeholder="DD/MM/YYYY" id="review_date_to" v-model="filterCPFloraReviewToDate">
                    </div>
                </div> -->
            </div>
        </CollapsibleFilters>

        <div v-if="addFloraCPVisibility" class="col-md-12">
            <div class="text-end">
                <button type="button" class="btn btn-primary mb-2 " @click.prevent="createFloraConservationPlan"><i class="fa-solid fa-circle-plus"></i> Add Conservation Plan</button>
            </div>
        </div>

        <div class="row">
            <div class="col-lg-12">
                <datatable
                        ref="flora_cp_datatable"
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
// require("select2/dist/css/select2.min.css");
// require("select2-bootstrap-5-theme/dist/select2-bootstrap-5-theme.min.css")
import {
    api_endpoints,
    constants,
    helpers
}from '@/utils/hooks'
export default {
    name: 'ConservationPlansFloraTable',
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
            default:0
        },
        url:{
            type: String,
            required: true
        },
        filterCPFloraType_cache: {
            type: String,
            required: false,
            default: 'filterCPFloraType',
        },
        filterCPFloraRegion_cache: {
            type: String,
            required: false,
            default: 'filterCPFloraRegion',
        },
        filterCPFloraDistrict_cache: {
            type: String,
            required: false,
            default: 'filterCPFloraDistrict',
        },
        filterCPFloraApplicationStatus_cache: {
            type: String,
            required: false,
            default: 'filterCPFloraApplicationStatus',
        },
        filterCPFloraEffectiveFromDate_cache: {
            type: String,
            required: false,
            default: 'filterCPFloraEffectiveFromDate',
        },
        filterCPFloraEffectiveToDate_cache: {
            type: String,
            required: false,
            default: 'filterCPFloraEffectiveToDate',
        },
        filterCPFloraReviewDate_cache: {
            type: String,
            required: false,
            default: 'filterCPFloraReviewDate',
        },

    },
    data() {
        let vm = this;
        return {
            datatable_id: 'species_flora_cp-datatable-'+vm._uid,

            //Profile to check if user has access to process Proposal
            profile: {},
            is_payment_admin: false,

            // selected values for filtering
            filterCPFloraType: sessionStorage.getItem(this.filterCPFloraType_cache) ?
                                    sessionStorage.getItem(this.filterCPFloraType_cache) : 'all',

            filterCPFloraRegion: sessionStorage.getItem(this.filterCPFloraRegion_cache) ?
                                    sessionStorage.getItem(this.filterCPFloraRegion_cache) : 'all',

            filterCPFloraDistrict: sessionStorage.getItem(this.filterCPFloraDistrict_cache) ?
                                    sessionStorage.getItem(this.filterCPFloraDistrict_cache) : 'all',

            filterCPFloraApplicationStatus: sessionStorage.getItem(this.filterCPFloraApplicationStatus_cache) ?
                                    sessionStorage.getItem(this.filterCPFloraApplicationStatus_cache) : 'all',

            filterCPFloraEffectiveFromDate: sessionStorage.getItem(this.filterCPFloraEffectiveFromDate_cache) ?
            sessionStorage.getItem(this.filterCPFloraEffectiveFromDate_cache) : '',

            filterCPFloraEffectiveToDate: sessionStorage.getItem(this.filterCPFloraEffectiveToDate_cache) ?
            sessionStorage.getItem(this.filterCPFloraEffectiveToDate_cache) : '',

            filterCPFloraReviewDate: sessionStorage.getItem(this.filterCPFloraReviewDate_cache) ?
            sessionStorage.getItem(this.filterCPFloraReviewDate_cache) : '',

            //Filter list for scientific name and common name
            filterRegionDistrict: {},
            region_list: [],
            district_list: [],
            filtered_district_list: [],

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
                {value: 'with_approver', name: 'With Approver'},
                {value: 'with_referral', name: 'With Referral'},
                {value: 'approved', name: 'Approved'},
                {value: 'declined', name: 'Declined'},
                {value: 'discarded', name: 'Discarded'},
                {value: 'closed', name: 'Closed'},
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
        filterCPFloraType: function(){
            let vm = this;
            vm.$refs.flora_cp_datatable.vmDataTable.ajax.reload(); // This calls ajax() backend call.
            sessionStorage.setItem(vm.filterCPFloraType_cache, vm.filterCPFloraType);
        },
        filterCPFloraRegion: function(){
            let vm = this;
            vm.$refs.flora_cp_datatable.vmDataTable.ajax.reload(); // This calls ajax() backend call.
            sessionStorage.setItem(vm.filterCPFloraRegion_cache, vm.filterCPFloraRegion);
        },
        filterCPFloraDistrict: function(){
            let vm = this;
            vm.$refs.flora_cp_datatable.vmDataTable.ajax.reload(); // This calls ajax() backend call.
            sessionStorage.setItem(vm.filterCPFloraDistrict_cache, vm.filterCPFloraDistrict);
        },
        filterCPFloraEffectiveFromDate: function(){
            let vm = this;
            vm.$refs.flora_cp_datatable.vmDataTable.ajax.reload(); // This calls ajax() backend call.
            sessionStorage.setItem(vm.filterCPFloraEffectiveFromDate_cache, vm.filterCPFloraEffectiveFromDate);
        },
        filterCPFloraEffectiveToDate: function(){
            let vm = this;
            vm.$refs.flora_cp_datatable.vmDataTable.ajax.reload(); // This calls ajax() backend call.
            sessionStorage.setItem(vm.filterCPFloraEffectiveToDate_cache, vm.filterCPFloraEffectiveToDate);
        },
        filterCPFloraApplicationStatus: function() {
            let vm = this;
            vm.$refs.flora_cp_datatable.vmDataTable.ajax.reload(); // This calls ajax() backend call.
            sessionStorage.setItem(vm.filterCPFloraApplicationStatus_cache, vm.filterCPFloraApplicationStatus);
        },
        filterCPFloraReviewDate: function(){
            let vm = this;
            vm.$refs.flora_cp_datatable.vmDataTable.ajax.reload(); // This calls ajax() backend call.
            sessionStorage.setItem(vm.filterCPFloraReviewDate_cache, vm.filterCPFloraReviewDate);
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
            if(this.filterCPFloraType === 'all' &&
                this.filterCPFloraRegion === 'all' &&
                this.filterCPFloraDistrict === 'all' &&
                this.filterCPFloraApplicationStatus === 'all' &&
                this.filterCPFloraEffectiveFromDate === '' &&
                this.filterCPFloraEffectiveToDate === '' &&
                this.filterCPFloraReviewDate === ''){
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
        addFloraCPVisibility: function() {
            let visibility = false;
            /*if (this.is_internal) {
                visibility = true;
            }*/
            visibility = true;
            return visibility;
        },
        datatable_headers: function(){
            if (this.is_external){
                // return ['Number', 'Type', 'WA Plan number',
                //    'Region', 'District', 'Effective From Date', 'Effective To Date', 'Review Due', 'Approval Status', 'Commonwealth Status', 'Western Australia Status',  'Status', 'Action']
                return ['Number', 'Type', 'WA Plan number', 'Region', 'District', 'Effective From Date', 'Effective To Date', 'Review Due', 'Status', 'Action']
            }
            if (this.is_internal){
                // return ['Number', 'Type', 'WA Plan number',
                //    'Region', 'District', 'Effective From Date', 'Effective To Date', 'Review Due', 'Approval Status', 'Commonwealth Status', 'Western Australia Status', 'Status', 'Action']
                return ['Number', 'Type', 'WA Plan number', 'Region', 'District', 'Effective From Date', 'Effective To Date', 'Review Due', 'Status', 'Action']
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
                data: "conservation_plan_number",
                orderable: true,
                searchable: true,
                visible: true,
                'render': function(data, type, full){
                    return full.conservation_plan_number
                },
                name: "conservation_plan_number",
            }
        },
        column_plan_type: function(){
            return {
                data: "plan_type",
                orderable: true,
                searchable: true,
                visible: true,
                'render': function(data, type, full){
                    return full.plan_type
                },
                name: "plan_type",
            }
        },
        column_wa_plan_number: function(){
            return {
                data: "wa_plan_number",
                orderable: true,
                searchable: true,
                visible: true,
                'render': function(data, type, full){
                    return full.wa_plan_number
                },
                name: "wa_plan_number",
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
        column_region: function(){
            return {
                data: "region",
                orderable: true,
                searchable: true, // handles by filter_queryset override method
                visible: true,
                'render': function(data, type, full){
                    if (full.region){
                        return full.region
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
                searchable: true, // handles by filter_queryset override method
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
        column_effective_from_date: function(){
            return {
                data: "effective_from_date",
                orderable: true,
                searchable: true, // handles by filter_queryset override method
                visible: true,
                'render': function(data, type, full){
                    if (full.effective_from_date){
                        return full.effective_from_date
                    }
                    // Should not reach here
                    return ''
                },
                name: "effective_from_date",
            }
        },
        column_effective_to_date: function(){
            return {
                data: "effective_to_date",
                orderable: true,
                searchable: true, // handles by filter_queryset override method
                visible: true,
                'render': function(data, type, full){
                    if (full.effective_to_date){
                        return full.effective_to_date
                    }
                    // Should not reach here
                    return ''
                },
                name: "effective_to_date",
            }
        },
        column_review_date: function(){
            return {
                data: "next_review_date",
                orderable: true,
                searchable: true, // handles by filter_queryset override method
                visible: true,
                'render': function(data, type, full){
                    if (full.next_review_date){
                        return full.next_review_date
                    }
                    // Should not reach here
                    return ''
                },
                name: "next_review_date",
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
                    if (!vm.is_external){
                        /*if(vm.check_assessor(full) && full.can_officer_process)*/
                        if(full.internal_user_edit)
                        {
                            links +=  `<a href='/internal/conservation_status/${full.id}'>Continue</a><br/>`;
                            links +=  `<a href='#${full.id}' data-discard-cs-proposal='${full.id}'>Discard</a><br/>`;
                        }
                        else{
                            if(full.assessor_process){
                                    links +=  `<a href='/internal/conservation_status/${full.id}'>Process</a><br/>`;
                            }
                            else{
                                if(full.assessor_edit){
                                    links +=  `<a href='/internal/conservation_status/${full.id}?action=edit'>Edit</a><br/>`;
                                }
                                links +=  `<a href='/internal/conservation_status/${full.id}?action=view'>View</a><br/>`;
                            }
                        }
                    }
                    return links;
                }
            }
        },
        datatable_options: function(){
            let vm = this

            let columns = []
            let search = null
            let buttons = [
                {
                    text: '<i class="fa-solid fa-download"></i> Excel',
                    className: 'btn btn-primary ml-2',
                    action: function (e, dt, node, config) {
                        vm.exportData("excel");
                    }
                },
                {
                    text: '<i class="fa-solid fa-download"></i> CSV',
                    className: 'btn btn-primary',
                    action: function (e, dt, node, config) {
                        vm.exportData("csv");
                    }
                }
            ]
            if(vm.is_external){
                columns = [
                    vm.column_number,
                    vm.column_plan_type,
                    vm.column_wa_plan_number,
                    // vm.column_species_number,
                    // vm.column_scientific_name,
                    // vm.column_common_name,
                    // vm.column_conservation_list,
                    // vm.column_conservation_category,
                    vm.column_region,
                    vm.column_district,
                    vm.column_effective_from_date,
                    vm.column_effective_to_date,
                    vm.column_next_review_date,
                    // vm.column_family,
                    // vm.column_genera,
                    vm.column_status,
                    vm.column_action,
                ]
                search = false
            }
            if(vm.is_internal){
                columns = [
                    vm.column_number,
                    vm.column_plan_type,
                    vm.column_wa_plan_number,
                    // vm.column_species_number,
                    // vm.column_scientific_name,
                    // vm.column_common_name,
                    // vm.column_conservation_list,
                    // vm.column_conservation_category,
                    vm.column_region,
                    vm.column_district,
                    vm.column_effective_from_date,
                    vm.column_effective_to_date,
                    vm.column_next_review_date,
                    // vm.column_family,
                    // vm.column_genera,
                    vm.column_status,
                    vm.column_action,
                ]
                search = true
            }

            return {
                autoWidth: false,
                language: {
                    processing: constants.DATATABLE_PROCESSING_HTML
                },
                order: [
                    [0, 'desc']
                ],
                lengthMenu: [ [10, 25, 50, 100, 100000000], [10, 25, 50, 100, "All"] ],
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
                        d.filter_group_type = vm.group_type_name;
                        d.filter_plan_type = vm.filterCPFloraType;
                        d.filter_region = vm.filterCPFloraRegion;
                        d.filter_district = vm.filterCPFloraDistrict;
                        d.filter_application_status = vm.filterCPFloraApplicationStatus;
                        d.filter_effective_from_date = vm.filterCPFloraEffectiveFromDate;
                        d.filter_effective_to_date = vm.filterCPFloraEffectiveToDate;
                        d.filter_review_date = vm.filterCPFloraReviewDate;
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
            //large FilterList of Species Values object
            vm.$http.get(api_endpoints.filter_lists_species+ '?group_type_name=' + vm.group_type_name).then((response) => {
                // vm.filterListsSpecies = response.body;
                // vm.scientific_name_list = vm.filterListsSpecies.scientific_name_list;
                // vm.common_name_list = vm.filterListsSpecies.common_name_list;
                // vm.family_list = vm.filterListsSpecies.family_list;
                // vm.genus_list = vm.filterListsSpecies.genus_list;
                // vm.conservation_list_dict = vm.filterListsSpecies.conservation_list_dict;
                // vm.conservation_category_list = vm.filterListsSpecies.conservation_category_list;
                // vm.filterConservationCategory();
                vm.filterDistrict();
                vm.proposal_status = vm.internal_status;
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
         //-------filter district dropdown dependent on region selected
         filterDistrict: function(event) {
                this.$nextTick(() => {
                    if(event){
                      this.filterCPFloraDistrict='all'; //-----to remove the previous selection
                    }
                    this.filtered_district_list=[];
                    //---filter districts as per region selected
                    for(let choice of this.district_list){
                        if(choice.region_id.toString() === this.filterCPFloraRegion.toString())
                        {
                          this.filtered_district_list.push(choice);
                        }

                    }
                });
        },
        createFloraConservationPlan: async function () {
            let newFloraCPId = null
            try {
                    const createUrl = api_endpoints.conservation_status+"/";
                    let payload = new Object();
                    payload.application_type_id = this.group_type_id
                    payload.internal_application = true
                    let savedFloraCP = await Vue.http.post(createUrl, payload);
                    if (savedFloraCP) {
                        newFloraCPId = savedFloraCP.body.id;
                    }
                }
            catch (err) {
                console.log(err);
                if (this.is_internal) {
                    return err;
                }
            }
            this.$router.push({
                name: 'internal-conservation_plan',
                params: {conservation_plan_id: newFloraCPId},
                });
        },
        discardCSProposal:function (conservation_plan_id) {
            let vm = this;
            swal({
                title: "Discard Application",
                text: "Are you sure you want to discard this proposal?",
                type: "warning",
                showCancelButton: true,
                confirmButtonText: 'Discard Application',
                confirmButtonColor:'#d9534f'
            }).then(() => {
                vm.$http.delete(api_endpoints.discard_cs_proposal(conservation_plan_id))
                .then((response) => {
                    swal(
                        'Discarded',
                        'Your proposal has been discarded',
                        'success'
                    )
                    vm.$refs.flora_cp_datatable.vmDataTable.ajax.reload();
                }, (error) => {
                    console.log(error);
                });
            },(error) => {

            });
        },
        addEventListeners: function(){
            let vm = this;
            // internal Discard listener
            vm.$refs.flora_cp_datatable.vmDataTable.on('click', 'a[data-discard-cs-proposal]', function(e) {
                e.preventDefault();
                var id = $(this).attr('data-discard-cs-proposal');
                vm.discardCSProposal(id);
            });
        },
        initialiseSearch:function(){
            this.submitterSearch();
        },
        submitterSearch:function(){
            let vm = this;
            vm.$refs.flora_cp_datatable.table.dataTableExt.afnFiltering.push(
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
        exportData: function (format) {
            let vm = this;
            const columns_new = {
                "0": {
                    "data": "conservation_status_number",
                    "name": "conservation_status__id, conservation_status__conservation_status_number",
                    "orderable": "true",
                    "search": {
                        "regex": "false",
                        "value": ""
                    },
                    "searchable": "false"
                },
                "1": {
                    "data": "species_number",
                    "name": "conservation_status__species__species_number",
                    "orderable": "true",
                    "search": {
                        "regex": "false",
                        "value": ""
                    },
                    "searchable": "true"
                },
                "2": {
                    "data": "scientific_name",
                    "name": "conservation_status__species__taxonomy__scientific_name",
                    "orderable": "true",
                    "search": {
                        "regex": "false",
                        "value": ""
                    },
                    "searchable": "true"
                },
                "3": {
                    "data": "conservation_list",
                    "name": "conservation_status__conservation_list__code",
                    "searchable": "true",
                    "orderable": "true",
                    "search": {
                        "value": "",
                        "regex": "false"
                    }
                },
                "4": {
                    "data": "conservation_category",
                    "name": "conservation_status__conservation_category__code",
                    "searchable": "true",
                    "orderable": "true",
                    "search": {
                        "value": "",
                        "regex": "false"
                    }
                },
                "5": {
                    "data": "family",
                    "name": "species__taxonomy__family__name",
                    "searchable": "true",
                    "orderable": "true",
                    "search": {
                        "value": "",
                        "regex": "false"
                    }
                },
                "6": {
                    "data": "genus",
                    "name": "species__taxonomy__genus__name",
                    "searchable": "true",
                    "orderable": "true",
                    "search": {
                        "value": "",
                        "regex": "false"
                    }
                },
                "7": {
                    "data": "processing_status",
                    "name": "conservation_status__processing_status",
                    "searchable": "true",
                    "orderable": "true",
                    "search": {
                        "value": "",
                        "regex": "false"
                    }
                },
                "8": {
                    "data": "id",
                    "name": "",
                    "searchable": "false",
                    "orderable": "false",
                    "search": {
                        "value": "",
                        "regex": "false"
                    }
                },
                "9": {
                    "data": "conservation_status",
                    "name": "",
                    "searchable": "true",
                    "orderable": "true",
                    "search": {
                        "value": "",
                        "regex": "false"
                    }
                },
                "10": {
                    "data": "district",
                    "name": "district__name",
                    "orderable": "true",
                    "search": {
                        "regex": "false",
                        "value": ""
                    },
                    "searchable": "false"
                },
                "11": {
                    "data": "region",
                    "name": "region__name",
                    "orderable": "true",
                    "search": {
                        "regex": "false",
                        "value": ""
                    },
                    "searchable": "false"
                }
            };

            const object_load = {
                columns: columns_new,
                filter_group_type: vm.group_type_name,
                filter_plan_type: vm.filterCPFloraType,
                filter_region: vm.filterCPFloraRegion,
                filter_district: vm.filterCPFloraDistrict,
                filter_application_status: vm.filterCPFloraApplicationStatus,
                filter_effective_from_date: vm.filterCPFloraEffectiveFromDate,
                filter_effective_to_date: vm.filterCPFloraEffectiveToDate,
                filter_review_date: vm.filterCPFloraReviewDate,
                is_internal: vm.is_internal,
                export_format: format
            };

            const url = api_endpoints.species_cs_internal_export;
            const keyValuePairs = [];

            for (const key in object_load) {
                if (object_load.hasOwnProperty(key)) {
                    const encodedKey = encodeURIComponent(key);
                    let encodedValue = '';

                    if (typeof object_load[key] === 'object') {
                        encodedValue = encodeURIComponent(JSON.stringify(object_load[key]));
                    }
                    else {
                        encodedValue = encodeURIComponent(object_load[key]);
                    }
                    keyValuePairs.push(`${encodedKey}=${encodedValue}`);
                }
            }
            const params = keyValuePairs.join('&');
            const fullUrl = `${url}?${params}`;
            try {
                if (format === "excel") {
                    $.ajax({
                        type: "GET",
                        url: fullUrl,
                        contentType: "application/vnd.ms-excel",
                        dataType: "binary",
                        xhrFields: {
                            responseType: 'blob'
                        },

                        success: function (response, status, request) {
                            var contentDispositionHeader = request.getResponseHeader('Content-Disposition');
                            var filename = contentDispositionHeader.split('filename=')[1];
                            window.URL = window.URL || window.webkitURL;
                            var blob = new Blob([response], { type: "application/vnd.ms-excel" });

                            var downloadUrl = window.URL.createObjectURL(blob);
                            var a = document.createElement("a");
                            a.href = downloadUrl;
                            a.download = filename;
                            document.body.appendChild(a);
                            a.click();
                            document.body.removeChild(a);
                        },
                        error: function (xhr, status, error) {
                            console.log(error);
                        },
                    });
                }
                else if (format === "csv") {
                    $.ajax({
                        type: "GET",
                        url: fullUrl,
                        success: function (response, status, request) {
                            var contentDispositionHeader = request.getResponseHeader('Content-Disposition');
                            var filename = contentDispositionHeader.split('filename=')[1];
                            window.URL = window.URL || window.webkitURL;
                            var blob = new Blob([response], { type: "text/csv" });

                            var downloadUrl = window.URL.createObjectURL(blob);
                            var a = document.createElement("a");
                            a.href = downloadUrl;
                            a.download = filename;
                            document.body.appendChild(a);
                            a.click();
                            document.body.removeChild(a);
                        },
                        error: function (xhr, status, error) {
                            console.log(error);
                        },
                    });
                }
            }
            catch (err) {
                console.log(err);
                if (vm.is_internal) {
                    return err;
                }
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

            // -- to set the select2 field with the session value if exists onload()
            // if(sessionStorage.getItem("filterCSFloraScientificName")!='all' && sessionStorage.getItem("filterCSFloraScientificName")!=null)
            // {
            //     // contructor new Option(text, value, defaultSelected, selected)
            //     var newOption = new Option(sessionStorage.getItem("filterCSFloraScientificNameText"), vm.filterCSFloraScientificName, false, true);
            //     $('#cp_scientific_name_lookup').append(newOption);
            //     //$('#scientific_name_lookup').append(newOption).trigger('change');
            // }
            // if(sessionStorage.getItem("filterCSFloraCommonName")!='all' && sessionStorage.getItem("filterCSFloraCommonName")!=null)
            // {
            //     // contructor new Option(text, value, defaultSelected, selected)
            //     var newOption = new Option(sessionStorage.getItem("filterCSFloraCommonNameText"), vm.filterCSFloraCommonName, false, true);
            //     $('#cp_non_current_name_lookup').append(newOption);
            // }
            // if(sessionStorage.getItem("filterCSFloraFamily")!='all' && sessionStorage.getItem("filterCSFloraFamily")!=null)
            // {
            //     // contructor new Option(text, value, defaultSelected, selected)
            //     var newOption = new Option(sessionStorage.getItem("filterCSFloraFamilyText"), vm.filterCSFloraFamily, false, true);
            //     $('#cs_family_lookup').append(newOption);
            // }
            // if(sessionStorage.getItem("filterCSFloraGenus")!='all' && sessionStorage.getItem("filterCSFloraGenus")!=null)
            // {
            //     // contructor new Option(text, value, defaultSelected, selected)
            //     var newOption = new Option(sessionStorage.getItem("filterCSFloraGenusText"), vm.filterCSFloraGenus, false, true);
            //     $('#cs_genera_lookup').append(newOption);
            // }
        });
    }
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
