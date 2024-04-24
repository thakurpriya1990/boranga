<!-- eslint-disable vue/no-mutating-props -->
<template lang="html">
    <div id="ocrLocation">
        <FormSection
            :form-collapse="false"
            label="Location"
            Index="occurrence_report"
            :is-show-comment="isShowComment"
            :has_comment_value="has_comment_value"
            :display-comment-section="!is_external"
            @toggleComment="toggleComment($event)"
        >
            <div v-if="!is_external">
                <div v-show="isShowComment">
                    <!-- Assessor Deficiencies and comment box -->
                    <div v-if="deficiencyVisibility" class="row mb-3">
                        <label for="" class="col-sm-4 control-label"
                            >Deficiencies:</label
                        >
                        <div class="col-sm-8">
                            <textarea
                                id="assessor_deficiencies"
                                v-model="occurrence_report_obj.deficiency_data"
                                :disabled="deficiency_readonly"
                                class="form-control"
                                rows="3"
                                placeholder=""
                            />
                        </div>
                    </div>
                    <div v-if="assessorCommentVisibility" class="row mb-3">
                        <label for="" class="col-sm-4 control-label"
                            >Assessor:</label
                        >
                        <div class="col-sm-8">
                            <textarea
                                id="assessor_comment"
                                v-model="occurrence_report_obj.assessor_data"
                                :disabled="assessor_comment_readonly"
                                class="form-control"
                                rows="3"
                                placeholder=""
                            />
                        </div>
                    </div>
                    <!-- --- -->

                    <!-- Assessor Deficiencies and comment box -->
                    <div v-if="referral_comments_boxes.length > 0">
                        <div v-for="ref in referral_comments_boxes" :key="ref">
                            <div v-if="ref.box_view" class="row mb-3">
                                <label for="" class="col-sm-4 control-label"
                                    >{{ ref.label }}:</label
                                >
                                <div class="col-sm-8">
                                    <textarea
                                        v-if="!ref.readonly"
                                        v-model="referral.referral_comment"
                                        :disabled="ref.readonly"
                                        :name="ref.name"
                                        class="form-control"
                                        rows="3"
                                        placeholder=""
                                    />
                                    <textarea
                                        v-else
                                        :disabled="ref.readonly"
                                        :name="ref.name"
                                        :value="ref.value"
                                        class="form-control"
                                        rows=""
                                        placeholder=""
                                    />
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
            <!--  -->
            <div class="row mb-3">
                <MapComponent
                    ref="component_map"
                    :key="componentMapKey"
                    class="me-3"
                    :context="occurrence_report_obj"
                    :proposal-ids="[occurrence_report_obj.id]"
                    :is_external="is_external"
                    :point-features-supported="true"
                    :polygon-features-supported="isFauna == false"
                    :drawable="true"
                    :editable="true"
                    level="external"
                    style-by="assessor"
                    :map-info-text="
                        is_internal
                            ? ''
                            : 'Use the <b>draw</b> tool to draw the area of the report on the map.</br>You can <b>save</b> the report and continue at a later time.'
                    "
                    :selectable="true"
                    :coordinate-reference-systems="coordinateReferenceSystems"
                    @validate-feature="validateFeature.bind(this)()"
                    @refreshFromResponse="refreshFromResponse"
                    @crs-select-search="searchForCRS"
                ></MapComponent>
            </div>

            <div v-show="!isCommunity">
                <div class="row mb-3">
                    <label for="" class="col-sm-3 control-label"
                        >Scientific Name:</label
                    >
                    <div :id="select_scientific_name" class="col-sm-9">
                        <select
                            :id="scientific_name_lookup"
                            :ref="scientific_name_lookup"
                            :disabled="isReadOnly"
                            :name="scientific_name_lookup"
                            class="form-control"
                        />
                    </div>
                </div>
                <div class="row mb-3">
                    <label for="" class="col-sm-3 control-label"></label>
                    <div class="col-sm-9">
                        <textarea
                            id="species_display"
                            v-model="species_display"
                            disabled
                            class="form-control"
                            rows="2"
                        />
                    </div>
                </div>
                <div class="row mb-3">
                    <label for="" class="col-sm-3 control-label"
                        >Previous Name:</label
                    >
                    <div class="col-sm-9">
                        <input
                            id="previous_name"
                            v-model="taxon_previous_name"
                            readonly
                            type="text"
                            class="form-control"
                            placeholder=""
                        />
                    </div>
                </div>
            </div>

            <div v-show="isCommunity">
                <div class="row mb-3">
                    <label for="" class="col-sm-3 control-label"
                        >Community Name:</label
                    >
                    <div :id="select_community_name" class="col-sm-9">
                        <select
                            :id="community_name_lookup"
                            :ref="community_name_lookup"
                            :disabled="isReadOnly"
                            :name="community_name_lookup"
                            class="form-control"
                        />
                    </div>
                </div>
                <div class="row mb-3">
                    <label for="" class="col-sm-3 control-label"></label>
                    <div class="col-sm-9">
                        <textarea
                            id="community_display"
                            v-model="community_display"
                            disabled
                            class="form-control"
                            rows="2"
                        />
                    </div>
                </div>
            </div>

            <div class="row mb-3">
                <label for="" class="col-sm-3 control-label"
                    >Observation Date:</label
                >
                <div class="col-sm-9">
                    <input
                        v-model="
                            occurrence_report_obj.location.observation_date
                        "
                        :disabled="isReadOnly"
                        type="datetime-local"
                        class="form-control"
                        name="start_date"
                    />
                </div>
            </div>
            <!-- ------------Observer Detail section -->

            <ObserverDatatable
                ref="observer_datatable"
                :occurrence_report_obj="occurrence_report_obj"
                :is_external="is_external"
                :is-read-only="isReadOnly"
            ></ObserverDatatable>

            <!-- -------------------------------- -->
            <div class="row mb-3">
                <label for="" class="col-sm-3 control-label"
                    >Location Description:</label
                >
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
                <label for="" class="col-sm-3 control-label"
                    >Boundary Description:</label
                >
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
            <div class="row mb-3">
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
            </div>
            <div class="row mb-3">
                <label for="" class="col-sm-3 control-label"
                    >Boundary(m) :</label
                >
                <div class="col-sm-6">
                    <input
                        id="boundary"
                        v-model="occurrence_report_obj.location.boundary"
                        :disabled="isReadOnly"
                        type="number"
                        class="form-control ocr_number"
                        placeholder=""
                        min="0"
                    />
                </div>
            </div>
            <div class="row mb-3">
                <label class="col-sm-3 control-label">Mapped Boundary</label>
                <div class="col-sm-1">
                    <input
                        id="mapBoundaryYes"
                        v-model="occurrence_report_obj.location.mapped_boundary"
                        :disabled="isReadOnly"
                        type="radio"
                        value="true"
                    />&nbsp;
                    <label for="mapBoundaryYes">Yes</label>
                </div>
                <div class="col-sm-1">
                    <input
                        id="mapBoundaryNo"
                        v-model="occurrence_report_obj.location.mapped_boundary"
                        :disabled="isReadOnly"
                        type="radio"
                        value="false"
                    />&nbsp;
                    <label for="mapBoundaryNo">No</label>
                </div>
            </div>
            <div class="row mb-3">
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
            </div>
            <div class="row mb-3">
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
                <!-- <div class="col-sm-3">
                    <button :disabled="isReadOnly" type="button" class="btn btn-primary btn-sm pull-left me-2">
                        Map
                    </button>
                    <button :disabled="isReadOnly" type="button" class="btn btn-primary btn-sm pull-left me-2">
                        View
                    </button>
                </div> -->
            </div>
            <div class="row mb-3">
                <label for="" class="col-sm-3 control-label"
                    >Coordination Source:</label
                >
                <div class="col-sm-9">
                    <select
                        v-model="
                            occurrence_report_obj.location
                                .coordination_source_id
                        "
                        :disabled="isReadOnly"
                        class="form-select"
                    >
                        <option
                            v-for="option in coordination_source_list"
                            :key="option.id"
                            :value="option.id"
                        >
                            {{ option.name }}
                        </option>
                    </select>
                </div>
            </div>
            <div class="row mb-3">
                <label for="" class="col-sm-3 control-label"
                    >Location Accuracy/Certainty:</label
                >
                <div class="col-sm-9">
                    <select
                        v-model="
                            occurrence_report_obj.location.location_accuracy_id
                        "
                        :disabled="isReadOnly"
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
                </div>
            </div>

            <div class="row mb-3">
                <div class="col-sm-12">
                    <!-- <button v-if="!updatingLocationDetails" class="pull-right btn btn-primary" @click.prevent="updateDetails()" :disabled="!can_update()">Update</button> -->
                    <button
                        v-if="!updatingLocationDetails"
                        class="btn btn-primary btn-sm float-end"
                        @click.prevent="updateLocationDetails()"
                    >
                        Update
                    </button>
                    <button v-else disabled class="float-end btn btn-primary">
                        <i class="fa fa-spin fa-spinner"></i>&nbsp;Updating
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
import ObserverDatatable from './observer_datatable.vue';
import MapComponent from '../component_map.vue';
import { api_endpoints, helpers } from '@/utils/hooks';
// require("select2/dist/css/select2.min.css");
// require("select2-bootstrap-5-theme/dist/select2-bootstrap-5-theme.min.css")
import { VueSelect } from 'vue-select';

