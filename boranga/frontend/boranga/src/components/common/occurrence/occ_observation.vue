<template lang="html">
    <div id="observation">
        <FormSection :formCollapse="false" label="Observation Details" :Index="observationDetailBody">
            <div class="row mb-3">
                <label for="" class="col-sm-3 control-label">Observation Method:</label>
                <div class="col-sm-9">
                    <select :disabled="isReadOnly" class="form-select"
                        v-model="occurrence_obj.observation_detail.observation_method_id">
                        <option v-for="option in observation_method_list" :value="option.id" v-bind:key="option.id">
                            {{ option.name }}
                        </option>
                    </select>

                </div>
            </div>
            <div class="row mb-3">
                <label for="" class="col-sm-3 control-label">Area Surveyed(m<sup>2</sup>) :</label>
                <div class="col-sm-6">
                    <input :disabled="isReadOnly" type="number" class="form-control occ_number" id="area_surveyed"
                        placeholder="" min="0" v-model="occurrence_obj.observation_detail.area_surveyed" />
                </div>
            </div>
            <div class="row mb-3">
                <label for="" class="col-sm-3 control-label">Survey Duration(mins) :</label>
                <div class="col-sm-6">
                    <input :disabled="isReadOnly" type="number" class="form-control occ_number" id="survey_duration"
                        placeholder="" min="0" v-model="occurrence_obj.observation_detail.survey_duration" />
                </div>
            </div>
            <div class="row mb-3">
                <div class="col-sm-12">
                    <span v-if="occurrence_obj.observation_detail.copied_ocr" class="float-end"><b>Sourced from
                            {{ occurrence_obj.observation_detail.copied_ocr }}</b></span>
                </div>
            </div>
            <div class="row mb-3">
                <div class="col-sm-12">
                    <!-- <button v-if="!updatingHabitatCompositionDetails" class="pull-right btn btn-primary" @click.prevent="updateDetails()" :disabled="!can_update()">Update</button> -->
                    <button v-if="!updatingObservationDetails" :disabled="isReadOnly"
                        class="btn btn-primary btn-sm float-end"
                        @click.prevent="updateObservationDetails()">Update</button>
                    <button v-else disabled class="float-end btn btn-primary"><i
                            class="fa fa-spin fa-spinner"></i>&nbsp;Updating</button>
                </div>
            </div>
            <RelatedReports :isReadOnly="isReadOnly" :occurrence_obj=occurrence_obj :section_type="'observation_detail'"
                @copyUpdate="copyUpdate" />
        </FormSection>

        <FormSection :formCollapse="false" label="Plant Count" :Index="plantCountBody" v-if="isFlora">
            <PlantCount v-if="isFlora" :plant_count="occurrence_obj.plant_count" :is_report=false
                :occurrence_id="occurrence_obj.id" id="plantCountDetail" :is_external="is_external"
                :isReadOnly="isReadOnly" ref="plantCountDetail" @mounted="populatePlantCountLookups">
            </PlantCount>
            <RelatedReports :isReadOnly="isReadOnly" :occurrence_obj=occurrence_obj :section_type="'plant_count'"
                @copyUpdate="copyUpdate" />
        </FormSection>

        <FormSection :formCollapse="false" label="Animal Observation" :Index="animalObsBody" v-if="isFauna">
            <AnimalObservation v-if="isFauna" :animal_observation="occurrence_obj.animal_observation" :is_report=false
                :occurrence_id="occurrence_obj.id" id="animalObservationDetail" :is_external="is_external"
                :isReadOnly="isReadOnly" ref="animalObservationDetail" @mounted="populateAnimalObservationLookups">
            </AnimalObservation>
            <RelatedReports :isReadOnly="isReadOnly" :occurrence_obj=occurrence_obj :section_type="'animal_observation'"
                @copyUpdate="copyUpdate" />
        </FormSection>

        <FormSection :formCollapse="false" label="Identification" :Index="identificationBody">
            <div class="row mb-3">
                <label for="" class="col-sm-3 control-label">ID Confirmed by:</label>
                <div class="col-sm-9">
                    <input :disabled="isReadOnly" type="text" class="form-control" id="id_confirmed_by" placeholder=""
                        v-model="occurrence_obj.identification.id_confirmed_by" />
                </div>
            </div>
            <div class="row mb-3">
                <label for="" class="col-sm-3 control-label fw-bold">Identification Certainty: <span
                        class="text-danger">*</span></label>
                <div class="col-sm-9">
                    <select :disabled="isReadOnly" class="form-select"
                        v-model="occurrence_obj.identification.identification_certainty_id">
                        <option v-for="option in identification_certainty_list" :value="option.id"
                            v-bind:key="option.id">
                            {{ option.name }}
                        </option>
                    </select>
                </div>
            </div>
            <div class="row mb-3">
                <label for="" class="col-sm-3 control-label">Sample Type:</label>
                <div class="col-sm-9">
                    <select :disabled="isReadOnly" class="form-select"
                        v-model="occurrence_obj.identification.sample_type_id">
                        <option v-for="option in sample_type_list" :value="option.id" v-bind:key="option.id">
                            {{ option.name }}
                        </option>
                    </select>
                </div>
            </div>
            <div class="row mb-3">
                <label for="" class="col-sm-3 control-label">Sample Destination:</label>
                <div class="col-sm-9">
                    <select :disabled="isReadOnly" class="form-select"
                        v-model="occurrence_obj.identification.sample_destination_id">
                        <option v-for="option in sample_dest_list" :value="option.id" v-bind:key="option.id">
                            {{ option.name }}
                        </option>
                    </select>
                </div>
            </div>
            <div class="row mb-3">
                <label for="" class="col-sm-3 control-label">Permit Type:</label>
                <div class="col-sm-9">
                    <template v-if="!isReadOnly">
                        <template
                            v-if="permit_type_list && permit_type_list.length > 0 && occurrence_obj.identification.permit_type_id && !permit_type_list.map((d) => d.id).includes(occurrence_obj.identification.permit_type_id)">
                            <input type="text" v-if="occurrence_obj.identification.permit_type" class="form-control mb-3"
                                :value="occurrence_obj.identification.permit_type + ' (Now Archived)'" disabled />
                            <div class="mb-3 text-muted">
                                Change permit type to:
                            </div>
                        </template>
                        <select class="form-select"
                        v-model="occurrence_obj.identification.permit_type_id">
                        <option v-for="option in permit_type_list" :value="option.id" v-bind:key="option.id">
                            {{ option.name }}
                        </option>
                    </select>
                    </template>
                    <template v-else>
                        <input class="form-control" type="text" :disabled="isReadOnly" v-model="occurrence_obj.identification.permit_type" />
                    </template>
                </div>
            </div>
            <div class="row mb-3">
                <label for="" class="col-sm-3 control-label">Permit ID:</label>
                <div class="col-sm-9">
                    <input :disabled="isReadOnly" type="text" class="form-control" id="permit_id" placeholder=""
                        v-model="occurrence_obj.identification.permit_id" />
                </div>
            </div>
            <div class="row mb-3">
                <label for="" class="col-sm-3 control-label">Sample Label/ Collector Number:</label>
                <div class="col-sm-9">
                    <textarea :disabled="isReadOnly" type="text" row="2" class="form-control" id="collector_number"
                        placeholder="" v-model="occurrence_obj.identification.collector_number" />
                </div>
            </div>
            <div class="row mb-3">
                <label for="" class="col-sm-3 control-label">Barcode/Catalog Number:</label>
                <div class="col-sm-9">
                    <textarea :disabled="isReadOnly" type="text" row="2" class="form-control" id="barcode_number"
                        placeholder="" v-model="occurrence_obj.identification.barcode_number" />
                </div>
            </div>
            <div class="row mb-3">
                <label for="" class="col-sm-3 control-label">Identification Comments:</label>
                <div class="col-sm-9">
                    <textarea :disabled="isReadOnly" type="text" row="2" class="form-control"
                        id="identification_comment" placeholder=""
                        v-model="occurrence_obj.identification.identification_comment" />
                </div>
            </div>
            <div class="row mb-3">
                <div class="col-sm-12">
                    <span v-if="occurrence_obj.identification.copied_ocr" class="float-end"><b>Sourced from
                            {{ occurrence_obj.identification.copied_ocr }}</b></span>
                </div>
            </div>
            <div class="row mb-3">
                <div class="col-sm-12">
                    <!-- <button v-if="!updatingHabitatCompositionDetails" class="pull-right btn btn-primary" @click.prevent="updateDetails()" :disabled="!can_update()">Update</button> -->
                    <button v-if="!updatingIdentificationDetails" :disabled="isReadOnly"
                        class="btn btn-primary btn-sm float-end"
                        @click.prevent="updateIdentificationDetails()">Update</button>
                    <button v-else disabled class="float-end btn btn-primary"><i
                            class="fa fa-spin fa-spinner"></i>&nbsp;Updating</button>
                </div>
            </div>
            <RelatedReports :isReadOnly="isReadOnly" :occurrence_obj=occurrence_obj :section_type="'identification'"
                @copyUpdate="copyUpdate" />
        </FormSection>
    </div>
