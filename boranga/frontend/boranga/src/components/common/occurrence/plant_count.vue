<template lang="html">
    <div id="plant_count">
        <div class="row mb-3">
            <label for="" class="col-sm-3 control-label">Plant Count Method:</label>
            <div class="col-sm-9">
                <template v-if="!isReadOnly">
                    <template
                        v-if="plant_count_method_list && plant_count_method_list.length > 0 && plant_count.plant_count_method_id && !plant_count_method_list.map((d) => d.id).includes(plant_count.plant_count_method_id)">
                        <input type="text" v-if="plant_count.plant_count_method" class="form-control mb-3"
                            :value="plant_count.plant_count_method + ' (Now Archived)'" disabled />
                        <div class="mb-3 text-muted">
                            Change plant count method to:
                        </div>
                    </template>
                    <select class="form-select" v-model="plant_count.plant_count_method_id">
                        <option v-for="plant_count_method in plant_count_method_list" :value="plant_count_method.id"
                            v-bind:key="plant_count_method.id">
                            {{ plant_count_method.name }}
                        </option>
                    </select>
                </template>
                <template v-else>
                    <input class="form-control" type="text" :disabled="isReadOnly"
                        v-model="plant_count.plant_count_method" />
                </template>
            </div>
        </div>
        <div class="row mb-3">
            <label for="" class="col-sm-3 control-label">Plant Count Accuracy:</label>
            <div class="col-sm-9">
                <template v-if="!isReadOnly">
                    <template
                        v-if="plant_count_accuracy_list && plant_count_accuracy_list.length > 0 && plant_count.plant_count_accuracy_id && !plant_count_accuracy_list.map((d) => d.id).includes(plant_count.plant_count_accuracy_id)">
                        <input type="text" v-if="plant_count.plant_count_accuracy" class="form-control mb-3"
                            :value="plant_count.plant_count_accuracy + ' (Now Archived)'" disabled />
                        <div class="mb-3 text-muted">
                            Change plant count accuracy to:
                        </div>
                    </template>
                    <select class="form-select" v-model="plant_count.plant_count_accuracy_id">
                        <option v-for="plant_count_accuracy in plant_count_accuracy_list" :value="plant_count_accuracy.id"
                            v-bind:key="plant_count_accuracy.id">
                            {{ plant_count_accuracy.name }}
                        </option>
                    </select>
                </template>
                <template v-else>
                    <input class="form-control" type="text" :disabled="isReadOnly"
                        v-model="plant_count.plant_count_accuracy" />
                </template>
            </div>
        </div>
        <div class="row mb-3">
            <label for="" class="col-sm-3 control-label">Counted Subject:</label>
            <div class="col-sm-9">
                <select :disabled="isReadOnly" class="form-select" v-model="plant_count.counted_subject_id">
                    <option v-for="option in counted_subject_list" :value="option.id" v-bind:key="option.id">
                        {{ option.name }}
                    </option>
                </select>
            </div>
        </div>
        <div class="row mb-3">
            <label for="" class="col-sm-3 control-label">Plant Count Date: </label>
            <div class="col-sm-9">
                <input v-model="plant_count.count_date
                    " :disabled="true" type="datetime-local" class="form-control" name="plant_count_date" />
            </div>
        </div>
        <div class="row mb-3">
            <label for="" class="col-sm-3 control-label">Estimated Population Area(m<sup>2</sup>) :</label>
            <div class="col-sm-6">
                <input :disabled="isReadOnly" type="number" class="form-control ocr_number" id="est_population_area"
                    placeholder="" min="0" v-model="plant_count.estimated_population_area" />
            </div>
        </div>
        <div class="row mb-3">
            <label for="" class="col-sm-3 control-label">Condition of Plants:</label>
            <div class="col-sm-9">
                <select :disabled="isReadOnly" class="form-select" v-model="plant_count.plant_condition_id">
                    <option v-for="option in plant_condition_list" :value="option.id" v-bind:key="option.id">
                        {{ option.name }}
                    </option>
                </select>
            </div>
        </div>
        <label for="" class="col-lg-3 control-label fs-5 fw-bold">Plant Count - Detailed</label>
        <div class="row mb-3">
            <div class="col-sm-2">
                <label class="form-check-label fw-bold" for="not-counted">Not Counted</label>
            </div>
            <div class="col-sm-2">
                <input type="checkbox" id="not-counted" v-model="plant_count.counted" true-value="false"
                    false-value="true" @change="checkboxChanged">
            </div>
        </div>
        <div class="row mb-3">
            <div class="col-sm-3">

            </div>
            <div class="col-sm-2 fw-bold">
                Mature
            </div>
            <div class="col-sm-2 fw-bold">
                Juvenile
            </div>
            <div class="col-sm-2 fw-bold">
                Seedling
            </div>
            <div class="col-sm-2 fw-bold">
                Unknown
            </div>
        </div>
        <div class="row mb-3">
            <div class="col-sm-3 fw-bold">
                Alive
            </div>
            <div class="col-sm-2">
                <input :disabled="isReadOnly || not_counted" type="number" class="form-control plant_count"
                    id="alive_mature" placeholder="" min="0" v-model="plant_count.detailed_alive_mature" />
            </div>
            <div class="col-sm-2">
                <input :disabled="isReadOnly || not_counted" type="number" class="form-control plant_count"
                    id="plant_alive_juvenile" placeholder="" min="0" v-model="plant_count.detailed_alive_juvenile" />
            </div>
            <div class="col-sm-2">
                <input :disabled="isReadOnly || not_counted" type="number" class="form-control plant_count"
                    id="alive_seedling" placeholder="" min="0" v-model="plant_count.detailed_alive_seedling" />
            </div>
            <div class="col-sm-2">
                <input :disabled="isReadOnly || not_counted" type="number" class="form-control plant_count"
                    id="alive_unknown" placeholder="" min="0" v-model="plant_count.detailed_alive_unknown" />
            </div>
        </div>
        <div class="row mb-3">
            <div class="col-sm-3 fw-bold">
                Dead
            </div>
            <div class="col-sm-2">
                <input :disabled="isReadOnly || not_counted" type="number" class="form-control plant_count"
                    id="dead_mature" placeholder="" min="0" v-model="plant_count.detailed_dead_mature" />
            </div>
            <div class="col-sm-2">
                <input :disabled="isReadOnly || not_counted" type="number" class="form-control plant_count"
                    id="plant_dead_juvenile" placeholder="" min="0" v-model="plant_count.detailed_dead_juvenile" />
            </div>
            <div class="col-sm-2">
                <input :disabled="isReadOnly || not_counted" type="number" class="form-control plant_count"
                    id="dead_seedling" placeholder="" min="0" v-model="plant_count.detailed_dead_seedling" />
            </div>
            <div class="col-sm-2">
                <input :disabled="isReadOnly || not_counted" type="number" class="form-control plant_count"
                    id="dead_unknown" placeholder="" min="0" v-model="plant_count.detailed_dead_unknown" />
            </div>
        </div>
        <label for="" class="col-lg-3 control-label fs-5 fw-bold">Plant Count - Simple</label>
        <div class="row mb-3">
            <label for="" class="col-sm-3 control-label">Number alive :</label>
            <div class="col-sm-6">
                <input :disabled="isReadOnly || not_counted" type="number" class="form-control ocr_number"
                    id="simple_alive" placeholder="" min="0" v-model="plant_count.simple_alive" />
            </div>
        </div>
        <div class="row mb-3">
            <label for="" class="col-sm-3 control-label">Number dead :</label>
            <div class="col-sm-6">
                <input :disabled="isReadOnly || not_counted" type="number" class="form-control ocr_number"
                    id="simple_dead" placeholder="" min="0" v-model="plant_count.simple_dead" />
            </div>
        </div>
        <label for="" class="col-lg-3 control-label fs-5 fw-bold">Quadrats</label>
        <div class="row mb-3">
            <label class="col-sm-3 control-label">Quadrats Present?</label>
            <div class="col">
                <div class="form-check form-check-inline">
                    <label for="quadratsPresentYes">Yes</label>
                    <input :disabled="isReadOnly" id="quadratsPresentYes" class="form-check-input" type="radio"
                        v-model="plant_count.quadrats_present" value="true">&nbsp;
                </div>
                <div class="form-check form-check-inline">
                    <label for="quadratsPresentNo">No</label>
                    <input :disabled="isReadOnly" id="quadratsPresentNo" class="form-check-input" type="radio"
                        v-model="plant_count.quadrats_present" value="false">&nbsp;
                </div>
            </div>
        </div>
        <div class="row mb-3">
            <label class="col-sm-3 control-label">Quadrats Data attached?</label>
            <div class="col">
                <div class="form-check form-check-inline">
                    <label for="quadratsDataYes">Yes</label>
                    <input :disabled="isReadOnly" id="quadratsDataYes" class="form-check-input" type="radio"
                        v-model="plant_count.quadrats_data_attached" value="true">&nbsp;
                </div>
                <div class="form-check form-check-inline">
                    <label for="quadratsDataNo">No</label>
                    <input :disabled="isReadOnly" id="quadratsDataNo" class="form-check-input" type="radio"
                        v-model="plant_count.quadrats_data_attached" value="false">&nbsp;
                </div>
            </div>
        </div>
        <div class="row mb-3">
            <label for="" class="col-sm-3 control-label">Number of quadrats surveyed :</label>
            <div class="col-sm-6">
                <input :disabled="isReadOnly" type="number" class="form-control ocr_number" id="quadrats_surveyed"
                    placeholder="" min="0" v-model="plant_count.quadrats_surveyed" />
            </div>
        </div>
        <div class="row mb-3">
            <label for="" class="col-sm-3 control-label">Individual quadrat area (m<sup>2</sup>) :</label>
            <div class="col-sm-6">
                <input :disabled="isReadOnly" type="number" class="form-control ocr_number" id="ind_quadrat_area"
                    placeholder="" min="0" v-model="plant_count.individual_quadrat_area" />
            </div>
        </div>
        <div class="row mb-3">
            <label for="" class="col-sm-3 control-label">Total quadrat area (m<sup>2</sup>) :</label>
            <div class="col-sm-6">
                <input :disabled="isReadOnly" type="number" class="form-control ocr_number" id="tot_quadrat_area"
                    placeholder="" min="0" v-model="plant_count.total_quadrat_area" />
            </div>
        </div>
        <div class="row mb-3">
            <label for="" class="col-sm-3 control-label">Flowering plants % :</label>
            <div class="col-sm-6">
                <input :disabled="isReadOnly" type="number" class="form-control ocr_number" id="flow_plant_per"
                    placeholder="" min="0" max="100" v-model="plant_count.flowering_plants_per" />
            </div>
        </div>
        <label for="" class="col-lg-3 control-label fs-5 fw-bold"></label>
        <div class="row mb-3">
            <label class="col-sm-3 control-label">Clonal Reproduction present?</label>
            <div class="col">
                <div class="form-check form-check-inline">
                    <label for="reprodPresentYes">Yes</label>
                    <input :disabled="isReadOnly" id="reprodPresentYes" class="form-check-input" type="radio"
                        v-model="plant_count.clonal_reproduction_present" value="true">&nbsp;
                </div>
                <div class="form-check form-check-inline">
                    <label for="reprodPresentNo">No</label>
                    <input :disabled="isReadOnly" id="reprodPresentNo" class="form-check-input" type="radio"
                        v-model="plant_count.clonal_reproduction_present" value="false">&nbsp;
                </div>
            </div>
        </div>
        <div class="row mb-3">
            <label class="col-sm-3 control-label">Vegetative State present?</label>
            <div class="col">
                <div class="form-check form-check-inline">
                    <label for="vegStatePresentYes">Yes</label>
                    <input :disabled="isReadOnly" id="vegStatePresentYes" class="form-check-input" type="radio"
                        v-model="plant_count.vegetative_state_present" value="true">&nbsp;
                </div>
                <div class="form-check form-check-inline">
                    <label for="vegStatePresentNo">No</label>
                    <input :disabled="isReadOnly" id="vegStatePresentNo" class="form-check-input" type="radio"
                        v-model="plant_count.vegetative_state_present" value="false">&nbsp;
                </div>
            </div>
        </div>
        <div class="row mb-3">
            <label class="col-sm-3 control-label">Flower Buds present?</label>
            <div class="col">
                <div class="form-check form-check-inline">
                    <label for="flowerBudsPresentYes">Yes</label>
                    <input :disabled="isReadOnly" id="flowerBudsPresentYes" class="form-check-input" type="radio"
                        v-model="plant_count.flower_bud_present" value="true">&nbsp;
                </div>
                <div class="form-check form-check-inline">
                    <label for="flowerBudsPresentNo">No</label>
                    <input :disabled="isReadOnly" id="flowerBudsPresentNo" class="form-check-input" type="radio"
                        v-model="plant_count.flower_bud_present" value="false">&nbsp;
                </div>
            </div>
        </div>
        <div class="row mb-3">
            <label class="col-sm-3 control-label">Flowers present?</label>
            <div class="col">
                <div class="form-check form-check-inline">
                    <label for="flowerPresentYes">Yes</label>
                    <input :disabled="isReadOnly" id="flowerPresentYes" class="form-check-input" type="radio"
                        v-model="plant_count.flower_present" value="true">&nbsp;
                </div>
                <div class="form-check form-check-inline">
                    <label for="flowerPresentNo">No</label>
                    <input :disabled="isReadOnly" id="flowerPresentNo" class="form-check-input" type="radio"
                        v-model="plant_count.flower_present" value="false">&nbsp;
                </div>
            </div>
        </div>
        <div class="row mb-3">
            <label class="col-sm-3 control-label">Immature Fruit present?</label>
            <div class="col">
                <div class="form-check form-check-inline">
                    <label for="immFruitPresentYes">Yes</label>
                    <input :disabled="isReadOnly" id="immFruitPresentYes" class="form-check-input" type="radio"
                        v-model="plant_count.immature_fruit_present" value="true">&nbsp;
                </div>
                <div class="form-check form-check-inline">
                    <label for="immFruitPresentNo">No</label>
                    <input :disabled="isReadOnly" id="immFruitPresentNo" class="form-check-input" type="radio"
                        v-model="plant_count.immature_fruit_present" value="false">&nbsp;
                </div>
            </div>
        </div>
        <div class="row mb-3">
            <label class="col-sm-3 control-label">Ripe Fruit present?</label>
            <div class="col">
                <div class="form-check form-check-inline">
                    <label for="ripeFruitPresentYes">Yes</label>
                    <input :disabled="isReadOnly" id="ripeFruitPresentYes" class="form-check-input" type="radio"
                        v-model="plant_count.ripe_fruit_present" value="true">&nbsp;
                </div>
                <div class="form-check form-check-inline">
                    <label for="ripeFruitPresentNo">No</label>
                    <input :disabled="isReadOnly" id="ripeFruitPresentNo" class="form-check-input" type="radio"
                        v-model="plant_count.ripe_fruit_present" value="false">&nbsp;
                </div>
            </div>
        </div>
        <div class="row mb-3">
            <label class="col-sm-3 control-label">Dehisced Fruit present?</label>
            <div class="col">
                <div class="form-check form-check-inline">
                    <label for="dehFruitPresentYes">Yes</label>
                    <input :disabled="isReadOnly" id="dehFruitPresentYes" class="form-check-input" type="radio"
                        v-model="plant_count.dehisced_fruit_present" value="true">&nbsp;
                </div>
                <div class="form-check form-check-inline">
                    <label for="dehFruitPresentNo">No</label>
                    <input :disabled="isReadOnly" id="dehFruitPresentNo" class="form-check-input" type="radio"
                        v-model="plant_count.dehisced_fruit_present" value="false">&nbsp;
                </div>
            </div>
        </div>
        <div class="row mb-3">
            <label for="" class="col-sm-3 control-label">Pollinator Observations :</label>
            <div class="col-sm-9">
                <textarea :disabled="isReadOnly" type="text" row="2" class="form-control" id="pollinator_obs"
                    placeholder="" v-model="plant_count.pollinator_observation" />
            </div>
        </div>
        <div class="row mb-3">
            <label for="" class="col-sm-3 control-label">Plant Count Comments :</label>
            <div class="col-sm-9">
                <textarea :disabled="isReadOnly" type="text" row="2" class="form-control" id="plant_count_comment"
                    placeholder="" v-model="plant_count.comment" />
            </div>
        </div>
        <div class="row mb-3">
            <div class="col-sm-12">
                <span v-if="plant_count.copied_ocr" class="float-end"><b>Sourced from
                        {{ plant_count.copied_ocr }}</b></span>
            </div>
        </div>
        <div class="row mb-3">
            <div class="col-sm-12">
                <button v-if="!updatingPlantCountDetails" :disabled="isReadOnly"
                    class="btn btn-primary btn-sm float-end" @click.prevent="updatePlantCountDetails()">Update</button>
                <button v-else disabled class="float-end btn btn-primary">Updating <span
                        class="spinner-border spinner-border-sm" role="status" aria-hidden="true"></span>
                    <span class="visually-hidden">Loading...</span></button>
            </div>
        </div>
    </div>
