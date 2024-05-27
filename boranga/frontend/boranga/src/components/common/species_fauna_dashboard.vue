<template id="species_fauna_dashboard">
    <div>
        <CollapsibleFilters component_title="Filters" ref="collapsible_filters" @created="collapsible_component_mounted" class="mb-2">
            <div class="row">
                <div class="col-md-3">
                    <div class="form-group">
                        <label for="scientific_name_lookup">Scientific Name:</label>
                        <select
                            id="scientific_name_lookup"
                            name="scientific_name_lookup"
                            ref="scientific_name_lookup"
                            class="form-control" />
                    </div>
                </div>
                <div class="col-md-3">
                    <div class="form-group">
                        <label for="common_name_lookup">Common Name:</label>
                        <select
                            id="common_name_lookup"
                            name="common_name_lookup"
                            ref="common_name_lookup"
                            class="form-control" />
                    </div>
                </div>
                <div class="col-md-3">
                    <div class="form-group">
                        <label for="phylo_group_lookup">Phylo Group:</label>
                        <select
                            id="phylo_group_lookup"
                            name="phylo_group_lookup"
                            ref="phylo_group_lookup"
                            class="form-control" />
                    </div>
                </div>
                <div class="col-md-3">
                    <div class="form-group">
                        <label for="family_lookup">Family:</label>
                        <select
                            id="family_lookup"
                            name="family_lookup"
                            ref="family_lookup"
                            class="form-control" />
                    </div>
                </div>
                <div class="col-md-3">
                    <div class="form-group">
                        <label for="genera_lookup">Genera:</label>
                        <select
                            id="genera_lookup"
                            name="genera_lookup"
                            ref="genera_lookup"
                            class="form-control" />
                    </div>
                </div>
                <div class="col-md-3">
                    <div class="form-group">
                        <label for="">Name Status:</label>
                        <select class="form-select" v-model="filterFaunaNameStatus">
                            <option value="all">All</option>
                            <option value="True">Current</option>
                            <option value="False">Non Current</option>
                        </select>
                    </div>
                </div>
                <div class="col-md-3">
                    <div class="form-group">
                        <label for="">Status:</label>
                        <select class="form-select" v-model="filterFaunaApplicationStatus">
                            <option value="all">All</option>
                            <option v-for="status in species_status" :value="status.value">{{ status.name }}</option>
                        </select>
                    </div>
                </div>
                <div class="col-md-3">
                    <div class="form-group">
                        <label for="">Region:</label>
                        <select class="form-select" v-model="filterFaunaRegion"
                        @change="filterDistrict($event)">
                            <option value="all">All</option>
                            <option v-for="region in region_list" :value="region.id"  v-bind:key="region.id">{{region.name}}</option>
                        </select>
                    </div>
                </div>
                <div class="col-md-3">
                    <div class="form-group">
                        <label for="">District:</label>
                        <select class="form-select" v-model="filterFaunaDistrict">
                            <option value="all">All</option>
                            <option v-for="district in filtered_district_list" :value="district.id">{{district.name}}</option>
                        </select>
                    </div>
                </div>
            </div>
        </CollapsibleFilters>

        <div v-if="newFaunaVisibility" class="col-md-12">
            <div class="text-end">
                <button type="button" class="btn btn-primary mb-2 " @click.prevent="createFauna"><i class="fa-solid fa-circle-plus"></i> New Fauna </button>
            </div>
        </div>

        <div class="row">
            <div class="col-lg-12">
                <datatable
                        ref="fauna_datatable"
                        :id="datatable_fauna_id"
                        :dtOptions="datatable_options"
                        :dtHeaders="datatable_headers"
                />
            </div>
        </div>
        <div v-if="speciesHistoryId">
            <SpeciesHistory
                ref="species_history"
                :key="speciesHistoryId"
                :species-id="speciesHistoryId"
            />
        </div>
    </div>
