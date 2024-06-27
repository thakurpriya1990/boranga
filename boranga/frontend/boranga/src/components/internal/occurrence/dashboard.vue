<template>
    <div class="container" id="internal-occurrence-dash">
        <ul class="nav nav-pills" id="pills-tab" role="tablist">
            <li class="nav-item">
                <a class="nav-link" id="pills-flora-tab" data-bs-toggle="pill" href="#pills-flora" role="tab"
                    aria-controls="pills-flora" aria-selected="true" @click="set_active_tab('flora')">Flora</a>
            </li>
            <li class="nav-item">
                <a class="nav-link" id="pills-fauna-tab" data-bs-toggle="pill" href="#pills-fauna" role="tab"
                    aria-controls="pills-fauna" aria-selected="false" @click="set_active_tab('fauna')">Fauna</a>
            </li>
            <li class="nav-item">
                <a class="nav-link" id="pills-community-tab" data-bs-toggle="pill" href="#pills-community" role="tab"
                    aria-controls="pills-community" aria-selected="false"
                    @click="set_active_tab('community')">Communities</a>
            </li>
        </ul>

        <div class="tab-content" id="pills-tabContent">
            <div class="tab-pane" id="pills-flora" role="tabpanel" aria-labelledby="pills-flora-tab">
                <FormSection v-if="show_occurrences" :formCollapse="false" label="Occurrences - Flora"
                    Index="occurrence-flora">
                    <OccurrenceFloraDashboard v-if="isFlora" ref="occ_flora_table" level="internal"
                        :group_type_name="group_name" :group_type_id="getGroupId" :url="species_occ_url"
                        :profile="profile" />
                </FormSection>
                <FormSection v-if="show_occurrence_reports" :formCollapse="false" label="Occurrence Report - Flora"
                    Index="occurrence-report-flora">
                    <OccurrenceReportFloraDashTable v-if="isFlora" ref="flora_table" level="internal"
                        :group_type_name="group_name" :group_type_id="getGroupId" :url="species_ocr_url"
                        :profile="profile" />
                </FormSection>
                <FormSection :formCollapse="false" label="Occurrence Report - Flora Referred to Me"
                    Index="occurrence-report-flora-referred-to-me">
                    <OccurrenceReportReferredToMeDashTable v-if="isFlora" ref="flora_referrals_table" level="internal"
                        :group_type_name="group_name" :group_type_id="getGroupId" :url="species_ocr_referrals_url"
                        :profile="profile" filterOCRReferralsOccurrence_cache="filterOCRFloraReferralsOccurrence"
                        filterOCRReferralsScientificName_cache="filterOCRFloraReferralsScientificName"
                        filterOCRReferralsName_cache="filterOCRFloraReferralsName"
                        filterOCRReferralsStatus_cache="filterOCRFloraReferralsStatus" />
                </FormSection>
            </div>
            <div class="tab-pane" id="pills-fauna" role="tabpanel" aria-labelledby="pills-fauna-tab">
                <FormSection v-if="show_occurrences" :formCollapse="false" label="Occurrences - Fauna"
                    Index="occurrence-fauna">
                    <OccurrenceFaunaDashboard v-if="isFauna" ref="occ_fauna_table" level="internal"
                        :group_type_name="group_name" :group_type_id="getGroupId" :url="species_occ_url"
                        :profile="profile" />
                </FormSection>
                <FormSection v-if="show_occurrence_reports" :formCollapse="false" label="Occurrence Report - Fauna"
                    Index="fauna">
                    <OccurrenceReportFaunaDashTable v-if="isFauna" ref="fauna_table" level="internal"
                        :group_type_name="group_name" :group_type_id="getGroupId" :url="species_ocr_url"
                        :profile="profile" />
                </FormSection>
                <FormSection :formCollapse="false" label="Occurrence Report - Fauna Referred to Me"
                    Index="occurrence-report-fauna-referred-to-me">
                    <OccurrenceReportReferredToMeDashTable v-if="isFauna" ref="fauna_referrals_table" level="internal"
                        :group_type_name="group_name" :group_type_id="getGroupId" :url="species_ocr_referrals_url"
                        :profile="profile" filterOCRReferralsOccurrence_cache="filterOCRCommunityReferralsOccurrence"
                        filterOCRReferralsScientificName_cache="filterOCRCommunityReferralsScientificName"
                        filterOCRReferralsName_cache="filterOCRCommunityReferralsName"
                        filterOCRReferralsStatus_cache="filterOCRCommunityReferralsStatus" />
                </FormSection>
            </div>
            <div class="tab-pane" id="pills-community" role="tabpanel" aria-labelledby="pills-community-tab">
                <FormSection v-if="show_occurrences" :formCollapse="false" label="Occurrences - Community"
                    Index="occurrence-community">
                    <OccurrenceCommunityDashboard v-if="isCommunity" ref="occ_community_table" level="internal"
                        :group_type_name="group_name" :group_type_id="getGroupId" :url="community_occ_url"
                        :profile="profile" />
                </FormSection>
                <FormSection v-if="show_occurrence_reports" :formCollapse="false" label="Occurrence Report - Community"
                    Index="community">
                    <OccurrenceReportCommunityDashTable v-if="isCommunity" ref="community_table" level="internal"
                        :group_type_name="group_name" :group_type_id="getGroupId" :url="community_ocr_url"
                        :profile="profile" />
                </FormSection>
                <FormSection :formCollapse="false" label="Occurrence Report - Community Referred to Me"
                    Index="occurrence-report-community-referred-to-me">
                    <OccurrenceReportReferredToMeDashTable v-if="isCommunity" ref="community_referrals_table"
                        level="internal" :group_type_name="group_name" :group_type_id="getGroupId"
                        :url="species_ocr_referrals_url" :profile="profile"
                        filterOCRReferralsOccurrence_cache="filterOCRFaunaReferralsOccurrence"
                        filterOCRReferralsScientificName_cache="filterOCRFaunaReferralsScientificName"
                        filterOCRReferralsName_cache="filterOCRFaunaReferralsName"
                        filterOCRReferralsStatus_cache="filterOCRFaunaReferralsStatus" />
                </FormSection>
            </div>
        </div>

    </div>
