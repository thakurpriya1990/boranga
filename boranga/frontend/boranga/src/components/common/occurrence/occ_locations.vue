<template lang="html">
    <div id="occLocations">
        <MapComponent
            ref="component_map"
            :key="componentMapKey"
            class="me-3"
            :context="occurrence"
            :proposal-ids="occurrenceReportIds"
            :proposal-ids-layer="'query_layer'"
            :is_external="false"
            :point-features-supported="true"
            :polygon-features-supported="true"
            :drawable="true"
            :editable="true"
            :file-upload-disabled="true"
            level="internal"
            style-by="model"
            :map-info-text="
                isInternal ? '' : 'Some text to explain the map and its use.'
            "
            :selectable="true"
            :coordinate-reference-systems="coordinateReferenceSystems"
            :query-layer-definition="{
                name: 'query_layer',
                title: 'Occurrence Reports',
                default: false,
                can_edit: true,
            }"
            :additional-layers-definitions="[
                {
                    name: 'processed_layer',
                    title: 'Occurrence',
                    default: true,
                    can_edit: true,
                },
            ]"
            @crs-select-search="searchForCRS"
        ></MapComponent>
        <!-- @refreshFromResponse="refreshFromResponse" -->
        <!-- @validate-feature="validateFeature.bind(this)()" -->
    </div>
</template>

<script>
import { v4 as uuid } from 'uuid';
import { api_endpoints, helpers } from '@/utils/hooks';
import MapComponent from '../component_map.vue';

export default {
    name: 'OCClocations',
    components: {
        MapComponent,
    },
    props: {
        occurrence: {
            type: Object,
            required: true,
        },
        isExternal: {
            type: Boolean,
            default: false,
        },
        isInternal: {
            type: Boolean,
            default: true,
        },
        canEditStatus: {
            type: Boolean,
            default: true,
        },
        referral: {
            type: Object,
            required: false,
            default: () => null,
        },
    },
    emits: [],
    data() {
        return {
            uuid: uuid(),
            crs: [],
        };
    },
    computed: {
        componentMapKey: function () {
            return `component-map-${this.uuid}`;
        },
        coordinateReferenceSystems() {
            return this.crs;
        },
        occurrenceReportIds() {
            return this.occurrence.occurrence_reports.map(
                (report) => report.id
            );
        },
    },
    created() {
        fetch(
            helpers.add_endpoint_join(
                api_endpoints.occurrence,
                `/available-occurrence-reports-crs/?id=${this.occurrence.id}`
            )
        )
            .then((response) => {
                if (!response.ok) {
                    throw new Error('Network response was not ok');
                }
                return response.json();
            })
            .then((data) => {
                this.crs = data.crs;
            })
            .catch((error) => {
                console.error(
                    'Error fetching available ocr crs values list:',
                    error
                );
            });
    },
    methods: {
        searchForCRS: function (search, loading) {
            const vm = this;
            if (search.length < 2) {
                loading(false);
                return;
            }

            loading(true);
            fetch(
                helpers.add_endpoint_join(
                    api_endpoints.occurrence,
                    `/epsg-code-datums/?search=${search}`
                )
            )
                .then(async (response) => {
                    if (!response.ok) {
                        const text = await response.json();
                        throw new Error(text);
                    } else {
                        return response.json();
                    }
                })
                .then((data) => {
                    console.log('New search data return:', data);
                    // Append to existing list of crs rather than overwrite and potentially lose prior search results which might create issues when setting a pre-selected value
                    const crs_ids = vm.crs.map((crs) => crs.id);
                    data.forEach((crs) => {
                        if (!crs_ids.includes(crs.id)) {
                            vm.crs.push(crs);
                        }
                    });
                })
                .catch((error) => {
                    console.log(error);
                    swal.fire({
                        title: 'Search',
                        text: error,
                        icon: 'error',
                    });
                })
                .finally(() => {
                    loading(false);
                });
        },
    },
};
</script>

<style lang="css" scoped></style>
