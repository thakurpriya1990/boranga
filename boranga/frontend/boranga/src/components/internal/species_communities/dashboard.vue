<template>
    <div class="container" id="internalDash">
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
                <FormSection :formCollapse="false" label="Flora" Index="flora">
                    <SpeciesFloraDashTable v-if="isFlora" ref="flora_table" level="internal"
                        :group_type_name="group_name" :group_type_id="getGroupId" :url="species_url" :profile="profile" />
                </FormSection>
            </div>
            <div class="tab-pane" id="pills-fauna" role="tabpanel" aria-labelledby="pills-fauna-tab">
                <FormSection :formCollapse="false" label="Fauna" Index="fauna">
                    <SpeciesFaunaDashTable v-if="isFauna" ref="fauna_table" level="internal"
                        :group_type_name="group_name" :group_type_id="getGroupId" :url="species_url" :profile="profile" />
                </FormSection>
            </div>
            <div class="tab-pane" id="pills-community" role="tabpanel" aria-labelledby="pills-community-tab">
                <FormSection :formCollapse="false" label="Community" Index="community">
                    <CommunitiesDashTable v-if="isCommunity" ref="community_table" level="internal"
                        :group_type_name="group_name" :group_type_id="getGroupId" :url="community_url" :profile="profile" />
                </FormSection>
            </div>
        </div>
    </div>
</template>
<script>
import SpeciesFloraDashTable from '@common-utils/species_flora_dashboard.vue'
import SpeciesFaunaDashTable from '@common-utils/species_fauna_dashboard.vue'
import CommunitiesDashTable from '@common-utils/communities_dashboard.vue'
import FormSection from '@/components/forms/section_toggle.vue'
import {
    api_endpoints,
}
    from '@/utils/hooks'
export default {
    name: 'InternalSpeciesCommunitiesDashboard',
    data() {
        return {
            group_types: [],
            group_name: null,
            species_url: api_endpoints.species_paginated_internal,
            community_url: api_endpoints.communities_paginated_internal,
            profile: null,
        }
    },
    components: {
        SpeciesFloraDashTable,
        SpeciesFaunaDashTable,
        CommunitiesDashTable,
        FormSection,
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
        }
    },
    methods: {
        set_active_tab: function (group_name) {
            this.group_name = group_name;
            if(!this.profile || !this.profile.area_of_interest){
                localStorage.setItem('speciesCommunitiesActiveTab', group_name);
            }
            let elem = $('#pills-tab a[href="#pills-' + group_name + '"]')
            let tab = bootstrap.Tab.getInstance(elem)
            if (!tab)
                tab = new bootstrap.Tab(elem)
            tab.show()
        },
        fetchProfile: function () {
            let vm = this;
            fetch(api_endpoints.profile).then(async (response) => {

                vm.profile = await response.json();
                vm.$nextTick(() => {
                    let speciesCommunitiesActiveTab = localStorage.getItem('speciesCommunitiesActiveTab')
                    if (vm.profile && vm.profile.area_of_interest) {
                        vm.set_active_tab(vm.profile.area_of_interest);
                        return;
                    }
                    if(speciesCommunitiesActiveTab === null) {
                        vm.set_active_tab('flora');
                    } else {
                        vm.set_active_tab(speciesCommunitiesActiveTab);
                    }
                })
            }, (error) => {
                console.log(error);
            });
        }
    },
    created: function () {
        fetch(api_endpoints.group_types_dict).then(async (response) => {
            this.group_types = await response.json();
        }, (error) => {
            console.log(error);
        });
        this.fetchProfile();
    },
    mounted: function () {
        chevron_toggle.init();
    },
}
</script>
