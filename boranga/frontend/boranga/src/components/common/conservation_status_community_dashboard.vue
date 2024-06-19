<template id="cs_communities_dashboard">
    <div>
        <CollapsibleFilters component_title="Filters" ref="collapsible_filters" @created="collapsible_component_mounted"
            class="mb-2">
            <div class="row">
                <div class="col-md-3">
                    <div class="form-group" id="select_community_id">
                        <label for="cs_community_id_lookup">Community ID:</label>
                        <select id="cs_community_id_lookup" name="cs_community_id_lookup" ref="cs_community_id_lookup"
                            class="form-control" />
                    </div>
                </div>
                <div class="col-md-3">
                    <div class="form-group" id="select_community_name">
                        <label for="cs_community_name_lookup">Community Name:</label>
                        <select id="cs_community_name_lookup" name="cs_community_name_lookup"
                            ref="cs_community_name_lookup" class="form-control" />
                    </div>
                </div>
                <div class="col-md-3">
                    <div class="form-group">
                        <label for="">Region:</label>
                        <select class="form-select" v-model="filterCSCommunityRegion" @change="filterDistrict($event)">
                            <option value="all">All</option>
                            <option v-for="region in region_list" :value="region.id" v-bind:key="region.id">
                                {{ region.name }}</option>
                        </select>
                    </div>
                </div>
                <div class="col-md-3">
                    <div class="form-group">
                        <label for="">District:</label>
                        <select class="form-select" v-model="filterCSCommunityDistrict">
                            <option value="all">All</option>
                            <option v-for="district in filtered_district_list" :value="district.id">{{ district.name }}
                            </option>
                        </select>
                    </div>
                </div>
                <div class="col-md-3">
                    <div class="form-group">
                        <label for="change-type">Change Type:</label>
                        <select id="change-type" class="form-select" v-model="filterCSCommunityChangeCode">
                            <option value="all">All</option>
                            <option v-for="change_code in change_codes" :value="change_code.id">{{ change_code.code }}
                            </option>
                        </select>
                    </div>
                </div>
                <div class="col-md-3">
                    <div class="form-group">
                        <label for="wa-legislative-list">WA Legislative List:</label>
                        <select id="wa-legislative-list" class="form-select"
                            v-model="filterCSCommunityWALegislativeList">
                            <option value="all">All</option>
                            <option v-for="list in wa_legislative_lists" :value="list.id">{{ list.code }}</option>
                        </select>
                    </div>
                </div>
                <div class="col-md-3">
                    <div class="form-group">
                        <label for="wa-legislative-category">WA Legislative Category:</label>
                        <select id="wa-legislative-category" class="form-select"
                            v-model="filterCSCommunityWALegislativeCategory">
                            <option value="all">All</option>
                            <option v-for="list in wa_legislative_categories" :value="list.id">{{ list.code }}
                            </option>
                        </select>
                    </div>
                </div>
                <div class="col-md-3">
                    <div class="form-group">
                        <label for="wa-priority-category">WA Priority Category:</label>
                        <select id="wa-priority-category" class="form-select"
                            v-model="filterCSCommunityWAPriorityCategory">
                            <option value="all">All</option>
                            <option v-for="list in wa_priority_categories" :value="list.id">{{ list.code }}
                            </option>
                        </select>
                    </div>
                </div>
                <div class="col-md-3">
                    <div class="form-group">
                        <label class="form-check-label" for="commonwealth-relevance">Commonwealth Relevance</label>
                        <div class="form-check form-switch mt-1">
                            <input class="form-check-input" type="checkbox" id="commonwealth-relevance"
                                v-model="filterCSCommunityCommonwealthRelevance" true-value="true" false-value="false">
                        </div>
                    </div>
                </div>
                <div class="col-md-3">
                    <div class="form-group">
                        <label class="form-check-label" for="international-relevance">International Relevance</label>
                        <div class="form-check form-switch mt-1">
                            <input class="form-check-input" type="checkbox" id="international-relevance"
                                v-model="filterCSCommunityInternationalRelevance" true-value="true" false-value="false">
                        </div>
                    </div>
                </div>
                <div class="col-md-3" v-show="!is_for_agenda">
                    <div class="form-group">
                        <label for="">Status:</label>
                        <select class="form-select" v-model="filterCSCommunityApplicationStatus">
                            <option value="all">All</option>
                            <option v-for="status in processing_statuses" :value="status.value">{{ status.name }}
                            </option>
                        </select>
                    </div>
                </div>
                <div class="col-md-3">
                    <div class="form-group" id="select_assessor">
                        <label for="cs_assessor_lookup">Assessor:</label>
                        <select id="cs_assessor_lookup" name="cs_assessor_lookup" ref="cs_assessor_lookup"
                            class="form-control" />
                    </div>
                </div>
                <div class="col-md-3">
                    <div class="form-group" id="select_submitter">
                        <label for="cs_submitter_lookup">Submitter:</label>
                        <select id="cs_submitter_lookup" name="cs_submitter_lookup" ref="cs_submitter_lookup"
                            class="form-control" />
                    </div>
                </div>
                <div class="col-md-3">
                    <div class="form-group">
                        <label for="submitter-category">Submitter Category:</label>
                        <select id="submitter-category" class="form-select"
                            v-model="filterCSCommunitySubmitterCategory">
                            <option value="all">All</option>
                            <option v-for="submitter_category in submitter_categories" :value="submitter_category.id">{{
                                submitter_category.name }}
                            </option>
                        </select>
                    </div>
                </div>
                <div class="col-md-6" v-show="!is_for_agenda">
                    <label for="" class="form-label px-2">Effective From Date Range:</label>
                    <div class="input-group px-2 mb-2">
                        <span class="input-group-text">From </span>
                        <input type="date" class="form-control" placeholder="DD/MM/YYYY" id="from_effective_from_date"
                            v-model="filterCSFromCommunityEffectiveFromDate">
                        <span class="input-group-text"> to </span>
                        <input type="date" class="form-control" placeholder="DD/MM/YYYY" id="to_effective_from_date"
                            v-model="filterCSToCommunityEffectiveFromDate">
                    </div>
                </div>
                <div class="col-md-6" v-show="!is_for_agenda">
                    <label for="" class="form-label px-2">Effective To Date Range:</label>
                    <div class="input-group px-2">
                        <span class="input-group-text">From </span>
                        <input type="date" class="form-control" placeholder="DD/MM/YYYY" id="from_effective_to_date"
                            v-model="filterCSFromCommunityEffectiveToDate">
                        <span class="input-group-text"> to </span>
                        <input type="date" class="form-control" placeholder="DD/MM/YYYY" id="to_effective_to_date"
                            v-model="filterCSToCommunityEffectiveToDate">
                    </div>
                </div>
                <div class="col-md-6" v-show="!is_for_agenda">
                    <label for="from_review_due_date" class="form-label px-2">Review Due Date Range:</label>
                    <div class="input-group px-2">
                        <span class="input-group-text">From </span>
                        <input type="date" class="form-control" placeholder="DD/MM/YYYY" id="from_review_due_date"
                            v-model="filterCSFromCommunityReviewDueDate">
                        <span class="input-group-text"> to </span>
                        <input type="date" class="form-control" placeholder="DD/MM/YYYY" id="to_review_due_date"
                            v-model="filterCSToCommunityReviewDueDate">
                    </div>
                </div>
            </div>
        </CollapsibleFilters>

        <div v-if="addCommunityCSVisibility && is_for_agenda == false" class="col-md-12">
            <div class="text-end">
                <button type="button" class="btn btn-primary mb-2 "
                    @click.prevent="createCommunityConservationStatus"><i class="fa-solid fa-circle-plus"></i> Propose
                    Conservation Status</button>
            </div>
        </div>

        <div class="row">
            <div class="col-lg-12">
                <datatable ref="cs_communities_datatable" :id="datatable_id" :dtOptions="datatable_options"
                    :dtHeaders="datatable_headers" />
            </div>
            <div v-if="communityConservationStatusHistoryId">
                <CommunityConservationStatusHistory ref="community_conservation_status_history"
                    :key="communityConservationStatusHistoryId"
                    :conservation-status-id="communityConservationStatusHistoryId" :community-id="communityHistoryId"
                    :conservation-list-id="listHistoryId" />
            </div>
        </div>
    </div>
