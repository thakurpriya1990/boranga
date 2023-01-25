<template id="species_fauna_cs_dashboard">
    <div>
        <CollapsibleFilters component_title="Filters" ref="collapsible_filters" @created="collapsible_component_mounted" class="mb-2">
            <div class="row">
                <div class="col-md-3">
                    <div class="form-group">
                        <label for="">Scientific Name:</label>
                        <select class="form-select" v-model="filterCSFaunaScientificName">
                            <option value="all">All</option>
                            <option v-for="option in scientific_name_list" :value="option.id">{{option.name}}
                            </option>
                        </select>
                    </div>
                </div>
                <div class="col-md-3">
                    <div class="form-group">
                        <label for="">Common Name:</label>
                        <select class="form-select" v-model="filterCSFaunaCommonName">
                            <option value="all">All</option>
                            <option v-for="option in common_name_list" :value="option.id">{{option.name}}</option>
                        </select>
                    </div>
                </div>
                <div class="col-md-3">
                    <div class="form-group">
                        <label for="">Phylo Group:</label>
                        <select class="form-select" v-model="filterCSFaunaPhylogeneticGroup">
                            <option value="all">All</option>
                            <option v-for="option in phylogenetic_group_list" :value="option.id">
                                {{option.name}}</option>
                        </select>
                    </div>
                </div>
                <div class="col-md-3">
                    <div class="form-group">
                        <label for="">Family:</label>
                        <select class="form-select" v-model="filterCSFaunaFamily">
                            <option value="all">All</option>
                            <option v-for="option in family_list" :value="option.id">{{option.name}}</option>
                        </select>
                    </div>
                </div>
                <div class="col-md-3">
                    <div class="form-group">
                        <label for="">Genera:</label>
                        <select class="form-select" v-model="filterCSFaunaGenus">
                            <option value="all">All</option>
                            <option v-for="option in genus_list" :value="option.id">{{option.name}}</option>
                        </select>
                    </div>
                </div>
                <div class="col-md-3">
                    <div class="form-group">
                        <label for="">Conservation List:</label>
                        <select class="form-select" v-model="filterCSFaunaConservationList" 
                        @change="filterConservationCategory($event)">
                            <option value="all">All</option>
                            <option v-for="list in conservation_list_dict" :value="list.id">{{list.code}}</option>
                        </select>
                    </div>
                </div>
                <div class="col-md-3">
                    <div class="form-group">
                        <label for="">Conservation Category:</label>
                        <select class="form-select" v-model="filterCSFaunaConservationCategory">
                            <option value="all">All</option>
                            <option v-for="list in filtered_conservation_category_list" :value="list.id">{{list.code}}</option>
                        </select>
                    </div>
                </div>
                <div class="col-md-3">
                    <div class="form-group">
                        <label for="">Status:</label>
                        <select class="form-select" v-model="filterCSFaunaApplicationStatus">
                            <option value="all">All</option>
                            <option v-for="status in proposal_status" :value="status.value">{{ status.name }}</option>
                        </select>
                    </div>
                </div>
                <div class="col-md-3">
                    <div class="form-group">
                        <label for="">Region:</label>
                        <select class="form-select" v-model="filterCSFaunaRegion">
                            <option value="all">All</option>
                            <option v-for="region in region_list" :value="region.id">{{region.name}}</option>
                        </select>
                    </div>
                </div>
                <div class="col-md-3">
                    <div class="form-group">
                        <label for="">District:</label>
                        <select class="form-select" v-model="filterCSFaunaDistrict">
                            <option value="all">All</option>
                            <option v-for="district in district_list" :value="district.id">{{district.name}}</option>
                        </select>
                    </div>
                </div>
                <div class="col-md-3">
                    <div class="form-group">
                        <label for="">Effective From Date:</label>
                        <input type="date" class="form-control" placeholder="DD/MM/YYYY" id="effective_from_date" v-model="filterCSFaunaEffectiveFromDate">
                    </div>
                </div>
                <div class="col-md-3">
                    <div class="form-group">
                        <label for="">Effective To Date:</label>
                        <input type="date" class="form-control" placeholder="DD/MM/YYYY" id="effective_from_date" v-model="filterCSFaunaEffectiveToDate">
                    </div>
                </div>
            </div>
        </CollapsibleFilters>
        
        <div v-if="addFaunaCSVisibility" class="col-md-12">
            <div class="text-end">
                <button type="button" class="btn btn-primary mb-2 " @click.prevent="createFaunaConservationStatus"><i class="fa-solid fa-circle-plus"></i> Add Conservation Satus</button>
            </div>
        </div>

        <div class="row">
            <div class="col-lg-12">
                <datatable
                        ref="fauna_cs_datatable"
                        :id="datatable_id"
                        :dtOptions="datatable_options"
                        :dtHeaders="datatable_headers"
                />
            </div>
        </div>
    </div>
