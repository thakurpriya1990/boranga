<template id="species_flora_ocr_referrals_dashboard">
    <div>
        <CollapsibleFilters component_title="Filters" ref="collapsible_filters" @created="collapsible_component_mounted"
            class="mb-2">
            <div class="row">
                <div class="col-md-4">
                    <div class="form-group" id="ocr_referrals_select_occurrence">
                        <label for="ocr_referrals_occurrence_lookup">Occurrence:</label>
                        <select id="ocr_referrals_occurrence_lookup" name="ocr_referrals_occurrence_lookup"
                            ref="ocr_referrals_occurrence_lookup" class="form-control" />
                    </div>
                </div>
                <div class="col-md-4">
                    <div class="form-group" id="ocr_referrals_select_scientific_name_by_groupname">
                        <label for="ocr_referrals_scientific_name_lookup_by_groupname">Scientific Name:</label>
                        <select id="ocr_referrals_scientific_name_lookup_by_groupname"
                            name="ocr_referrals_scientific_name_lookup_by_groupname"
                            ref="ocr_referrals_scientific_name_lookup_by_groupname" class="form-control" />
                    </div>
                </div>
                <div class="col-md-4">
                    <div class="form-group" id="select_status">
                        <label for="">Status:</label>
                        <select class="form-select" v-model="filterOCRFloraReferralsStatus">
                            <option value="all">All</option>
                            <option v-for="status in processing_statuses" :value="status.value">{{ status.name }}
                            </option>
                        </select>
                    </div>
                </div>
            </div>
        </CollapsibleFilters>
        <div class="row">
            <div class="col-lg-12">
                <datatable ref="flora_ocr_referrals_datatable" :id="datatable_id" :dtOptions="datatable_options"
                    :dtHeaders="datatable_headers" />
            </div>
        </div>
    </div>
</template>
<script>

import "babel-polyfill"
import datatable from '@/utils/vue/datatable.vue'
import CollapsibleFilters from '@/components/forms/collapsible_component.vue'
import FormSection from '@/components/forms/section_toggle.vue'

