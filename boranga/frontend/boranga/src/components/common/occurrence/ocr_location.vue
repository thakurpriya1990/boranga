<!-- eslint-disable vue/no-mutating-props -->
<template lang="html">
    <div id="ocrLocation">
        <FormSection
            :form-collapse="false"
            label="Location"
            Index="occurrence_report_location"
        >
            <div class="row mb-3">
                <div class="col">
                    <span class="text-danger">*</span>
                    <span class="text-muted"
                        >You must indicate the location for your occurrence
                        report</span
                    >
                </div>
            </div>
            <div class="row mb-3">
                <MapComponent
                    ref="component_map"
                    :key="componentMapKey"
                    class="me-3"
                    :context="occurrence_report_obj"
                    :is_external="is_external"
                    :point-features-supported="true"
                    :polygon-features-supported="isFauna == false"
                    :drawable="!isReadOnly"
                    :editable="!isReadOnly"
                    level="external"
                    style-by="assessor"
                    :map-info-text="
                        is_internal
                            ? ''
                            : 'Use the <b>draw</b> tool to draw the area of the report on the map.</br>You can <b>save</b> the report and continue at a later time.'
                    "
                    :selectable="true"
                    :coordinate-reference-systems="coordinateReferenceSystems"
                    :tile-layer-api-url="tileLayerApiUrl"
                    :query-layer-definition="{
                        name: 'query_layer',
                        title: 'Occurrence Report',
                        default: true,
                        can_edit: canEditGeometry,
                        api_url: proposalApiUrl,
                        ids: [occurrence_report_obj.id],
                        geometry_name: 'ocr_geometry',
                        collapse: false,
                        property_display_map: ocrPropertyDisplayMap,
                    }"
                    @refresh-from-response="refreshFromResponse"
                    @crs-select-search="searchForCRS"
                ></MapComponent>
            </div>

            <div class="row mb-3">
                <label for="" class="col-sm-3 control-label">Region:</label>
                <div class="col-sm-9">
                    <select
                        v-model="occurrence_report_obj.location.region_id"
                        :disabled="isReadOnly"
                        class="form-select"
                        @change="filterDistrict($event)"
                    >
                        <option
                            v-for="option in region_list"
                            :key="option.id"
                            :value="option.id"
                        >
                            {{ option.name }}
                        </option>
                    </select>
                </div>
            </div>
            <div class="row mb-3">
                <label for="" class="col-sm-3 control-label">District:</label>
                <div class="col-sm-9">
                    <select
                        v-model="occurrence_report_obj.location.district_id"
                        :disabled="isReadOnly"
                        class="form-select"
                    >
                        <option
                            v-for="option in filtered_district_list"
                            :key="option.id"
                            :value="option.id"
                        >
                            {{ option.name }}
                        </option>
                    </select>
                </div>
            </div>
            <div class="row mb-3">
                <label for="" class="col-sm-3 control-label fw-bold"
                    >Location Description: <span class="text-danger">*</span>
                    <HelpText
                        section_id="occurrence_report_location_description"
                /></label>
                <div class="col-sm-9">
                    <textarea
                        id="loc_description"
                        v-model="
                            occurrence_report_obj.location.location_description
                        "
                        :disabled="isReadOnly"
                        class="form-control"
                        rows="2"
                        placeholder=""
                    />
                </div>
            </div>
            <div class="row mb-3">
                <label for="" class="col-sm-3 control-label">Locality:</label>
                <div class="col-sm-9">
                    <textarea
                        id="locality"
                        v-model="occurrence_report_obj.location.locality"
                        :disabled="isReadOnly"
                        class="form-control"
                        rows="1"
                        placeholder=""
                    />
                </div>
            </div>
            <div class="row mb-3">
                <label for="" class="col-sm-3 control-label"
                    >Boundary Description:
                    <HelpText
                        section_id="occurrence_report_boundary_description"
                /></label>
                <div class="col-sm-9">
                    <textarea
                        id="boundary_descr"
                        v-model="
                            occurrence_report_obj.location.boundary_description
                        "
                        :disabled="isReadOnly"
                        class="form-control"
                        rows="2"
                        placeholder=""
                    />
                </div>
            </div>
            <!--<div class="row mb-3">
                <label class="col-sm-3 control-label">New Occurrence</label>
                <div class="col-sm-1">
                    <input
                        id="newOccurrenceYes"
                        v-model="occurrence_report_obj.location.new_occurrence"
                        :disabled="isReadOnly"
                        type="radio"
                        value="true"
                    />&nbsp;
                    <label for="newOccurrenceYes">Yes</label>
                </div>
                <div class="col-sm-1">
                    <input
                        id="newOccurrenceNo"
                        v-model="occurrence_report_obj.location.new_occurrence"
                        :disabled="isReadOnly"
                        type="radio"
                        value="false"
                    />&nbsp;
                    <label for="newOccurrenceNo">No</label>
                </div>
            </div>-->
            <div v-if="canAssess" class="row mb-3">
                <label for="" class="col-sm-3 control-label"
                    >Map Data Type</label
                >
                <div class="col-sm-6">
                    <label class="me-2">Boundary</label
                    ><input
                        disabled
                        type="radio"
                        :checked="occurrence_report_obj.location.has_boundary"
                        class="form-check-input me-2"
                    />
                    <label class="me-2">Point/s</label
                    ><input
                        disabled
                        type="radio"
                        :checked="occurrence_report_obj.location.has_points"
                        class="form-check-input me-2"
                    />
                </div>
            </div>

            <!--<div class="row mb-3">
                <label for="" class="col-sm-3 control-label">Datum:</label>
                <div class="col-sm-9">
                    <VueSelect
                        v-model="occurrence_report_obj.location.epsg_code"
                        :options="datum_list"
                        :reduce="(option) => option.id"
                        label="name"
                        :disabled="isReadOnly"
                        @search="searchForCRS"
                    >
                    </VueSelect>
                </div>
            </div>
            <div class="row mb-3">
                <label for="" class="col-sm-3 control-label"
                    >Point Coordinate :</label
                >
                <div class="col-sm-2">
                    <input
                        id="point_coord1"
                        :disabled="isReadOnly"
                        type="decimal"
                        class="form-control ocr_number"
                        placeholder=""
                    />
                </div>
                <div class="col-sm-2">
                    <input
                        id="point_coord2"
                        :disabled="isReadOnly"
                        type="decimal"
                        class="form-control ocr_number"
                        placeholder=""
                    />
                </div>
            </div>-->
            <div class="row mb-3">
                <label for="" class="col-sm-3 control-label"
                    >Coordinate Source:</label
                >
                <div class="col-sm-9">
                    <template v-if="!isReadOnly">
                        <template
                            v-if="
                                coordinate_source_list &&
                                coordinate_source_list.length > 0 &&
                                occurrence_report_obj.location
                                    .coordinate_source_id &&
                                !coordinate_source_list
                                    .map((d) => d.id)
                                    .includes(
                                        occurrence_report_obj.location
                                            .coordinate_source_id
                                    )
                            "
                        >
                            <input
                                v-if="
                                    occurrence_report_obj.location
                                        .coordinate_source
                                "
                                type="text"
                                class="form-control mb-3"
                                :value="
                                    occurrence_report_obj.location
                                        .coordinate_source + ' (Now Archived)'
                                "
                                disabled
                            />
                            <div class="mb-3 text-muted">
                                Change coordinate source to:
                            </div>
                        </template>
                        <select
                            v-model="
                                occurrence_report_obj.location
                                    .coordinate_source_id
                            "
                            class="form-select"
                        >
                            <option
                                v-for="option in coordinate_source_list"
                                :key="option.id"
                                :value="option.id"
                            >
                                {{ option.name }}
                            </option>
                        </select>
                    </template>
                    <template v-else>
                        <input
                            v-model="
                                occurrence_report_obj.location
                                    .coordinate_source_id
                            "
                            class="form-control"
                            type="text"
                            :disabled="isReadOnly"
                        />
                    </template>
                </div>
            </div>

            <!--
            <div v-if="canAssess" class="row mb-3">
                <label for="" class="col-sm-3 control-label"
                    >Buffer Radius(m) :</label
                >
                <div class="col-sm-6">
                    <input
                        id="buffer_radius"
                        v-model="occurrence_report_obj.location.buffer_radius"
                        :disabled="isReadOnly"
                        type="number"
                        class="form-control ocr_number"
                        placeholder=""
                        min="0"
                    />
                </div>
            </div>-->
            <div v-if="canAssess" class="row mb-3">
                <label
                    for=""
                    class="col-sm-3 control-label"
                    :class="
                        occurrence_report_obj.processing_status ==
                        constants.PROPOSAL_STATUS.WITH_ASSESSOR.TEXT
                            ? 'fw-bold'
                            : ''
                    "
                    >Location Accuracy:<span
                        v-if="
                            occurrence_report_obj.processing_status ==
                            constants.PROPOSAL_STATUS.WITH_ASSESSOR.TEXT
                        "
                        class="text-danger ms-1"
                        >*</span
                    ></label
                >
                <div class="col-sm-9">
                    <template v-if="!isReadOnly">
                        <template
                            v-if="
                                location_accuracy_list &&
                                location_accuracy_list.length > 0 &&
                                occurrence_report_obj.location
                                    .location_accuracy_id &&
                                !location_accuracy_list
                                    .map((d) => d.id)
                                    .includes(
                                        occurrence_report_obj.location
                                            .location_accuracy_id
                                    )
                            "
                        >
                            <input
                                v-if="
                                    occurrence_report_obj.location
                                        .location_accuracy
                                "
                                type="text"
                                class="form-control mb-3"
                                :value="
                                    occurrence_report_obj.location
                                        .location_accuracy + ' (Now Archived)'
                                "
                                disabled
                            />
                            <div class="mb-3 text-muted">
                                Change coordinate source to:
                            </div>
                        </template>
                        <select
                            v-model="
                                occurrence_report_obj.location
                                    .location_accuracy_id
                            "
                            class="form-select"
                        >
                            <option
                                v-for="option in location_accuracy_list"
                                :key="option.id"
                                :value="option.id"
                            >
                                {{ option.name }}
                            </option>
                        </select>
                    </template>
                    <template v-else>
                        <input
                            v-model="
                                occurrence_report_obj.location.location_accuracy
                            "
                            class="form-control"
                            type="text"
                            :disabled="isReadOnly"
                        />
                    </template>
                </div>
            </div>

            <div class="row mb-3">
                <div class="col-sm-12">
                    <!-- <button v-if="!updatingLocationDetails" class="pull-right btn btn-primary" @click.prevent="updateDetails()" :disabled="!can_update()">Update</button> -->
                    <button
                        v-if="!updatingLocationDetails"
                        class="btn btn-primary btn-sm float-end"
                        :disabled="isReadOnly"
                        @click.prevent="updateLocationDetails()"
                    >
                        Save Section
                    </button>
                    <button v-else disabled class="float-end btn btn-primary">
                        Saving
                        <span
                            class="spinner-border spinner-border-sm"
                            role="status"
                            aria-hidden="true"
                        ></span>
                        <span class="visually-hidden">Loading...</span>
                    </button>
                </div>
            </div>
        </FormSection>
    </div>
