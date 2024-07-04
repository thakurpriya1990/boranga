<template lang="html">
    <div v-if="species_community" class="container" id="externalSpeciesCommunity">
        <div class="row" style="padding-bottom: 50px;">
            <h3>{{ display_group_type }} {{ display_number }} - {{ display_name }}</h3>
            <h4 v-if="species_community.conservation_status">{{ species_community.conservation_status.conservation_category }}</h4>
            <div class="col-md-3">
                <template>
                    <div class="">
                        <div class="card card-default mb-3">
                            <div class="card-header">
                                Image
                            </div>
                            <div class="card-body card-collapse">
                                <div class="row">
                                    <div class="col-sm-12">
                                        <div class="site-logo row">
                                            <template v-if="uploadedID">
                                                <img :src="`/api/external_species/${species_community.id}/public_image/`" class="img-responsive" :alt="display_name" />
                                            </template>
                                            <template v-else>
                                                <span class="text-muted">No Image Available</span>
                                            </template>
                                        </div>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>
                </template>
            </div>
            <div class="col-md-9">
                <div class="row">
                    <template>
                        <div class="">
                            <div class="row">
                                <form>
                                    <ProposalSpeciesCommunities ref="species_communities"
                                        :species_community="species_community" :species_community_original="species_community" id="speciesCommunityStart"
                                        :is_internal="false" :is_readonly="true">
                                    </ProposalSpeciesCommunities>
                                </form>
                            </div>
                        </div>
                    </template>
                </div>
            </div>
        </div>
    </div>
</template>
<script>
import Vue from 'vue'
import datatable from '@vue-utils/datatable.vue'

import ProposalSpeciesCommunities from '@/components/form_species_communities.vue'

import {
    api_endpoints,
    helpers
}
    from '@/utils/hooks'
export default {
    name: 'ExternalSpeciesCommunity',
    data: function () {
        let vm = this;
        return {
            "species_community": null,
            uploadedID: null,
        }
    },
    components: {
        datatable,
        ProposalSpeciesCommunities,
    },
    computed: {
        isCommunity: function () {
            return this.species_community.group_type === "community"
        },
        display_group_type: function () {
            let group_type_string = this.species_community.group_type
            // to Capitalize only first character
            return group_type_string.charAt(0).toUpperCase() + group_type_string.slice(1);
        },
        display_number: function () {
            return (this.species_community.group_type === "community") ?
                this.species_community.community_number :
                this.species_community.species_number;
        },
        display_name: function () {
            return (this.species_community.group_type === "community") ?
                (this.species_community.taxonomy_details != null) ? this.species_community.taxonomy_details.community_migrated_id : '' :
                (this.species_community.taxonomy_details != null) ? this.species_community.taxonomy_details.scientific_name + " (" + this.species_community.taxonomy_details.taxon_name_id + ")" : '';
        },
    },
    mounted: function () {
        let vm = this;
    },
    beforeRouteEnter: function (to, from, next) {
        //-------------get species object if received species id
        if (to.query.group_type_name === 'flora' || to.query.group_type_name === "fauna") {
            Vue.http.get(`/api/external_species/${to.params.species_community_id}/`).then(res => {
                next(vm => {
                    vm.species_community = res.body; //--temp species_obj
                    vm.uploadedID = vm.species_community.image_doc;
                });
            },
                err => {
                    console.log(err);
                });
        }
        //------get community object if received community id
        else {
            Vue.http.get(`/api/external_community/${to.params.species_community_id}/`).then(res => {
                next(vm => {
                    vm.species_community = res.body; //--temp community_obj
                    vm.uploadedID = vm.species_community.image_doc;
                });
            },
                err => {
                    console.log(err);
                });
        }
    },
}
</script>
<style scoped>
.top-buffer-s {
    margin-top: 10px;
}

.actionBtn {
    cursor: pointer;
}

.hidePopover {
    display: none;
}

.separator {
    border: 1px solid;
    margin-top: 15px;
    margin-bottom: 10px;
    width: 100%;
}
</style>