</template>
<script>
import "babel-polyfill"
import datatable from '@/utils/vue/datatable.vue'
import CollapsibleFilters from '@/components/forms/collapsible_component.vue'
import FormSection from '@/components/forms/section_toggle.vue'
import SpeciesHistory from '../internal/species_communities/species_history.vue';
import Vue from 'vue'
import {
    api_endpoints,
    constants,
    helpers
}from '@/utils/hooks'
export default {
    name: 'SpeciesFaunaTable',
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
        profile:{
            type: Object,
            default: null
        },
        filterFaunaScientificName_cache: {
            type: String,
            required: false,
            default: 'filterFaunaScientificName',
        },
        filterFaunaCommonName_cache: {
            type: String,
            required: false,
            default: 'filterFaunaCommonName',
        },
        filterFaunaPhylogeneticGroup_cache: {
            type: String,
            required: false,
            default: 'filterFaunaPhylogeneticGroup',
        },
        filterFaunaFamily_cache: {
            type: String,
            required: false,
            default: 'filterFaunaFamily',
        },
        filterFaunaGenus_cache: {
            type: String,
            required: false,
            default: 'filterFaunaGenus',
        },
        filterFaunaNameStatus_cache: {
            type: String,
            required: false,
            default: 'filterFaunaNameStatus',
        },
        filterFaunaConservationList_cache: {
            type: String,
            required: false,
            default: 'filterFaunaConservationList',
        },
        filterFaunaConservationCategory_cache: {
            type: String,
            required: false,
            default: 'filterFaunaConservationCategory',
        },
        filterFaunaApplicationStatus_cache: {
            type: String,
            required: false,
            default: 'filterFaunaApplicationStatus',
        },
        filterFaunaRegion_cache: {
            type: String,
            required: false,
            default: 'filterFaunaRegion',
        },
        filterFaunaDistrict_cache: {
            type: String,
            required: false,
            default: 'filterFaunaDistrict',
        },
    },
    data() {
        let vm = this;
        return {
            uuid:0,
            speciesHistoryId: null,
            datatable_fauna_id: 'species_fauna-datatable-'+vm._uid,

            //Profile to check if user has access to process Proposal

            // selected values for filtering
            filterFaunaScientificName: sessionStorage.getItem(this.filterFaunaScientificName_cache) ?
                                        sessionStorage.getItem(this.filterFaunaScientificName_cache) : 'all',

            filterFaunaCommonName: sessionStorage.getItem(this.filterFaunaCommonName_cache) ?
                                    sessionStorage.getItem(this.filterFaunaCommonName_cache) : 'all',

            filterFaunaPhylogeneticGroup: sessionStorage.getItem(this.filterFaunaPhylogeneticGroup_cache) ?
                                            sessionStorage.getItem(this.filterFaunaPhylogeneticGroup_cache) : 'all',

            filterFaunaFamily: sessionStorage.getItem(this.filterFaunaFamily_cache) ?
                                sessionStorage.getItem(this.filterFaunaFamily_cache) : 'all',

            filterFaunaGenus: sessionStorage.getItem(this.filterFaunaGenus_cache) ?
                                sessionStorage.getItem(this.filterFaunaGenus_cache) : 'all',

            filterFaunaNameStatus: sessionStorage.getItem(this.filterFaunaNameStatus_cache) ?
                    sessionStorage.getItem(this.filterFaunaNameStatus_cache) : 'all',

            filterFaunaConservationList: sessionStorage.getItem(this.filterFaunaConservationList_cache) ?
                                    sessionStorage.getItem(this.filterFaunaConservationList_cache) : 'all',

            filterFaunaConservationCategory: sessionStorage.getItem(this.filterFaunaConservationCategory_cache) ?
                                    sessionStorage.getItem(this.filterFaunaConservationCategory_cache) : 'all',

            filterFaunaApplicationStatus: sessionStorage.getItem(this.filterFaunaApplicationStatus_cache) ?
                                    sessionStorage.getItem(this.filterFaunaApplicationStatus_cache) : 'all',

            filterFaunaRegion: sessionStorage.getItem(this.filterFaunaRegion_cache) ?
                                sessionStorage.getItem(this.filterFaunaRegion_cache) : 'all',

            filterFaunaDistrict: sessionStorage.getItem(this.filterFaunaDistrict_cache) ?
                                    sessionStorage.getItem(this.filterFaunaDistrict_cache) : 'all',


            //Filter list for scientific name and common name
            filterListsSpecies: {},
            common_name_list: [],
            scientific_name_list: [],
            family_list: [],
            phylogenetic_group_list: [],
            conservation_list_dict: [],
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
                {value: 'active', name: 'Active'},
                {value: 'historical', name: 'Historical'},
            ],

            species_status: [],

        }
    },
    components:{
        datatable,
        CollapsibleFilters,
        FormSection,
        SpeciesHistory,
    },
    watch:{
        filterFaunaScientificName: function(){
            let vm = this;
            vm.$refs.fauna_datatable.vmDataTable.ajax.reload(helpers.enablePopovers,false); // This calls ajax() backend call.
            sessionStorage.setItem(vm.filterFaunaScientificName_cache, vm.filterFaunaScientificName);
        },
        filterFaunaCommonName: function() {
            let vm = this;
            vm.$refs.fauna_datatable.vmDataTable.ajax.reload(helpers.enablePopovers,false); // This calls ajax() backend call.
            sessionStorage.setItem(vm.filterFaunaCommonName_cache, vm.filterFaunaCommonName);
        },
        filterFaunaPhylogeneticGroup: function() {
            let vm = this;
            vm.$refs.fauna_datatable.vmDataTable.ajax.reload(helpers.enablePopovers,false); // This calls ajax() backend call.
            sessionStorage.setItem(vm.filterFaunaPhylogeneticGroup_cache, vm.filterFaunaPhylogeneticGroup);
        },
        filterFaunaFamily: function() {
            let vm = this;
            vm.$refs.fauna_datatable.vmDataTable.ajax.reload(helpers.enablePopovers,false); // This calls ajax() backend call.
            sessionStorage.setItem(vm.filterFaunaFamily_cache, vm.filterFaunaFamily);
        },
        filterFaunaGenus: function() {
            let vm = this;
            vm.$refs.fauna_datatable.vmDataTable.ajax.reload(helpers.enablePopovers,false); // This calls ajax() backend call.
            sessionStorage.setItem(vm.filterFaunaGenus_cache, vm.filterFaunaGenus);
        },
        filterFaunaNameStatus: function() {
            let vm = this;
            vm.$refs.fauna_datatable.vmDataTable.ajax.reload(helpers.enablePopovers,false); // This calls ajax() backend call.
            sessionStorage.setItem(vm.filterFaunaNameStatus_cache, vm.filterFaunaNameStatus);
        },
        filterFaunaConservationList: function() {
            let vm = this;
            vm.$refs.fauna_datatable.vmDataTable.ajax.reload(helpers.enablePopovers,false); // This calls ajax() backend call.
            sessionStorage.setItem(vm.filterFaunaConservationList_cache, vm.filterFaunaConservationList);
        },
        filterFaunaConservationCategory: function() {
            let vm = this;
            vm.$refs.fauna_datatable.vmDataTable.ajax.reload(helpers.enablePopovers,false); // This calls ajax() backend call.
            sessionStorage.setItem(vm.filterFaunaConservationCategory_cache, vm.filterFaunaConservationCategory);
        },
        filterFaunaApplicationStatus: function() {
            let vm = this;
            vm.$refs.fauna_datatable.vmDataTable.ajax.reload(helpers.enablePopovers,false); // This calls ajax() backend call.
            sessionStorage.setItem(vm.filterFaunaApplicationStatus_cache, vm.filterFaunaApplicationStatus);
        },
        filterFaunaRegion: function(){
            let vm = this;
            vm.$refs.fauna_datatable.vmDataTable.ajax.reload(helpers.enablePopovers,false); // This calls ajax() backend call.
            sessionStorage.setItem(vm.filterFaunaRegion_cache, vm.filterFaunaRegion);
        },
        filterFaunaDistrict: function(){
            let vm = this;
            vm.$refs.fauna_datatable.vmDataTable.ajax.reload(helpers.enablePopovers,false); // This calls ajax() backend call.
            sessionStorage.setItem(vm.filterFaunaDistrict_cache, vm.filterFaunaDistrict);
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
            if(this.filterFaunaScientificName === 'all' &&
                this.filterFaunaCommonName === 'all' &&
                this.filterFaunaPhylogeneticGroup === 'all' &&
                this.filterFaunaConservationList === 'all' &&
                this.filterFaunaConservationCategory === 'all' &&
                this.filterFaunaFamily === 'all' &&
                this.filterFaunaGenus === 'all' &&
                this.filterFaunaNameStatus === 'all' &&
                this.filterFaunaApplicationStatus === 'all' &&
                this.filterFaunaRegion === 'all' &&
                this.filterFaunaDistrict === 'all'){
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
        newFaunaVisibility: function() {
            return this.profile && this.profile.groups.includes(constants.GROUPS.SPECIES_AND_COMMUNITIES_APPROVERS)
        },
        datatable_headers: function(){
            if (this.is_external){
                return ['Id','Number', 'Scientific Name', 'Common Name', 'Phylo Group', 'Family',  'Genera', 'Region', 'District', 'Action']
            }
            if (this.is_internal){
                return ['Id','Number', 'Scientific Name', 'Common Name', 'Phylo Group', 'Family', 'Genera', 'Region', 'District','Status', 'Action']
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
//                                    'data-toggle="popover" ' +
//                                    'data-trigger="click" ' +
//                                    'data-placement="top auto"' +
//                                    'data-html="true" ' +
//                                    'data-content="<%= text %>" ' +
//                                    '>more</a>');
//                            if (_.endsWith(truncated, ellipsis)) {
//                                result += popTemplate({
//                                    text: value
//                                });
//                            }
//                            //return result;
//                            return type=='export' ? value : result;
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
                name: "taxonomy__informal_groups__classification_system_fk__class_desc",
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
                name: "taxonomy__family_name",
            }
        },
        column_genera: function(){
            return {
                data: "genus",
                orderable: true,
                searchable: true,
                visible: true,
                'render': function(data, type, full){
                    if(full.genus){
                        return full.genus;
                    }
                    // Should not reach here
                    return ''
                },
                name: "taxonomy__genera_name",
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
                        if (full.processing_status === "Active" && full.publishing_status) {
                            return full.processing_status +" - "+ full.publishing_status.public_status;
                        }
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
                searchable: false, // handles by filter_queryset override method - class ProposalFilterBackend
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
                            links += `<a href='#' data-history-species='${full.id}'>History</a><br>`;
                        }
                        else{
                            if(full.user_process){
                                links +=  `<a href='/internal/species_communities/${full.id}?group_type_name=${full.group_type}&action=edit'>Edit</a><br/>`;
                            }
                            links +=  `<a href='/internal/species_communities/${full.id}?group_type_name=${full.group_type}&action=view'>View</a><br/>`;
                            links += `<a href='#' data-history-species='${full.id}'>History</a><br>`;
                        }
                    } else {
                        links += `<a href='/external/species_communities/${full.id}?group_type_name=${full.group_type}&action=view'>View</a><br/>`;
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
                    className: 'btn btn-primary me-2 rounded',
                    action: function (e, dt, node, config) {
                        vm.exportData("excel");
                    }
                },
                {
                    text: '<i class="fa-solid fa-download"></i> CSV',
                    className: 'btn btn-primary rounded',
                    action: function (e, dt, node, config) {
                        vm.exportData("csv");
                    }
                }
            ]
            if(vm.is_external){
                columns = [
                    vm.column_id,
                    vm.column_number,
                    vm.column_scientific_name,
                    vm.column_common_name,
                    vm.column_phylogenetic_group,
                    vm.column_family,
                    vm.column_genera,
                    vm.column_region,
                    vm.column_district,
                    vm.column_action,
                ]
                search = false
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
                    vm.column_region,
                    vm.column_district,
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
                        d.filter_scientific_name = vm.filterFaunaScientificName;
                        d.filter_common_name = vm.filterFaunaCommonName;
                        d.filter_phylogenetic_group = vm.filterFaunaPhylogeneticGroup;
                        d.filter_family = vm.filterFaunaFamily;
                        d.filter_genus = vm.filterFaunaGenus;
                        d.filter_name_status = vm.filterFaunaNameStatus;
                        d.filter_conservation_list = vm.filterFaunaConservationList;
                        d.filter_conservation_category = vm.filterFaunaConservationCategory;
                        d.filter_application_status = vm.filterFaunaApplicationStatus;
                        d.filter_region = vm.filterFaunaRegion;
                        d.filter_district = vm.filterFaunaDistrict;
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
                drawCallback: function() {
                    helpers.enablePopovers();
                },
                initComplete: function() {
                    helpers.enablePopovers();
                },
            }
        }

    },
    methods:{
        historyDocument: function(id){
                this.speciesHistoryId = parseInt(id);
                this.uuid++;
                this.$nextTick(() => {
                    this.$refs.species_history.isModalOpen = true;
                });
            },
        collapsible_component_mounted: function(){
            this.$refs.collapsible_filters.show_warning_icon(this.filterApplied)
        },
        initialiseScientificNameLookup: function(){
                let vm = this;
                $(vm.$refs.scientific_name_lookup).select2({
                    minimumInputLength: 2,
                    "theme": "bootstrap-5",
                    allowClear: true,
                    placeholder:"Select Scientific Name",
                    ajax: {
                        url: api_endpoints.scientific_name_lookup,
                        dataType: 'json',
                        data: function(params) {
                            var query = {
                                term: params.term,
                                type: 'public',
                                group_type_id: vm.group_type_id,
                            }
                            return query;
                        },
                    },
                }).
                on("select2:select", function (e) {
                    var selected = $(e.currentTarget);
                    let data = e.params.data.id;
                    vm.filterFaunaScientificName = data; // this is id session
                    sessionStorage.setItem("filterFaunaScientificNameText", e.params.data.text); // this is name session
                }).
                on("select2:unselect",function (e) {
                    var selected = $(e.currentTarget);
                    vm.filterFaunaScientificName = 'all';
                    sessionStorage.setItem("filterFaunaScientificNameText",'');
                }).
                on("select2:open",function (e) {
                    const searchField = $('[aria-controls="select2-scientific_name_lookup-results"]')
                    // move focus to select2 field
                    searchField[0].focus();
                });
        },
        initialiseCommonNameLookup: function(){
                let vm = this;
                $(vm.$refs.common_name_lookup).select2({
                    minimumInputLength: 2,
                    "theme": "bootstrap-5",
                    allowClear: true,
                    placeholder:"Select Common Name",
                    ajax: {
                        url: api_endpoints.common_name_lookup,
                        dataType: 'json',
                        data: function(params) {
                            var query = {
                                term: params.term,
                                type: 'public',
                                group_type_id: vm.group_type_id,
                            }
                            return query;
                        },
                    },
                }).
                on("select2:select", function (e) {
                    var selected = $(e.currentTarget);
                    let data = e.params.data.id;
                    vm.filterFaunaCommonName = data;
                    sessionStorage.setItem("filterFaunaCommonNameText", e.params.data.text);
                }).
                on("select2:unselect",function (e) {
                    var selected = $(e.currentTarget);
                    vm.filterFaunaCommonName = 'all';
                    sessionStorage.setItem("filterFaunaCommonNameText",'');
                }).
                on("select2:open",function (e) {
                    const searchField = $('[aria-controls="select2-common_name_lookup-results"]')
                    // move focus to select2 field
                    searchField[0].focus();
                });
        },
        initialisePhyloGroupLookup: function(){
                let vm = this;
                $(vm.$refs.phylo_group_lookup).select2({
                    minimumInputLength: 2,
                    "theme": "bootstrap-5",
                    allowClear: true,
                    placeholder:"Select Phylo Group",
                    ajax: {
                        url: api_endpoints.phylo_group_lookup,
                        dataType: 'json',
                        data: function(params) {
                            var query = {
                                term: params.term,
                                type: 'public',
                                group_type_id: vm.group_type_id,
                            }
                            return query;
                        },
                    },
                }).
                on("select2:select", function (e) {
                    var selected = $(e.currentTarget);
                    let data = e.params.data.id;
                    vm.filterFaunaPhylogeneticGroup = data;
                    sessionStorage.setItem("filterFaunaPhylogeneticGroupText", e.params.data.text);
                }).
                on("select2:unselect",function (e) {
                    var selected = $(e.currentTarget);
                    vm.filterFaunaPhylogeneticGroup = 'all';
                    sessionStorage.setItem("filterFaunaPhylogeneticGroupText",'');
                }).
                on("select2:open",function (e) {
                    const searchField = $('[aria-controls="select2-phylo_group_lookup-results"]')
                    // move focus to select2 field
                    searchField[0].focus();
                });
        },
        initialiseFamilyLookup: function(){
                let vm = this;
                $(vm.$refs.family_lookup).select2({
                    minimumInputLength: 2,
                    "theme": "bootstrap-5",
                    allowClear: true,
                    placeholder:"Select Family",
                    ajax: {
                        url: api_endpoints.family_lookup,
                        dataType: 'json',
                        data: function(params) {
                            var query = {
                                term: params.term,
                                type: 'public',
                                group_type_id: vm.group_type_id,
                            }
                            return query;
                        },
                    },
                }).
                on("select2:select", function (e) {
                    var selected = $(e.currentTarget);
                    let data = e.params.data.id;
                    vm.filterFaunaFamily = data;
                    sessionStorage.setItem("filterFaunaFamilyText", e.params.data.text);
                }).
                on("select2:unselect",function (e) {
                    var selected = $(e.currentTarget);
                    vm.filterFaunaFamily = 'all';
                    sessionStorage.setItem("filterFaunaFamilyText",'');
                }).
                on("select2:open",function (e) {
                    //const searchField = $(".select2-search__field")
                    const searchField = $('[aria-controls="select2-family_lookup-results"]')
                    // move focus to select2 field
                    searchField[0].focus();
                });
        },
        initialiseGeneraLookup: function(){
                let vm = this;
                $(vm.$refs.genera_lookup).select2({
                    minimumInputLength: 2,
                    "theme": "bootstrap-5",
                    allowClear: true,
                    placeholder:"Select Genera",
                    ajax: {
                        url: api_endpoints.genera_lookup,
                        dataType: 'json',
                        data: function(params) {
                            var query = {
                                term: params.term,
                                type: 'public',
                                group_type_id: vm.group_type_id,
                            }
                            return query;
                        },
                    },
                }).
                on("select2:select", function (e) {
                    var selected = $(e.currentTarget);
                    let data = e.params.data.id;
                    vm.filterFaunaGenus = data;
                    sessionStorage.setItem("filterFaunaGenusText", e.params.data.text);
                }).
                on("select2:unselect",function (e) {
                    var selected = $(e.currentTarget);
                    vm.filterFaunaGenus = 'all';
                    sessionStorage.setItem("filterFaunaGenusText",'');
                }).
                on("select2:open",function (e) {
                    //const searchField = $(".select2-search__field")
                    const searchField = $('[aria-controls="select2-genera_lookup-results"]')
                    // move focus to select2 field
                    searchField[0].focus();
                });
        },
        fetchFilterLists: function(){
            let vm = this;

            vm.$http.get(api_endpoints.filter_lists_species+ '?group_type_name=' + vm.group_type_name).then((response) => {
                vm.filterListsSpecies = response.body;
                vm.scientific_name_list = vm.filterListsSpecies.scientific_name_list;
                vm.common_name_list = vm.filterListsSpecies.common_name_list;
                vm.family_list = vm.filterListsSpecies.family_list;
                vm.phylogenetic_group_list = vm.filterListsSpecies.phylogenetic_group_list;
                vm.filterDistrict();
                vm.species_status = vm.internal_status.slice().sort((a, b) => {
                    return a.name.trim().localeCompare(b.name.trim());
                });
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
                      this.filterFaunaDistrict='all'; //-----to remove the previous selection
                    }
                    this.filtered_district_list=[];
                    //---filter districts as per region selected
                    for(let choice of this.district_list){
                        if(choice.region_id.toString() === this.filterFaunaRegion.toString())
                        {
                          this.filtered_district_list.push(choice);
                        }

                    }
                });
        },
        createFauna: async function () {
            let newFaunaId = null
            try {
                    const createUrl = api_endpoints.species+"/";
                    let payload = new Object();
                    payload.group_type_id = this.group_type_id
                    let savedFauna = await Vue.http.post(createUrl, payload);
                    if (savedFauna) {
                        newFaunaId = savedFauna.body.id;
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
                params: {species_community_id: newFaunaId},
                query: {group_type_name: this.group_type_name},
                });
        },
        exportData: function (format) {
            let vm = this;
            const columns_new = {
                "0": {
                    "data": "id",
                    "name": "id",
                    "orderable": "true",
                    "search": {
                        "regex": "false",
                        "value": ""
                    },
                    "searchable": "false"
                },
                "1": {
                    "data": "species_number",
                    "name": "id",
                    "orderable": "true",
                    "search": {
                        "regex": "false",
                        "value": ""
                    },
                    "searchable": "true"
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
                    "data": "processing_status",
                    "name": "processing_status",
                    "orderable": "true",
                    "search": {
                        "regex": "false",
                        "value": ""
                    },
                    "searchable": "true"
                },
                "12": {
                    "data": "id",
                    "name": "",
                    "orderable": "false",
                    "search": {
                        "regex": "false",
                        "value": ""
                    },
                    "searchable": "false"
                },
                "2": {
                    "data": "scientific_name",
                    "name": "taxonomy__scientific_name",
                    "orderable": "true",
                    "search": {
                        "regex": "false",
                        "value": ""
                    },
                    "searchable": "true"
                },
                "3": {
                    "data": "common_name",
                    "name": "taxonomy__vernaculars__vernacular_name",
                    "orderable": "true",
                    "search": {
                        "regex": "false",
                        "value": ""
                    },
                    "searchable": "true"
                },
                "4": {
                    "data": "phylogenetic_group",
                    "name": "taxonomy__phylogenetic_group__name",
                    "orderable": "true",
                    "search": {
                        "regex": "false",
                        "value": ""
                    },
                    "searchable": "true"
                },
                "5": {
                    "data": "family",
                    "name": "taxonomy__family_name",
                    "orderable": "true",
                    "search": {
                        "regex": "false",
                        "value": ""
                    },
                    "searchable": "true"
                },
                "6": {
                    "data": "genus",
                    "name": "taxonomy__genera_name",
                    "orderable": "true",
                    "search": {
                        "regex": "false",
                        "value": ""
                    },
                    "searchable": "true"
                },
                "7": {
                    "data": "conservation_list",
                    "name": "conservation_status__conservation_list__code",
                    "orderable": "true",
                    "search": {
                        "regex": "false",
                        "value": ""
                    },
                    "searchable": "true"
                },
                "8": {
                    "data": "conservation_category",
                    "name": "conservation_status__conservation_category__code",
                    "orderable": "true",
                    "search": {
                        "regex": "false",
                        "value": ""
                    },
                    "searchable": "true"
                },
                "9": {
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
                filter_scientific_name: vm.filterFaunaScientificName,
                filter_common_name: vm.filterFaunaCommonName,
                filter_family: vm.filterFaunaFamily,
                filter_phylogenetic_group: vm.filterFaunaPhylogeneticGroup,
                filter_genus: vm.filterFaunaGenus,
                filter_conservation_list: vm.filterFaunaConservationList,
                filter_conservation_category: vm.filterFaunaConservationCategory,
                filter_name_status: vm.filterFaunaNameStatus,
                filter_application_status: vm.filterFaunaApplicationStatus,
                filter_region: vm.filterFaunaRegion,
                filter_district: vm.filterFaunaDistrict,
                is_internal: vm.is_internal,
                export_format: format
            };

            const url = api_endpoints.species_internal_export;
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
        discardSpeciesProposal:function (species_id) {
            let vm = this;
            swal.fire({
                title: "Discard Application",
                text: "Are you sure you want to discard this proposal?",
                icon: "warning",
                showCancelButton: true,
                confirmButtonText: 'Discard Application',
                confirmButtonColor:'#d9534f'
            }).then((result) => {
                if(result.isConfirmed){
                    vm.$http.delete(api_endpoints.discard_species_proposal(species_id))
                    .then((response) => {
                        swal.fire({
                            title: 'Discarded',
                            text: 'Your proposal has been discarded',
                            icon: 'success',
                            confirmButtonColor:'#226fbb',
                        });
                        vm.$refs.fauna_datatable.vmDataTable.ajax.reload(helpers.enablePopovers,false);
                    }, (error) => {
                        console.log(error);
                    });
                }
            },(error) => {

            });
        },
        addEventListeners: function(){
            let vm = this;
            // External Discard listener
            vm.$refs.fauna_datatable.vmDataTable.on('click', 'a[data-discard-species-proposal]', function(e) {
                e.preventDefault();
                var id = $(this).attr('data-discard-species-proposal');
                vm.discardSpeciesProposal(id);
            });
            vm.$refs.fauna_datatable.vmDataTable.on('click', 'a[data-history-species]', function(e) {
                    e.preventDefault();
                    var id = $(this).attr('data-history-species');
                    vm.historyDocument(id);
                });
            vm.$refs.fauna_datatable.vmDataTable.on('childRow.dt', function (e, settings) {
                helpers.enablePopovers();
            });
        },
        initialiseSearch:function(){
            this.submitterSearch();
        },
        submitterSearch:function(){
            let vm = this;
            vm.$refs.fauna_datatable.table.dataTableExt.afnFiltering.push(
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
            vm.initialiseScientificNameLookup();
            vm.initialiseCommonNameLookup();
            vm.initialisePhyloGroupLookup();
            vm.initialiseFamilyLookup();
            vm.initialiseGeneraLookup()
            vm.initialiseSearch();
            vm.addEventListeners();
            // -- to set the select2 field with the session value if exists onload()
            if(sessionStorage.getItem("filterFaunaScientificName")!='all' && sessionStorage.getItem("filterFaunaScientificName")!=null)
            {
                // contructor new Option(text, value, defaultSelected, selected)
                var newOption = new Option(sessionStorage.getItem("filterFaunaScientificNameText"), vm.filterFaunaScientificName, false, true);
                $('#scientific_name_lookup').append(newOption);
            }
            if(sessionStorage.getItem("filterFaunaCommonName")!='all' && sessionStorage.getItem("filterFaunaCommonName")!=null)
            {
                // contructor new Option(text, value, defaultSelected, selected)
                var newOption = new Option(sessionStorage.getItem("filterFaunaCommonNameText"), vm.filterFaunaCommonName, false, true);
                $('#common_name_lookup').append(newOption);
            }
            if(sessionStorage.getItem("filterFaunaPhylogeneticGroup")!='all' && sessionStorage.getItem("filterFaunaPhylogeneticGroup")!=null)
            {
                // contructor new Option(text, value, defaultSelected, selected)
                var newOption = new Option(sessionStorage.getItem("filterFaunaPhylogeneticGroupText"), vm.filterFaunaPhylogeneticGroup, false, true);
                $('#phylo_group_lookup').append(newOption);
            }
            if(sessionStorage.getItem("filterFaunaFamily")!='all' && sessionStorage.getItem("filterFaunaFamily")!=null)
            {
                // contructor new Option(text, value, defaultSelected, selected)
                var newOption = new Option(sessionStorage.getItem("filterFaunaFamilyText"), vm.filterFaunaFamily, false, true);
                $('#family_lookup').append(newOption);
            }
            if(sessionStorage.getItem("filterFaunaGenus")!='all' && sessionStorage.getItem("filterFaunaGenus")!=null)
            {
                // contructor new Option(text, value, defaultSelected, selected)
                var newOption = new Option(sessionStorage.getItem("filterFaunaGenusText"), vm.filterFaunaGenus, false, true);
                $('#genera_lookup').append(newOption);
            }
        });
    },
}
</script>
<style scoped>
.dt-buttons{
    float: right;
}
</style>
