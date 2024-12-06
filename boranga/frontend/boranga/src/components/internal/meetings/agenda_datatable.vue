<template lang="html">
    <div id="AgendaModal">
        <modal transition="modal fade" @ok="ok()" @cancel="cancel()" :title="title" large id="agenda-modal">
            <div class="container-fluid">
                <div class="row">
                    <form class="form-horizontal" name="agendaForm">
                        <alert v-if="showError" type="danger"><strong>{{ errorString }}</strong></alert>
                        <div>
                            <div class="col-md-12">
                                <ul class="nav nav-pills" id="pills-tab" role="tablist">
                                    <li class="nav-item">
                                        <a class="nav-link" id="pills-flora-tab" data-bs-toggle="pill"
                                            href="#pills-flora" role="tab" aria-controls="pills-flora"
                                            aria-selected="true"
                                            @click="set_active_tab('pills-flora', 'flora')">Flora</a>
                                    </li>
                                    <li class="nav-item">
                                        <a class="nav-link" id="pills-fauna-tab" data-bs-toggle="pill"
                                            href="#pills-fauna" role="tab" aria-controls="pills-fauna"
                                            aria-selected="false"
                                            @click="set_active_tab('pills-fauna', 'fauna')">Fauna</a>
                                    </li>
                                    <li class="nav-item">
                                        <a class="nav-link" id="pills-community-tab" data-bs-toggle="pill"
                                            href="#pills-community" role="tab" aria-controls="pills-community"
                                            aria-selected="false"
                                            @click="set_active_tab('pills-community', 'community')">Communities</a>
                                    </li>
                                </ul>
                                <div class="tab-content" id="pills-tabContent">
                                    <div class="tab-pane" id="pills-flora" role="tabpanel"
                                        aria-labelledby="pills-flora-tab">
                                        <FormSection :formCollapse="false" label="Conservation Status - Flora"
                                            Index="flora">
                                            <ConservationStatusFloraDashTable v-if="isFlora" ref="flora_table"
                                                level="internal" :group_type_name="group_name"
                                                :group_type_id="getGroupId" :url="species_agenda_cs_url"
                                                :is_for_agenda="for_agenda" :meeting_obj="meeting_obj"
                                                filterCSFloraScientificName_cache="filterCSFloraScientificNameAgenda"
                                                filterCSFloraCommonName_cache="filterCSFloraCommonNameAgenda"
                                                filterCSFloraPhylogeneticGroup_cache="filterCSFloraPhylogeneticGroupAgenda"
                                                filterCSFloraFamily_cache="filterCSFloraFamilyAgenda"
                                                filterCSFloraGenus_cache="filterCSFloraGenusAgenda"
                                                filterCSFloraChangeCode_cache="filterCSFloraChangeCodeAgenda"
                                                filterCSFloraWALegislativeList_cache="filterCSFloraWALegislativeListAgenda"
                                                filterCSFloraWALegislativeCategory_cache="filterCSFloraWALegislativeCategoryAgenda"
                                                filterCSFloraWAPriorityCategory_cache="filterCSFloraWAPriorityCategoryAgenda"
                                                filterCSFloraCommonwealthRelevance_cache="filterCSFloraCommonwealthRelevanceAgenda"
                                                filterCSFloraInternationalRelevance_cache="filterCSFloraInternationalRelevanceAgenda"
                                                filterCSFloraAssessor_cache="filterCSFloraAssessorAgenda"
                                                filterCSFloraSubmitter_cache="filterCSFloraSubmitterAgenda"
                                                filterCSFloraSubmitterCategory_cache="filterCSFloraSubmitterCategoryAgenda"
                                                filterCSFloraApplicationStatus_cache="filterCSFloraApplicationStatusAgenda"
                                                filterCSFromFloraEffectiveFromDate_cache="filterCSFromFloraEffectiveFromDateAgenda"
                                                filterCSToFloraEffectiveFromDate_cache="filterCSToFloraEffectiveFromDateAgenda"
                                                filterCSFromFloraEffectiveToDate_cache="filterCSFromFloraEffectiveToDateAgenda"
                                                filterCSToFloraEffectiveToDate_cache="filterCSToFloraEffectiveToDateAgenda"
                                                filterCSFromFloraReviewDueDate_cache="filterCSFromFloraReviewDueDateAgenda"
                                                filterCSToFloraReviewDueDate_cache="filterCSToFloraReviewDueDateAgenda"
                                                @updateAgendaItems="updateAgendaItems" />
                                        </FormSection>
                                    </div>
                                    <div class="tab-pane" id="pills-fauna" role="tabpanel"
                                        aria-labelledby="pills-fauna-tab">
                                        <FormSection :formCollapse="false" label="Conservation Status - Fauna"
                                            Index="fauna">
                                            <ConservationStatusFaunaDashTable v-if="isFauna" ref="fauna_table"
                                                level="internal" :group_type_name="group_name"
                                                :group_type_id="getGroupId" :url="species_agenda_cs_url"
                                                :is_for_agenda="for_agenda" :meeting_obj="meeting_obj"
                                                filterCSFaunaScientificName_cache="filterCSFaunaScientificNameAgenda"
                                                filterCSFaunaCommonName_cache="filterCSFaunaCommonNameAgenda"
                                                filterCSFaunaPhylogeneticGroup_cache="filterCSFaunaPhylogeneticGroupAgenda"
                                                filterCSFaunaFamily_cache="filterCSFaunaFamilyAgenda"
                                                filterCSFaunaGenus_cache="filterCSFaunaGenusAgenda"
                                                filterCSFaunaChangeCode_cache="filterCSFaunaChangeCodeAgenda"
                                                filterCSFaunaWALegislativeList_cache="filterCSFaunaWALegislativeListAgenda"
                                                filterCSFaunaWALegislativeCategory_cache="filterCSFaunaWALegislativeCategoryAgenda"
                                                filterCSFaunaWAPriorityCategory_cache="filterCSFaunaWAPriorityCategoryAgenda"
                                                filterCSFaunaCommonwealthRelevance_cache="filterCSFaunaCommonwealthRelevanceAgenda"
                                                filterCSFaunaInternationalRelevance_cache="filterCSFaunaInternationalRelevanceAgenda"
                                                filterCSFaunaAssessor_cache="filterCSFaunaAssessorAgenda"
                                                filterCSFaunaSubmitter_cache="filterCSFaunaSubmitterAgenda"
                                                filterCSFaunaSubmitterCategory_cache="filterCSFaunaSubmitterCategoryAgenda"
                                                filterCSFaunaApplicationStatus_cache="filterCSFaunaApplicationStatusAgenda"
                                                filterCSFromFaunaEffectiveFromDate_cache="filterCSFromFaunaEffectiveFromDateAgenda"
                                                filterCSToFaunaEffectiveFromDate_cache="filterCSToFaunaEffectiveFromDateAgenda"
                                                filterCSFromFaunaEffectiveToDate_cache="filterCSFromFaunaEffectiveToDateAgenda"
                                                filterCSToFaunaEffectiveToDate_cache="filterCSToFaunaEffectiveToDateAgenda"
                                                filterCSFromFaunaReviewDueDate_cache="filterCSFromFaunaReviewDueDateAgenda"
                                                filterCSToFaunaReviewDueDate_cache="filterCSToFaunaReviewDueDateAgenda"
                                                @updateAgendaItems="updateAgendaItems" />
                                        </FormSection>
                                    </div>
                                    <div class="tab-pane" id="pills-community" role="tabpanel"
                                        aria-labelledby="pills-community-tab">
                                        <FormSection :formCollapse="false" label="Conservation Status - Community"
                                            Index="community">
                                            <ConservationStatusCommunityDashTable v-if="isCommunity"
                                                ref="community_table" level="internal" :group_type_name="group_name"
                                                :group_type_id="getGroupId" :url="community_agenda_cs_url"
                                                :is_for_agenda="for_agenda" :meeting_obj="meeting_obj"
                                                filterCSCommunityMigratedId_cache="filterCSCommunityMigratedIdAgenda"
                                                filterCSCommunityName_cache="filterCSCommunityNameAgenda"
                                                filterCSCommunityChangeCode_cache="filterCSCommunityChangeCodeAgenda"
                                                filterCSCommunityWALegislativeList_cache="filterCSCommunityWALegislativeListAgenda"
                                                filterCSCommunityWALegislativeCategory_cache="filterCSCommunityWALegislativeCategoryAgenda"
                                                filterCSCommunityWAPriorityCategory_cache="filterCSCommunityWAPriorityCategoryAgenda"
                                                filterCSCommunityCommonwealthRelevance_cache="filterCSCommunityCommonwealthRelevanceAgenda"
                                                filterCSCommunityInternationalRelevance_cache="filterCSCommunityInternationalRelevanceAgenda"
                                                filterCSCommunityAssessor_cache="filterCSCommunityAssessorAgenda"
                                                filterCSCommunitySubmitter_cache="filterCSCommunitySubmitterAgenda"
                                                filterCSCommunitySubmitterCategory_cache="filterCSCommunitySubmitterCategoryAgenda"
                                                filterCSCommunityApplicationStatus_cache="filterCSCommunityApplicationStatusAgenda"
                                                filterCSFromCommunityEffectiveFromDate_cache="filterCSFromCommunityEffectiveFromDateAgenda"
                                                filterCSToCommunityEffectiveFromDate_cache="filterCSToCommunityEffectiveFromDateAgenda"
                                                filterCSFromCommunityEffectiveToDate_cache="filterCSFromCommunityEffectiveToDateAgenda"
                                                filterCSToCommunityEffectiveToDate_cache="filterCSToCommunityEffectiveToDateAgenda"
                                                filterCSFromCommunityReviewDueDate_cache="filterCSFromCommunityReviewDueDateAgenda"
                                                filterCSToCommunityReviewDueDate_cache="filterCSToCommunityReviewDueDateAgenda"
                                                @updateAgendaItems="updateAgendaItems" />
                                        </FormSection>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </form>
                </div>
            </div>

            <div slot="footer">
                <button type="button" class="btn btn-primary pull-right" @click="cancel">Close</button>
            </div>
        </modal>
    </div>
