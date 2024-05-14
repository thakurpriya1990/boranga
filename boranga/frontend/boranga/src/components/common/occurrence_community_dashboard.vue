<template id="communities_occ_dashboard">
    <div>
        <CollapsibleFilters component_title="Filters" ref="collapsible_filters" @created="collapsible_component_mounted" class="mb-2">
            <div class="row">
                <div class="col-md-4">
                    <div class="form-group" id="occurrence_name_lookup_form_group_id">
                        <label for="occurrence_name_lookup">Name of Occurrence:</label>
                        <select id="occurrence_name_lookup"
                            name="occurrence_name_lookup" ref="occurrence_name_lookup"
                            class="form-control" />
                    </div>
                </div>
                <div class="col-md-4">
                    <div class="form-group" id="select_occ_community_name">
                        <label for="occ_community_name_lookup">Community Name:</label>
                            <select
                                id="occ_community_name_lookup"
                                name="occ_community_name_lookup"
                                ref="occ_community_name_lookup"
                                class="form-control" />
                    </div>
                </div>
                <div class="col-md-4">
                    <div class="form-group" id="select_status">
                        <label for="occ_status_lookup">Status:</label>
                        <select class="form-select" v-model="filterOCCCommunityStatus">
                                <option value="all">All</option>
                                <option v-for="status in proposal_status" :value="status.value">{{ status.name }}</option>
                            </select>
                    </div>
                </div>

                <div class="col-md-3" >
                    <div class="form-group">
                        <label for="">Effective From Date Range:</label>
                        <input type="date" class="form-control" placeholder="DD/MM/YYYY" id="from_effective_from_date" v-model="filterOCCFromCommunityEffectiveFromDate">
                    </div>
                </div>
                <div class="col-md-3" >
                    <div class="form-group">
                        <label for=""></label>
                        <input type="date" class="form-control" placeholder="DD/MM/YYYY" id="to_effective_from_date" v-model="filterOCCToCommunityEffectiveFromDate">
                    </div>
                </div>
                
                <div class="col-md-3" >
                    <div class="form-group">
                        <label for="">Effective To Date Range:</label>
                        <input type="date" class="form-control" placeholder="DD/MM/YYYY" id="from_effective_to_date" v-model="filterOCCFromCommunityEffectiveToDate">
                    </div>
                </div>

                <div class="col-md-3" >
                    <div class="form-group">
                        <label for=""></label>
                        <input type="date" class="form-control" placeholder="DD/MM/YYYY" id="to_effective_to_date" v-model="filterOCCToCommunityEffectiveToDate">
                    </div>
                </div>

                <!--<div class="col-md-3" >
                    <div class="form-group">
                        <label for="">Due Date Range:</label>
                        <input type="date" class="form-control" placeholder="DD/MM/YYYY" id="from_due_date" v-model="filterOCCFromCommunityDueDate">
                    </div>
                </div>

                <div class="col-md-3" >
                    <div class="form-group">
                        <label for=""></label>
                        <input type="date" class="form-control" placeholder="DD/MM/YYYY" id="to_due_date" v-model="filterOCCToCommunityDueDate">
                    </div>
                </div>-->
            </div>
        </CollapsibleFilters>

        <div class="col-md-12">
            <div class="text-end">
                <button type="button" class="btn btn-primary mb-2 " @click.prevent="createCommunityOccurrence"><i class="fa-solid fa-circle-plus"></i> Add Community Occurrence</button>
            </div>
        </div>

        <div class="row">
            <div class="col-lg-12">
                <datatable
                        ref="community_occ_datatable"
                        :id="datatable_id"
                        :dtOptions="datatable_options"
                        :dtHeaders="datatable_headers"
                    />
            </div>
            <div v-if="occurrenceHistoryId">
                <OccurrenceReportHistory
                    ref="occurrence_history"
                    :key="occurrenceHistoryId"
                    :occurrence-id="occurrenceHistoryId"
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
import OccurrenceReportHistory from '../internal/occurrence/community_occurrence_history.vue';
import Vue from 'vue'
import {
    api_endpoints,
    constants,
    helpers
}from '@/utils/hooks'
export default {
    name: 'OccurrenceReportCommunityTable',
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
        filterOCCCommunityOccurrenceName_cache: {
            type: String,
            required: false,
            default: 'filterOCCCommunityOccurrenceName',
        },
        filterOCCCommunityName_cache: {
            type: String,
            required: false,
            default: 'filterOCCCommunityName',
        },
        filterOCCCommunityStatus_cache: {
            type: String,
            required: false,
            default: 'filterOCCCommunityStatus',
        },
        filterOCCFromCommunityEffectiveFromDate_cache: {
            type: String,
            required: false,
            default: 'filterOCCFromCommunityEffectiveFromDate',
        },
        filterOCCToCommunityEffectiveFromDate_cache: {
            type: String,
            required: false,
            default: 'filterOCCToCommunityEffectiveFromDate',
        },
        filterOCCFromCommunityEffectiveToDate_cache: {
            type: String,
            required: false,
            default: 'filterOCCFromCommunityEffectiveToDate',
        },
        filterOCCToCommunityEffectiveToDate_cache: {
            type: String,
            required: false,
            default: 'filterOCCToCommunityEffectiveToDate',
        },
        filterOCCFromCommunityDueDate_cache: {
            type: String,
            required: false,
            default: 'filterOCCFromCommunityDueDate',
        },
        filterOCCToCommunityDueDate_cache: {
            type: String,
            required: false,
            default: 'filterOCCToCommunityDueDate',
        },
    },
    data() {
        let vm = this;
        return {
            uuid:0,
            occurrenceHistoryId: null,
            datatable_id: 'community_ocr-datatable-'+vm._uid,

            //Profile to check if user has access to process Proposal
            profile: {},
            is_payment_admin: false,

            // selected values for filtering
            filterOCCCommunityOccurrenceName: sessionStorage.getItem(this.filterOCCCommunityOccurrenceName_cache) ?
                        sessionStorage.getItem(this.filterOCCCommunityOccurrenceName_cache) : 'all',

            filterOCCCommunityName: sessionStorage.getItem(this.filterOCCCommunityName_cache) ?
                        sessionStorage.getItem(this.filterOCCCommunityName_cache) : 'all',

            filterOCCCommunityStatus: sessionStorage.getItem(this.filterOCCCommunityStatus_cache) ?
                        sessionStorage.getItem(this.filterOCCCommunityStatus_cache) : 'all',

            filterOCCFromCommunityEffectiveFromDate: sessionStorage.getItem(this.filterOCCFromCommunityEffectiveFromDate_cache) ?
            sessionStorage.getItem(this.filterOCCFromCommunityEffectiveFromDate_cache) : '',
            filterOCCToCommunityEffectiveFromDate: sessionStorage.getItem(this.filterOCCToCommunityEffectiveFromDate_cache) ?
            sessionStorage.getItem(this.filterOCCToCommunityEffectiveFromDate_cache) : '',

            filterOCCFromCommunityEffectiveToDate: sessionStorage.getItem(this.filterOCCFromCommunityEffectiveToDate_cache) ?
            sessionStorage.getItem(this.filterOCCFromCommunityEffectiveToDate_cache) : '',
            filterOCCToCommunityEffectiveToDate: sessionStorage.getItem(this.filterOCCToCommunityEffectiveToDate_cache) ?
            sessionStorage.getItem(this.filterOCCToCommunityEffectiveToDate_cache) : '',

            filterOCCFromCommunityDueDate: sessionStorage.getItem(this.filterOCCFromCommunityDueDate_cache) ?
            sessionStorage.getItem(this.filterOCCFromCommunityDueDate_cache) : '',
            filterOCCToCommunityDueDate: sessionStorage.getItem(this.filterOCCToCommunityDueDate_cache) ?
            sessionStorage.getItem(this.filterOCCToCommunityDueDate_cache) : '',

            filterListsCommunity: {},
            occurrence_list: [],
            community_name_list: [],
            status_list: [],
            submissions_from_list: [],
            submissions_to_list: [],

            // filtering options
            // external_status refers to CUSTOMER_STATUS_CHOICES
            // internal_status referes to PROCESSING_STATUS_CHOICES
            internal_status:[
                {value: 'active', name: 'Active'},
                {value: 'locked', name: 'Locked'},
                {value: 'historical', name: 'Historical'},
            ],

            proposal_status: [],

            proposal_status: [],

        }
    },
    components:{
        datatable,
        CollapsibleFilters,
        FormSection,
        OccurrenceReportHistory,
    },
    watch:{
        filterOCCCommunityOccurrenceName: function(){
            let vm = this;
            vm.$refs.community_occ_datatable.vmDataTable.ajax.reload(helpers.enablePopovers,false); // This calls ajax() backend call.
            sessionStorage.setItem(vm.filterOCCCommunityOccurrenceName_cache, vm.filterOCCCommunityOccurrenceName);
        },
        filterOCCCommunityName: function() {
            let vm = this;
            vm.$refs.community_occ_datatable.vmDataTable.ajax.reload(helpers.enablePopovers,false); // This calls ajax() backend call.
            sessionStorage.setItem(vm.filterOCCCommunityName_cache, vm.filterOCCCommunityName);
        },
        filterOCCCommunityStatus: function() {
            let vm = this;
            vm.$refs.community_occ_datatable.vmDataTable.ajax.reload(helpers.enablePopovers,false); // This calls ajax() backend call.
            sessionStorage.setItem(vm.filterOCCCommunityStatus_cache, vm.filterOCCCommunityStatus);
        },
        filterApplied: function(){
            if (this.$refs.collapsible_filters){
                // Collapsible component exists
                this.$refs.collapsible_filters.show_warning_icon(this.filterApplied)
            }
        },
        filterOCCFromCommunityEffectiveFromDate: function(){
            let vm = this;
            vm.$refs.community_occ_datatable.vmDataTable.ajax.reload(helpers.enablePopovers,false); // This calls ajax() backend call.
            sessionStorage.setItem(vm.filterOCCFromCommunityEffectiveFromDate_cache, vm.filterOCCFromCommunityEffectiveFromDate);
        },
        filterOCCToCommunityEffectiveFromDate: function(){
            let vm = this;
            vm.$refs.community_occ_datatable.vmDataTable.ajax.reload(helpers.enablePopovers,false); // This calls ajax() backend call.
            sessionStorage.setItem(vm.filterOCCToCommunityEffectiveFromDate_cache, vm.filterOCCToCommunityEffectiveFromDate);
        },
        filterOCCFromCommunityEffectiveToDate: function(){
            let vm = this;
            vm.$refs.community_occ_datatable.vmDataTable.ajax.reload(helpers.enablePopovers,false); // This calls ajax() backend call.
            sessionStorage.setItem(vm.filterOCCFromCommunityEffectiveToDate_cache, vm.filterOCCFromCommunityEffectiveToDate);
        },
        filterOCCToCommunityEffectiveToDate: function(){
            let vm = this;
            vm.$refs.community_occ_datatable.vmDataTable.ajax.reload(helpers.enablePopovers,false); // This calls ajax() backend call.
            sessionStorage.setItem(vm.filterOCCToCommunityEffectiveToDate_cache, vm.filterOCCToCommunityEffectiveToDate);
        },
        filterOCCFromCommunityDueDate: function(){
            let vm = this;
            vm.$refs.community_occ_datatable.vmDataTable.ajax.reload(helpers.enablePopovers,false); // This calls ajax() backend call.
            sessionStorage.setItem(vm.filterOCCFromCommunityDueDate_cache, vm.filterOCCFromCommunityDueDate);
        },
        filterOCCToCommunityDueDate: function(){
            let vm = this;
            vm.$refs.community_occ_datatable.vmDataTable.ajax.reload(helpers.enablePopovers,false); // This calls ajax() backend call.
            sessionStorage.setItem(vm.filterOCCToCommunityDueDate_cache, vm.filterOCCToCommunityDueDate);
        },
    },
    computed: {
        filterApplied: function(){
            if(this.filterOCCCommunityOccurrenceName === 'all' &&
                this.filterOCCCommunityName === 'all' &&
                this.filterOCCCommunityStatus === 'all' &&
                this.filterOCCFromCommunityEffectiveFromDate === '' &&
                this.filterOCCToCommunityEffectiveFromDate === '' &&
                this.filterOCCFromCommunityEffectiveToDate === '' &&
                this.filterOCCToCommunityEffectiveToDate === '' &&
                this.filterOCCFromCommunityDueDate === '' &&
                this.filterOCCToCommunityDueDate === ''){
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
        addCommunityOCCVisibility: function() {
            let visibility = false;
            if (this.is_internal) {
                visibility = true;
            }
            return visibility;
        },
        datatable_headers: function(){
            if (this.is_internal){
                return ['Number','Name of Occurrence','Community Name', 'Wild Status', 'Number of Reports',  'Effective From', 'Effective To', 'Review Due', 'Status', 'Action']
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
                data: "occurrence_number",
                orderable: true,
                searchable: true,
                visible: true,
                name: "occurrence_number",
            }
        },
        column_occurrence_name: function(){
            return {
                data: "occurrence_name",
                orderable: true,
                searchable: true,
                visible: true,
                name: "occurrence_name",
            }
        },
        column_community_name: function(){
            return {
                data: "community_name",
                orderable: true,
                searchable: true,
                visible: true,
                name: "community__taxonomy__community_name",
            }
        },
        column_number_of_reports: function(){
            return {
                data: "number_of_reports",
                orderable: true,
                searchable: false,
                visible: true,
            }
        },
        column_wild_status: function(){
            return {
                data: "wild_status",
                orderable: false,
                searchable: false,
                visible: true,
            }
        },
        column_effective_from: function(){
            return {
                data: "effective_from",
                orderable: true,
                searchable: true,
                visible: true,
                name: "effective_from",
            }
        },
        column_effective_to: function(){
            return {
                data: "effective_to",
                orderable: true,
                searchable: true,
                visible: true,
                name: "effective_to",
            }
        },
        column_review_due_date: function(){
            return {
                data: "review_due_date",
                orderable: true,
                searchable: true,
                visible: true,
                name: "review_due_date",
            }
        },
        column_status: function(){
            return {
                data: "processing_status_display",
                orderable: true,
                searchable: true,
                visible: true,
                'render': function(data, type, full){
                    if (full.processing_status_display){
                        return full.processing_status_display;
                    }
                    return ''
                },
                name: "processing_status",
            }
        },
        // TODO update this to suit the design
        column_action: function(){
            let vm = this
            return {
                data: "id",
                orderable: false,
                searchable: false,
                visible: true,
                'render': function(data, type, full){
                    let links = "";
                    if (vm.is_internal) {                        
                        if (full.can_user_edit) {
                            links += `<a href='/internal/occurrence/${full.id}?group_type_name=${vm.group_type_name}&action=edit'>Edit</a><br/>`;
                        } else {
                            links += `<a href='/internal/occurrence/${full.id}?group_type_name=${vm.group_type_name}&action=view'>View</a><br/>`;
                        }
                        links += `<a href='#' data-history-occurrence='${full.id}'>History</a><br>`;                       
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
                    extend: 'excel',
                    text: '<i class="fa-solid fa-download"></i> Excel',
                    className: 'btn btn-primary me-2 rounded',
                },
                {
                    extend: 'csv',
                    text: '<i class="fa-solid fa-download"></i> CSV',
                    className: 'btn btn-primary rounded',
                }
            ]
            if(vm.is_internal){
                columns = [
                    vm.column_number,
                    vm.column_occurrence_name,
                    vm.column_community_name,
                    vm.column_wild_status,
                    vm.column_number_of_reports,
                    vm.column_effective_from,
                    vm.column_effective_to,
                    vm.column_review_due_date,
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
                        d.filter_occurrence_name = vm.filterOCCCommunityOccurrenceName;
                        d.filter_community_name = vm.filterOCCCommunityName;
                        d.filter_status = vm.filterOCCCommunityStatus;
                        d.filter_from_effective_from_date = vm.filterOCCFromCommunityEffectiveFromDate;
                        d.filter_to_effective_from_date = vm.filterOCCToCommunityEffectiveFromDate;
                        d.filter_from_effective_to_date = vm.filterOCCFromCommunityEffectiveToDate;
                        d.filter_to_effective_to_date = vm.filterOCCToCommunityEffectiveToDate;
                        d.filter_from_due_date = vm.filterOCCFromCommunityDueDate;
                        d.filter_to_due_date = vm.filterOCCToCommunityDueDate;
                        d.is_internal = vm.is_internal;
                    }
                },
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
                this.occurrenceHistoryId = parseInt(id);
                this.uuid++;
                this.$nextTick(() => {
                    this.$refs.occurrence_history.isModalOpen = true;
                });
            },
        collapsible_component_mounted: function(){
            this.$refs.collapsible_filters.show_warning_icon(this.filterApplied)
        },
        initialiseOccurrenceNameLookup: function(){
                let vm = this;
                $(vm.$refs.occurrence_name_lookup).select2({
                    minimumInputLength: 2,
                    dropdownParent: $("#occurrence_name_lookup_form_group_id"),
                    "theme": "bootstrap-5",
                    allowClear: true,
                    placeholder:"Select Occurrence Name",
                    ajax: {
                        url: api_endpoints.occurrence_name_lookup,
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
                    let data = e.params.data.text;
                    vm.filterOCCCommunityOccurrenceName = data;
                    sessionStorage.setItem("filterOCCCommunityOccurrenceNameText", e.params.data.text);
                }).
                on("select2:unselect",function (e) {
                    var selected = $(e.currentTarget);
                    vm.filterOCCCommunityOccurrenceName = 'all';
                    sessionStorage.setItem("filterOCCCommunityOccurrenceNameText",'');
                }).
                on("select2:open",function (e) {
                    const searchField = $('[aria-controls="select2-occurrence_name_lookup-results"]')
                    searchField[0].focus();
                });
        },
        initialiseCommunityNameLookup: function(){
                let vm = this;
                $(vm.$refs.occ_community_name_lookup).select2({
                    minimumInputLength: 2,
                    dropdownParent: $("#select_occ_community_name"),
                    theme: 'bootstrap-5',
                    allowClear: true,
                    placeholder:"Select Community Name",
                    ajax: {
                        url: api_endpoints.community_name_lookup,
                        dataType: 'json',
                        data: function(params) {
                            var query = {
                                term: params.term,
                                type: 'public',
                            }
                            return query;
                        },
                    },
                }).
                on("select2:select", function (e) {
                    var selected = $(e.currentTarget);
                    let data = e.params.data.id;
                    vm.filterOCCCommunityName = data;
                    sessionStorage.setItem("filterOCCCommunityNameText", e.params.data.text);
                }).
                on("select2:unselect",function (e) {
                    var selected = $(e.currentTarget);
                    vm.filterOCCCommunityName = 'all';
                    sessionStorage.setItem("filterOCCCommunityNameText",'');
                }).
                on("select2:open",function (e) {
                    const searchField = $('[aria-controls="select2-occ_community_name_lookup-results"]')
                    searchField[0].focus();
                });
        },
        fetchFilterLists: function(){
            let vm = this;
            //large FilterList of Community Values object

            //TODO occurrence status filters...

            vm.$http.get(api_endpoints.community_filter_dict+ '?group_type_name=' + vm.group_type_name).then((response) => {
                vm.filterListsCommunity = response.body;
                vm.occurrence_list = vm.filterListsCommunity.occurrence_list;
                vm.community_name_list = vm.filterListsCommunity.community_name_list;
                vm.status_list = vm.filterListsCommunity.status_list;
                vm.submissions_from_list = vm.filterListsCommunity.submissions_from_list;
                vm.submissions_to_list = vm.filterListsCommunity.submissions_to_list;
                vm.proposal_status = vm.internal_status.slice().sort((a, b) => {
                        return a.name.trim().localeCompare(b.name.trim());
                    });
                //vm.proposal_status = vm.level == 'internal' ? response.body.processing_status_choices: response.body.customer_status_choices;
                //vm.proposal_status = vm.level == 'internal' ? vm.internal_status: vm.external_status;
            },(error) => {
                console.log(error);
            })
        },
        createCommunityOccurrence: async function () {
            let newCommunityOCCId = null
            try {
                    const createUrl = api_endpoints.occurrence;
                    let payload = new Object();
                    payload.group_type_id = this.group_type_id
                    payload.internal_application = true
                    let savedCommunityOCC = await Vue.http.post(createUrl, payload);
                    if (savedCommunityOCC) {
                        newCommunityOCCId = savedCommunityOCC.body.id;
                    }
                }
            catch (err) {
                console.log(err);
                if (this.is_internal) {
                    return err;
                }
            }
            this.$router.push({
                name: 'internal-occurrence-detail',
                params: {occurrence_id: newCommunityOCCId},
                });
        },
        discardOCCProposal:function (occurrence_id) {
            let vm = this;
            swal.fire({
                title: "Discard Report",
                text: "Are you sure you want to discard this report?",
                icon: "warning",
                showCancelButton: true,
                confirmButtonText: 'Discard Report',
                confirmButtonColor:'#d9534f'
            }).then((swalresult) => {
                if(swalresult.isConfirmed){
                    vm.$http.delete(api_endpoints.discard_occ_proposal(occurrence_id))
                    .then((response) => {
                        swal.fire({
                            title: 'Discarded',
                            text: 'Your report has been discarded',
                            icon: 'success',
                            confirmButtonColor:'#226fbb',
                        });
                        vm.$refs.community_occ_datatable.vmDataTable.ajax.reload(helpers.enablePopovers,false);
                    }, (error) => {
                        console.log(error);
                    });
                }
            },(error) => {

            });
        },
        addEventListeners: function(){
            let vm = this;
            // internal Discard listener
            vm.$refs.community_occ_datatable.vmDataTable.on('click', 'a[data-discard-ocr-proposal]', function(e) {
                e.preventDefault();
                var id = $(this).attr('data-discard-ocr-proposal');
                vm.discardOCCProposal(id);
            });
            vm.$refs.community_occ_datatable.vmDataTable.on('click', 'a[data-history-occurrence]', function(e) {
                    e.preventDefault();
                    var id = $(this).attr('data-history-occurrence');
                    vm.historyDocument(id);
                });
            vm.$refs.community_occ_datatable.vmDataTable.on('childRow.dt', function (e, settings) {
                helpers.enablePopovers();
            });
        },
        initialiseSearch:function(){
            this.submitterSearch();
        },
        submitterSearch:function(){
            let vm = this;
            vm.$refs.community_occ_datatable.table.dataTableExt.afnFiltering.push(
                function(settings,data,dataIndex,original){
                    let filtered_submitter = vm.filterProposalSubmitter;
                    if (filtered_submitter == 'All'){ return true; }
                    return filtered_submitter == original.submitter.email;
                }
            );
        },
        exportData: function (format) {
            let vm = this;
            const columns_new = {
                "0": {
                    "data": "occurrence",
                    "name": "occurrence__id, occurrence__occurrence_number",
                    "orderable": "true",
                    "search": {
                        "regex": "false",
                        "value": ""
                    },
                    "searchable": "false"
                },
                "1": {
                    "data": "occurrence",
                    "name": "occurrence__occurence",
                    "orderable": "true",
                    "search": {
                        "regex": "false",
                        "value": ""
                    },
                    "searchable": "true"
                },
                "2": {
                    "data": "community_name",
                    "name": "occurrence__community__taxonomy__community_name",
                    "orderable": "true",
                    "search": {
                        "regex": "false",
                        "value": ""
                    },
                    "searchable": "true"
                },
                "3": {
                    "data": "reported_date",
                    "name": "occurrence__reported_date",
                    "searchable": "true",
                    "orderable": "true",
                    "search": {
                        "value": "",
                        "regex": "false"
                    }
                },
                "4": {
                    "data": "submitter",
                    // "name": "occurrence__submitter",
                    "searchable": "true",
                    "orderable": "true",
                    "search": {
                        "value": "",
                        "regex": "false"
                    }
                },
                "5": {
                    "data": "processing_status",
                    "name": "occurrence__processing_status",
                    "searchable": "true",
                    "orderable": "true",
                    "search": {
                        "value": "",
                        "regex": "false"
                    }
                },
            };

            const object_load = {
                columns: columns_new,
                filter_group_type: vm.group_type_name,
                filter_occurrence_name: vm.filterOCCCommunityOccurrenceName,
                filter_community_name: vm.filterOCCCommunityName,
                filter_status: vm.filterOCCCommunityStatus,
                filter_from_effective_from_date: vm.filterOCCFromCommunityEffectiveFromDate,
                filter_to_effective_from_date: vm.filterOCCToCommunityEffectiveFromDate,
                filter_from_effective_to_date: vm.filterOCCFromCommunityEffectiveToDate,
                filter_to_effective_to_date: vm.filterOCCToCommunityEffectiveToDate,
                filter_from_due_date: vm.filterOCCFromCommunityDueDate,
                filter_to_due_date: vm.filterOCCToCommunityDueDate,
                is_internal: vm.is_internal,
                export_format: format
            };

            const url = api_endpoints.community_occurrence_internal_export;
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
        let vm = this;
        $( 'a[data-toggle="collapse"]' ).on( 'click', function () {
            var chev = $( this ).children()[ 0 ];
            window.setTimeout( function () {
                $( chev ).toggleClass( "glyphicon-chevron-down glyphicon-chevron-up" );
            }, 100 );
        });
        this.$nextTick(() => {
            vm.initialiseOccurrenceNameLookup();
            vm.initialiseCommunityNameLookup();
            vm.addEventListeners();

            // -- to set the select2 field with the session value if exists onload()
            if(sessionStorage.getItem("filterOCCCommunityOccurrenceName")!='all' && sessionStorage.getItem("filterOCCCommunityOccurrenceName")!=null)
            {
                // contructor new Option(text, value, defaultSelected, selected)
                var newOption = new Option(sessionStorage.getItem("filterOCCCommunityOccurrenceNameText"), vm.filterOCCCommunityOccurrenceName, false, true);
                $('#occ_occurrence_lookup').append(newOption);
                //$('#scientific_name_lookup').append(newOption).trigger('change');
            }
            if(sessionStorage.getItem("filterOCCCommunityName")!='all' && sessionStorage.getItem("filterOCCCommunityName")!=null)
            {
                // contructor new Option(text, value, defaultSelected, selected)
                var newOption = new Option(sessionStorage.getItem("filterOCCCommunityNameText"), vm.filterOCCCommunityName, false, true);
                $('#occ_community_name_lookup').append(newOption);
            }
        });
    }
}
</script>
<style scoped>
.dt-buttons{
    float: right;
}
</style>
