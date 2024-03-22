<template>
    <!--
        TODO tasks (and ideas):
        - populate tenure, locality, and categorisation from geoserver response (see: map_functions::validateFeature for response values and owsQuery prop for query paramerters)
        - [DONE] prevent polygon delete after save (or save + status change)
        - polygon redo button
        - polygon edit button (move and add/remove vertices)
        - pass in map tab filterable proposals as prop (see: prop featureCollection)
        - standardise feature tooltip fields (lodgement_date formatting, application_type, processing_status, etc.) across models
        - hide feature tooltip on save as it might overlap the save response modal
        - solve click-select and hover-select for overlapping polygons (cannot click-select a feature for delete if it is under another feature)
        - prevent referrals from creating/editing polygons in the frontend (does not save in backend anyway)
        - disable draw tool for external when model is not in draft status
        - disable draw tool for referral when model is not in with referral status
        - [] display polygons of approved proposal on new license proposal (external 017, internal 041)
        - [] display polygons from the competitive process of an proposal that proceeded to a competitive process on the proposal page
        - implement map on approval details page and map tab
        - keyboard input (del to delete a feature, ctrl+z to undo, ctrl+y to redo, d to draw, etc.)
        - delete old map files
        - rename this file
        - automatic zoom to all on map load
     -->
    <div>
        <div class="justify-content-end align-items-center mb-2">
            <div v-if="mapInfoText.length > 0" class="row">
                <div class="col-md-6">
                    <BootstrapAlert class="mb-0">
                        <!-- eslint-disable vue/no-v-html -->
                        <p><span v-html="mapInfoText"></span></p>
                        <!--eslint-enable-->
                    </BootstrapAlert>
                </div>
            </div>
        </div>

        <VueAlert
            :show="hasErrorMessage"
            type="danger"
            style="color: red"
            ><strong> {{ errorMessage }} </strong>
        </VueAlert>

        <div
            :id="map_container_id"
            class="d-flex justify-content-center"
            style="position: relative"
        >
            <div :id="elem_id" class="map">
                <div class="basemap-button" title="Toggle background map">
                    <img
                        id="basemap_sat"
                        src="../../assets/satellite_icon.jpg"
                        @click="setBaseLayer('sat')"
                    />
                    <img
                        id="basemap_osm"
                        src="../../assets/map_icon.png"
                        @click="setBaseLayer('osm')"
                    />
                </div>
                <div class="optional-layers-wrapper">
                    <!-- Toggle measure tool between active and not active -->
                    <div class="optional-layers-button-wrapper">
                        <div
                            :title="
                                mode == 'measure'
                                    ? 'Deactivate measure tool'
                                    : 'Activate measure tool'
                            "
                            :class="[
                                mode == 'measure'
                                    ? 'optional-layers-button-active'
                                    : 'optional-layers-button',
                            ]"
                            @click="set_mode.bind(this)('measure')"
                        >
                            <img
                                class="svg-icon"
                                src="../../assets/ruler.svg"
                            />
                        </div>
                    </div>
                    <div v-if="drawable" class="optional-layers-button-wrapper">
                        <div
                            :title="
                                mode == 'draw'
                                    ? 'Deactivate draw tool'
                                    : 'Activate draw tool'
                            "
                            :class="[
                                mode == 'draw'
                                    ? 'optional-layers-button-active'
                                    : 'optional-layers-button',
                            ]"
                            @click="set_mode('draw')"
                        >
                            <img
                                class="svg-icon"
                                src="../../assets/pen-icon.svg"
                            />
                        </div>
                    </div>
                    <div
                        v-if="polygonCount"
                        class="optional-layers-button-wrapper"
                    >
                        <div
                            title="Zoom map to layer(s)"
                            class="optional-layers-button"
                            @click="displayAllFeatures"
                        >
                            <img
                                class="svg-icon"
                                src="../../assets/map-zoom.svg"
                            />
                        </div>
                    </div>
                    <div class="optional-layers-button-wrapper">

                        <div
                            title="Download layers as GeoJSON"
                            class="optional-layers-button"
                            @click="geoJsonButtonClicked"
                        >
                            <img
                                class="svg-icon"
                                src="../../assets/download.svg"
                            />
                        </div>
                    </div>
                    
                    <!-- <div
                        v-if="optionalLayersActive"
                        class="optional-layers-button-wrapper"
                    >
                        <div
                            :title="
                                mode == 'info'
                                    ? 'Deactivate info tool'
                                    : 'Activate info tool'
                            "
                            :class="[
                                mode == 'info'
                                    ? 'optional-layers-button-active'
                                    : 'optional-layers-button',
                            ]"
                            @click="set_mode.bind(this)('info')"
                        >
                            <img
                                class="svg-icon"
                                src="../../assets/info-query.svg"
                            />
                        </div>
                    </div> -->
                    <div
                        v-if="selectedFeatureIds.length > 0"
                        class="optional-layers-button-wrapper"
                    >
                        <div
                            class="optional-layers-button"
                            title="Delete selected features"
                            @click="removeModelFeatures()"
                        >
                            <img
                                class="svg-icon"
                                src="../../assets/trash-bin.svg"
                            />
                            <span
                                id="selectedFeatureCount"
                                class="badge badge-warning"
                                >{{ selectedFeatureIds.length }}</span
                            >
                        </div>
                    </div>
                    <div
                        v-if="showUndoButton"
                        class="optional-layers-button-wrapper"
                    >
                        <div
                            class="optional-layers-button"
                            title="Undo last point"
                            @click="undoLeaseLicensePoint()"
                        >
                            <img
                                class="svg-icon"
                                src="../../assets/map-undo.svg"
                            />
                        </div>
                    </div>
                    <div
                        v-if="showRedoButton"
                        class="optional-layers-button-wrapper"
                    >
                        <div
                            class="optional-layers-button"
                            title="Redo last point"
                            @click="redoLeaseLicensePoint()"
                        >
                            <img
                                class="svg-icon"
                                src="../../assets/map-redo.svg"
                            />
                        </div>
                    </div>
                </div>

                <!-- <div id="featureToast" class="toast" style="z-index: 9999">
                    <template v-if="selectedModel">
                        <div class="toast-header">
                            <img src="" class="rounded me-2" alt="" />
                            // FIXME: Can this be standardised into the same field name? 
                            <strong class="me-auto"
                                >{{
                                    selectedModel.label ||
                                    selectedModel.application_type_name_display ||
                                    selectedModel.application_type.name_display
                                }}: {{ selectedModel.lodgement_number }}</strong
                            >
                        </div>
                        <div class="toast-body">
                            <table class="table table-sm">
                                <tbody>
                                    <tr>
                                        <th scope="row">Processing Status</th>
                                        // FIXME: Can this be standardised into the same field name? 
                                        <td>
                                            {{
                                                selectedModel.status ||
                                                selectedModel.status_display ||
                                                selectedModel.processing_status_display ||
                                                selectedModel.processing_status
                                            }}
                                        </td>
                                    </tr>
                                     TODO: `created_at` is not formatted to DD/MM/YYYY 
                                    <tr
                                        v-if="
                                            selectedModel.copied_from ||
                                            selectedModel.lodgement_date_display ||
                                            selectedModel.lodgement_date ||
                                            selectedModel.created_at ||
                                            selectedModel.created_at_display
                                        "
                                    >
                                        <th
                                            v-if="selectedModel.copied_from"
                                            scope="row"
                                        >
                                            Lodgement (original application)
                                        </th>
                                        <th v-else scope="row">
                                            Lodgement Date
                                        </th>
                                         FIXME: Can this be standardised into the same field name? 
                                        <td v-if="selectedModel.copied_from">
                                            {{
                                                selectedModel.copied_from
                                                    .lodgement_date_display
                                            }}
                                        </td>
                                        <td v-else>
                                            {{
                                                selectedModel.lodgement_date_display ||
                                                selectedModel.lodgement_date ||
                                                selectedModel.created_at ||
                                                selectedModel.created_at_display
                                            }}
                                        </td>
                                    </tr>
                                    <tr v-if="selectedModel.geometry_source">
                                        <th scope="row">Geometry Source</th>
                                        <td>
                                            {{ selectedModel.geometry_source }}
                                        </td>
                                    </tr>
                                    <tr v-if="selectedModel.area_sqm">
                                        <template
                                            v-if="
                                                selectedModel.area_sqm > 10000
                                            "
                                        >
                                            <th scope="row">Area (hm&#178;)</th>
                                            <td>
                                                {{
                                                    selectedModel.area_sqm /
                                                    10000
                                                }}
                                            </td>
                                        </template>
                                        <template v-else>
                                            <th scope="row">Area (m&#178;)</th>
                                            <td>
                                                {{ selectedModel.area_sqm }}
                                            </td>
                                        </template>
                                    </tr>
                                </tbody>
                            </table>
                        </div>
                    </template>
                </div> -->

                <!-- Overlay popup bubble when clicking a DBCA layer feature -->
                <!-- <div id="popup" class="ol-popup overlay-feature-popup">
                    <template v-if="overlayFeatureInfo">
                        <div class="toast-header">
                            <img src="" class="rounded me-2" alt="" />
                            <strong class="me-auto">{{
                                overlayFeatureInfo.leg_name
                            }}</strong>
                        </div>
                        <div id="popup-content toast-body">
                            <table
                                style="width: 100%; z-index: 9999"
                                class="table table-sm"
                            >
                                <tbody>
                                    <tr>
                                        <th scope="row">Identifier</th>
                                        <td>
                                            {{
                                                overlayFeatureInfo.leg_identifier
                                            }}
                                        </td>
                                    </tr>
                                    <tr>
                                        <th scope="row">Vesting</th>
                                        <td>
                                            {{ overlayFeatureInfo.leg_vesting }}
                                        </td>
                                    </tr>
                                    <tr>
                                        <th scope="row">Legal Act</th>
                                        <td>
                                            {{ overlayFeatureInfo.leg_act }}
                                        </td>
                                    </tr>
                                    <tr>
                                        <th scope="row">Tenure</th>
                                        <td>
                                            {{ overlayFeatureInfo.leg_tenure }}
                                        </td>
                                    </tr>
                                    <tr>
                                        <th scope="row">Category</th>
                                        <td>
                                            {{ overlayFeatureInfo.category }}
                                        </td>
                                    </tr>
                                </tbody>
                            </table>
                        </div>
                    </template>
                </div> -->
                <!-- <BootstrapSpinner
                    v-if="
                        redirectingToModelDetails ||
                        queryingGeoserver ||
                        fetchingProposals ||
                        loadingMap
                    "
                    id="map-spinner"
                    class="text-primary"
                /> -->
            </div>
            <div id="coords"></div>
            <!-- <BootstrapSpinner v-if="!proposals" class="text-primary" /> -->
        </div>
        <!-- <div class="row shapefile-row">
            <div class="col-sm-6 border p-2">
                <div class="row mb-2">
                    <div class="col">
                        <label for="shapefile_document" class="fw-bold"
                            >Upload Shapefile
                        </label>
                    </div>
                    <div class="col">
                        <FileField
                            id="shapefile_document_document"
                            ref="shapefile_document"
                            :readonly="false"
                            name="shapefile_document"
                            :is-repeatable="true"
                            :document-action-url="shapefileDocumentUrl"
                            :replace_button_by_text="true"
                            file-types=".dbf, .prj, .shp, .shx"
                            text_string="Attach File (.prj .dbf .shp
                                .shx)"
                        />
                    </div>
                </div>
                <div class="row">
                    <div class="col">
                        <BootstrapAlert
                            >If you do not upload a .prj file, we will use
                            <a
                                href="https://en.wikipedia.org/wiki/World_Geodetic_System#WGS84"
                                target="_blank"
                                >WGS 84</a
                            >
                            / 'EPSG:4326'
                        </BootstrapAlert>
                    </div>
                </div>
                <div class="row">
                    <div class="col">
                        <button
                            v-if="isValidating"
                            type="button"
                            disabled
                            class="btn btn-primary"
                        >
                            <div class="row">
                                <div
                                    class="col-sm-12 text-nowrap text-truncate"
                                >
                                    <i class="fa fa-spinner fa-spin"></i>
                                </div>
                            </div>
                        </button>
                        <button
                            v-else
                            type="button"
                            class="btn btn-primary"
                            @click="validate_map_docs"
                        >
                            <div class="row">
                                <div
                                    class="col-sm-12 text-nowrap text-truncate"
                                >
                                    Process Files
                                </div>
                            </div>
                        </button>
                    </div>
                </div>
            </div>
            <div class="col-sm-6">
                <div id="legend_title"></div>
                <div id="legend">
                    <img src="" />
                </div>
            </div>
        </div> -->
    </div>
</template>

<script>
import { v4 as uuid } from 'uuid';
import { api_endpoints, helpers, utils } from '@/utils/hooks';
//import CollapsibleFilters from '@/components/forms/collapsible_component.vue';
import VueAlert from '@vue-utils/alert.vue';

import { toRaw } from 'vue';
import 'ol/ol.css';
import Map from 'ol/Map';
import View from 'ol/View';
import TileLayer from 'ol/layer/Tile';
import TileWMS from 'ol/source/TileWMS';
import { Draw, Select } from 'ol/interaction';
import Feature from 'ol/Feature';
import VectorLayer from 'ol/layer/Vector';
import VectorSource from 'ol/source/Vector';
import { Circle as CircleStyle, Fill, Stroke, Style } from 'ol/style';
import { FullScreen as FullScreenControl } from 'ol/control';
import { LineString, Point, Polygon } from 'ol/geom';
import GeoJSON from 'ol/format/GeoJSON';
import Overlay from 'ol/Overlay.js';
import MeasureStyles, { formatLength } from '@/components/common/measure.js';
//import RangeSlider from '@/components/forms/range_slider.vue';
import FileField from '@/components/forms/filefield_immediate.vue';
import {
    addOptionalLayers,
    //set_mode,
    baselayer_name,
} from '@/components/common/map_functions.js';

export default {
    name: 'MapComponent',
    components: {
        //CollapsibleFilters,
        FileField,
        //RangeSlider,
        VueAlert,
    },
    props: {
        // level: {
        //     type: String,
        //     required: true,
        //     validator: function (val) {
        //         let options = ['internal', 'referral', 'external'];
        //         return options.indexOf(val) != -1 ? true : false;
        //     },
        // },
        /**
         * The context of the map. This is used to determine which layers to show on the map.
         * The context should be a model object, e.g. a Proposal, Application, etc.
         * Used to allocate ids, labels, etc to new features
         */
        context: {
            type: Object,
            required: false,
            default: null,
        },
        /**
         * Ids of porposals to be fetched by the map componment and displayed on the map.
         * Negative values fetch no proposals
         * Positive values fetch proposals with those ids
         * Empty list `[]` fetches all proposals
         */
        proposalIds: {
            type: Array,
            required: false,
            default() {
                return [];
            },
        },
        /**
         * A geojson feature collection of features (possibvly related to the context) to display on the map.
         */
        featureCollection: {
            type: Object,
            required: false,
            default() {
                return { features: [], type: 'FeatureCollection' };
            },
            validator: function (val) {
                return val.type == 'FeatureCollection' ? true : false;
            },
        },
        /**
         * A classifier to style the features by.
         * `model` displays all features belonging to the same model by the same (randomly generated) color
         * `assessor` displays all features by same color depending on the role of the user who created the feature
         * @values model, assessor
         */
        styleBy: {
            type: String,
            required: false,
            default: 'model',
            validator: function (val) {
                let options = ['model', 'assessor'];
                return options.indexOf(val) != -1 ? true : false;
            },
        },
        /**
         * Color definitions for the features to be used when styling by `assessor`
         * @values unknown, draw, applicant, assessor
         */
        featureColors: {
            type: Object,
            required: false,
            default: () => {
                return {
                    unknown: '#9999', // greyish
                    draw: '#00FFFF', // cyan
                    applicant: '#00FF0077',
                    assessor: '#0000FF77',
                };
            },
            validator: function (val) {
                let options = ['unknown', 'draw', 'applicant', 'assessor'];
                Object.keys(val).forEach((key) => {
                    if (!options.includes(key.toLowerCase())) {
                        console.error('Invalid feature color key: ' + key);
                        return false;
                    }
                    // Invalid color values will evaluate to an empty string
                    let test = new Option().style;
                    test.color = val[key];
                    if (test.color === '') {
                        console.error(
                            `Invalid ${key} color value: ${val[key]}`
                        );
                        return false;
                    }
                });
                return true;
            },
        },
        /**
         * A dictionary of query parameters to pass to the WFS geoserver
         * The parent component needs to add the `cql_filter` parameter to filter the features by a spatial opration
         */
        // owsQuery: {
        //     type: Object,
        //     required: false,
        //     default: () => {
        //         return {
        //             version: '1.0.0', // WFS version
        //             landwater: {
        //                 typeName: 'public:dbca_legislated_lands_and_waters',
        //                 srsName: 'EPSG:4326',
        //                 propertyName: 'wkb_geometry', // Default to query for feature geometries only
        //                 geometry: 'wkb_geometry', // Geometry name (not `the_geom`)
        //             },
        //         };
        //     },
        // },
        /**
         * Whether to display a filter component above the map
         */
        // filterable: {
        //     type: Boolean,
        //     required: false,
        //     default: true,
        // },
        /**
         * Whether to enable drawing of new features
         */
        drawable: {
            type: Boolean,
            required: false,
            default: false,
        },
        /**
         * Whether to enable selecting existing features (e.g. for deletion)
         */
        selectable: {
            type: Boolean,
            required: false,
            default: false,
        },
        /**
         * A text that explains what is expected on the map
         */
        mapInfoText: {
            type: String,
            required: false,
            default: '',
        },
        /**
         * Whether to refresh the map when the component is mounted
         * Defaults to false, as it might be advisable to load and refresh the map only when it is needed
         * E.g. when the map tab is selected
         */
        refreshMapOnMounted: {
            type: Boolean,
            required: false,
            default: false,
        },
    },
    emits: ['validate-feature', 'refreshFromResponse'],
    data() {
        let vm = this;
        return {
            
            elem_id: uuid(),
            map_container_id: uuid(),
            map: null,
            tileLayerMapbox: null,
            tileLayerSat: null,
            optionalLayers: [],
            hover: false,
            mode: 'normal',
            drawForMeasure: null,
            drawForModel: null,
            newFeatureId: 0,
            measurementLayer: null,
            style: MeasureStyles.defaultStyle,
            segmentStyle: MeasureStyles.segmentStyle,
            labelStyle: MeasureStyles.labelStyle,
            segmentStyles: null,
            content_element: null,
            featureToast: null,
            selectedFeature: null,
            selectedModel: null,
            redirectingToModelDetails: false,
            queryingGeoserver: false,
            loadingMap: false,
            fetchingProposals: false,
            proposals: [],
            filteredProposals: [],
            modelQuerySource: null,
            modelQueryLayer: null,
            selectedFeatureIds: [],
            lastPoint: null,
            sketchCoordinates: [[]],
            sketchCoordinatesHistory: [[]],
            defaultColor: '#eeeeee',
            clickSelectStroke: new Stroke({
                color: 'rgba(255, 0, 0, 0.7)',
                width: 2,
            }),
            hoverFill: new Fill({
                color: 'rgba(255, 255, 255, 0.5)',
            }),
            hoverStroke: new Stroke({
                color: 'rgba(255, 255, 255, 0.5)',
                width: 1,
            }),
            //set_mode: set_mode,
            isValidating: false,
            errorMessage: null,
            overlayFeatureInfo: {},
            deletedFeatures: [], // keep track of deleted features
        };
    },
    computed: {
        // shapefileDocumentUrl: function () {
        //     let endpoint = '';
        //     let obj_id = 0;
        //     if (this.context.model_name == 'proposal') {
        //         endpoint = api_endpoints.proposal;
        //         obj_id = this.context.id;
        //     } else if (this.context.model_name == 'competitiveprocess') {
        //         endpoint = api_endpoints.competitive_process;
        //         obj_id = this.context.id;
        //     } else {
        //         console.warn('shapefileDocumentUrl: invalid context');
        //         return ''; // Should not reach here.
        //     }
        //     let url = helpers.add_endpoint_join(
        //         endpoint,
        //         '/' + obj_id + '/process_shapefile_document/'
        //     );
        //     console.log({ url });
        //     return url;
        // },
        showUndoButton: function () {
            return (
                this.mode == 'draw' &&
                this.drawForModel &&
                this.drawForModel.getActive() &&
                this.sketchCoordinates.length > 1
            );
        },
        showRedoButton: function () {
            return false;
            /* Todo: The redo button is partially implemented so it is disabled for now.
            return (
                this.mode == 'draw' &&
                this.drawForModel &&
                this.drawForModel.getActive() &&
                this.sketchCoordinatesHistory.length >
                    this.sketchCoordinates.length
            )*/
        },
        // optionalLayersActive: function () {
        //     if (this.optionalLayers.length == 0) {
        //         return false;
        //     }
        //     let visible_layers = this.optionalLayers.filter(
        //         (layer) => layer.values_.visible === true
        //     );
        //     return visible_layers.length > 0;
        // },
        polygonCount: function () {
            let vm = this;
            if (!this.modelQuerySource) {
                return 0;
            }
            return vm.modelQuerySource.getFeatures().length;
        },
        hasErrorMessage: function () {
            let vm = this;
            return vm.errorMessage !== null;
        },
    },
    watch: {
        selectedFeatureIds: function () {
            if (this.selectedFeatureIds.length == 0) {
                this.errorMessageProperty(null);
            }
        },
    },
    created: function () {
        console.log('created()');
        //this.fetchProposals();
    },
    mounted: function () {
        console.log('mounted()');
        let vm = this;
        vm.loadingMap = true;

        this.$nextTick(() => {
            // var toastEl = document.getElementById('featureToast');
            $('#map-spinner').children().css('position', 'static'); // Position spinner in center of map
            vm.initialiseMap();
            vm.set_mode('layer');
            vm.setBaseLayer('osm');
            //addOptionalLayers(this);
            // vm.featureToast = new bootstrap.Toast(toastEl, { autohide: false });
            if (vm.refreshMapOnMounted) {
                vm.forceToRefreshMap();
            } else {
                console.log('Done initializing map (no refresh)');
                vm.loadingMap = false;
            }
        });
    },
    methods: {
        valueChanged: function (value, tileLayer) {
            tileLayer.setOpacity(value / 100);
        },
        download_content: function (content, fileName, contentType) {
            var a = document.createElement('a');
            var file = new Blob([content], { type: contentType });
            a.href = URL.createObjectURL(file);
            a.download = fileName;
            a.click();
        },
        geoJsonButtonClicked: function () {
            let vm = this;
            let json = new GeoJSON().writeFeatures(
                vm.modelQuerySource.getFeatures(),
                {}
            );
            vm.download_content(
                json,
                'leases_and_licensing_layers.geojson',
                'text/plain'
            );
        },
        displayAllFeatures: function () {
            console.log('in displayAllFeatures()');
            let vm = this;
            if (vm.map) {
                if (vm.modelQuerySource.getFeatures().length > 0) {
                    let view = vm.map.getView();
                    let ext = vm.modelQuerySource.getExtent();
                    let centre = [
                        (ext[0] + ext[2]) / 2.0,
                        (ext[1] + ext[3]) / 2.0,
                    ];
                    let resolution = view.getResolutionForExtent(ext);
                    let z = view.getZoomForResolution(resolution) - 1;
                    view.animate({ zoom: z, center: centre });
                }
            }
        },
        setBaseLayer: function (selected_layer_name) {
            let vm = this;
            if (selected_layer_name == 'sat') {
                vm.tileLayerMapbox.setVisible(false);
                vm.tileLayerSat.setVisible(true);
                $('#basemap_sat').hide();
                $('#basemap_osm').show();
            } else {
                vm.tileLayerMapbox.setVisible(true);
                vm.tileLayerSat.setVisible(false);
                $('#basemap_osm').hide();
                $('#basemap_sat').show();
            }
        },
        // changeLayerVisibility: function (targetLayer) {
        //     targetLayer.setVisible(!targetLayer.getVisible());
        // },
        // clearMeasurementLayer: function () {
        //     let vm = this;
        //     let features = vm.measurementLayer.getSource().getFeatures();
        //     features.forEach((feature) => {
        //         vm.measurementLayer.getSource().removeFeature(feature);
        //     });
        // },
        forceToRefreshMap(timeout = 700) {
            let vm = this;
            setTimeout(function () {
                console.log('Refreshing map');
                vm.map.updateSize();
                // Unset loading map spinner here
                vm.loadingMap = false;
            }, timeout);
        },
        addJoint: function (point, styles) {
            let s = new Style({
                image: new CircleStyle({
                    radius: 2,
                    fill: new Fill({
                        color: '#3399cc',
                    }),
                }),
            });
            s.setGeometry(point);
            styles.push(s);

            return styles;
        },
        /**
         * Returns a color for a feature based on the styleBy property
         * and either the feature or model object
         * @param {dict} featureData A feature object
         * @param {Proxy} model A model object
         */
        styleByColor: function (featureData, model) {
            let vm = this;

            if (vm.styleBy === 'assessor') {
                // Assume the object is a feature containing a geometry_source property
                return vm.featureColors[
                    featureData.properties.geometry_source.toLowerCase()
                ];
            } else if (vm.styleBy === 'model') {
                // Assume the object is a model containing a color field
                return model.color;
            } else {
                return vm.featureColors['unknown'] || vm.defaultColor;
            }
        },
        createStyle: function (color) {
            let vm = this;
            if (!color) {
                color = vm.defaultColor;
            }

            let style = new Style({
                stroke: new Stroke({
                    color: color,
                    width: 1,
                }),
                fill: new Fill({
                    color: color,
                }),
            });

            return style;
        },
        styleFunctionForMeasurement: function (feature) {
            let vm = this;
            let for_layer = feature.get('for_layer', false);

            const styles = [];
            styles.push(vm.style); // This style is for the feature itself
            styles.push(vm.segmentStyle);

            ///////
            // From here, adding labels and tiny circles at the end points of the linestring
            ///////
            const geometry = feature.getGeometry();
            if (geometry.getType() === 'LineString') {
                let segment_count = 0;
                geometry.forEachSegment(function (a, b) {
                    const segment = new LineString([a, b]);
                    const label = formatLength(segment);
                    const segmentPoint = new Point(
                        segment.getCoordinateAt(0.5)
                    );

                    // Add a style for this segment
                    let segment_style = vm.segmentStyle.clone(); // Because there could be multilpe segments, we should copy the style per segment
                    segment_style.setGeometry(segmentPoint);
                    segment_style.getText().setText(label);
                    styles.push(segment_style);

                    if (segment_count == 0) {
                        // Add a tiny circle to the very first coordinate of the linestring
                        let p = new Point(a);
                        vm.addJoint(p, styles);
                    }
                    // Add tiny circles to the end of the linestring
                    let p = new Point(b);
                    vm.addJoint(p, styles);

                    segment_count++;
                });
            }

            if (!for_layer) {
                // We don't need the last label when draw on the layer.
                let label_on_mouse = formatLength(geometry); // Total length of the linestring
                let point = new Point(geometry.getLastCoordinate());
                vm.labelStyle.setGeometry(point);
                vm.labelStyle.getText().setText(label_on_mouse);
                styles.push(vm.labelStyle);
            }

            return styles;
        },
        initialiseMap: function () {
            let vm = this;

            let satelliteTileWms = new TileWMS({
                url: env['kmi_server_url'] + '/geoserver/public/wms',
                params: {
                    FORMAT: 'image/png',
                    VERSION: '1.1.1',
                    tiled: true,
                    STYLES: '',
                    LAYERS: 'public:mapbox-satellite',
                },
            });

            let streetsTileWMS = new TileWMS({
                url: env['kmi_server_url'] + '/geoserver/public/wms',
                params: {
                    FORMAT: 'image/png',
                    VERSION: '1.1.1',
                    tiled: true,
                    STYLES: '',
                    LAYERS: `public:${baselayer_name}`,
                },
            });
            vm.tileLayerMapbox = new TileLayer({
                title: 'StreetsMap',
                type: 'base',
                visible: true,
                source: streetsTileWMS,
            });

            vm.tileLayerSat = new TileLayer({
                title: 'Satellite',
                type: 'base',
                visible: true,
                source: satelliteTileWms,
            });

            let container = document.getElementById('popup');
            let overlay = new Overlay({
                element: container,
                autoPan: true,
                autoPanAnimation: {
                    duration: 150,
                },
            });

            vm.map = new Map({
                layers: [vm.tileLayerMapbox, vm.tileLayerSat],
                overlays: [overlay],
                target: vm.elem_id,
                view: new View({
                    center: [115.95, -31.95],
                    zoom: 7,
                    projection: 'EPSG:4326',
                }),
            });

            // Full screen toggle
            let fullScreenControl = new FullScreenControl();
            vm.map.addControl(fullScreenControl);

            //vm.initialiseMeasurementLayer();
            vm.initialiseQueryLayer();
            vm.initialiseDrawLayer();

            // update map extent when new features added
            vm.map.on('rendercomplete', vm.displayAllFeatures());

            vm.initialisePointerMoveEvent();
            vm.initialiseSelectFeatureEvent();
            vm.initialiseSingleClickEvent();
            //vm.initialiseDoubleClickEvent();
        },
        // initialiseMeasurementLayer: function () {
        //     let vm = this;

        //     // Measure tool
        //     let draw_source = new VectorSource({ wrapX: false });
        //     vm.drawForMeasure = new Draw({
        //         source: draw_source,
        //         type: 'LineString',
        //         style: vm.styleFunctionForMeasurement,
        //     });
        //     // Set a custom listener to the Measure tool
        //     vm.drawForMeasure.set('escKey', '');
        //     vm.drawForMeasure.on('change:escKey', function () {});
        //     vm.drawForMeasure.on('drawstart', function () {
        //         // Set measuring to true on mode change (fn `set_mode`), not drawstart
        //     });
        //     vm.drawForMeasure.on('drawend', function () {
        //         // Set measuring to false on mode change
        //     });

        //     // Create a layer to retain the measurement
        //     vm.measurementLayer = new VectorLayer({
        //         title: 'Measurement Layer',
        //         source: draw_source,
        //         style: function (feature, resolution) {
        //             feature.set('for_layer', true);
        //             return vm.styleFunctionForMeasurement(feature, resolution);
        //         },
        //     });
        //     vm.map.addInteraction(vm.drawForMeasure);
        //     vm.map.addLayer(vm.measurementLayer);
        // },
        initialiseQueryLayer: function () {
            let vm = this;

            vm.modelQuerySource = new VectorSource({});
            const style = new Style({
                fill: new Fill({
                    color: vm.defaultColor,
                }),
            });

            vm.modelQueryLayer = new VectorLayer({
                title: 'Model Occurrence Report',
                name: 'query_layer',
                source: vm.modelQuerySource,
                style: function (feature) {
                    const color = feature.get('color') || vm.defaultColor;
                    style.getFill().setColor(color);
                    return style;
                },
            });
            // Add the layer
            vm.map.addLayer(vm.modelQueryLayer);
            // Set zIndex to some layers to be rendered over the other layers
            vm.modelQueryLayer.setZIndex(10);
        },
        initialiseDrawLayer: function () {
            let vm = this;
            if (!vm.drawable) {
                return;
            }

            vm.drawForModel = new Draw({
                source: vm.modelQuerySource,
                type: 'Polygon',
                geometryFunction: function (coordinates, geometry) {
                    
                    if (geometry) {
                        if (coordinates[0].length) {
                            // Add a closing coordinate to match the first
                            geometry.setCoordinates(
                                [coordinates[0].concat([coordinates[0][0]])],
                                this.geometryLayout_
                            );
                        } else {
                            geometry.setCoordinates([], this.geometryLayout_);
                        }
                    } else {
                        geometry = new Polygon(
                            coordinates,
                            this.geometryLayout_
                            );
                        }
                    vm.sketchCoordinates = coordinates[0].slice();
                    if (
                        coordinates[0].length >
                        vm.sketchCoordinatesHistory.length
                    ) {
                        // Only reassign the sketchCoordinatesHistory if the new coordinates are longer than the previous
                        // so we don't lose the history when the user undoes a point
                        vm.sketchCoordinatesHistory = coordinates[0].slice();
                    }

                    return geometry;
                },
                condition: function (evt) {
                    if (evt.originalEvent.buttons === 1) {
                        // Only allow drawing when the left mouse button is pressed
                        return true;
                    } else if (evt.originalEvent.buttons === 2) {
                        // If the right mouse button is pressed, undo the last point
                        if (vm.showUndoButton) {
                            vm.undoLeaseLicensePoint();
                        } else {
                            vm.set_mode('layer');
                        }
                    } else {
                        return false;
                    }
                },
                finishCondition: function () {
                    if (vm.lastPoint) {
                        //vm.$emit('validate-feature');
                        vm.finishDrawing();
                    }
                    return false;
                },
            });
            vm.drawForModel.set('escKey', '');
            vm.drawForModel.on('change:escKey', function () {
                console.log('ESC key pressed');
            });
            vm.drawForModel.on('drawstart', function () {
                vm.errorMessage = null;
                vm.lastPoint = null;
            });
            vm.drawForModel.on('click'),
                function (evt) {
                    console.log(evt);
                };
            vm.drawForModel.on('drawend', function (evt) {
                console.log(evt);
                console.log(evt.feature.values_.geometry.flatCoordinates);
                // Priya I think context is the occurrencereport_obj thats sent through prop
                let model = vm.context || {};

                let color =
                    vm.featureColors['draw'] ||
                    vm.featureColors['unknown'] ||
                    vm.defaultColor;
                evt.feature.setProperties({
                    id: vm.newFeatureId,
                    model: model,
                    geometry_source: 'New',
                    name: model.id || -1,
                    // FIXME: Can this be standardised into the same field name?
                    label:
                        //TODO sure whta to set 
                        model.occurrence_report_number ||
                        // model.label ||
                        // model.application_type_name_display ||
                        // (model.application_type
                        //     ? model.application_type.name_display
                        //     : undefined) ||
                        'Draw',
                    color: color,
                    locked: false,
                });
                vm.newFeatureId++;
                console.log('newFeatureId = ' + vm.newFeatureId);
                vm.lastPoint = evt.feature;
                vm.sketchCoordinates = [[]];
                vm.sketchCoordinatesHistory = [[]];
                vm.getJSONFeatures();
            });
            vm.map.addInteraction(vm.drawForModel);
        },
        initialisePointerMoveEvent: function () {
            let vm = this;
            const hoverStyle = new Style({
                fill: vm.hoverFill,
                stroke: vm.hoverStroke,
            });
            // Cache the hover fill so we don't have to create a new one every time
            // Also prevent overwriting property `hoverFill` color
            let _hoverFill = null;
            function hoverSelect(feature) {
                const color = feature.get('color') || vm.defaultColor;
                _hoverFill = new Fill({ color: color });

                // If the feature is already selected, use the select stroke when hovering
                if (
                    vm.selectedFeatureIds.includes(feature.getProperties().id)
                ) {
                    hoverStyle.setFill(_hoverFill);
                    hoverStyle.setStroke(vm.clickSelectStroke);
                } else {
                    hoverStyle.setFill(vm.hoverFill);
                    hoverStyle.setStroke(vm.hoverStroke);
                }
                return hoverStyle;
            }

            let selected = null;
            vm.map.on('pointermove', function (evt) {
                if (vm.measuring || vm.drawing) {
                    // Don't highlight features when measuring or drawing
                    return;
                }
                if (selected !== null) {
                    if (
                        vm.selectedFeatureIds.includes(
                            selected.getProperties().id
                        )
                    ) {
                        // Don't alter style of click-selected features
                        console.log('ignoring hover on selected feature');
                    } else {
                        selected.setStyle(undefined);
                        selected.setStyle(
                            vm.createStyle(selected.values_.color)
                        );
                    }
                    selected = null;
                }
                vm.map.forEachFeatureAtPixel(
                    evt.pixel,
                    function (feature) {
                        selected = feature;
                        let model = selected.getProperties().model;
                        if (!model) {
                            console.error('No model found for feature');
                        } else {
                            model.geometry_source =
                                selected.getProperties().geometry_source;
                            model.copied_from =
                                selected.getProperties().copied_from;
                            model.area_sqm = selected.getProperties().area_sqm;
                        }
                        vm.selectedModel = model;
                        selected.setStyle(hoverSelect);

                        return true;
                    },
                    {
                        layerFilter: function (layer) {
                            return layer.get('name') === 'query_layer';
                        },
                    }
                );

                // Change to info cursor if hovering over an optional layer
                // let hit = vm.map.forEachLayerAtPixel(
                //     evt.pixel,
                //     function (layer) {
                //         layer.get('name'); //dbca_legislated_lands_and_waters
                //         let optional_layer_names = vm.optionalLayers.map(
                //             (layer) => {
                //                 return layer.get('name');
                //             }
                //         );

                //         if (vm.informing) {
                //             return optional_layer_names.includes(
                //                 layer.get('name')
                //             );
                //         }
                //         return false;
                //     }
                // );
                // vm.map.getTargetElement().style.cursor = hit
                //     ? 'help'
                //     : 'default';

                // if (selected) {
                //     vm.featureToast.show();
                // } else {
                //     vm.featureToast.hide();
                // }
            });
        },
        initialiseSingleClickEvent: function () {
            let vm = this;
            vm.map.on('singleclick', function (evt) {
                if (vm.drawing || vm.measuring) {
                    console.log(evt);
                    // TODO: must be a feature
                    vm.lastPoint = new Point(evt.coordinate);
                    return;
                }

                let feature = vm.map.forEachFeatureAtPixel(
                    evt.pixel,
                    function (feature) {
                        return feature;
                    }
                    );
                    if (feature) {
                    vm.map.getInteractions().forEach((interaction) => {
                        if (interaction instanceof Select) {
                            let selected = [];
                            let deselected = [];
                            let feature_id = feature.get('id');
                            if (vm.selectedFeatureIds.includes(feature_id)) {
                                // already selected, so deselect
                                deselected.push(feature);
                            } else {
                                // not selected, so select
                                selected.push(feature);
                            }
                            interaction.dispatchEvent({
                                type: 'select',
                                selected: selected,
                                deselected: deselected,
                            });
                        }
                    });
                }
            });
        },
        initialiseDoubleClickEvent: function () {
            let vm = this;
            vm.map.on('dblclick', function (evt) {
                vm.redirectingToModelDetails = true;
                evt.stopPropagation();

                let feature = vm.map.forEachFeatureAtPixel(
                    evt.pixel,
                    function (feature) {
                        return feature;
                    }
                );
                if (feature) {
                    let model = feature.getProperties().model;
                    if (!model) {
                        vm.redirectingToModelDetails = false;
                        return;
                    }

                    // TODO: Return path from serializer
                    let model_path = model.details_url;
                    // Remove trailing slash from urls
                    let pathnames = [
                        window.location.pathname,
                        model.details_url,
                    ];
                    for (let i = 0; i < pathnames.length; i++) {
                        let path_name = pathnames[i];
                        if (path_name[path_name.length - 1] === '/') {
                            path_name = path_name.slice(0, -1);
                        }
                        pathnames[i] = path_name;
                    }
                    // array remove duplicates
                    pathnames = [...new Set(pathnames)];
                    if (pathnames.length === 1) {
                        console.log('already on model details page');
                        vm.redirectingToModelDetails = false;
                    } else {
                        window.open(model_path, '_blank'); // Open in new tab
                        vm.redirectingToModelDetails = false;
                    }
                } else {
                    vm.redirectingToModelDetails = false;
                }
            });
        },
        initialiseSelectFeatureEvent: function () {
            let vm = this;
            if (!vm.selectable) {
                return;
            }

            const clickSelectStyle = new Style({
                fill: new Fill({
                    color: '#000000',
                }),
                stroke: vm.clickSelectStroke,
            });

            function clickSelect(feature) {
                // Keep feature fill color but change stroke color
                const color = feature.get('color') || vm.defaultColor;
                clickSelectStyle.getFill().setColor(color);
                return clickSelectStyle;
            }

            // select interaction working on "singleclick"
            const selectSingleClick = new Select({
                style: clickSelect,
                layers: [vm.modelQueryLayer],
            });
            vm.map.addInteraction(selectSingleClick);
            selectSingleClick.on('select', (evt) => {
                $.each(evt.selected, function (idx, feature) {
                    console.log(
                        `Selected feature ${feature.getProperties().id}`,
                        toRaw(feature)
                    );
                    feature.setStyle(clickSelect);
                    // priya added this if condition
                    if (
                        vm.selectedFeatureIds.includes(
                            feature.getProperties().id
                        )
                    ){
                        return;
                    }
                    else{
                        vm.selectedFeatureIds.push(feature.getProperties().id);
                    }
                });

                $.each(evt.deselected, function (idx, feature) {
                    console.log(
                        `Unselected feature ${feature.getProperties().id}`
                    );
                    feature.setStyle(undefined);
                    vm.selectedFeatureIds = vm.selectedFeatureIds.filter(
                        (id) => id != feature.getProperties().id
                    );
                });
            });
        },
        undoLeaseLicensePoint: function () {
            let vm = this;
            console.log(vm.drawForModel.sketchCoords_);
            if (vm.lastPoint) {
                vm.modelQuerySource.removeFeature(vm.lastPoint);
                vm.lastPoint = null;
                vm.sketchCoordinates = [[]];
                vm.sketchCoordinatesHistory = [[]];
                this.selectedFeatureId = null;
            } else {
                vm.drawForModel.removeLastPoint();
            }
        },
        redoLeaseLicensePoint: function () {
            let vm = this;
            if (
                vm.sketchCoordinatesHistory.length > vm.sketchCoordinates.length
            ) {
                let nextCoordinate = vm.sketchCoordinatesHistory.slice(
                    vm.sketchCoordinates.length,
                    vm.sketchCoordinates.length + 1
                );
                vm.drawForLeaselicence.appendCoordinates([nextCoordinate[0]]);
            }
        },
        removeModelFeatures: function () {
            let vm = this;
            let cannot_delete_features = [];
            const features = vm.modelQuerySource
                .getFeatures()
                .filter((feature) => {
                    if (
                        vm.selectedFeatureIds.includes(
                            feature.getProperties().id
                        )
                    ) {
                        if (feature.getProperties().locked === false) {
                            return feature;
                        } else {
                            console.warn(
                                `Cannot delete feature. ${
                                    feature.getProperties().id
                                } is locked`
                            );
                            cannot_delete_features.push(
                                feature.getProperties().id
                            );
                        }
                    }
                });

            if (cannot_delete_features.length > 0) {
                vm.errorMessageProperty(null);
                vm.errorMessageProperty(
                    `Cannot delete feature(s) ${cannot_delete_features.join(
                        ', '
                    )} anymore.`
                );
            }

            for (let feature of features) {
                vm.deletedFeaturesProperty(feature);
                vm.modelQuerySource.removeFeature(feature);
            }
            // Remove selected features (mapped by id) from `selectedFeatureIds`
            vm.selectedFeatureIds = vm.selectedFeatureIds.filter(
                (id) =>
                    !features
                        .map((feature) => feature.getProperties().id)
                        .includes(id)
            );
        },
        // fetchProposals: async function () {
        //     let vm = this;
        //     vm.fetchingProposals = true;
        //     let url = api_endpoints.proposal + 'list_for_map/';
        //     // Characters to concatenate pseudo url elements
        //     let chars = ['&', '&', '?'];

        //     if (vm.proposalIds.length > 0) {
        //         url +=
        //             `${chars.pop()}proposal_ids=` + vm.proposalIds.toString();
        //     }
        //     if (vm.filterApplicationsMapApplicationType != 'all') {
        //         url +=
        //             `${chars.pop()}application_type=` +
        //             vm.filterApplicationsMapApplicationType;
        //     }
        //     if (vm.filterApplicationsMapProcessingStatus != 'all') {
        //         url +=
        //             `${chars.pop()}processing_status=` +
        //             vm.filterApplicationsMapProcessingStatus;
        //     }
        //     fetch(url)
        //         .then(async (response) => {
        //             const data = await response.json();
        //             if (!response.ok) {
        //                 const error =
        //                     (data && data.message) || response.statusText;
        //                 console.log(error);
        //                 return Promise.reject(error);
        //             }
        //             vm.proposals = data;
        //             vm.filteredProposals = [...vm.proposals];
        //             let initialisers = [
        //                 vm.assignProposalFeatureColors(vm.proposals),
        //                 vm.loadFeatures(vm.proposals),
        //                 vm.applyFiltersFrontEnd(),
        //             ];
        //             Promise.all(initialisers).then(() => {
        //                 console.log(
        //                     'Done loading features and applying filters'
        //                 );
        //                 vm.fetchingProposals = false;
        //             });
        //         })
        //         .catch((error) => {
        //             console.error('There was an error!', error);
        //             vm.fetchingProposals = false;
        //         });
        // },
        
        addFeatureCollectionToMap: function (featureCollection) {
            let vm = this;
            if (featureCollection == null) {
                featureCollection = vm.featureCollection;
            }
            console.log('Adding features to map:', featureCollection);

            for (let featureData of featureCollection['features']) {
                let feature = vm.featureFromDict(
                    featureData,
                    featureData.model
                );

                vm.modelQuerySource.addFeature(feature);
                vm.newFeatureId++;
            }
        },
        // assignProposalFeatureColors: function (proposals) {
        //     let vm = this;
        //     proposals.forEach(function (proposal) {
        //         proposal.color = vm.getRandomRGBAColor();
        //         console.log(proposal.lodgement_date);
        //         console.log(typeof proposal.lodgement_date);
        //     });
        // },
        loadFeatures: function (proposals) {
            let vm = this;
            console.log(proposals);
            // Remove all features from the layer
            vm.modelQuerySource.clear();
            proposals.forEach(function (proposal) {
                proposal.proposalgeometry.features.forEach(
                    function (featureData) {
                        let feature = vm.featureFromDict(featureData, proposal);

                        if (
                            vm.modelQuerySource.getFeatureById(feature.getId())
                        ) {
                            console.warn(
                                `Feature ${feature.getId()} already exists in the source. Skipping...`
                            );
                            return;
                        }
                        vm.modelQuerySource.addFeature(feature);
                        vm.newFeatureId++;
                    }
                );
                if (proposal.competitive_process) {
                    proposal.competitive_process.competitive_process_geometries.features.forEach(
                        function (featureData) {
                            let feature = vm.featureFromDict(
                                featureData,
                                proposal.competitive_process
                            );
                            if (
                                vm.modelQuerySource.getFeatureById(
                                    feature.getId()
                                )
                            ) {
                                console.warn(
                                    `Feature ${feature.getId()} already exists in the source. Removing...`
                                );
                                vm.modelQuerySource.removeFeature(
                                    vm.modelQuerySource.getFeatureById(
                                        feature.getId()
                                    )
                                );
                            }
                            vm.modelQuerySource.addFeature(feature);
                            vm.newFeatureId++;
                        }
                    );
                }
            });
            vm.addFeatureCollectionToMap();
        },
        /**
         * Creates a styled feature object from a feature dictionary
         * @param {dict} featureData A feature dictionary
         * @param {Proxy} model A model object
         */
        featureFromDict: function (featureData, model) {
            let vm = this;
            if (model == null) {
                model = {};
            }

            let color = vm.styleByColor(featureData, model);
            let style = vm.createStyle(color);

            let feature = new Feature({
                id: vm.newFeatureId, // Incrementing-id of the polygon/feature on the map
                geometry: new Polygon(featureData.geometry.coordinates),
                name: model.id,
                label: model.label || model.application_type_name_display,
                color: color,
                source: featureData.properties.source,
                geometry_source: featureData.properties.geometry_source,
                locked: featureData.properties.locked,
                copied_from: featureData.properties.proposal_copied_from,
                area_sqm: featureData.properties.area_sqm,
            });
            // Id of the model object (https://datatracker.ietf.org/doc/html/rfc7946#section-3.2)
            feature.setId(featureData.id);

            feature.setProperties({
                model: model,
            });
            feature.setStyle(style);

            return feature;
        },
        getProposalById: function (id) {
            return this.proposals.find((proposal) => proposal.id === id);
        },
        getRandomColor: function () {
            let letters = '0123456789ABCDEF';
            let color = '#';
            for (let i = 0; i < 6; i++) {
                color += letters[Math.floor(Math.random() * 16)];
            }
            return color;
        },
        getRandomRGBAColor: function () {
            var o = Math.round,
                r = Math.random,
                s = 255;
            return [o(r() * s), o(r() * s), o(r() * s), 0.5];
        },
        //priya this function is used to get modelqueryjson to submit the geometry data in parent component
        getJSONFeatures: function () {
            const format = new GeoJSON();
            const features = this.modelQuerySource.getFeatures();
            features.forEach(function (feature) {
                console.log(feature.getProperties());
                // feature.unset("model")
            });

            return format.writeFeatures(features);
        },
        
        /**
         * Returns a Well-known-text (WKT) representation of a feature
         * @param {Feature} feature A feature to validate
         */
        featureToWKT: function (feature) {
            let vm = this;

            if (feature === undefined) {
                // If no feature is provided, create a feature from the current sketch
                let coordinates = vm.sketchCoordinates.slice();
                coordinates.push(coordinates[0]);
                feature = new Feature({
                    id: -1,
                    geometry: new Polygon([coordinates]),
                    label: 'validation',
                    color: vm.defaultColor,
                    geometry_source: 'validation',
                });
            }

            // Prepare a WFS feature intersection request
            let flatCoordinates = feature.values_.geometry.flatCoordinates;

            // Transform list of flat coordinates into a list of coordinate pairs,
            // e.g. ['x1 y1', 'x2 y2', 'x3 y3']
            let flatCoordinateStringPairs = flatCoordinates
                .map((coord, index) =>
                    index % 2 == 0
                        ? [
                              flatCoordinates[index],
                              flatCoordinates[index + 1],
                          ].join(' ')
                        : ''
                )
                .filter((item) => item != '');

            // Create a Well-Known-Text polygon string from the coordinate pairs
            return `POLYGON ((${flatCoordinateStringPairs.join(', ')}))`;
        },
        /**
         * Validates an openlayers feature against a geoserver `url`.
         * @param {Feature} feature A feature to validate
         * @returns {Promise} A promise that resolves to a list of intersected features
         */
        validateFeatureQuery: async function (query) {
            let vm = this;

            let features = [];
            // Query the WFS
            vm.queryingGeoserver = true;
            // var urls = [`${url}${params}`];
            let urls = [query];

            let requests = urls.map((url) =>
                utils.fetchUrl(url).then((response) => response)
            );
            await Promise.all(requests)
                .then((data) => {
                    features = new GeoJSON().readFeatures(data[0]);
                })
                .catch((error) => {
                    console.log(error.message);
                    vm.errorMessage = error.message;
                });

            return features;
        },
        /**
         * Finish drawing of the current feature sketch.
         */
        finishDrawing: function () {
            let vm = this;
            //vm.queryingGeoserver = false;
            vm.errorMessage = null;
            vm.drawForModel.finishDrawing();
        },
        /**
         * Returns the current error message or sets it to the provided message.
         * @param {String} message The new error message
         */
        errorMessageProperty: function (message) {
            let vm = this;
            if (message === undefined) {
                return vm.errorMessage;
            }

            vm.queryingGeoserver = false;

            // Only overwrite the current message if the new message is null (removes the message)
            // Or the current message is null (no message is set)
            if (message === null || vm.errorMessage === null) {
                vm.errorMessage = message;
            }
        },
        /**
         * Sets or unsets overlay feature information bubble
         * @param {Array} coordinate clicked coordinate pair
         * @param {Dict} feature clicked feature properties or undefined
         */
        overlay: function (coordinate, feature) {
            let vm = this;
            let overlay = vm.map.overlays_.array_[0];
            if (feature === undefined) {
                vm.overlayFeatureInfo = {};
            } else {
                vm.overlayFeatureInfo = feature.getProperties();
            }
            overlay.setPosition(coordinate);

            return overlay;
        },
        deletedFeaturesProperty: function (feature) {
            let vm = this;
            if (feature === undefined) {
                return vm.deletedFeatures;
            } else {
                vm.deletedFeatures.push(feature);
            }
        },
    //     validate_map_docs: function () {
    //         let vm = this;
    //         vm.isValidating = true;
    //         vm.errorString = '';
    //         const options = {
    //             method: 'POST',
    //             'content-type': 'application/json',
    //         };
    //         fetch(
    //             helpers.add_endpoint_json(
    //                 api_endpoints.proposals,
    //                 vm.context.id + '/validate_map_files'
    //             ),
    //             options
    //         )
    //             .then(async (response) => {
    //                 if (!response.ok) {
    //                     const text = await response.json();
    //                     throw new Error(text);
    //                 } else {
    //                     return response.json();
    //                 }
    //             })
    //             .then((data) => {
    //                 vm.$emit('refreshFromResponse', data);
    //                 // Once the shapefile is converted to a proposal geometry the files are deleted
    //                 // so calling this will remove the file list from the front end
    //                 vm.$refs.shapefile_document.get_documents();
    //                 vm.$nextTick(() => {
    //                     vm.loadFeatures([data]);
    //                     vm.displayAllFeatures();
    //                     swal.fire(
    //                         'Success',
    //                         'Shapefile processed successfully',
    //                         'success'
    //                     );
    //                 });
    //             })
    //             .catch((error) => {
    //                 console.log(error);
    //                 vm.errorString = helpers.apiVueResourceError(error);
    //                 swal.fire({
    //                     title: 'Validation',
    //                     text: error,
    //                     icon: 'error',
    //                 });
    //             })
    //             .finally(() => {
    //                 vm.isValidating = false;
    //             });
    //     },

        set_mode: function (mode) {
            let vm=this;
            // Toggle map mode on/off when the new mode is the old one
            if (this.mode == mode) {
                this.mode = 'layer';
            } else {
                this.mode = mode;
            }

            this.drawing = false;
            this.measuring = false;
            //this.informing = false;
            this.errorMessageProperty(null);
            this.overlay(undefined);
            this.map.getTargetElement().style.cursor = 'default';

            if (this.mode === 'layer') {
                //this.clearMeasurementLayer();
                vm.toggle_draw_measure_license.bind(this)(false, false);
            } else if (this.mode === 'draw') {
                //this.clearMeasurementLayer();
                this.sketchCoordinates = [[]];
                this.sketchCoordinatesHistory = [[]];
                vm.toggle_draw_measure_license(false, true);
                this.drawing = true;
            } else if (this.mode === 'measure') {
                vm.toggle_draw_measure_license.bind(this)(true, false);
                this.measuring = true;
            } else if (this.mode === 'info') {
                vm.toggle_draw_measure_license.bind(this)(false, false);
                this.informing = true;
            } else {
                console.error(`Cannot set mode ${mode}`);
            }
        },
        toggle_draw_measure_license: function (drawForMeasure, drawForModel) {
            if (this.drawForMeasure) {
                this.drawForMeasure.setActive(drawForMeasure);
            }
            if (this.drawForModel) {
                this.drawForModel.setActive(drawForModel);
            }
        },
    },
};
</script>
<style scoped>
@import '../../../../../static/boranga/css/map.css';

#featureToast {
    position: absolute;
    bottom: 10px;
    left: 10px;
}

.badge {
    position: absolute;
    z-index: 100;
    padding-left: 9px;
    padding-right: 9px;
    -webkit-border-radius: 9px;
    -moz-border-radius: 9px;
    border-radius: 9px;
}

.label-warning[href],
.badge-warning[href] {
    background-color: #c67605;
}

#selectedFeatureCount {
    font-size: 12px;
    background: #ff0000;
    color: #fff;
    padding: 0 5px;
    vertical-align: top;
    margin-left: -10px;
}
.map-spinner {
    position: absolute !important;
}

.shapefile-row {
    /* Works to make the Upload shapefile section fit neatly with the map
    haven't investigated why it's needed. */
    margin-left: 0px;
}
</style>
