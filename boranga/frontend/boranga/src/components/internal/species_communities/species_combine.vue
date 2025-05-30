<template lang="html">
    <div id="combineSpecies">
        <modal
            id="species-combine-modal"
            transition="modal fade"
            :title="title"
            extra-large
            @ok="ok()"
            @cancel="cancel()"
        >
            <div class="container-fluid">
                <div class="row">
                    <form class="form-horizontal" name="combineSpeciesForm">
                        <alert v-if="showError" type="danger"
                            ><strong>{{ errorString }}</strong></alert
                        >
                        <div>
                            <div class="col-md-12">
                                <ul
                                    v-if="is_internal"
                                    id="combine-pills-tab"
                                    class="nav nav-pills"
                                    role="tablist"
                                >
                                    <li class="nav-item">
                                        <a
                                            id="pills-new-species-tab"
                                            class="nav-link"
                                            data-bs-toggle="pill"
                                            :data-bs-target="`#${newSpeciesBody}`"
                                            :href="'#' + newSpeciesBody"
                                            role="tab"
                                            :aria-controls="newSpeciesBody"
                                            aria-selected="true"
                                        >
                                            New Species
                                            {{
                                                new_combine_species
                                                    ? new_combine_species.species_number
                                                    : ''
                                            }}
                                        </a>
                                    </li>
                                    <li
                                        v-for="(
                                            species, index
                                        ) in original_species_combine_list"
                                        :key="'li' + species.id"
                                        class="nav-item"
                                    >
                                        <a
                                            :id="
                                                'pills-species-' +
                                                index +
                                                '-tab'
                                            "
                                            class="nav-link"
                                            data-bs-toggle="pill"
                                            :data-bs-target="
                                                '#species-body-' + index
                                            "
                                            :href="'#species-body-' + index"
                                            role="tab"
                                            :aria-controls="
                                                'species-body-' + index
                                            "
                                            aria-selected="false"
                                        >
                                            {{ species.species_number
                                            }}<span
                                                v-if="index > 0"
                                                :id="index"
                                                class="ms-2"
                                                @click.prevent="
                                                    removeCombineSpecies(
                                                        species
                                                    )
                                                "
                                                ><i
                                                    class="bi bi-trash3-fill"
                                                ></i
                                            ></span>
                                            <!-- can delete the original species except the current original species , so check index>0 -->
                                        </a>
                                    </li>
                                    <li class="nav-item">
                                        <a
                                            id="combineSpeciesBtnAdd"
                                            class="nav-link"
                                            href="#"
                                            @click.prevent="
                                                addSpeciesToCombine()
                                            "
                                            ><i class="bi bi-window-plus"></i>
                                            Add Another Species</a
                                        >
                                    </li>
                                    <li class="nav-item">
                                        <a
                                            id="finalise-combine"
                                            class="nav-link"
                                            data-bs-toggle="pill"
                                            data-bs-target="#finalise-combine-tab-pane"
                                            href="#finalise-combine-tab-pane"
                                            role="tab"
                                            aria-controls="finalise-combine-tab-pane"
                                            aria-selected="false"
                                            ><i class="bi bi-check2-circle"></i>
                                            Finalise Combine</a
                                        >
                                    </li>
                                </ul>
                                <div
                                    id="combine-pills-tabContent"
                                    class="tab-content border p-3"
                                >
                                    <div
                                        :id="newSpeciesBody"
                                        class="tab-pane"
                                        role="tabpanel"
                                        aria-labelledby="pills-new-species-tab"
                                    >
                                        <SpeciesCombineForm
                                            v-if="
                                                new_combine_species &&
                                                new_combine_species.id
                                            "
                                            id="new_combine_species"
                                            ref="species_communities_new"
                                            :key="speciesCombineFormKey"
                                            :species_community="
                                                new_combine_species
                                            "
                                            :original_species_combine_list="
                                                original_species_combine_list
                                            "
                                            :is_internal="true"
                                        >
                                        </SpeciesCombineForm>
                                    </div>
                                    <div
                                        v-for="(
                                            species, index
                                        ) in original_species_combine_list"
                                        :id="'species-body-' + index"
                                        :key="'div' + species.id"
                                        class="tab-pane fade"
                                        role="tabpanel"
                                        :aria-labelledby="
                                            'pills-species' + index + '-tab'
                                        "
                                    >
                                        <SpeciesCommunitiesComponent
                                            :id="'species-' + index"
                                            :ref="
                                                'species_communities_species' +
                                                index
                                            "
                                            :species_community_original="
                                                species
                                            "
                                            :species_community="species"
                                            :is_internal="true"
                                            :is_readonly="true"
                                        >
                                        </SpeciesCommunitiesComponent>
                                    </div>
                                    <div
                                        v-if="
                                            new_combine_species &&
                                            original_species_combine_list &&
                                            original_species_combine_list.length >
                                                0
                                        "
                                        id="finalise-combine-tab-pane"
                                        class="tab-pane"
                                        role="tabpanel"
                                        aria-labelledby="finalise-combine"
                                    >
                                        <p class="border-bottom mb-3">
                                            <HelpText
                                                section_id="species_combine_finalise"
                                            />
                                        </p>

                                        <p>
                                            You are about to combine the
                                            following species:
                                        </p>

                                        <div class="mb-3">
                                            <li
                                                v-for="species in original_species_combine_list"
                                                :key="species.id"
                                                class="text-secondary mb-3"
                                            >
                                                <span
                                                    class="badge bg-light text-primary text-capitalize border p-2 fs-6 me-2"
                                                    >{{
                                                        species.species_number
                                                    }}
                                                    -
                                                    {{
                                                        species.taxonomy_details
                                                            .scientific_name
                                                    }}</span
                                                >
                                            </li>
                                        </div>

                                        <p>Into the new species:</p>

                                        <div class="border-bottom mb-3 pb-3">
                                            <span
                                                class="badge bg-light text-primary text-capitalize border p-2 fs-6"
                                                >{{
                                                    new_combine_species.species_number
                                                }}
                                                <template
                                                    v-if="
                                                        new_combine_species.taxonomy_details &&
                                                        new_combine_species
                                                            .taxonomy_details
                                                            .scientific_name
                                                    "
                                                    >-
                                                    {{
                                                        new_combine_species
                                                            .taxonomy_details
                                                            .scientific_name
                                                    }}</template
                                                ></span
                                            >
                                        </div>

                                        <button
                                            class="button btn btn-primary"
                                            :disabled="finalise_combine_loading"
                                            @click.prevent="ok()"
                                        >
                                            <i class="bi bi-check2-circle"></i>
                                            Finalise Combine
                                            <template
                                                v-if="finalise_combine_loading"
                                                ><span
                                                    class="spinner-border spinner-border-sm"
                                                    role="status"
                                                    aria-hidden="true"
                                                ></span>
                                                <span class="visually-hidden"
                                                    >Loading...</span
                                                ></template
                                            >
                                        </button>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </form>
                </div>
            </div>

            <template #footer>
                <div>
                    <button
                        type="button"
                        class="btn btn-secondary me-2"
                        @click="cancel"
                    >
                        Cancel
                    </button>
                </div>
            </template>
        </modal>

        <AddCombineSpecies ref="addCombineSpecies"></AddCombineSpecies>
    </div>