export default {
    name: 'OCRLocation',
    components: {
        FormSection,
        ObserverDatatable,
        MapComponent,
        VueSelect,
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
            scientific_name_lookup:
                'scientific_name_lookup' + vm.occurrence_report_obj.id,
            select_scientific_name:
                'select_scientific_name' + vm.occurrence_report_obj.id,
            community_name_lookup: 'community_name_lookup' + vm._uid,
            select_community_name: 'select_community_name' + vm._uid,
            isShowComment: false,
            //---to show fields related to Fauna
            isFauna:
                vm.occurrence_report_obj.group_type === 'fauna' ? true : false,
            isCommunity:
                vm.occurrence_report_obj.group_type === 'community'
                    ? true
                    : false,
            //----list of values dictionary
            cs_profile_dict: {},
            species_list: [],
            referral_comments_boxes: [],
            // to display the species selected
            species_display: '',
            community_display: '',
            taxon_previous_name: '',
            //---Comment box attributes

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
            coordination_source_list: [],
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
        has_comment_value: function () {
            let has_value = false;
            // TODO need to add assessor comment value as well
            for (let i = 0; i < this.referral_comments_boxes.length; i++) {
                if (Object.hasOwn(this.referral_comments_boxes[i], 'value')) {
                    if (
                        this.referral_comments_boxes[i].value != null &&
                        this.referral_comments_boxes[i].value != undefined &&
                        this.referral_comments_boxes[i].value != ''
                    ) {
                        has_value = true;
                    }
                }
            }
            return has_value;
        },
        isReadOnly: function () {
            let action = this.$route.query.action;
            if (
                action === 'edit' &&
                this.occurrence_report_obj &&
                this.occurrence_report_obj.assessor_mode.has_assessor_mode
            ) {
                return false;
            } else {
                return this.occurrence_report_obj.readonly;
            }
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
    },
    watch: {},
    created: async function () {
        let vm = this;
        this.uuid = uuid();
        //------fetch list of values according to action
        let action = this.$route.query.action;
        let dict_url =
            action == 'view'
                ? api_endpoints.cs_profile_dict +
                  '?group_type=' +
                  vm.occurrence_report_obj.group_type +
                  '&action=' +
                  action
                : api_endpoints.cs_profile_dict +
                  '?group_type=' +
                  vm.occurrence_report_obj.group_type;
        vm.$http.get(dict_url).then(
            (response) => {
                vm.cs_profile_dict = response.body;
                vm.species_list = vm.cs_profile_dict.species_list;
                this.getSpeciesDisplay();

                vm.community_list = vm.cs_profile_dict.community_list;
                this.getCommunityDisplay();
            },
            (error) => {
                console.log(error);
            }
        );

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
                vm.coordination_source_list =
                    vm.listOfValuesDict.coordination_source_list;
                vm.coordination_source_list.splice(0, 0, {
                    id: null,
                    name: null,
                });
                vm.location_accuracy_list =
                    vm.listOfValuesDict.location_accuracy_list;
                vm.location_accuracy_list.splice(0, 0, {
                    id: null,
                    name: null,
                });
                if (!vm.is_external) {
                    this.generateReferralCommentBoxes();
                }
            })
            .catch((error) => {
                console.error('Error fetching location values list:', error);
            });
    },
    mounted: function () {
        let vm = this;
        this.$nextTick(() => {
            vm.eventListeners();
            vm.initialiseScientificNameLookup();
            vm.initialiseCommunityNameLookup();
        });
    },
    methods: {
        initialiseScientificNameLookup: function () {
            let vm = this;
            $(vm.$refs[vm.scientific_name_lookup])
                .select2({
                    minimumInputLength: 2,
                    dropdownParent: $('#' + vm.select_scientific_name),
                    theme: 'bootstrap-5',
                    allowClear: true,
                    placeholder: 'Select Scientific Name',
                    ajax: {
                        url: api_endpoints.scientific_name_lookup,
                        dataType: 'json',
                        data: function (params) {
                            var query = {
                                term: params.term,
                                type: 'public',
                                group_type_id:
                                    vm.occurrence_report_obj.group_type_id,
                                cs_species: true,
                                cs_species_status:
                                    vm.occurrence_report_obj.processing_status,
                            };
                            return query;
                        },
                        // results: function (data, page) { // parse the results into the format expected by Select2.
                        //     // since we are using custom formatting functions we do not need to alter remote JSON data
                        //     return {results: data};
                        // },
                    },
                })
                .on('select2:select', function (e) {
                    // eslint-disable-next-line no-unused-vars
                    var selected = $(e.currentTarget);
                    let data = e.params.data.id;
                    vm.occurrence_report_obj.species_id = data;
                    vm.species_display = e.params.data.text;
                    vm.taxon_previous_name = e.params.data.taxon_previous_name;
                })
                .on('select2:unselect', function (e) {
                    // eslint-disable-next-line no-unused-vars
                    var selected = $(e.currentTarget);
                    vm.occurrence_report_obj.species_id = null;
                    vm.species_display = '';
                    vm.taxon_previous_name = '';
                })
                // eslint-disable-next-line no-unused-vars
                .on('select2:open', function (e) {
                    const searchField = $(
                        '[aria-controls="select2-' +
                            vm.scientific_name_lookup +
                            '-results"]'
                    );
                    // move focus to select2 field
                    searchField[0].focus();
                });
        },
        getSpeciesDisplay: function () {
            let vm = this;
            for (let choice of vm.species_list) {
                if (choice.id === vm.occurrence_report_obj.species_id) {
                    const newOption = new Option(
                        choice.name,
                        choice.id,
                        false,
                        true
                    );
                    $('#' + vm.scientific_name_lookup).append(newOption);
                    vm.species_display = choice.name;
                    vm.taxon_previous_name = choice.taxon_previous_name;
                }
            }
        },
        initialiseCommunityNameLookup: function () {
            let vm = this;
            $(vm.$refs[vm.community_name_lookup])
                .select2({
                    minimumInputLength: 2,
                    dropdownParent: $('#' + vm.select_community_name),
                    theme: 'bootstrap-5',
                    allowClear: true,
                    placeholder: 'Select Community Name',
                    ajax: {
                        url: api_endpoints.community_name_lookup,
                        dataType: 'json',
                        data: function (params) {
                            var query = {
                                term: params.term,
                                type: 'public',
                                cs_community: true,
                            };
                            return query;
                        },
                        // results: function (data, page) { // parse the results into the format expected by Select2.
                        //     // since we are using custom formatting functions we do not need to alter remote JSON data
                        //     return {results: data};
                        // },
                    },
                })
                .on('select2:select', function (e) {
                    // eslint-disable-next-line no-unused-vars
                    var selected = $(e.currentTarget);
                    let data = e.params.data.id;
                    vm.occurrence_report_obj.community_id = data;
                    vm.community_display = e.params.data.text;
                })
                .on('select2:unselect', function (e) {
                    // eslint-disable-next-line no-unused-vars
                    var selected = $(e.currentTarget);
                    vm.occurrence_report_obj.community_id = null;
                    vm.community_display = '';
                })
                // eslint-disable-next-line no-unused-vars
                .on('select2:open', function (e) {
                    const searchField = $(
                        '[aria-controls="select2-' +
                            vm.community_name_lookup +
                            '-results"]'
                    );
                    // move focus to select2 field
                    searchField[0].focus();
                });
        },
        getCommunityDisplay: function () {
            for (let choice of this.community_list) {
                if (choice.id === this.occurrence_report_obj.community_id) {
                    const newOption = new Option(
                        choice.name,
                        choice.id,
                        false,
                        true
                    );
                    $('#' + this.community_name_lookup).append(newOption);
                    this.community_display = choice.name;
                }
            }
        },
        generateReferralCommentBoxes: function () {
            var box_visibility =
                this.occurrence_report_obj.assessor_mode.assessor_box_view;
            var assessor_mode =
                this.occurrence_report_obj.assessor_mode.assessor_level;
            if (!this.occurrence_report_obj.can_user_edit) {
                // eslint-disable-next-line no-unused-vars
                let current_referral_present = false;
                $.each(this.occurrence_report_obj.latest_referrals, (i, v) => {
                    var referral_name = `comment-field-Referral-${v.referral_obj.email}`;
                    var referral_visibility =
                        assessor_mode == 'referral' &&
                        this.occurrence_report_obj.assessor_mode
                            .assessor_can_assess &&
                        this.referral.referral == v.referral_obj.id
                            ? false
                            : true;
                    var referral_label = `${v.referral_obj.fullname}`;
                    var referral_comment_val = `${v.referral_comment}`;
                    this.referral_comments_boxes.push({
                        box_view: box_visibility,
                        name: referral_name,
                        label: referral_label,
                        readonly: referral_visibility,
                        value: referral_comment_val,
                    });
                });
            }
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
            }

            // const res = await fetch(vm.proposal_form_url, {
            //     body: JSON.stringify(payload),
            //     method: 'POST',
            // });

            vm.$http
                .post(
                    helpers.add_endpoint_json(
                        api_endpoints.occurrence_report,
                        vm.occurrence_report_obj.id + '/update_location_details'
                    ),
                    JSON.stringify(payload),
                    {
                        emulateJSON: true,
                    }
                )
                .then(
                    (response) => {
                        vm.updatingLocationDetails = false;
                        vm.occurrence_report_obj.location = response.body;
                        swal.fire({
                            title: 'Saved',
                            text: 'Location details have been saved',
                            icon: 'success',
                            confirmButtonColor: '#226fbb',
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
                            confirmButtonColor: '#226fbb',
                        });
                        vm.updatingLocationDetails = false;
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
    width: inherit; /* Or auto */
    padding: 0 10px; /* To give a bit of padding on the left and right */
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
