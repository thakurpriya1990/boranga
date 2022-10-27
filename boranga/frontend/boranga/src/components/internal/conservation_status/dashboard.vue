<template>
    <div class="container" id="internalConservationStatusDash">

        <ul class="nav nav-pills" id="pills-tab" role="tablist">
            <li class="nav-item">
                <a
                    class="nav-link"
                    id="pills-flora-tab"
                    data-bs-toggle="pill"
                    href="#pills-flora"
                    role="tab"
                    aria-controls="pills-flora"
                    aria-selected="true"
                    @click="set_active_tab('pills-flora','flora')"
                >Flora</a>
            </li>
            <li class="nav-item">
                <a
                    class="nav-link"
                    id="pills-fauna-tab"
                    data-bs-toggle="pill"
                    href="#pills-fauna"
                    role="tab"
                    aria-controls="pills-fauna"
                    aria-selected="false"
                    @click="set_active_tab('pills-fauna','fauna')"
                >Fauna</a>
            </li>
            <li class="nav-item">
                <a
                    class="nav-link"
                    id="pills-community-tab"
                    data-bs-toggle="pill"
                    href="#pills-community"
                    role="tab"
                    aria-controls="pills-community"
                    aria-selected="false"
                    @click="set_active_tab('pills-community','community')"
                >Communities</a>
            </li>
        </ul>

        <div class="tab-content" id="pills-tabContent">
            <div class="tab-pane" id="pills-flora" role="tabpanel" aria-labelledby="pills-flora-tab">
                <FormSection :formCollapse="false" label="Conservation Status - Flora" Index="flora">
                    <ConservationStatusFloraDashTable v-if="isFlora" ref="flora_table" level="internal"
                    :group_type_name="group_name"
                    :group_type_id="getGroupId"
                    :url="species_cs_url" />
                </FormSection>
                <FormSection :formCollapse="false" label="Conservation Status - Flora Applications Referred To Me" Index="flora_cs">
                    <CSFloraReferralsDashTable v-if="isFlora" ref="flora_referral_table"
                    :group_type_name="group_name"
                    :group_type_id="getGroupId"
                    :url="species_cs_referrals_url" />
                </FormSection>
            </div>
            <div class="tab-pane" id="pills-fauna" role="tabpanel" aria-labelledby="pills-fauna-tab">
                <FormSection :formCollapse="false" label="Conservation Status - Fauna" Index="fauna">
                    <ConservationStatusFaunaDashTable v-if="isFauna" ref="fauna_table" level="internal"
                    :group_type_name="group_name"
                    :group_type_id="getGroupId"
                    :url="species_cs_url"/>
                </FormSection>
                <FormSection :formCollapse="false" label="Conservation Status - Fauna Applications Referred To Me" Index="fauna_cs">
                    <CSFaunaReferralsDashTable v-if="isFauna" ref="fauna_referral_table"
                    :group_type_name="group_name"
                    :group_type_id="getGroupId"
                    :url="species_cs_referrals_url" />
                </FormSection>
            </div>
            <div class="tab-pane" id="pills-community" role="tabpanel" aria-labelledby="pills-community-tab">
                <FormSection :formCollapse="false" label="Conservation Status - Community" Index="community">
                    <ConservationStatusCommunityDashTable v-if="isCommunity" ref="community_table" level="internal"
                    :group_type_name="group_name"
                    :group_type_id="getGroupId"
                    :url="community_cs_url"/>
                </FormSection>
                <FormSection :formCollapse="false" label="Conservation Status - Community Applications Referred To Me" Index="community_cs">
                    <CSCommunityReferralsDashTable v-if="isCommunity" ref="community_referral_table"
                    :group_type_name="group_name"
                    :group_type_id="getGroupId"
                    :url="community_cs_referrals_url" />
                </FormSection>
            </div>
        </div>

    </div>
