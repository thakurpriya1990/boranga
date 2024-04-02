<template>
    <div>
        <div class="justify-content-end align-items-center mb-2">
            <div v-if="mapInfoText.length > 0" class="row">
                <div class="col-md-6">
                    <!-- <BootstrapAlert class="mb-0">
                        // eslint-disable vue/no-v-html
                        <p><span v-html="mapInfoText"></span></p>
                        //eslint-enable
                    </BootstrapAlert> -->
                    <alert type="info"
                        ><strong>
                            <!-- eslint-disable-next-line vue/no-v-html -->
                            <p><span v-html="mapInfoText"></span></p></strong
                    ></alert>
                </div>
                <div class="col-md-6">
                    <div class="row" style="margin: auto">
                        <alert
                            v-if="hasErrorMessage"
                            class="mb-1 ml-1"
                            type="danger"
                            icon="exclamation-triangle-fill"
                        >
                            <span> {{ errorMessage }} </span>
                        </alert>
                    </div>
                    <div class="row" style="margin: auto">
                        <alert
                            v-if="hasModifiedFeatures"
                            class="mb-0 ml-1"
                            type="warning"
                            icon="exclamation-triangle-fill"
                        >
                            <span>
                                Adding or modifying a feature will cause any
                                existing geospatial data to be re-evaluated on
                                save and possibly be changed.
                            </span>
                        </alert>
                    </div>
                </div>
            </div>
        </div>

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
                    <!-- <div style="position: relative">
                        <transition>
                            <div
                                class="optional-layers-button-wrapper"
                                :title="`There are ${optionalLayers.length} optional layers available}`"
                            >
                                <div
                                    class="optional-layers-button btn"
                                    :class="
                                        optionalLayers.length ? '' : 'disabled'
                                    "
                                    @mouseover="hover = true"
                                >
                                    <img src="../../assets/layers.svg" />
                                </div>
                            </div>
                        </transition>
                        <transition>
                            <div
                                v-show="hover"
                                div
                                class="layer_options layer_menu"
                                @mouseleave="hover = false"
                            >
                                <div
                                    v-for="layer in optionalLayers"
                                    :key="layer.ol_uid"
                                >
                                    <div
                                        class="row"
                                        :title="layer.values_.abstract"
                                    >
                                        <input
                                            :id="layer.ol_uid"
                                            type="checkbox"
                                            :checked="layer.values_.visible"
                                            class="layer_option col-md-1"
                                            @change="
                                                changeLayerVisibility(layer)
                                            "
                                        />
                                        <label
                                            :for="layer.ol_uid"
                                            class="layer_option col-md-6"
                                            >{{ layer.get('title') }}</label
                                        >
                                        <RangeSlider
                                            class="col-md-5"
                                            @value-changed="
                                                valueChanged($event, layer)
                                            "
                                        />
                                    </div>
                                </div>
                            </div>
                        </transition>
                    </div> -->
                    <!-- Toggle measure tool between active and not active -->
                    <div class="optional-layers-button-wrapper">
                        <div
                            :title="
                                mode == 'measure'
                                    ? 'Deactivate measure tool'
                                    : 'Measure distances on the map'
                            "
                            class="btn"
                            :class="[
                                mode == 'measure'
                                    ? 'optional-layers-button-active'
                                    : 'optional-layers-button',
                            ]"
                            @click="set_mode('measure')"
                        >
                            <img
                                class="svg-icon"
                                src="../../assets/ruler.svg"
                            />
                        </div>
                    </div>

                    <div
                        id="submenu-draw"
                        class="map-menu-submenu moved-menu-vertical"
                    >
                        <div class="scaled-button">
                            <div class="submenu-button-wrapper">
                                <div
                                    :title="
                                        mode == 'draw' && subMode == 'Polygon'
                                            ? 'Deactivate draw tool'
                                            : 'Draw a new polygon feature'
                                    "
                                    class="btn optional-layers-button"
                                    :class="[
                                        mode == 'draw' && subMode == 'Polygon'
                                            ? 'optional-layers-button-active'
                                            : 'optional-layers-button',
                                    ]"
                                    @click="set_mode('draw', 'Polygon')"
                                >
                                    <img
                                        class="svg-icon"
                                        src="../../assets/draw-polygon.svg"
                                    />
                                </div>
                            </div>
                            <div class="submenu-button-wrapper">
                                <div
                                    :title="
                                        mode == 'draw' && subMode == 'Point'
                                            ? 'Deactivate draw tool'
                                            : 'Draw new point features or edit selected points or polygon vertices'
                                    "
                                    class="btn optional-layers-button"
                                    :class="[
                                        mode == 'draw' && subMode == 'Point'
                                            ? 'optional-layers-button-active'
                                            : 'optional-layers-button',
                                    ]"
                                    @click="set_mode('draw', 'Point')"
                                >
                                    <img
                                        class="svg-icon"
                                        src="../../assets/draw-points.svg"
                                    />
                                </div>
                            </div>
                        </div>
                    </div>

                    <div v-if="drawable" class="optional-layers-button-wrapper">
                        <div
                            :title="
                                mode == 'draw'
                                    ? 'Drawing mode active'
                                    : 'Select a drawing mode'
                            "
                            class="btn optional-layers-button"
                            :class="[
                                mode == 'draw'
                                    ? 'optional-layers-button-active'
                                    : 'optional-layers-button',
                            ]"
                            @click="toggleElementVisibility('submenu-draw')"
                        >
                            <img
                                class="svg-icon"
                                src="../../assets/pen-icon.svg"
                            />
                        </div>
                    </div>
                    <div
                        v-if="editable"
                        class="optional-layers-button-wrapper"
                        title="Transform a drawn feature"
                    >
                        <div
                            :title="
                                mode == 'transform'
                                    ? 'Deactivate transform tool'
                                    : 'Transform an existing feature'
                            "
                            class="btn"
                            :class="[
                                mode == 'transform'
                                    ? 'optional-layers-button-active'
                                    : 'optional-layers-button',
                                drawable && polygonCount ? '' : 'disabled',
                            ]"
                            @click="set_mode('transform')"
                        >
                            <img
                                class="svg-icon"
                                src="../../assets/transform-polygon.svg"
                            />
                        </div>
                    </div>
                    <div class="optional-layers-button-wrapper">
                        <div
                            title="Zoom map to layer(s)"
                            class="optional-layers-button btn"
                            :class="polygonCount ? '' : 'disabled'"
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
                            class="optional-layers-button btn"
                            @click="geoJsonButtonClicked"
                        >
                            <img
                                class="svg-icon"
                                src="../../assets/download.svg"
                            />
                        </div>
                    </div>
                    <div
                        v-if="editable"
                        class="optional-layers-button-wrapper"
                        :title="
                            polygonCount
                                ? 'Select a feature to delete'
                                : 'No features to delete'
                        "
                    >
                        <div
                            class="optional-layers-button btn"
                            :class="[
                                selectedFeatureIds.length == 0
                                    ? 'disabled'
                                    : 'btn-danger',
                                navbarButtonsDisabled ? 'disabled' : '',
                            ]"
                            title="Delete selected features"
                            @click="removeModelFeatures()"
                        >
                            <img
                                class="svg-icon"
                                src="../../assets/trash-bin.svg"
                            />
                            <span
                                v-if="selectedFeatureIds.length"
                                id="selectedFeatureCount"
                                class="badge badge-warning"
                                >{{ selectedFeatureIds.length }}</span
                            >
                        </div>
                    </div>
                    <div
                        v-if="canUndoAction || canUndoDrawnVertex"
                        class="optional-layers-button-wrapper"
                        title="Undo last action"
                    >
                        <div
                            class="optional-layers-button btn"
                            :class="[
                                (mode !== 'draw' && hasUndo) ||
                                (mode === 'draw' && canUndoDrawnVertex)
                                    ? ''
                                    : 'disabled',
                                navbarButtonsDisabled ? 'disabled' : '',
                            ]"
                            :title="
                                'Undo ' +
                                (canUndoDrawnVertex
                                    ? 'last point'
                                    : undoRedoStackTopInteractionName('undo'))
                            "
                            @click="undo()"
                        >
                            <img
                                class="svg-icon"
                                src="../../assets/map-undo.svg"
                            />
                        </div>
                    </div>
                    <div
                        v-if="canRedoAction || canRedoDrawnVertex"
                        class="optional-layers-button-wrapper"
                        title="Redo last action"
                    >
                        <div
                            class="optional-layers-button btn"
                            :class="[
                                (mode !== 'draw' && hasRedo) ||
                                (mode === 'draw' && canRedoDrawnVertex)
                                    ? ''
                                    : 'disabled',
                                navbarButtonsDisabled ? 'disabled' : '',
                            ]"
                            :title="
                                'Redo ' +
                                (canRedoDrawnVertex
                                    ? 'last point'
                                    : undoRedoStackTopInteractionName('redo'))
                            "
                            @click="redo()"
                        >
                            <img
                                class="svg-icon"
                                src="../../assets/map-redo.svg"
                            />
                        </div>
                    </div>
                    <div
                        v-if="optionalLayersActive"
                        class="optional-layers-button-wrapper"
                    >
                        <div
                            :title="
                                mode == 'info'
                                    ? 'Deactivate info tool'
                                    : 'Click a data set feature for more information'
                            "
                            class="btn"
                            :class="[
                                mode == 'info'
                                    ? 'optional-layers-button-active'
                                    : 'optional-layers-button',
                            ]"
                            @click="set_mode('info')"
                        >
                            <img
                                class="svg-icon"
                                src="../../assets/info-query.svg"
                            />
                        </div>
                    </div>
                </div>

                <div id="featureToast" class="toast" style="z-index: 9999">
                    <template v-if="selectedModel">
                        <div class="toast-header">
                            <img src="" class="rounded me-2" alt="" />
                            <!-- FIXME: Can this be standardised into the same field name? -->
                            <strong class="me-auto">
                                {{ selectedModel.label }}:
                                {{ selectedModel.occurrence_report_number }}
                            </strong>
                        </div>
                        <div class="toast-body">
                            <table class="table table-sm">
                                <tbody>
                                    <tr>
                                        <th scope="row">Processing Status</th>
                                        <!-- FIXME: Can this be standardised into the same field name? -->
                                        <td>
                                            {{
                                                selectedModel.status ||
                                                selectedModel.status_display ||
                                                selectedModel.processing_status_display ||
                                                selectedModel.processing_status
                                            }}
                                        </td>
                                    </tr>
                                    <!-- TODO: `created_at` is not formatted to DD/MM/YYYY -->
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
                                            Occurrence (original report)
                                        </th>
                                        <th v-else scope="row">
                                            Lodgement Date
                                        </th>
                                        <!-- FIXME: Can this be standardised into the same field name? -->
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
                                            <th scope="row">Area (ha)</th>
                                            <td>
                                                {{
                                                    (
                                                        selectedModel.area_sqm /
                                                        10000
                                                    ).toFixed(1)
                                                }}
                                            </td>
                                        </template>
                                        <template v-else>
                                            <th scope="row">Area (m&#178;)</th>
                                            <td>
                                                {{
                                                    Math.round(
                                                        selectedModel.area_sqm
                                                    )
                                                }}
                                            </td>
                                        </template>
                                    </tr>
                                </tbody>
                            </table>
                        </div>
                    </template>
                </div>

                <!-- Overlay popup bubble when clicking a DBCA layer feature -->
                <!-- <div id="popup" class="ol-popup overlay-feature-popup">
                    <template v-if="overlayFeatureInfo">
                        <div class="toast-header">
                            <img src="" class="rounded me-2" alt="" />
                            <strong class="me-auto">{{
                                overlayFeatureInfo.leg_name
                            }}</strong>
                            <button
                                type="button"
                                class="btn btn-sm btn-light text-nowrap"
                                aria-label="Close Overlay"
                                @click="overlay(undefined)"
                            >
                                <span style="font-size: smaller"
                                    ><i
                                        class="fa-fw fa-regular fa-window-close"
                                    ></i>
                                    Close</span
                                >
                            </button>
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
                                    <tr>
                                        <th scope="row">Area (ha)</th>
                                        <td>
                                            {{
                                                (
                                                    overlayFeatureInfo.leg_poly_area +
                                                    Number.EPSILON
                                                ).toFixed(1)
                                            }}
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
        <div v-if="debug" class="row">
            <div class="col-sm-6">Undo Stack:</div>
            <div class="col-sm-6">Redo Stack:</div>
            <div class="col-sm-6">
                <div v-for="(item, idx) in undoStack" :key="idx">
                    <div>{{ idx }} {{ item.type }}</div>
                </div>
            </div>
            <div class="col-sm-6">
                <div v-for="(item, idx) in redoStack" :key="idx">
                    <div>{{ idx }} {{ item.type }}</div>
                </div>
            </div>
        </div>
        <!-- If no context provided, e.g. no proposal or cp, don't allow for shapefile upload -->
        <div v-if="context" class="row shapefile-row">
            <div class="col-sm-6 border p-2">
                <div class="row mb-2">
                    <div class="col">
                        <label for="shapefile_document" class="fw-bold"
                            >Upload Shapefile or archive(s) containing
                            shapefiles
                            <span>({{ archiveTypesAllowed.join(', ') }})</span>
                        </label>
                    </div>
                    <div class="col">
                        <FileField
                            id="shapefile_document_document"
                            ref="shapefile_document"
                            :readonly="false"
                            name="shapefile_document"
                            :multiple="true"
                            :is-repeatable="true"
                            :document-action-url="shapefileDocumentUrl"
                            :replace_button_by_text="true"
                            :file-types="
                                shapefileTypesAllowed
                                    .concat(archiveTypesAllowed)
                                    .join(', ')
                            "
                            :text_string="`Attach Files ${shapefileTypesAllowed.join(
                                ', '
                            )} or ${archiveTypesAllowed.join(', ')}`"
                            @update-parent="shapeFilesUpdated"
                        />
                    </div>
                </div>
                <div
                    v-if="
                        !uploadedFileTypes.includes('.zip') &&
                        !uploadedFileTypes.includes('.prj')
                    "
                    class="row"
                >
                    <div class="col">
                        <!-- <BootstrapAlert> -->
                        <alert
                            >If you do not upload a .prj file, we will use
                            <a
                                href="https://en.wikipedia.org/wiki/World_Geodetic_System#WGS84"
                                target="_blank"
                                >WGS 84</a
                            >
                            / 'EPSG:4326'
                        </alert>
                        <!-- </BootstrapAlert> -->
                    </div>
                </div>
                <div v-if="hasUploadedShapefiles" class="row">
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
                            :class="uploadedFilesComplete ? '' : 'disabled'"
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
        </div>
    </div>
</template>

<script>
import { v4 as uuid } from 'uuid';
import { api_endpoints, helpers } from '@/utils/hooks';

import { toRaw } from 'vue';
import 'ol/ol.css';
import alert from '@vue-utils/alert.vue';
import Map from 'ol/Map';
import View from 'ol/View';
import TileLayer from 'ol/layer/Tile';
import TileWMS from 'ol/source/TileWMS';
import { Draw, Select, Snap } from 'ol/interaction';
import ModifyFeature from 'ol-ext/interaction/ModifyFeature';
import UndoRedo from 'ol-ext/interaction/UndoRedo';
import Transform from 'ol-ext/interaction/Transform';
import Feature from 'ol/Feature';
import VectorLayer from 'ol/layer/Vector';
import VectorSource from 'ol/source/Vector';
import { Circle as CircleStyle, Fill, Stroke, Style } from 'ol/style';
import { FullScreen as FullScreenControl } from 'ol/control';
import { LineString, Point, MultiPoint, Polygon } from 'ol/geom';
import { getArea } from 'ol/sphere.js';
import GeoJSON from 'ol/format/GeoJSON';
import Overlay from 'ol/Overlay.js';
import DragAndDrop from 'ol/interaction/DragAndDrop.js';
import MeasureStyles, { formatLength } from '@/components/common/measure.js';
//import RangeSlider from '@/components/forms/range_slider.vue';
import FileField from '@/components/forms/filefield_immediate.vue';
import {
    // addOptionalLayers,
    set_mode,
    baselayer_name,
    // validateFeature,
    layerAtEventPixel,
} from '@/components/common/map_functions.js';
import shp from 'shpjs';

export default {
    name: 'MapComponent',
    components: {
        FileField,
        alert,
        //RangeSlider,
    },
    props: {
        level: {
            type: String,
            required: true,
            validator: function (val) {
                let options = ['internal', 'referral', 'external'];
                return options.indexOf(val) != -1 ? true : false;
            },
        },
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
         * Whether to enable drawing of new features
         */
        drawable: {
            type: Boolean,
            required: false,
            default: false,
        },
        /**
         * Whether to enable editing of existing features (e.g. select for deletion or transformation)
         */
        editable: {
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
        /**
         * Tolerance for considering the pointer close enough to a segment or vertex for editing
         * See: https://openlayers.org/en/latest/apidoc/module-ol_interaction_Modify-Modify.html
         */
        pixelTolerance: {
            type: Number,
            required: false,
            default: 5,
        },
        /**
         * Consider features within some distance of a provided pixel
         * See: https://openlayers.org/en/latest/examples/hit-tolerance.html
         */
        hitTolerance: {
            type: Number,
            required: false,
            default: 4,
        },
        /**
         * The maximum length of the undo/redo stacks
         */
        undoStackMaxLength: {
            type: Number,
            required: false,
            default: 0, // 0 means no limit
        },
        navbarButtonsDisabled: {
            type: Boolean,
            required: false,
            default: false,
        },
    },
    // emits: ['filter-appied', 'validate-feature', 'refreshFromResponse'],
    emits: ['validate-feature', 'refreshFromResponse'],
    data() {
        // eslint-disable-next-line no-unused-vars
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
            subMode: null,
            drawForMeasure: null,
            drawPolygonsForModel: null, // Polygon Draw interaction
            drawPointsForModel: null, // Points Draw interaction
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
            modelQuerySource: null,
            modelQueryLayer: null,
            selectedFeatureIds: [],
            lastPoint: null,
            sketchCoordinates: [[]],
            defaultColor: '#eeeeee',
            clickSelectStroke: new Stroke({
                color: 'rgba(255, 0, 0, 0.7)',
                width: 2,
            }),
            hoverFill: new Fill({
                color: 'rgba(255, 255, 255, 0.5)',
            }),
            hoverStrokePolygon: new Stroke({
                color: 'rgba(255, 255, 255, 0.5)',
                width: 1,
            }),
            hoverStrokePoint: new Stroke({
                color: 'rgba(255, 255, 255, 0.5)',
                width: 2,
            }),
            set_mode: set_mode,
            isValidating: false,
            errorMessage: null,
            overlayFeatureInfo: {},
            deletedFeatures: [], // keep track of deleted features
            undoredo: null,
            undoredo_forSketch: null, // Undo/redo stack for the sketch layer
            unOrRedoing_sketchPoint: false, // Whether currently undoing or redoing a sketch point
            modifiedFeaturesStack: [], // A stack of only those undoable actions that modified a feature
            drawing: false, // Whether the map is in draw (pencil icon) mode
            transforming: false, // Whether the map is in transform (resize, scale, rotate) mode
            numShapefiles: 0,
            uploadedFileTypes: [], // The currently uploaded types
            archiveTypesAllowed: ['.zip'], // The allowed archive types
            shapefileTypesAllowed: ['.shp', '.dbf', '.prj', '.shx'], // The allowed shapefile types
            shapefileTypesRequired: ['.shp', '.dbf', '.shx'], // The required shapefile types
        };
    },
    computed: {
        shapefileDocumentUrl: function () {
            let endpoint = '';
            let obj_id = 0;
            // if (this.context?.model_name == 'proposal') {
            //     endpoint = api_endpoints.proposal;
            //     obj_id = this.context.id;
            // } else if (this.context?.model_name == 'competitiveprocess') {
            //     endpoint = api_endpoints.competitive_process;
            //     obj_id = this.context.id;
            // }
            if (this.context?.model_name == 'occurrencereport') {
                endpoint = api_endpoints.occurrence_report;
                obj_id = this.context.id;
            } else {
                console.warn('shapefileDocumentUrl: invalid context');
                return ''; // Should not reach here.
            }
            let url = helpers.add_endpoint_join(
                endpoint,
                '/' + obj_id + '/process_shapefile_document/'
            );
            console.log({ url });
            return url;
        },
        canUndoAction: function () {
            // The ol-ext undo/redo module states it is still experimental, might want to disable undo/redo at all
            return true;
        },
        canRedoAction: function () {
            // The ol-ext undo/redo module states it is still experimental, might want to disable undo/redo at all
            return true;
        },
        canUndoDrawnVertex: function () {
            this.sketchCoordinates || this.unOrRedoing_sketchPoint; // Mentioned here to force update of the computed property
            return (
                this.mode == 'draw' &&
                !this.unOrRedoing_sketchPoint &&
                this.drawPolygonsForModel &&
                this.drawPolygonsForModel.getActive() &&
                this.undoredo_forSketch.getStack('undo').length > 0
            );
        },
        canRedoDrawnVertex: function () {
            this.sketchCoordinates || this.unOrRedoing_sketchPoint; // Mentioned here to force update of the computed property
            return (
                this.mode == 'draw' &&
                !this.unOrRedoing_sketchPoint &&
                this.drawPolygonsForModel &&
                this.drawPolygonsForModel.getActive() &&
                this.undoredo_forSketch.getStack('redo').length > 0
            );
        },
        optionalLayersActive: function () {
            if (this.optionalLayers.length == 0) {
                return false;
            }
            let visible_layers = this.optionalLayers.filter(
                (layer) => layer.values_.visible === true
            );
            return visible_layers.length > 0;
        },
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
        hasModifiedFeatures: function () {
            let vm = this;
            return vm.modifiedFeaturesStack.length > 0;
        },
        debug: function () {
            if (this.$route.query.debug) {
                return this.$route.query.debug === 'true';
            }
            return false;
        },
        /**
         * Returns the stack of undoable actions
         */
        undoStack: function () {
            let vm = this;
            if (!vm.undoredo_forSketch) {
                return [];
            } else {
                return vm.undoredo_forSketch.getStack('undo');
            }
        },
        /**
         * Returns the stack of undoable actions
         */
        redoStack: function () {
            let vm = this;
            if (!vm.undoredo_forSketch) {
                return [];
            } else {
                return vm.undoredo_forSketch.getStack('redo');
            }
        },
        hasUndo: function () {
            let vm = this;
            if (!vm.undoredo) {
                return false;
            } else {
                vm.modifiedFeaturesStack; // Mentioned here to force update of the computed property
                let stack = vm.undoredo.getStack('undo');
                return stack.length > 0;
            }
        },
        hasRedo: function () {
            let vm = this;
            if (!vm.undoredo) {
                return false;
            } else {
                vm.modifiedFeaturesStack; // Mentioned here to force update of the computed property
                let stack = vm.undoredo.getStack('redo');
                return stack.length > 0;
            }
        },
        hasUploadedShapefiles: function () {
            return this.numShapefiles;
        },
        csrf_token: function () {
            return helpers.getCookie('csrftoken');
        },
        /**
         * Returns whether the uploaded files are either only shapefiles or only archives
         */
        uploadedFilesComplete: function () {
            // The uploaded files contain archives
            const containsArchiveTypes = this.archiveTypesAllowed.some((type) =>
                this.uploadedFileTypes.includes(type)
            );
            // Every uploaded file is an archive
            const archiveTypesComplete = this.uploadedFileTypes.every((type) =>
                this.archiveTypesAllowed.includes(type)
            );
            // The uploaded files contain shapefiles
            const containsShapefileTypes = this.shapefileTypesAllowed.some(
                (type) => this.uploadedFileTypes.includes(type)
            );
            // Every required shapefile type is uploaded
            const shapefileTypesComplete = this.shapefileTypesRequired.every(
                (type) => this.uploadedFileTypes.includes(type)
            );

            // Either every uploaded file is an archive or
            // every required shapefile type is uploaded but not both
            return (
                (archiveTypesComplete && !containsShapefileTypes) ||
                (shapefileTypesComplete && !containsArchiveTypes)
            );
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
        this.fetchProposals();
    },
    mounted: function () {
        console.log('mounted()');
        let vm = this;
        vm.loadingMap = true;

        this.$nextTick(() => {
            var toastEl = document.getElementById('featureToast');
            $('#map-spinner').children().css('position', 'static'); // Position spinner in center of map
            vm.initialiseMap();
            vm.set_mode('layer');
            vm.setBaseLayer('osm');
            // addOptionalLayers(this);
            vm.featureToast = new bootstrap.Toast(toastEl, { autohide: false });
            if (vm.refreshMapOnMounted) {
                vm.forceToRefreshMap();
            } else {
                console.log('Done initializing map (no refresh)');
                vm.loadingMap = false;
            }
            // Priya calling this event from mounted as its only been triggered from loadFeatures() which is coomented at the moment
            // vm.map.dispatchEvent({
            //     type: 'features-loaded',
            //     details: {
            //         loaded: true,
            //     },
            // });
        });
    },
    methods: {
        /**
         * Returns the euclidean distance between two pixel coordinates
         * @param {Array} p1 a pixel coordinate pair in the form [x1, y1]
         * @param {Array} p2 a pixel coordinate pair in the form [x2, y2]
         */
        pixelDistance(p1, p2) {
            return Math.sqrt(
                Math.pow(p1[0] - p2[0], 2) + Math.pow(p1[1] - p2[1], 2)
            );
        },
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
            vm.download_content(json, 'boranga_layers.geojson', 'text/plain');
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
        clearMeasurementLayer: function () {
            let vm = this;
            let features = vm.measurementLayer.getSource().getFeatures();
            features.forEach((feature) => {
                vm.measurementLayer.getSource().removeFeature(feature);
            });
        },
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
            let s = this.createStyle('#3399cc', '#3399cc', 'Point', 2);
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
        styleByColor: function (featureData, model, geometry_source = null) {
            let vm = this;
            if (!geometry_source) {
                geometry_source =
                    featureData.properties.geometry_source?.toLowerCase() ||
                    'draw';
            }

            if (vm.styleBy === 'assessor') {
                // Assume the object is a feature containing a geometry_source property
                return vm.featureColors[geometry_source];
            } else if (vm.styleBy === 'model') {
                // Assume the object is a model containing a color field
                return model.color;
            } else {
                return vm.featureColors['unknown'] || vm.defaultColor;
            }
        },
        /**
         * Returns a style based on feature type. Defaults to a polygon style
         * @param {string|object} fill The fill color or a Fill object
         * @param {string=|object=} stroke The stroke color or a Stroke object
         * @param {string=} type The feature type
         * @param {number=} radius The radius of the point circle, defaults to 7
         * @param {number=} width The stroke width, defaults to 2
         */
        createStyle: function (
            fill,
            stroke = null,
            type = null,
            radius = 7,
            width = 2
        ) {
            let vm = this;
            if (!fill) {
                fill = vm.defaultColor;
            }
            if (!stroke) {
                stroke = vm.defaultColor;
            }
            if (!(fill instanceof Fill)) {
                // TODO: check is color
                fill = new Fill({ color: fill });
            }
            if (!(stroke instanceof Stroke)) {
                // TODO: check is color
                stroke = new Stroke({
                    color: stroke,
                    width: width,
                });
            }

            if (['MultiPolygon', 'Polygon', null].includes(type)) {
                return new Style({
                    stroke: stroke,
                    fill: fill,
                });
            } else if (type === 'LineString') {
                return new Style({
                    stroke: stroke,
                });
            } else if (type === 'Point') {
                return new Style({
                    image: new CircleStyle({
                        radius: radius,
                        stroke: stroke,
                        fill: fill,
                    }),
                });
            } else {
                console.error('Unknown feature type: ' + type);
            }
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
        setStyleForUnAndSelectedFeatures: function (style) {
            let vm = this;
            if (style === undefined) {
                if (this.mode == 'draw') {
                    style = vm.modifySelectStyle;
                } else {
                    style = vm.basicSelectStyle;
                }
            }
            let features = vm.modelQuerySource.getFeatures();
            features.forEach((feature) => {
                if (
                    vm.selectedFeatureIds.includes(feature.getProperties().id)
                ) {
                    feature.setStyle(style);
                } else {
                    feature.setStyle(undefined);
                }
            });
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

            vm.initialiseMeasurementLayer();
            vm.initialiseQueryLayer();
            vm.initialiseDrawLayer();

            // update map extent when new features added
            vm.map.on('rendercomplete', vm.displayAllFeatures());
            vm.map.on('features-loaded', function (evt) {
                if (evt.details.loaded == true) {
                    // Add undo/redo AFTER proposal geometries have been added to the map
                    vm.undoredo = new UndoRedo({
                        layers: [vm.modelQueryLayer],
                    });
                    vm.undoredo.clear();

                    // Somehow passing the parameter has no effect, so we set it here
                    vm.undoredo.setMaxLength(vm.undoStackMaxLength);
                    // Define a custom undo/redo for selected features
                    vm.undoredo.define(
                        'select feature',
                        function (s) {
                            // Undo fn: set to the previous id list and styles
                            console.log('undo selected', s.before, s.after);
                            vm.selectedFeatureIds = s.before;
                            vm.setStyleForUnAndSelectedFeatures();
                        },
                        function (s) {
                            // Redo fn: reset the ids list and styles
                            console.log('redo selected', s.before, s.after);
                            vm.selectedFeatureIds = s.after;
                            vm.setStyleForUnAndSelectedFeatures();
                        }
                    );

                    // Setup a dedicated undo/redo for sketch points on the draw layer
                    vm.undoredo_forSketch = new UndoRedo({
                        layers: [vm.modelQueryLayer],
                    });
                    vm.undoredo_forSketch.clear();

                    vm.undoredo_forSketch.setMaxLength(vm.undoStackMaxLength);
                    vm.undoredo_forSketch.define(
                        'add polygon point',
                        function (s) {
                            // Undo fn: set to the previous sketch coordinates
                            vm.unOrRedoing_sketchPoint = true;
                            vm.sketchCoordinates = s.before;
                            vm.undoLeaseLicensePoint();
                            vm.unOrRedoing_sketchPoint = false;
                        },
                        function (s) {
                            // Redo fn: reset the sketch coordinates
                            vm.unOrRedoing_sketchPoint = true;
                            vm.sketchCoordinates = s.after;
                            vm.redoLeaseLicensePoint();
                            vm.unOrRedoing_sketchPoint = false;
                        }
                    );

                    for (let eventName of ['stack:add', 'stack:remove']) {
                        vm.undoredo.addEventListener(eventName, function () {
                            let undo_stack = vm.undoredo.getStack('undo');

                            let stack = undo_stack.filter((item) => {
                                // Filter out the actions that modify an existing or add a feature
                                return (
                                    (['addfeature'].includes(item.type) &&
                                        item.feature.getProperties()
                                            .geometry_source === 'New') ||
                                    ['translate', 'rotate', 'scale'].includes(
                                        item.name
                                    )
                                );
                            });

                            vm.modifiedFeaturesStack = Object.assign(stack, {});
                        });
                    }

                    vm.map.addInteraction(vm.undoredo);
                    vm.map.addInteraction(vm.undoredo_forSketch);
                }
            });

            vm.initialisePointerMoveEvent();
            vm.snap = new Snap({ source: vm.modelQuerySource });
            vm.dragAndDrop = new DragAndDrop({
                projection: 'EPSG:4326',
                formatConstructors: [GeoJSON],
            });
            vm.dragAndDrop.on('addfeatures', function (event) {
                console.log('dragAndDrop addfeatures', event);
                let features = event.features;
                let source = vm.modelQuerySource;
                for (let i = 0, ii = features.length; i < ii; i++) {
                    let feature = features[i];
                    let color = vm.styleByColor(feature, vm.context, 'draw');
                    let style = vm.createStyle(
                        color,
                        null,
                        feature.getGeometry().getType()
                    );

                    const properties = {
                        id: vm.newFeatureId, // Incrementing-id of the polygon/feature on the map
                        model: vm.context,
                        name: vm.context.id,
                        label: vm.context.label,
                        color: color,
                        geometry_source: 'New',
                        locked: false,
                        copied_from: null,
                        area_sqm: vm.featureArea(feature),
                    };

                    feature.setProperties(properties);
                    feature.setStyle(style);
                    source.addFeature(feature);
                    vm.newFeatureId++;
                }
            });

            let extent_interactions = [vm.snap, vm.dragAndDrop];
            if (vm.editable) {
                // Only add these interactions if polygons are editable
                vm.select = vm.initialiseSelectFeatureEvent();
                vm.modify = vm.initialiseModifyFeatureEvent();
                vm.transform = vm.initialiseTransform();
                extent_interactions.push(vm.select, vm.modify, vm.transform);
            }

            vm.map.getInteractions().extend(extent_interactions);

            vm.modifySetActive(false);

            vm.initialiseSingleClickEvent();
            vm.initialiseDoubleClickEvent();

            // Custom drag and drop
            vm.map.getViewport().addEventListener('dragover', function (evt) {
                evt.preventDefault();
                for (let i = 0; i < evt.dataTransfer.items.length; i++) {
                    console.log(
                        'drag: dragover',
                        evt.dataTransfer.items[i].type
                    );
                }
            });
            vm.map.getViewport().addEventListener('drop', function (evt) {
                console.log('drag: drop', evt);
                // Prevent default behavior (Prevent file from being opened)
                evt.preventDefault();

                // TODO: Handle drop of shapefile zips, see: loadshp package, or https://www.npmjs.com/package/shape2json
                // TODO: Make this a function
                // TODO: See if addFeatureCollectionToMap can be used for drag&drop of geojson files (search for dragAndDrop addfeatures)
                shp;
                const files = evt.dataTransfer.files[0];
                files;
                if (evt.dataTransfer.items) {
                    // Use DataTransferItemList interface to access the file(s)
                    [...evt.dataTransfer.items].forEach(async (item, i) => {
                        // If dropped items aren't files, reject them
                        if (item.kind === 'file') {
                            const file = item.getAsFile();
                            console.log(`… file[${i}].name = ${file.name}`);
                            await file.arrayBuffer().then(async (buffer) => {
                                await shp(buffer).then(function (geojson) {
                                    console.log(geojson);
                                    vm.addFeatureCollectionToMap(geojson);
                                });
                            });
                        }
                    });
                } else {
                    // Use DataTransfer interface to access the file(s)
                    [...evt.dataTransfer.files].forEach((file, i) => {
                        console.log(`… file[${i}].name = ${file.name}`);
                    });
                }
            });
        },
        initialiseMeasurementLayer: function () {
            let vm = this;

            // Measure tool
            let draw_source = new VectorSource({ wrapX: false });
            vm.drawForMeasure = new Draw({
                source: draw_source,
                type: 'LineString',
                style: vm.styleFunctionForMeasurement,
            });
            // Set a custom listener to the Measure tool
            vm.drawForMeasure.set('escKey', '');
            vm.drawForMeasure.on('change:escKey', function () {});
            vm.drawForMeasure.on('drawstart', function () {
                // Set measuring to true on mode change (fn `set_mode`), not drawstart
            });
            vm.drawForMeasure.on('drawend', function () {
                // Set measuring to false on mode change
            });

            // Create a layer to retain the measurement
            vm.measurementLayer = new VectorLayer({
                title: 'Measurement Layer',
                source: draw_source,
                style: function (feature, resolution) {
                    feature.set('for_layer', true);
                    return vm.styleFunctionForMeasurement(feature, resolution);
                },
            });
            vm.map.addInteraction(vm.drawForMeasure);
            vm.map.addLayer(vm.measurementLayer);
        },
        initialiseQueryLayer: function () {
            let vm = this;

            vm.modelQuerySource = new VectorSource({});
            const polygonStyle = vm.createStyle(null, null, 'Polygon');
            const pointStyle = vm.createStyle(null, null, 'Point');

            vm.modelQueryLayer = new VectorLayer({
                title: 'Model Occurrence Report',
                name: 'query_layer',
                source: vm.modelQuerySource,
                style: function (feature) {
                    const color = feature.get('color') || vm.defaultColor;
                    let style = polygonStyle;
                    if (feature.getGeometry().getType() === 'Polygon') {
                        style.getFill().setColor(color);
                    } else if (feature.getGeometry().getType() === 'Point') {
                        style = pointStyle;
                        style.getImage().getFill().setColor(color);
                        style.getImage().getStroke().setColor(color);
                    }
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

            vm.drawPolygonsForModel = new Draw({
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

                    if (vm.unOrRedoing_sketchPoint) {
                        // Don't run below undo stack logic while executing an undo/redo of sketch points
                        return geometry;
                    }

                    // Current feature id list for undo stack
                    let before = [...vm.sketchCoordinates];
                    // Ignore the last coordinate that is the movable cursor point
                    let drawnVertexCoords = coordinates[0].toSpliced(-1);
                    if (before.length != drawnVertexCoords.length) {
                        // Sort out back-to-back duplicate coordinates
                        let sketchCoordinates = drawnVertexCoords
                            .slice()
                            .reduce((acc, cur) => {
                                let prev = acc.slice(-1)[0] || [];
                                if (prev[0] !== cur[0] && prev[1] !== cur[1]) {
                                    acc.push(cur);
                                }
                                return acc;
                            }, []);

                        // Return from calculation if the new sketch coordinates are the same as the previous
                        if (
                            before.length === sketchCoordinates.length &&
                            before
                                .flat(1)
                                .every(
                                    (coord, index) =>
                                        coord ===
                                        sketchCoordinates.flat(1)[index]
                                )
                        ) {
                            return geometry;
                        }
                        // Set new sketch coordinates
                        vm.sketchCoordinates = sketchCoordinates;

                        // Add to undo stack
                        vm.undoredo_forSketch.push('add polygon point', {
                            before: before,
                            after: vm.sketchCoordinates,
                        });
                    }

                    return geometry;
                },
                condition: function (evt) {
                    if (evt.originalEvent.buttons === 1) {
                        // Only allow drawing when the left mouse button is pressed
                        return true;
                    } else if (evt.originalEvent.buttons === 2) {
                        // If the right mouse button is pressed, undo the last point
                        if (vm.canUndoDrawnVertex) {
                            vm.undoredo_forSketch.undo();
                        } else {
                            vm.set_mode('layer');
                        }
                    } else {
                        return false;
                    }
                },
                finishCondition: function () {
                    if (vm.lastPoint) {
                        // vm.$emit('validate-feature');
                        vm.finishDrawing();
                    }
                    return true;
                },
            });

            vm.drawPointsForModel = new Draw({
                source: vm.modelQuerySource,
                type: 'Point',
                // geometryFunction: function (coordinates, geometry) {
                //     if (geometry) {
                //         if (coordinates[0].length) {
                //             // Add a closing coordinate to match the first
                //             geometry.setCoordinates(
                //                 [coordinates[0].concat([coordinates[0][0]])],
                //                 this.geometryLayout_
                //             );
                //         } else {
                //             geometry.setCoordinates([], this.geometryLayout_);
                //         }
                //     } else {
                //         geometry = new Polygon(
                //             coordinates,
                //             this.geometryLayout_
                //         );
                //     }

                //     if (vm.unOrRedoing_sketchPoint) {
                //         // Don't run below undo stack logic while executing an undo/redo of sketch points
                //         return geometry;
                //     }

                //     // Current feature id list for undo stack
                //     let before = [...vm.sketchCoordinates];
                //     // Ignore the last coordinate that is the movable cursor point
                //     let drawnVertexCoords = coordinates[0].toSpliced(-1);
                //     if (before.length != drawnVertexCoords.length) {
                //         // Sort out back-to-back duplicate coordinates
                //         let sketchCoordinates = drawnVertexCoords
                //             .slice()
                //             .reduce((acc, cur) => {
                //                 let prev = acc.slice(-1)[0] || [];
                //                 if (prev[0] !== cur[0] && prev[1] !== cur[1]) {
                //                     acc.push(cur);
                //                 }
                //                 return acc;
                //             }, []);

                //         // Return from calculation if the new sketch coordinates are the same as the previous
                //         if (
                //             before.length === sketchCoordinates.length &&
                //             before
                //                 .flat(1)
                //                 .every(
                //                     (coord, index) =>
                //                         coord ===
                //                         sketchCoordinates.flat(1)[index]
                //                 )
                //         ) {
                //             return geometry;
                //         }
                //         // Set new sketch coordinates
                //         vm.sketchCoordinates = sketchCoordinates;

                //         // Add to undo stack
                //         vm.undoredo_forSketch.push('add polygon point', {
                //             before: before,
                //             after: vm.sketchCoordinates,
                //         });
                //     }

                //     return geometry;
                // },
                // condition: function (evt) {
                //     if (evt.originalEvent.buttons === 1) {
                //         // Only allow drawing when the left mouse button is pressed
                //         return true;
                //     } else if (evt.originalEvent.buttons === 2) {
                //         // If the right mouse button is pressed, undo the last point
                //         if (vm.canUndoDrawnVertex) {
                //             vm.undoredo_forSketch.undo();
                //         } else {
                //             vm.set_mode('layer');
                //         }
                //     } else {
                //         return false;
                //     }
                // },
                // finishCondition: function () {
                //     if (vm.lastPoint) {
                //         // vm.$emit('validate-feature');
                //         vm.finishDrawing();
                //     }
                //     return true;
                // },
            });

            vm.drawPolygonsForModel.set('escKey', '');
            vm.drawPolygonsForModel.on('change:escKey', function () {
                console.log('ESC key pressed');
            });
            vm.drawPolygonsForModel.on('drawstart', function () {
                vm.errorMessage = null;
                vm.lastPoint = null;
            });
            vm.drawPolygonsForModel.on('click', function (evt) {
                console.log('Draw: click event', evt);
            });
            vm.drawPolygonsForModel.on('drawend', function (evt) {
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
                    label:
                        model.occurrence_report_number ||
                        model.label ||
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
            });

            vm.drawPointsForModel.on('drawend', function (evt) {
                console.log(evt);
                console.log(evt.feature.values_.geometry.flatCoordinates);
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
                    label:
                        model.occurrence_report_number || model.label || 'Draw',
                    color: color,
                    locked: false,
                });
                vm.newFeatureId++;
                console.log('newFeatureId = ' + vm.newFeatureId);
                vm.lastPoint = evt.feature;
                vm.sketchCoordinates = [[]];
            });

            vm.map.addInteraction(vm.drawPolygonsForModel);
            vm.map.addInteraction(vm.drawPointsForModel);
        },
        initialisePointerMoveEvent: function () {
            let vm = this;

            const hoverStylePolygon = vm.createStyle(
                vm.hoverFill,
                vm.hoverStrokePolygon,
                'Polygon'
            );

            const hoverStylePoint = vm.createStyle(
                vm.hoverFill,
                vm.hoverStrokePoint,
                'Point'
            );

            // Cache the hover fill so we don't have to create a new one every time
            // Also prevent overwriting property `hoverFill` color
            let _hoverFill = null;
            function hoverSelect(feature) {
                const color = feature.get('color') || vm.defaultColor;
                let hoverStyle = hoverStylePolygon;
                if (feature.getGeometry().getType() === 'Point') {
                    hoverStyle = hoverStylePoint;
                }
                _hoverFill = new Fill({ color: color });

                // If the feature is already selected, use the select stroke when hovering
                if (
                    vm.selectedFeatureIds.includes(feature.getProperties().id)
                ) {
                    hoverStyle.setFill(_hoverFill);
                    hoverStyle.setStroke(vm.clickSelectStroke);
                } else {
                    if (feature.getGeometry().getType() === 'Polygon') {
                        hoverStyle.setFill(vm.hoverFill);
                        hoverStyle.setStroke(vm.hoverStrokePolygon);
                    } else if (feature.getGeometry().getType() === 'Point') {
                        hoverStyle.getImage().setFill(vm.hoverFill);
                        hoverStyle.getImage().setStroke(vm.hoverStrokePoint);
                    }
                }
                return hoverStyle;
            }

            let selected = null;
            vm.map.on('pointermove', function (evt) {
                function isSelectedFeature(selected) {
                    if (!selected) {
                        return false;
                    }
                    return vm.selectedFeatureIds.includes(
                        selected.getProperties().id
                    );
                }
                if (selected !== null) {
                    if (isSelectedFeature(selected)) {
                        // Don't alter style of click-selected features
                        console.log('ignoring hover on selected feature');
                        if (vm.drawing) {
                            // Enable modify polygon the hovered polygon is selected and drawing mode is active
                            vm.modifySetActive(true);
                            vm.transformSetActive(false);
                        } else {
                            // Disable modify polygon when drawing mode is not active
                            vm.modifySetActive(false);
                        }
                    } else {
                        if (!(vm.measuring || vm.drawing)) {
                            // Don't highlight features when measuring or drawing
                            selected.setStyle(undefined);
                            const type = selected.getGeometry().getType();
                            selected.setStyle(
                                vm.createStyle(
                                    selected.values_.color,
                                    null,
                                    type
                                )
                            );
                        }
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
                            model.area_sqm = Math.round(
                                getArea(selected.getGeometry(), {
                                    projection: 'EPSG:4326',
                                })
                            );
                        }
                        vm.selectedModel = null;
                        vm.selectedModel = model;
                        if (!isSelectedFeature(selected)) {
                            selected.setStyle(hoverSelect);
                        }

                        return true;
                    },
                    {
                        layerFilter: function (layer) {
                            return layer.get('name') === 'query_layer';
                        },
                    }
                );

                // Change to info cursor if hovering over an optional layer
                let layer_at_pixel = layerAtEventPixel(vm, evt);
                // Compare layer names at pixel with optional layer names and set `hit` property accordingly
                let optional_layer_names = vm.optionalLayers.map((layer) => {
                    return layer.get('name');
                });
                let hit = layer_at_pixel.some(
                    (lyr) => optional_layer_names.indexOf(lyr.get('name')) >= 0
                );

                vm.map.getTargetElement().style.cursor = hit
                    ? 'help'
                    : 'default';

                if (selected) {
                    vm.featureToast.show();
                } else {
                    vm.featureToast.hide();
                }
            });
        },
        initialiseSingleClickEvent: function () {
            let vm = this;
            vm.map.on('singleclick', function (evt) {
                if (vm.drawing || vm.measuring) {
                    vm.lastPoint = new Feature(new Point(evt.coordinate));
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
                                // Priya commented the below to avoid the duplication count of 2 on delete button
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
                    ].filter((path) => ![undefined, null, ''].includes(path));

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
            if (!vm.editable) {
                return null;
            }
            // A basic style for selected polygons
            vm.basicSelectStyle = function (feature) {
                var color = feature.get('color') || vm.defaultColor;
                const type = feature.getGeometry().getType();
                return [vm.createStyle(color, vm.clickSelectStroke, type)];
            };
            // Basic style plus extra circles for vertices to help with modifying
            // See: https://github.com/openlayers/openlayers/issues/3165#issuecomment-71432465
            vm.modifySelectStyle = function (feature) {
                var image = new CircleStyle({
                    radius: 5,
                    fill: null,
                    stroke: new Stroke({ color: 'orange', width: 2 }),
                });
                var color = feature.get('color') || vm.defaultColor;
                return [
                    new Style({
                        image: image,
                        geometry: function (feature) {
                            const type = feature.getGeometry().getType();
                            if (type === 'Point') {
                                return feature.getGeometry();
                            }
                            const coordinates = feature
                                .getGeometry()
                                .getCoordinates()[0];
                            return new MultiPoint(coordinates);
                        },
                    }),
                    vm.createStyle(color, vm.clickSelectStroke, 'Polygon'),
                ];
            };

            // select interaction working on "singleclick"
            const selectSingleClick = new Select({
                style: vm.basicSelectStyle,
                layers: [vm.modelQueryLayer],
                wrapX: false,
                condition: function () {
                    // Prevent the interaction's standard select event
                    return false;
                },
            });
            selectSingleClick.on('select', (evt) => {
                if (vm.transforming) {
                    return;
                }
                $.each(evt.selected, function (idx, feature) {
                    console.log(
                        `Selected feature ${feature.getProperties().id}`,
                        toRaw(feature)
                    );
                    // Current feature id list for undo stack
                    let before = [...vm.selectedFeatureIds];
                    feature.setStyle(vm.basicSelectStyle);
                    vm.selectedFeatureIds.push(feature.getProperties().id);
                    // Add to undo stack
                    vm.undoredo.push('select feature', {
                        before: before,
                        after: vm.selectedFeatureIds,
                    });
                });

                $.each(evt.deselected, function (idx, feature) {
                    console.log(
                        `Unselected feature ${feature.getProperties().id}`
                    );
                    // Current feature id list for undo stack
                    let before = [...vm.selectedFeatureIds];
                    feature.setStyle(undefined);
                    vm.selectedFeatureIds = vm.selectedFeatureIds.filter(
                        (id) => id != feature.getProperties().id
                    );
                    // Add to undo stack
                    vm.undoredo.push('select feature', {
                        before: before,
                        after: vm.selectedFeatureIds,
                    });
                });
            });
            // When the map mode changes between draw and anything else, update the style of the selected features
            selectSingleClick.addEventListener('map:modeChanged', (evt) => {
                console.log('map mode changed', evt);
                if (
                    evt.details.new_mode === 'draw' &&
                    evt.details.new_subMode === 'Point'
                ) {
                    vm.setStyleForUnAndSelectedFeatures(vm.modifySelectStyle);
                } else {
                    vm.setStyleForUnAndSelectedFeatures();
                }
            });

            return selectSingleClick;
        },
        initialiseModifyFeatureEvent: function () {
            let vm = this;
            const modify = new ModifyFeature({
                source: vm.modelQuerySource, // Same source as the draw interaction
                // features: vm.select.getFeatures(), // Either need to provide source or features, but features doesn't seem to work
                pixelTolerance: vm.pixelTolerance,
                deleteCondition: function (evt) {
                    if (
                        evt.type !== 'pointerdown' ||
                        evt.originalEvent.button !== 2 // Remove vertex on right click
                    ) {
                        return false;
                    }
                    evt.stopPropagation();

                    let f = vm.map.getFeaturesAtPixel(evt.pixel, {
                        hitTolerance: vm.hitTolerance,
                    });
                    if (!f) {
                        return false;
                    }

                    let features = vm.selectedFeatures();

                    features.forEach((feature) => {
                        let coords = feature.getGeometry().getCoordinates();

                        for (let j = 0; j < coords.length; j++) {
                            let coord = coords[j];
                            if (coord.length <= 4) {
                                // Needs three vertices to form a polygon, four because the first and last are the same
                                return false;
                            }

                            for (let k = 0; k < coord.length; k++) {
                                let pxl1 = evt.pixel; // clicked pixel coordinates
                                let pxl2 = vm.map.getPixelFromCoordinate(
                                    coord[k]
                                ); // calculated pixel coordinates

                                // Distance between pixel1 and pixel2
                                let distance = vm.pixelDistance(pxl1, pxl2);
                                if (distance <= vm.pixelTolerance) {
                                    let selectedCoord = coord[k];
                                    console.log('delete coord', selectedCoord);
                                    coord.splice(k, 1);
                                    if (selectedCoord == null) {
                                        return;
                                    }
                                    feature
                                        .getGeometry()
                                        .setCoordinates([coord]);
                                    //commented validateFeature by Priya
                                    //validateFeature(feature, vm);
                                }
                            }
                        }
                    });
                },
            });

            modify.addEventListener('modifyend', function (evt) {
                console.log('Modify end', evt.features);
                // let feature = evt.features[0];
                //commented validateFeature by Priya
                //validateFeature(feature, vm);
            });

            return modify;
        },
        initialiseTransform: function () {
            let vm = this;

            const transform = new Transform({
                source: vm.modelQuerySource,
                hitTolerance: vm.hitTolerance,
            });

            const transformEndCallback = function (evt) {
                // eslint-disable-next-line no-unused-vars
                evt.features.forEach((feature) => {
                    //commented validateFeature by Priya
                    // validateFeature(feature, vm);
                });
            };

            for (const eventName of ['translateend', 'rotateend', 'scaleend']) {
                transform.addEventListener(eventName, transformEndCallback);
            }

            return transform;
        },
        undoLeaseLicensePoint: function () {
            let vm = this;
            if (vm.lastPoint) {
                vm.modelQuerySource.removeFeature(vm.lastPoint);
                vm.lastPoint = null;
                vm.sketchCoordinates = [[]];
                this.selectedFeatureId = null;
            } else {
                vm.drawPolygonsForModel.removeLastPoint();
            }
        },
        redoLeaseLicensePoint: function () {
            let vm = this;

            const sketchLineGeom =
                vm.drawPolygonsForModel.sketchLine_?.getGeometry();
            let coordinates = vm.drawPolygonsForModel.sketchCoords_[0];
            // Redo finish coordinate
            let finishCoordinate = vm.sketchCoordinates.slice(-1);

            if (sketchLineGeom !== undefined) {
                // No geometry, only the first sketch coordinates point present
                sketchLineGeom.setCoordinates([coordinates]);
            }

            if (finishCoordinate) {
                vm.drawPolygonsForModel.appendCoordinates(finishCoordinate);
            }

            vm.drawPolygonsForModel.updateSketchFeatures_();
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
                        if (
                            feature.getProperties().locked === false ||
                            vm.debug // Allow deletion of locked features if debug mode is enabled
                        ) {
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
        fetchProposals: async function () {
            let vm = this;
            vm.fetchingProposals = true;
            let url = api_endpoints.occurrence_report + '/list_for_map/';
            // Characters to concatenate pseudo url elements
            let chars = ['&', '&', '?'];

            if (vm.proposalIds.length > 0) {
                url +=
                    `${chars.pop()}proposal_ids=` + vm.proposalIds.toString();
            }
            fetch(url)
                .then(async (response) => {
                    const data = await response.json();
                    if (!response.ok) {
                        const error =
                            (data && data.message) || response.statusText;
                        console.log(error);
                        return Promise.reject(error);
                    }
                    vm.proposals = data;
                    let initialisers = [
                        vm.assignProposalFeatureColors(vm.proposals),
                        vm.loadFeatures(vm.proposals),
                    ];
                    Promise.all(initialisers).then(() => {
                        console.log('Done loading features');
                    });
                })
                .catch((error) => {
                    console.error('There was an error!', error);
                })
                .finally(() => {
                    vm.fetchingProposals = false;
                });
        },
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
        assignProposalFeatureColors: function (proposals) {
            let vm = this;
            proposals.forEach(function (proposal) {
                proposal.color = vm.getRandomRGBAColor();
                console.log(proposal.lodgement_date);
                console.log(typeof proposal.lodgement_date);
            });
        },
        loadFeatures: function (proposals) {
            let vm = this;
            console.log(proposals);
            // Remove all features from the layer
            vm.modelQuerySource.clear();
            proposals.forEach(function (proposal) {
                proposal.ocr_geometry.features.forEach(function (featureData) {
                    let feature = vm.featureFromDict(featureData, proposal);
                    if (vm.modelQuerySource.getFeatureById(feature.getId())) {
                        console.warn(
                            `Feature ${feature.getId()} already exists in the source. Skipping...`
                        );
                        return;
                    }
                    vm.modelQuerySource.addFeature(feature);
                    vm.newFeatureId++;
                });
            });
            // vm.addFeatureCollectionToMap();
            vm.map.dispatchEvent({
                type: 'features-loaded',
                details: {
                    loaded: true,
                },
            });
        },
        /**
         * Creates a styled feature object from a feature dictionary
         * @param {dict} featureData A feature dictionary
         * @param {Proxy} model A model object
         */
        featureFromDict: function (featureData, model) {
            let vm = this;
            if (model == null) {
                model = vm.context || {};
            }

            let color = vm.styleByColor(featureData, model);
            const type = featureData.geometry.type;
            let style = vm.createStyle(color, vm.defaultColor, type);
            let geometry;
            if (type === 'Polygon') {
                geometry = new Polygon(featureData.geometry.coordinates);
            } else if (type === 'Point') {
                geometry = new Point(featureData.geometry.coordinates);
            } else if (type === 'LineString') {
                alert('LineString not yet supported');
            } else {
                console.error(`Unsupported geometry type ${type}`);
            }

            let feature = new Feature({
                id: vm.newFeatureId, // Incrementing-id of the polygon/feature on the map
                geometry: geometry,
                name: model.id,
                // label: model.label || model.application_type_name_display,
                label: model.label,
                color: color,
                source: featureData.properties.source || null,
                geometry_source:
                    featureData.properties.geometry_source || 'New',
                locked: featureData.properties.locked || false,
                copied_from: featureData.properties.report_copied_from || null,
                area_sqm: featureData.properties.area_sqm || null,
            });
            if (featureData.id) {
                // Id of the model object (https://datatracker.ietf.org/doc/html/rfc7946#section-3.2)
                feature.setId(featureData.id);
            }
            if (!feature.getProperties().area) {
                feature.getProperties().area = vm.featureArea(feature);
            }

            // to remove the ocr_geometry as it shows up when the geometry is downloaded
            let propertyModel = model;
            delete propertyModel.ocr_geometry;

            feature.setProperties({
                model: propertyModel,
            });
            feature.setStyle(style);
            console.log(feature);

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
         * Returns a dictionary of query parameters for a given layer
         * @param {String} layerStr The dictionary key containing the layer information
         */
        queryParamsDict: function (layerStr) {
            let vm = this;

            if (!(layerStr in vm.owsQuery)) {
                console.error(`Layer ${layerStr} not found in OWS query`);
                return {};
            }
            if (!vm.owsQuery[layerStr].typeName) {
                console.error(`Layer ${layerStr} needs a typeName`);
                return {};
            }

            return {
                service: vm.owsQuery.service || 'WFS',
                version: vm.owsQuery.version || '1.0.0',
                request: vm.owsQuery[layerStr].request || 'GetFeature',
                typeName: vm.owsQuery[layerStr].typeName,
                maxFeatures: vm.owsQuery[layerStr].maxFeatures || '5000',
                srsName: vm.owsQuery[layerStr].srsName || 'EPSG:4326',
                outputFormat:
                    vm.owsQuery[layerStr].outputFormat || 'application/json',
                propertyName:
                    vm.owsQuery[layerStr].propertyName || 'wkb_geometry',
            };
        },
        finishDrawing: function () {
            let vm = this;
            vm.queryingGeoserver = false;
            vm.errorMessage = null;
            vm.drawPolygonsForModel.finishDrawing();
            if (vm.mode == 'draw' && vm.selectedFeatureIds.length == 0) {
                vm.set_mode('layer');
            }
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
        validate_map_docs: function () {
            var formData = new FormData();
            var vm = this;
            formData.append('csrfmiddlewaretoken', vm.csrf_token);
            vm.isValidating = true;
            vm.errorString = '';
            const options = {
                method: 'POST',
                body: formData,
                'content-type': 'application/json',
            };
            fetch(
                helpers.add_endpoint_join(
                    api_endpoints.occurrence_report,
                    `/${vm.context.id}/validate_map_files/`
                ),
                options
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
                    vm.$emit('refreshFromResponse', data);
                    // Once the shapefile is converted to a proposal geometry the files are deleted
                    // so calling this will remove the file list from the front end
                    vm.$refs.shapefile_document.get_documents();
                    vm.$nextTick(() => {
                        vm.loadFeatures([data]);
                        vm.displayAllFeatures();
                        swal.fire(
                            'Success',
                            'Shapefile processed successfully',
                            'success'
                        );
                    });
                })
                .catch((error) => {
                    console.log(error);
                    vm.errorString = helpers.apiVueResourceError(error);
                    swal.fire({
                        title: 'Validation',
                        text: error,
                        icon: 'error',
                    });
                })
                .finally(() => {
                    vm.isValidating = false;
                });
        },
        /**
         * Returns the selected features
         */
        selectedFeatures: function () {
            let vm = this;
            let features = vm.modelQuerySource.getFeatures();
            return features.filter((feature) => {
                return vm.selectedFeatureIds.includes(
                    feature.getProperties().id
                );
            });
        },
        /**
         * Sets interactions for modify to active or inactive
         * @param {boolean} active
         */
        modifySetActive(active) {
            let vm = this;
            if (vm.editable) {
                vm.modify.setActive(active);
            }
            vm.snap.setActive(active);
        },
        /**
         * Sets interactions for modify to active or inactive
         */
        transformSetActive(active) {
            let vm = this;
            if (!vm.editable) {
                return;
            }
            vm.select.setActive(!active);
            vm.transform.setActive(active);
        },
        /**
         * Undoes the last map interaction
         */
        undo: function () {
            let vm = this;
            // Need to do double check here
            if (vm.canUndoDrawnVertex) {
                vm.undoredo_forSketch.undo();
            } else if (vm.canUndoAction) {
                vm.undoredo.undo();
                // Find the last feature in the redo stack and validate it (the last feature doesn't necessarily need to be the last item in the stack, as the last item could e.g. be a 'blockend' object)
                let item = vm.undoredo._redoStack
                    .getArray()
                    .toReversed()
                    .find((item) => {
                        if (item.feature) {
                            return item;
                        }
                    });
                if (item && item.feature) {
                    vm.finishDrawing();
                }
            } else {
                // Nothing
            }
        },
        /**
         * Redoes the last map interaction
         */
        redo: function () {
            let vm = this;
            if (vm.canRedoDrawnVertex) {
                vm.undoredo_forSketch.redo();
            } else if (vm.canRedoAction) {
                vm.undoredo.redo();
                // Find the last feature in the undo stack and validate it
                let item = vm.undoredo._undoStack
                    .getArray()
                    .toReversed() // .reverse() mutates in-place, .toReversed() doesn't
                    .find((item) => {
                        if (item.feature) {
                            return item;
                        }
                    });
                if (item && item.feature) {
                    vm.finishDrawing();
                }
            } else {
                // Nothing
            }
        },
        /**
         * Returns a description for the top action in the undo or redo stack
         * @param {String} stack_name The name of the stack to get the top action from
         */
        undoRedoStackTopInteractionName: function (stack_name = 'undo') {
            let vm = this;
            if (!vm.undoredo) {
                return;
            }
            let stack = vm.undoredo.getStack(stack_name);

            if (stack && stack.length > 0) {
                return (
                    (stack.slice(-1)[0] || []).name ||
                    (stack.slice(-1)[0] || []).type
                );
            }
            return 'last action';
        },
        toggleElementVisibility: function (elementId) {
            let element = document.getElementById(elementId);
            if (element.style.display !== 'block') {
                element.style.display = 'block';
            } else {
                element.style.display = 'none';
            }
        },
        shapeFilesUpdated: function () {
            let numShapefiles =
                this.$refs.shapefile_document?.numDocuments || 0;
            this.numShapefiles = numShapefiles;
            this.uploadedFileTypes =
                this.$refs.shapefile_document.documents.map((doc) => {
                    return doc.name.slice(doc.name.lastIndexOf('.'));
                }, []);
        },
        featureArea: function (feature, projection = 'EPSG:4326') {
            return Math.round(
                getArea(feature.getGeometry(), {
                    projection: projection,
                })
            );
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

.force-parent-lh {
    line-height: inherit !important;
}

#submenu-draw {
    display: none;
}
</style>
