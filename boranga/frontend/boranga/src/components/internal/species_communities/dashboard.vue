<template>
<div class="container" id="internalDash">
    <ul class="nav nav-pills mb-3" id="pills-tab" role="tablist">
        <li v-if="showFlora" class="nav-item">
            <a class="nav-link active" id="pills-flora-tab" data-toggle="pill" href="#pills-flora" role="tab" aria-controls="pills-flora" aria-selected="true">
              Flora
            </a>
        </li>
        <li v-if='showFauna' class="nav-item">
            <a class="nav-link" id="pills-fauna-tab" data-toggle="pill" href="#pills-fauna" role="tab" aria-controls="pills-fauna" aria-selected="false">
              Fauna
            </a>
        </li>
        <li v-if='showCommunity' class="nav-item">
            <a class="nav-link" id="pills-community-tab" data-toggle="pill" href="#pills-community" role="tab" aria-controls="pills-community" aria-selected="false">
            Communities
            </a>
        </li>
    </ul>
    <div class="tab-content" id="pills-tabContent">
        <div class="tab-pane fade" id="pills-flora" role="tabpanel" aria-labelledby="pills-flora-tab">
            <SpeciesFloraDashTable level="internal" :group_type_name="'flora'"/>
        </div>
        <div class="tab-pane fade" id="pills-fauna" role="tabpanel" aria-labelledby="pills-fauna-tab">
             <SpeciesFaunaDashTable level="internal" :group_type_name="'fauna'"/>
        </div>
        <div class="tab-pane fade" id="pills-community" role="tabpanel" aria-labelledby="pills-community-tab">
            <CommunitiesDashTable level="internal" :group_type_name="'community'"/>
        </div>
    </div>
    <!-- <FormSection v-bind:label="filterGroupType.toUpperCase()" >
        <div class="row">
            <div class="col-md-3">
                <div class="form-group">
                    <label for="">Group Type</label>
                    <select class="form-control" v-model="filterGroupType">
                        <option v-for="group in group_types" :value="group[0]" >{{group[1]}}</option>
                    </select>
                </div>
            </div>
        </div>
        <SpeciesFloraDashTable v-if='is_flora' level="internal" :group_type_name="filterGroupType"/>
        <SpeciesFaunaDashTable v-if='is_fauna' level="internal" :group_type_name="filterGroupType"/>
        <CommunitiesDashTable v-if='is_community' level="internal" :group_type_name="filterGroupType"/>
    </FormSection> -->
</div>
</template>
<script>
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
            filterGroupType: 'fauna', 
            group_types: [],
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
        showFlora: function(){
            return this.group_types.includes('flora');
        },
        showFauna: function(){
            return this.group_types.includes('fauna');
        },
        showCommunity: function(){
            return this.group_types.includes('community');
        },
    },
    methods: {
        set_tabs: function(){
            let vm = this;
            /* set user preference tab by default on load of dashboard */
            if(vm.user_preference === 'flora'){
                $('#pills-tab a[href="#pills-flora"]').tab('show');
            }
            if(vm.user_preference === 'fauna'){
                $('#pills-tab a[href="#pills-fauna"]').tab('show');
            }
            if(vm.user_preference === 'community'){
                $('#pills-tab a[href="#pills-community"]').tab('show');
            }
        }
    },
    created: function () {
        this.$http.get(api_endpoints.group_types_dict).then((response) => {
                this.group_types= response.body;
                },(error) => {
                console.log(error);
            });
    },
    updated: function () {
        this.set_tabs();
    }
}
</script>

<style type="text/css" scoped>
     .nav-item {
        background-color: rgb(200,200,200,0.8) !important;
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

</style>
