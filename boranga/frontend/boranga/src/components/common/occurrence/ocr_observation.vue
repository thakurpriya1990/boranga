<template lang="html">
    <div id="observation">
        <FormSection
            :form-collapse="false"
            label="Observation Details"
            :Index="observationDetailBody"
        >
            <div class="row mb-3">
                <label for="" class="col-sm-3 control-label"
                    >Observation Method:</label
                >
                <div class="col-sm-9">
                    <template v-if="!isReadOnly">
                        <template
                            v-if="
                                observation_method_list &&
                                observation_method_list.length > 0 &&
                                occurrence_report_obj.observation_detail
                                    .observation_method_id &&
                                !observation_method_list
                                    .map((d) => d.id)
                                    .includes(
                                        occurrence_report_obj.observation_detail
                                            .observation_method_id
                                    )
                            "
                        >
                            <input
                                v-if="
                                    occurrence_report_obj.observation_detail
                                        .observation_method
                                "
                                type="text"
                                class="form-control mb-3"
                                :value="
                                    occurrence_report_obj.observation_detail
                                        .observation_method + ' (Now Archived)'
                                "
                                disabled
                            />
                            <div class="mb-3 text-muted">
                                Change observation method to:
                            </div>
                        </template>
                        <select
                            v-model="
                                occurrence_report_obj.observation_detail
                                    .observation_method_id
                            "
                            class="form-select"
                        >
                            <option
                                v-for="observation_method in observation_method_list"
                                :key="observation_method.id"
                                :value="observation_method.id"
                            >
                                {{ observation_method.name }}
                            </option>
                        </select>
                    </template>
                    <template v-else>
                        <input
                            v-model="
                                occurrence_report_obj.observation_detail
                                    .observation_method
                            "
                            class="form-control"
                            type="text"
                            :disabled="isReadOnly"
                        />
                    </template>
                </div>
            </div>
            <div class="row mb-3">
                <label for="" class="col-sm-3 control-label"
                    >Area Surveyed:</label
                >
                <div class="col-sm-4">
                    <div class="input-group">
                        <input
                            id="area_surveyed"
                            v-model="
                                occurrence_report_obj.observation_detail
                                    .area_surveyed
                            "
                            :disabled="isReadOnly"
                            type="number"
                            class="form-control"
                            placeholder=""
                            min="0"
                            max="2147483647"
                        />
                        <span class="input-group-text">m<sup>2</sup></span>
                    </div>
                </div>
            </div>
            <div class="row mb-3">
                <label for="" class="col-sm-3 control-label"
                    >Survey Duration:</label
                >
                <div class="col-sm-4">
                    <div class="input-group">
                        <input
                            id="survey_duration"
                            v-model="
                                occurrence_report_obj.observation_detail
                                    .survey_duration
                            "
                            :disabled="isReadOnly"
                            type="number"
                            class="form-control"
                            placeholder=""
                            min="0"
                            max="2147483647"
                        />
                        <span class="input-group-text">minutes</span>
                    </div>
                </div>
            </div>
            <div class="row mb-3">
                <label for="" class="col-sm-3 control-label">Comments:</label>
                <div class="col-sm-9">
                    <textarea
                        id="survey_duration"
                        v-model="
                            occurrence_report_obj.observation_detail.comments
                        "
                        :disabled="isReadOnly"
                        class="form-control"
                        placeholder=""
                        min="0"
                        rows="6"
                    />
                </div>
            </div>
            <div class="row mb-3">
                <div class="col-sm-12">
                    <button
                        v-if="!updatingObservationDetails"
                        :disabled="isReadOnly"
                        class="btn btn-primary btn-sm float-end"
                        @click.prevent="updateObservationDetails()"
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

        <FormSection
            v-if="isFlora"
            :form-collapse="false"
            label="Plant Count"
            :Index="plantCountBody"
        >
            <PlantCount
                v-if="isFlora"
                id="plantCountDetail"
                ref="plantCountDetail"
                :plant_count="occurrence_report_obj.plant_count"
                :processing_status="occurrence_report_obj.processing_status"
                :is_report="true"
                :occurrence_id="occurrence_report_obj.id"
                :is_external="is_external"
                :is-read-only="isReadOnly"
            >
            </PlantCount>
        </FormSection>

        <FormSection
            v-if="isFauna"
            :form-collapse="false"
            label="Animal Observation"
            :Index="animalObsBody"
        >
            <AnimalObservation
                v-if="isFauna"
                id="animalObservationDetail"
                ref="animalObservationDetail"
                :animal_observation="occurrence_report_obj.animal_observation"
                :processing_status="occurrence_report_obj.processing_status"
                :is_report="true"
                :occurrence_id="occurrence_report_obj.id"
                :is_external="is_external"
                :is-read-only="isReadOnly"
                @update-animal-observation="updateAnimalObservation"
            >
            </AnimalObservation>
        </FormSection>

        <FormSection
            :form-collapse="false"
            label="Identification"
            :Index="identificationBody"
        >
            <div class="row mb-3">
                <label for="" class="col-sm-3 control-label"
                    >ID Confirmed by:</label
                >
                <div class="col-sm-9">
                    <input
                        id="id_confirmed_by"
                        v-model="
                            occurrence_report_obj.identification.id_confirmed_by
                        "
                        :disabled="isReadOnly"
                        type="text"
                        class="form-control"
                        placeholder=""
                    />
                </div>
            </div>
            <div class="row mb-3">
                <label
                    for=""
                    class="col-sm-3 control-label"
                    :class="
                        occurrence_report_obj.processing_status ==
                        constants.PROPOSAL_STATUS.WITH_ASSESSOR.TEXT
                            ? 'fw-bold'
                            : ''
                    "
                    >Identification Certainty:<span
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
                                identification_certainty_list &&
                                identification_certainty_list.length > 0 &&
                                occurrence_report_obj.identification
                                    .identification_certainty_id &&
                                !identification_certainty_list
                                    .map((d) => d.id)
                                    .includes(
                                        occurrence_report_obj.identification
                                            .identification_certainty_id
                                    )
                            "
                        >
                            <input
                                v-if="
                                    occurrence_report_obj.identification
                                        .identification_certainty
                                "
                                type="text"
                                class="form-control mb-3"
                                :value="
                                    occurrence_report_obj.identification
                                        .identification_certainty +
                                    ' (Now Archived)'
                                "
                                disabled
                            />
                            <div class="mb-3 text-muted">
                                Change identification certainty to:
                            </div>
                        </template>
                        <select
                            v-model="
                                occurrence_report_obj.identification
                                    .identification_certainty_id
                            "
                            class="form-select"
                        >
                            <option
                                v-for="option in identification_certainty_list"
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
                                occurrence_report_obj.identification
                                    .identification_certainty
                            "
                            class="form-control"
                            type="text"
                            :disabled="isReadOnly"
                        />
                    </template>
                </div>
            </div>
            <div class="row mb-3">
                <label for="" class="col-sm-3 control-label"
                    >Sample Type:</label
                >
                <div class="col-sm-9">
                    <template v-if="!isReadOnly">
                        <template
                            v-if="
                                sample_type_list &&
                                sample_type_list.length > 0 &&
                                occurrence_report_obj.identification
                                    .sample_type_id &&
                                !sample_type_list
                                    .map((d) => d.id)
                                    .includes(
                                        occurrence_report_obj.identification
                                            .sample_type_id
                                    )
                            "
                        >
                            <input
                                v-if="
                                    occurrence_report_obj.identification
                                        .sample_type
                                "
                                type="text"
                                class="form-control mb-3"
                                :value="
                                    occurrence_report_obj.identification
                                        .sample_type + ' (Now Archived)'
                                "
                                disabled
                            />
                            <div class="mb-3 text-muted">
                                Change sample type to:
                            </div>
                        </template>
                        <select
                            v-model="
                                occurrence_report_obj.identification
                                    .sample_type_id
                            "
                            class="form-select"
                        >
                            <option
                                v-for="option in sample_type_list"
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
                                occurrence_report_obj.identification.sample_type
                            "
                            class="form-control"
                            type="text"
                            :disabled="isReadOnly"
                        />
                    </template>
                </div>
            </div>
            <div class="row mb-3">
                <label for="" class="col-sm-3 control-label"
                    >Sample Destination:</label
                >
                <div class="col-sm-9">
                    <template v-if="!isReadOnly">
                        <template
                            v-if="
                                sample_dest_list &&
                                sample_dest_list.length > 0 &&
                                occurrence_report_obj.identification
                                    .sample_destination_id &&
                                !sample_dest_list
                                    .map((d) => d.id)
                                    .includes(
                                        occurrence_report_obj.identification
                                            .sample_destination_id
                                    )
                            "
                        >
                            <input
                                v-if="
                                    occurrence_report_obj.identification
                                        .sample_destination
                                "
                                type="text"
                                class="form-control mb-3"
                                :value="
                                    occurrence_report_obj.identification
                                        .sample_destination + ' (Now Archived)'
                                "
                                disabled
                            />
                            <div class="mb-3 text-muted">
                                Change sample destination to:
                            </div>
                        </template>
                        <select
                            v-model="
                                occurrence_report_obj.identification
                                    .sample_destination_id
                            "
                            class="form-select"
                        >
                            <option
                                v-for="option in sample_dest_list"
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
                                occurrence_report_obj.identification
                                    .sample_destination
                            "
                            class="form-control"
                            type="text"
                            :disabled="isReadOnly"
                        />
                    </template>
                </div>
            </div>
            <div class="row mb-3">
                <label for="" class="col-sm-3 control-label"
                    >Permit Type:</label
                >
                <div class="col-sm-9">
                    <template v-if="!isReadOnly">
                        <template
                            v-if="
                                permit_type_list &&
                                permit_type_list.length > 0 &&
                                occurrence_report_obj.identification
                                    .permit_type_id &&
                                !permit_type_list
                                    .map((d) => d.id)
                                    .includes(
                                        occurrence_report_obj.identification
                                            .permit_type_id
                                    )
                            "
                        >
                            <input
                                v-if="
                                    occurrence_report_obj.identification
                                        .permit_type
                                "
                                type="text"
                                class="form-control mb-3"
                                :value="
                                    occurrence_report_obj.identification
                                        .permit_type + ' (Now Archived)'
                                "
                                disabled
                            />
                            <div class="mb-3 text-muted">
                                Change permit type to:
                            </div>
                        </template>
                        <select
                            v-model="
                                occurrence_report_obj.identification
                                    .permit_type_id
                            "
                            class="form-select"
                        >
                            <option
                                v-for="option in permit_type_list"
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
                                occurrence_report_obj.identification.permit_type
                            "
                            class="form-control"
                            type="text"
                            :disabled="isReadOnly"
                        />
                    </template>
                </div>
            </div>
            <div class="row mb-3">
                <label for="" class="col-sm-3 control-label">Permit ID:</label>
                <div class="col-sm-9">
                    <input
                        id="permit_id"
                        v-model="occurrence_report_obj.identification.permit_id"
                        :disabled="isReadOnly"
                        type="text"
                        class="form-control"
                        placeholder=""
                    />
                </div>
            </div>
            <div class="row mb-3">
                <label for="" class="col-sm-3 control-label"
                    >Sample Label/ Collector Number:</label
                >
                <div class="col-sm-9">
                    <textarea
                        id="collector_number"
                        v-model="
                            occurrence_report_obj.identification
                                .collector_number
                        "
                        :disabled="isReadOnly"
                        type="text"
                        row="2"
                        class="form-control"
                        placeholder=""
                    />
                </div>
            </div>
            <div class="row mb-3">
                <label for="" class="col-sm-3 control-label"
                    >Barcode/Catalog Number:</label
                >
                <div class="col-sm-9">
                    <textarea
                        id="barcode_number"
                        v-model="
                            occurrence_report_obj.identification.barcode_number
                        "
                        :disabled="isReadOnly"
                        type="text"
                        row="2"
                        class="form-control"
                        placeholder=""
                    />
                </div>
            </div>
            <div class="row mb-3">
                <label for="" class="col-sm-3 control-label"
                    >Identification Comments:</label
                >
                <div class="col-sm-9">
                    <textarea
                        id="identification_comment"
                        v-model="
                            occurrence_report_obj.identification
                                .identification_comment
                        "
                        :disabled="isReadOnly"
                        type="text"
                        row="2"
                        class="form-control"
                        placeholder=""
                    />
                </div>
            </div>
            <div class="row mb-3">
                <div class="col-sm-12">
                    <!-- <button v-if="!updatingHabitatCompositionDetails" class="pull-right btn btn-primary" @click.prevent="updateDetails()" :disabled="!can_update()">Update</button> -->
                    <button
                        v-if="!updatingIdentificationDetails"
                        :disabled="isReadOnly"
                        class="btn btn-primary btn-sm float-end"
                        @click.prevent="updateIdentificationDetails()"
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
import FormSection from '@/components/forms/section_toggle.vue';
import PlantCount from './plant_count.vue';
import AnimalObservation from './animal_observation.vue';
import { api_endpoints, constants, helpers } from '@/utils/hooks';
export default {
    name: 'OCRObservation',
    components: {
        FormSection,
        PlantCount,
        AnimalObservation,
    },
    props: {
        occurrence_report_obj: {
            type: Object,
            required: true,
        },
        // this prop is only send from split species form to make the original species readonly
        is_readonly: {
            type: Boolean,
            default: false,
        },
        is_external: {
            type: Boolean,
            default: false,
        },
    },
    data: function () {
        let vm = this;
        return {
            constants: constants,
            observationDetailBody: 'observationDetailBody' + uuid(),
            plantCountBody: 'plantCountBody' + uuid(),
            animalObsBody: 'animalObsBody' + uuid(),
            identificationBody: 'identificationBody' + uuid(),
            //---to show fields related to Fauna
            isFauna:
                vm.occurrence_report_obj.group_type === 'fauna' ? true : false,
            isFlora:
                vm.occurrence_report_obj.group_type === 'flora' ? true : false,
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
        };
    },
    computed: {
        isReadOnly: function () {
            //override for split reports
            if (this.is_readonly) {
                return this.is_readonly;
            }
            return this.occurrence_report_obj.readonly;
        },
    },
    watch: {},
    created: async function () {
        let vm = this;
        //------fetch list of values
        const response = await fetch(
            `/api/occurrence/observation_list_of_values.json?group_type=${vm.occurrence_report_obj.group_type}`
        );
        vm.listOfValuesDict = await response.json();
        vm.observation_method_list =
            vm.listOfValuesDict.observation_method_list;
        vm.observation_method_list.splice(0, 0, {
            id: null,
            name: null,
        });

        vm.identification_certainty_list =
            vm.listOfValuesDict.identification_certainty_list;
        vm.identification_certainty_list.splice(0, 0, {
            id: null,
            name: null,
        });
        vm.sample_type_list = vm.listOfValuesDict.sample_type_list;
        vm.sample_type_list.splice(0, 0, {
            id: null,
            name: null,
        });
        vm.sample_dest_list = vm.listOfValuesDict.sample_dest_list;
        vm.sample_dest_list.splice(0, 0, {
            id: null,
            name: null,
        });
        vm.permit_type_list = vm.listOfValuesDict.permit_type_list;
        vm.permit_type_list.splice(0, 0, {
            id: null,
            name: null,
        });
    },
    mounted: function () {
        let vm = this;
        vm.eventListeners();
    },
    methods: {
        eventListeners: function () {},
        updateObservationDetails: function () {
            let vm = this;
            vm.updatingObservationDetails = true;
            fetch(
                helpers.add_endpoint_json(
                    api_endpoints.occurrence_report,
                    vm.occurrence_report_obj.id + '/update_observation_details'
                ),
                {
                    method: 'POST',
                    body: JSON.stringify(
                        vm.occurrence_report_obj.observation_detail
                    ),
                    headers: {
                        'Content-Type': 'application/json',
                    },
                }
            ).then(
                async (response) => {
                    vm.updatingObservationDetails = false;
                    vm.occurrence_report_obj.observation_detail =
                        await response.json();
                    swal.fire({
                        title: 'Saved',
                        text: 'Observation details have been saved',
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
                },
                (error) => {
                    var text = helpers.apiVueResourceError(error);
                    swal.fire({
                        title: 'Error',
                        text:
                            'Observation details cannot be saved because of the following error: ' +
                            text,
                        icon: 'error',
                        customClass: {
                            confirmButton: 'btn btn-primary',
                        },
                    });
                    vm.updatingObservationDetails = false;
                }
            );
        },
        updateIdentificationDetails: function () {
            let vm = this;
            vm.updatingIdentificationDetails = true;
            fetch(
                helpers.add_endpoint_json(
                    api_endpoints.occurrence_report,
                    vm.occurrence_report_obj.id +
                        '/update_identification_details'
                ),
                {
                    method: 'POST',
                    body: JSON.stringify(
                        vm.occurrence_report_obj.identification
                    ),
                    headers: {
                        'Content-Type': 'application/json',
                    },
                }
            ).then(
                async (response) => {
                    vm.updatingIdentificationDetails = false;
                    vm.occurrence_report_obj.identification =
                        await response.json();
                    swal.fire({
                        title: 'Saved',
                        text: 'Identification details have been saved',
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
                },
                (error) => {
                    var text = helpers.apiVueResourceError(error);
                    swal.fire({
                        title: 'Error',
                        text:
                            'Identification details cannot be saved because of the following error: ' +
                            text,
                        icon: 'error',
                        customClass: {
                            confirmButton: 'btn btn-primary',
                        },
                    });
                    vm.updatingIdentificationDetails = false;
                }
            );
        },
        updateAnimalObservation: function (data) {
            this.occurrence_report_obj.animal_observation = data;
        },
    },
};
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

input.plant_count {
    width: 63%;
}
</style>