</template>
<script>
//require('@popperjs/core');
//import { createPopper } from '@popperjs/core';
//require('popperjs');
//require('bootstrap');
import "babel-polyfill"
import datatable from '@/utils/vue/datatable.vue'
import CollapsibleFilters from '@/components/forms/collapsible_component.vue'
import FormSection from '@/components/forms/section_toggle.vue'
import Vue from 'vue'
//require("select2/dist/css/select2.min.css");
//require("select2-bootstrap-theme/dist/select2-bootstrap.min.css");
import {
    api_endpoints,
    helpers
}from '@/utils/hooks'
export default {
    name: 'ConservationStatusFaunaTable',
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
        filterCSFaunaScientificName_cache: {
            type: String,
            required: false,
            default: 'filterCSFaunaScientificName',
        },
        filterCSFaunaCommonName_cache: {
            type: String,
            required: false,
            default: 'filterCSFaunaCommonName',
        },
        filterCSFaunaPhylogeneticGroup_cache: {
            type: String,
            required: false,
            default: 'filterCSFaunaPhylogeneticGroup',
        },
        filterCSFaunaFamily_cache: {
            type: String,
            required: false,
            default: 'filterCSFaunaFamily',
        },
        filterCSFaunaGenus_cache: {
            type: String,
            required: false,
            default: 'filterCSFaunaGenus',
        },
        filterCSFaunaConservationList_cache: {
            type: String,
            required: false,
            default: 'filterCSFaunaConservationList',
        },
        filterCSFaunaConservationCategory_cache: {
            type: String,
            required: false,
            default: 'filterCSFaunaConservationCategory',
        },
        filterCSFaunaRegion_cache: {
            type: String,
            required: false,
            default: 'filterCSFaunaRegion',
        },
        filterCSFaunaDistrict_cache: {
            type: String,
            required: false,
            default: 'filterCSFaunaDistrict',
        },
        filterCSFaunaApplicationStatus_cache: {
            type: String,
            required: false,
            default: 'filterCSFaunaApplicationStatus',
        },
        filterCSFaunaEffectiveFromDate_cache: {
            type: String,
            required: false,
            default: 'filterCSFaunaEffectiveFromDate',
        },
        filterCSFaunaEffectiveToDate_cache: {
            type: String,
            required: false,
            default: 'filterCSFaunaEffectiveToDate',
        },
    },
    data() {
        let vm = this;
        return {
            datatable_id: 'species_fauna_cs-datatable-'+vm._uid,
     
            //Profile to check if user has access to process Proposal
            profile: {},
            is_payment_admin: false,
            
            // selected values for filtering
            filterCSFaunaScientificName: sessionStorage.getItem(this.filterCSFaunaScientificName_cache) ? 
                                    sessionStorage.getItem(this.filterCSFaunaScientificName_cache) : 'all',

            filterCSFaunaCommonName: sessionStorage.getItem(this.filterCSFaunaCommonName_cache) ? 
                                    sessionStorage.getItem(this.filterCSFaunaCommonName_cache) : 'all',

            filterCSFaunaPhylogeneticGroup: sessionStorage.getItem(this.filterCSFaunaPhylogeneticGroup_cache) ? 
                                            sessionStorage.getItem(this.filterCSFaunaPhylogeneticGroup_cache) : 'all',

            filterCSFaunaFamily: sessionStorage.getItem(this.filterCSFaunaFamily_cache) ? 
                                sessionStorage.getItem(this.filterCSFaunaFamily_cache) : 'all',

            filterCSFaunaGenus: sessionStorage.getItem(this.filterCSFaunaGenus_cache) ? 
                                sessionStorage.getItem(this.filterCSFaunaGenus_cache) : 'all',

            filterCSFaunaConservationList: sessionStorage.getItem(this.filterCSFaunaConservationList_cache) ? 
                                    sessionStorage.getItem(this.filterCSFaunaConservationList_cache) : 'all',

            filterCSFaunaConservationCategory: sessionStorage.getItem(this.filterCSFaunaConservationCategory_cache) ? 
                                    sessionStorage.getItem(this.filterCSFaunaConservationCategory_cache) : 'all',

            filterCSFaunaRegion: sessionStorage.getItem(this.filterCSFaunaRegion_cache) ? 
                                    sessionStorage.getItem(this.filterCSFaunaRegion_cache) : 'all',

            filterCSFaunaDistrict: sessionStorage.getItem(this.filterCSFaunaDistrict_cache) ? 
                                    sessionStorage.getItem(this.filterCSFaunaDistrict_cache) : 'all',

            filterCSFaunaApplicationStatus: sessionStorage.getItem(this.filterCSFaunaApplicationStatus_cache) ?
                                    sessionStorage.getItem(this.filterCSFaunaApplicationStatus_cache) : 'all',

            filterCSFaunaEffectiveFromDate: sessionStorage.getItem(this.filterCSFaunaEffectiveFromDate_cache) ?
            sessionStorage.getItem(this.filterCSFaunaEffectiveFromDate_cache) : '',

            filterCSFaunaEffectiveToDate: sessionStorage.getItem(this.filterCSFaunaEffectiveToDate_cache) ?
            sessionStorage.getItem(this.filterCSFaunaEffectiveToDate_cache) : '',

            //Filter list for scientific name and common name
            filterListsSpecies: {},
            scientific_name_list: [],
            common_name_list: [],
            family_list: [],
            genus_list: [],
            phylogenetic_group_list: [],
            conservation_list_dict: [],
            filtered_conservation_category_list: [],
            conservation_category_list: [],
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
                {value: 'with_approver', name: 'With Approver'},
                {value: 'with_referral', name: 'With Referral'},
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
        filterCSFaunaScientificName: function(){
            let vm = this;
            vm.$refs.fauna_cs_datatable.vmDataTable.ajax.reload(); // This calls ajax() backend call.
            sessionStorage.setItem(vm.filterCSFaunaScientificName_cache, vm.filterCSFaunaScientificName);  
        },
        filterCSFaunaCommonName: function() {
            let vm = this;
            vm.$refs.fauna_cs_datatable.vmDataTable.ajax.reload(); // This calls ajax() backend call.
            sessionStorage.setItem(vm.filterCSFaunaCommonName_cache, vm.filterCSFaunaCommonName);  
        },
        filterCSFaunaPhylogeneticGroup: function() {
            let vm = this;
            vm.$refs.fauna_cs_datatable.vmDataTable.ajax.reload(); // This calls ajax() backend call. 
            sessionStorage.setItem(vm.filterCSFaunaPhylogeneticGroup_cache, vm.filterCSFaunaPhylogeneticGroup);
        },
        filterCSFaunaFamily: function() {
            let vm = this;
            vm.$refs.fauna_cs_datatable.vmDataTable.ajax.reload(); // This calls ajax() backend call.
            sessionStorage.setItem(vm.filterCSFaunaFamily_cache, vm.filterCSFaunaFamily);  
        },
        filterCSFaunaGenus: function() {
            let vm = this;
            vm.$refs.fauna_cs_datatable.vmDataTable.ajax.reload(); // This calls ajax() backend call.
            sessionStorage.setItem(vm.filterCSFaunaGenus_cache, vm.filterCSFaunaGenus);  
        },
        filterCSFaunaConservationList: function() {
            let vm = this;
            vm.$refs.fauna_cs_datatable.vmDataTable.ajax.reload(); // This calls ajax() backend call.  
            sessionStorage.setItem(vm.filterCSFaunaConservationList_cache, vm.filterCSFaunaConservationList);
        },
        filterCSFaunaConservationCategory: function() {
            let vm = this;
            vm.$refs.fauna_cs_datatable.vmDataTable.ajax.reload(); // This calls ajax() backend call.  
            sessionStorage.setItem(vm.filterCSFaunaConservationCategory_cache, vm.filterCSFaunaConservationCategory);
        },
        filterCSFaunaRegion: function(){
            let vm = this;
            vm.$refs.fauna_cs_datatable.vmDataTable.ajax.reload(); // This calls ajax() backend call.
            sessionStorage.setItem(vm.filterCSFaunaRegion_cache, vm.filterCSFaunaRegion);
        },
        filterCSFaunaDistrict: function(){
            let vm = this;
            vm.$refs.fauna_cs_datatable.vmDataTable.ajax.reload(); // This calls ajax() backend call.
            sessionStorage.setItem(vm.filterCSFaunaDistrict_cache, vm.filterCSFaunaDistrict);
        },
        filterCSFaunaEffectiveFromDate: function(){
            let vm = this;
            vm.$refs.fauna_cs_datatable.vmDataTable.ajax.reload(); // This calls ajax() backend call.
            sessionStorage.setItem(vm.filterCSFaunaEffectiveFromDate_cache, vm.filterCSFaunaEffectiveFromDate);
        },
        filterCSFaunaEffectiveToDate: function(){
            let vm = this;
            vm.$refs.fauna_cs_datatable.vmDataTable.ajax.reload(); // This calls ajax() backend call.
            sessionStorage.setItem(vm.filterCSFaunaEffectiveToDate_cache, vm.filterCSFaunaEffectiveToDate);
        },
        filterCSFaunaApplicationStatus: function() {
            let vm = this;
            vm.$refs.fauna_cs_datatable.vmDataTable.ajax.reload(); // This calls ajax() backend call.  
            sessionStorage.setItem(vm.filterCSFaunaApplicationStatus_cache, vm.filterCSFaunaApplicationStatus);
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
            if(this.filterCSFaunaScientificName === 'all' && 
                this.filterCSFaunaCommonName === 'all' && 
                this.filterCSFaunaPhylogeneticGroup === 'all' && 
                this.filterCSFaunaFamily === 'all' && 
                this.filterCSFaunaGenus === 'all' && 
                this.filterCSFaunaConservationList === 'all' && 
                this.filterCSFaunaConservationCategory === 'all' && 
                this.filterCSFaunaRegion === 'all' && 
                this.filterCSFaunaDistrict === 'all' && 
                this.filterCSFaunaApplicationStatus === 'all' &&
                this.filterCSFaunaEffectiveFromDate === '' &&
                this.filterCSFaunaEffectiveToDate === ''){
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
        addFaunaCSVisibility: function() {
            let visibility = false;
            if (this.is_internal) {
                visibility = true;
            }
            return visibility;
        },
        datatable_headers: function(){
            if (this.is_external){
                return ['Number','Species','Scientific Name', 'Common Name', 'Conservation List', 
                    'Conservation Category', 'Region', 'District', 'Effective From Date', 'Effective To Date', 'Status', 'Action']
            }
            if (this.is_internal){
                return ['Number','Species','Scientific Name', 'Common Name','Conservation List', 
                    'Conservation Category', 'Region', 'District', 'Effective From Date', 'Effective To Date', 'Status', 'Action']
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
        column_species_number: function(){
            return {
                data: "species_number",
                orderable: true,
                searchable: true,
                visible: true,
                'render': function(data, type, full){
                    return full.species_number
                },
                name: "species__species_number",
            }
        },
        column_scientific_name: function(){
            return {
                data: "scientific_name",
                orderable: true,
                searchable: true,
                visible: true,
                'render': function(value, type){
                    let result = helpers.dtPopover(value, 30, 'hover');
                    return type=='export' ? value : result;
                },
                name: "species__taxonomy__scientific_name",
            }
        },
        column_common_name: function(){
            return {
                data: "common_name",
                orderable: true,
                searchable: true,
                visible: true,
                'render': function(value, type){
                    let result = helpers.dtPopover(value, 30, 'hover');
                    return type=='export' ? value : result;
                },
                //'createdCell': helpers.dtPopoverCellFn,
                name: "species__taxonomy__vernaculars__vernacular_name",
            }
        },
        /*column_family: function(){
            return {
                data: "family",
                orderable: true,
                searchable: true,
                visible: true,
                'render': function(value, type){
                    let result = helpers.dtPopover(value, 30, 'hover');
                    return type=='export' ? value : result;
                },
                //'createdCell': helpers.dtPopoverCellFn,
                name: "species__taxonomy__family__name",
            }
        },
        column_genera: function(){
            return {
                data: "genus",
                orderable: true,
                searchable: true,
                visible: true,
                'render': function(value, type){
                    let result = helpers.dtPopover(value, 30, 'hover');
                    return type=='export' ? value : result;
                },
                //'createdCell': helpers.dtPopoverCellFn,
                name: "species__taxonomy__genus__name",
            }
        },*/
        column_conservation_list: function(){
            return {
                data: "conservation_list",
                orderable: true,
                searchable: true,
                visible: true,
                'render': function(data, type, full){
                    if(full.conservation_list){
                        return full.conservation_list;
                    }
                    // Should not reach here
                    return ''
                },
                name: "conservation_list__code",
            }
        },
        column_conservation_category: function(){
            return {
                data: "conservation_category",
                orderable: true,
                searchable: true,
                visible: true,
                'render': function(data, type, full){
                    if(full.conservation_category){
                        return full.conservation_category;
                    }
                    // Should not reach here
                    return ''
                },
                name: "conservation_category__code",
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
                searchable: false, // handles by filter_queryset override method
                visible: true,
                'render': function(data, type, full){
                    if (full.region){
                        return full.region
                    }
                    // Should not reach here
                    return ''
                },
                name: "species__region__name",
            }
        },
        column_district: function(){
            return {
                data: "district",
                orderable: true,
                searchable: false, // handles by filter_queryset override method
                visible: true,
                'render': function(data, type, full){
                    if (full.district){
                        return full.district
                    }
                    // Should not reach here
                    return ''
                },
                name: "species__district__name",
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
                name: "conservationstatusissuanceapprovaldetails__effective_from_date",
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
                name: "conservationstatusissuanceapprovaldetails__effective_to_date",
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
            let buttons = []
            if(vm.is_external){
                columns = [
                    vm.column_number,
                    vm.column_species_number,
                    vm.column_scientific_name,
                    vm.column_common_name,
                    /*vm.column_family,
                    vm.column_genera,*/
                    vm.column_conservation_list,
                    vm.column_conservation_category,
                    vm.column_region,
                    vm.column_district,
                    vm.column_effective_from_date,
                    vm.column_effective_to_date,
                    vm.column_status,
                    vm.column_action,
                ]
                search = false
                buttons = []
            }
            if(vm.is_internal){
                columns = [
                    vm.column_number,
                    vm.column_species_number,
                    vm.column_scientific_name,
                    vm.column_common_name,
                    /*vm.column_family,
                    vm.column_genera,*/
                    vm.column_conservation_list,
                    vm.column_conservation_category,
                    vm.column_region,
                    vm.column_district,
                    vm.column_effective_from_date,
                    vm.column_effective_to_date,
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
                        d.filter_group_type = vm.group_type_name;
                        d.filter_scientific_name = vm.filterCSFaunaScientificName;
                        d.filter_common_name = vm.filterCSFaunaCommonName;
                        d.filter_phylogenetic_group = vm.filterCSFaunaPhylogeneticGroup;
                        d.filter_family = vm.filterCSFaunaFamily;
                        d.filter_genus = vm.filterCSFaunaGenus;
                        d.filter_conservation_list = vm.filterCSFaunaConservationList;
                        d.filter_conservation_category = vm.filterCSFaunaConservationCategory;
                        d.filter_region = vm.filterCSFaunaRegion;
                        d.filter_district = vm.filterCSFaunaDistrict;
                        d.filter_application_status = vm.filterCSFaunaApplicationStatus;
                        d.filter_effective_from_date = vm.filterCSFaunaEffectiveFromDate;
                        d.filter_effective_to_date = vm.filterCSFaunaEffectiveToDate;
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
                vm.filterListsSpecies = response.body;
                vm.scientific_name_list = vm.filterListsSpecies.scientific_name_list;
                vm.common_name_list = vm.filterListsSpecies.common_name_list;
                vm.family_list = vm.filterListsSpecies.family_list;
                vm.genus_list = vm.filterListsSpecies.genus_list;
                vm.phylogenetic_group_list = vm.filterListsSpecies.phylogenetic_group_list;
                vm.conservation_list_dict = vm.filterListsSpecies.conservation_list_dict;
                vm.conservation_category_list = vm.filterListsSpecies.conservation_category_list;
                vm.filterConservationCategory();
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
        //-------filter category dropdown dependent on conservation_list selected
        filterConservationCategory: function(event) {
                //this.$nextTick(() => {
                    if(event){
                      this.filterCSFaunaConservationCategory='all'; //-----to remove the previous selection
                    }
                    this.filtered_conservation_category_list=[];
                    //---filter conservation_categories as per cons_list selected
                    for(let choice of this.conservation_category_list){
                        if(choice.conservation_list_id.toString() === this.filterCSFaunaConservationList.toString())
                        {
                          this.filtered_conservation_category_list.push(choice);
                        }
                    }
                //});
        },
        createFaunaConservationStatus: async function () {
            let newFaunaCSId = null
            try {
                    const createUrl = api_endpoints.conservation_status+"/";
                    let payload = new Object();
                    payload.application_type_id = this.group_type_id
                    payload.internal_application = true
                    let savedFaunaCS = await Vue.http.post(createUrl, payload);
                    if (savedFaunaCS) {
                        newFaunaCSId = savedFaunaCS.body.id;
                    }
                }
            catch (err) {
                console.log(err);
                if (this.is_internal) {
                    return err;
                }
            }
            this.$router.push({
                name: 'internal-conservation_status',
                params: {conservation_status_id: newFaunaCSId},
                });
        },
        discardCSProposal:function (conservation_status_id) {
            let vm = this;
            swal({
                title: "Discard Application",
                text: "Are you sure you want to discard this proposal?",
                type: "warning",
                showCancelButton: true,
                confirmButtonText: 'Discard Application',
                confirmButtonColor:'#d9534f'
            }).then(() => {
                vm.$http.delete(api_endpoints.discard_cs_proposal(conservation_status_id))
                .then((response) => {
                    swal(
                        'Discarded',
                        'Your proposal has been discarded',
                        'success'
                    )
                    vm.$refs.fauna_cs_datatable.vmDataTable.ajax.reload();
                }, (error) => {
                    console.log(error);
                });
            },(error) => {

            });
        },
        addEventListeners: function(){
            let vm = this;
            // External Discard listener
            vm.$refs.fauna_cs_datatable.vmDataTable.on('click', 'a[data-discard-cs-proposal]', function(e) {
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
            vm.$refs.fauna_cs_datatable.table.dataTableExt.afnFiltering.push(
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
