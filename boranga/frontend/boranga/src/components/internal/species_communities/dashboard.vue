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
                        :group_type_name="group_name" :group_type_id="getGroupId" :url="species_url" />
                </FormSection>
            </div>
            <div class="tab-pane" id="pills-fauna" role="tabpanel" aria-labelledby="pills-fauna-tab">
                <FormSection :formCollapse="false" label="Fauna" Index="fauna">
                    <SpeciesFaunaDashTable v-if="isFauna" ref="fauna_table" level="internal"
                        :group_type_name="group_name" :group_type_id="getGroupId" :url="species_url" />
                </FormSection>
            </div>
            <div class="tab-pane" id="pills-community" role="tabpanel" aria-labelledby="pills-community-tab">
                <FormSection :formCollapse="false" label="Community" Index="community">
                    <CommunitiesDashTable v-if="isCommunity" ref="community_table" level="internal"
                        :group_type_name="group_name" :group_type_id="getGroupId" :url="community_url" />
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
        let vm = this;
        return {
            user_preference: 'flora',    // TODO : set it to default user preference but for now is hardcoded value
            group_types: [],
            group_name: null,
            species_url: api_endpoints.species_paginated_internal,
            community_url: api_endpoints.communities_paginated_internal,
        }
    },
    components: {
        SpeciesFloraDashTable,
        SpeciesFaunaDashTable,
        CommunitiesDashTable,
        FormSection,
    },
    computed: {
        /*------properties to show the user authenticated Tabs only-----------*/
        showFloraTab: function () {
            return this.group_types.includes('flora');
        },
        showFaunaTab: function () {
            return this.group_types.includes('fauna');
        },
        showCommunityTab: function () {
            return this.group_types.includes('community');
        },
        /*---------------------------------------------------------------------*/
        /*---------properties to load group related vue components-------------*/
        isFlora: function () {
            return this.group_name == 'flora';
        },
        isFauna: function () {
            return this.group_name == 'fauna';
        },
        isCommunity: function () {
            return this.group_name == 'community';
        },
        /*---------------------------------------------------------------------*/
        getGroupId: function () {
            for (var i = 0; i < this.group_types.length; i++) {
                if (this.group_name === this.group_types[i].name) {
                    return this.group_types[i].id;
                }
            }
        }
    },
    methods: {
        set_tabs: function () {
            let vm = this;
            /* set user preference tab by default on load of dashboard (Note: doesn't affect on the load group component)*/
            if (vm.user_preference === 'flora') {
                $('#pills-tab a[href="#pills-flora"]').tab('show');
            }
            if (vm.user_preference === 'fauna') {
                $('#pills-tab a[href="#pills-fauna"]').tab('show');
            }
            if (vm.user_preference === 'community') {
                $('#pills-tab a[href="#pills-community"]').tab('show');
            }
        },
        set_active_tab: function (group_name) {
            this.group_name = group_name;
            localStorage.setItem('speciesCommunitiesActiveTab', group_name);
            let elem = $('#pills-tab a[href="#pills-' + group_name + '"]')
            let tab = bootstrap.Tab.getInstance(elem)
            if (!tab)
                tab = new bootstrap.Tab(elem)
            tab.show()
        },
    },
    created: function () {
        this.$http.get(api_endpoints.group_types_dict).then((response) => {
            this.group_types = response.body;
        }, (error) => {
            console.log(error);
        });
    },
    mounted: function () {
        let vm = this;
        this.$nextTick(function () {
            chevron_toggle.init();
            if (localStorage.getItem('speciesCommunitiesActiveTab') === null) {
                vm.set_active_tab(vm.user_preference);
            }
            else {
                vm.set_active_tab(localStorage.getItem('speciesCommunitiesActiveTab'));
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