</template>
<script>
import "babel-polyfill"
import datatable from '@/utils/vue/datatable.vue'
import CollapsibleFilters from '@/components/forms/collapsible_component.vue'
import FormSection from '@/components/forms/section_toggle.vue'
import CommunityConservationStatusHistory from '../internal/conservation_status/community_conservation_status_history.vue';

import Vue from 'vue'
import {
    api_endpoints,
    constants,
    helpers
} from '@/utils/hooks'
export default {
    name: 'ConservationStatusCommunityTable',
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
        filterCSCommunityMigratedId_cache: {
            type: String,
            required: false,
            default: 'filterCSCommunityMigratedId',
        },
        filterCSCommunityName_cache: {
            type: String,
            required: false,
            default: 'filterCSCommunityName',
        },
        filterCSCommunityRegion_cache: {
            type: String,
            required: false,
            default: 'filterCSCommunityRegion',
        },
        filterCSCommunityDistrict_cache: {
            type: String,
            required: false,
            default: 'filterCSCommunityDistrict',
        },
        filterCSCommunityChangeCode_cache: {
            type: String,
            required: false,
            default: 'filterCSCommunityChangeCode',
        },
        filterCSCommunityWALegislativeList_cache: {
            type: String,
            required: false,
            default: 'filterCSCommunityWALegislativeList',
        },
        filterCSCommunityWALegislativeCategory_cache: {
            type: String,
            required: false,
            default: 'filterCSCommunityWALegislativeCategory',
        },
        filterCSCommunityWAPriorityCategory_cache: {
            type: String,
            required: false,
            default: 'filterCSCommunityWAPriorityCategory',
        },
        filterCSCommunityCommonwealthRelevance_cache: {
            type: String,
            required: false,
            default: 'filterCSCommunityCommonwealthRelevance',
        },
        filterCSCommunityInternationalRelevance_cache: {
            type: String,
            required: false,
            default: 'filterCSCommunityInternationalRelevance',
        },
        filterCSCommunityAssessor_cache: {
            type: String,
            required: false,
            default: 'filterCSCommunityAssessor',
        },
        filterCSCommunitySubmitter_cache: {
            type: String,
            required: false,
            default: 'filterCSCommunitySubmitter',
        },
        filterCSCommunitySubmitterCategory_cache: {
            type: String,
            required: false,
            default: 'filterCSCommunitySubmitterCategory',
        },
        filterCSCommunityApplicationStatus_cache: {
            type: String,
            required: false,
            default: 'filterCSCommunityApplicationStatus',
        },
        filterCSFromCommunityEffectiveFromDate_cache: {
            type: String,
            required: false,
            default: 'filterCSFromCommunityEffectiveFromDate',
        },
        filterCSToCommunityEffectiveFromDate_cache: {
            type: String,
            required: false,
            default: 'filterCSToCommunityEffectiveFromDate',
        },
        filterCSFromCommunityEffectiveToDate_cache: {
            type: String,
            required: false,
            default: 'filterCSFromCommunityEffectiveToDate',
        },
        filterCSToCommunityEffectiveToDate_cache: {
            type: String,
            required: false,
            default: 'filterCSToCommunityEffectiveToDate',
        },
        filterCSFromCommunityReviewDueDate_cache: {
            type: String,
            required: false,
            default: 'filterCSFromCommunityReviewDueDate',
        },
        filterCSToCommunityReviewDueDate_cache: {
            type: String,
            required: false,
            default: 'filterCSToCommunityReviewDueDate',
        },
    },
    data() {
        let vm = this;
        return {
            datatable_id: 'cs-communities-datatable-' + vm._uid,
            communityConservationStatusHistoryId: null,
            communityHistoryId: null,
            listHistoryId: null,

            // selected values for filtering
            filterCSCommunityMigratedId: sessionStorage.getItem(this.filterCSCommunityMigratedId_cache) ?
                sessionStorage.getItem(this.filterCSCommunityMigratedId_cache) : 'all',

            filterCSCommunityName: sessionStorage.getItem(this.filterCSCommunityName_cache) ?
                sessionStorage.getItem(this.filterCSCommunityName_cache) : 'all',

            filterCSCommunityRegion: sessionStorage.getItem(this.filterCSCommunityRegion_cache) ?
                sessionStorage.getItem(this.filterCSCommunityRegion_cache) : 'all',

            filterCSCommunityDistrict: sessionStorage.getItem(this.filterCSCommunityDistrict_cache) ?
                sessionStorage.getItem(this.filterCSCommunityDistrict_cache) : 'all',

            filterCSCommunityChangeCode: sessionStorage.getItem(this.filterCSCommunityChangeCode_cache) ?
                sessionStorage.getItem(this.filterCSCommunityChangeCode_cache) : 'all',

            filterCSCommunityWALegislativeList: sessionStorage.getItem(this.filterCSCommunityWALegislativeList_cache) ?
                sessionStorage.getItem(this.filterCSCommunityWALegislativeList_cache) : 'all',

            filterCSCommunityWALegislativeCategory: sessionStorage.getItem(this.filterCSCommunityWALegislativeCategory_cache) ?
                sessionStorage.getItem(this.filterCSCommunityWALegislativeCategory_cache) : 'all',

            filterCSCommunityWAPriorityCategory: sessionStorage.getItem(this.filterCSCommunityWAPriorityCategory_cache) ?
                sessionStorage.getItem(this.filterCSCommunityWAPriorityCategory_cache) : 'all',

            filterCSCommunityCommonwealthRelevance: sessionStorage.getItem(this.filterCSCommunityCommonwealthRelevance_cache) ?
                sessionStorage.getItem(this.filterCSCommunityCommonwealthRelevance_cache) : "false",

            filterCSCommunityInternationalRelevance: sessionStorage.getItem(this.filterCSCommunityInternationalRelevance_cache) ?
                sessionStorage.getItem(this.filterCSCommunityInternationalRelevance_cache) : "false",

            filterCSCommunityApplicationStatus: sessionStorage.getItem(this.filterCSCommunityApplicationStatus_cache) ?
                sessionStorage.getItem(this.filterCSCommunityApplicationStatus_cache) : 'approved',

            filterCSCommunityAssessor: sessionStorage.getItem(this.filterCSCommunityAssessor_cache) ?
                sessionStorage.getItem(this.filterCSCommunityAssessor_cache) : 'all',

            filterCSCommunitySubmitter: sessionStorage.getItem(this.filterCSCommunitySubmitter_cache) ?
                sessionStorage.getItem(this.filterCSCommunitySubmitter_cache) : 'all',

            filterCSCommunitySubmitterCategory: sessionStorage.getItem(this.filterCSCommunitySubmitterCategory_cache) ?
                sessionStorage.getItem(this.filterCSCommunitySubmitterCategory_cache) : 'all',

            filterCSFromCommunityEffectiveFromDate: sessionStorage.getItem(this.filterCSFromCommunityEffectiveFromDate_cache) ?
                sessionStorage.getItem(this.filterCSFromCommunityEffectiveFromDate_cache) : '',
            filterCSToCommunityEffectiveFromDate: sessionStorage.getItem(this.filterCSToCommunityEffectiveFromDate_cache) ?
                sessionStorage.getItem(this.filterCSToCommunityEffectiveFromDate_cache) : '',

            filterCSFromCommunityEffectiveToDate: sessionStorage.getItem(this.filterCSFromCommunityEffectiveToDate_cache) ?
                sessionStorage.getItem(this.filterCSFromCommunityEffectiveToDate_cache) : '',
            filterCSToCommunityEffectiveToDate: sessionStorage.getItem(this.filterCSToCommunityEffectiveToDate_cache) ?
                sessionStorage.getItem(this.filterCSToCommunityEffectiveToDate_cache) : '',

            filterCSFromCommunityReviewDueDate: sessionStorage.getItem(this.filterCSFromCommunityReviewDueDate_cache) ?
                sessionStorage.getItem(this.filterCSFromCommunityReviewDueDate_cache) : '',
            filterCSToCommunityReviewDueDate: sessionStorage.getItem(this.filterCSToCommunityReviewDueDate_cache) ?
                sessionStorage.getItem(this.filterCSToCommunityReviewDueDate_cache) : '',

            //Filter list for Community select box
            filterListsCommunities: {},
            communities_data_list: [],
            filterRegionDistrict: {},
            region_list: [],
            district_list: [],
            filtered_district_list: [],
            change_codes: [],
            submitter_categories: [],
            wa_legislative_lists: [],
            wa_legislative_categories: [],
            wa_priority_categories: [],

            internal_status: [
                { value: 'draft', name: 'Draft' },
                { value: 'with_assessor', name: 'With Assessor' },
                { value: 'with_approver', name: 'With Approver' },
                { value: 'ready_for_agenda', name: 'Ready For Agenda' },
                { value: 'closed', name: 'Closed' },
                { value: 'delisted', name: 'DeListed' },
                { value: 'with_referral', name: 'With Referral' },
                { value: 'approved', name: 'Approved' },
                { value: 'declined', name: 'Declined' },
            ],
            processing_statuses: [],
        }
    },
    components: {
        datatable,
        CollapsibleFilters,
        FormSection,
        CommunityConservationStatusHistory,
    },
    watch: {
        filterCSCommunityMigratedId: function () {
            let vm = this;
            vm.$refs.cs_communities_datatable.vmDataTable.ajax.reload(helpers.enablePopovers, false); // This calls ajax() backend call.
            sessionStorage.setItem(vm.filterCSCommunityMigratedId_cache, vm.filterCSCommunityMigratedId);
        },
        filterCSCommunityName: function () {
            let vm = this;
            vm.$refs.cs_communities_datatable.vmDataTable.ajax.reload(helpers.enablePopovers, false); // This calls ajax() backend call.
            sessionStorage.setItem(vm.filterCSCommunityName_cache, vm.filterCSCommunityName);
        },
        filterCSCommunityRegion: function () {
            let vm = this;
            vm.$refs.cs_communities_datatable.vmDataTable.ajax.reload(helpers.enablePopovers, false); // This calls ajax() backend call.
            sessionStorage.setItem(vm.filterCSCommunityRegion_cache, vm.filterCSCommunityRegion);
        },
        filterCSCommunityDistrict: function () {
            let vm = this;
            vm.$refs.cs_communities_datatable.vmDataTable.ajax.reload(helpers.enablePopovers, false); // This calls ajax() backend call.
            sessionStorage.setItem(vm.filterCSCommunityDistrict_cache, vm.filterCSCommunityDistrict);
        },
        filterCSFromCommunityEffectiveFromDate: function () {
            let vm = this;
            vm.$refs.cs_communities_datatable.vmDataTable.ajax.reload(helpers.enablePopovers, false); // This calls ajax() backend call.
            sessionStorage.setItem(vm.filterCSFromCommunityEffectiveFromDate_cache, vm.filterCSFromCommunityEffectiveFromDate);
        },
        filterCSToCommunityEffectiveFromDate: function () {
            let vm = this;
            vm.$refs.cs_communities_datatable.vmDataTable.ajax.reload(helpers.enablePopovers, false); // This calls ajax() backend call.
            sessionStorage.setItem(vm.filterCSToCommunityEffectiveFromDate_cache, vm.filterCSToCommunityEffectiveFromDate);
        },
        filterCSFromCommunityEffectiveToDate: function () {
            let vm = this;
            vm.$refs.cs_communities_datatable.vmDataTable.ajax.reload(helpers.enablePopovers, false); // This calls ajax() backend call.
            sessionStorage.setItem(vm.filterCSFromCommunityEffectiveToDate_cache, vm.filterCSFromCommunityEffectiveToDate);
        },
        filterCSToCommunityEffectiveToDate: function () {
            let vm = this;
            vm.$refs.cs_communities_datatable.vmDataTable.ajax.reload(helpers.enablePopovers, false); // This calls ajax() backend call.
            sessionStorage.setItem(vm.filterCSToCommunityEffectiveToDate_cache, vm.filterCSToCommunityEffectiveToDate);
        },
        filterCSFromCommunityReviewDueDate: function () {
            let vm = this;
            vm.$refs.cs_communities_datatable.vmDataTable.ajax.reload(helpers.enablePopovers, false); // This calls ajax() backend call.
            sessionStorage.setItem(vm.filterCSFromCommunityReviewDueDate_cache, vm.filterCSFromCommunityReviewDueDate);
        },
        filterCSToCommunityReviewDueDate: function () {
            let vm = this;
            vm.$refs.cs_communities_datatable.vmDataTable.ajax.reload(helpers.enablePopovers, false); // This calls ajax() backend call.
            sessionStorage.setItem(vm.filterCSToCommunityReviewDueDate_cache, vm.filterCSToCommunityReviewDueDate);
        },
        filterCSCommunityApplicationStatus: function () {
            let vm = this;
            vm.$refs.cs_communities_datatable.vmDataTable.ajax.reload(helpers.enablePopovers, false); // This calls ajax() backend call.
            sessionStorage.setItem(vm.filterCSCommunityApplicationStatus_cache, vm.filterCSCommunityApplicationStatus);
        },
        filterCSCommunityChangeCode: function () {
            let vm = this;
            vm.$refs.cs_communities_datatable.vmDataTable.ajax.reload(helpers.enablePopovers, false); // This calls ajax() backend call.
            sessionStorage.setItem(vm.filterCSCommunityChangeCode_cache, vm.filterCSCommunityChangeCode);
        },
        filterCSCommunityWALegislativeList: function () {
            let vm = this;
            vm.$refs.cs_communities_datatable.vmDataTable.ajax.reload(helpers.enablePopovers, false); // This calls ajax() backend call.
            sessionStorage.setItem(vm.filterCSCommunityWALegislativeList_cache, vm.filterCSCommunityWALegislativeList);
        },
        filterCSCommunityWALegislativeCategory: function () {
            let vm = this;
            vm.$refs.cs_communities_datatable.vmDataTable.ajax.reload(helpers.enablePopovers, false); // This calls ajax() backend call.
            sessionStorage.setItem(vm.filterCSCommunityWALegislativeCategory_cache, vm.filterCSCommunityWALegislativeCategory);
        },
        filterCSCommunityWAPriorityCategory: function () {
            let vm = this;
            vm.$refs.cs_communities_datatable.vmDataTable.ajax.reload(helpers.enablePopovers, false); // This calls ajax() backend call.
            sessionStorage.setItem(vm.filterCSCommunityWAPriorityCategory_cache, vm.filterCSCommunityWAPriorityCategory);
        },
        filterCSCommunityCommonwealthRelevance: function () {
            let vm = this;
            vm.$refs.cs_communities_datatable.vmDataTable.ajax.reload(helpers.enablePopovers, false); // This calls ajax() backend call.
            sessionStorage.setItem(vm.filterCSCommunityCommonwealthRelevance_cache, vm.filterCSCommunityCommonwealthRelevance);
        },
        filterCSCommunityInternationalRelevance: function () {
            let vm = this;
            vm.$refs.cs_communities_datatable.vmDataTable.ajax.reload(helpers.enablePopovers, false); // This calls ajax() backend call.
            sessionStorage.setItem(vm.filterCSCommunityInternationalRelevance_cache, vm.filterCSCommunityInternationalRelevance);
        },
        filterCSCommunityAssessor: function () {
            let vm = this;
            vm.$refs.cs_communities_datatable.vmDataTable.ajax.reload(helpers.enablePopovers, false); // This calls ajax() backend call.
            sessionStorage.setItem(vm.filterCSCommunityAssessor_cache, vm.filterCSCommunityAssessor);
        },
        filterCSCommunitySubmitter: function () {
            let vm = this;
            vm.$refs.cs_communities_datatable.vmDataTable.ajax.reload(helpers.enablePopovers, false); // This calls ajax() backend call.
            sessionStorage.setItem(vm.filterCSCommunitySubmitter_cache, vm.filterCSCommunitySubmitter);
        },
        filterCSCommunitySubmitterCategory: function () {
            let vm = this;
            vm.$refs.cs_communities_datatable.vmDataTable.ajax.reload(helpers.enablePopovers, false); // This calls ajax() backend call.
            sessionStorage.setItem(vm.filterCSCommunitySubmitterCategory_cache, vm.filterCSCommunitySubmitterCategory);
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
            if (this.filterCSCommunityMigratedId === 'all' &&
                this.filterCSCommunityName === 'all' &&
                this.filterCSCommunityRegion === 'all' &&
                this.filterCSCommunityDistrict === 'all' &&
                this.filterCSCommunityChangeCode === 'all' &&
                this.filterCSCommunityWALegislativeList === 'all' &&
                this.filterCSCommunityWALegislativeCategory === 'all' &&
                this.filterCSCommunityWAPriorityCategory === 'all' &&
                this.filterCSCommunityCommonwealthRelevance === 'false' &&
                this.filterCSCommunityInternationalRelevance === 'false' &&
                this.filterCSCommunityAssessor === 'all' &&
                this.filterCSCommunitySubmitter === 'all' &&
                this.filterCSCommunitySubmitterCategory === 'all' &&
                this.filterCSCommunityApplicationStatus === 'approved' &&
                this.filterCSFromCommunityEffectiveFromDate === '' &&
                this.filterCSToCommunityEffectiveFromDate === '' &&
                this.filterCSFromCommunityEffectiveToDate === '' &&
                this.filterCSToCommunityEffectiveToDate === '' &&
                this.filterCSFromCommunityReviewDueDate === '' &&
                this.filterCSToCommunityReviewDueDate === '') {
                return false
            } else {
                return true
            }
        },
        is_referral: function () {
            return this.level == 'referral';
        },
        addCommunityCSVisibility: function () {
            return this.profile && this.profile.groups.find(
                (i) => [
                    constants.GROUPS.INTERNAL_CONTRIBUTORS
                ].includes(i)
            );
        },
        datatable_headers: function () {
            return ['Number', 'Community', 'Community Id', 'Community Name', 'Region', 'District', 'Change Type', 'WA Priority List',
                'WA Priority Category', 'WA Legislative List', 'WA Legislative Category', 'Commonwealth Conservation List', 'International Conservation',
                'Conservation Criteria',
                'Submitter Name', 'Submitter Category', 'Submitter Organisation', 'Assessor Name', 'Effective From Date', 'Effective To Date', 'Review Due Date',
                'Status', 'Action']
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
                    if (full.is_new_contributor) {
                        value += ' <span class="badge bg-warning">New Contributor</span>'
                    }
                    return value
                },
                name: "id",
            }
        },
        column_community_number: function () {
            return {
                data: "community_number",
                orderable: true,
                searchable: true,
                visible: true,
                'render': function (data, type, full) {
                    return full.community_number
                },
                name: "community__community_number",
            }
        },
        column_community_id: function () {
            return {
                data: "community_migrated_id",
                orderable: true,
                searchable: true,
                visible: true,
                'render': function (value, type) {
                    let result = helpers.dtPopover(value, 30, 'hover');
                    return type == 'export' ? value : result;
                },
                name: "community__taxonomy__community_migrated_id",
            }
        },
        column_community_name: function () {
            return {
                data: "community_name",
                orderable: true,
                searchable: true,
                visible: true,
                'render': function (value, type) {
                    let result = helpers.dtPopover(value, 30, 'hover');
                    return type == 'export' ? value : result;
                },
                //'createdCell': helpers.dtPopoverCellFn,
                name: "community__taxonomy__community_name",
            }
        },
        column_status: function () {
            return {
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
                searchable: false,
                visible: true,
                'render': function (data, type, full) {
                    if (full.region) {
                        return full.region;
                    }
                    // Should not reach here
                    return ''
                },
                name: "community__region__name",
            }
        },
        column_district: function () {
            return {
                data: "district",
                orderable: true,
                searchable: false, // handles by filter_queryset override method - class ProposalFilterBackend
                visible: true,
                'render': function (data, type, full) {
                    if (full.district) {
                        return full.district
                    }
                    // Should not reach here
                    return ''
                },
                name: "community__district__name",
            }
        },
        column_change_code: function () {
            return {
                data: "change_code",
                orderable: true,
                searchable: false,
                visible: true,
                name: "change_code__code",
            }
        },
        column_wa_priority_list: function () {
            return {
                data: "wa_priority_list",
                orderable: true,
                searchable: false,
                visible: true,
                name: "wa_priority_list__code",
            }
        },
        column_wa_priority_category: function () {
            return {
                data: "wa_priority_category",
                orderable: true,
                searchable: false,
                visible: true,
                name: "wa_priority_category__code",
            }
        },
        column_wa_legislative_list: function () {
            return {
                data: "wa_legislative_list",
                orderable: true,
                searchable: false,
                visible: true,
                name: "wa_legislative_list__code",
            }
        },
        column_wa_legislative_category: function () {
            return {
                data: "wa_legislative_category",
                orderable: true,
                searchable: false,
                visible: true,
                name: "wa_legislative_category__code",
            }
        },
        column_commonwealth_conservation_list: function () {
            return {
                data: "commonwealth_conservation_list",
                orderable: true,
                searchable: false,
                visible: true,
                name: "commonwealth_conservation_list",
            }
        },
        column_international_conservation:
            function () {
                return {
                    data: "international_conservation",
                    orderable: true,
                    searchable: true,
                    visible: true,
                    name: "international_conservation",
                }
            },
        column_conservation_criteria: function () {
            return {
                data: "conservation_criteria",
                orderable: true,
                searchable: true,
                visible: true,
                name: "conservation_criteria",
            }
        },
        column_submitter_name: function () {
            return {
                data: "submitter_name",
                orderable: true,
                searchable: true,
                visible: true,
                name: "submitter_information__name",
            }
        },
        column_submitter_category: function () {
            return {
                data: "submitter_category",
                orderable: true,
                searchable: false,
                visible: true,
                name: "submitter_information__submitter_category__name",
            }
        },
        column_submitter_organisation: function () {
            return {
                data: "submitter_organisation",
                orderable: true,
                searchable: true,
                visible: true,
                name: "submitter_information__organisation",
            }
        },
        column_assessor_name: function () {
            return {
                data: "assessor_name",
                orderable: true,
                searchable: false,
                visible: true,
            }
        },
        column_effective_from: function () {
            return {
                data: "effective_from",
                orderable: true,
                searchable: true, // handles by filter_queryset override method
                visible: true,
                name: "effective_from",
            }
        },
        column_effective_to: function () {
            return {
                data: "effective_to",
                orderable: true,
                searchable: true,
                visible: true,
                name: "effective_to",
            }
        },
        column_review_due_date: function () {
            return {
                data: "review_due_date",
                orderable: true,
                searchable: false,
                visible: true,
            }
        },
        column_action: function () {
            let vm = this
            return {
                // 9. Action
                data: "id",
                orderable: false,
                searchable: false,
                visible: true,
                'render': function (data, type, full) {
                    let links = "";
                    if (vm.is_for_agenda == false) {
                        if (full.internal_user_edit) {
                            links += `<a href='/internal/conservation_status/${full.id}'>Continue</a><br/>`;
                            links += `<a href='#${full.id}' data-discard-cs-proposal='${full.id}'>Discard</a><br/>`;
                            links += `<a href='#' data-history-conservation-status-community='${full.id}'
                            data-history-community='${full.community_number}'
                            data-history-conservation-list='${full.conservation_list}'>History</a><br>`;
                        }
                        else {
                            if (full.assessor_process) {
                                links += `<a href='/internal/conservation_status/${full.id}'>Process</a><br/>`;
                                links += `<a href='#' data-history-conservation-status-community='${full.id}'
                                    data-history-community='${full.community_number}'
                                    data-history-conservation-list='${full.conservation_list}'>History</a><br>`;
                            }
                            else {
                                links += `<a href='/internal/conservation_status/${full.id}?action=view'>View</a><br/>`;
                                links += `<a href='#' data-history-conservation-status-community='${full.id}'
                                data-history-community='${full.community_number}'
                                data-history-conservation-list='${full.conservation_list}'>History</a><br>`;
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

            columns = [
                vm.column_number,
                vm.column_community_number,
                vm.column_community_id,
                vm.column_community_name,
                vm.column_region,
                vm.column_district,
                vm.column_change_code,
                vm.column_wa_priority_list,
                vm.column_wa_priority_category,
                vm.column_wa_legislative_list,
                vm.column_wa_legislative_category,
                vm.column_commonwealth_conservation_list,
                vm.column_international_conservation,
                vm.column_conservation_criteria,
                vm.column_submitter_name,
                vm.column_submitter_category,
                vm.column_submitter_organisation,
                vm.column_assessor_name,
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
                    { responsivePriority: 3, targets: -1 },
                    { responsivePriority: 2, targets: -2 }
                ],
                ajax: {
                    "url": this.url,
                    "dataSrc": 'data',
                    "method": 'post',
                    headers: {
                        'X-CSRFToken': helpers.getCookie('csrftoken'),
                    },
                    // adding extra params for Custom filtering
                    "data": function (d) {
                        d.filter_community_migrated_id = vm.filterCSCommunityMigratedId;
                        d.filter_community_name = vm.filterCSCommunityName;
                        d.filter_group_type = vm.group_type_name;
                        d.filter_region = vm.filterCSCommunityRegion;
                        d.filter_district = vm.filterCSCommunityDistrict;
                        d.filter_change_code = vm.filterCSCommunityChangeCode;
                        d.filter_wa_legislative_list = vm.filterCSCommunityWALegislativeList;
                        d.filter_wa_legislative_category = vm.filterCSCommunityWALegislativeCategory;
                        d.filter_wa_priority_category = vm.filterCSCommunityWAPriorityCategory;
                        d.filter_commonwealth_relevance = vm.filterCSCommunityCommonwealthRelevance;
                        d.filter_international_relevance = vm.filterCSCommunityInternationalRelevance;
                        d.filter_assessor = vm.filterCSCommunityAssessor;
                        d.filter_submitter = vm.filterCSCommunitySubmitter;
                        d.filter_submitter_category = vm.filterCSCommunitySubmitterCategory;
                        d.filter_application_status = vm.filterCSCommunityApplicationStatus;
                        d.filter_from_effective_from_date = vm.filterCSFromCommunityEffectiveFromDate;
                        d.filter_to_effective_from_date = vm.filterCSToCommunityEffectiveFromDate;
                        d.filter_from_effective_to_date = vm.filterCSFromCommunityEffectiveToDate;
                        d.filter_to_effective_to_date = vm.filterCSToCommunityEffectiveToDate;
                        d.filter_from_review_due_date = vm.filterCSFromCommunityReviewDueDate;
                        d.filter_to_review_due_date = vm.filterCSToCommunityReviewDueDate;
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
        historyDocument: function (id, list, community) {
            this.communityConservationStatusHistoryId = parseInt(id);
            this.listHistoryId = list ? list : "List not specified";
            this.communityHistoryId = community ? community : "not specified";
            this.uuid++;
            this.$nextTick(() => {
                this.$refs.community_conservation_status_history.isModalOpen = true;
            });
        },
        collapsible_component_mounted: function () {
            this.$refs.collapsible_filters.show_warning_icon(this.filterApplied)
        },
        initialiseCommunityNameLookup: function () {
            let vm = this;
            $(vm.$refs.cs_community_name_lookup).select2({
                minimumInputLength: 2,
                dropdownParent: $("#select_community_name"),
                "theme": "bootstrap-5",
                allowClear: true,
                placeholder: "Select Community Name",
                ajax: {
                    url: api_endpoints.community_name_lookup,
                    dataType: 'json',
                    data: function (params) {
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
                    vm.filterCSCommunityName = data;
                    sessionStorage.setItem("filterCSCommunityNameText", e.params.data.text);
                }).
                on("select2:unselect", function (e) {
                    var selected = $(e.currentTarget);
                    vm.filterCSCommunityName = 'all';
                    sessionStorage.setItem("filterCSCommunityNameText", '');
                }).
                on("select2:open", function (e) {
                    const searchField = $('[aria-controls="select2-cs_community_name_lookup-results"]')
                    // move focus to select2 field
                    searchField[0].focus();
                });
        },
        initialiseCommunityIdLookup: function () {
            let vm = this;
            $(vm.$refs.cs_community_id_lookup).select2({
                minimumInputLength: 1,
                dropdownParent: $("#select_community_id"),
                "theme": "bootstrap-5",
                allowClear: true,
                placeholder: "Select Community ID",
                ajax: {
                    url: api_endpoints.community_id_lookup,
                    dataType: 'json',
                    data: function (params) {
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
                    vm.filterCSCommunityMigratedId = data;
                    sessionStorage.setItem("filterCSCommunityMigratedIdText", e.params.data.text);
                }).
                on("select2:unselect", function (e) {
                    var selected = $(e.currentTarget);
                    vm.filterCSCommunityMigratedId = 'all';
                    sessionStorage.setItem("filterCSCommunityMigratedIdText", '');
                }).
                on("select2:open", function (e) {
                    const searchField = $('[aria-controls="select2-cs_community_id_lookup-results"]')
                    // move focus to select2 field
                    searchField[0].focus();
                });
        },
        initialiseAssessorLookup: function () {
            let vm = this;
            $(vm.$refs.cs_assessor_lookup).select2({
                minimumInputLength: 2,
                "theme": "bootstrap-5",
                allowClear: true,
                placeholder: "Search for Assessor",
                ajax: {
                    url: api_endpoints.users_api + '/get_department_users_ledger_id/',
                    dataType: 'json',
                    data: function (params) {
                        var query = {
                            term: params.term,
                        }
                        return query;
                    },
                },
            })
                .on("select2:select", function (e) {
                    let data = e.params.data.id;
                    vm.filterCSCommunityAssessor = data;
                    sessionStorage.setItem("filterCSCommunityAssessorText", e.params.data.text);
                })
                .on("select2:unselect", function (e) {
                    vm.filterCSCommunityAssessor = 'all';
                    sessionStorage.setItem("filterCSCommunityAssessorText", '');
                })
                .on("select2:open", function (e) {
                    const searchField = $('[aria-controls="select2-cs_assessor_lookup-results"]')
                    searchField[0].focus();
                });
        },
        initialiseSubmitterLookup: function () {
            let vm = this;
            $(vm.$refs.cs_submitter_lookup).select2({
                minimumInputLength: 2,
                "theme": "bootstrap-5",
                allowClear: true,
                placeholder: "Search for Submitter",
                ajax: {
                    url: api_endpoints.users_api + '/get_users_ledger_id/',
                    dataType: 'json',
                    data: function (params) {
                        var query = {
                            term: params.term,
                        }
                        return query;
                    },
                },
            })
                .on("select2:select", function (e) {
                    let data = e.params.data.id;
                    vm.filterCSCommunitySubmitter = data;
                    sessionStorage.setItem("filterCSCommunitySubmitterText", e.params.data.text);
                })
                .on("select2:unselect", function (e) {
                    vm.selected_referral = null;
                    vm.filterCSCommunitySubmitter = 'all';
                    sessionStorage.setItem("filterCSCommunitySubmitterText", '');
                })
                .on("select2:open", function (e) {
                    const searchField = $('[aria-controls="select2-cs_submitter_lookup-results"]')
                    searchField[0].focus();
                });
        },
        fetchFilterLists: function () {
            let vm = this;

            vm.$http.get(api_endpoints.community_filter_dict + '?group_type_name=' + vm.group_type_name).then((response) => {
                vm.filterListsCommunities = response.body;
                vm.communities_data_list = vm.filterListsCommunities.community_data_list;
                vm.filterDistrict();
                vm.wa_legislative_lists = vm.filterListsCommunities.wa_legislative_lists;
                vm.wa_legislative_categories = vm.filterListsCommunities.wa_legislative_categories;
                vm.wa_priority_lists = vm.filterListsCommunities.wa_priority_lists;
                vm.wa_priority_categories = vm.filterListsCommunities.wa_priority_categories;
                vm.processing_statuses = vm.internal_status.slice().sort((a, b) => {
                    return a.name.trim().localeCompare(b.name.trim());
                });
                vm.change_codes = vm.filterListsCommunities.change_codes;
                vm.submitter_categories = vm.filterListsCommunities.submitter_categories;
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
        //-------filter district dropdown dependent on region selected
        filterDistrict: function (event) {
            this.$nextTick(() => {
                if (event) {
                    this.filterCSCommunityDistrict = 'all'; //-----to remove the previous selection
                }
                this.filtered_district_list = [];
                //---filter districts as per region selected
                for (let choice of this.district_list) {
                    if (choice.region_id.toString() === this.filterCSCommunityRegion.toString()) {
                        this.filtered_district_list.push(choice);
                    }
                }
            });
        },
        createCommunityConservationStatus: async function () {
            let newCommunityCSId = null
            try {
                const createUrl = api_endpoints.conservation_status + "/";
                let payload = new Object();
                payload.application_type_id = this.group_type_id
                payload.internal_application = true
                let savedCommunityCS = await Vue.http.post(createUrl, payload);
                if (savedCommunityCS) {
                    newCommunityCSId = savedCommunityCS.body.id;
                }
            }
            catch (err) {
                console.log(err);
            }
            this.$router.push({
                name: 'internal-conservation_status',
                params: { conservation_status_id: newCommunityCSId },
            });
        },
        discardCSProposal: function (conservation_status_id) {
            let vm = this;
            swal.fire({
                title: "Discard Conservation Status Proposal",
                text: "Are you sure you want to discard this proposal?",
                icon: "question",
                showCancelButton: true,
                confirmButtonText: 'Discard Proposal',
                customClass: {
                    confirmButton: 'btn btn-primary',
                    cancelButton: 'btn btn-secondary',
                },
                reverseButtons: true,
            }).then((result) => {
                if (result.isConfirmed) {
                    vm.$http.patch(api_endpoints.discard_cs_proposal(conservation_status_id))
                        .then((response) => {
                            swal.fire({
                                title: 'Discarded',
                                text: 'Your proposal has been discarded',
                                icon: 'success',
                                confirmButtonColor: '#226fbb',
                            });
                            vm.$refs.cs_communities_datatable.vmDataTable.ajax.reload(helpers.enablePopovers, false);
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
                vm.$refs.cs_communities_datatable.vmDataTable.ajax.reload(helpers.enablePopovers, false);
                this.$emit('updateAgendaItems');
            },
                err => {
                    console.log(err);
                });
        },
        addEventListeners: function () {
            let vm = this;
            // internal Discard listener
            vm.$refs.cs_communities_datatable.vmDataTable.on('click', 'a[data-discard-cs-proposal]', function (e) {
                e.preventDefault();
                var id = $(this).attr('data-discard-cs-proposal');
                vm.discardCSProposal(id);
            });
            vm.$refs.cs_communities_datatable.vmDataTable.on('click', 'a[data-add-to-agenda]', function (e) {
                e.preventDefault();
                var id = $(this).attr('data-add-to-agenda');
                vm.addToMeetingAgenda(id);
            });
            vm.$refs.cs_communities_datatable.vmDataTable.on('click', 'a[data-history-conservation-status-community]', function (e) {
                e.preventDefault();
                var id = $(this).attr('data-history-conservation-status-community');
                var list = $(this).attr('data-history-conservation-list');
                var community = $(this).attr('data-history-community');
                vm.historyDocument(id, list, community);
            });
            vm.$refs.cs_communities_datatable.vmDataTable.on('childRow.dt', function (e, settings) {
                helpers.enablePopovers();
            });
        },
        initialiseSearch: function () {
            this.submitterSearch();
        },
        submitterSearch: function () {
            let vm = this;
            vm.$refs.cs_communities_datatable.table.dataTableExt.afnFiltering.push(
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
                    "searchable": "true",
                    "orderable": "true",
                    "search": {
                        "value": "",
                        "regex": "false"
                    }
                },
                "1": {
                    "data": "community_number",
                    "name": "conservation_status__community__community_number",
                    "searchable": "true",
                    "orderable": "true",
                    "search": {
                        "value": "",
                        "regex": "false"
                    }
                },
                "2": {
                    "data": "community_migrated_id",
                    "name": "conservation_status__community__community_migrated_id",
                    "searchable": "true",
                    "orderable": "true",
                    "search": {
                        "value": "",
                        "regex": "false"
                    }
                },
                "3": {
                    "data": "community_name",
                    "name": "conservation_status__community__community_name__name",
                    "searchable": "true",
                    "orderable": "true",
                    "search": {
                        "value": "",
                        "regex": "false"
                    }
                },
                "4": {
                    "data": "conservation_list",
                    "name": "conservation_status__conservation_list__code",
                    "searchable": "true",
                    "orderable": "true",
                    "search": {
                        "value": "",
                        "regex": "false"
                    }
                },
                "5": {
                    "data": "conservation_category",
                    "name": "conservation_status__conservation_category__code",
                    "searchable": "true",
                    "orderable": "true",
                    "search": {
                        "value": "",
                        "regex": "false"
                    }
                },
                "6": {
                    "data": "family",
                    "name": "species__taxonomy__family__name",
                    "searchable": "true",
                    "orderable": "true",
                    "search": {
                        "value": "",
                        "regex": "false"
                    }
                },
                "7": {
                    "data": "genus",
                    "name": "species__taxonomy__genus__name",
                    "searchable": "true",
                    "orderable": "true",
                    "search": {
                        "value": "",
                        "regex": "false"
                    }
                },
                "8": {
                    "data": "processing_status",
                    "name": "conservation_status__processing_status",
                    "searchable": "true",
                    "orderable": "true",
                    "search": {
                        "value": "",
                        "regex": "false"
                    }
                },
                "9": {
                    "data": "id",
                    "name": "",
                    "searchable": "false",
                    "orderable": "false",
                    "search": {
                        "value": "",
                        "regex": "false"
                    }
                },
                "10": {
                    "data": "conservation_status",
                    "name": "",
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
                filter_community_migrated_id: vm.filterCSCommunityMigratedId,
                filter_group_type: vm.group_type_name,
                filter_community_name: vm.filterCSCommunityName,
                filter_application_status: vm.filterCSCommunityApplicationStatus,
                filter_region: vm.filterCSCommunityRegion,
                filter_district: vm.filterCSCommunityDistrict,
                filter_change_code: vm.filterCSCommunityChangeCode,
                filter_wa_legislative_list: vm.filterCSCommunityWALegislativeList,
                filter_wa_legislative_category: vm.filterCSCommunityWALegislativeCategory,
                filter_wa_priority_category: vm.filterCSCommunityWAPriorityCategory,
                filter_commonwealth_relevance: vm.filterCSCommunityCommonwealthRelevance,
                filter_international_relevance: vm.filterCSCommunityInternationalRelevance,
                filter_application_status: vm.filterCSCommunityApplicationStatus,
                filter_assessor: vm.filterCSCommunityAssessor,
                filter_submitter: vm.filterCSCommunitySubmitter,
                filter_submitter_category: vm.filterCSCommunitySubmitterCategory,
                filter_from_effective_from_date: vm.filterCSFromCommunityEffectiveFromDate,
                filter_to_effective_from_date: vm.filterCSToCommunityEffectiveFromDate,
                filter_from_effective_to_date: vm.filterCSFromCommunityEffectiveToDate,
                filter_to_effective_to_date: vm.filterCSToCommunityEffectiveToDate,
                filter_from_review_due_date: vm.filterCSFromCommunityReviewDueDate,
                filter_to_review_due_date: vm.filterCSToCommunityReviewDueDate,
                export_format: format
            };

            const url = api_endpoints.community_cs_internal_export;
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
                        type: "POST",
                        headers: {
                            'X-CSRFToken': helpers.getCookie('csrftoken'),
                        },
                        url: url + "/",
                        data: object_load,
                        //contentType: "application/vnd.ms-excel",
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
                        type: "POST",
                        headers: {
                            'X-CSRFToken': helpers.getCookie('csrftoken'),
                        },
                        url: url + "/",
                        data: object_load,
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
            vm.initialiseCommunityNameLookup();
            vm.initialiseCommunityIdLookup();
            vm.initialiseAssessorLookup();
            vm.initialiseSubmitterLookup();
            vm.addEventListeners();
            // -- to set the select2 field with the session value if exists onload()
            if (sessionStorage.getItem("filterCSCommunityName") != 'all' && sessionStorage.getItem("filterCSCommunityName") != null) {
                // contructor new Option(text, value, defaultSelected, selected)
                var newOption = new Option(sessionStorage.getItem("filterCSCommunityNameText"), vm.filterCSCommunityName, false, true);
                $('#cs_community_name_lookup').append(newOption);
            }
            if (sessionStorage.getItem("filterCSCommunityMigratedId") != 'all' && sessionStorage.getItem("filterCSCommunityMigratedId") != null) {
                // contructor new Option(text, value, defaultSelected, selected)
                var newOption = new Option(sessionStorage.getItem("filterCSCommunityMigratedIdText"), vm.filterCSCommunityMigratedId, false, true);
                $('#cs_community_id_lookup').append(newOption);
            }
        });
    }
}
</script>
<style scoped>
.dt-buttons {
    float: right;
}
</style>
