<template lang="html">
     <div class="map-wrapper row col-sm-12">
        <div :id="elem_id" class="map">
            <div class="basemap-button">
                <img v-if="showSatIcon" id="basemap_sat" src="../../assets/satellite_icon.jpg" @click="setBaseLayer('sat')" />
                <img v-if="!showSatIcon" id="basemap_osm" src="../../assets/map_icon.png" @click="setBaseLayer('osm')" />
            </div>
            <div class="optional-layers-wrapper">
                <div class="optional-layers-button-wrapper">
                    <div :class="[
                                mode == 'measure' ? 'optional-layers-button-active': 'optional-layers-button'
                                ]"
                    >
                        <img class="svg-icon" src="../../assets/ruler.svg" />
                    </div>
                </div>
                <div class="optional-layers-button-wrapper">
                    <div :class="[
                                mode == 'draw' ? 'optional-layers-button-active': 'optional-layers-button'
                                ]"
                    >
                        <img class="svg-icon" src="../../assets/pen-icon.svg" />
                    </div>
                </div>
                <div class="optional-layers-button-wrapper">
                    <a id="download" download="features.json">Download</a>
                </div>
            </div>
        </div>
        <button class="col-sm-1" type="submit">Save Point</button>
        <div class="overlay-container">
            <span class="overlay-text" id="feature-id"></span>
        </div>
        <div id="coordinates" class="coordinates"></div>
        <div id="mouse-overlay" class="overlay"></div>
    </div>
</template>

<script>
import { v4 as uuid } from 'uuid';
import Vue from 'vue' ;
import VectorLayer from 'ol/layer/Vector';
import VectorSource from 'ol/source/Vector';
import 'ol/ol.css';
import Map from 'ol/Map';
import View from 'ol/View';
//import Feature from 'ol/Feature';
import TileLayer from 'ol/layer/Tile';
import TileWMS from 'ol/source/TileWMS';
import OSM from 'ol/source/OSM';
import GeoJSON from 'ol/format/GeoJSON';
import { Circle as CircleStyle, Fill, Stroke, Style, Text, RegularShape } from 'ol/style';
import OverlayLayer from 'ol/Overlay';
import Feature from 'ol/Feature';
import { Draw, Modify, Snap, Select } from 'ol/interaction';
import { MousePosition, defaults as DefaultControls } from 'ol/control';
import { createStringXY } from 'ol/coordinate';
import Point from 'ol/geom/Point';
import {
  api_endpoints,
  helpers
}
from '@/utils/hooks'
import Ocr_location from './occurrence/ocr_location.vue';
import { Polygon } from 'ol/geom';

