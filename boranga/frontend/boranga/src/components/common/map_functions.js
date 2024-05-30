// import WMSCapabilities from 'ol/format/WMSCapabilities';
import TileWMS from 'ol/source/TileWMS';
import TileLayer from 'ol/layer/Tile';
import GeoJSON from 'ol/format/GeoJSON';
import Feature from 'ol/Feature';
import { Polygon } from 'ol/geom';
import { Style, Fill, Stroke } from 'ol/style';
import { utils } from '@/utils/hooks';

// Tile server url
// var urlKmi = `${env['gis_server_url']}/geoserver/public/wms/?SERVICE=WMS&VERSION=1.0.0&REQUEST=GetCapabilities`;
// const urlKbBase = `${env['gis_server_url']}`;

// Layer to use as map base layer
export var baselayer_name = 'mapbox-emerald';
// export var baselayer_name = 'mapbox-dark'

/**
 * Returns layers at map event pixel coordinates
 * @param {Proxy} map_component A map component instance
 * @param {Event} evt An Event object
 * @returns an array of layers
 */
export function layerAtEventPixel(map_component, evt) {
    const layer_at_pixel = [];
    const layers = [];
    map_component.map.getLayers().forEach((layer) => {
        if (typeof layer.getLayers === 'function') {
            layers.concat(layer.getLayersArray());
        } else {
            layers.push(layer);
        }
    }, layers);

    layers.forEach((layer) => {
        if (!map_component.informing) {
            return;
        }
        let pixel = map_component.map.getEventPixel(evt.originalEvent);

        let data = layer.getData(pixel);
        // Return if no data or the alpha channel in RGBA is zero (transparent)
        if (!data || data[3] == 0) {
            return;
        }
        layer_at_pixel.push(layer);
    });

    return layer_at_pixel;
}

/**
 * Queries the WMS server for its capabilities and adds optional layers to a map
 * @param {Proxy} map_component A map component instance
 * @param {string} tileLayerApiUrl The url to the tile layer API
 */
export async function fetchTileLayers(map_component, tileLayerApiUrl) {
    // let parser = new WMSCapabilities();
    if (!tileLayerApiUrl) {
        console.error('No tile layer API url provided');
        return [];
    }
    let tileLayers = [];

    await fetch(tileLayerApiUrl)
        .then(async (response) => {
            if (!response.ok) {
                throw new Error('Network response was not ok');
            }
            return response.json();
        })
        .then((layers) => {
            console.log('tilelayer', layers);
            tileLayers = _helper.tileLayerFromLayerDefinitions(layers);
        })
        .catch((error) => {
            console.error('Error fetching tilelayer:', error);
        });
    return tileLayers;
}

/**
 * Returns proposal objects by ID from an API endpoint
 * @param {Object} map_component The map component instance
 * @param {String} proposalApiUrl The URL to the proposal API
 * @param {Array} proposalIds An array of proposal IDs to fetch
 * @returns Proposal objects
 */
export async function fetchProposals(
    map_component,
    proposalApiUrl,
    proposalIds
) {
    if (!proposalApiUrl) {
        console.error('No proposal API URL provided');
        return [];
    }
    if (!proposalIds) {
        console.error('No proposal IDs provided');
        return [];
    }
    map_component.fetchingProposals = true;
    let url = proposalApiUrl;
    // Characters to concatenate pseudo url elements
    let chars = ['&', '&', '?'];
    let proposals = [];

    if (proposalIds.length > 0) {
        url += `${chars.pop()}proposal_ids=` + proposalIds.toString();
    }
    await fetch(url)
        .then(async (response) => {
            const data = await response.json();
            if (!response.ok) {
                const error = (data && data.message) || response.statusText;
                console.log(error);
                return Promise.reject(error);
            }
            proposals = data;
        })
        .catch((error) => {
            console.error('There was an error!', error);
        })
        .finally(() => {
            map_component.fetchingProposals = false;
        });

    return proposals;
}

/**
 * Sets the mode of interaction of the map.
 * @param {string} mode The mode to set the map to (layer, draw, measure)
 * @param {string=} subMode The submode to set the map to (e.g. draw: 'Polygon', 'Point')
 */
