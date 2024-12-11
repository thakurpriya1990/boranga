<template lang="html">
    <div>
        <div class="col-md-12">
            <ul
                v-if="is_internal || is_public"
                id="pills-tab"
                class="nav nav-pills"
                role="tablist"
            >
                <li class="nav-item">
                    <a
                        id="pills-profile-tab"
                        class="nav-link active"
                        data-bs-toggle="pill"
                        :href="'#' + profileBody"
                        role="tab"
                        :aria-controls="profileBody"
                        aria-selected="true"
                    >
                        Profile
                    </a>
                </li>
                <li v-if="is_internal" class="nav-item">
                    <a
                        id="pills-documents-tab"
                        class="nav-link"
                        data-bs-toggle="pill"
                        :href="'#' + documentBody"
                        role="tab"
                        aria-controls="pills-documents"
                        :aria-selected="documentBody"
                        @click="tabClicked()"
                    >
                        Documents
                    </a>
                </li>
                <li v-if="is_internal || threats_public" class="nav-item">
                    <a
                        id="pills-threats-tab"
                        class="nav-link"
                        data-bs-toggle="pill"
                        :href="'#' + threatBody"
                        role="tab"
                        :aria-controls="threatBody"
                        aria-selected="false"
                        @click="tabClicked()"
                    >
                        Threats
                    </a>
                </li>
                <li v-if="is_internal" class="nav-item">
                    <a
                        id="pills-related-items-tab"
                        class="nav-link"
                        data-bs-toggle="pill"
                        :href="'#' + relatedItemBody"
                        role="tab"
                        :aria-controls="relatedItemBody"
                        aria-selected="false"
                        @click="tabClicked()"
                    >
                        Related Items
                    </a>
                </li>
            </ul>
            <div id="pills-tabContent" class="tab-content">
                <div
                    v-if="is_internal || is_public"
                    :id="profileBody"
                    class="tab-pane fade show active"
                    role="tabpanel"
                    aria-labelledby="pills-profile-tab"
                >
                    <Community
                        v-if="isCommunity"
                        id="communityInformation"
                        ref="community_information"
                        :is_internal="is_internal"
                        :species_community="species_community"
                        :species_community_original="species_community_original"
                        :is_readonly="is_readonly"
                    >
                    </Community>
                    <Species
                        v-else
                        id="speciesInformation"
                        ref="species_information"
                        :is_internal="is_internal"
                        :species_community="species_community"
                        :species_community_original="species_community_original"
                        :is_readonly="is_readonly"
                        :rename_species="rename_species"
                    >
                    </Species>
                </div>
                <div
                    v-if="is_internal"
                    :id="documentBody"
                    class="tab-pane fade"
                    role="tabpanel"
                    aria-labelledby="pills-documents-tab"
                >
                    <CommunityDocuments
                        v-if="isCommunity"
                        id="communityDocuments"
                        :key="reloadcount"
                        ref="community_documents"
                        :is_internal="is_internal"
                        :species_community="species_community"
                        :is_readonly="is_readonly"
                    >
                    </CommunityDocuments>
                    <SpeciesDocuments
                        v-else
                        id="speciesDocuments"
                        :key="`${reloadcount}-else`"
                        ref="species_documents"
                        :is_internal="is_internal"
                        :species_community="species_community"
                        :is_readonly="is_readonly"
                    >
                    </SpeciesDocuments>
                </div>
                <div
                    v-if="is_internal || threats_public"
                    :id="threatBody"
                    class="tab-pane fade"
                    role="tabpanel"
                    aria-labelledby="pills-threats-tab"
                >
                    <CommunityThreats
                        v-if="isCommunity"
                        id="communityThreats"
                        :key="reloadcount"
                        ref="community_threats"
                        :is_internal="is_internal"
                        :species_community="species_community"
                        :is_readonly="is_readonly"
                    >
                    </CommunityThreats>
                    <SpeciesThreats
                        v-else
                        id="speciesThreats"
                        :key="`${reloadcount}-else`"
                        ref="species_threats"
                        :is_internal="is_internal"
                        :species_community="species_community"
                        :is_readonly="is_readonly"
                    >
                    </SpeciesThreats>
                </div>
                <div
                    v-if="is_internal"
                    :id="relatedItemBody"
                    class="tab-pane fade"
                    role="tabpanel"
                    aria-labelledby="pills-related-items-tab"
                >
                    <RelatedItems
                        id="speciesCommunitiesRelatedItems"
                        :key="reloadcount"
                        ref="species_communities_related_items"
                        :ajax_url="related_items_ajax_url"
                        :filter_list_url="related_items_filter_list_url"
                    >
                    </RelatedItems>
                </div>
            </div>
        </div>
    </div>
</template>

<script>
import Species from '@/components/common/species_communities/species_profile.vue';
import Community from '@/components/common/species_communities/community_profile.vue';
import SpeciesDocuments from '@/components/common/species_communities/species_documents.vue';
import CommunityDocuments from '@/components/common/species_communities/community_documents.vue';
import SpeciesThreats from '@/components/common/species_communities/species_threats.vue';
import CommunityThreats from '@/components/common/species_communities/community_threats.vue';
import RelatedItems from '@/components/common/table_related_items.vue';

export default {
    components: {
        Species,
        Community,
        SpeciesDocuments,
        CommunityDocuments,
        SpeciesThreats,
        CommunityThreats,
        RelatedItems,
    },
    props: {
        species_community: {
            type: Object,
            required: true,
        },
        species_community_original: {
            type: Object,
            required: true,
        },
        is_external: {
            type: Boolean,
            default: false,
        },
        is_internal: {
            type: Boolean,
            default: false,
        },
        is_readonly: {
            type: Boolean,
            default: false,
        },
        rename_species: {
            type: Boolean,
            default: false,
        },
    },
    data: function () {
        let vm = this;
        return {
            profileBody: 'profileBody' + vm._uid,
            documentBody: 'documentBody' + vm._uid,
            threatBody: 'threatBody' + vm._uid,
            relatedItemBody: 'relatedItemBody' + vm._uid,
            values: null,
            reloadcount: 0,
        };
    },
    computed: {
        isCommunity: function () {
            return this.species_community.group_type == 'community';
        },
        is_public: function () {
            if (this.isCommunity) {
                return this.species_community.publishing_status
                    .community_public;
            }
            return this.species_community.publishing_status.species_public;
        },
        threats_public: function () {
            if (this.isCommunity) {
                return this.species_community.publishing_status.threats_public;
            }
            return (
                this.is_public &&
                this.species_community.publishing_status.threats_public
            );
        },
        related_items_ajax_url: function () {
            if (this.isCommunity) {
                return (
                    '/api/community/' +
                    this.species_community.id +
                    '/get_related_items/'
                );
            } else {
                return (
                    '/api/species/' +
                    this.species_community.id +
                    '/get_related_items/'
                );
            }
        },
        related_items_filter_list_url: function () {
            if (this.isCommunity) {
                return '/api/community/filter_list.json';
            } else {
                return '/api/species/filter_list.json';
            }
        },
    },
    mounted: function () {
        let vm = this;
        vm.form = document.forms.new_species;
    },
    methods: {
        tabClicked: function (param) {
            this.reloadcount = this.reloadcount + 1;
        },
        refreshSpeciesCommunity: function () {
            let vm = this;
            vm.$parent.refreshSpeciesCommunity();
        },
    },
};
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

.nav-item > li > a {
    background-color: yellow !important;
    color: #fff;
}

.nav-item > li.active > a,
.nav-item > li.active > a:hover,
.nav-item > li.active > a:focus {
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
