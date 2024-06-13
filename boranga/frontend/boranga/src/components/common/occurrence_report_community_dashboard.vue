<template id="communities_ocr_dashboard">
    <div>
        <CollapsibleFilters component_title="Filters" ref="collapsible_filters" @created="collapsible_component_mounted" class="mb-2">
            <div class="row">
                <div class="col-md-4">
                    <div class="form-group" id="select_occurrence">
                        <label for="ocr_occurrence_lookup">Occurrence:</label>
                            <select
                                id="ocr_occurrence_lookup"
                                name="ocr_occurrence_lookup"
                                ref="ocr_occurrence_lookup"
                                class="form-control" />
                    </div>
                </div>
                <div class="col-md-4">
                    <div class="form-group" id="select_ocr_community_name">
                        <label for="ocr_community_name_lookup">Community Name:</label>
                            <select
                                id="ocr_community_name_lookup"
                                name="ocr_community_name_lookup"
                                ref="ocr_community_name_lookup"
                                class="form-control" />
                    </div>
                </div>
                <div class="col-md-4">
                    <div class="form-group" id="select_status">
                        <label for="ocr_status_lookup">Status:</label>
                        <select class="form-select" v-model="filterOCRCommunityStatus">
                                <option value="all">All</option>
                                <option v-for="status in proposal_status" :value="status.value">{{ status.name }}</option>
                            </select>
                    </div>
                </div>
                <div class="col-md-3">
                    <div class="form-group">
                        <label for="">Submitted Date Range:</label>
                        <input type="date" class="form-control" placeholder="DD/MM/YYYY" id="submitted_from_date" v-model="filterOCRCommunitySubmittedFromDate">
                    </div>
                </div>
                <div class="col-md-3">
                    <div class="form-group">
                        <label for=""></label>
                        <input type="date" class="form-control" placeholder="DD/MM/YYYY" id="submitted_from_date" v-model="filterOCRCommunitySubmittedToDate">
                    </div>
                </div>
            </div>
        </CollapsibleFilters>

        <div v-if="addCommunityOCRVisibility" class="col-md-12">
            <div class="text-end">
                <button type="button" class="btn btn-primary mb-2 " @click.prevent="createCommunityOccurrenceReport"><i class="fa-solid fa-circle-plus"></i> Add Community Occurrence Report</button>
            </div>
        </div>

        <div class="row">
            <div class="col-lg-12">
                <datatable
                        ref="community_ocr_datatable"
                        :id="datatable_id"
                        :dtOptions="datatable_options"
                        :dtHeaders="datatable_headers"
                    />
            </div>
            <div v-if="occurrenceReportHistoryId">
                <OccurrenceReportHistory
                    ref="occurrence_report_history"
                    :key="occurrenceReportHistoryId"
                    :occurrence-report-id="occurrenceReportHistoryId"
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
import OccurrenceReportHistory from '../internal/occurrence/community_occurrence_report_history.vue';
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
        profile: {
            type: Object,
            default: null
        },
        filterOCRCommunityOccurrence_cache: {
            type: String,
            required: false,
            default: 'filterOCRCommunityOccurrence',
        },
        filterOCRCommunityName_cache: {
            type: String,
            required: false,
            default: 'filterOCRCommunityName',
        },
        filterOCRCommunityStatus_cache: {
            type: String,
            required: false,
            default: 'filterOCRCommunityStatus',
        },
        filterOCRCommunitySubmittedFromDate_cache: {
            type: String,
            required: false,
            default: 'filterOCRCommunitySubmittedFromDate',
        },
        filterOCRCommunitySubmittedToDate_cache: {
            type: String,
            required: false,
            default: 'filterOCRCommunitySubmittedToDate',
        },
        filterOCRFromCommunityDueDate_cache: {
            type: String,
            required: false,
            default: 'filterOCRFromCommunityDueDate',
        },
        filterOCRToCommunityDueDate_cache: {
            type: String,
            required: false,
            default: 'filterOCRToCommunityDueDate',
        },
    },
    data() {
        let vm = this;
        return {
            uuid:0,
            occurrenceReportHistoryId: null,
            datatable_id: 'community_ocr-datatable-'+vm._uid,

            // selected values for filtering
            filterOCRCommunityOccurrence: sessionStorage.getItem(this.filterOCRCommunityOccurrence_cache) ?
                                    sessionStorage.getItem(this.filterOCRCommunityOccurrence_cache) : 'all',

            filterOCRCommunityName: sessionStorage.getItem(this.filterOCRCommunityName_cache) ?
                                sessionStorage.getItem(this.filterOCRCommunityName_cache) : 'all',

            filterOCRCommunityStatus: sessionStorage.getItem(this.filterOCRCommunityStatus_cache) ?
                        sessionStorage.getItem(this.filterOCRCommunityStatus_cache) : 'all',

            filterOCRCommunitySubmittedFromDate: sessionStorage.getItem(this.filterOCRCommunitySubmittedFromDate_cache) ?
                                sessionStorage.getItem(this.filterOCRCommunitySubmittedFromDate_cache) : '',

            filterOCRCommunitySubmittedToDate: sessionStorage.getItem(this.filterOCRCommunitySubmittedToDate_cache) ?
                                sessionStorage.getItem(this.filterOCRCommunitySubmittedToDate_cache) : '',

            filterOCRFromCommunityDueDate: sessionStorage.getItem(this.filterOCRFromCommunityDueDate_cache) ?
            sessionStorage.getItem(this.filterOCRFromCommunityDueDate_cache) : '',
            filterOCRToCommunityDueDate: sessionStorage.getItem(this.filterOCRToCommunityDueDate_cache) ?
            sessionStorage.getItem(this.filterOCRToCommunityDueDate_cache) : '',

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
                {value: 'draft', name: 'Draft'},
                {value: 'with_assessor', name: 'With Assessor'},
                {value: 'with_referral', name: 'With Referral'},
                {value: 'with_approver', name: 'With Approver'},
                {value: 'approved', name: 'Approved'},
                {value: 'declined', name: 'Declined'},
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
        filterOCRCommunityOccurrence: function(){
            let vm = this;
            vm.$refs.community_ocr_datatable.vmDataTable.ajax.reload(helpers.enablePopovers,false); // This calls ajax() backend call.
            sessionStorage.setItem(vm.filterOCRCommunityOccurrence_cache, vm.filterOCRCommunityOccurrence);
        },
        filterOCRCommunityName: function() {
            let vm = this;
            vm.$refs.community_ocr_datatable.vmDataTable.ajax.reload(helpers.enablePopovers,false); // This calls ajax() backend call.
            sessionStorage.setItem(vm.filterOCRCommunityName_cache, vm.filterOCRCommunityName);
        },
        filterOCRCommunityStatus: function() {
            let vm = this;
            vm.$refs.community_ocr_datatable.vmDataTable.ajax.reload(helpers.enablePopovers,false); // This calls ajax() backend call.
            sessionStorage.setItem(vm.filterOCRCommunityStatus_cache, vm.filterOCRCommunityStatus);
        },
        filterOCRCommunitySubmittedFromDate: function() {
            let vm = this;
            vm.$refs.community_ocr_datatable.vmDataTable.ajax.reload(helpers.enablePopovers,false); // This calls ajax() backend call.
            sessionStorage.setItem(vm.filterOCRCommunitySubmittedFromDate_cache, vm.filterOCRCommunitySubmittedFromDate);
        },
        filterOCRCommunitySubmittedToDate: function() {
            let vm = this;
            vm.$refs.community_ocr_datatable.vmDataTable.ajax.reload(helpers.enablePopovers,false); // This calls ajax() backend call.
            sessionStorage.setItem(vm.filterOCRCommunitySubmittedToDate_cache, vm.filterOCRCommunitySubmittedToDate);
        },
        filterOCRFromCommunityDueDate: function(){
            let vm = this;
            vm.$refs.community_ocr_datatable.vmDataTable.ajax.reload(helpers.enablePopovers,false); // This calls ajax() backend call.
            sessionStorage.setItem(vm.filterOCRFromCommunityDueDate_cache, vm.filterOCRFromCommunityDueDate);
        },
        filterOCRToCommunityDueDate: function(){
            let vm = this;
            vm.$refs.community_ocr_datatable.vmDataTable.ajax.reload(helpers.enablePopovers,false); // This calls ajax() backend call.
            sessionStorage.setItem(vm.filterOCRToCommunityDueDate_cache, vm.filterOCRToCommunityDueDate);
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
            if(this.filterOCRCommunityOccurrence === 'all' &&
                this.filterOCRCommunityName === 'all' &&
                this.filterOCRCommunityStatus === 'all' &&
                this.filterOCRCommunitySubmittedFromDate === '' &&
                this.filterOCRCommunitySubmittedToDate === ''&&
                this.filterOCRFromCommunityDueDate === '' &&
                this.filterOCRToCommunityDueDate === ''){
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
        addCommunityOCRVisibility: function() {
            return this.profile && this.profile.groups.includes(constants.GROUPS.INTERNAL_CONTRIBUTORS);
        },
        datatable_headers: function(){
            if (this.is_internal){
                return ['Number','Occurrence','Community Name', 'Submission date/time', 'Submitter', 'Review Due', 'Status', 'Action']
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
            let vm = this;
            return {
                data: "occurrence_report_number",
                orderable: true,
                searchable: true,
                visible: true,
                'render': function (data, type, full) {
                    let value = full.occurrence_report_number
                    if (vm.is_internal && full.is_new_contributor) {
                        value += ' <span class="badge bg-warning">New Contributor</span>'
                    }
                    return value
                },
                name: "id",
            }
        },
        column_occurrence: function(){
            return {
                data: "occurrence_name",
                orderable: true,
                searchable: true,
                visible: true,
                'render': function(data, type, full){
                    if (full.occurrence_name){
                        return full.occurrence_name;
                    }
                    return 'NOT SET'
                },
                name: "occurrence__occurrence_number",
            }
        },
        column_community_name: function(){
            return {
                data: "community_name",
                orderable: true,
                searchable: true,
                visible: true,
                'render': function(data, type, full){
                    if (full.community_name){
                        return full.community_name;
                    }
                    return ''
                },
                name: "community__taxonomy__community_name",
            }
        },
        column_submission_date_time: function(){
            return {
                data: "reported_date",
                orderable: true,
                searchable: true,
                visible: true,
                'render': function(data, type, full){
                    if (full.reported_date){
                        return full.reported_date;
                    }
                    return ''
                },
                name: "reported_date",
            }
        },
        column_submitter: function(){
            return {
                data: "submitter",
                orderable: false,
                searchable: false,
                visible: true,
                'render': function(data, type, full){
                    if (full.submitter){
                        return full.submitter;
                    }
                    return ''
                },
                name: "submitter__first_name, submitter__last_name",
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
                'render': function (data, type, full) {
                    let links = "";
                    if (!vm.is_external) {
                        if (full.internal_user_edit) {
                            links += `<a href='/internal/occurrence_report/${full.id}?action=edit'>Continue</a><br/>`;
                            links += `<a href='#${full.id}' data-discard-ocr-proposal='${full.id}'>Discard</a><br/>`;
                            links += `<a href='#' data-history-occurrence-report='${full.id}'>History</a><br>`;
                        }
                        else {
                            if (full.can_user_assess || full.can_user_approve) {
                                links += `<a href='/internal/occurrence_report/${full.id}?action=edit'>Process</a><br/>`;
                            }
                            else {
                                links += `<a href='/internal/occurrence_report/${full.id}?action=view'>View</a><br/>`;
                            }
                            links += `<a href='#' data-history-occurrence-report='${full.id}'>History</a><br>`;
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
            if(vm.is_internal){
                columns = [
                vm.column_number,
                    vm.column_occurrence,
                    vm.column_community_name,
                    vm.column_submission_date_time,
                    vm.column_submitter,
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
                        d.filter_occurrence = vm.filterOCRCommunityOccurrence;
                        d.filter_community_name = vm.filterOCRCommunityName;
                        d.filter_status = vm.filterOCRCommunityStatus;
                        d.filter_submitted_from_date = vm.filterOCRCommunitySubmittedFromDate;
                        d.filter_submitted_to_date = vm.filterOCRCommunitySubmittedToDate;
                        d.filter_from_due_date = vm.filterOCRFromCommunityDueDate;
                        d.filter_to_due_date = vm.filterOCRToCommunityDueDate;
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
                this.occurrenceReportHistoryId = parseInt(id);
                this.uuid++;
                this.$nextTick(() => {
                    this.$refs.occurrence_report_history.isModalOpen = true;
                });
            },
        collapsible_component_mounted: function(){
            this.$refs.collapsible_filters.show_warning_icon(this.filterApplied)
        },
        initialiseOccurrenceLookup: function(){
                let vm = this;
                $(vm.$refs.ocr_occurrence_lookup).select2({
                    minimumInputLength: 2,
                    dropdownParent: $("#select_occurrence"),
                    "theme": "bootstrap-5",
                    allowClear: true,
                    placeholder:"Select Occurrence",
                    ajax: {
                        url: api_endpoints.community_lookup,
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
                    vm.filterOCRCommunityOccurrence = data;
                    sessionStorage.setItem("filterOCRCommunityOccurrenceText", e.params.data.text);
                }).
                on("select2:unselect",function (e) {
                    var selected = $(e.currentTarget);
                    vm.filterOCRCommunityOccurrence = 'all';
                    sessionStorage.setItem("filterOCRCommunityOccurrenceText",'');
                }).
                on("select2:open",function (e) {
                    const searchField = $('[aria-controls="select2-ocr_occurrence_lookup-results"]')
                    searchField[0].focus();
                });
        },
        initialiseCommunityNameLookup: function(){
                let vm = this;
                $(vm.$refs.ocr_community_name_lookup).select2({
                    minimumInputLength: 2,
                    dropdownParent: $("#select_ocr_community_name"),
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
                    vm.filterOCRCommunityName = data;
                    sessionStorage.setItem("filterOCRCommunityNameText", e.params.data.text);
                }).
                on("select2:unselect",function (e) {
                    var selected = $(e.currentTarget);
                    vm.filterOCRCommunityName = 'all';
                    sessionStorage.setItem("filterOCRCommunityNameText",'');
                }).
                on("select2:open",function (e) {
                    const searchField = $('[aria-controls="select2-ocr_community_name_lookup-results"]')
                    searchField[0].focus();
                });
        },
        fetchFilterLists: function(){
            let vm = this;
            //large FilterList of Community Values object
            vm.$http.get(api_endpoints.community_filter_dict).then((response) => {
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
        createCommunityOccurrenceReport: async function () {
            swal.fire({
                title: `Add ${this.group_type_name} Occurrence Report`,
                text: "Are you sure you want to add a new occurrence report?",
                icon: "question",
                showCancelButton: true,
                confirmButtonText: 'Add Occurrence Report',
                reverseButtons: true,
                confirmButtonColor: '#226fbb',

            }).then(async (swalresult) => {
                if (swalresult.isConfirmed) {
                    let newCommunityOCRId = null
                    try {
                            const createUrl = api_endpoints.occurrence_report+"/";
                            let payload = new Object();
                            payload.group_type_id = this.group_type_id
                            payload.internal_application = true
                            let savedCommunityOCR = await Vue.http.post(createUrl, payload);
                            if (savedCommunityOCR) {
                                newCommunityOCRId = savedCommunityOCR.body.id;
                            }
                        }
                    catch (err) {
                        console.log(err);
                        if (this.is_internal) {
                            return err;
                        }
                    }
                    this.$router.push({
                        name: 'internal-occurrence-report-detail',
                        params: {occurrence_report_id: newCommunityOCRId},
                        });
                    }
                });
        },
        discardOCRProposal:function (occurrence_report_id) {
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
                    vm.$http.delete(api_endpoints.discard_ocr_proposal(occurrence_report_id))
                    .then((response) => {
                        swal.fire({
                            title: 'Discarded',
                            text: 'Your report has been discarded',
                            icon: 'success',
                            confirmButtonColor:'#226fbb',
                        });
                        vm.$refs.community_ocr_datatable.vmDataTable.ajax.reload(helpers.enablePopovers,false);
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
            vm.$refs.community_ocr_datatable.vmDataTable.on('click', 'a[data-discard-ocr-proposal]', function(e) {
                e.preventDefault();
                var id = $(this).attr('data-discard-ocr-proposal');
                vm.discardCSProposal(id);
            });
            vm.$refs.community_ocr_datatable.vmDataTable.on('click', 'a[data-history-occurrence-report]', function(e) {
                    e.preventDefault();
                    var id = $(this).attr('data-history-occurrence-report');
                    vm.historyDocument(id);
                });
            vm.$refs.community_ocr_datatable.vmDataTable.on('childRow.dt', function (e, settings) {
                helpers.enablePopovers();
            });
        },
        initialiseSearch:function(){
            this.submitterSearch();
        },
        submitterSearch:function(){
            let vm = this;
            vm.$refs.community_ocr_datatable.table.dataTableExt.afnFiltering.push(
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
                    "name": "occurrence_report__id, occurrence_report__occurrence_report_number",
                    "orderable": "true",
                    "search": {
                        "regex": "false",
                        "value": ""
                    },
                    "searchable": "false"
                },
                "1": {
                    "data": "occurrence",
                    "name": "occurrence_report__occurence",
                    "orderable": "true",
                    "search": {
                        "regex": "false",
                        "value": ""
                    },
                    "searchable": "true"
                },
                "2": {
                    "data": "community_name",
                    "name": "occurrence_report__community__taxonomy__community_name",
                    "orderable": "true",
                    "search": {
                        "regex": "false",
                        "value": ""
                    },
                    "searchable": "true"
                },
                "3": {
                    "data": "reported_date",
                    "name": "occurrence_report__reported_date",
                    "searchable": "true",
                    "orderable": "true",
                    "search": {
                        "value": "",
                        "regex": "false"
                    }
                },
                "4": {
                    "data": "submitter",
                    // "name": "occurrence_report__submitter",
                    "searchable": "true",
                    "orderable": "true",
                    "search": {
                        "value": "",
                        "regex": "false"
                    }
                },
                "5": {
                    "data": "processing_status",
                    "name": "occurrence_report__processing_status",
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
                filter_occurrence: vm.filterOCRCommunityOccurrence,
                filter_community_name: vm.filterOCRCommunityName,
                filter_status: vm.filterOCRCommunityStatus,
                filter_submitted_from_date: vm.filterOCRCommunitySubmittedFromDate,
                filter_submitted_to_date: vm.filterOCRCommunitySubmittedToDate,
                filter_from_due_date: vm.filterOCRFromCommunityDueDate,
                filter_to_due_date: vm.filterOCRToCommunityDueDate,
                is_internal: vm.is_internal,
                export_format: format
            };

            const url = api_endpoints.community_occurrence_report_internal_export;
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
            vm.initialiseOccurrenceLookup();
            vm.initialiseCommunityNameLookup();
            //vm.initialiseSearch();
            vm.addEventListeners();

            // -- to set the select2 field with the session value if exists onload()
            if(sessionStorage.getItem("filterOCRCommunityOccurrence")!='all' && sessionStorage.getItem("filterOCRCommunityOccurrence")!=null)
            {
                // contructor new Option(text, value, defaultSelected, selected)
                var newOption = new Option(sessionStorage.getItem("filterOCRCommunityOccurrenceText"), vm.filterOCRCommunityOccurrence, false, true);
                $('#ocr_occurrence_lookup').append(newOption);
                //$('#scientific_name_lookup').append(newOption).trigger('change');
            }
            if(sessionStorage.getItem("filterOCRCommunityName")!='all' && sessionStorage.getItem("filterOCRCommunityName")!=null)
            {
                // contructor new Option(text, value, defaultSelected, selected)
                var newOption = new Option(sessionStorage.getItem("filterOCRCommunityNameText"), vm.filterOCRCommunityName, false, true);
                $('#ocr_community_name_lookup').append(newOption);
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