</template>

<script>
import modal from '@vue-utils/bootstrap-modal.vue'
import alert from '@vue-utils/alert.vue'
import ConservationStatusFloraDashTable from '@common-utils/conservation_status_flora_dashboard.vue'
import ConservationStatusFaunaDashTable from '@common-utils/conservation_status_fauna_dashboard.vue'
import ConservationStatusCommunityDashTable from '@common-utils/conservation_status_community_dashboard.vue'
import FormSection from '@/components/forms/section_toggle.vue'
import { helpers, api_endpoints } from "@/utils/hooks.js"

export default {
    name: 'AgendaModal',
    components: {
        modal,
        alert,
        ConservationStatusFloraDashTable,
        ConservationStatusFaunaDashTable,
        ConservationStatusCommunityDashTable,
        FormSection,
    },
    props: {
        meeting_obj: {
            type: Object,
            required: true
        },
        is_internal: {
            type: Boolean,
            required: true
        },
    },
    data: function () {
        let vm = this;
        return {
            isModalOpen: false,
            new_species_list: [],
            group_types: [],
            group_name: null,
            species_agenda_cs_url: api_endpoints.species_agenda_conservation_status_paginated_internal,
            community_agenda_cs_url: api_endpoints.community_agenda_conservation_status_paginated_internal,
            for_agenda: true,
            form: null,
            errors: false,
            errorString: '',
        }
    },
    computed: {
        csrf_token: function () {
            return helpers.getCookie('csrftoken')
        },
        showError: function () {
            var vm = this;
            return vm.errors;
        },
        title: function () {
            return 'Agenda (Add Conservation Status)';
        },
        isFlora: function () {
            return this.group_name == 'flora' && this.$parent.updateModal === true; // parent condition checked as to resolve the datatable css problem onload
        },
        isFauna: function () {
            return this.group_name == 'fauna';
        },
        isCommunity: function () {
            return this.group_name == 'community';
        },
        getGroupId: function () {
            for (var i = 0; i < this.group_types.length; i++) {
                if (this.group_name === this.group_types[i].name) {
                    return this.group_types[i].id;
                }
            }
        }
    },
    methods: {
        updateAgendaItems: function () {
            let vm = this;
            vm.$parent.updateAgendaItems();
        },
        cancel: function () {
            this.close()
        },
        close: function () {
            this.$parent.updateModal = false;
            this.isModalOpen = false;
        },
        set_active_tab: function (tab_href_name, group_name) {
            this.group_name = group_name;
            let elem = $('#pills-tab a[href="#' + tab_href_name + '"]')
            let tab = bootstrap.Tab.getInstance(elem)
            if (!tab)
                tab = new bootstrap.Tab(elem)
            tab.show()
        },
    },
    mounted: function () {
        let vm = this;
        this.$nextTick(function () {
            chevron_toggle.init();
            vm.set_active_tab('pills-flora', 'flora');
        })
    },
    created: function () {
        fetch(api_endpoints.group_types_dict).then(async (response) => {
            this.group_types = await response.json();
        }, (error) => {
            console.log(error);
        });
    },
}
</script>
