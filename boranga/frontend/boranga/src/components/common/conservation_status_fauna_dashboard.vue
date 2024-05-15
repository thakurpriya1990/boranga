<template id="species_fauna_cs_dashboard">
    <div>
        <CollapsibleFilters component_title="Filters" ref="collapsible_filters" @created="collapsible_component_mounted"
            class="mb-2">
            <div class="row">
                <div class="col-md-3">
                    <div class="form-group" id="select_scientific_name">
                        <label for="cs_scientific_name_lookup">Scientific Name:</label>
                        <select id="cs_scientific_name_lookup" name="cs_scientific_name_lookup"
                            ref="cs_scientific_name_lookup" class="form-control" />
                    </div>
                </div>
                <div class="col-md-3">
                    <div class="form-group" id="select_common_name">
                        <label for="cs_common_name_lookup">Common Name:</label>
                        <select id="cs_common_name_lookup" name="cs_common_name_lookup" ref="cs_common_name_lookup"
                            class="form-control" />
                    </div>
                </div>
                <div class="col-md-3">
                    <div class="form-group" id="select_phylo_group">
                        <label for="cs_phylo_group_lookup">Phylo Group:</label>
                        <select id="cs_phylo_group_lookup" name="cs_phylo_group_lookup" ref="cs_phylo_group_lookup"
                            class="form-control" />
                    </div>
                </div>
                <div class="col-md-3">
                    <div class="form-group" id="select_family">
                        <label for="cs_family_lookup">Family:</label>
                        <select id="cs_family_lookup" name="cs_family_lookup" ref="cs_family_lookup"
                            class="form-control" />
                    </div>
                </div>
                <div class="col-md-3">
                    <div class="form-group" id="select_genera">
                        <label for="cs_genera_lookup">Genera:</label>
                        <select id="cs_genera_lookup" name="cs_genera_lookup" ref="cs_genera_lookup"
                            class="form-control" />
                    </div>
                </div>
                <div class="col-md-3">
                    <div class="form-group">
                        <label for="">Conservation List:</label>
                        <select class="form-select" v-model="filterCSFaunaConservationList"
                            @change="filterConservationCategory($event)">
                            <option value="all">All</option>
                            <option v-for="list in conservation_list_dict" :value="list.id">{{ list.code }}</option>
                        </select>
                    </div>
                </div>
                <div class="col-md-3">
                    <div class="form-group">
                        <label for="">Conservation Category:</label>
                        <select class="form-select" v-model="filterCSFaunaConservationCategory">
                            <option value="all">All</option>
                            <option v-for="list in filtered_conservation_category_list" :value="list.id">{{ list.code }}
                            </option>
                        </select>
                    </div>
                </div>
                <div class="col-md-3" v-show="!is_for_agenda">
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
                        <select class="form-select" v-model="filterCSFaunaRegion" @change="filterDistrict($event)">
                            <option value="all">All</option>
                            <option v-for="region in region_list" :value="region.id" v-bind:key="region.id">
                                {{ region.name }}</option>
                        </select>
                    </div>
                </div>
                <div class="col-md-3">
                    <div class="form-group">
                        <label for="">District:</label>
                        <select class="form-select" v-model="filterCSFaunaDistrict">
                            <option value="all">All</option>
                            <option v-for="district in filtered_district_list" :value="district.id">{{ district.name }}
                            </option>
                        </select>
                    </div>
                </div>
                <div class="col-md-3" v-show="!is_for_agenda">
                    <div class="form-group">
                        <label for="">Effective From Date Range:</label>
                        <input type="date" class="form-control" placeholder="DD/MM/YYYY" id="from_effective_from_date" v-model="filterCSFromFaunaEffectiveFromDate">
                    </div>
                </div>
                <div class="col-md-3" v-show="!is_for_agenda">
                    <div class="form-group">
                        <label for=""></label>
                        <input type="date" class="form-control" placeholder="DD/MM/YYYY" id="to_effective_from_date" v-model="filterCSToFaunaEffectiveFromDate">
                    </div>
                </div>

                <div class="col-md-3" v-show="!is_for_agenda">
                    <div class="form-group">
                        <label for="">Effective To Date Range:</label>
                        <input type="date" class="form-control" placeholder="DD/MM/YYYY" id="from_effective_to_date" v-model="filterCSFromFaunaEffectiveToDate">
                    </div>
                </div>

                <div class="col-md-3" v-show="!is_for_agenda">
                    <div class="form-group">
                        <label for=""></label>
                        <input type="date" class="form-control" placeholder="DD/MM/YYYY" id="to_effective_to_date" v-model="filterCSToFaunaEffectiveToDate">
                    </div>
                </div>
            </div>
        </CollapsibleFilters>

        <div v-if="addFaunaCSVisibility && is_for_agenda == false" class="col-md-12">
            <div class="text-end">
                <button type="button" class="btn btn-primary mb-2 " @click.prevent="createFaunaConservationStatus"><i
                        class="fa-solid fa-circle-plus"></i> Propose Conservation Satus</button>
            </div>
        </div>

        <div class="row">
            <div class="col-lg-12">
                <datatable ref="fauna_cs_datatable" :id="datatable_id" :dtOptions="datatable_options"
                    :dtHeaders="datatable_headers" />
            </div>
            <div v-if="speciesConservationStatusHistoryId">
                <SpeciesConservationStatusHistory ref="species_conservation_status_history"
                    :key="speciesConservationStatusHistoryId"
                    :conservation-status-id="speciesConservationStatusHistoryId" :species-id="speciesHistoryId"
                    :conservation-list-id="listHistoryId" />
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
import SpeciesConservationStatusHistory from '../internal/conservation_status/species_conservation_status_history.vue';
import Vue from 'vue'
//require("select2/dist/css/select2.min.css");
//require("select2-bootstrap-theme/dist/select2-bootstrap.min.css");
import {
    api_endpoints,
    constants,
    helpers
} from '@/utils/hooks'
export default {
    name: 'ConservationStatusFaunaTable',
    props: {
        level: {
            type: String,
            required: true,
            validator: function (val) {
                let options = ['internal', 'referral', 'external'];
                return options.indexOf(val) != -1 ? true : false;
            }
        },
        group_type_name: {
            type: String,
            required: true
        },
        group_type_id: {
            type: Number,
            required: true,
            default: 0
        },
        url: {
            type: String,
            required: true
        },
        profile: {
            type: Object,
            default: null
        },
        // when the datable need to be shown for agenda_items in meeting check this variable is true
        is_for_agenda: {
            type: Boolean,
            default: false
        },
        // for adding agendaitems for the meeting_obj.id
        meeting_obj: {
            type: Object,
            required: false
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
        filterCSFromFaunaEffectiveFromDate_cache: {
            type: String,
            required: false,
            default: 'filterCSFromFaunaEffectiveFromDate',
        },
        filterCSToFaunaEffectiveFromDate_cache: {
            type: String,
            required: false,
            default: 'filterCSToFaunaEffectiveFromDate',
        },
        filterCSFromFaunaEffectiveToDate_cache: {
            type: String,
            required: false,
            default: 'filterCSFromFaunaEffectiveToDate',
        },
        filterCSToFaunaEffectiveToDate_cache: {
            type: String,
            required: false,
            default: 'filterCSToFaunaEffectiveToDate',
        },
    },
    data() {
        let vm = this;
        return {
            datatable_id: 'species_fauna_cs-datatable-' + vm._uid,
            speciesConservationStatusHistoryId: null,
            speciesHistoryId: null,
            listHistoryId: null,
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

            filterCSFromFaunaEffectiveFromDate: sessionStorage.getItem(this.filterCSFromFaunaEffectiveFromDate_cache) ?
            sessionStorage.getItem(this.filterCSFromFaunaEffectiveFromDate_cache) : '',
            filterCSToFaunaEffectiveFromDate: sessionStorage.getItem(this.filterCSToFaunaEffectiveFromDate_cache) ?
            sessionStorage.getItem(this.filterCSToFaunaEffectiveFromDate_cache) : '',

            filterCSFromFaunaEffectiveToDate: sessionStorage.getItem(this.filterCSFromFaunaEffectiveToDate_cache) ?
            sessionStorage.getItem(this.filterCSFromFaunaEffectiveToDate_cache) : '',
            filterCSToFaunaEffectiveToDate: sessionStorage.getItem(this.filterCSToFaunaEffectiveToDate_cache) ?
            sessionStorage.getItem(this.filterCSToFaunaEffectiveToDate_cache) : '',

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
            filtered_district_list: [],

            // filtering options
            external_status: [
                { value: 'draft', name: 'Draft' },
                { value: 'with_assessor', name: 'Under Review' },
                { value: 'approved', name: 'Approved' },
                { value: 'declined', name: 'Declined' },
                { value: 'discarded', name: 'Discarded' },
                { value: 'awaiting_payment', name: 'Awaiting Payment' },
            ],
            internal_status: [
                { value: 'draft', name: 'Draft' },
                { value: 'with_assessor', name: 'With Assessor' },
                { value: 'ready_for_agenda', name: 'Ready For Agenda' },
                // {value: 'with_approver', name: 'With Approver'},
                { value: 'with_referral', name: 'With Referral' },
                { value: 'approved', name: 'Approved' },
                { value: 'declined', name: 'Declined' },
                { value: 'discarded', name: 'Discarded' },
                { value: 'closed', name: 'Closed' },
            ],

            proposal_status: [],
        }
    },
    components: {
        datatable,
        CollapsibleFilters,
        FormSection,
        SpeciesConservationStatusHistory,
    },
    watch: {
        filterCSFaunaScientificName: function () {
            let vm = this;
            vm.$refs.fauna_cs_datatable.vmDataTable.ajax.reload(helpers.enablePopovers, false); // This calls ajax() backend call.
            sessionStorage.setItem(vm.filterCSFaunaScientificName_cache, vm.filterCSFaunaScientificName);
        },
        filterCSFaunaCommonName: function () {
            let vm = this;
            vm.$refs.fauna_cs_datatable.vmDataTable.ajax.reload(helpers.enablePopovers, false); // This calls ajax() backend call.
            sessionStorage.setItem(vm.filterCSFaunaCommonName_cache, vm.filterCSFaunaCommonName);
        },
        filterCSFaunaPhylogeneticGroup: function () {
            let vm = this;
            vm.$refs.fauna_cs_datatable.vmDataTable.ajax.reload(helpers.enablePopovers, false); // This calls ajax() backend call.
            sessionStorage.setItem(vm.filterCSFaunaPhylogeneticGroup_cache, vm.filterCSFaunaPhylogeneticGroup);
        },
        filterCSFaunaFamily: function () {
            let vm = this;
            vm.$refs.fauna_cs_datatable.vmDataTable.ajax.reload(helpers.enablePopovers, false); // This calls ajax() backend call.
            sessionStorage.setItem(vm.filterCSFaunaFamily_cache, vm.filterCSFaunaFamily);
        },
        filterCSFaunaGenus: function () {
            let vm = this;
            vm.$refs.fauna_cs_datatable.vmDataTable.ajax.reload(helpers.enablePopovers, false); // This calls ajax() backend call.
            sessionStorage.setItem(vm.filterCSFaunaGenus_cache, vm.filterCSFaunaGenus);
        },
        filterCSFaunaConservationList: function () {
            let vm = this;
            vm.$refs.fauna_cs_datatable.vmDataTable.ajax.reload(helpers.enablePopovers, false); // This calls ajax() backend call.
            sessionStorage.setItem(vm.filterCSFaunaConservationList_cache, vm.filterCSFaunaConservationList);
        },
        filterCSFaunaConservationCategory: function () {
            let vm = this;
            vm.$refs.fauna_cs_datatable.vmDataTable.ajax.reload(helpers.enablePopovers, false); // This calls ajax() backend call.
            sessionStorage.setItem(vm.filterCSFaunaConservationCategory_cache, vm.filterCSFaunaConservationCategory);
        },
        filterCSFaunaRegion: function () {
            let vm = this;
            vm.$refs.fauna_cs_datatable.vmDataTable.ajax.reload(helpers.enablePopovers, false); // This calls ajax() backend call.
            sessionStorage.setItem(vm.filterCSFaunaRegion_cache, vm.filterCSFaunaRegion);
        },
        filterCSFaunaDistrict: function () {
            let vm = this;
            vm.$refs.fauna_cs_datatable.vmDataTable.ajax.reload(helpers.enablePopovers, false); // This calls ajax() backend call.
            sessionStorage.setItem(vm.filterCSFaunaDistrict_cache, vm.filterCSFaunaDistrict);
        },
        filterCSFromFaunaEffectiveFromDate: function(){
            let vm = this;
            vm.$refs.fauna_cs_datatable.vmDataTable.ajax.reload(helpers.enablePopovers,false); // This calls ajax() backend call.
            sessionStorage.setItem(vm.filterCSFromFaunaEffectiveFromDate_cache, vm.filterCSFromFaunaEffectiveFromDate);
        },
        filterCSToFaunaEffectiveFromDate: function(){
            let vm = this;
            vm.$refs.fauna_cs_datatable.vmDataTable.ajax.reload(helpers.enablePopovers,false); // This calls ajax() backend call.
            sessionStorage.setItem(vm.filterCSToFaunaEffectiveFromDate_cache, vm.filterCSToFaunaEffectiveFromDate);
        },
        filterCSFromFaunaEffectiveToDate: function(){
            let vm = this;
            vm.$refs.fauna_cs_datatable.vmDataTable.ajax.reload(helpers.enablePopovers,false); // This calls ajax() backend call.
            sessionStorage.setItem(vm.filterCSFromFaunaEffectiveToDate_cache, vm.filterCSFromFaunaEffectiveToDate);
        },
        filterCSToFaunaEffectiveToDate: function(){
            let vm = this;
            vm.$refs.fauna_cs_datatable.vmDataTable.ajax.reload(helpers.enablePopovers,false); // This calls ajax() backend call.
            sessionStorage.setItem(vm.filterCSToFaunaEffectiveToDate_cache, vm.filterCSToFaunaEffectiveToDate);
        },
        filterCSFaunaApplicationStatus: function () {
            let vm = this;
            vm.$refs.fauna_cs_datatable.vmDataTable.ajax.reload(helpers.enablePopovers, false); // This calls ajax() backend call.
            sessionStorage.setItem(vm.filterCSFaunaApplicationStatus_cache, vm.filterCSFaunaApplicationStatus);
        },
        filterApplied: function () {
            if (this.$refs.collapsible_filters) {
                // Collapsible component exists
                this.$refs.collapsible_filters.show_warning_icon(this.filterApplied)
            }
        },
    },
    computed: {
        filterApplied: function () {
            if (this.filterCSFaunaScientificName === 'all' &&
                this.filterCSFaunaCommonName === 'all' &&
                this.filterCSFaunaPhylogeneticGroup === 'all' &&
                this.filterCSFaunaFamily === 'all' &&
                this.filterCSFaunaGenus === 'all' &&
                this.filterCSFaunaConservationList === 'all' &&
                this.filterCSFaunaConservationCategory === 'all' &&
                this.filterCSFaunaRegion === 'all' &&
                this.filterCSFaunaDistrict === 'all' &&
                this.filterCSFaunaApplicationStatus === 'all' &&
                this.filterCSFromFaunaEffectiveFromDate === '' &&
                this.filterCSToFaunaEffectiveFromDate === '' &&
                this.filterCSFromFaunaEffectiveToDate === '' &&
                this.filterCSToFaunaEffectiveToDate === ''){
                return false
            } else {
                return true
            }
        },
        is_external: function () {
            return this.level == 'external';
        },
        is_internal: function () {
            return this.level == 'internal'
        },
        is_referral: function () {
            return this.level == 'referral';
        },
        addFaunaCSVisibility: function () {
            return this.profile && this.profile.groups.find(
                (i) => [
                    constants.GROUPS.INTERNAL_CONTRIBUTORS
                ].includes(i)
            );
        },
        datatable_headers: function () {
            if (this.is_external) {
                return ['Number', 'Species', 'Scientific Name', 'Common Name', 'Conservation List',
                    'Conservation Category', 'Region', 'District', 'Effective From Date', 'Effective To Date', 'Family', 'Genera', 'Status', 'Action']
            }
            if (this.is_internal) {
                return ['Number', 'Species', 'Scientific Name', 'Common Name', 'Conservation List',
                    'Conservation Category', 'Region', 'District', 'Effective From Date', 'Effective To Date', 'Family', 'Genera', 'Status', 'Action']
            }
        },
        column_id: function () {
            return {
                data: "id",
                orderable: true,
                searchable: false,
                visible: false,
                'render': function (data, type, full) {
                    return full.id
                },
                name: "id",
            }
        },
        column_number: function () {
            let vm = this;
            return {
                data: "conservation_status_number",
                orderable: true,
                searchable: true,
                visible: true,
                'render': function (data, type, full) {
                    let value = full.conservation_status_number
                    if (vm.is_internal && full.is_new_contributor) {
                        value += ' <span class="badge bg-warning">New Contributor</span>'
                    }
                    return value
                },
                name: "id",
            }
        },
        column_species_number: function () {
            return {
                data: "species_number",
                orderable: true,
                searchable: true,
                visible: true,
                'render': function (data, type, full) {
                    return full.species_number
                },
                name: "species__species_number",
            }
        },
        column_scientific_name: function () {
            return {
                data: "scientific_name",
                orderable: true,
                searchable: true,
                visible: true,
                'render': function (value, type) {
                    let result = helpers.dtPopover(value, 30, 'hover');
                    return type == 'export' ? value : result;
                },
                name: "species__taxonomy__scientific_name",
            }
        },
        column_common_name: function () {
            return {
                data: "common_name",
                orderable: true,
                searchable: true,
                visible: true,
                'render': function (value, type) {
                    let result = helpers.dtPopover(value, 30, 'hover');
                    return type == 'export' ? value : result;
                },
                //'createdCell': helpers.dtPopoverCellFn,
                name: "species__taxonomy__vernaculars__vernacular_name",
            }
        },
        column_family: function () {
            return {
                data: "family",
                orderable: true,
                searchable: true,
                visible: true,
                'render': function (value, type) {
                    let result = helpers.dtPopover(value, 30, 'hover');
                    return type == 'export' ? value : result;
                },
                //'createdCell': helpers.dtPopoverCellFn,
                name: "species__taxonomy__family_name",
            }
        },
        column_genera: function () {
            return {
                data: "genus",
                orderable: true,
                searchable: true,
                visible: true,
                'render': function (value, type) {
                    let result = helpers.dtPopover(value, 30, 'hover');
                    return type == 'export' ? value : result;
                },
                //'createdCell': helpers.dtPopoverCellFn,
                name: "species__taxonomy__genera_name",
            }
        },
        column_conservation_list: function () {
            return {
                data: "conservation_list",
                orderable: true,
                searchable: true,
                visible: true,
                'render': function (data, type, full) {
                    if (full.conservation_list) {
                        return full.conservation_list;
                    }
                    // Should not reach here
                    return ''
                },
                name: "conservation_list__code",
            }
        },
        column_conservation_category: function () {
            return {
                data: "conservation_category",
                orderable: true,
                searchable: true,
                visible: true,
                'render': function (data, type, full) {
                    if (full.conservation_category) {
                        return full.conservation_category;
                    }
                    // Should not reach here
                    return ''
                },
                name: "conservation_category__code",
            }
        },
        column_status: function () {
            return {
                // 9. Workflow Status
                data: "processing_status",
                orderable: true,
                searchable: true,
                visible: true,
                'render': function (data, type, full) {
                    if (full.processing_status) {
                        return full.processing_status;
                    }
                    // Should not reach here
                    return ''
                },
                name: "processing_status",
            }
        },
        column_region: function () {
            return {
                data: "region",
                orderable: true,
                searchable: false, // handles by filter_queryset override method
                visible: true,
                'render': function (data, type, full) {
                    if (full.region) {
                        return full.region
                    }
                    // Should not reach here
                    return ''
                },
                name: "species__region__name",
            }
        },
        column_district: function () {
            return {
                data: "district",
                orderable: true,
                searchable: false, // handles by filter_queryset override method
                visible: true,
                'render': function (data, type, full) {
                    if (full.district) {
                        return full.district
                    }
                    // Should not reach here
                    return ''
                },
                name: "species__district__name",
            }
        },
        column_effective_from_date: function () {
            return {
                data: "effective_from_date",
                orderable: true,
                searchable: true, // handles by filter_queryset override method
                visible: true,
                'render': function (data, type, full) {
                    if (full.effective_from_date) {
                        return full.effective_from_date
                    }
                    // Should not reach here
                    return ''
                },
                name: "conservationstatusissuanceapprovaldetails__effective_from_date",
            }
        },
        column_effective_to_date: function () {
            return {
                data: "effective_to_date",
                orderable: true,
                searchable: true, // handles by filter_queryset override method
                visible: true,
                'render': function (data, type, full) {
                    if (full.effective_to_date) {
                        return full.effective_to_date
                    }
                    // Should not reach here
                    return ''
                },
                name: "conservationstatusissuanceapprovaldetails__effective_to_date",
            }
        },
        column_action: function () {
            let vm = this
            return {
                // 10. Action
                data: "id",
                orderable: false,
                searchable: false,
                visible: true,
                'render': function (data, type, full) {
                    let links = "";
                    if (vm.is_for_agenda == false) {
                        if (!vm.is_external) {
                            /*if(vm.check_assessor(full) && full.can_officer_process)*/
                            if (full.internal_user_edit) {
                                links += `<a href='/internal/conservation_status/${full.id}'>Continue</a><br/>`;
                                links += `<a href='#${full.id}' data-discard-cs-proposal='${full.id}'>Discard</a><br/>`;
                                links += `<a href='#' data-history-conservation-status-species='${full.id}'
                                data-history-species='${full.species_number}'
                                data-history-conservation-list='${full.conservation_list}'>History</a><br>`;
                            }
                            else {
                                if (full.assessor_process) {
                                    links += `<a href='/internal/conservation_status/${full.id}'>Process</a><br/>`;
                                    links += `<a href='#' data-history-conservation-status-species='${full.id}'
                                        data-history-species='${full.species_number}'
                                        data-history-conservation-list='${full.conservation_list}'>History</a><br>`;
                                }
                                else {
                                    if (full.assessor_edit) {
                                        links += `<a href='/internal/conservation_status/${full.id}?action=edit'>Edit</a><br/>`;
                                    }
                                    links += `<a href='/internal/conservation_status/${full.id}?action=view'>View</a><br/>`;
                                    links += `<a href='#' data-history-conservation-status-species='${full.id}'
                                    data-history-species='${full.species_number}'
                                    data-history-conservation-list='${full.conservation_list}'>History</a><br>`;
                                }
                            }
                        }
                    }
                    else {
                        if (vm.meeting_obj.agenda_items_arr.includes(full.id)) {
                            links += `<a>Added</a><br/>`;
                        }
                        else {
                            links += `<a href='#${full.id}' data-add-to-agenda='${full.id}'>Add</a><br/>`;
                        }
                    }
                    return links;
                }
            }
        },
        datatable_options: function () {
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
            if (vm.is_external) {
                columns = [
                    vm.column_number,
                    vm.column_species_number,
                    vm.column_scientific_name,
                    vm.column_common_name,
                    vm.column_conservation_list,
                    vm.column_conservation_category,
                    vm.column_region,
                    vm.column_district,
                    vm.column_effective_from_date,
                    vm.column_effective_to_date,
                    vm.column_family,
                    vm.column_genera,
                    vm.column_status,
                    vm.column_action,
                ]
                search = false
            }
            if (vm.is_internal) {
                columns = [
                    vm.column_number,
                    vm.column_species_number,
                    vm.column_scientific_name,
                    vm.column_common_name,
                    vm.column_conservation_list,
                    vm.column_conservation_category,
                    vm.column_region,
                    vm.column_district,
                    vm.column_effective_from_date,
                    vm.column_effective_to_date,
                    vm.column_family,
                    vm.column_genera,
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
                lengthMenu: [[10, 25, 50, 100, 100000000], [10, 25, 50, 100, "All"]],
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
                    "data": function (d) {
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
                        d.filter_from_effective_from_date = vm.filterCSFromFaunaEffectiveFromDate;
                        d.filter_to_effective_from_date = vm.filterCSToFaunaEffectiveFromDate;
                        d.filter_from_effective_to_date = vm.filterCSFromFaunaEffectiveToDate;
                        d.filter_to_effective_to_date = vm.filterCSToFaunaEffectiveToDate;
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
                drawCallback: function () {
                    helpers.enablePopovers();
                },
                initComplete: function () {
                    helpers.enablePopovers();
                },
            }
        }

    },
    methods: {
        historyDocument: function (id, list, species) {
            this.speciesConservationStatusHistoryId = parseInt(id);
            this.listHistoryId = list ? list : "List not specified";
            this.speciesHistoryId = species ? species : "not specified";
            this.uuid++;
            this.$nextTick(() => {
                this.$refs.species_conservation_status_history.isModalOpen = true;
            });
        },
        collapsible_component_mounted: function () {
            this.$refs.collapsible_filters.show_warning_icon(this.filterApplied)
        },
        initialiseScientificNameLookup: function () {
            let vm = this;
            $(vm.$refs.cs_scientific_name_lookup).select2({
                minimumInputLength: 2,
                dropdownParent: $("#select_scientific_name"),
                "theme": "bootstrap-5",
                allowClear: true,
                placeholder: "Select Scientific Name",
                ajax: {
                    url: api_endpoints.scientific_name_lookup,
                    dataType: 'json',
                    data: function (params) {
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
                    vm.filterCSFaunaScientificName = data; // this is id session
                    sessionStorage.setItem("filterCSFaunaScientificNameText", e.params.data.text); // this is name session
                }).
                on("select2:unselect", function (e) {
                    var selected = $(e.currentTarget);
                    vm.filterCSFaunaScientificName = 'all';
                    sessionStorage.setItem("filterCSFaunaScientificNameText", '');
                }).
                on("select2:open", function (e) {
                    const searchField = $('[aria-controls="select2-cs_scientific_name_lookup-results"]')
                    // move focus to select2 field
                    searchField[0].focus();
                });
        },
        initialiseCommonNameLookup: function () {
            let vm = this;
            $(vm.$refs.cs_common_name_lookup).select2({
                minimumInputLength: 2,
                dropdownParent: $("#select_common_name"),
                "theme": "bootstrap-5",
                allowClear: true,
                placeholder: "Select Common Name",
                ajax: {
                    url: api_endpoints.common_name_lookup,
                    dataType: 'json',
                    data: function (params) {
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
                    vm.filterCSFaunaCommonName = data;
                    sessionStorage.setItem("filterCSFaunaCommonNameText", e.params.data.text);
                }).
                on("select2:unselect", function (e) {
                    var selected = $(e.currentTarget);
                    vm.filterCSFaunaCommonName = 'all';
                    sessionStorage.setItem("filterCSFaunaCommonNameText", '');
                }).
                on("select2:open", function (e) {
                    const searchField = $('[aria-controls="select2-cs_common_name_lookup-results"]')
                    // move focus to select2 field
                    searchField[0].focus();
                });
        },
        initialisePhyloGroupLookup: function () {
            let vm = this;
            $(vm.$refs.cs_phylo_group_lookup).select2({
                minimumInputLength: 2,
                dropdownParent: $("#select_phylo_group"),
                "theme": "bootstrap-5",
                allowClear: true,
                placeholder: "Select Phylo Group",
                ajax: {
                    url: api_endpoints.phylo_group_lookup,
                    dataType: 'json',
                    data: function (params) {
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
                    vm.filterCSFaunaPhylogeneticGroup = data;
                    sessionStorage.setItem("filterCSFaunaPhylogeneticGroupText", e.params.data.text);
                }).
                on("select2:unselect", function (e) {
                    var selected = $(e.currentTarget);
                    vm.filterCSFaunaPhylogeneticGroup = 'all';
                    sessionStorage.setItem("filterCSFaunaPhylogeneticGroupText", '');
                }).
                on("select2:open", function (e) {
                    const searchField = $('[aria-controls="select2-cs_phylo_group_lookup-results"]')
                    // move focus to select2 field
                    searchField[0].focus();
                });
        },
        initialiseFamilyLookup: function () {
            let vm = this;
            $(vm.$refs.cs_family_lookup).select2({
                minimumInputLength: 2,
                dropdownParent: $("#select_family"),
                "theme": "bootstrap-5",
                allowClear: true,
                placeholder: "Select Family",
                ajax: {
                    url: api_endpoints.family_lookup,
                    dataType: 'json',
                    data: function (params) {
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
                    vm.filterCSFaunaFamily = data;
                    sessionStorage.setItem("filterCSFaunaFamilyText", e.params.data.text);
                }).
                on("select2:unselect", function (e) {
                    var selected = $(e.currentTarget);
                    vm.filterCSFaunaFamily = 'all';
                    sessionStorage.setItem("filterCSFaunaFamilyText", '');
                }).
                on("select2:open", function (e) {
                    //const searchField = $(".select2-search__field")
                    const searchField = $('[aria-controls="select2-cs_family_lookup-results"]')
                    // move focus to select2 field
                    searchField[0].focus();
                });
        },
        initialiseGeneraLookup: function () {
            let vm = this;
            $(vm.$refs.cs_genera_lookup).select2({
                minimumInputLength: 2,
                dropdownParent: $("#select_genera"),
                "theme": "bootstrap-5",
                allowClear: true,
                placeholder: "Select Genera",
                ajax: {
                    url: api_endpoints.genera_lookup,
                    dataType: 'json',
                    data: function (params) {
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
                    vm.filterCSFaunaGenus = data;
                    sessionStorage.setItem("filterCSFaunaGenusText", e.params.data.text);
                }).
                on("select2:unselect", function (e) {
                    var selected = $(e.currentTarget);
                    vm.filterCSFaunaGenus = 'all';
                    sessionStorage.setItem("filterCSFaunaGenusText", '');
                }).
                on("select2:open", function (e) {
                    //const searchField = $(".select2-search__field")
                    const searchField = $('[aria-controls="select2-cs_genera_lookup-results"]')
                    // move focus to select2 field
                    searchField[0].focus();
                });
        },
        fetchFilterLists: function () {
            let vm = this;
            //large FilterList of Species Values object
            vm.$http.get(api_endpoints.filter_lists_species + '?group_type_name=' + vm.group_type_name).then((response) => {
                vm.filterListsSpecies = response.body;
                vm.scientific_name_list = vm.filterListsSpecies.scientific_name_list;
                vm.common_name_list = vm.filterListsSpecies.common_name_list;
                vm.family_list = vm.filterListsSpecies.family_list;
                vm.genus_list = vm.filterListsSpecies.genus_list;
                vm.phylogenetic_group_list = vm.filterListsSpecies.phylogenetic_group_list;
                vm.conservation_list_dict = vm.filterListsSpecies.conservation_list_dict;
                vm.conservation_category_list = vm.filterListsSpecies.conservation_category_list;
                vm.filterConservationCategory();
                vm.filterDistrict();
                vm.proposal_status = vm.internal_status.slice().sort((a, b) => {
                    return a.name.trim().localeCompare(b.name.trim());
                });
                //vm.proposal_status = vm.level == 'internal' ? response.body.processing_status_choices: response.body.customer_status_choices;
                //vm.proposal_status = vm.level == 'internal' ? vm.internal_status: vm.external_status;
            }, (error) => {
                console.log(error);
            })
            vm.$http.get(api_endpoints.region_district_filter_dict).then((response) => {
                vm.filterRegionDistrict = response.body;
                vm.region_list = vm.filterRegionDistrict.region_list;
                vm.district_list = vm.filterRegionDistrict.district_list;
            }, (error) => {
                console.log(error);
            })
        },
        //-------filter category dropdown dependent on conservation_list selected
        filterConservationCategory: function (event) {
            //this.$nextTick(() => {
            if (event) {
                this.filterCSFaunaConservationCategory = 'all'; //-----to remove the previous selection
            }
            this.filtered_conservation_category_list = [];
            //---filter conservation_categories as per cons_list selected
            for (let choice of this.conservation_category_list) {
                if (choice.conservation_list_id.toString() === this.filterCSFaunaConservationList.toString()) {
                    this.filtered_conservation_category_list.push(choice);
                }
            }
            //});
        },
        //-------filter district dropdown dependent on region selected
        filterDistrict: function (event) {
            this.$nextTick(() => {
                if (event) {
                    this.filterCSFaunaDistrict = 'all'; //-----to remove the previous selection
                }
                this.filtered_district_list = [];
                //---filter districts as per region selected
                for (let choice of this.district_list) {
                    if (choice.region_id.toString() === this.filterCSFaunaRegion.toString()) {
                        this.filtered_district_list.push(choice);
                    }

                }
            });
        },
        createFaunaConservationStatus: async function () {
            let newFaunaCSId = null
            try {
                const createUrl = api_endpoints.conservation_status + "/";
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
                params: { conservation_status_id: newFaunaCSId },
            });
        },
        discardCSProposal: function (conservation_status_id) {
            let vm = this;
            swal.fire({
                title: "Discard Application",
                text: "Are you sure you want to discard this proposal?",
                icon: "warning",
                showCancelButton: true,
                confirmButtonText: 'Discard Application',
                confirmButtonColor: '#d9534f'
            }).then((result) => {
                if (result.isConfirmed) {
                    vm.$http.delete(api_endpoints.discard_cs_proposal(conservation_status_id))
                        .then((response) => {
                            swal.fire({
                                title: 'Discarded',
                                text: 'Your proposal has been discarded',
                                icon: 'success',
                                confirmButtonColor: '#226fbb',
                            });
                            vm.$refs.fauna_cs_datatable.vmDataTable.ajax.reload(helpers.enablePopovers, false);
                        }, (error) => {
                            console.log(error);
                        });
                }
            }, (error) => {

            });
        },
        addToMeetingAgenda: function (conservation_status_id) {
            let vm = this;
            let payload = new Object();
            payload.conservation_status_id = conservation_status_id;
            Vue.http.post(`/api/meeting/${vm.meeting_obj.id}/add_agenda_item.json`, payload).then(res => {
                vm.meeting_obj.agenda_items_arr = res.body;
                vm.$refs.fauna_cs_datatable.vmDataTable.ajax.reload(helpers.enablePopovers, false);
                this.$emit('updateAgendaItems');
            },
                err => {
                    console.log(err);
                });
        },
        addEventListeners: function () {
            let vm = this;
            // External Discard listener
            vm.$refs.fauna_cs_datatable.vmDataTable.on('click', 'a[data-discard-cs-proposal]', function (e) {
                e.preventDefault();
                var id = $(this).attr('data-discard-cs-proposal');
                vm.discardCSProposal(id);
            });
            vm.$refs.fauna_cs_datatable.vmDataTable.on('click', 'a[data-add-to-agenda]', function (e) {
                e.preventDefault();
                var id = $(this).attr('data-add-to-agenda');
                vm.addToMeetingAgenda(id);
            });
            vm.$refs.fauna_cs_datatable.vmDataTable.on('click', 'a[data-history-conservation-status-species]', function (e) {
                e.preventDefault();
                var id = $(this).attr('data-history-conservation-status-species');
                var list = $(this).attr('data-history-conservation-list');
                var species = $(this).attr('data-history-species');
                vm.historyDocument(id, list, species);
            });
            vm.$refs.fauna_cs_datatable.vmDataTable.on('childRow.dt', function (e, settings) {
                helpers.enablePopovers();
            });
        },
        initialiseSearch: function () {
            this.submitterSearch();
        },
        submitterSearch: function () {
            let vm = this;
            vm.$refs.fauna_cs_datatable.table.dataTableExt.afnFiltering.push(
                function (settings, data, dataIndex, original) {
                    let filtered_submitter = vm.filterProposalSubmitter;
                    if (filtered_submitter == 'All') { return true; }
                    return filtered_submitter == original.submitter.email;
                }
            );
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
                    "name": "species__taxonomy__family_name",
                    "searchable": "true",
                    "orderable": "true",
                    "search": {
                        "value": "",
                        "regex": "false"
                    }
                },
                "6": {
                    "data": "genus",
                    "name": "species__taxonomy__genera_name",
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
                filter_scientific_name: vm.filterCSFaunaScientificName,
                filter_common_name: vm.filterCSFaunaCommonName,
                filter_family: vm.filterCSFaunaFamily,
                filter_phylogenetic_group: vm.filterCSFaunaPhylogeneticGroup,
                filter_genus: vm.filterCSFaunaGenus,
                filter_conservation_list: vm.filterCSFaunaConservationList,
                filter_conservation_category: vm.filterCSFaunaConservationCategory,
                filter_application_status: vm.filterCSFaunaApplicationStatus,
                filter_region: vm.filterCSFaunaRegion,
                filter_district: vm.filterCSFaunaDistrict,
                filter_from_effective_from_date: vm.filterCSFromFaunaEffectiveFromDate,
                filter_to_effective_from_date: vm.filterCSToFaunaEffectiveFromDate,
                filter_effective_to_date: vm.filterCSFromFaunaEffectiveToDate,
                filter_effective_to_date: vm.filterCSToFaunaEffectiveToDate,
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
    mounted: function () {
        this.fetchFilterLists();
        let vm = this;
        $('a[data-toggle="collapse"]').on('click', function () {
            var chev = $(this).children()[0];
            window.setTimeout(function () {
                $(chev).toggleClass("glyphicon-chevron-down glyphicon-chevron-up");
            }, 100);
        });
        this.$nextTick(() => {
            vm.initialiseScientificNameLookup();
            vm.initialiseCommonNameLookup();
            vm.initialisePhyloGroupLookup();
            vm.initialiseFamilyLookup();
            vm.initialiseGeneraLookup();
            //vm.initialiseSearch();
            vm.addEventListeners();

            // -- to set the select2 field with the session value if exists onload()
            if (sessionStorage.getItem("filterCSFaunaScientificName") != 'all' && sessionStorage.getItem("filterCSFaunaScientificName") != null) {
                // contructor new Option(text, value, defaultSelected, selected)
                var newOption = new Option(sessionStorage.getItem("filterCSFaunaScientificNameText"), vm.filterCSFaunaScientificName, false, true);
                $('#cs_scientific_name_lookup').append(newOption);
                //$('#scientific_name_lookup').append(newOption).trigger('change');
            }
            if (sessionStorage.getItem("filterCSFaunaCommonName") != 'all' && sessionStorage.getItem("filterCSFaunaCommonName") != null) {
                // contructor new Option(text, value, defaultSelected, selected)
                var newOption = new Option(sessionStorage.getItem("filterCSFaunaCommonNameText"), vm.filterCSFaunaCommonName, false, true);
                $('#cs_common_name_lookup').append(newOption);
            }
            if (sessionStorage.getItem("filterCSFaunaPhylogeneticGroup") != 'all' && sessionStorage.getItem("filterCSFaunaPhylogeneticGroup") != null) {
                // contructor new Option(text, value, defaultSelected, selected)
                var newOption = new Option(sessionStorage.getItem("filterCSFaunaPhylogeneticGroupText"), vm.filterCSFaunaPhylogeneticGroup, false, true);
                $('#cs_phylo_group_lookup').append(newOption);
            }
            if (sessionStorage.getItem("filterCSFaunaFamily") != 'all' && sessionStorage.getItem("filterCSFaunaFamily") != null) {
                // contructor new Option(text, value, defaultSelected, selected)
                var newOption = new Option(sessionStorage.getItem("filterCSFaunaFamilyText"), vm.filterCSFaunaFamily, false, true);
                $('#cs_family_lookup').append(newOption);
            }
            if (sessionStorage.getItem("filterCSFaunaGenus") != 'all' && sessionStorage.getItem("filterCSFaunaGenus") != null) {
                // contructor new Option(text, value, defaultSelected, selected)
                var newOption = new Option(sessionStorage.getItem("filterCSFaunaGenusText"), vm.filterCSFaunaGenus, false, true);
                $('#cs_genera_lookup').append(newOption);
            }
        });
    }
}
</script>
<style scoped>
.dt-buttons {
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
