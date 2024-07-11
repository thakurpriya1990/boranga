<template lang="html">
    <div id="occLocations">
        <FormSection :form-collapse="false" label="Location" Index="occurrence_location">
            <div class="row mb-3">
                <div class="col">
                    <span class="text-danger">*</span> <span class="text-muted">You must indicate the location for your occurrence</span>
                </div>
            </div>
            <div class="row mb-3">
                <MapComponent ref="component_map" :key="componentMapKey" class="me-3" :context="occurrence_obj"
                    :is_external="false" :point-features-supported="true" :polygon-features-supported="true"
                    :drawable="true" :editable="true" :file-upload-disabled="true" level="internal" style-by="model"
                    :map-info-text="isInternal ? '' : 'Some text to explain the map and its use.'
                        " :selectable="true" :coordinate-reference-systems="coordinateReferenceSystems"
                    :spatial-operations-allowed="['__all__']" :tile-layer-api-url="tileLayerApiUrl"
                    :query-layer-definition="{
                        name: queryLayerName,
                        title: 'Occurrence Reports',
                        default: false,
                        can_edit: false,
                        can_buffer: false,
                        can_hide_geometries: true,
                        api_url: ocrApiUrl,
                        ids: occurrenceReportIds,
                        geometry_name: 'ocr_geometry',
                        z_index: 2,
                        collapse: true,
                        property_display_map: ocrPropertyDisplayMap,
                    }" :additional-layers-definitions="[
                        {
                            name: occurrenceLayerName,
                            title: 'Occurrence',
                            default: true,
                            processed: true,
                            can_edit: true,
                            can_buffer: true,
                            api_url: occApiUrl,
                            ids: [occurrence_obj.id],
                            geometry_name: 'occ_geometry',
                            z_index: 3,
                            property_display_map: occPropertyDisplayMap,
                            property_overwrite: {
                                area_sqm: featureAreaMeter,
                                area_sqhm: (feature) =>
                                    featureAreaMeter(feature) / 10000,
                            },
                        },
                        {
                            name: 'buffer_layer',
                            title: 'Buffer Geometries',
                            default: false,
                            processed: false,
                            can_edit: false,
                            can_buffer: false,
                            handler: bufferGeometryHandler, // Buffer geometries are a property of occurrence geometry. This handler returns the buffer geometries from the occurrence geometries.
                            geometry_name: 'geometry',
                            z_index: 1,
                            property_display_map: bufferPropertyDisplayMap,
                            property_overwrite: {
                                area_sqm: featureAreaMeter,
                                area_sqhm: (feature) =>
                                    featureAreaMeter(feature) / 10000,
                            },
                        },
                        {
                            name: 'site_layer',
                            title: 'Site Geometries',
                            default: false,
                            processed: false,
                            can_edit: true,
                            can_buffer: false,
                            api_url: siteApiUrl,
                            query_param_key: 'occurrence_id',
                            z_index: 4,
                            ids: [occurrence_obj.id],
                            property_display_map: sitePropertyDisplayMap,
                            property_overwrite: { label: 'Site' },
                        },
                    ]"
                    @features-loaded="mapFeaturesLoaded"
                    @crs-select-search="searchForCRS"
                    @toggle-show-hide="toggleShowOnMapLayer"
                ></MapComponent>
            </div>
            <!-- @refreshFromResponse="refreshFromResponse" -->
            <!-- @validate-feature="validateFeature.bind(this)()" -->

            <div class="row mb-3">
                <label for="" class="col-sm-3 control-label">Region:</label>
                <div class="col-sm-9">
                    <select :disabled="isReadOnly" class="form-select" @change="filterDistrict($event)"
                        v-model="occurrence_obj.location.region_id">
                        <option v-for="option in region_list" :value="option.id" v-bind:key="option.id">
                            {{ option.name }}
                        </option>
                    </select>
                </div>
            </div>
            <div class="row mb-3">
                <label for="" class="col-sm-3 control-label">District:</label>
                <div class="col-sm-9">
                    <select :disabled="isReadOnly" class="form-select" v-model="occurrence_obj.location.district_id">
                        <option v-for="option in filtered_district_list" :value="option.id" v-bind:key="option.id">
                            {{ option.name }}
                        </option>
                    </select>
                </div>
            </div>
            <div class="row mb-3">
                <label for="" class="col-sm-3 control-label">Locality:</label>
                <div class="col-sm-9">
                    <textarea id="locality" v-model="occurrence_obj.location.locality
                        " :disabled="isReadOnly" class="form-control" rows="1" placeholder="" />
                </div>
            </div>

            <!-- -------------------------------- -->
            <div class="row mb-3">
                <label for="" class="col-sm-3 control-label">Location Description:</label>
                <div class="col-sm-9">
                    <textarea id="loc_description" v-model="occurrence_obj.location.location_description
                        " :disabled="isReadOnly" class="form-control" rows="2" placeholder="" />
                </div>
            </div>
            <div class="row mb-3">
                <label for="" class="col-sm-3 control-label">Boundary Description:</label>
                <div class="col-sm-9">
                    <textarea id="boundary_descr" v-model="occurrence_obj.location.boundary_description
                        " :disabled="isReadOnly" class="form-control" rows="2" placeholder="" />
                </div>
            </div>

            <div class="row mb-3">
                <label for="" class="col-sm-3 control-label">Map Data Type</label>
                <div class="col-sm-6">
                    <label class="me-2">Boundary</label><input disabled type="radio"
                        :checked="occurrence_obj.location.has_boundary" class="form-check-input me-2">
                    <label class="me-2">Point/s</label><input disabled type="radio"
                        :checked="occurrence_obj.location.has_points" class="form-check-input me-2">
                </div>
            </div>

            <div class="row mb-3">
                <label for="" class="col-sm-3 control-label">Coordinate Source:</label>
                <div class="col-sm-9">
                    <select v-model="occurrence_obj.location
                        .coordinate_source_id
                        " :disabled="isReadOnly" class="form-select">
                        <option v-for="option in coordinate_source_list" :key="option.id" :value="option.id">
                            {{ option.name }}
                        </option>
                    </select>
                </div>
            </div>

            <!--<div class="row mb-3">
                <label for="" class="col-sm-3 control-label"
                    >Boundary(m) :</label
                >
                <div class="col-sm-6">
                    <input
                        id="boundary"
                        v-model="occurrence_obj.location.boundary"
                        :disabled="isReadOnly"
                        type="number"
                        class="form-control ocr_number"
                        placeholder=""
                        min="0"
                    />
                </div>
            </div>
            <div class="row mb-3">
                <label for="" class="col-sm-3 control-label"
                    >Buffer Radius(m) :</label
                >
                <div class="col-sm-6">
                    <input
                        id="buffer_radius"
                        v-model="occurrence_obj.location.buffer_radius"
                        :disabled="isReadOnly"
                        type="number"
                        class="form-control ocr_number"
                        placeholder=""
                        min="0"
                    />
                </div>
            </div>-->
            <div class="row mb-3">
                <label for="" class="col-sm-3 control-label fw-bold">Location Accuracy: <span
                    class="text-danger">*</span></label>
                <div class="col-sm-9">
                    <select v-model="occurrence_obj.location.location_accuracy_id
                        " :disabled="isReadOnly" class="form-select">
                        <option v-for="option in location_accuracy_list" :key="option.id" :value="option.id">
                            {{ option.name }}
                        </option>
                    </select>
                </div>
            </div>
            <div class="row mb-3">
                <div class="col-sm-12">
                    <span v-if="occurrence_obj.location.copied_ocr" class="float-end"><b>Sourced from
                            {{ occurrence_obj.location.copied_ocr }}</b></span>
                </div>
            </div>
            <div class="row mb-3">
                <div class="col-sm-12">
                    <!-- <button v-if="!updatingLocationDetails" class="pull-right btn btn-primary" @click.prevent="updateDetails()" :disabled="!can_update()">Update</button> -->
                    <button v-if="!updatingLocationDetails" class="btn btn-primary btn-sm float-end"
                        @click.prevent="updateLocationDetails()" :disabled="isReadOnly">
                        Update
                    </button>
                    <button v-else disabled class="float-end btn btn-primary">
                        <i class="fa fa-spin fa-spinner"></i>&nbsp;Updating
                    </button>
                </div>
            </div>
            <FormSection :form-collapse="false" label="Occurrence Sites" Index="occurrence_sites_datatable">
                <div>
                    <OccurrenceSiteDatatable v-if="occurrence_obj" ref="occurrence_sites_datatable"
                        :key="datatableOCCSiteKey" :occurrence_obj="occurrence_obj" @updatedSites="updatedSites">
                    </OccurrenceSiteDatatable>
                </div>
            </FormSection>
            <!-- Occurrence Tenure Datatable -->
            <FormSection :form-collapse="false" label="Occurrence Tenures" Index="occurrence_tenure_datatable">
                <div>
                    <OccurrenceTenureDatatable v-if="occurrence_obj" ref="occurrence_tenure_datatable"
                        :key="datatableOCCTenureKey" :occurrence-id="occurrence_obj.id"
                        :href-container-id="getMapContainerId"
                        @highlight-on-map="highlightPointOnMap"
                        @edit-tenure-details="editTenureDetails"
                    >
                    </OccurrenceTenureDatatable>
                </div>
            </FormSection>
            <RelatedReports v-if="occurrence_obj" ref="related_reports_datatable" :key="datatableRelatedOCRKey"
                :is-read-only="isReadOnly" :occurrence_obj="occurrence_obj" :section_type="'location'"
                :href-container-id="getMapContainerId" :target-map-layer-name-for-copy="occurrenceLayerName"
                :target-map-layer-name-for-show-hide="queryLayerName"
                @copyUpdate="copyUpdate" @highlight-on-map="highlightIdOnMapLayer"
                @copy-to-map-layer="copyToMapLayer"
                @toggle-show-on-map="toggleShowOnMapLayer"
                />
        </FormSection>
    </div>
