<template id="species_flora_dashboard">
    <div>
        <CollapsibleFilters component_title="Filters" ref="collapsible_filters" @created="collapsible_component_mounted" class="mb-2">
            <div class="row">
                <div class="col-md-3">
                    <div class="form-group">
                        <label for="">Scientific Name:</label>
                        <select class="form-select" v-model="filterFloraScientificName">
                            <option value="all">All</option>
                            <option v-for="option in scientific_name_list" :value="option.name">{{option.name}}
                            </option>
                        </select>
                    </div>
                </div>
                <div class="col-md-3">
                    <div class="form-group">
                        <label for="">Common Name:</label>
                        <select class="form-select" v-model="filterFloraCommonName">
                            <option value="all">All</option>
                            <option v-for="option in common_name_list" :value="option.id">{{option.name}}</option>
                        </select>
                    </div>
                </div>
                <div class="col-md-3">
                    <div class="form-group">
                        <label for="">Phylo Group:</label>
                        <select class="form-select" v-model="filterFloraPhylogeneticGroup">
                            <option value="all">All</option>
                            <option v-for="option in phylogenetic_group_list" :value="option.id">
                                {{option.name}}</option>
                        </select>
                    </div>
                </div>
                <div class="col-md-3">
                    <div class="form-group">
                        <label for="">Family:</label>
                        <select class="form-select" v-model="filterFloraFamily">
                            <option value="all">All</option>
                            <option v-for="option in family_list" :value="option.id">{{option.name}}</option>
                        </select>
                    </div>
                </div>
                <div class="col-md-3">
                    <div class="form-group">
                        <label for="">Genera:</label>
                        <select class="form-select" v-model="filterFloraGenus">
                            <option value="all">All</option>
                            <option v-for="option in genus_list" :value="option.id">{{option.name}}</option>
                        </select>
                    </div>
                </div>
                <div class="col-md-3">
                    <div class="form-group">
                        <label for="">Conservation List:</label>
                        <select class="form-select" v-model="filterFloraConservationList" 
                        @change="filterConservationCategory($event)">
                            <option value="all">All</option>
                            <option v-for="list in conservation_list_dict" :value="list.id" v-bind:key="list.id">{{list.code}}</option>
                        </select>
                    </div>
                </div>
                <div class="col-md-3">
                    <div class="form-group">
                        <label for="">Conservation Category:</label>
                        <select class="form-select" v-model="filterFloraConservationCategory">
                            <option value="all">All</option>
                            <option v-for="list in filtered_conservation_category_list" :value="list.id" v-bind:key="list.id">{{list.code}}</option>
                        </select>
                    </div>
                </div>
                <div class="col-md-3">
                    <div class="form-group">
                        <label for="">Status:</label>
                        <select class="form-select" v-model="filterFloraApplicationStatus">
                            <option value="all">All</option>
                            <option v-for="status in proposal_status" :value="status.value">{{ status.name }}</option>
                        </select>
                    </div>
                </div>
                <div class="col-md-3">
                    <div class="form-group">
                        <label for="">Region:</label>
                        <select class="form-select" v-model="filterFloraRegion">
                            <option value="all">All</option>
                            <option v-for="region in region_list" :value="region.id">{{region.name}}</option>
                        </select>
                    </div>
                </div>
                <div class="col-md-3">
                    <div class="form-group">
                        <label for="">District:</label>
                        <select class="form-select" v-model="filterFloraDistrict">
                            <option value="all">All</option>
                            <option v-for="district in district_list" :value="district.id">{{district.name}}</option>
                        </select>
                    </div>
                </div>
            </div>
        </CollapsibleFilters>

        <div v-if="newFloraVisibility" class="col-md-12">
            <div class="text-end">
                <button type="button" class="btn btn-primary mb-2 " @click.prevent="createFlora"><i class="fa-solid fa-circle-plus"></i> New Flora </button>
            </div>
        </div>

        <div class="row">
            <div class="col-lg-12">
                <datatable
                        ref="flora_datatable"
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
    name: 'SpeciesFloraTable',
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
        filterFloraScientificName_cache: {
            type: String,
            required: false,
            default: 'filterFloraScientificName',
        },
        filterFloraCommonName_cache: {
            type: String,
            required: false,
            default: 'filterFloraCommonName',
        },
        filterFloraFamily_cache: {
            type: String,
            required: false,
            default: 'filterFloraFamily',
        },
        filterFloraPhylogeneticGroup_cache: {
            type: String,
            required: false,
            default: 'filterFloraPhylogeneticGroup',
        },
        filterFloraGenus_cache: {
            type: String,
            required: false,
            default: 'filterFloraGenus',
        },
        filterFloraConservationList_cache: {
            type: String,
            required: false,
            default: 'filterFloraConservationList',
        },
        filterFloraConservationCategory_cache: {
            type: String,
            required: false,
            default: 'filterFloraConservationCategory',
        },
        filterFloraApplicationStatus_cache: {
            type: String,
            required: false,
            default: 'filterFloraApplicationStatus',
        },
        filterFloraRegion_cache: {
            type: String,
            required: false,
            default: 'filterFloraRegion',
        },
        filterFloraDistrict_cache: {
            type: String,
            required: false,
            default: 'filterFloraDistrict',
        },
    },
    data() {
        let vm = this;
        return {
            datatable_id: 'species_flora-datatable-'+vm._uid,
     
            //Profile to check if user has access to process Proposal
            profile: {},
            is_payment_admin: false,
            
            // selected values for filtering
            filterFloraScientificName: sessionStorage.getItem(this.filterFloraScientificName_cache) ? 
                                    sessionStorage.getItem(this.filterFloraScientificName_cache) : 'all',

            filterFloraCommonName: sessionStorage.getItem(this.filterFloraCommonName_cache) ? 
                                    sessionStorage.getItem(this.filterFloraCommonName_cache) : 'all',

            filterFloraFamily: sessionStorage.getItem(this.filterFloraFamily_cache) ? 
                                sessionStorage.getItem(this.filterFloraFamily_cache) : 'all',

            filterFloraPhylogeneticGroup: sessionStorage.getItem(this.filterFloraPhylogeneticGroup_cache) ? 
                                            sessionStorage.getItem(this.filterFloraPhylogeneticGroup_cache) : 'all',

            filterFloraGenus: sessionStorage.getItem(this.filterFloraGenus_cache) ? 
                                sessionStorage.getItem(this.filterFloraGenus_cache) : 'all',

            filterFloraConservationList: sessionStorage.getItem(this.filterFloraConservationList_cache) ? 
                                    sessionStorage.getItem(this.filterFloraConservationList_cache) : 'all',

            filterFloraConservationCategory: sessionStorage.getItem(this.filterFloraConservationCategory_cache) ? 
                                    sessionStorage.getItem(this.filterFloraConservationCategory_cache) : 'all',
            
            filterFloraApplicationStatus: sessionStorage.getItem(this.filterFloraApplicationStatus_cache) ?
            sessionStorage.getItem(this.filterFloraApplicationStatus_cache) : 'all',

            filterFloraRegion: sessionStorage.getItem(this.filterFloraRegion_cache) ? 
                                    sessionStorage.getItem(this.filterFloraRegion_cache) : 'all',

            filterFloraDistrict: sessionStorage.getItem(this.filterFloraDistrict_cache) ? 
                                    sessionStorage.getItem(this.filterFloraDistrict_cache) : 'all',

            //Filter list for scientific name and common name
            filterListsSpecies: {},
            scientific_name_list: [],
            common_name_list: [],
            family_list: [],
            phylogenetic_group_list: [],
            genus_list: [],
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
                {value: 'with_referral', name: 'With Referral'},
                {value: 'with_approver', name: 'With Approver'},
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
        filterFloraScientificName: function(){
            let vm = this;
            vm.$refs.flora_datatable.vmDataTable.ajax.reload(); // This calls ajax() backend call.
            sessionStorage.setItem(vm.filterFloraScientificName_cache, vm.filterFloraScientificName);  
        },
        filterFloraCommonName: function() {
            let vm = this;
            vm.$refs.flora_datatable.vmDataTable.ajax.reload(); // This calls ajax() backend call.
            sessionStorage.setItem(vm.filterFloraCommonName_cache, vm.filterFloraCommonName);  
        },
        filterFloraFamily: function() {
            let vm = this;
            vm.$refs.flora_datatable.vmDataTable.ajax.reload(); // This calls ajax() backend call.
            sessionStorage.setItem(vm.filterFloraFamily_cache, vm.filterFloraFamily);  
        },
        filterFloraPhylogeneticGroup: function() {
            let vm = this;
            vm.$refs.flora_datatable.vmDataTable.ajax.reload(); // This calls ajax() backend call. 
            sessionStorage.setItem(vm.filterFloraPhylogeneticGroup_cache, vm.filterFloraPhylogeneticGroup);
        },
        filterFloraGenus: function() {
            let vm = this;
            vm.$refs.flora_datatable.vmDataTable.ajax.reload(); // This calls ajax() backend call.
            sessionStorage.setItem(vm.filterFloraGenus_cache, vm.filterFloraGenus);  
        },
        filterFloraConservationList: function() {
            let vm = this;
            vm.$refs.flora_datatable.vmDataTable.ajax.reload(); // This calls ajax() backend call.  
            sessionStorage.setItem(vm.filterFloraConservationList_cache, vm.filterFloraConservationList);
        },
        filterFloraConservationCategory: function() {
            let vm = this;
            vm.$refs.flora_datatable.vmDataTable.ajax.reload(); // This calls ajax() backend call.  
            sessionStorage.setItem(vm.filterFloraConservationCategory_cache, vm.filterFloraConservationCategory);
        },
        filterFloraApplicationStatus: function() {
            let vm = this;
            vm.$refs.flora_datatable.vmDataTable.ajax.reload(); // This calls ajax() backend call.  
            sessionStorage.setItem(vm.filterFloraApplicationStatus_cache, vm.filterFloraApplicationStatus);
        },
        filterFloraRegion: function(){
            let vm = this;
            vm.$refs.flora_datatable.vmDataTable.ajax.reload(); // This calls ajax() backend call.
            sessionStorage.setItem(vm.filterFloraRegion_cache, vm.filterFloraRegion);
        },
        filterFloraDistrict: function(){
            let vm = this;
            vm.$refs.flora_datatable.vmDataTable.ajax.reload(); // This calls ajax() backend call.
            sessionStorage.setItem(vm.filterFloraDistrict_cache, vm.filterFloraDistrict);
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
            if(this.filterFloraScientificName === 'all' && 
                this.filterFloraCommonName === 'all' && 
                this.filterFloraFamily === 'all' && 
                this.filterFloraPhylogeneticGroup === 'all' && 
                this.filterFloraGenus === 'all' && 
                this.filterFloraConservationList === 'all' && 
                this.filterFloraConservationCategory === 'all' && 
                this.filterFloraApplicationStatus === 'all' &&
                this.filterFloraRegion === 'all' && 
                this.filterFloraDistrict === 'all'){
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
        newFloraVisibility: function() {
            let visibility = false;
            if (this.is_internal) {
                visibility = true;
            }
            return visibility;
        },
        datatable_headers: function(){
            if (this.is_external){
                return ['Id','Number', 'Scientific Name', 'Common Name', 'Phylo Group', 'Family', 'Genera',
                     'Conservation List', 'Conservation Category', 'Region', 'District', 'Status', 'Action']
            }
            if (this.is_internal){
                return ['Id','Number', 'Scientific Name', 'Common Name', 'Phylo Group', 'Family', 'Genera',
                    'Conservation List', 'Conservation Category', 'Region', 'District', 'Status', 'Action']
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
                data: "species_number",
                orderable: true,
                searchable: true,
                visible: true,
                'render': function(data, type, full){
                    return full.species_number
                },
                name: "id",
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
//                        var ellipsis = '...',
//                                truncated = _.truncate(value, {
//                                    length: 25,
//                                    omission: ellipsis,
//                                    separator: ' '
//                                }),
//                                result = '<span>' + truncated + '</span>',
//                                popTemplate = _.template('<a href="#" ' +
//                                    'role="button" ' +
//                                    'data-bs-toggle="popover" ' +
//                                    'data-bs-trigger="focus" ' +
//                                    'data-bs-placement="top"' +
//                                    'data-bs-html="true" ' +
//                                    'data-bs-content="<%= text %>" ' +
//                                    '>more</a>');
//                            if (_.endsWith(truncated, ellipsis)) {
//                                result += popTemplate({
//                                    text: value
//                                });
//                            }
//                            return result;
//                            //return type=='export' ? value : result;
                },
                //'createdCell': helpers.dtPopoverCellFn,
                name: "taxonomy__scientific_name",
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
                name: "taxonomy__vernaculars__vernacular_name",
            }
        },
        column_family: function(){
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
                name: "taxonomy__family_fk__scientific_name",
            }
        },
        column_phylogenetic_group: function(){
            return {
                data: "phylogenetic_group",
                orderable: true,
                searchable: true,
                visible: true,
                'render': function(value, type){
                    let result = helpers.dtPopover(value, 30, 'hover');
                    return type=='export' ? value : result;
                },
                //'createdCell': helpers.dtPopoverCellFn,
                name: "taxonomy__phylogenetic_group__name",
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
                name: "taxonomy__genus__name",
            }
        },
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
                name: "conservation_status__conservation_list__code",
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
                name: "conservation_status__conservation_category__code",
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
                name: "region__name",
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
                name: "district__name",
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
                        if (full.can_user_edit) {
                            links +=  `<a href='/internal/species_communities/${full.id}?group_type_name=${full.group_type}'>Continue</a><br/>`;
                            links +=  `<a href='#${full.id}' data-discard-species-proposal='${full.id}?group_type_name=${full.group_type}'>Discard</a><br/>`;
                        }
                        else{
                            if(full.user_process){   

                                links +=  `<a href='/internal/species_communities/${full.id}?group_type_name=${full.group_type}&action=edit'>Edit</a><br/>`;    
                            }
                            links +=  `<a href='/internal/species_communities/${full.id}?group_type_name=${full.group_type}&action=view'>View</a><br/>`;
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
                    vm.column_id,
                    vm.column_number,
                    vm.column_scientific_name,
                    vm.column_common_name,
                    vm.column_phylogenetic_group,
                    vm.column_family,
                    vm.column_genera,
                    vm.column_conservation_list,
                    vm.column_conservation_category,
                    vm.column_region,
                    vm.column_district,
                    vm.column_status,
                    vm.column_action,
                ]
                search = false
                buttons = []
            }
            if(vm.is_internal){
                columns = [
                    vm.column_id,
                    vm.column_number,
                    vm.column_scientific_name,
                    vm.column_common_name,
                    vm.column_phylogenetic_group,
                    vm.column_family,
                    vm.column_genera,
                    vm.column_conservation_list,
                    vm.column_conservation_category,
                    vm.column_region,
                    vm.column_district,
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
                //  to show the "Action" column always in the last position
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
                        d.filter_scientific_name = vm.filterFloraScientificName;
                        d.filter_common_name = vm.filterFloraCommonName;
                        d.filter_family = vm.filterFloraFamily;
                        d.filter_phylogenetic_group = vm.filterFloraPhylogeneticGroup;
                        d.filter_genus = vm.filterFloraGenus;
                        d.filter_conservation_list = vm.filterFloraConservationList;
                        d.filter_conservation_category = vm.filterFloraConservationCategory;
                        d.filter_application_status = vm.filterFloraApplicationStatus;
                        d.filter_region = vm.filterFloraRegion;
                        d.filter_district = vm.filterFloraDistrict;
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
                vm.phylogenetic_group_list = vm.filterListsSpecies.phylogenetic_group_list;
                vm.genus_list = vm.filterListsSpecies.genus_list;
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
                this.$nextTick(() => {
                    if(event){
                      this.filterFloraConservationCategory='all'; //-----to remove the previous selection
                    }
                    this.filtered_conservation_category_list=[];
                    //---filter conservation_categories as per cons_list selected
                    for(let choice of this.conservation_category_list){
                        if(choice.conservation_list_id.toString() === this.filterFloraConservationList.toString())
                        {
                          this.filtered_conservation_category_list.push(choice);
                        }
                    }
                });
        },
        createFlora: async function () {
            let newFloraId = null
            try {
                    const createUrl = api_endpoints.species+"/";
                    let payload = new Object();
                    payload.group_type_id = this.group_type_id
                    let savedFlora = await Vue.http.post(createUrl, payload);
                    if (savedFlora) {
                        newFloraId = savedFlora.body.id;
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
                params: {species_community_id: newFloraId},
                query: {group_type_name: this.group_type_name},
                });
        },
        discardSpeciesProposal:function (species_id) {
            let vm = this;
            swal({
                title: "Discard Application",
                text: "Are you sure you want to discard this proposal?",
                type: "warning",
                showCancelButton: true,
                confirmButtonText: 'Discard Application',
                confirmButtonColor:'#d9534f'
            }).then(() => {
                vm.$http.delete(api_endpoints.discard_species_proposal(species_id))
                .then((response) => {
                    swal(
                        'Discarded',
                        'Your proposal has been discarded',
                        'success'
                    )
                    vm.$refs.flora_datatable.vmDataTable.ajax.reload();
                }, (error) => {
                    console.log(error);
                });
            },(error) => {

            });
        },
        addEventListeners: function(){
            let vm = this;
            // External Discard listener
            vm.$refs.flora_datatable.vmDataTable.on('click', 'a[data-discard-species-proposal]', function(e) {
                e.preventDefault();
                var id = $(this).attr('data-discard-species-proposal');
                vm.discardSpeciesProposal(id);
            });
        },
        initialiseSearch:function(){
            this.submitterSearch();
        },
        submitterSearch:function(){
            let vm = this;
            vm.$refs.flora_datatable.table.dataTableExt.afnFiltering.push(
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
        let vm = this;
        vm.fetchFilterLists();
        vm.fetchProfile();
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