export function set_mode(mode, subMode = null) {
    // Toggle map mode on/off when the new mode is the old one
    if (this.mode == mode) {
        if (this.subMode == subMode) {
            this.mode = 'layer';
            this.subMode = null;
        } else {
            // If only the submode is different, set the new submode but keep the mode
            this.subMode = subMode;
        }
    } else {
        this.mode = mode;
        this.subMode = subMode;
    }

    this.drawing = false;
    this.measuring = false;
    this.informing = false;
    this.transforming = false;
    this.errorMessageProperty(null);
    this.overlay(undefined);
    this.map.getTargetElement().style.cursor = 'default';
    this.transformSetActive(false);

    if (this.mode === 'layer') {
        this.clearMeasurementLayer();
        _helper.toggle_draw_or_measure.bind(this)(false, false);
    } else if (this.mode === 'draw') {
        this.clearMeasurementLayer();
        this.sketchCoordinates = [[]];
        _helper.toggle_draw_or_measure.bind(this)(false, true);
        this.undoredo_forSketch.clear(); // Clear the sketch coordinates undo/redo stack
        this.drawing = true;
    } else if (this.mode === 'transform') {
        this.clearMeasurementLayer();
        this.transformSetActive(true);
        _helper.toggle_draw_or_measure.bind(this)(false, false);
        this.transforming = true;
    } else if (this.mode === 'measure') {
        _helper.toggle_draw_or_measure.bind(this)(true, false);
        this.measuring = true;
    } else if (this.mode === 'info') {
        _helper.toggle_draw_or_measure.bind(this)(false, false);
        this.informing = true;
    } else {
        console.error(`Cannot set mode ${mode}`);
        return false;
    }
    if (this.select) {
        // Call back to the map so selected features can adept their style to the new mode
        this.select.dispatchEvent({
            type: 'map:modeChanged',
            details: {
                new_mode: this.mode,
                new_subMode: this.subMode,
            },
        });
    }

    return true;
}

/**
 * Defines polygon feature styling depending on whether the geometry source
 * is a Registration of Interest or a Competitive Process
 * @param {object} feature A single geometry feature (e.g. a drawn polygon)
 */
export function polygon_style(feature) {
    let strokecolor = '#3498DB';
    let fillcolor = '#85C1E9';
    if (feature.get('source') === 'registration_of_interest') {
        // yellowish
        strokecolor = [244, 208, 63, 1.0];
        fillcolor = [241, 196, 15, 0.7];
    } else if (feature.get('source') === 'competitive_process') {
        // orangish
        strokecolor = [240, 178, 122, 1.0];
        fillcolor = [230, 126, 34, 0.7];
    }
    return new Style({
        fill: new Fill({
            color: fillcolor,
        }),
        stroke: new Stroke({
            color: strokecolor,
            width: 1,
        }),
    });
}

/**
 * Validate feature callback function. Calls `finnishDrawing` on the map component
 * when the feature is valid. A feature is condidered valid when it intersects with
 * the DBCS legislated land-water layer.
 * @param {string} feature The feature
 * @param {Proxy} component_map The map component
 */
export function validateFeature(feature, component_map) {
    let vm = this;
    let feature_wkt = undefined;
    console.log('Validate feature', feature);
    if (feature === undefined) {
        // Get the WKT representation of the currently drawn polygon sketch
        feature_wkt = _helper.featureToWKT.bind(vm)();
    } else {
        // Get the WKT representation of the provided feature
        feature_wkt = _helper.featureToWKT(feature);
    }

    if (component_map === undefined) {
        component_map = vm.$refs.component_map;
    }

    let query = _helper.geoserverQuery(feature_wkt, component_map);

    _helper.validateFeatureQuery(query).then(async (features) => {
        if (features.length === 0) {
            console.warn('New feature is not valid');
            component_map.errorMessageProperty(
                'The polygon you have drawn does not intersect with any DBCA lands or water.'
            );
        } else {
            console.log('New feature is valid', features);
            component_map.finishDrawing();
        }
    });
}

export let owsQuery = {
    version: '1.0.0', // TODO: Change to 1.1.0 or 2.0.0 when supported by the geoserver
    landwater: {
        typeName: 'public:dbca_legislated_lands_and_waters',
        srsName: 'EPSG:4326',
        propertyName:
            'objectid,wkb_geometry,category,leg_act,leg_identifier,leg_name,leg_tenure,leg_vesting,shape_area,leg_poly_area',
        geometry: 'wkb_geometry',
    },
};

/**
 * Module with map related helper functions
 */