</template>

<script>
import Vue from 'vue';
import FormSection from '@/components/forms/section_toggle.vue';
import {
    api_endpoints,
    helpers
}
    from '@/utils/hooks'
export default {
    name: 'PlantCount',
    props: {
        plant_count: {
            type: Object,
            required: true
        },
        is_report: {
            type: Boolean,
            required: true
        },
        occurrence_id: {
            type: Number,
            required: true
        },
        processing_status: {
            type: String,
            required: false
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
        isReadOnly: {
            type: Boolean,
            default: false
        },
    },
    data: function () {
        let vm = this;
        return {
            //----list of values dictionary
            listOfPlantValuesDict: {},
            plant_count_method_list: [],
            plant_count_accuracy_list: [],
            plant_condition_list: [],
            counted_subject_list: [],
            updatingPlantCountDetails: false,
            not_counted: false,
        }
    },
    components: {
        FormSection,
    },
    computed: {
    },
    watch: {
    },
    methods: {
        eventListeners: function () {
        },
        checkboxChanged: function () {
            this.not_counted = this.plant_count.counted == 'false';
        },
        updatePlantCountDetails: function () {
            let vm = this;
            vm.updatingPlantCountDetails = true;
            let endpoint = api_endpoints.occurrence;
            if (vm.is_report) {
                endpoint = api_endpoints.occurrence_report;
            }
            vm.$http.post(helpers.add_endpoint_json(endpoint, (vm.occurrence_id + '/update_plant_count_details')), JSON.stringify(vm.plant_count), {
                emulateJSON: true
            }).then((response) => {
                vm.updatingPlantCountDetails = false;
                //vm.plant_count = response.body;
                swal.fire({
                    title: 'Saved',
                    text: 'Plant Count details have been saved',
                    icon: 'success',
                    customClass: {
                        confirmButton: 'btn btn-primary'
                    },
                }).then((result) => {
                    if (vm.processing_status == "Unlocked") {
                        vm.$router.go();
                    }
                });
            }, (error) => {
                var text = helpers.apiVueResourceError(error);
                swal.fire({
                    title: 'Error',
                    text: 'Plant Count details cannot be saved because of the following error: ' + text,
                    icon: 'error',
                    customClass: {
                        confirmButton: 'btn btn-primary'
                    },
                });
                vm.updatingPlantCountDetails = false;
            });
        },
    },
    created: async function () {
        let vm = this;
        const res = await Vue.http.get(`/api/occurrence/plant_count_list_of_values.json`);
        vm.listOfPlantValuesDict = res.body;
        vm.plant_count_method_list = vm.listOfPlantValuesDict.plant_count_method_list;
        vm.plant_count_method_list.splice(0, 0,
            {
                id: null,
                name: null,
            });
        vm.plant_count_accuracy_list = vm.listOfPlantValuesDict.plant_count_accuracy_list;
        vm.plant_count_accuracy_list.splice(0, 0,
            {
                id: null,
                name: null,
            });
        vm.plant_condition_list = vm.listOfPlantValuesDict.plant_condition_list;
        vm.plant_condition_list.splice(0, 0,
            {
                id: null,
                name: null,
            });
        vm.counted_subject_list = vm.listOfPlantValuesDict.counted_subject_list;
        vm.counted_subject_list.splice(0, 0,
            {
                id: null,
                name: null,
            });

    },
    mounted: function () {
        let vm = this;
        //this.$emit('component-mounted');
        vm.not_counted = !vm.plant_count.counted;

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

input.plant_count {
    width: 63%;
}

input.ocr_number {
    width: 20%;
}
</style>
