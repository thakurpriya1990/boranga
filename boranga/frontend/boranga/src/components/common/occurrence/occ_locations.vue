<template lang="html">
    <div id="occLocations">
        <MapComponent
            ref="component_map"
            :key="componentMapKey"
            class="me-3"
            :context="occurrence"
            :proposal-ids="[]"
            :is_external="false"
            :point-features-supported="true"
            :polygon-features-supported="true"
            :drawable="true"
            :editable="true"
            :file-upload-disabled="true"
            level="internal"
            style-by="assessor"
            :map-info-text="
                isInternal ? '' : 'Some text to explain the map and its use.'
            "
            :selectable="true"
            :coordinate-reference-systems="coordinateReferenceSystems"
        ></MapComponent>
        <!-- @refreshFromResponse="refreshFromResponse" -->
        <!-- @validate-feature="validateFeature.bind(this)()" -->
        <!-- @crs-select-search="searchForCRS" -->
    </div>
</template>

<script>
import { v4 as uuid } from 'uuid';
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
            datum_list: [],
        };
    },
    computed: {
        componentMapKey: function () {
            return `component-map-${this.uuid}`;
        },
        coordinateReferenceSystems() {
            return [{ id: 4326, name: 'EPSG:4326 - WGS 84' }];
        },
    },
};
</script>

<style lang="css" scoped></style>