const _helper = {
    /**
     * Toggles measure and polygon layer active or inactive
     * @param {boolean} drawForMeasure Whether to set the measure layer active or inactive
     * @param {boolean} drawForModel Whether to set the model's polygon layer active or inactive
     */
    toggle_draw_or_measure: function (drawForMeasure, drawForModel) {
        /**
         * Sets the active state of the Draw layers
         * @param {boolean} pointsActive Set the active state of the points layer
         * @param {boolean} polygonsActive Set the active state of the polygons layer
         */
        var drawForModelSetActive = function (pointsActive, polygonsActive) {
            if (this.drawPointsForModel) {
                this.drawPointsForModel.setActive(pointsActive);
            }
            if (this.drawPolygonsForModel) {
                this.drawPolygonsForModel.setActive(polygonsActive);
            }
        }.bind(this);

        if (this.drawForMeasure) {
            this.drawForMeasure.setActive(drawForMeasure);
        }
        if (drawForModel && this.subMode === 'Polygon') {
            // Set points drawing layer inactive and polygons drawing layer active
            drawForModelSetActive(false, true);
        } else if (drawForModel && this.subMode === 'Point') {
            // Set points drawing layer active and polygons drawing layer inactive
            drawForModelSetActive(true, false);
        } else {
            // Set both points and polygons drawing layers inactive
            drawForModelSetActive(false, false);
        }
    },
    /**
     * Returns a Well-known-text (WKT) representation of a feature
     * @param {Feature} feature A feature to validate
     */
    featureToWKT: function (feature) {
        let vm = this;

        if (feature === undefined) {
            // If no feature is provided, create a feature from the current sketch
            let coordinates = vm.$refs.component_map.sketchCoordinates.slice();
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
                    ? [flatCoordinates[index], flatCoordinates[index + 1]].join(
                          ' '
                      )
                    : ''
            )
            .filter((item) => item != '');

        // Create a Well-Known-Text polygon string from the coordinate pairs
        return `POLYGON ((${flatCoordinateStringPairs.join(', ')}))`;
    },
    /**
     * Builds a query string for the geoserver based on the provided WKT
     * @param {str} wkt A geometry in Well-known-text (WKT) format
     * @param {Object} map_component The map component
     * @returns A query string for the geoserver
     */
    geoserverQuery: function (wkt, map_component) {
        let vm = this;
        if (wkt === undefined) {
            console.warn('No WKT provided');
            return;
        }
        if (map_component === undefined) {
            map_component = vm.$refs.component_map;
        }
        // The geoserver url
        // TODO: Only changed the env part here, so the url probably doesn't work with the new geoserver
        let owsUrl = `${env['gis_server_url']}/geoserver/public/ows/?`;
        // Create a params dict for the WFS request to the land-water layer
        let paramsDict = map_component.queryParamsDict('landwater');
        let geometry_name = map_component.owsQuery.landwater.geometry;
        paramsDict['CQL_FILTER'] = `INTERSECTS(${geometry_name},${wkt})`;

        // Turn params dict into a param query string
        let params = new URLSearchParams(paramsDict).toString();
        let query = `${owsUrl}${params}`;

        return query;
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
    tileLayerFromLayerDefinitions: function (layers) {
        const tileLayers = [];

        for (let j in layers) {
            let layer = layers[j];

            let l = new TileWMS({
                url: layer.geoserver_url,
                // crossOrigin: 'anonymous', // Data for a image tiles can only be retrieved if the source's crossOrigin property is set (https://openlayers.org/en/latest/apidoc/module-ol_layer_Tile-TileLayer.html#getData)
                params: {
                    FORMAT: 'image/png',
                    VERSION: '1.1.1',
                    tiled: true,
                    STYLES: '',
                    LAYERS: `${layer.layer_name}`,
                },
            });

            const isBackgroundLayer =
                layer.is_satellite_background || layer.is_streets_background;

            let tileLayer = new TileLayer({
                name: layer.Name,
                // abstract: layer.Abstract.trim(),
                title: layer.display_title.trim(),
                visible: layer.visible,
                // extent: layer.BoundingBox[0].extent,
                source: l,
                displayInLayerSwitcher: !isBackgroundLayer,
                is_satellite_background: layer.is_satellite_background,
                is_streets_background: layer.is_streets_background,
                minZoom: layer.min_zoom,
                maxZoom: layer.max_zoom,
            });

            let legend_url = null;
            if (layer.Name == baselayer_name) {
                // TODO don't add the baselayer to the optional layer control
            } else {
                if (typeof layer.Style != 'undefined') {
                    legend_url = layer.Style[0].LegendURL[0].OnlineResource;
                }
            }

            // Set additional attributes to the layer
            tileLayer.set('columns', []); // []
            tileLayer.set('display_all_columns', true); // true
            tileLayer.set('legend_url', legend_url);

            tileLayers.push(tileLayer);
        }
        return tileLayers;
    },
};