</template>

<script>
import { v4 as uuid } from 'uuid';
// import datatable from '@vue-utils/datatable.vue';
import FormSection from '@/components/forms/section_toggle.vue';
//import ObserverDatatable from './observer_datatable.vue';
import MapComponent from '../component_map.vue';
import HelpText from '@/components/common/help_text.vue';
import { api_endpoints, constants, helpers } from '@/utils/hooks';
// require("select2/dist/css/select2.min.css");
// require("select2-bootstrap-5-theme/dist/select2-bootstrap-5-theme.min.css")
// import { VueSelect } from 'vue-select';

export default {
    name: 'OCRLocation',
    components: {
        FormSection,
        HelpText,
        MapComponent,
        // VueSelect,
    },
    props: {
        occurrence_report_obj: {
            type: Object,
            required: true,
        },
        referral: {
            type: Object,
            required: false,
            default: () => {
                return {};
            },
        },
        is_external: {
            type: Boolean,
            default: false,
        },
        canEditStatus: {
            type: Boolean,
            default: true,
        },
        is_internal: {
            type: Boolean,
            default: false,
        },
    },
    emits: ['refreshFromResponse'],
    data: function () {
        let vm = this;
        return {
            uuid: null,
            constants: constants,
            isShowComment: false,
            //---to show fields related to Fauna
            isFauna:
                vm.occurrence_report_obj.group_type === 'fauna' ? true : false,
            isCommunity:
                vm.occurrence_report_obj.group_type === 'community'
                    ? true
                    : false,
            //----list of values dictionary

            region_list: [],
            district_list: [],
            filtered_district_list: [],

            deficiency_readonly:
                !this.is_external &&
                !this.occurrence_report_obj.can_user_edit &&
                this.occurrence_report_obj.assessor_mode.assessor_level ==
                    'assessor' &&
                this.occurrence_report_obj.assessor_mode.has_assessor_mode &&
                !this.occurrence_report_obj.assessor_mode
                    .status_without_assessor
                    ? false
                    : true,
            assessor_comment_readonly:
                !this.is_external &&
                !this.occurrence_report_obj.can_user_edit &&
                this.occurrence_report_obj.assessor_mode.assessor_level ==
                    'assessor' &&
                this.occurrence_report_obj.assessor_mode.has_assessor_mode &&
                !this.occurrence_report_obj.assessor_mode
                    .status_without_assessor
                    ? false
                    : true,

            updatingLocationDetails: false,
            listOfValuesDict: {},
            datum_list: [],
            coordinate_source_list: [],
            location_accuracy_list: [],
        };
    },
    computed: {
        deficiencyVisibility: function () {
            return this.occurrence_report_obj.assessor_mode.assessor_box_view;
        },
        assessorCommentVisibility: function () {
            return this.occurrence_report_obj.assessor_mode.assessor_box_view;
        },
        canAssess: function () {
            if (!this.is_external) {
                return this.occurrence_report_obj.assessor_mode
                    .assessor_can_assess;
            } else {
                return false;
            }
        },
        canEditGeometry: function () {
            const mode = this.occurrence_report_obj.assessor_mode || {};
            const assessorCanAssess =
                mode.assessor_level === 'assessor' &&
                mode.assessor_mode &&
                mode.assessor_can_assess;
            const refereeCanAssess =
                mode.assessor_level === 'referral' &&
                mode.assessor_mode &&
                mode.assessor_can_assess;

            // Allow referees to edit geometries, but commented for now
            const userCanEdit =
                this.occurrence_report_obj.can_user_edit ||
                assessorCanAssess ||
                refereeCanAssess;

            const readOnly = refereeCanAssess ? false : this.isReadOnly;
            if (!userCanEdit || readOnly) {
                return false;
            }
            if (this.is_external) {
                return ['Draft'].includes(
                    this.occurrence_report_obj.processing_status
                );
            } else if (this.is_internal) {
                return ['Draft', 'With Assessor', 'With Referral'].includes(
                    this.occurrence_report_obj.processing_status
                );
            } else {
                return (
                    refereeCanAssess &&
                    ['With Referral'].includes(
                        this.occurrence_report_obj.processing_status
                    )
                );
            }
        },
        isReadOnly: function () {
            return this.occurrence_report_obj.readonly;
        },
        componentMapKey: function () {
            return `component-map-${this.uuid}`;
        },
        csrf_token: function () {
            return helpers.getCookie('csrftoken');
        },
        coordinateReferenceSystems: function () {
            return this.datum_list;
        },
        tileLayerApiUrl: function () {
            return api_endpoints.tile_layer;
        },
        proposalApiUrl: function () {
            return api_endpoints.occurrence_report + '/list_for_map/';
        },
        ocrPropertyDisplayMap: function () {
            const displayMap = {
                label: 'Label', // Occurrence Report
                geometry_source: 'Geometry Source',
                occurrence_report_number: 'Identification Number',
                processing_status_display: 'Processing Status',
                drawn_by: 'Drawn By', // fullname
                updated_date: 'Last updated',
            };
            const mode = this.occurrence_report_obj.assessor_mode || {};
            const assessorCanAssess =
                mode.assessor_level === 'assessor' &&
                mode.assessor_mode &&
                mode.assessor_can_assess;
            if (assessorCanAssess) {
                displayMap['last_updated_by'] = 'Updated By';
                displayMap['lodgement_date_display'] = 'Lodgement Date';
                displayMap['locked'] = 'Locked';
            }

            return displayMap;
        },
    },
    watch: {},
    created: async function () {
        let vm = this;
        this.uuid = uuid();

        //------fetch list of values
        fetch(
            helpers.add_endpoint_join(
                api_endpoints.occurrence_report,
                `/location-list-of-values/?id=${vm.occurrence_report_obj.id}`
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

        const response = await fetch('/api/region_district_filter_dict/');
        vm.filterRegionDistrict = await response.json();
        vm.region_list = vm.filterRegionDistrict.region_list;
        vm.district_list = vm.filterRegionDistrict.district_list;
        vm.region_list.splice(0, 0, {
            id: null,
            name: null,
        });
        this.filterDistrict();
    },
    mounted: function () {
        let vm = this;
        this.$nextTick(() => {
            vm.eventListeners();
        });
    },
    methods: {
        filterDistrict: function (event) {
            this.$nextTick(() => {
                if (event) {
                    this.occurrence_report_obj.location.district_id = null; //-----to remove the previous selection
                }
                this.filtered_district_list = [];
                this.filtered_district_list = [
                    {
                        id: null,
                        name: '',
                        region_id: null,
                    },
                ];
                //---filter districts as per region selected
                for (let choice of this.district_list) {
                    if (
                        choice.region_id ===
                        this.occurrence_report_obj.location.region_id
                    ) {
                        this.filtered_district_list.push(choice);
                    }
                }
            });
        },
        eventListeners: function () {
            // eslint-disable-next-line no-unused-vars
            let vm = this;
        },
        toggleComment: function (updatedShowComment) {
            //this.isShowComment = ! this.isShowComment;
            this.isShowComment = updatedShowComment;
        },
        updateLocationDetails: function () {
            let vm = this;
            vm.updatingLocationDetails = true;

            let payload = { location: vm.occurrence_report_obj.location };
            // species_id added in updateLocationDetails as its not part of Location model but needs to be updated on button click
            payload.species_id = vm.occurrence_report_obj.species_id;
            // community_id added in updateLocationDetails as its not part of Location model but needs to be updated on button click
            payload.community_id = vm.occurrence_report_obj.community_id;

            // When in Entering Conditions status ApplicationForm might not be there
            // adding ocr_geometry from the map_component to payload
            if (vm.$refs.component_map) {
                payload.ocr_geometry = vm.$refs.component_map.getJSONFeatures();
                vm.$refs.component_map.setLoadingMap(true);
            }

            fetch(
                helpers.add_endpoint_json(
                    api_endpoints.occurrence_report,
                    vm.occurrence_report_obj.id + '/update_location_details'
                ),
                {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify(payload),
                }
            ).then(
                async (response) => {
                    vm.updatingLocationDetails = false;
                    vm.occurrence_report_obj.location = await response.json();
                    swal.fire({
                        title: 'Saved',
                        text: 'Location details have been saved',
                        icon: 'success',
                        customClass: {
                            confirmButton: 'btn btn-primary',
                        },
                    }).then(() => {
                        if (
                            vm.occurrence_report_obj.processing_status ==
                            'Unlocked'
                        ) {
                            vm.$router.go();
                        }
                    });
                    vm.$refs.component_map.forceToRefreshMap();
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
            this.uuid = uuid();
        },
        // eslint-disable-next-line no-unused-vars
        refreshFromResponse: function (data) {
            //this.proposal = Object.assign({}, data);
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
                    // Append to existing list of datum rather than overwrite and potentially lose prior search results which might create issues when setting a pre-selected value
                    const datum_ids = vm.datum_list.map((datum) => datum.id);
                    data.forEach((datum) => {
                        if (!datum_ids.includes(datum.id)) {
                            vm.datum_list.push(datum);
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

<style lang="css" scoped>
@import 'vue-select/dist/vue-select.css';

/*ul, li {
        zoom:1;
        display: inline;
    }*/
fieldset.scheduler-border {
    border: 1px groove #ddd !important;
    padding: 0 1.4em 1.4em 1.4em !important;
    margin: 0 0 1.5em 0 !important;
    -webkit-box-shadow: 0px 0px 0px 0px #000;
    box-shadow: 0px 0px 0px 0px #000;
}

legend.scheduler-border {
    width: inherit;
    /* Or auto */
    padding: 0 10px;
    /* To give a bit of padding on the left and right */
    border-bottom: none;
}

input[type='text'],
select {
    width: 100%;
    padding: 0.375rem 2.25rem 0.375rem 0.75rem;
}

input[type='number'] {
    width: 50%;
}

input.ocr_number {
    width: 20%;
}
</style>
