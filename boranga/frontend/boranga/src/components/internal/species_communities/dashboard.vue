<template>
    <div class="container" id="internalDash">

        <ul class="nav nav-pills" id="pills-tab" role="tablist">
            <li class="nav-item" role="tab">
                <a
                    class="nav-link"
                    id="pills-flora-tab"
                    data-bs-toggle="pill"
                    href="#pills-flora"
                    aria-controls="pills-flora"
                    aria-selected="true"
                    @click="set_active_tab('pills-flora')"
                >Flora</a>
            </li>
            <li class="nav-item">
                <a
                    class="nav-link"
                    id="pills-fauna-tab"
                    data-bs-toggle="pill"
                    href="#pills-fauna"
                    aria-controls="pills-fauna"
                    aria-selected="false"
                    @click="set_active_tab('pills-fauna')"
                >Fauna</a>
            </li>
            <li class="nav-item">
                <a
                    class="nav-link"
                    id="pills-community-tab"
                    data-bs-toggle="pill"
                    href="#pills-community"
                    aria-controls="pills-community"
                    aria-selected="false"
                    @click="set_active_tab('pills-community')"
                >Communities</a>
            </li>


        </ul>

        <div class="tab-content" id="pills-tabContent">
            <div class="tab-pane fade show active" id="pills-flora" role="tabpanel" aria-labelledby="pills-flora-tab">
                <FormSection :formCollapse="false" label="Flora" Index="flora">
                    <SpeciesFloraDashTable level="internal" group_type_name="flora" :url="species_url" />
                </FormSection>
            </div>
            <div class="tab-pane fade" id="pills-fauna" role="tabpanel" aria-labelledby="pills-fauna-tab">
                <FormSection :formCollapse="false" label="Fauna" Index="fauna">
                    <SpeciesFaunaDashTable level="internal" group_type_name="fauna" :url="species_url"/>
                </FormSection>
            </div>
            <div class="tab-pane fade" id="pills-community" role="tabpanel" aria-labelledby="pills-community-tab">
                <FormSection :formCollapse="false" label="Community" Index="community">
                    <CommunitiesDashTable level="internal" group_type_name="community" :url="community_url"/>
                </FormSection>
            </div>
        </div>

    </div>
</template>
<script>
import datatable from '@/utils/vue/datatable.vue'
import SpeciesFloraDashTable from '@common-utils/species_flora_dashboard.vue'
import SpeciesFaunaDashTable from '@common-utils/species_fauna_dashboard.vue'
import CommunitiesDashTable from '@common-utils/communities_dashboard.vue'
import FormSection from '@/components/forms/section_toggle.vue'
import {
  api_endpoints,
  helpers
}
from '@/utils/hooks'
export default {
    name: 'InternalSpeciesCommunitiesDashboard',
    data() {
        let vm = this;
        return {
            user_preference:'flora',    // TODO : set it to default user preference but for now is hardcoded value
            filterGroupType: 'flora',  // TODO : need to set to default user preferance as cannot call click event of Tab onload
            group_types: [],
            species_url: api_endpoints.species_paginated_internal,
            community_url: api_endpoints.communities_paginated_internal,
        }
    
    },
    watch: {},
    components: {
        SpeciesFloraDashTable,
        SpeciesFaunaDashTable,
        CommunitiesDashTable,
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
            return this.filterGroupType == 'flora';
        },
        isFauna: function(){
            return this.filterGroupType == 'fauna';
        },
        isCommunity: function(){
            return this.filterGroupType == 'community';
        },
        /*---------------------------------------------------------------------*/
    },
    methods: {
        set_tabs: function(){
            let vm = this;
            /* set user preference tab by default on load of dashboard (Note: doesn't affect on the load group component)*/
            if(vm.user_preference === 'flora'){
                $('#pills-tab a[href="#pills-flora"]').tab('show');
            }
            if(vm.user_preference === 'fauna'){
                $('#pills-tab a[href="#pills-fauna"]').tab('show');
            }
            if(vm.user_preference === 'community'){
                $('#pills-tab a[href="#pills-community"]').tab('show');
            }
        },
        load_group_datatable: function(grouptype){
            /*----------to set the  filterGroupType to load the particular component only----------*/
            if(grouptype === 'flora'){
                this.filterGroupType = grouptype;
            }
            else if(grouptype === 'fauna'){
                this.filterGroupType = grouptype;
            }
            else if(grouptype === 'community'){
                this.filterGroupType = grouptype;
            }
        },
        set_active_tab: function(tab_href_name){
            let elem = $('#pills-tab a[href="#' + tab_href_name + '"]')
            let tab = bootstrap.Tab.getInstance(elem)
            if(!tab)
                tab = new bootstrap.Tab(elem)
            tab.show()
        },
        set_active_tab2: function(tab_href_name){
            var elem = document.querySelector('#pills-tab a[href="#' + tab_href_name + '"]')
            bootstrap.Tab.getInstance(elem).show() 
        },
    },
    created: function () {
        this.$http.get(api_endpoints.group_types_dict).then((response) => {
                this.group_types= response.body;
                },(error) => {
                console.log(error);
            });
    },
    updated: function () {
        //this.set_active_tab('pills-community');
        this.set_tabs();
    },
    mounted: function () {
        let vm = this

        this.$nextTick(function(){
            chevron_toggle.init();
            //vm.set_active_tab('pills-flora')
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

