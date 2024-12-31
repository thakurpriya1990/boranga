<template>
    <div id="internalDash" class="container">
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
                <FormSection :form-collapse="false" label="Flora" Index="flora">
                    <SpeciesFloraDashTable
                        v-if="isFlora"
                        ref="flora_table"
                        level="internal"
                        :group_type_name="group_name"
                        :group_type_id="getGroupId"
                        :url="species_url"
                        :profile="profile"
                    />
                </FormSection>
            </div>
            <div
                id="pills-fauna"
                class="tab-pane"
                role="tabpanel"
                aria-labelledby="pills-fauna-tab"
            >
                <FormSection :form-collapse="false" label="Fauna" Index="fauna">
                    <SpeciesFaunaDashTable
                        v-if="isFauna"
                        ref="fauna_table"
                        level="internal"
                        :group_type_name="group_name"
                        :group_type_id="getGroupId"
                        :url="species_url"
                        :profile="profile"
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
                    :form-collapse="false"
                    label="Community"
                    Index="community"
                >
                    <CommunitiesDashTable
                        v-if="isCommunity"
                        ref="community_table"
                        level="internal"
                        :group_type_name="group_name"
                        :group_type_id="getGroupId"
                        :url="community_url"
                        :profile="profile"
                    />
                </FormSection>
            </div>
        </div>
    </div>
</template>
<script>
import SpeciesFloraDashTable from '@common-utils/species_flora_dashboard.vue';
import SpeciesFaunaDashTable from '@common-utils/species_fauna_dashboard.vue';
import CommunitiesDashTable from '@common-utils/communities_dashboard.vue';
import FormSection from '@/components/forms/section_toggle.vue';
import { api_endpoints } from '@/utils/hooks';
export default {
    name: 'InternalSpeciesCommunitiesDashboard',
    components: {
        SpeciesFloraDashTable,
        SpeciesFaunaDashTable,
        CommunitiesDashTable,
        FormSection,
    },
    data() {
        return {
            group_types: [],
            group_name: null,
            species_url: api_endpoints.species_paginated_internal,
            community_url: api_endpoints.communities_paginated_internal,
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
            return null;
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
        // eslint-disable-next-line no-undef
        chevron_toggle.init();
    },
    methods: {
        set_active_tab: function (group_name) {
            this.group_name = group_name;
            if (!this.profile || !this.profile.area_of_interest) {
                localStorage.setItem('speciesCommunitiesActiveTab', group_name);
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
                        let speciesCommunitiesActiveTab = localStorage.getItem(
                            'speciesCommunitiesActiveTab'
                        );
                        if (vm.profile && vm.profile.area_of_interest) {
                            vm.set_active_tab(vm.profile.area_of_interest);
                            return;
                        }
                        if (speciesCommunitiesActiveTab === null) {
                            vm.set_active_tab('flora');
                        } else {
                            vm.set_active_tab(speciesCommunitiesActiveTab);
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
