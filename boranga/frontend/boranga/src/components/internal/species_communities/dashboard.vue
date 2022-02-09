<template>
<div class="container" id="internalDash">
    <FormSection v-bind:label="filterGroupType.toUpperCase()" >
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
    </FormSection>
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
            user_preference:'flora',
            filterGroupType: 'fauna', // TODO : set it to default user preference but for now is hardcoded value
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
        is_flora: function(){
            return this.filterGroupType == 'flora';
        },
        is_fauna: function(){
            return this.filterGroupType == 'fauna';
        },
        is_community: function(){
            return this.filterGroupType == 'community';
        },
    },
    methods: {},
    created: function () {
        this.$http.get(api_endpoints.group_types_dict).then((response) => {
                this.group_types= response.body;
                },(error) => {
                console.log(error);
            });
    }
}
</script>