import {
    api_endpoints,
    constants,
    helpers
} from '@/utils/hooks'
export default {
    name: 'OccurrenceReportFloraTable',
    props: {
        level: {
            type: String,
            required: true,
            validator: function (val) {
                let options = ['internal', 'external'];
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
        // for adding agendaitems for the meeting_obj.id
        meeting_obj: {
            type: Object,
            required: false
        },
        filterOCRFloraReferralsOccurrence_cache: {
            type: String,
            required: false,
            default: 'filterOCRFloraReferralsOccurrence',
        },
        filterOCRFloraReferralsScientificName_cache: {
            type: String,
            required: false,
            default: 'filterOCRFloraReferralsScientificName',
        },
        filterOCRFloraReferralsStatus_cache: {
            type: String,
            required: false,
            default: 'filterOCRFloraReferralsStatus',
        },
    },
    data() {
        let vm = this;
        return {
            uuid: 0,
            occurrenceReportHistoryId: null,
            datatable_id: 'species_flora_ocr_referrals_datatable_' + vm._uid,
            filterOCRFloraReferralsOccurrence: sessionStorage.getItem(this.filterOCRFloraReferralsOccurrence_cache) ?
                sessionStorage.getItem(this.filterOCRFloraReferralsOccurrence_cache) : 'all',
            filterOCRFloraReferralsScientificName: sessionStorage.getItem(this.filterOCRFloraReferralsScientificName_cache) ?
                sessionStorage.getItem(this.filterOCRFloraReferralsScientificName_cache) : 'all',
            filterOCRFloraReferralsStatus: sessionStorage.getItem(this.filterOCRFloraReferralsStatus_cache) ?
                sessionStorage.getItem(this.filterOCRFloraReferralsStatus_cache) : 'all',
            processing_statuses: [
                { value: 'with_referral', name: 'Awaiting' },
                { value: 'completed', name: 'Completed' },
            ],
        }
    },
    components: {
        datatable,
        CollapsibleFilters,
        FormSection,
    },
    watch: {
        filterOCRFloraReferralsOccurrence: function () {
            let vm = this;
            vm.$refs.flora_ocr_referrals_datatable.vmDataTable.ajax.reload(helpers.enablePopovers, false); // This calls ajax() backend call.
            sessionStorage.setItem(vm.filterOCRFloraReferralsOccurrence_cache, vm.filterOCRFloraReferralsOccurrence);
        },
        filterOCRFloraReferralsScientificName: function () {
            let vm = this;
            vm.$refs.flora_ocr_referrals_datatable.vmDataTable.ajax.reload(helpers.enablePopovers, false); // This calls ajax() backend call.
            sessionStorage.setItem(vm.filterOCRFloraReferralsScientificName_cache, vm.filterOCRFloraReferralsScientificName);
        },
        filterOCRFloraReferralsStatus: function () {
            let vm = this;
            vm.$refs.flora_ocr_referrals_datatable.vmDataTable.ajax.reload(helpers.enablePopovers, false); // This calls ajax() backend call.
            sessionStorage.setItem(vm.filterOCRFloraReferralsStatus_cache, vm.filterOCRFloraReferralsStatus);
        },
        filterApplied: function () {
            if (this.$refs.collapsible_filters) {
                this.$refs.collapsible_filters.show_warning_icon(this.filterApplied)
            }
        },
    },
    computed: {
        filterApplied: function () {
            if (this.filterOCRFloraReferralsOccurrence === 'all' &&
                this.filterOCRFloraReferralsScientificName === 'all' &&
                this.filterOCRFloraReferralsStatus === 'all') {
                return false
            } else {
                return true
            }
        },
        datatable_headers: function () {
            return ['ID', 'Number', 'Occurrence', 'Scientific Name', 'Submission date/time', 'Submitter', 'Effective From', 'Effective To', 'Review Due', 'Status', 'Action']
        },
        column_id: function () {
            return {
                data: "id",
                orderable: true,
                searchable: false,
                visible: false,
            }
        },
        column_number: function () {
            let vm = this;
            return {
                data: "occurrence_report_number",
                orderable: true,
                searchable: true,
                visible: true,
                name: "occurrence_report__occurrence_report_number",
            }
        },
        column_occurrence: function () {
            return {
                data: "occurrence_name",
                orderable: true,
                searchable: true,
                visible: true,
                'render': function (data, type, full) {
                    if (full.occurrence_name) {
                        return full.occurrence_name;
                    }
                    return 'NOT SET'
                },
                name: "occurrence_report__occurrence__occurrence_number",
            }
        },
        column_scientific_name: function () {
            return {
                data: "scientific_name",
                orderable: true,
                searchable: true,
                visible: true,
                name: "occurrence_report__species__taxonomy__scientific_name",
            }
        },
        column_submission_date_time: function () {
            return {
                data: "reported_date",
                orderable: true,
                searchable: true,
                visible: true,
                name: "occurrence_report__reported_date",
            }
        },
        column_submitter: function () {
            return {
                data: "submitter",
                orderable: false,
                searchable: false,
                visible: true,
            }
        },
        column_effective_from: function () {
            return {
                data: "effective_from",
                orderable: true,
                searchable: true,
                visible: true,
                name: "occurrence_report__effective_from",
            }
        },
        column_effective_to: function () {
            return {
                data: "effective_to",
                orderable: true,
                searchable: true,
                visible: true,
                name: "occurrence_report__effective_to",
            }
        },
        column_review_due_date: function () {
            return {
                data: "review_due_date",
                orderable: true,
                searchable: true,
                visible: true,
                name: "occurrence_report__review_due_date",
            }
        },
        column_status: function () {
            return {
                data: "processing_status_display",
                orderable: true,
                searchable: true,
                visible: true,
                name: "processing_status",
            }
        },
        column_action: function () {
            return {
                data: "id",
                orderable: false,
                searchable: false,
                visible: true,
                'render': function (data, type, full) {
                    let links = "";
                    if (full.processing_status == 'with_referral') {
                        links += `<a href='/internal/occurrence_report/${full.id}?action=edit'>Process</a><br/>`;
                    }
                    else {
                        links += `<a href='/internal/occurrence_report/${full.id}?action=view'>View</a><br/>`;
                    }
                    return links;
                },
            }
        },
        datatable_options: function () {
            let vm = this
            let columns = []
            let search = null
            let buttons = [
                {
                    extend: 'excel',
                    text: '<i class="fa-solid fa-download"></i> Excel',
                    className: 'btn btn-primary me-2 rounded',
                    exportOptions: {
                        columns: ':visible:not(.no-export)'
                    }
                },
                {
                    extend: 'csv',
                    text: '<i class="fa-solid fa-download"></i> CSV',
                    className: 'btn btn-primary rounded',
                    exportOptions: {
                        columns: ':visible:not(.no-export)'
                    }
                }
            ]
            columns = [
                vm.column_id,
                vm.column_number,
                vm.column_occurrence,
                vm.column_scientific_name,
                vm.column_submission_date_time,
                vm.column_submitter,
                vm.column_effective_from,
                vm.column_effective_to,
                vm.column_review_due_date,
                vm.column_status,
                vm.column_action,
            ]
            search = true

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
                    { responsivePriority: 3, targets: -1, className: 'no-export' },
                    { responsivePriority: 2, targets: -2 }
                ],
                ajax: {
                    "url": this.url,
                    "dataSrc": 'data',
                    "data": function (d) {
                        d.filter_group_type = vm.group_type_name;
                        d.filter_occurrence = vm.filterOCRFloraReferralsOccurrence;
                        d.filter_scientific_name = vm.filterOCRFloraReferralsScientificName;
                        d.filter_status = vm.filterOCRFloraReferralsStatus;
                    }
                },
                dom: "<'d-flex align-items-center'<'me-auto'l>fB>" +
                    "<'row'<'col-sm-12'tr>>" +
                    "<'d-flex align-items-center'<'me-auto'i>p>",
                buttons: buttons,
                columns: columns,
                processing: true,
                initComplete: function () {
                    helpers.enablePopovers();
                },
            }
        }
    },
    methods: {
        historyDocument: function (id) {
            this.occurrenceReportHistoryId = parseInt(id);
            this.uuid++;
            this.$nextTick(() => {
                this.$refs.occurrence_report_history.isModalOpen = true;
            });
        },
        collapsible_component_mounted: function () {
            this.$refs.collapsible_filters.show_warning_icon(this.filterApplied)
        },
        initialiseOccurrenceLookup: function () {
            let vm = this;
            $(vm.$refs.ocr_referrals_occurrence_lookup).select2({
                minimumInputLength: 2,
                dropdownParent: $("#ocr_referrals_select_occurrence"),
                "theme": "bootstrap-5",
                allowClear: true,
                placeholder: "Select Occurrence",
                ajax: {
                    url: api_endpoints.occurrence_lookup,
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
                    vm.filterOCRFloraReferralsOccurrence = data;
                    sessionStorage.setItem("filterOCRFloraReferralsOccurrenceText", e.params.data.text);
                }).
                on("select2:unselect", function (e) {
                    var selected = $(e.currentTarget);
                    vm.filterOCRFloraReferralsOccurrence = 'all';
                    sessionStorage.setItem("filterOCRFloraReferralsOccurrenceText", '');
                }).
                on("select2:open", function (e) {
                    const searchField = $('[aria-controls="select2-ocr_referrals_occurrence_lookup-results"]')
                    searchField[0].focus();
                });
        },
        initialiseScientificNameLookup: function () {
            let vm = this;
            $(vm.$refs.ocr_referrals_scientific_name_lookup_by_groupname).select2({
                minimumInputLength: 2,
                dropdownParent: $("#ocr_referrals_select_scientific_name_by_groupname"),
                theme: 'bootstrap-5',
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
                },
            }).
                on("select2:select", function (e) {
                    var selected = $(e.currentTarget);
                    let data = e.params.data.id;
                    vm.filterOCRFloraReferralsScientificName = data;
                    sessionStorage.setItem("filterOCRFloraReferralsScientificNameText", e.params.data.text);
                }).
                on("select2:unselect", function (e) {
                    var selected = $(e.currentTarget);
                    vm.filterOCRFloraReferralsScientificName = 'all';
                    sessionStorage.setItem("filterOCRFloraReferralsScientificNameText", '');
                }).
                on("select2:open", function (e) {
                    const searchField = $('[aria-controls="select2-ocr_referrals_scientific_name_lookup_by_groupname-results"]')
                    searchField[0].focus();
                });
        },
        addEventListeners: function () {
            let vm = this;
            vm.$refs.flora_ocr_referrals_datatable.vmDataTable.on('childRow.dt', function (e, settings) {
                helpers.enablePopovers();
            });
        },
    },
    mounted: function () {
        let vm = this;
        $('a[data-toggle="collapse"]').on('click', function () {
            var chev = $(this).children()[0];
            window.setTimeout(function () {
                $(chev).toggleClass("glyphicon-chevron-down glyphicon-chevron-up");
            }, 100);
        });
        this.$nextTick(() => {
            vm.initialiseOccurrenceLookup();
            vm.initialiseScientificNameLookup();
            vm.addEventListeners();
            if (sessionStorage.getItem("filterOCRFloraReferralsOccurrence") != 'all' && sessionStorage.getItem("filterOCRFloraReferralsOccurrence") != null) {
                var newOption = new Option(sessionStorage.getItem("filterOCRFloraReferralsOccurrenceText"), vm.filterOCRFloraReferralsOccurrence, false, true);
                $('#ocr_referrals_occurrence_lookup').append(newOption);
            }
            if (sessionStorage.getItem("filterOCRFloraReferralsScientificName") != 'all' && sessionStorage.getItem("filterOCRFloraReferralsScientificName") != null) {
                var newOption = new Option(sessionStorage.getItem("filterOCRFloraReferralsScientificNameText"), vm.filterOCRFloraReferralsScientificName, false, true);
                $('#ocr_referrals_scientific_name_lookup').append(newOption);
            }
        });
    }
}
</script>