</template>
<script>
import datatable from '@/utils/vue/datatable.vue'
import ConservationStatusFloraDashTable from '@common-utils/conservation_status_flora_dashboard.vue'
import ConservationStatusFaunaDashTable from '@common-utils/conservation_status_fauna_dashboard.vue'
import ConservationStatusCommunityDashTable from '@common-utils/conservation_status_community_dashboard.vue'
import CSFloraReferralsDashTable from '@common-utils/cs_flora_referrals_dashboard.vue'
import CSFaunaReferralsDashTable from '@common-utils/cs_fauna_referrals_dashboard.vue'
import CSCommunityReferralsDashTable from '@common-utils/cs_community_referrals_dashboard.vue'
import FormSection from '@/components/forms/section_toggle.vue'
import {
  api_endpoints,
  helpers
}
from '@/utils/hooks'
export default {
    name: 'InternalConservationStatusDashboard',
    data() {
        let vm = this;
        return {
            user_preference:'flora',    // TODO : set it to default user preference but for now is hardcoded value
            group_types: [],
            group_name: null,
            species_cs_url: api_endpoints.species_conservation_status_paginated_internal,
            species_cs_referrals_url: api_endpoints.species_conservation_status_referrals_paginated_internal,
            community_cs_url: api_endpoints.community_conservation_status_paginated_internal,
            community_cs_referrals_url: api_endpoints.community_conservation_status_referrals_paginated_internal,
        }
    },
    watch: {},
    components: {
        ConservationStatusFloraDashTable,
        ConservationStatusFaunaDashTable,
        ConservationStatusCommunityDashTable,
        CSFloraReferralsDashTable,
        CSFaunaReferralsDashTable,
        CSCommunityReferralsDashTable,
        FormSection,
    },
    computed: {
        /*------properties to show the user authenticated Tabs only-----------*/
        showFloraTab: function(){
            return this.group_types.includes('flora');
        },
        showFaunaTab: function(){
            return this.group_types.includes('fauna');
        },
        showCommunityTab: function(){
            return this.group_types.includes('community');
        },
        /*---------------------------------------------------------------------*/
        /*---------properties to load group related vue components-------------*/
        isFlora: function(){
            return this.group_name == 'flora';
        },
        isFauna: function(){
            return this.group_name == 'fauna';
        },
        isCommunity: function(){
            return this.group_name == 'community';
        },
        /*---------------------------------------------------------------------*/
        getGroupId: function(){
            for(var i=0; i<this.group_types.length; i++){
                if(this.group_name === this.group_types[i].name){
                    return this.group_types[i].id;
                }
            }
        }

    },
    methods: {
        /*load_group_datatable: function(grouptype){
            if(grouptype === 'flora'){
                this.filterGroupType = grouptype;
            }
            else if(grouptype === 'fauna'){
                this.filterGroupType = grouptype;
            }
            else if(grouptype === 'community'){
                this.filterGroupType = grouptype;
            }
        },*/
        set_active_tab: function(tab_href_name, group_name){
            this.group_name=group_name;
            let elem = $('#pills-tab a[href="#' + tab_href_name + '"]')
            let tab = bootstrap.Tab.getInstance(elem)
            if(!tab)
                tab = new bootstrap.Tab(elem)
            tab.show()
        },
    },
    created: function () {
        this.$http.get(api_endpoints.group_types_dict).then((response) => {
                this.group_types= response.body;
                },(error) => {
                console.log(error);
            });
    },
    mounted: function () {
        let vm = this;
        this.$nextTick(function(){
            chevron_toggle.init();
            vm.set_active_tab('pills-'+vm.user_preference, vm.user_preference);
            this.getGroupId;
        })
    },

}
</script>

<style lang="css" scoped>
    .section{
        text-transform: capitalize;
    }
    .list-group{
        margin-bottom: 0;
    }
    .fixed-top{
        position: fixed;
        top:56px;
    }

    .nav-item {
        margin-bottom: 2px;
    }

    .nav-item>li>a {
        background-color: yellow !important;
        color: #fff;
    }

    .nav-item>li.active>a, .nav-item>li.active>a:hover, .nav-item>li.active>a:focus {
      color: white;
      background-color: blue;
      border: 1px solid #888888;
    }

    .admin > div {
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
