<template lang="html">
    <div id="habitat">
        <FormSection :formCollapse="false" label="Habitat Composition" :Index="habitatCompositionBody">
            <div class="row mb-3">
                <label for="" class="col-sm-3 control-label">Land Form:</label>
                <div class="col-sm-9">
                    <select :disabled="isReadOnly" style="width:100%;" class="form-select input-sm"
                        ref="land_form_select" v-model="occurrence_report_obj.habitat_composition.land_form">
                        <option v-for="option in land_form_list" :value="option.id" :key="option.id">
                            {{ option.name }}
                        </option>
                    </select>
                </div>
            </div>
            <div class="row mb-3">
                <label for="" class="col-sm-3 control-label">Rock Type:</label>
                <div class="col-sm-9">
                    <template v-if="!isReadOnly">
                        <template
                            v-if="rock_type_list && rock_type_list.length > 0 && occurrence_report_obj.habitat_composition.rock_type_id && !rock_type_list.map((d) => d.id).includes(occurrence_report_obj.habitat_composition.rock_type_id)">
                            <input type="text" v-if="occurrence_report_obj.habitat_composition.rock_type" class="form-control mb-3"
                                :value="occurrence_report_obj.habitat_composition.rock_type + ' (Now Archived)'" disabled />
                            <div class="mb-3 text-muted">
                                Change rock type to:
                            </div>
                        </template>
                        <select class="form-select" v-model="occurrence_report_obj.habitat_composition.rock_type_id">
                            <option v-for="rock_type in rock_type_list" :value="rock_type.id" v-bind:key="rock_type.id">
                                {{ rock_type.name }}
                            </option>
                        </select>
                    </template>
                    <template v-else>
                        <input class="form-control" type="text" :disabled="isReadOnly" v-model="occurrence_report_obj.habitat_composition.rock_type" />
                    </template>
                </div>
            </div>
            <div class="row mb-3">
                <label for="" class="col-sm-3 control-label">Loose Rock % :</label>
                <div class="col-sm-6">
                    <input :disabled="isReadOnly" type="number" class="form-control" id="loose_rock_per" placeholder=""
                        min="0" max="100" v-model="occurrence_report_obj.habitat_composition.loose_rock_percent" />
                </div>
            </div>
            <div class="row mb-3">
                <label for="" class="col-sm-3 control-label">Soil Type:</label>
                <div class="col-sm-9">
                    <template v-if="!isReadOnly">
                        <template
                            v-if="soil_type_list && soil_type_list.length > 0 && occurrence_report_obj.habitat_composition.soil_type_id && !soil_type_list.map((d) => d.id).includes(occurrence_report_obj.habitat_composition.soil_type_id)">
                            <input type="text" v-if="occurrence_report_obj.habitat_composition.soil_type" class="form-control mb-3"
                                :value="occurrence_report_obj.habitat_composition.soil_type + ' (Now Archived)'" disabled />
                            <div class="mb-3 text-muted">
                                Change soil type to:
                            </div>
                        </template>
                        <select class="form-select" v-model="occurrence_report_obj.habitat_composition.soil_type_id">
                            <option v-for="soil_type in soil_type_list" :value="soil_type.id" v-bind:key="soil_type.id">
                                {{ soil_type.name }}
                            </option>
                        </select>
                    </template>
                    <template v-else>
                        <input class="form-control" type="text" :disabled="isReadOnly" v-model="occurrence_report_obj.habitat_composition.soil_type" />
                    </template>
                </div>
            </div>
            <div class="row mb-3">
                <label for="" class="col-sm-3 control-label">Soil Colour:</label>
                <div class="col-sm-9">
                    <template v-if="!isReadOnly">
                        <template
                            v-if="soil_colour_list && soil_colour_list.length > 0 && occurrence_report_obj.habitat_composition.soil_colour_id && !soil_colour_list.map((d) => d.id).includes(occurrence_report_obj.habitat_composition.soil_colour_id)">
                            <input colour="text" v-if="occurrence_report_obj.habitat_composition.soil_colour" class="form-control mb-3"
                                :value="occurrence_report_obj.habitat_composition.soil_colour + ' (Now Archived)'" disabled />
                            <div class="mb-3 text-muted">
                                Change soil colour to:
                            </div>
                        </template>
                        <select class="form-select" v-model="occurrence_report_obj.habitat_composition.soil_colour_id">
                            <option v-for="soil_colour in soil_colour_list" :value="soil_colour.id" v-bind:key="soil_colour.id">
                                {{ soil_colour.name }}
                            </option>
                        </select>
                    </template>
                    <template v-else>
                        <input class="form-control" colour="text" :disabled="isReadOnly" v-model="occurrence_report_obj.habitat_composition.soil_colour" />
                    </template>
                </div>
            </div>
            <div class="row mb-3">
                <label for="" class="col-sm-3 control-label">Soil Condition:</label>
                <div class="col-sm-9">
                    <template v-if="!isReadOnly">
                        <template
                            v-if="soil_condition_list && soil_condition_list.length > 0 && occurrence_report_obj.habitat_composition.soil_condition_id && !soil_condition_list.map((d) => d.id).includes(occurrence_report_obj.habitat_composition.soil_condition_id)">
                            <input type="text" v-if="occurrence_report_obj.habitat_composition.soil_condition" class="form-control mb-3"
                                :value="occurrence_report_obj.habitat_composition.soil_condition + ' (Now Archived)'" disabled />
                            <div class="mb-3 text-muted">
                                Change soil condition to:
                            </div>
                        </template>
                        <select class="form-select" v-model="occurrence_report_obj.habitat_composition.soil_condition_id">
                            <option v-for="soil_condition in soil_condition_list" :value="soil_condition.id" v-bind:key="soil_condition.id">
                                {{ soil_condition.name }}
                            </option>
                        </select>
                    </template>
                    <template v-else>
                        <input class="form-control" type="text" :disabled="isReadOnly" v-model="occurrence_report_obj.habitat_composition.soil_condition" />
                    </template>
                </div>
            </div>
            <div class="row mb-3">
                <label for="" class="col-sm-3 control-label">Drainage:</label>
                <div class="col-sm-9">
                    <template v-if="!isReadOnly">
                        <template
                            v-if="drainage_list && drainage_list.length > 0 && occurrence_report_obj.habitat_composition.drainage_id && !drainage_list.map((d) => d.id).includes(occurrence_report_obj.habitat_composition.drainage_id)">
                            <input type="text" v-if="occurrence_report_obj.habitat_composition.drainage"
                                class="form-control mb-3"
                                :value="occurrence_report_obj.habitat_composition.drainage + ' (Now Archived)'"
                                disabled />
                            <div class="mb-3 text-muted">
                                Change drainage to:
                            </div>
                        </template>
                        <select class="form-select" v-model="occurrence_report_obj.habitat_composition.drainage_id">
                            <option v-for="drainage in drainage_list" :value="drainage.id"
                                v-bind:key="drainage.id">
                                {{ drainage.name }}
                            </option>
                        </select>
                    </template>
                    <template v-else>
                        <input class="form-control" type="text" :disabled="isReadOnly"
                            v-model="occurrence_report_obj.habitat_composition.drainage" />
                    </template>
                </div>
            </div>
            <div class="row mb-3">
                <label for="" class="col-sm-3 control-label">Water Quality:</label>
                <div class="col-sm-9">
                    <textarea :disabled="isReadOnly" type="text" class="form-control" placeholder=""
                        v-model="occurrence_report_obj.habitat_composition.water_quality" />
                </div>
            </div>
            <div class="row mb-3">
                <label for="" class="col-sm-3 control-label">Habitat Notes:</label>
                <div class="col-sm-9">
                    <textarea :disabled="isReadOnly" type="text" class="form-control" placeholder=""
                        v-model="occurrence_report_obj.habitat_composition.habitat_notes" />
                </div>
            </div>
            <div class="row mb-3">
                <div class="col-sm-12">
                    <!-- <button v-if="!updatingHabitatCompositionDetails" class="pull-right btn btn-primary" @click.prevent="updateDetails()" :disabled="!can_update()">Update</button> -->
                    <button v-if="!updatingHabitatCompositionDetails" :disabled="isReadOnly"
                        class="btn btn-primary btn-sm float-end"
                        @click.prevent="updateHabitatCompositionDetails()">Update</button>
                    <button v-else disabled class="float-end btn btn-primary">Updating <span
                            class="spinner-border spinner-border-sm" role="status" aria-hidden="true"></span>
                        <span class="visually-hidden">Loading...</span></button>
                </div>
            </div>
        </FormSection>
        <FormSection :formCollapse="false" label="Habitat Condition" :Index="habitatConditionBody">
            <label for="" class="col-lg-3 control-label fs-5 fw-bold">Keighery Scale</label>
            <div class="row mb-3">
                <label for="" class="col-sm-3 control-label">Pristine %:</label>
                <div class="col-sm-6">
                    <input :disabled="isReadOnly" type="number" class="form-control ocr_number" id="pristine"
                        placeholder="" min="0" max="100" v-model="occurrence_report_obj.habitat_condition.pristine"
                        @change.prevent="calcKeigheryTotal()" />
                </div>
            </div>
            <div class="row mb-3">
                <label for="" class="col-sm-3 control-label">Excellent %:</label>
                <div class="col-sm-6">
                    <input :disabled="isReadOnly" type="number" class="form-control ocr_number" id="excellent"
                        placeholder="" min="0" max="100" v-model="occurrence_report_obj.habitat_condition.excellent"
                        @change.prevent="calcKeigheryTotal()" />
                </div>
            </div>
            <div class="row mb-3">
                <label for="" class="col-sm-3 control-label">Very Good %:</label>
                <div class="col-sm-6">
                    <input :disabled="isReadOnly" type="number" class="form-control ocr_number" id="very_good"
                        placeholder="" min="0" max="100" v-model="occurrence_report_obj.habitat_condition.very_good"
                        @change.prevent="calcKeigheryTotal()" />
                </div>
            </div>
            <div class="row mb-3">
                <label for="" class="col-sm-3 control-label">Good %:</label>
                <div class="col-sm-6">
                    <input :disabled="isReadOnly" type="number" class="form-control ocr_number" id="good" placeholder=""
                        min="0" max="100" v-model="occurrence_report_obj.habitat_condition.good"
                        @change.prevent="calcKeigheryTotal()" />
                </div>
            </div>
            <div class="row mb-3">
                <label for="" class="col-sm-3 control-label">Degraded %:</label>
                <div class="col-sm-6">
                    <input :disabled="isReadOnly" type="number" class="form-control ocr_number" id="degraded"
                        placeholder="" min="0" max="100" v-model="occurrence_report_obj.habitat_condition.degraded"
                        @change.prevent="calcKeigheryTotal()" />
                </div>
            </div>
            <div class="row mb-3">
                <label for="" class="col-sm-3 control-label">Completely Degraded %:</label>
                <div class="col-sm-6">
                    <input :disabled="isReadOnly" type="number" class="form-control ocr_number" id="completely_degraded"
                        placeholder="" min="0" max="100"
                        v-model="occurrence_report_obj.habitat_condition.completely_degraded"
                        @change.prevent="calcKeigheryTotal()" />
                </div>
            </div>
            <div class="row mb-3">
                <label for="" class="col-sm-3 control-label"></label>
                <div class="col-sm-6">
                    <input readonly type="text" class="form-control ocr_number" id="habitat_cond_sum" placeholder=""
                        v-model="habitat_cond_sum" />
                </div>
            </div>
            <div v-if="occurrence_report_obj.group_type=='community'" class="row mb-3">
                <label for="" class="col-sm-3 control-label">Count Date: </label>
                <div class="col-sm-9">
                    <input v-model="occurrence_report_obj.habitat_condition.count_date
                        " :disabled="true" type="datetime-local" class="form-control" name="count_date" />
                </div>
            </div>
            <div class="row mb-3">
                <div class="col-sm-12">
                    <button v-if="!updatingHabitatConditionDetails" :disabled="isReadOnly"
                        class="btn btn-primary btn-sm float-end"
                        @click.prevent="updateHabitatConditionDetails()">Update</button>
                    <button v-else disabled class="float-end btn btn-primary">Updating <span
                            class="spinner-border spinner-border-sm" role="status" aria-hidden="true"></span>
                        <span class="visually-hidden">Loading...</span></button>
                </div>
            </div>
        </FormSection>
        <FormSection :formCollapse="false" label="Vegetation Structure" :Index="vegetationStructureBody">
            <div class="row mb-3">
                <label for="" class="col-sm-6 control-label">Vegetation Structure - Layer 1:</label>
                <div class="col-sm-9">
                    <textarea :disabled="isReadOnly" type="text" row="2" class="form-control"
                        id="vegetation_structure_text_1" placeholder=""
                        v-model="occurrence_report_obj.vegetation_structure.vegetation_structure_layer_one" />
                </div>
            </div>
            <div class="row mb-3">
                <label for="" class="col-sm-6 control-label">Vegetation Structure - Layer 2:</label>
                <div class="col-sm-9">
                    <textarea :disabled="isReadOnly" type="text" row="2" class="form-control"
                        id="vegetation_structure_text_2" placeholder=""
                        v-model="occurrence_report_obj.vegetation_structure.vegetation_structure_layer_two" />
                </div>
            </div>
            <div class="row mb-3">
                <label for="" class="col-sm-6 control-label">Vegetation Structure - Layer 3:</label>
                <div class="col-sm-9">
                    <textarea :disabled="isReadOnly" type="text" row="2" class="form-control"
                        id="vegetation_structure_text_3" placeholder=""
                        v-model="occurrence_report_obj.vegetation_structure.vegetation_structure_layer_three" />
                </div>
            </div>
            <div class="row mb-3">
                <label for="" class="col-sm-6 control-label">Vegetation Structure - Layer 4:</label>
                <div class="col-sm-9">
                    <textarea :disabled="isReadOnly" type="text" row="2" class="form-control"
                        id="vegetation_structure_text_4" placeholder=""
                        v-model="occurrence_report_obj.vegetation_structure.vegetation_structure_layer_four" />
                </div>
            </div>
            <div class="row mb-3">
                <div class="col-sm-12">
                    <button v-if="!updatingVegetationStructure" :disabled="isReadOnly"
                        class="btn btn-primary btn-sm float-end"
                        @click.prevent="updateVegetationStructure()">Update</button>
                    <button v-else disabled class="float-end btn btn-primary">Updating <span
                            class="spinner-border spinner-border-sm" role="status" aria-hidden="true"></span>
                        <span class="visually-hidden">Loading...</span></button>
                </div>
            </div>
        </FormSection>
        <FormSection :formCollapse="false" label="Fire History" :Index="fireHistoryBody">
            <label for="" class="col-lg-3 control-label fs-5 fw-bold">Last Fire History</label>
            <div class="row mb-3">
                <label for="" class="col-sm-3 control-label">Last Fire Estimate:</label>
                <div class="col-sm-9">
                    <input :disabled="isReadOnly" type="month" class="form-control" name="last_fire_date"
                        ref="last_fire_date" @change="checkDate()"
                        v-model="occurrence_report_obj.fire_history.last_fire_estimate" />
                </div>
            </div>
            <div class="row mb-3">
                <label for="" class="col-sm-3 control-label">Intensity:</label>
                <div class="col-sm-9">
                    <template v-if="!isReadOnly">
                        <template
                            v-if="intensity_list && intensity_list.length > 0 && occurrence_report_obj.fire_history.intensity_id && !intensity_list.map((d) => d.id).includes(occurrence_report_obj.fire_history.intensity_id)">
                            <input type="text" v-if="occurrence_report_obj.fire_history.intensity" class="form-control mb-3"
                                :value="occurrence_report_obj.fire_history.intensity + ' (Now Archived)'" disabled />
                            <div class="mb-3 text-muted">
                                Change intensity to:
                            </div>
                        </template>
                        <select class="form-select" v-model="occurrence_report_obj.fire_history.intensity_id">
                            <option v-for="intensity in intensity_list" :value="intensity.id" v-bind:key="intensity.id">
                                {{ intensity.name }}
                            </option>
                        </select>
                    </template>
                    <template v-else>
                        <input class="form-control" type="text" :disabled="isReadOnly"
                            v-model="occurrence_report_obj.fire_history.intensity" />
                    </template>
                </div>
            </div>
            <div class="row mb-3">
                <label for="" class="col-sm-3 control-label">Comments :</label>
                <div class="col-sm-9">
                    <textarea :disabled="isReadOnly" type="text" row="2" class="form-control" id="fire_history_comment"
                        placeholder="" v-model="occurrence_report_obj.fire_history.comment" />
                </div>
            </div>
            <div class="row mb-3">
                <div class="col-sm-12">
                    <button v-if="!updatingFireHistoryDetails" :disabled="isReadOnly"
                        class="btn btn-primary btn-sm float-end"
                        @click.prevent="updateFireHistoryDetails()">Update</button>
                    <button v-else disabled class="float-end btn btn-primary">Updating <span
                            class="spinner-border spinner-border-sm" role="status" aria-hidden="true"></span>
                        <span class="visually-hidden">Loading...</span></button>
                </div>
            </div>
        </FormSection>
        <FormSection :formCollapse="false" label="Associated Species" :Index="associatedSpeciesBody">
            <RelatedSpecies :isReadOnly="isReadOnly" ref="related_species"
                :occurrence_report_obj=occurrence_report_obj />
            <div class="row mb-3">
                <div class="col-sm-3">
                    <label for="related_species" class="control-label">Comment</label>
                </div>
                <div class="col-sm-9">
                    <textarea :disabled="isReadOnly" type="text" row="2" class="form-control" id="related_species"
                        placeholder="" v-model="occurrence_report_obj.associated_species.comment" />
                </div>
            </div>
            <div class="row mb-3">
                <div class="col-sm-12">
                    <button v-if="!updatingAssociatedSpeciesDetails" :disabled="isReadOnly"
                        class="btn btn-primary btn-sm float-end"
                        @click.prevent="updateAssociatedSpeciesDetails()">Update</button>
                    <button v-else disabled class="float-end btn btn-primary">Updating <span
                            class="spinner-border spinner-border-sm" role="status" aria-hidden="true"></span>
                        <span class="visually-hidden">Loading...</span></button>
                </div>
            </div>
        </FormSection>
    </div>