</template>

<script>
import Vue from 'vue';
import { v4 as uuid } from 'uuid';
import FormSection from '@/components/forms/section_toggle.vue';
import { api_endpoints, helpers } from '@/utils/hooks';
import MapComponent from '../component_map.vue';
import { VueSelect } from 'vue-select';
import OccurrenceSiteDatatable from '@/components/internal/occurrence/occurrence_site_datatable.vue';
import OccurrenceTenureDatatable from '@/components/internal/occurrence/occurrence_tenure_datatable.vue';
import RelatedReports from '@/components/common/occurrence/occ_related_ocr_table.vue'

export default {
    name: 'OCClocations',
    components: {
        MapComponent,
        FormSection,
        VueSelect,
        OccurrenceSiteDatatable,
        OccurrenceTenureDatatable,
        RelatedReports,
    },
    props: {
        occurrence_obj: {
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
            uuid_component_map: uuid(),
            uuid_datatable_ocr: uuid(),
            uuid_datatable_occ_site: uuid(),
            uuid_datatable_occ_tenure: uuid(),
            crs: [],
            region_list: [],
            district_list: [],
            filtered_district_list: [],
            updatingLocationDetails: false,
            listOfValuesDict: {},
            datum_list: [],
            coordinate_source_list: [],
            location_accuracy_list: [],
            mapReady: false,
            mapContainerId: false,
            queryLayerName: 'query_layer',
            occurrenceLayerName: 'occurrence_layer',
        };
    },
    computed: {
        componentMapKey: function () {
            return `component-map-${this.uuid_component_map}`;
        },
        datatableRelatedOCRKey: function () {
            return `datatable-ocr-${this.uuid_datatable_ocr}`;
        },
        datatableOCCSiteKey: function () {
            return `datatable-occ-site-${this.uuid_datatable_occ_site}`;
        },
        datatableOCCTenureKey: function () {
            return `datatable-occ-tenure-${this.uuid_datatable_occ_tenure}`;
        },
        coordinateReferenceSystems: function () {
            return this.crs;
        },
        occurrenceReportIds: function () {
            let ocrIds = this.occurrence_obj.occurrence_reports.map(
                (report) => report.id
            );
            // If no ocr ids for this occ, return [-1], because [] pulls _all_ ocrs
            ocrIds = ocrIds.length ? ocrIds : [-1];
            return ocrIds;
        },
        tileLayerApiUrl: function () {
            return api_endpoints.tile_layer;
        },
        ocrApiUrl: function () {
            return api_endpoints.occurrence_report + '/list_for_map/';
        },
        occApiUrl: function () {
            return api_endpoints.occurrence + 'list_for_map/';
        },
        siteApiUrl: function () {
            // TODO: Update to use the correct endpoint
            return '/api/occurrence_sites/list_for_map/';
        },
        ocrPropertyDisplayMap: function () {
            return {
                id: 'ID',
                // name: 'Name',
                label: 'Label', // Occurrence Report
                geometry_source: 'Geometry Source',
                occurrence_report_number: 'Identification Number',
                processing_status: 'Processing Status',
                lodgement_date_display: 'Lodgement Date',
                locked: 'Locked',
            };
        },
        occPropertyDisplayMap: function () {
            return {
                id: 'ID',
                // name: 'Name',
                label: 'Label', // Occurrence
                occurrence_number: 'Identification Number', // OCC1
                geometry_source: 'Geometry Source',
                processing_status_display: 'Processing Status',
                area_sqm: 'Area [m²]',
                area_sqhm: 'Area [ha]',
            };
        },
        bufferPropertyDisplayMap: function () {
            return {
                id: 'ID',
                // name: 'Name',
                label: 'Label', // OCC1 [Buffer]
                geometry_source: 'Geometry Source',
                // processing_status: 'Processing Status',
                // lodgement_date_display: 'Lodgement Date',
                area_sqm: 'Area [m²]',
                area_sqhm: 'Area [ha]',
                buffer_radius: 'Buffer Radius [m]',
            };
        },
        sitePropertyDisplayMap: function () {
            return {
                id: 'ID', // 8
                label: 'Label', // Site
                site_number: 'Identification Number', // ST1
                site_name: 'Site Name', // My Site
            };
        },
        bufferGeometriesApiUrl: function () {
            return api_endpoints.occurrence + 'buffer_geometries/';
        },
        isReadOnly: function () {
            //override for split reports
            if (this.is_readonly) {
                return this.is_readonly;
            }
            return this.occurrence_obj.readonly
        },
        csrf_token: function () {
            return helpers.getCookie('csrftoken');
        },
        getMapContainerId: function () {
            if (!this.mapReady) {
                return '';
            }
            return this.mapContainerId;
        },
    },
    created: async function () {
        let vm = this;
        let action = this.$route.query.action;

        fetch(
            helpers.add_endpoint_join(
                api_endpoints.occurrence,
                `/location-list-of-values/?id=${vm.occurrence_obj.id}`
            )
        )
            .then((response) => {
                if (!response.ok) {
                    throw new Error('Network response was not ok');
                }
                return response.json();
            })
            .then((data) => {
                vm.listOfValuesDict = Object.assign({}, data);
                vm.datum_list = vm.listOfValuesDict.datum_list;
                vm.coordinate_source_list =
                    vm.listOfValuesDict.coordinate_source_list;
                vm.coordinate_source_list.splice(0, 0, {
                    id: null,
                    name: null,
                });
                vm.location_accuracy_list =
                    vm.listOfValuesDict.location_accuracy_list;
                vm.location_accuracy_list.splice(0, 0, {
                    id: null,
                    name: null,
                });
            })
            .catch((error) => {
                console.error('Error fetching location values list:', error);
            });

        const response = await Vue.http.get('/api/region_district_filter_dict/');
        vm.filterRegionDistrict = response.body;
        vm.region_list = vm.filterRegionDistrict.region_list;
        vm.district_list = vm.filterRegionDistrict.district_list;
        vm.region_list.splice(0, 0,
            {
                id: null,
                name: null,
            });
        this.filterDistrict();

        fetch(
            helpers.add_endpoint_join(
                api_endpoints.occurrence,
                `/available-occurrence-reports-crs/?id=${this.occurrence_obj.id}`
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

        // Make sure the datatables have access to the map container id to have the page scroll to the map anchor
        this.refreshDatatables();
    },
    methods: {
        filterDistrict: function (event) {
            this.$nextTick(() => {
                if (event) {
                    this.occurrence_obj.location.district_id = null; //-----to remove the previous selection
                }
                this.filtered_district_list = [];
                this.filtered_district_list = [{
                    id: null,
                    name: "",
                    region_id: null,
                }];
                //---filter districts as per region selected
                for (let choice of this.district_list) {
                    if (choice.region_id === this.occurrence_obj.location.region_id) {
                        this.filtered_district_list.push(choice);
                    }
                }
            });
        },
        copyUpdate: function (object, section) {
            let vm = this;
            vm.occurrence_obj[section] = object[section];
        },
        updateLocationDetails: function () {
            let vm = this;
            vm.updatingLocationDetails = true;

            let payload = { location: vm.occurrence_obj.location };
            // species_id added in updateLocationDetails as its not part of Location model but needs to be updated on button click
            payload.species_id = vm.occurrence_obj.species_id;
            // community_id added in updateLocationDetails as its not part of Location model but needs to be updated on button click
            payload.community_id = vm.occurrence_obj.community_id;

            // When in Entering Conditions status ApplicationForm might not be there
            // adding occ_geometry from the map_component to payload
            if (vm.$refs.component_map) {
                payload.occ_geometry = vm.$refs.component_map.getJSONFeatures();
                vm.$refs.component_map.setLoadingMap(true);
            }

            payload.site_geometry = vm.$refs.component_map.getJSONFeatures("site_layer");

            // const res = await fetch(vm.proposal_form_url, {
            //     body: JSON.stringify(payload),
            //     method: 'POST',
            // });

            vm.$http
                .post(
                    helpers.add_endpoint_json(
                        api_endpoints.occurrence,
                        vm.occurrence_obj.id + '/update_location_details'
                    ),
                    JSON.stringify(payload),
                    {
                        emulateJSON: true,
                    }
                )
                .then(
                    (response) => {
                        vm.updatingLocationDetails = false;
                        vm.occurrence_obj.location = response.body;
                        swal.fire({
                            title: 'Saved',
                            text: 'Location details have been saved',
                            icon: 'success',
                            customClass: {
                                confirmButton: 'btn btn-primary',
                            },
                        }).then((result) => {
                            if (vm.occurrence_obj.processing_status == "Unlocked") {
                                vm.$router.go();
                            }
                        });
                        vm.incrementComponentMapKey();
                        vm.refreshDatatables();
                    },
                    (error) => {
                        var text = helpers.apiVueResourceError(error);
                        swal.fire({
                            title: 'Error',
                            text:
                                'Location details cannot be saved because of the following error: ' +
                                text,
                            icon: 'error',
                            customClass: {
                                confirmButton: 'btn btn-primary',
                            },
                        });
                        vm.updatingLocationDetails = false;
                        vm.$refs.component_map.setLoadingMap(false);
                    }
                );
        },
        incrementComponentMapKey: function () {
            this.uuid_component_map = uuid();
            this.$nextTick(() => {
                this.mapContainerId = this.$refs.component_map.map_container_id;
            });
        },
        refreshDatatables: function () {
            this.refreshDatatableRelatedOCR();
            this.uuid_datatable_occ_site = uuid();
            this.uuid_datatable_occ_tenure = uuid();
        },
        refreshDatatableRelatedOCR: function () {
            this.uuid_datatable_ocr = uuid();
        },
        updatedSites: function() {
            this.incrementComponentMapKey()
        },
        searchForCRS: function (search, loading) {
            const vm = this;
            if (search.length < 2) {
                loading(false);
                return;
            }

            loading(true);
            fetch(
                helpers.add_endpoint_join(
                    api_endpoints.occurrence_report,
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
        mapFeaturesLoaded: function () {
            console.log('Map features loaded.');
            this.mapContainerId = this.$refs.component_map.map_container_id;
            this.mapReady = true;
        },
        getMapFeatureById: function (id, layer_name) {
            if (!layer_name) {
                layer_name = this.queryLayerName;
            }
            const map = this.$refs.component_map;
            const layer = map.getLayerByName(layer_name);
            return map.getFeatureById(layer, id);
        },
        highlightPointOnMap: function (coordinates) {
            if (!coordinates) {
                console.warn('No coordinates found');
                return;
            }
            this.$refs.component_map.highlightPointOnTenureLayer(coordinates);
        },
        highlightIdOnMapLayer: function (id) {
            const feature = this.getMapFeatureById(id);
            this.$refs.component_map.centerOnFeature(feature);
        },
        editTenureDetails: function (id) {
            console.log(id);
        },
        copyToMapLayer: function (id, target_layer) {
            console.log('Copy to map layer:', id, target_layer);
            const map = this.$refs.component_map;
            const feature = this.getMapFeatureById(id);
            map.copyFeatureToLayer(feature, map.getLayerByName(target_layer));
        },
        /**
         * Toggle the show on map property of a feature.
         * @param {Object|Number} feature - The feature object or the feature id.
         * @param {String} layer_name - The layer name where the feature is located.
         */
        toggleShowOnMapLayer: function (feature, layer_name) {
            if (!isNaN(Number(feature))) {
                const id = feature;
                feature = this.getMapFeatureById(id, layer_name);
            }
            const show_on_map = feature.getProperties().show_on_map;
            feature.set('show_on_map', !show_on_map);
            this.updateShowHide(feature, layer_name).then(() => {
                this.refreshDatatableRelatedOCR();
            });
        },
        bufferGeometryHandler: function () {
            const occurrence_features = this.$refs.component_map
                .getLayerByName(this.occurrenceLayerName)
                .getSource()
                .getFeatures();

            const features = [];
            occurrence_features.forEach((feature) => {
                features.push(feature.getProperties().buffer_geometry);
            });

            return [
                {
                    geometry: {
                        features: features,
                    },
                },
            ];
        },
        updateShowHide: function (feature, layerName) {
            if (!layerName) {
                console.warn(`No layer name provided for update show/hide.`);
                return;
            }

            let apiEndpoint = null;
            if (layerName == this.queryLayerName) {
                apiEndpoint = helpers.add_endpoint_join(
                    api_endpoints.occurrence_report,
                    `/${feature.getProperties().name}/update_show_on_map/`
                );
            }

            if (!apiEndpoint) {
                console.warn(
                    `No API endpoint found for update show/hide for layer ${layerName}.`
                );
                return;
            }

            const showOnMap = feature.getProperties().show_on_map;
            const modelId = feature.getProperties().model_id;
            const payload = {
                method: 'PATCH',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': this.csrf_token,
                },
                body: JSON.stringify({
                    show_on_map: showOnMap,
                    model_id: modelId,
                }),
            };

            console.log(
                `Updating show on map for ${
                    feature.getProperties().label
                }: ${showOnMap}.`
            );
            return fetch(apiEndpoint, payload)
                .then(async (response) => {
                    if (!response.ok) {
                        return await response.json().then((json) => {
                            throw new Error(json);
                        });
                    }
                    return response.json();
                })
                .then((data) => {
                    return data;
                })
                .catch((error) => {
                    swal.fire({
                        title: 'Error',
                        text:
                            'Cannot change geometry visibility because of the following error: ' +
                            error,
                        icon: 'error',
                        customClass: {
                            confirmButton: 'btn btn-primary',
                        },
                    });
                });
        },
        featureAreaMeter: function (feature) {
            if (feature) {
                return this.$refs.component_map.featureArea(feature);
            }
            return null;
        },
    },
};
</script>

<style lang="css" scoped></style>
