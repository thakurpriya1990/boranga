<template>
    <div id="internalConservationStatusDash" class="container">
        <ul id="pills-tab" class="nav nav-pills" role="tablist">
            <li class="nav-item">
                <a
                    id="pills-flora-tab"
                    class="nav-link"
                    data-bs-toggle="pill"
                    href="#pills-flora"
                    role="tab"
                    aria-controls="pills-flora"
                    aria-selected="true"
                    @click="set_active_tab('flora')"
                    >Flora</a
                >
            </li>
            <li class="nav-item">
                <a
                    id="pills-fauna-tab"
                    class="nav-link"
                    data-bs-toggle="pill"
                    href="#pills-fauna"
                    role="tab"
                    aria-controls="pills-fauna"
                    aria-selected="false"
                    @click="set_active_tab('fauna')"
                    >Fauna</a
                >
            </li>
            <li class="nav-item">
                <a
                    id="pills-community-tab"
                    class="nav-link"
                    data-bs-toggle="pill"
                    href="#pills-community"
                    role="tab"
                    aria-controls="pills-community"
                    aria-selected="false"
                    @click="set_active_tab('community')"
                    >Communities</a
                >
            </li>
        </ul>
        <div id="pills-tabContent" class="tab-content">
            <div
                id="pills-flora"
                class="tab-pane"
                role="tabpanel"
                aria-labelledby="pills-flora-tab"
            >
                <FormSection
                    v-if="showConservationStatusDatatables"
                    :form-collapse="false"
                    label="Conservation Status - Flora"
                    Index="flora"
                >
                    <ConservationStatusFloraDashTable
                        v-if="isFlora"
                        ref="flora_table"
                        level="internal"
                        :group_type_name="group_name"
                        :group_type_id="getGroupId"
                        :url="species_cs_url"
                        :profile="profile"
                    />
                </FormSection>
                <FormSection
                    :form-collapse="false"
                    label="Conservation Status - Flora Applications Referred To Me"
                    Index="flora_cs"
                >
                    <CSFloraReferralsDashTable
                        v-if="isFlora"
                        ref="flora_referral_table"
                        :group_type_name="group_name"
                        :group_type_id="getGroupId"
                        :url="species_cs_referrals_url"
                    />
                </FormSection>
            </div>
            <div
                id="pills-fauna"
                class="tab-pane"
                role="tabpanel"
                aria-labelledby="pills-fauna-tab"
            >
                <FormSection
                    v-if="showConservationStatusDatatables"
                    :form-collapse="false"
                    label="Conservation Status - Fauna"
                    Index="fauna"
                >
                    <ConservationStatusFaunaDashTable
                        v-if="isFauna"
                        ref="fauna_table"
                        level="internal"
                        :group_type_name="group_name"
                        :group_type_id="getGroupId"
                        :url="species_cs_url"
                        :profile="profile"
                    />
                </FormSection>
                <FormSection
                    :form-collapse="false"
                    label="Conservation Status - Fauna Applications Referred To Me"
                    Index="fauna_cs"
                >
                    <CSFaunaReferralsDashTable
                        v-if="isFauna"
                        ref="fauna_referral_table"
                        :group_type_name="group_name"
                        :group_type_id="getGroupId"
                        :url="species_cs_referrals_url"
                    />
                </FormSection>
            </div>
            <div
                id="pills-community"
                class="tab-pane"
                role="tabpanel"
                aria-labelledby="pills-community-tab"
            >
                <FormSection
                    v-if="showConservationStatusDatatables"
                    :form-collapse="false"
                    label="Conservation Status - Community"
                    Index="community"
                >
                    <ConservationStatusCommunityDashTable
                        v-if="isCommunity"
                        ref="community_table"
                        level="internal"
                        :group_type_name="group_name"
                        :group_type_id="getGroupId"
                        :url="community_cs_url"
                        :profile="profile"
                    />
                </FormSection>
                <FormSection
                    :form-collapse="false"
                    label="Conservation Status - Community Applications Referred To Me"
                    Index="community_cs"
                >
                    <CSCommunityReferralsDashTable
                        v-if="isCommunity"
                        ref="community_referral_table"
                        :group_type_name="group_name"
                        :group_type_id="getGroupId"
                        :url="community_cs_referrals_url"
                    />
                </FormSection>
            </div>
        </div>
    </div>