</template>

<script>
import Vue from 'vue';
import FormSection from '@/components/forms/section_toggle.vue';
import PlantCount from './plant_count.vue'
import AnimalObservation from './animal_observation.vue'
import RelatedReports from '@/components/common/occurrence/occ_related_ocr_table.vue'
import {
    api_endpoints,
    helpers
}
    from '@/utils/hooks'
export default {
    name: 'OCCObservation',
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
            observationDetailBody: 'observationDetailBody' + vm._uid,
            plantCountBody: 'plantCountBody' + vm._uid,
            animalObsBody: 'animalObsBody' + vm._uid,
            identificationBody: 'identificationBody' + vm._uid,
            //---to show fields related to Fauna
            isFauna: vm.occurrence_obj.group_type === "fauna" ? true : false,
            isFlora: vm.occurrence_obj.group_type === "flora" ? true : false,
            //----list of values dictionary
            listOfValuesDict: {},
            //scientific_name_list: [],
            observation_method_list: [],
            identification_certainty_list: [],
            sample_type_list: [],
            sample_dest_list: [],
            permit_type_list: [],
            updatingObservationDetails: false,
            updatingIdentificationDetails: false,
        }
    },
    components: {
        FormSection,
        PlantCount,
        AnimalObservation,
        RelatedReports,
    },
    computed: {
        isReadOnly: function () {
            return !(this.occurrence_obj.can_user_edit);
        },
    },
    watch: {
    },
    methods: {
        eventListeners: function () {
        },
        updateObservationDetails: function () {
            let vm = this;
            vm.updatingObservationDetails = true;
            vm.$http.post(helpers.add_endpoint_json(api_endpoints.occurrence, (vm.occurrence_obj.id + '/update_observation_details')), JSON.stringify(vm.occurrence_obj.observation_detail), {
                emulateJSON: true
            }).then((response) => {
                vm.updatingObservationDetails = false;
                vm.occurrence_obj.observation_detail = response.body;
                swal.fire({
                    title: 'Saved',
                    text: 'Observation details have been saved',
                    icon: 'success',
                    customClass: {
                        confirmButton: 'btn btn-primary'
                    },
                });
            }, (error) => {
                var text = helpers.apiVueResourceError(error);
                swal.fire({
                    title: 'Error',
                    text: 'Observation details cannot be saved because of the following error: ' + text,
                    icon: 'error',
                    customClass: {
                        confirmButton: 'btn btn-primary'
                    },
                });
                vm.updatingObservationDetails = false;
            });
        },
        copyUpdate: function (object, section) {
            let vm = this;
            vm.occurrence_obj[section] = object[section];
        },
        updateIdentificationDetails: function () {
            let vm = this;
            vm.updatingIdentificationDetails = true;
            vm.$http.post(helpers.add_endpoint_json(api_endpoints.occurrence, (vm.occurrence_obj.id + '/update_identification_details')), JSON.stringify(vm.occurrence_obj.identification), {
                emulateJSON: true
            }).then((response) => {
                vm.updatingIdentificationDetails = false;
                vm.occurrence_obj.identification = response.body;
                swal.fire({
                    title: 'Saved',
                    text: 'Identification details have been saved',
                    icon: 'success',
                    customClass: {
                        confirmButton: 'btn btn-primary'
                    },
                });
            }, (error) => {
                var text = helpers.apiVueResourceError(error);
                swal.fire({
                    title: 'Error',
                    text: 'Identification details cannot be saved because of the following error: ' + text,
                    icon: 'error',
                    customClass: {
                        confirmButton: 'btn btn-primary'
                    },
                });
                vm.updatingIdentificationDetails = false;
            });
        },
        populatePlantCountLookups: function () {
            // using child refs to assign the list values to avoid calling the above api again in plantCount component
            vm.$refs.plantCountDetail.plant_count_method_list = vm.listOfValuesDict.plant_count_method_list;
            vm.$refs.plantCountDetail.plant_count_method_list.splice(0, 0,
                {
                    id: null,
                    name: null,
                });
            vm.$refs.plantCountDetail.plant_count_accuracy_list = vm.listOfValuesDict.plant_count_accuracy_list;
            vm.$refs.plantCountDetail.plant_count_accuracy_list.splice(0, 0,
                {
                    id: null,
                    name: null,
                });
            vm.$refs.plantCountDetail.plant_condition_list = vm.listOfValuesDict.plant_condition_list;
            vm.$refs.plantCountDetail.plant_condition_list.splice(0, 0,
                {
                    id: null,
                    name: null,
                });
            vm.$refs.plantCountDetail.counted_subject_list = vm.listOfValuesDict.counted_subject_list;
            vm.$refs.plantCountDetail.counted_subject_list.splice(0, 0,
                {
                    id: null,
                    name: null,
                });
        },
        populateAnimalObservationLookups: function () {
            // using child refs to assign the list values to avoid calling the above api again in AnimalObservation component
            vm.$refs.animalObservationDetail.primary_detection_method_list = vm.listOfValuesDict.primary_detection_method_list;
            vm.$refs.animalObservationDetail.primary_detection_method_list.splice(0, 0,
                {
                    id: '',
                    name: '',
                });
            vm.$refs.animalObservationDetail.secondary_sign_list = vm.listOfValuesDict.secondary_sign_list;
            vm.$refs.animalObservationDetail.secondary_sign_list.splice(0, 0,
                {
                    id: '',
                    name: '',
                });
            vm.$refs.animalObservationDetail.reprod_state_list = vm.listOfValuesDict.reprod_state_list;
            vm.$refs.animalObservationDetail.reprod_state_list.splice(0, 0,
                {
                    id: '',
                    name: '',
                });
            vm.$refs.animalObservationDetail.death_reason_list = vm.listOfValuesDict.death_reason_list;
            vm.$refs.animalObservationDetail.death_reason_list.splice(0, 0,
                {
                    id: null,
                    name: null,
                });
            vm.$refs.animalObservationDetail.animal_health_list = vm.listOfValuesDict.animal_health_list;
            vm.$refs.animalObservationDetail.animal_health_list.splice(0, 0,
                {
                    id: null,
                    name: null,
                });
        }

    },
    created: async function () {
        let vm = this;
        //------fetch list of values
        const res = await Vue.http.get(`/api/occurrence/observation_list_of_values.json?group_type=${vm.occurrence_obj.group_type}`);
        vm.listOfValuesDict = res.body;
        vm.observation_method_list = vm.listOfValuesDict.observation_method_list;
        vm.observation_method_list.splice(0, 0,
            {
                id: null,
                name: null,
            });
        vm.identification_certainty_list = vm.listOfValuesDict.identification_certainty_list;
        vm.identification_certainty_list.splice(0, 0,
            {
                id: null,
                name: null,
            });
        vm.sample_type_list = vm.listOfValuesDict.sample_type_list;
        vm.sample_type_list.splice(0, 0,
            {
                id: null,
                name: null,
            });
        vm.sample_dest_list = vm.listOfValuesDict.sample_dest_list;
        vm.sample_dest_list.splice(0, 0,
            {
                id: null,
                name: null,
            });
        vm.permit_type_list = vm.listOfValuesDict.permit_type_list;
        vm.permit_type_list.splice(0, 0,
            {
                id: null,
                name: null,
            });
    },
    mounted: function () {
        let vm = this;
        vm.eventListeners();
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

input.plant_count {
    width: 63%;
}
</style>