</template>

<script>
import Vue from 'vue';
import FormSection from '@/components/forms/section_toggle.vue';
import RelatedSpecies from '@/components/common/occurrence/ocr_related_species_table.vue'
import {
    api_endpoints,
    helpers
}
    from '@/utils/hooks'
export default {
    name: 'OCRHabitat',
    props: {
        occurrence_report_obj: {
            type: Object,
            required: true
        },
        // this prop is only send from split species form to make the original species readonly
        is_readonly: {
            type: Boolean,
            default: false
        },
        is_external: {
            type: Boolean,
            default: false
        },
    },
    data: function () {
        let vm = this;
        return {
            habitatCompositionBody: 'habitatCompositionBody' + vm._uid,
            habitatConditionBody: 'habitatConditionBody' + vm._uid,
            vegetationStructureBody: 'vegetationStructureBody' + vm._uid,
            fireHistoryBody: 'fireHistoryBody' + vm._uid,
            associatedSpeciesBody: 'associatedSpeciesBody' + vm._uid,
            //---to show fields related to Fauna
            isFauna: vm.occurrence_report_obj.group_type === "fauna" ? true : false,
            //----list of values dictionary
            listOfValuesDict: {},
            //scientific_name_list: [],
            rock_type_list: [],
            soil_type_list: [],
            soil_colour_list: [],
            soil_condition_list: [],
            land_form_list: [],
            drainage_list: [],
            intensity_list: [],
            habitat_cond_sum: 0,
            updatingHabitatCompositionDetails: false,
            updatingHabitatConditionDetails: false,
            updatingVegetationStructure: false,
            updatingFireHistoryDetails: false,
            updatingAssociatedSpeciesDetails: false,
        }
    },
    components: {
        FormSection,
        RelatedSpecies,
    },
    computed: {
        isReadOnly: function () {
            //override for split reports
            if (this.is_readonly) {
                return this.is_readonly;
            }
            return this.occurrence_report_obj.readonly
        },
    },
    watch: {
        // "occurrence_report_obj.distribution.noo_auto": function(newVal) {
        //     let vm=this;
        //     var selectedValue = newVal;
        //         if(selectedValue === "true"){
        //             vm.occurrence_report_obj.distribution.number_of_occurrences=vm.occurrence_report_obj.distribution.cal_number_of_occurrences;
        //         }
        //         else{
        //             vm.occurrence_report_obj.distribution.number_of_occurrences=null;
        //         }
        // },
    },
    methods: {
        eventListeners: function () {
            let vm = this;
            $(vm.$refs.flowering_period_select).select2({
                "theme": "bootstrap-5",
                allowClear: true,
                placeholder: "Select Flowering Period",
                multiple: true,
            }).
                on("select2:select", function (e) {
                    var selected = $(e.currentTarget);
                    vm.occurrence_report_obj.conservation_attributes.flowering_period = selected.val();
                }).
                on("select2:unselect", function (e) {
                    var selected = $(e.currentTarget);
                    vm.occurrence_report_obj.conservation_attributes.flowering_period = selected.val();
                });
        },
        checkDate: function () {
            let vm = this;
            if (vm.$refs.last_fire_date.value) {
                vm.occurrence_report_obj.fire_history.last_fire_estimate = vm.$refs.last_fire_date.value;
            }
            else {
                vm.occurrence_report_obj.fire_history.last_fire_estimate = null;
            }
        },
        relatedSpeciesTextChanged: function (new_text) {
            this.occurrence_report_obj.associated_species.related_species = new_text
        },
        initialiseLandFormSelect: function () {
            let vm = this;
            // Initialise select2 for proposed Conservation Criteria
            $(vm.$refs.land_form_select).select2({
                "theme": "bootstrap-5",
                allowClear: true,
                multiple: true,
                placeholder: "Select Land Form",
            }).
                on("select2:select", function (e) {
                    var selected = $(e.currentTarget);
                    vm.occurrence_report_obj.habitat_composition.land_form = selected.val();
                }).
                on("select2:unselect", function (e) {
                    var selected = $(e.currentTarget);
                    vm.occurrence_report_obj.habitat_composition.land_form = selected.val();
                });
        },
        updateHabitatCompositionDetails: function () {
            let vm = this;
            vm.updatingHabitatCompositionDetails = true;
            fetch(helpers.add_endpoint_json(api_endpoints.occurrence_report, (vm.occurrence_report_obj.id + '/update_habitat_composition_details')), {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(vm.occurrence_report_obj.habitat_composition)
            }).then(async (response) => {
                vm.updatingHabitatCompositionDetails = false;
                vm.occurrence_report_obj.habitat_composition = await response.json();
                swal.fire({
                    title: 'Saved',
                    text: 'Habitat Composition details have been saved',
                    icon: 'success',
                    customClass: {
                        confirmButton: 'btn btn-primary'
                    },
                }).then((result) => {
                    if (vm.occurrence_report_obj.processing_status == "Unlocked") {
                        vm.$router.go();
                    }
                });
            }, (error) => {
                var text = helpers.apiVueResourceError(error);
                swal.fire({
                    title: 'Error',
                    text: 'Habitat Composition details cannot be saved because of the following error: ' + text,
                    icon: 'error',
                    customClass: {
                        confirmButton: 'btn btn-primary'
                    },
                });
                vm.updatingHabitatCompositionDetails = false;
            });
        },
        updateHabitatConditionDetails: function () {
            let vm = this;
            var valKeigheryTotal = vm.calcKeigheryTotal();
            if (valKeigheryTotal) {
                vm.updatingHabitatConditionDetails = true;
                fetch(helpers.add_endpoint_json(api_endpoints.occurrence_report, (vm.occurrence_report_obj.id + '/update_habitat_condition_details')), {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify(vm.occurrence_report_obj.habitat_condition)
                }).then(async (response) => {
                    vm.updatingHabitatConditionDetails = false;
                    vm.occurrence_report_obj.habitat_condition = await response.json();
                    swal.fire({
                        title: 'Saved',
                        text: 'Habitat Condition details have been saved',
                        icon: 'success',
                        customClass: {
                            confirmButton: 'btn btn-primary'
                        },
                    }).then((result) => {
                        if (vm.occurrence_report_obj.processing_status == "Unlocked") {
                            vm.$router.go();
                        }
                    });
                }, (error) => {
                    var text = helpers.apiVueResourceError(error);
                    swal.fire({
                        title: 'Error',
                        text: 'Habitat Condition details cannot be saved because of the following error: ' + text,
                        icon: 'error',
                        customClass: {
                            confirmButton: 'btn btn-primary'
                        },
                    }).then((result) => {
                        if (vm.occurrence_report_obj.processing_status == "Unlocked") {
                            vm.$router.go();
                        }
                    });
                    vm.updatingHabitatConditionDetails = false;
                });
            }
        },
        updateVegetationStructure: function () {
            let vm = this;
            vm.updatingVegetationStructure = true;
            fetch(helpers.add_endpoint_json(api_endpoints.occurrence_report, (vm.occurrence_report_obj.id + '/update_vegetation_structure')), {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(vm.occurrence_report_obj.vegetation_structure)
            }).then(async (response) => {
                vm.updatingVegetationStructure = false;
                vm.occurrence_report_obj.vegetation_structure = await response.json();
                swal.fire({
                    title: 'Saved',
                    text: 'Vegetation Structure details have been saved',
                    icon: 'success',
                    customClass: {
                        confirmButton: 'btn btn-primary'
                    },
                }).then((result) => {
                    if (vm.occurrence_report_obj.processing_status == "Unlocked") {
                        vm.$router.go();
                    }
                });
            }, (error) => {
                var text = helpers.apiVueResourceError(error);
                swal.fire({
                    title: 'Error',
                    text: 'Vegetation Structure details cannot be saved because of the following error: ' + text,
                    icon: 'error',
                    customClass: {
                        confirmButton: 'btn btn-primary'
                    },
                });
                vm.updatingVegetationStructure = false;
            });
        },
        updateFireHistoryDetails: function () {
            let vm = this;
            vm.updatingFireHistoryDetails = true;
            fetch(helpers.add_endpoint_json(api_endpoints.occurrence_report, (vm.occurrence_report_obj.id + '/update_fire_history_details')), {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(vm.occurrence_report_obj.fire_history)
            }).then(async (response) => {
                vm.updatingFireHistoryDetails = false;
                vm.occurrence_report_obj.fire_history = await response.json();
                swal.fire({
                    title: 'Saved',
                    text: 'Fire History details have been saved',
                    icon: 'success',
                    customClass: {
                        confirmButton: 'btn btn-primary'
                    },
                }).then((result) => {
                    if (vm.occurrence_report_obj.processing_status == "Unlocked") {
                        vm.$router.go();
                    }
                });
            }, (error) => {
                var text = helpers.apiVueResourceError(error);
                swal.fire({
                    title: 'Error',
                    text: 'Fire History details cannot be saved because of the following error: ' + text,
                    icon: 'error',
                    customClass: {
                        confirmButton: 'btn btn-primary'
                    },
                });
                vm.updatingFireHistoryDetails = false;
            });
        },
        updateAssociatedSpeciesDetails: function () {
            let vm = this;
            vm.updatingAssociatedSpeciesDetails = true;
            fetch(helpers.add_endpoint_json(api_endpoints.occurrence_report, (vm.occurrence_report_obj.id + '/update_associated_species_details')), {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(vm.occurrence_report_obj.associated_species)
            }).then(async (response) => {
                vm.updatingAssociatedSpeciesDetails = false;
                vm.occurrence_report_obj.associated_species = await response.json();
                swal.fire({
                    title: 'Saved',
                    text: 'Associated Species details have been saved',
                    icon: 'success',
                    customClass: {
                        confirmButton: 'btn btn-primary'
                    },
                }).then((result) => {
                    if (vm.occurrence_report_obj.processing_status == "Unlocked") {
                        vm.$router.go();
                    }
                });
            }, (error) => {
                var text = helpers.apiVueResourceError(error);
                swal.fire({
                    title: 'Error',
                    text: 'Associated Species cannot be saved because of the following error: ' + text,
                    icon: 'error',
                    customClass: {
                        confirmButton: 'btn btn-primary'
                    },
                });
                vm.updatingAssociatedSpeciesDetails = false;
            });
        },
        calcKeigheryTotal: function () {
            let vm = this;
            let total = 0;
            let a = parseInt(vm.occurrence_report_obj.habitat_condition.pristine);
            let b = parseInt(vm.occurrence_report_obj.habitat_condition.excellent);
            let c = parseInt(vm.occurrence_report_obj.habitat_condition.very_good);
            let d = parseInt(vm.occurrence_report_obj.habitat_condition.good);
            let e = parseInt(vm.occurrence_report_obj.habitat_condition.degraded);
            let f = parseInt(vm.occurrence_report_obj.habitat_condition.completely_degraded);
            total = a + b + c + d + e + f;
            vm.habitat_cond_sum = total;
            if (total > 100) {
                swal.fire({
                    title: 'warning',
                    text: 'The total Kiery Scale should not exceed 100% ',
                    icon: 'warning',
                    customClass: {
                        confirmButton: 'btn btn-primary'
                    },
                });
                return false;
            }
            else {
                return true;
            }

        }
    },
    created: async function () {
        let vm = this;
        //------fetch list of values
        const response = await fetch('/api/occurrence_report/list_of_values.json');
        vm.listOfValuesDict = response.json();
        vm.land_form_list = vm.listOfValuesDict.land_form_list;
        vm.land_form_list.splice(0, 0,
            {
                id: '',
                name: '',
            });
        vm.rock_type_list = vm.listOfValuesDict.rock_type_list;
        vm.rock_type_list.splice(0, 0,
            {
                id: null,
                name: null,
            });
        vm.soil_type_list = vm.listOfValuesDict.soil_type_list;
        vm.soil_type_list.splice(0, 0,
            {
                id: null,
                name: null,
            });
        vm.soil_colour_list = vm.listOfValuesDict.soil_colour_list;
        vm.soil_colour_list.splice(0, 0,
            {
                id: null,
                name: null,
            });
        vm.soil_condition_list = vm.listOfValuesDict.soil_condition_list;
        vm.soil_condition_list.splice(0, 0,
            {
                id: null,
                name: null,
            });
        vm.drainage_list = vm.listOfValuesDict.drainage_list;
        vm.drainage_list.splice(0, 0,
            {
                id: null,
                name: null,
            });
        vm.intensity_list = vm.listOfValuesDict.intensity_list;
        vm.intensity_list.splice(0, 0,
            {
                id: null,
                name: null,
            });
    },
    mounted: function () {
        let vm = this;
        vm.eventListeners();
        vm.initialiseLandFormSelect();
        vm.calcKeigheryTotal();
    },
}
</script>

<style lang="css" scoped>
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

input[type=text],
select {
    width: 100%;
    padding: 0.375rem 2.25rem 0.375rem 0.75rem;
}

input[type=number] {
    width: 50%;
}

input.ocr_number {
    width: 20%;
}

#habitat_cond_sum {
    color: red;
}
</style>