</template>
<script>
import ConservationStatusFloraDashTable from '@common-utils/conservation_status_flora_dashboard.vue';
import ConservationStatusFaunaDashTable from '@common-utils/conservation_status_fauna_dashboard.vue';
import ConservationStatusCommunityDashTable from '@common-utils/conservation_status_community_dashboard.vue';
import CSFloraReferralsDashTable from '@common-utils/cs_flora_referrals_dashboard.vue';
import CSFaunaReferralsDashTable from '@common-utils/cs_fauna_referrals_dashboard.vue';
import CSCommunityReferralsDashTable from '@common-utils/cs_community_referrals_dashboard.vue';
import FormSection from '@/components/forms/section_toggle.vue';
import { api_endpoints, constants } from '@/utils/hooks';

export default {
    name: 'InternalConservationStatusDashboard',
    components: {
        ConservationStatusFloraDashTable,
        ConservationStatusFaunaDashTable,
        ConservationStatusCommunityDashTable,
        CSFloraReferralsDashTable,
        CSFaunaReferralsDashTable,
        CSCommunityReferralsDashTable,
        FormSection,
    },
    data() {
        return {
            group_types: [],
            group_name: null,
            species_cs_url:
                api_endpoints.species_conservation_status_paginated_internal,
            species_cs_referrals_url:
                api_endpoints.species_conservation_status_referrals_paginated_internal,
            community_cs_url:
                api_endpoints.community_conservation_status_paginated_internal,
            community_cs_referrals_url:
                api_endpoints.community_conservation_status_referrals_paginated_internal,
            profile: null,
        };
    },
    computed: {
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
        },
        showConservationStatusDatatables: function () {
            return (
                this.profile &&
                this.profile.groups.some((i) =>
                    [
                        constants.GROUPS.READ_ONLY_USERS,
                        constants.GROUPS.CONSERVATION_STATUS_ASSESSORS,
                        constants.GROUPS.CONSERVATION_STATUS_APPROVERS,
                        constants.GROUPS.OCCURRENCE_APPROVERS,
                        constants.GROUPS.OCCURRENCE_ASSESSORS,
                        constants.GROUPS.SPECIES_AND_COMMUNITIES_APPROVERS,
                        constants.GROUPS.INTERNAL_CONTRIBUTORS,
                    ].includes(i)
                )
            );
        },
    },
    created: function () {
        fetch(api_endpoints.group_types_dict).then(
            async (response) => {
                this.group_types = await response.json();
            },
            (error) => {
                console.log(error);
            }
        );
        this.fetchProfile();
    },
    mounted: function () {
        chevron_toggle.init();
    },
    methods: {
        set_active_tab: function (group_name) {
            this.group_name = group_name;
            if (!this.profile || !this.profile.area_of_interest) {
                localStorage.setItem('conservationStatusActiveTab', group_name);
            }
            let elem = $('#pills-tab a[href="#pills-' + group_name + '"]');
            let tab = bootstrap.Tab.getInstance(elem);
            if (!tab) tab = new bootstrap.Tab(elem);
            tab.show();
        },
        fetchProfile: function () {
            let vm = this;
            fetch(api_endpoints.profile).then(
                async (response) => {
                    vm.profile = await response.json();
                    vm.$nextTick(() => {
                        if (vm.profile && vm.profile.area_of_interest) {
                            vm.set_active_tab(vm.profile.area_of_interest);
                            return;
                        }
                        let conservationStatusActiveTab = localStorage.getItem(
                            'conservationStatusActiveTab'
                        );
                        if (conservationStatusActiveTab === null) {
                            vm.set_active_tab('flora');
                        } else {
                            vm.set_active_tab(conservationStatusActiveTab);
                        }
                    });
                },
                (error) => {
                    console.log(error);
                }
            );
        },
    },
};
</script>