</template>
<script>

import OccurrenceFloraDashboard from '@/components/common/occurrence_flora_dashboard.vue'
import OccurrenceFaunaDashboard from '@/components/common/occurrence_fauna_dashboard.vue'
import OccurrenceCommunityDashboard from '@/components/common/occurrence_community_dashboard.vue'

import OccurrenceReportFloraDashTable from '@/components/common/occurrence_report_flora_dashboard.vue'
import OccurrenceReportFaunaDashTable from '@common-utils/occurrence_report_fauna_dashboard.vue'
import OccurrenceReportCommunityDashTable from '@common-utils/occurrence_report_community_dashboard.vue'

import OccurrenceReportReferredToMeDashTable from '@common-utils/ocr_referrals_dashboard.vue'

import FormSection from '@/components/forms/section_toggle.vue'

import {
    api_endpoints,
    constants
}
    from '@/utils/hooks'
export default {
    name: 'InternalOccurrenceDashboard',
    data() {
        return {
            user_preference: 'flora',    // TODO : set it to default user preference but for now is hardcoded value
            group_types: [],
            group_name: null,
            species_occ_url: api_endpoints.occurrence_paginated_internal,
            community_occ_url: api_endpoints.occurrence_paginated_internal,
            species_ocr_url: api_endpoints.occurrence_report_paginated_internal,
            community_ocr_url: api_endpoints.occurrence_report_paginated_internal,
            species_ocr_referrals_url: api_endpoints.occurrence_report_paginated_referred_to_me,
            profile: null,
        }
    },
    components: {
        OccurrenceFloraDashboard,
        OccurrenceFaunaDashboard,
        OccurrenceCommunityDashboard,
        OccurrenceReportFloraDashTable,
        OccurrenceReportFaunaDashTable,
        OccurrenceReportCommunityDashTable,
        OccurrenceReportReferredToMeDashTable,
        FormSection,
    },
    computed: {
        show_occurrences: function () {
            return this.profile && this.profile.groups.some(i => [
                constants.GROUPS.READ_ONLY_USERS,
                constants.GROUPS.CONSERVATION_STATUS_ASSESSORS,
                constants.GROUPS.CONSERVATION_STATUS_APPROVERS,
                constants.GROUPS.OCCURRENCE_APPROVERS,
                constants.GROUPS.OCCURRENCE_ASSESSORS,
                constants.GROUPS.SPECIES_AND_COMMUNITIES_APPROVERS,
            ].includes(i));
        },
        show_occurrence_reports: function () {
            return this.profile && this.profile.groups.some(i => [
                constants.GROUPS.READ_ONLY_USERS,
                constants.GROUPS.CONSERVATION_STATUS_ASSESSORS,
                constants.GROUPS.CONSERVATION_STATUS_APPROVERS,
                constants.GROUPS.OCCURRENCE_APPROVERS,
                constants.GROUPS.OCCURRENCE_ASSESSORS,
                constants.GROUPS.SPECIES_AND_COMMUNITIES_APPROVERS,
                constants.GROUPS.INTERNAL_CONTRIBUTORS
            ].includes(i));
        },
        showFloraTab: function () {
            return this.group_types.includes('flora');
        },
        showFaunaTab: function () {
            return this.group_types.includes('fauna');
        },
        showCommunityTab: function () {
            return this.group_types.includes('community');
        },
        isFlora: function () {
            return this.group_name == 'flora';
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
        set_active_tab: function (group_name) {
            this.group_name = group_name;
            localStorage.setItem("occurrenceActiveTab", group_name);
            let elem = $('#pills-tab a[href="#pills-' + group_name + '"]')
            let tab = bootstrap.Tab.getInstance(elem)
            if (!tab)
                tab = new bootstrap.Tab(elem)
            tab.show()
        },
        fetchProfile: function () {
            this.$http.get(api_endpoints.profile).then((response) => {
                this.profile = response.body;
            }, (error) => {
                console.log(error);
            });
        }
    },
    created: function () {
        this.$http.get(api_endpoints.group_types_dict).then((response) => {
            this.group_types = response.body;
        }, (error) => {
            console.log(error);
        });
        this.fetchProfile();
    },
    mounted: function () {
        let vm = this;
        this.$nextTick(function () {
            chevron_toggle.init();
            if (localStorage.getItem('occurrenceActiveTab') === null) {
                vm.set_active_tab(vm.user_preference);
            }
            else {
                vm.set_active_tab(localStorage.getItem('occurrenceActiveTab'));
            }
            this.getGroupId;
        })
    },
}
</script>

<style lang="css" scoped>
.section {
    text-transform: capitalize;
}

.list-group {
    margin-bottom: 0;
}

.fixed-top {
    position: fixed;
    top: 56px;
}

.nav-item {
    margin-bottom: 2px;
}

.nav-item>li>a {
    background-color: yellow !important;
    color: #fff;
}

.nav-item>li.active>a,
.nav-item>li.active>a:hover,
.nav-item>li.active>a:focus {
    color: white;
    background-color: blue;
    border: 1px solid #888888;
}

.admin>div {
    display: inline-block;
    vertical-align: top;
    margin-right: 1em;
}

.nav-pills .nav-link {
    border-bottom-left-radius: 0;
    border-bottom-right-radius: 0;
    border-top-left-radius: 0.5em;
    border-top-right-radius: 0.5em;
    margin-right: 0.25em;
}

.nav-pills .nav-link {
    background: lightgray;
}

.nav-pills .nav-link.active {
    background: gray;
}
</style>
