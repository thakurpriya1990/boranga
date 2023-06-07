<template>
    <div class="container" id="internalMeetDash">

        <ul class="nav nav-pills" id="pills-tab" role="tablist">
            <li class="nav-item">
                <a
                    class="nav-link"
                    id="pills-meeting-tab"
                    data-bs-toggle="pill"
                    href="#pills-meeting"
                    role="tab"
                    aria-controls="pills-meeting"
                    aria-selected="true"
                    @click="set_active_tab('pills-meeting','meeting')"
                >Meeting</a>
            </li>
            <li class="nav-item">
                <a
                    class="nav-link"
                    id="pills-committee-tab"
                    data-bs-toggle="pill"
                    href="#pills-committee"
                    role="tab"
                    aria-controls="pills-committee"
                    aria-selected="false"
                    @click="set_active_tab('pills-committee','committee')"
                >Committee Meeting</a>
            </li>
            
        </ul>

        <div class="tab-content" id="pills-tabContent">
            <div class="tab-pane" id="pills-meeting" role="tabpanel" aria-labelledby="pills-meeting-tab">
                <FormSection :formCollapse="false" label="Meeting" Index="meeting">
                    <MeetingsDashTable ref="meetings_table" level="internal"  :url="meetings_url" />
                </FormSection>
            </div>
            <div class="tab-pane" id="pills-committee" role="tabpanel" aria-labelledby="pills-committee-tab">
                <FormSection :formCollapse="false" label="Committee Meeting" Index="committee">
                </FormSection>
            </div>
        </div>
        
    </div>
</template>
<script>
import datatable from '@/utils/vue/datatable.vue'
import FormSection from '@/components/forms/section_toggle.vue'
import MeetingsDashTable from './meetings_datatable.vue'
import {
  api_endpoints,
  helpers
}
from '@/utils/hooks'
export default {
    name: 'InternalMeetingsDashboard',
    data() {
        let vm = this;
        return {
            user_preference:'meeting',    // TODO : set it to default user preference but for now is hardcoded value
            //filterGroupType: 'flora',  // TODO : need to set to default user preferance as cannot call click event of Tab onload
            group_name: null,
            meetings_url: api_endpoints.meetings_paginated,
            
        }
    
    },
    watch: {},
    components: {
        MeetingsDashTable,
        FormSection,
    },
    computed: {
    },
    methods: {
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
    },
    mounted: function () {
        let vm = this;
        this.$nextTick(function(){
            chevron_toggle.init();
            vm.set_active_tab('pills-'+vm.user_preference, vm.user_preference);
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
