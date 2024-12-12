<template lang="html">
    <div>
        <div class="col-md-12">
            <ul
                v-if="is_internal"
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
                <li class="nav-item">
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
                <li class="nav-item">
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
            </ul>
            <div id="pills-tabContent" class="tab-content">
                <div
                    :id="profileBody"
                    class="tab-pane fade show active"
                    role="tabpanel"
                    aria-labelledby="pills-profile-tab"
                >
                    <SpeciesProfile
                        id="speciesInformation"
                        ref="species_information"
                        :is_internal="is_internal"
                        :species_community="species_community"
                        :original_species_combine_list="
                            original_species_combine_list
                        "
                    >
                    </SpeciesProfile>
                </div>
                <div
                    :id="documentBody"
                    class="tab-pane fade"
                    role="tabpanel"
                    aria-labelledby="pills-documents-tab"
                >
                    <div v-for="species in original_species_combine_list">
                        <SpeciesDocuments
                            id="speciesDocuments"
                            :key="reloadcount"
                            ref="species_documents"
                            :is_internal="is_internal"
                            :species_community="species_community"
                            :species_original="species"
                        >
                        </SpeciesDocuments>
                    </div>
                </div>
                <div
                    :id="threatBody"
                    class="tab-pane fade"
                    role="tabpanel"
                    aria-labelledby="pills-threats-tab"
                >
                    <div v-for="species in original_species_combine_list">
                        <SpeciesThreats
                            id="speciesThreats"
                            :key="reloadcount"
                            ref="species_threats"
                            :is_internal="is_internal"
                            :species_community="species_community"
                            :species_original="species"
                        >
                        </SpeciesThreats>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>

<script>
import { v4 as uuid } from 'uuid';
import SpeciesProfile from '@/components/common/species_communities/species_combine/species_combine_profile.vue';
import SpeciesDocuments from '@/components/common/species_communities/species_combine/species_combine_documents.vue';
import SpeciesThreats from '@/components/common/species_communities/species_combine/species_combine_threats.vue';

export default {
    components: {
        SpeciesProfile,
        SpeciesDocuments,
        SpeciesThreats,
    },
    props: {
        original_species_combine_list: {
            type: Array,
            required: true,
        },
        species_community: {
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
    },
    data: function () {
        return {
            profileBody: 'profileBody' + uuid(),
            documentBody: 'documentBody' + uuid(),
            threatBody: 'threatBody' + uuid(),
            values: null,
            reloadcount: 0,
        };
    },
    computed: {
        related_items_ajax_url: function () {
            return (
                '/api/species/' +
                this.species_community.id +
                '/get_related_items/'
            );
        },
        related_items_filter_list_url: function () {
            return '/api/species/filter_list.json';
        },
    },
    mounted: function () {
        let vm = this;
        //vm.set_tabs();
        vm.form = document.forms.new_species;
    },
    methods: {
        //----function to resolve datatable exceeding beyond the div
        tabClicked: function () {
            this.reloadcount = this.reloadcount + 1;
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
