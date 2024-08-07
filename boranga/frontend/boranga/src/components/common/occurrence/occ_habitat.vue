<template lang="html">
    <div id="habitat">
        <FormSection :formCollapse="false" label="Habitat Composition" :Index="habitatCompositionBody">
            <div class="row mb-3">
                <label for="" class="col-sm-3 control-label">Land Form:</label>
                <div class="col-sm-9">
                    <select :disabled="isReadOnly" style="width:100%;" class="form-select input-sm"
                        ref="land_form_select" v-model="occurrence_obj.habitat_composition.land_form">
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
                            v-if="rock_type_list && rock_type_list.length > 0 && occurrence_obj.habitat_composition.rock_type_id && !rock_type_list.map((d) => d.id).includes(occurrence_obj.habitat_composition.rock_type_id)">
                            <input type="text" v-if="occurrence_obj.habitat_composition.rock_type" class="form-control mb-3"
                                :value="occurrence_obj.habitat_composition.rock_type + ' (Now Archived)'" disabled />
                            <div class="mb-3 text-muted">
                                Change rock type to:
                            </div>
                        </template>
                        <select class="form-select" v-model="occurrence_obj.habitat_composition.rock_type_id">
                            <option v-for="rock_type in rock_type_list" :value="rock_type.id" v-bind:key="rock_type.id">
                                {{ rock_type.name }}
                            </option>
                        </select>
                    </template>
                    <template v-else>
                        <input class="form-control" type="text" :disabled="isReadOnly" v-model="occurrence_obj.habitat_composition.rock_type" />
                    </template>
                </div>
            </div>
            <div class="row mb-3">
                <label for="" class="col-sm-3 control-label">Loose Rock % :</label>
                <div class="col-sm-6">
                    <input :disabled="isReadOnly" type="number" class="form-control" id="loose_rock_per" placeholder=""
                        min="0" max="100" v-model="occurrence_obj.habitat_composition.loose_rock_percent" />
                </div>
            </div>
            <div class="row mb-3">
                <label for="" class="col-sm-3 control-label">Soil Type:</label>
                <div class="col-sm-9">
                    <template v-if="!isReadOnly">
                        <template
                            v-if="soil_type_list && soil_type_list.length > 0 && occurrence_obj.habitat_composition.soil_type_id && !soil_type_list.map((d) => d.id).includes(occurrence_obj.habitat_composition.soil_type_id)">
                            <input type="text" v-if="occurrence_obj.habitat_composition.soil_type" class="form-control mb-3"
                                :value="occurrence_obj.habitat_composition.soil_type + ' (Now Archived)'" disabled />
                            <div class="mb-3 text-muted">
                                Change soil type to:
                            </div>
                        </template>
                        <select class="form-select" v-model="occurrence_obj.habitat_composition.soil_type_id">
                            <option v-for="soil_type in soil_type_list" :value="soil_type.id" v-bind:key="soil_type.id">
                                {{ soil_type.name }}
                            </option>
                        </select>
                    </template>
                    <template v-else>
                        <input class="form-control" type="text" :disabled="isReadOnly" v-model="occurrence_obj.habitat_composition.soil_type" />
                    </template>
                </div>
            </div>
            <div class="row mb-3">
                <label for="" class="col-sm-3 control-label">Soil Colour:</label>
                <div class="col-sm-9">
                    <template v-if="!isReadOnly">
                        <template
                            v-if="soil_colour_list && soil_colour_list.length > 0 && occurrence_obj.habitat_composition.soil_colour_id && !soil_colour_list.map((d) => d.id).includes(occurrence_obj.habitat_composition.soil_colour_id)">
                            <input colour="text" v-if="occurrence_obj.habitat_composition.soil_colour" class="form-control mb-3"
                                :value="occurrence_obj.habitat_composition.soil_colour + ' (Now Archived)'" disabled />
                            <div class="mb-3 text-muted">
                                Change soil colour to:
                            </div>
                        </template>
                        <select class="form-select" v-model="occurrence_obj.habitat_composition.soil_colour_id">
                            <option v-for="soil_colour in soil_colour_list" :value="soil_colour.id" v-bind:key="soil_colour.id">
                                {{ soil_colour.name }}
                            </option>
                        </select>
                    </template>
                    <template v-else>
                        <input class="form-control" colour="text" :disabled="isReadOnly" v-model="occurrence_obj.habitat_composition.soil_colour" />
                    </template>
                </div>
            </div>
            <div class="row mb-3">
                <label for="" class="col-sm-3 control-label">Soil Condition:</label>
                <div class="col-sm-9">
                    <template v-if="!isReadOnly">
                        <template
                            v-if="soil_condition_list && soil_condition_list.length > 0 && occurrence_obj.habitat_composition.soil_condition_id && !soil_condition_list.map((d) => d.id).includes(occurrence_obj.habitat_composition.soil_condition_id)">
                            <input type="text" v-if="occurrence_obj.habitat_composition.soil_condition" class="form-control mb-3"
                                :value="occurrence_obj.habitat_composition.soil_condition + ' (Now Archived)'" disabled />
                            <div class="mb-3 text-muted">
                                Change soil type to:
                            </div>
                        </template>
                        <select class="form-select" v-model="occurrence_obj.habitat_composition.soil_condition_id">
                            <option v-for="soil_condition in soil_condition_list" :value="soil_condition.id" v-bind:key="soil_condition.id">
                                {{ soil_condition.name }}
                            </option>
                        </select>
                    </template>
                    <template v-else>
                        <input class="form-control" type="text" :disabled="isReadOnly" v-model="occurrence_obj.habitat_composition.soil_condition" />
                    </template>
                </div>
            </div>
            <div class="row mb-3">
                <label for="" class="col-sm-3 control-label">Drainage:</label>
                <div class="col-sm-9">
                    <select :disabled="isReadOnly" class="form-select"
                        v-model="occurrence_obj.habitat_composition.drainage_id">
                        <option v-for="option in drainage_list" :value="option.id" v-bind:key="option.id">
                            {{ option.name }}
                        </option>
                    </select>

                </div>
            </div>
            <div class="row mb-3">
                <label for="" class="col-sm-3 control-label">Water Quality:</label>
                <div class="col-sm-9">
                    <textarea :disabled="isReadOnly" type="text" class="form-control" placeholder=""
                        v-model="occurrence_obj.habitat_composition.water_quality" />
                </div>
            </div>
            <div class="row mb-3">
                <label for="" class="col-sm-3 control-label">Habitat Notes:</label>
                <div class="col-sm-9">
                    <textarea :disabled="isReadOnly" type="text" class="form-control" placeholder=""
                        v-model="occurrence_obj.habitat_composition.habitat_notes" />
                </div>
            </div>
            <div class="row mb-3">
                <div class="col-sm-12">
                    <span v-if="occurrence_obj.habitat_composition.copied_ocr" class="float-end"><b>Sourced from
                            {{ occurrence_obj.habitat_composition.copied_ocr }}</b></span>
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

            <RelatedReports :isReadOnly="isReadOnly" :occurrence_obj=occurrence_obj
                :section_type="'habitat_composition'" @copyUpdate="copyUpdate" />
        </FormSection>
        <FormSection :formCollapse="false" label="Habitat Condition" :Index="habitatConditionBody">
            <label for="" class="col-lg-3 control-label fs-5 fw-bold">Keighery Scale</label>
            <div class="row mb-3">
                <label for="" class="col-sm-3 control-label">Pristine %:</label>
                <div class="col-sm-6">
                    <input :disabled="isReadOnly" type="number" class="form-control occ_number" id="pristine"
                        placeholder="" min="0" max="100" v-model="occurrence_obj.habitat_condition.pristine"
                        @change.prevent="calcKeigheryTotal()" />
                </div>
            </div>
            <div class="row mb-3">
                <label for="" class="col-sm-3 control-label">Excellent %:</label>
                <div class="col-sm-6">
                    <input :disabled="isReadOnly" type="number" class="form-control occ_number" id="excellent"
                        placeholder="" min="0" max="100" v-model="occurrence_obj.habitat_condition.excellent"
                        @change.prevent="calcKeigheryTotal()" />
                </div>
            </div>
            <div class="row mb-3">
                <label for="" class="col-sm-3 control-label">Very Good %:</label>
                <div class="col-sm-6">
                    <input :disabled="isReadOnly" type="number" class="form-control occ_number" id="very_good"
                        placeholder="" min="0" max="100" v-model="occurrence_obj.habitat_condition.very_good"
                        @change.prevent="calcKeigheryTotal()" />
                </div>
            </div>
            <div class="row mb-3">
                <label for="" class="col-sm-3 control-label">Good %:</label>
                <div class="col-sm-6">
                    <input :disabled="isReadOnly" type="number" class="form-control occ_number" id="good" placeholder=""
                        min="0" max="100" v-model="occurrence_obj.habitat_condition.good"
                        @change.prevent="calcKeigheryTotal()" />
                </div>
            </div>
            <div class="row mb-3">
                <label for="" class="col-sm-3 control-label">Degraded %:</label>
                <div class="col-sm-6">
                    <input :disabled="isReadOnly" type="number" class="form-control occ_number" id="degraded"
                        placeholder="" min="0" max="100" v-model="occurrence_obj.habitat_condition.degraded"
                        @change.prevent="calcKeigheryTotal()" />
                </div>
            </div>
            <div class="row mb-3">
                <label for="" class="col-sm-3 control-label">Completely Degraded %:</label>
                <div class="col-sm-6">
                    <input :disabled="isReadOnly" type="number" class="form-control occ_number" id="completely_degraded"
                        placeholder="" min="0" max="100" v-model="occurrence_obj.habitat_condition.completely_degraded"
                        @change.prevent="calcKeigheryTotal()" />
                </div>
            </div>
            <div class="row mb-3">
                <label for="" class="col-sm-3 control-label"></label>
                <div class="col-sm-6">
                    <input readonly type="text" class="form-control occ_number" id="habitat_cond_sum" placeholder=""
                        v-model="habitat_cond_sum" />
                </div>
            </div>
            <div class="row mb-3">
                <label for="" class="col-sm-3 control-label">Count Date: </label>
                <div class="col-sm-9">
                    <input v-model="occurrence_obj.habitat_condition.count_date
                        " :disabled="true" type="datetime-local" class="form-control" name="count_date" />
                </div>
            </div>
            <div class="row mb-3">
                <div class="col-sm-12">
                    <span v-if="occurrence_obj.habitat_condition.copied_ocr" class="float-end"><b>Sourced from
                            {{ occurrence_obj.habitat_condition.copied_ocr }}</b></span>
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
            <RelatedReports :isReadOnly="isReadOnly" :occurrence_obj=occurrence_obj :section_type="'habitat_condition'"
                @copyUpdate="copyUpdate" />
        </FormSection>

        <FormSection :formCollapse="false" label="Vegetation Structure" :Index="vegetationStructureBody">
            <div class="row mb-3">
                <label for="" class="col-sm-6 control-label">Vegetation Structure - Layer 1:</label>
                <div class="col-sm-9">
                    <textarea :disabled="isReadOnly" type="text" row="2" class="form-control"
                        id="vegetation_structure_text_1" placeholder=""
                        v-model="occurrence_obj.vegetation_structure.vegetation_structure_layer_one" />
                </div>
            </div>
            <div class="row mb-3">
                <label for="" class="col-sm-6 control-label">Vegetation Structure - Layer 2:</label>
                <div class="col-sm-9">
                    <textarea :disabled="isReadOnly" type="text" row="2" class="form-control"
                        id="vegetation_structure_text_2" placeholder=""
                        v-model="occurrence_obj.vegetation_structure.vegetation_structure_layer_two" />
                </div>
            </div>
            <div class="row mb-3">
                <label for="" class="col-sm-6 control-label">Vegetation Structure - Layer 3:</label>
                <div class="col-sm-9">
                    <textarea :disabled="isReadOnly" type="text" row="2" class="form-control"
                        id="vegetation_structure_text_3" placeholder=""
                        v-model="occurrence_obj.vegetation_structure.vegetation_structure_layer_three" />
                </div>
            </div>
            <div class="row mb-3">
                <label for="" class="col-sm-6 control-label">Vegetation Structure - Layer 4:</label>
                <div class="col-sm-9">
                    <textarea :disabled="isReadOnly" type="text" row="2" class="form-control"
                        id="vegetation_structure_text_4" placeholder=""
                        v-model="occurrence_obj.vegetation_structure.vegetation_structure_layer_four" />
                </div>
            </div>
            <div class="row mb-3">
                <div class="col-sm-12">
                    <span v-if="occurrence_obj.vegetation_structure.copied_ocr" class="float-end"><b>Sourced from
                            {{ occurrence_obj.vegetation_structure.copied_ocr }}</b></span>
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
            <RelatedReports :isReadOnly="isReadOnly" :occurrence_obj=occurrence_obj
                :section_type="'vegetation_structure'" @copyUpdate="copyUpdate" />
        </FormSection>

        <FormSection :formCollapse="false" label="Fire History" :Index="fireHistoryBody">
            <label for="" class="col-lg-3 control-label fs-5 fw-bold">Last Fire History</label>
            <div class="row mb-3">
                <label for="" class="col-sm-3 control-label">Last Fire Estimate:</label>
                <div class="col-sm-9">
                    <input :disabled="isReadOnly" type="month" class="form-control" name="last_fire_date"
                        ref="last_fire_date" @change="checkDate()"
                        v-model="occurrence_obj.fire_history.last_fire_estimate" />
                </div>
            </div>
            <div class="row mb-3">
                <label for="" class="col-sm-3 control-label">Intensity:</label>
                <div class="col-sm-9">
                    <select :disabled="isReadOnly" class="form-select"
                        v-model="occurrence_obj.fire_history.intensity_id">
                        <option v-for="option in intensity_list" :value="option.id" v-bind:key="option.id">
                            {{ option.name }}
                        </option>
                    </select>

                </div>
            </div>
            <div class="row mb-3">
                <label for="" class="col-sm-3 control-label">Comments :</label>
                <div class="col-sm-9">
                    <textarea :disabled="isReadOnly" type="text" row="2" class="form-control" id="fire_history_comment"
                        placeholder="" v-model="occurrence_obj.fire_history.comment" />
                </div>
            </div>
            <div class="row mb-3">
                <div class="col-sm-12">
                    <span v-if="occurrence_obj.fire_history.copied_ocr" class="float-end"><b>Sourced from
                            {{ occurrence_obj.fire_history.copied_ocr }}</b></span>
                </div>
            </div>
            <div class="row mb-3">
                <div class="col-sm-12">
                    <button v-if="!updatingFireHistoryDetails" :disabled="isReadOnly"
                        class="btn btn-primary btn-sm float-end"
                        @click.prevent="updateFireHistoryDetails()">Update</button>
                    <button v-else disabled class="float-end btn btn-primary">Updating</button>
                </div>
            </div>
            <RelatedReports :isReadOnly="isReadOnly" :occurrence_obj=occurrence_obj :section_type="'fire_history'"
                @copyUpdate="copyUpdate" />
        </FormSection>
        <FormSection :formCollapse="false" label="Associated Species" :Index="associatedSpeciesBody">

            <RelatedSpecies :isReadOnly="isReadOnly" ref="related_species" :occurrence_obj=occurrence_obj />

            <div class="row mb-3">
                <div class="col-sm-3">
                    <label for="related_species" class="control-label">Comment</label>
                </div>
                <div class="col-sm-9">
                    <textarea :disabled="isReadOnly" type="text" row="2" class="form-control" id="related_species"
                        placeholder="" v-model="occurrence_obj.associated_species.comment" />
                </div>
            </div>
            <div class="row mb-3">
                <div class="col-sm-12">
                    <span v-if="occurrence_obj.associated_species.copied_ocr" class="float-end"><b>Sourced from
                            {{ occurrence_obj.associated_species.copied_ocr }}</b></span>
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

            <RelatedReports :isReadOnly="isReadOnly" :occurrence_obj=occurrence_obj :section_type="'associated_species'"
                @copyUpdate="copyUpdate" />
        </FormSection>
    </div>
