<template lang="html">
    <div>
        <div :id="occurrenceBody" class="">
            <CommunityOccurrence
                v-if="isCommunity"
                id="communityOccurrence"
                ref="community_occurrence"
                :occurrence_obj="occurrence_obj"
            >
            </CommunityOccurrence>
            <SpeciesOccurrence
                v-else
                id="speciesOccurrence"
                ref="species_occurrence"
                :occurrence_obj="occurrence_obj"
            >
            </SpeciesOccurrence>
        </div>
        <div class="col-md-12">
            <ul id="pills-tab" class="nav nav-pills" role="tablist">
                <li class="nav-item">
                    <a
                        id="pills-location-tab"
                        class="nav-link active"
                        data-bs-toggle="pill"
                        :href="'#' + locationBody"
                        role="tab"
                        :aria-controls="locationBody"
                        aria-selected="true"
                        @click="tabClicked()"
                    >
                        Location
                    </a>
                </li>
                <li class="nav-item">
                    <a
                        id="pills-habitat-tab"
                        class="nav-link"
                        data-bs-toggle="pill"
                        :href="'#' + habitatBody"
                        role="tab"
                        aria-selected="false"
                        @click="tabClicked()"
                    >
                        Habitat
                    </a>
                </li>
                <li class="nav-item">
                    <a
                        id="pills-observation-tab"
                        class="nav-link"
                        data-bs-toggle="pill"
                        :href="'#' + observationBody"
                        role="tab"
                        aria-selected="false"
                        @click="tabClicked()"
                    >
                        Observation
                    </a>
                </li>
                <li class="nav-item">
                    <a
                        id="pills-documents-tab"
                        class="nav-link"
                        data-bs-toggle="pill"
                        :href="'#' + documentBody"
                        role="tab"
                        aria-selected="false"
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
                        aria-selected="false"
                        @click="tabClicked()"
                    >
                        Threats
                    </a>
                </li>
                <li class="nav-item">
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
                    :id="locationBody"
                    class="tab-pane fade show active"
                    role="tabpanel"
                    aria-labelledby="pills-location-tab"
                >
                    <OCCLocations
                        id="occLocation"
                        :key="reloadcount"
                        ref="occ_location"
                        :is-external="is_external"
                        :is-internal="is_internal"
                        :can-edit-status="canEditStatus"
                        :occurrence_obj="occurrence_obj"
                        :referral="referral"
                        @refresh-from-response="refreshFromResponse"
                    >
                    </OCCLocations>
                </div>
                <div
                    :id="habitatBody"
                    class="tab-pane fade"
                    role="tabpanel"
                    aria-labelledby="pills-habitat-tab"
                >
                    <OCCHabitat
                        id="occhabitat"
                        :key="reloadcount"
                        ref="occ_habitat"
                        :is_internal="is_internal"
                        :occurrence_obj="occurrence_obj"
                    >
                    </OCCHabitat>
                </div>
                <div
                    :id="observationBody"
                    class="tab-pane fade"
                    role="tabpanel"
                    aria-labelledby="pills-observation-tab"
                >
                    <OCCObservation
                        id="occObservation"
                        :key="reloadcount"
                        ref="occ_observation"
                        :is_internal="is_internal"
                        :occurrence_obj="occurrence_obj"
                    >
                    </OCCObservation>
                </div>
                <div
                    :id="documentBody"
                    class="tab-pane fade"
                    role="tabpanel"
                    aria-labelledby="pills-documents-tab"
                >
                    <OCCDocuments
                        id="occDocuments"
                        :key="reloadcount"
                        ref="occ_documents"
                        :is_internal="is_internal"
                        :is_external="is_external"
                        :occurrence_obj="occurrence_obj"
                    >
                    </OCCDocuments>
                </div>
                <div
                    :id="threatBody"
                    class="tab-pane fade"
                    role="tabpanel"
                    aria-labelledby="pills-threats-tab"
                >
                    <OCCThreats
                        id="occThreats"
                        :key="reloadcount"
                        ref="occ_threats"
                        :is_internal="is_internal"
                        :occurrence_obj="occurrence_obj"
                    >
                    </OCCThreats>
                </div>
                <div
                    :id="reportBody"
                    class="tab-pane fade"
                    role="tabpanel"
                    aria-labelledby="pills-report-tab"
                ></div>
                <div
                    :id="sitesBody"
                    class="tab-pane fade"
                    role="tabpanel"
                    aria-labelledby="pills-sites-tab"
                ></div>
                <div
                    :id="relatedItemBody"
                    class="tab-pane fade"
                    role="tabpanel"
                    aria-labelledby="pills-sites-tab"
                >
                    <RelatedItems
                        id="occurrenceRelatedItems"
                        :key="reloadcount"
                        ref="occurrence_related_items"
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
import OCCLocations from '@/components/common/occurrence/occ_locations.vue';
import OCCHabitat from '@/components/common/occurrence/occ_habitat.vue';
import OCCObservation from '@/components/common/occurrence/occ_observation.vue';
import RelatedItems from '@/components/common/table_related_items.vue';
import OCCDocuments from '@/components/common/occurrence/occ_documents.vue';
import OCCThreats from '@/components/common/occurrence/occ_threats.vue';
import SpeciesOccurrence from '@/components/common/occurrence/species_occurrence.vue';
import CommunityOccurrence from '@/components/common/occurrence/community_occurrence.vue';

export default {
    components: {
        OCCLocations,
        OCCHabitat,
        OCCObservation,
        OCCDocuments,
        OCCThreats,
        SpeciesOccurrence,
        CommunityOccurrence,
        RelatedItems,
    },
    props: {
        occurrence_obj: {
            type: Object,
            required: true,
        },
        referral: {
            type: Object,
            required: false,
        },
        is_external: {
            type: Boolean,
            default: false,
        },
        is_internal: {
            type: Boolean,
            default: false,
        },
        canEditStatus: {
            type: Boolean,
            default: true,
        },
    },
    emits: ['refreshFromResponse'],
    data: function () {
        let vm = this;
        return {
            values: null,
            reloadcount: 0,
            locationBody: 'locationBody' + vm._uid,
            habitatBody: 'habitatBody' + vm._uid,
            observationBody: 'observationBody' + vm._uid,
            threatBody: 'threatBody' + vm._uid,
            documentBody: 'documentBody' + vm._uid,
            relatedItemBody: 'relatedItemBody' + vm._uid,
            reportBody: 'reportBody' + vm._uid,
            sitesBody: 'sitesBody' + vm._uid,
            occurrenceBody: 'occurrenceBody' + vm._uid,
        };
    },
    computed: {
        isCommunity: function () {
            return this.occurrence_obj.group_type == 'community';
        },
        related_items_ajax_url: function () {
            return (
                '/api/occurrence/' +
                this.occurrence_obj.id +
                '/get_related_items/'
            );
        },
        related_items_filter_list_url: function () {
            return '/api/occurrence/filter_list.json';
        },
    },
    mounted: function () {
        let vm = this;
        vm.form = document.forms.new_occurrence;
        vm.eventListener();
    },
    methods: {
        //----function to resolve datatable exceeding beyond the div
        // eslint-disable-next-line no-unused-vars
        tabClicked: function (param) {
            this.reloadcount = this.reloadcount + 1;
        },
        eventListener: function () {
            // eslint-disable-next-line no-unused-vars
            let vm = this;
        },
        // eslint-disable-next-line no-unused-vars
        refreshFromResponse: function (data) {
            //this.$emit('refreshFromResponse', data);
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