export default {
        name: 'MapComponent',
        props:{
            occurrence_report_obj:{
                type: Object,
                required:true
            },
            is_external:{
              type: Boolean,
              default: false
            },
        },
        data:function () {
            let vm = this;
            return{
                elem_id: uuid(),
                map: null,
                showSatIcon: true,
                form:null,
                errors: false,
                tileLayerOSM: null,
                tileLayerSat: null,
                mode: 'normal',
                source : null,
                modelQuerySource: null,
                point_data:null,
                shapefile_json: {"type":"FeatureCollection","features":[{"type":"Feature","properties":{"id":1},"geometry":{"coordinates":[[[116.06664827879348,-31.93675031506431],[116.06664827879348,-31.994867724519167],[116.17443408838562,-31.994867724519167],[116.17443408838562,-31.93675031506431],[116.06664827879348,-31.93675031506431]]],"type":"Polygon"}},{"type":"Feature","properties":{"id":2},"geometry":{"type":"Polygon","coordinates":[[[116.04653664085203,-31.89991187254868],[116.04545524108961,-31.89995697026007],[116.0443842526443,-31.90009182921046],[116.04333398668759,-31.90031515102484],[116.04231455505979,-31.90062478562606],[116.0413357729947,-31.901017751916903],[116.04040706468766,-31.9014902664569],[116.03953737261281,-31.902037779858986],[116.03873507145939,-31.90265502055705],[116.03800788751451,-31.903336045524537],[116.03736282426674,-31.9040742974576],[116.03680609494673,-31.904862667874127],[116.03634306265535,-31.90569356552278],[116.03597818865663,-31.906558989445326],[116.03571498933616,-31.90745060599025],[116.03555600224243,-31.908359829037533],[116.03550276154138,-31.90927790266327],[116.03555578312505,-31.910195985448997],[116.03571455952195,-31.91110523562421],[116.03597756466311,-31.911996896222504],[116.03634226846226,-31.912862379430912],[116.03680516107445,-31.913693349319594],[116.03736178660341,-31.914481802154175],[116.03800678593703,-31.915220143516045],[116.03873394830072,-31.915901261486383],[116.0395362710353,-31.916518595187295],[116.04040602702435,-31.917066198018183],[116.04133483912238,-31.917538794976238],[116.04231376086666,-31.91793183350711],[116.04333336269406,-31.9182415273942],[116.04438382283006,-31.91846489326196],[116.0454550219722,-31.918599779340276],[116.04653664085203,-31.918644886211645],[116.04761825973183,-31.918599779340276],[116.04868945887398,-31.91846489326196],[116.04973991901,-31.9182415273942],[116.05075952083739,-31.91793183350711],[116.05173844258168,-31.917538794976238],[116.0526672546797,-31.917066198018183],[116.05353701066875,-31.916518595187295],[116.05433933340333,-31.915901261486383],[116.05506649576701,-31.915220143516045],[116.05571149510062,-31.914481802154175],[116.05626812062958,-31.913693349319594],[116.05673101324177,-31.912862379430912],[116.05709571704094,-31.911996896222504],[116.05735872218212,-31.91110523562421],[116.05751749857902,-31.910195985448997],[116.05757052016266,-31.90927790266327],[116.0575172794616,-31.908359829037533],[116.05735829236791,-31.90745060599025],[116.05709509304744,-31.906558989445326],[116.0567302190487,-31.90569356552278],[116.05626718675732,-31.904862667874127],[116.05571045743731,-31.9040742974576],[116.05506539418953,-31.903336045524537],[116.05433821024468,-31.90265502055705],[116.05353590909125,-31.902037779858986],[116.05266621701638,-31.9014902664569],[116.05173750870935,-31.901017751916903],[116.05075872664425,-31.90062478562606],[116.04973929501647,-31.90031515102484],[116.04868902905974,-31.90009182921046],[116.04761804061444,-31.89995697026007],[116.04653664085203,-31.89991187254868]]]}}]},
            }
        },
        components: {
        },
        computed: {
            title: function(){
                return "Add Location";
        },
            
        },
        watch:{
        },
        methods:{
            eventListeners:function (){
                let vm = this;
            },
            initMap: function (){
                let vm = this;

                let satelliteTileWms = new TileWMS({
                    url: env['kmi_server_url'] + '/geoserver/public/wms',
                    params: {
                        'FORMAT': 'image/png',
                        'VERSION': '1.1.1',
                        tiled: true,
                        STYLES: '',
                        LAYERS: 'public:mapbox-satellite',
                    } 
                });

                // let streetsTileWMS = new TileWMS({
                //     url: env['kmi_server_url'] + '/geoserver/public/wms',
                //     params: {
                //         'FORMAT': 'image/png',
                //         'VERSION': '1.1.1',
                //         tiled: true,
                //         STYLES: '',
                //         LAYERS: `public:${baselayer_name}`
                //     }
                // });
                vm.tileLayerOSM = new TileLayer({
                    title: 'StreetsMap',
                    type: 'base',
                    visible: true,
                    source: new OSM(),
                });
                vm.tileLayerSat = new TileLayer({
                    title: 'Satellite',
                    type: 'base',
                    visible: false,
                    source: satelliteTileWms,
                })

                vm.map = new Map({
                    target: vm.elem_id,
                    layers: [
                        vm.tileLayerOSM, 
                        vm.tileLayerSat,
                    ],
                    view: new View({
                        center: [115.95, -31.95],
                        zoom: 7,
                        projection: 'EPSG:4326',
                    }),
                    controls: DefaultControls().extend([
                        new MousePosition({
                        coordinateFormat: createStringXY(4), // Format coordinates with 4 decimal places
                        projection: 'EPSG:4326', // Use WGS 84 projection (longitude/latitude)
                        target: document.getElementById('coordinates'), // The DOM element to display coordinates
                        undefinedHTML: '&nbsp;', // Text to display when the mouse is not over the map
                        }),
                    ]),
                })

                // update map extent when new features added
                //vm.map.on('rendercomplete', vm.displayAllFeatures());

                let fillStyle = new Fill({
                    color: [84,118,255,1]
                })

                let strokeStyle = new Stroke({
                    color: [46,45,45,1],
                    width: 1.2
                })

                let circleStyle = new CircleStyle({
                    fill: new Fill({
                        color: [245,49,5,1]
                    }),
                    radius: 7,
                    stroke: strokeStyle,
                })

                vm.source = new VectorSource({
                    //features: new GeoJSON().readFeatures(vm.shapefile_json),
                    features: vm.point_data,
                })

                let vectorData = new VectorLayer({
                    source: vm.source,
                    visible: true,
                    title: 'VectorDataExample',
                    style: new Style({
                        fill: fillStyle,
                        stroke: strokeStyle,
                        image: circleStyle,
                    })
                })

                // Create a feature with a marker
                // var marker = new ol.Feature({
                //     geometry: new ol.geom.Point(ol.proj.fromLonLat([longitude, latitude]))
                // });

                // // Add the feature to the vector layer
                // vectorLayer.getSource().addFeature(marker);

                vm.map.addLayer(vectorData);

                const draw = new Draw({
                    type: 'Point',
                    source: vm.source
                });
                vm.map.addInteraction(draw)

                draw.on('drawend', (event) => {
                    const coordinates = event.feature.getGeometry().getCoordinates();
                    vm.occurrence_report_obj.location.geojson_point = `POINT(${coordinates[0]} ${coordinates[1]})`;
                });


                //vector Feature popup
                let overlayElement = document.querySelector('.overlay-container');
                let overlayLayer = new OverlayLayer({
                    element: overlayElement
                })

                vm.map.addOverlay(overlayLayer);
                let overlayFeatureId = document.getElementById('feature-id');

                vm.map.on('click', function(e){
                    overlayLayer.setPosition(undefined);
                    vm.map.forEachFeatureAtPixel(e.pixel, function(feature,layer){
                        let clickedCoords=e.coordinate
                        overlayLayer.setPosition(clickedCoords);
                        overlayFeatureId.innerHTML=clickedCoords;
                        //console.log(feature.get('id'));
                    })
                })

                // Create a custom overlay for displaying coordinates on top of the mouse
                const mouseOverlay = new OverlayLayer({
                    element: document.getElementById('mouse-overlay'),
                    positioning: 'bottom-left',
                    stopEvent: false, // Allow map events to pass through the overlay
                });

                vm.map.addOverlay(mouseOverlay);
                
                // Add a mousemove event listener to update the overlay's position
                vm.map.on('pointermove', (e) => {
                    if (e.dragging) {
                        return;
                    }
                    const coordinate = e.coordinate;
                    mouseOverlay.setPosition(coordinate);
                    document.getElementById('mouse-overlay').innerHTML=coordinate;
                });

             },
             setBaseLayer: function(selected_layer_name){
                console.log('in setBaseLayer')
                if (selected_layer_name == 'sat') {
                    this.toggleSatIcon('sat');
                    this.tileLayerOSM.setVisible(false)
                    this.tileLayerSat.setVisible(true)
                } else {
                    this.toggleSatIcon('osm');
                    this.tileLayerOSM.setVisible(true)
                    this.tileLayerSat.setVisible(false)
                }
            },
            toggleSatIcon: function(layer) {
                if (layer === 'osm') {
                    this.showSatIcon = true;
                } else {
                    this.showSatIcon = false;
                }
            },
        },
        created: async function() {
            let vm=this;
            
        },
        mounted: function(){
            let vm = this;
            vm.initMap();
            const format = new GeoJSON({featureProjection: 'EPSG:4326'});
            const download = document.getElementById('download');
            vm.source.on('change', function () {
            const features = vm.source.getFeatures();
            const json = format.writeFeatures(features);
            console.log(json);
            download.href =
                'data:application/json;charset=utf-8,' + encodeURIComponent(json);
            });
            if(vm.occurrence_report_obj.location.geojson_point!=null){
                //vm.source.addFeature(vm.occurrence_report_obj.location.geojson_point)
                vm.source.clear();
                vm.point_data = new Point(vm.occurrence_report_obj.location.geojson_point);
                var feature = new Feature({
                    geometry: vm.point_data,
                    // You can also add properties to the feature here
                });
                vm.source.addFeature(feature);
            }
        },
    }
</script>

<style lang="css" scoped>
 @import '../../../../../static/boranga/css/map.css';
</style>