</template>

<script>
import { v4 as uuid } from 'uuid';
import modal from '@vue-utils/bootstrap-modal.vue';
import alert from '@vue-utils/alert.vue';
import SpeciesCommunitiesComponent from '@/components/form_species_communities.vue';
import SpeciesCombineForm from '@/components/form_species_combine.vue';
import AddCombineSpecies from '@/components/common/species_communities/species_combine/add_combine_species.vue';
import HelpText from '@/components/common/help_text.vue';

import { helpers, api_endpoints } from '@/utils/hooks.js';

export default {
    name: 'SpeciesCombine',
    components: {
        modal,
        alert,
        SpeciesCommunitiesComponent,
        SpeciesCombineForm,
        AddCombineSpecies,
        HelpText,
    },
    props: {
        species_community: {
            type: Object,
            required: true,
        },
        is_internal: {
            type: Boolean,
            required: true,
        },
    },
    data: function () {
        return {
            newSpeciesBody: 'newSpeciesBody' + uuid(),
            speciesBody: 'speciesBody' + uuid(),
            speciesCombineFormKey: 0,
            new_combine_species: null,
            new_combine_species_display: '',
            submitSpeciesCombine: false,
            isModalOpen: false,
            original_species_combine_list: [],
            finalise_combine_loading: false,
            form: null,
            errors: false,
            errorString: '',
        };
    },
    computed: {
        csrf_token: function () {
            return helpers.getCookie('csrftoken');
        },
        showError: function () {
            var vm = this;
            return vm.errors;
        },
        title: function () {
            //return this.processing_status == 'With Approver' ? 'Approve Conservation Status' : 'Propose to approve Conservation Status';
            return this.new_combine_species != null
                ? 'Combine Species '
                : 'Combine Species';
        },
        species_split_form_url: function () {
            var vm = this;
            return `/api/species/${vm.new_combine_species.id}/species_split_save.json`;
        },
        combine_into_species_scientific_name: function () {
            return this.new_combine_species.scientific_name
                ? this.new_combine_species.scientific_name
                : '';
        },
    },
    watch: {
        isModalOpen: function (val) {
            if (val) {
                this.$nextTick(() => {
                    // was added to set the first species Tab active but the updated() method overrides it
                    var firstTabEl = document.querySelector(
                        '#combine-pills-tab li:nth-child(1) a'
                    );
                    var firstTab =
                        bootstrap.Tab.getOrCreateInstance(firstTabEl);
                    firstTab.show();
                });
            }
        },
    },
    mounted: function () {
        let vm = this;
        vm.form = document.forms.combineSpeciesForm;
    },
    methods: {
        ok: function () {
            let vm = this;
            if ($(vm.form).valid()) {
                vm.sendData();
            }
        },
        cancel: function () {
            this.close();
        },
        close: function () {
            let vm = this;
            vm.removeSpecies(vm.new_combine_species.id);
            vm.new_combine_species = null;
            vm.original_species_combine_list = [];
            $(this.$refs.occurrence_name_lookup_propose_approve)
                .empty()
                .trigger('change');
            this.isModalOpen = false;
            vm.speciesCombineFormKey += 1;
            this.errors = false;
        },
        save_before_submit: async function (new_species) {
            let vm = this;
            vm.saveError = false;

            let payload = new Object();
            Object.assign(payload, new_species);
            const result = await fetch(
                `/api/species/${new_species.id}/species_split_save.json`,
                {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify(payload),
                }
            ).then(
                async (response) => {
                    if (!response.ok) {
                        const data = await response.json();
                        swal.fire({
                            title: 'Error',
                            text: data,
                            icon: 'error',
                            customClass: {
                                confirmButton: 'btn btn-primary',
                            },
                        });
                        return;
                    }
                    return true;
                },
                (err) => {
                    var errorText = helpers.apiVueResourceError(err);
                    swal.fire({
                        title: 'Submit Error',
                        text: errorText,
                        icon: 'error',
                        customClass: {
                            confirmButton: 'btn btn-primary',
                        },
                    });
                    vm.submitSpeciesCombine = false;
                    vm.saveError = true;
                    return false;
                }
            );
            return result;
        },
        can_submit: function () {
            let vm = this;
            let blank_fields = [];
            if (
                vm.new_combine_species.taxonomy_id == null ||
                vm.new_combine_species.taxonomy_id == ''
            ) {
                blank_fields.push(
                    ' Species ' +
                        vm.new_combine_species.species_number +
                        ' Scientific Name is missing'
                );
            }
            if (
                vm.new_combine_species.distribution.distribution == null ||
                vm.new_combine_species.distribution.distribution == ''
            ) {
                blank_fields.push(' Distribution is missing');
            }
            if (
                vm.new_combine_species.regions == null ||
                vm.new_combine_species.regions == '' ||
                vm.new_combine_species.regions.length == 0
            ) {
                blank_fields.push(' Region is missing');
            }
            if (
                vm.new_combine_species.districts == null ||
                vm.new_combine_species.districts == '' ||
                vm.new_combine_species.districts.length == 0
            ) {
                blank_fields.push(' District is missing');
            }
            if (blank_fields.length == 0) {
                return true;
            } else {
                return blank_fields;
            }
        },
        sendData: async function () {
            let vm = this;
            var missing_data = vm.can_submit();
            if (missing_data != true) {
                await swal.fire({
                    title: 'Please fix following errors before submitting',
                    text: missing_data,
                    icon: 'error',
                    customClass: {
                        confirmButton: 'btn btn-primary',
                    },
                });
                // was added to set the first species Tab active but the updated() method overrides it
                var firstTabEl = document.querySelector(
                    '#combine-pills-tab li:nth-child(1) a'
                );
                var firstTab = bootstrap.Tab.getOrCreateInstance(firstTabEl);
                firstTab.show();
                return false;
            }

            vm.submitSpeciesCombine = true;
            swal.fire({
                title: 'Combine Species',
                text: 'Are you sure you want to combine those species?',
                icon: 'question',
                showCancelButton: true,
                confirmButtonText: 'Combine Species',
                customClass: {
                    confirmButton: 'btn btn-primary',
                    cancelButton: 'btn btn-secondary',
                },
                reverseButtons: true,
            })
                .then(
                    async (swalresult) => {
                        if (swalresult.isConfirmed) {
                            //---save and submit the new combine species
                            let new_species = vm.new_combine_species;
                            //-- save new species before submit
                            await vm.save_before_submit(new_species);
                            if (!vm.saveError) {
                                vm.finalise_combine_loading = true;

                                // add the parent species array to the new species object
                                new_species.parent_species =
                                    vm.original_species_combine_list;
                                let payload = new Object();
                                Object.assign(payload, new_species);
                                let submit_url = helpers.add_endpoint_json(
                                    api_endpoints.species,
                                    new_species.id +
                                        '/combine_new_species_submit'
                                );
                                fetch(submit_url, {
                                    method: 'POST',
                                    headers: {
                                        'Content-Type': 'application/json',
                                    },
                                    body: JSON.stringify(payload),
                                }).then(
                                    async (response) => {
                                        vm.new_species = await response.json();
                                        vm.$router.push({
                                            name: 'internal-species-communities-dash',
                                        });
                                    },
                                    (err) => {
                                        swal.fire({
                                            title: 'Submit Error',
                                            text: helpers.apiVueResourceError(
                                                err
                                            ),
                                            icon: 'error',
                                            customClass: {
                                                confirmButton:
                                                    'btn btn-primary',
                                            },
                                        });
                                        vm.saveError = true;
                                        vm.finalise_combine_loading = false;
                                    }
                                );
                            }
                        }
                    },
                    (error) => {
                        console.log(error);
                    }
                )
                .finally(() => {
                    vm.finalise_combine_loading = false;
                });
        },
        removeSpecies: function (species_id) {
            try {
                // In this case we are allowing a http DELETE call to remove the species
                fetch(api_endpoints.remove_species_proposal(species_id), {
                    method: 'DELETE',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                });
            } catch (err) {
                console.log(err);
                if (this.is_internal) {
                    return err;
                }
            }
        },
        removeCombineSpecies: function (species) {
            let vm = this;
            swal.fire({
                title: 'Remove Species',
                text: `Are you sure you want to remove species ${species.species_number} from this combine?`,
                icon: 'question',
                showCancelButton: true,
                confirmButtonText: 'Remove Species',
                customClass: {
                    confirmButton: 'btn btn-primary',
                    cancelButton: 'btn btn-secondary',
                },
                reverseButtons: true,
            }).then(async (swalresult) => {
                if (swalresult.isConfirmed) {
                    let species_index =
                        vm.original_species_combine_list.indexOf(species);
                    vm.original_species_combine_list.splice(species_index, 1);
                    this.$nextTick(() => {
                        // was added to set the first species Tab active but the updated() method overrides it
                        var firstTabEl = document.querySelector(
                            '#combine-pills-tab li:nth-child(1) a'
                        );
                        var firstTab =
                            bootstrap.Tab.getOrCreateInstance(firstTabEl);
                        firstTab.show();
                    });
                }
            });
        },
        addSpeciesToCombine: function () {
            this.$refs.addCombineSpecies.isModalOpen = true;
        },
    },
};
</script>

<style scoped>
.bi.bi-trash3-fill:hover {
    cursor: pointer;
    color: red;
}
</style>
