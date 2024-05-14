<template id="species_flora_dashboard">
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
                        <select class="form-select" v-model="filterFloraNameStatus">
                            <option value="all">All</option>
                            <option value="True">Current</option>
                            <option value="False">Non Current</option>
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
                            <option v-for="status in species_status" :value="status.value">{{ status.name }}</option>
                        </select>
                    </div>
                </div>
                <div class="col-md-3">
                    <div class="form-group">
                        <label for="">Region:</label>
                        <select class="form-select" v-model="filterFloraRegion"
                        @change="filterDistrict($event)">
                            <option value="all">All</option>
                            <option v-for="region in region_list" :value="region.id" v-bind:key="region.id">{{region.name}}</option>
                        </select>
                    </div>
                </div>
                <div class="col-md-3">
                    <div class="form-group">
                        <label for="">District:</label>
                        <select class="form-select" v-model="filterFloraDistrict">
                            <option value="all">All</option>
                            <option v-for="district in filtered_district_list" :value="district.id">{{district.name}}</option>
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
        profile:{
            type: Object,
            default: null
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
        filterFloraNameStatus_cache: {
            type: String,
            required: false,
            default: 'filterFloraNameStatus',
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
            uuid:0,
            speciesHistoryId: null,
            datatable_id: 'species_flora-datatable-'+vm._uid,
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

            filterFloraNameStatus: sessionStorage.getItem(this.filterFloraNameStatus_cache) ?
                        sessionStorage.getItem(this.filterFloraNameStatus_cache) : 'all',

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
        filterFloraScientificName: function(){
            let vm = this;
            vm.$refs.flora_datatable.vmDataTable.ajax.reload(helpers.enablePopovers,false); // This calls ajax() backend call.
            sessionStorage.setItem(vm.filterFloraScientificName_cache, vm.filterFloraScientificName);
        },
        filterFloraCommonName: function() {
            let vm = this;
            vm.$refs.flora_datatable.vmDataTable.ajax.reload(helpers.enablePopovers,false); // This calls ajax() backend call.
            sessionStorage.setItem(vm.filterFloraCommonName_cache, vm.filterFloraCommonName);
        },
        filterFloraFamily: function() {
            let vm = this;
            vm.$refs.flora_datatable.vmDataTable.ajax.reload(helpers.enablePopovers,false); // This calls ajax() backend call.
            sessionStorage.setItem(vm.filterFloraFamily_cache, vm.filterFloraFamily);
        },
        filterFloraPhylogeneticGroup: function() {
            let vm = this;
            vm.$refs.flora_datatable.vmDataTable.ajax.reload(helpers.enablePopovers,false); // This calls ajax() backend call.
            sessionStorage.setItem(vm.filterFloraPhylogeneticGroup_cache, vm.filterFloraPhylogeneticGroup);
        },
        filterFloraGenus: function() {
            let vm = this;
            vm.$refs.flora_datatable.vmDataTable.ajax.reload(helpers.enablePopovers,false); // This calls ajax() backend call.
            sessionStorage.setItem(vm.filterFloraGenus_cache, vm.filterFloraGenus);
        },
        filterFloraNameStatus: function() {
            let vm = this;
            vm.$refs.flora_datatable.vmDataTable.ajax.reload(helpers.enablePopovers,false); // This calls ajax() backend call.
            sessionStorage.setItem(vm.filterFloraNameStatus_cache, vm.filterFloraNameStatus);
        },
        filterFloraConservationList: function() {
            let vm = this;
            vm.$refs.flora_datatable.vmDataTable.ajax.reload(helpers.enablePopovers,false); // This calls ajax() backend call.
            sessionStorage.setItem(vm.filterFloraConservationList_cache, vm.filterFloraConservationList);
        },
        filterFloraConservationCategory: function() {
            let vm = this;
            vm.$refs.flora_datatable.vmDataTable.ajax.reload(helpers.enablePopovers,false); // This calls ajax() backend call.
            sessionStorage.setItem(vm.filterFloraConservationCategory_cache, vm.filterFloraConservationCategory);
        },
        filterFloraApplicationStatus: function() {
            let vm = this;
            vm.$refs.flora_datatable.vmDataTable.ajax.reload(helpers.enablePopovers,false); // This calls ajax() backend call.
            sessionStorage.setItem(vm.filterFloraApplicationStatus_cache, vm.filterFloraApplicationStatus);
        },
        filterFloraRegion: function(){
            let vm = this;
            vm.$refs.flora_datatable.vmDataTable.ajax.reload(helpers.enablePopovers,false); // This calls ajax() backend call.
            sessionStorage.setItem(vm.filterFloraRegion_cache, vm.filterFloraRegion);
        },
        filterFloraDistrict: function(){
            let vm = this;
            vm.$refs.flora_datatable.vmDataTable.ajax.reload(helpers.enablePopovers,false); // This calls ajax() backend call.
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
                this.filterFloraNameStatus === 'all' &&
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
            return this.profile && this.profile.groups.includes(constants.GROUPS.SPECIES_AND_COMMUNITIES_APPROVERS)
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
                name: "taxonomy__informal_groups__classification_system_fk__class_desc",
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
                            links += `<a href='#' data-history-species='${full.id}'>History</a><br>`;
                        }
                        else{
                            links +=  `<a href='/internal/species_communities/${full.id}?group_type_name=${full.group_type}&action=view'>View</a><br/>`;
                            links += `<a href='#' data-history-species='${full.id}'>History</a><br>`;
                        }
                    } else {
                        links +=  `<a href='/external/species_communities/${full.id}?group_type_name=${full.group_type}&action=view'>View</a><br/>`;
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
                    vm.column_conservation_list,
                    vm.column_conservation_category,
                    vm.column_region,
                    vm.column_district,
                    vm.column_status,
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
                    vm.column_conservation_list,
                    vm.column_conservation_category,
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
                        d.filter_scientific_name = vm.filterFloraScientificName;
                        d.filter_common_name = vm.filterFloraCommonName;
                        d.filter_family = vm.filterFloraFamily;
                        d.filter_phylogenetic_group = vm.filterFloraPhylogeneticGroup;
                        d.filter_genus = vm.filterFloraGenus;
                        d.filter_name_status = vm.filterFloraNameStatus;
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
                drawCallback: function() {
                    helpers.enablePopovers();
                },
                initComplete: function() {
                    helpers.enablePopovers();
                    var $searchInput = $('div.dataTables_filter input');

                    $searchInput.unbind('keyup search input');

                    $searchInput.bind('keypress', (vm.delay(function(e) {

                        if (e.which == 13) {

                            vm.$refs.flora_datatable.vmDataTable.search(this.value).draw();

                        }

                    }, 0)));
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
                        // results: function (data, page) { // parse the results into the format expected by Select2.
                        //     // since we are using custom formatting functions we do not need to alter remote JSON data
                        //     return {results: data};
                        // },
                    },
                }).
                on("select2:select", function (e) {
                    var selected = $(e.currentTarget);
                    let data = e.params.data.id;
                    vm.filterFloraScientificName = data;
                    sessionStorage.setItem("filterFloraScientificNameText", e.params.data.text);
                }).
                on("select2:unselect",function (e) {
                    var selected = $(e.currentTarget);
                    vm.filterFloraScientificName = 'all';
                    sessionStorage.setItem("filterFloraScientificNameText",'');
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
                    vm.filterFloraCommonName = data;
                    sessionStorage.setItem("filterFloraCommonNameText", e.params.data.text);
                }).
                on("select2:unselect",function (e) {
                    var selected = $(e.currentTarget);
                    vm.filterFloraCommonName = 'all';
                    sessionStorage.setItem("filterFloraCommonNameText",'');
                }).
                on("select2:open",function (e) {
                    const searchField = $('[aria-controls="select2-common_name_lookup-results"]')
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
                    vm.filterFloraFamily = data;
                    sessionStorage.setItem("filterFloraFamilyText", e.params.data.text);
                }).
                on("select2:unselect",function (e) {
                    var selected = $(e.currentTarget);
                    vm.filterFloraFamily = 'all';
                    sessionStorage.setItem("filterFloraFamilyText",'');
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
                    vm.filterFloraGenus = data;
                    sessionStorage.setItem("filterFloraGenusText", e.params.data.text);
                }).
                on("select2:unselect",function (e) {
                    var selected = $(e.currentTarget);
                    vm.filterFloraGenus = 'all';
                    sessionStorage.setItem("filterFloraGenusText",'');
                }).
                on("select2:open",function (e) {
                    //const searchField = $(".select2-search__field")
                    const searchField = $('[aria-controls="select2-genera_lookup-results"]')
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
                    vm.filterFloraPhylogeneticGroup = data;
                    sessionStorage.setItem("filterFloraPhylogeneticGroupText", e.params.data.text);
                }).
                on("select2:unselect",function (e) {
                    var selected = $(e.currentTarget);
                    vm.filterFloraPhylogeneticGroup = 'all';
                    sessionStorage.setItem("filterFloraPhylogeneticGroupText",'');
                }).
                on("select2:open",function (e) {
                    const searchField = $('[aria-controls="select2-phylo_group_lookup-results"]')
                    // move focus to select2 field
                    searchField[0].focus();
                });
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
                vm.filterDistrict();
                vm.species_status = vm.internal_status.slice().sort((a, b) => {
                    return a.name.trim().localeCompare(b.name.trim());
                });
            },(error) => {
                console.log(error);
            })
            vm.$http.get(api_endpoints.region_district_filter_dict).then((response) => {
                vm.filterRegionDistrict= response.body;
                vm.region_list = vm.filterRegionDistrict.region_list;
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
        //-------filter district dropdown dependent on region selected
        filterDistrict: function(event) {
                this.$nextTick(() => {
                    if(event){
                      this.filterFloraDistrict='all'; //-----to remove the previous selection
                    }
                    this.filtered_district_list=[];
                    //---filter districts as per region selected
                    for(let choice of this.district_list){
                        if(choice.region_id.toString() === this.filterFloraRegion.toString())
                        {
                          this.filtered_district_list.push(choice);
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
                params: { species_community_id: newFloraId },
                query: { group_type_name: this.group_type_name },
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
                    "name": "taxonomy__family_fk__scientific_name",
                    "orderable": "true",
                    "search": {
                        "regex": "false",
                        "value": ""
                    },
                    "searchable": "true"
                },
                "6": {
                    "data": "genus",
                    "name": "taxonomy__genus__name",
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
                filter_scientific_name: vm.filterFloraScientificName,
                filter_common_name: vm.filterFloraCommonName,
                filter_family: vm.filterFloraFamily,
                filter_phylogenetic_group: vm.filterFloraPhylogeneticGroup,
                filter_genus: vm.filterFloraGenus,
                filter_name_status: vm.filterFloraNameStatus,
                filter_conservation_list: vm.filterFloraConservationList,
                filter_conservation_category: vm.filterFloraConservationCategory,
                filter_application_status: vm.filterFloraApplicationStatus,
                filter_region: vm.filterFloraRegion,
                filter_district: vm.filterFloraDistrict,
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
                        vm.$refs.flora_datatable.vmDataTable.ajax.reload(helpers.enablePopovers,false);
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
            vm.$refs.flora_datatable.vmDataTable.on('click', 'a[data-discard-species-proposal]', function(e) {
                e.preventDefault();
                var id = $(this).attr('data-discard-species-proposal');
                vm.discardSpeciesProposal(id);
            });
            vm.$refs.flora_datatable.vmDataTable.on('click', 'a[data-history-species]', function(e) {
                    e.preventDefault();
                    var id = $(this).attr('data-history-species');
                    vm.historyDocument(id);
                });
            vm.$refs.flora_datatable.vmDataTable.on('childRow.dt', function (e, settings) {
                helpers.enablePopovers();
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
        delay(callback, ms) {
            var timer = 0;

            return function () {

                var context = this, args = arguments;

                clearTimeout(timer);

                timer = setTimeout(function () {

                    callback.apply(context, args);

                }, ms || 0);

            };
        },
    },

    mounted: function(){
        let vm = this;
        vm.fetchFilterLists();
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
            vm.initialiseGeneraLookup();
            vm.initialiseSearch();
            vm.addEventListeners();
            // -- to set the select2 field with the session value if exists onload()
            if(sessionStorage.getItem("filterFloraScientificName")!='all' && sessionStorage.getItem("filterFloraScientificName")!=null)
            {
                // contructor new Option(text, value, defaultSelected, selected)
                var newOption = new Option(sessionStorage.getItem("filterFloraScientificNameText"), vm.filterFloraScientificName, false, true);
                $('#scientific_name_lookup').append(newOption);
                //$('#scientific_name_lookup').append(newOption).trigger('change');
            }
            if(sessionStorage.getItem("filterFloraCommonName")!='all' && sessionStorage.getItem("filterFloraCommonName")!=null)
            {
                // contructor new Option(text, value, defaultSelected, selected)
                var newOption = new Option(sessionStorage.getItem("filterFloraCommonNameText"), vm.filterFloraCommonName, false, true);
                $('#common_name_lookup').append(newOption);
            }
            if(sessionStorage.getItem("filterFloraPhylogeneticGroup")!='all' && sessionStorage.getItem("filterFloraPhylogeneticGroup")!=null)
            {
                // contructor new Option(text, value, defaultSelected, selected)
                var newOption = new Option(sessionStorage.getItem("filterFloraPhylogeneticGroupText"), vm.filterFloraPhylogeneticGroup, false, true);
                $('#phylo_group_lookup').append(newOption);
            }
            if(sessionStorage.getItem("filterFloraFamily")!='all' && sessionStorage.getItem("filterFloraFamily")!=null)
            {
                // contructor new Option(text, value, defaultSelected, selected)
                var newOption = new Option(sessionStorage.getItem("filterFloraFamilyText"), vm.filterFloraFamily, false, true);
                $('#family_lookup').append(newOption);
            }
            if(sessionStorage.getItem("filterFloraGenus")!='all' && sessionStorage.getItem("filterFloraGenus")!=null)
            {
                // contructor new Option(text, value, defaultSelected, selected)
                var newOption = new Option(sessionStorage.getItem("filterFloraGenusText"), vm.filterFloraGenus, false, true);
                $('#genera_lookup').append(newOption);
            }
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