</template>

<script>
import Vue from 'vue';
import FormSection from '@/components/forms/section_toggle.vue';
import RichText from '@/components/forms/richtext.vue'
import RelatedReports from '@/components/common/occurrence/occ_related_ocr_table.vue'
import RelatedSpecies from '@/components/common/occurrence/occ_related_species_table.vue'
import {
    api_endpoints,
    helpers
}
    from '@/utils/hooks'
export default {
    name: 'OCCHabitat',
    props: {
        occurrence_obj: {
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
            isFauna: vm.occurrence_obj.group_type === "fauna" ? true : false,
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
        RichText,
        RelatedReports,
        RelatedSpecies,
    },
    computed: {
        isReadOnly: function () {
            return !(this.occurrence_obj.can_user_edit);
        },
    },
    watch: {
        // "occurrence_obj.distribution.noo_auto": function(newVal) {
        //     let vm=this;
        //     var selectedValue = newVal;
        //         if(selectedValue === "true"){
        //             vm.occurrence_obj.distribution.number_of_occurrences=vm.occurrence_obj.distribution.cal_number_of_occurrences;
        //         }
        //         else{
        //             vm.occurrence_obj.distribution.number_of_occurrences=null;
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
                    vm.occurrence_obj.conservation_attributes.flowering_period = selected.val();
                }).
                on("select2:unselect", function (e) {
                    var selected = $(e.currentTarget);
                    vm.occurrence_obj.conservation_attributes.flowering_period = selected.val();
                });
        },
        checkDate: function () {
            let vm = this;
            if (vm.$refs.last_fire_date.value) {
                vm.occurrence_obj.fire_history.last_fire_estimate = vm.$refs.last_fire_date.value;
            }
            else {
                vm.occurrence_obj.fire_history.last_fire_estimate = null;
            }
        },
        relatedSpeciesTextChanged: function (new_text) {
            this.occurrence_obj.associated_species.related_species = new_text
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
                    vm.occurrence_obj.habitat_composition.land_form = selected.val();
                }).
                on("select2:unselect", function (e) {
                    var selected = $(e.currentTarget);
                    vm.occurrence_obj.habitat_composition.land_form = selected.val();
                });
        },
        copyUpdate: function (object, section) {
            let vm = this;
            vm.occurrence_obj[section] = object[section];
            $(vm.$refs.land_form_select).val(vm.occurrence_obj.habitat_composition.land_form).trigger('change.select2');
            vm.$refs.related_species.reload();
            vm.calcKeigheryTotal();
        },
        updateHabitatCompositionDetails: function () {
            let vm = this;
            vm.updatingHabitatCompositionDetails = true;
            vm.$http.post(helpers.add_endpoint_json(api_endpoints.occurrence, (vm.occurrence_obj.id + '/update_habitat_composition_details')), JSON.stringify(vm.occurrence_obj.habitat_composition), {
                emulateJSON: true
            }).then((response) => {
                vm.updatingHabitatCompositionDetails = false;
                vm.occurrence_obj.habitat_composition = response.body;
                swal.fire({
                    title: 'Saved',
                    text: 'Habitat Composition details have been saved',
                    icon: 'success',
                    customClass: {
                        confirmButton: 'btn btn-primary'
                    },
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
                vm.$http.post(helpers.add_endpoint_json(api_endpoints.occurrence, (vm.occurrence_obj.id + '/update_habitat_condition_details')), JSON.stringify(vm.occurrence_obj.habitat_condition), {
                    emulateJSON: true
                }).then((response) => {
                    vm.updatingHabitatConditionDetails = false;
                    vm.occurrence_obj.habitat_condition = response.body;
                    swal.fire({
                        title: 'Saved',
                        text: 'Habitat Condition details have been saved',
                        icon: 'success',
                        customClass: {
                            confirmButton: 'btn btn-primary'
                        },
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
                    });
                    vm.updatingHabitatConditionDetails = false;
                });
            }
        },
        updateVegetationStructure: function () {
            let vm = this;
            vm.updatingVegetationStructure = true;
            vm.$http.post(helpers.add_endpoint_json(api_endpoints.occurrence, (vm.occurrence_obj.id + '/update_vegetation_structure')), JSON.stringify(vm.occurrence_obj.vegetation_structure), {
                emulateJSON: true
            }).then((response) => {
                vm.updatingVegetationStructure = false;
                vm.occurrence_obj.vegetation_structure = response.body;
                swal.fire({
                    title: 'Saved',
                    text: 'Vegetation Structure details have been saved',
                    icon: 'success',
                    customClass: {
                        confirmButton: 'btn btn-primary'
                    },

                }).then((result) => {
                    if (vm.occurrence_obj.processing_status == "Unlocked") {
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
            vm.$http.post(helpers.add_endpoint_json(api_endpoints.occurrence, (vm.occurrence_obj.id + '/update_fire_history_details')), JSON.stringify(vm.occurrence_obj.fire_history), {
                emulateJSON: true
            }).then((response) => {
                vm.updatingFireHistoryDetails = false;
                vm.occurrence_obj.fire_history = response.body;
                swal.fire({
                    title: 'Saved',
                    text: 'Fire History details have been saved',
                    icon: 'success',
                    customClass: {
                        confirmButton: 'btn btn-primary'
                    },

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
            vm.$http.post(helpers.add_endpoint_json(api_endpoints.occurrence, (vm.occurrence_obj.id + '/update_associated_species_details')), JSON.stringify(vm.occurrence_obj.associated_species), {
                emulateJSON: true
            }).then((response) => {
                vm.updatingAssociatedSpeciesDetails = false;
                vm.occurrence_obj.associated_species = response.body;
                swal.fire({
                    title: 'Saved',
                    text: 'Associated Species details have been saved',
                    icon: 'success',
                    customClass: {
                        confirmButton: 'btn btn-primary'
                    },

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
            let a = parseInt(vm.occurrence_obj.habitat_condition.pristine);
            let b = parseInt(vm.occurrence_obj.habitat_condition.excellent);
            let c = parseInt(vm.occurrence_obj.habitat_condition.very_good);
            let d = parseInt(vm.occurrence_obj.habitat_condition.good);
            let e = parseInt(vm.occurrence_obj.habitat_condition.degraded);
            let f = parseInt(vm.occurrence_obj.habitat_condition.completely_degraded);
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
        const res = await Vue.http.get('/api/occurrence/list_of_values.json');
        vm.listOfValuesDict = res.body;
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

input.occ_number {
    width: 20%;
}

#habitat_cond_sum {
    color: red;
}
</style>
