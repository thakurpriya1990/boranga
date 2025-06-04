<template lang="html">
    <div id="splitSpecies">
        <modal
            id="species-split-modal"
            transition="modal fade"
            :title="title"
            extra-large
            @ok="ok()"
            @cancel="cancel()"
        >
            <div class="container-fluid">
                <div class="row">
                    <form class="form-horizontal" name="splitSpeciesForm">
                        <alert v-if="showError" type="danger"
                            ><strong>{{ errorString }}</strong></alert
                        >
                        <div>
                            <div class="col-md-12">
                                <ul
                                    v-if="is_internal"
                                    id="split-pills-tab"
                                    class="nav nav-pills"
                                    role="tablist"
                                >
                                    <li class="nav-item">
                                        <a
                                            id="pills-original-tab"
                                            class="nav-link"
                                            data-bs-toggle="pill"
                                            :href="'#' + originalBody"
                                            role="tab"
                                            :aria-controls="originalBody"
                                            aria-selected="true"
                                        >
                                            Original
                                            {{
                                                species_community_original
                                                    ? species_community_original.species_number
                                                    : ''
                                            }}
                                        </a>
                                    </li>
                                    <li
                                        v-for="(
                                            species, index
                                        ) in new_species_list"
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
                                            :href="'#species-body-' + index"
                                            role="tab"
                                            :aria-controls="
                                                'species-body-' + index
                                            "
                                            aria-selected="false"
                                        >
                                            {{ species.species_number }}
                                            <span :id="index" class="ms-2"
                                                ><i
                                                    class="bi bi-trash3-fill"
                                                ></i
                                            ></span>
                                        </a>
                                    </li>
                                    <li class="nav-item">
                                        <a
                                            id="btnAdd"
                                            href="#"
                                            role="button"
                                            class="nav-link"
                                            @click.prevent="addSpecies"
                                            ><i class="bi bi-window-plus"></i>
                                            Add Another Species</a
                                        >
                                    </li>
                                    <li class="nav-item">
                                        <a
                                            id="finalise-split"
                                            class="nav-link"
                                            data-bs-toggle="pill"
                                            href="#finalise-split-tab-pane"
                                            role="tab"
                                            aria-controls="finalise-split-tab-pane"
                                            aria-selected="false"
                                            ><i class="bi bi-check2-circle"></i>
                                            Finalise Split</a
                                        >
                                    </li>
                                </ul>
                                <div
                                    id="split-pills-tabContent"
                                    class="tab-content border p-3"
                                >
                                    <!-- the fade show active was creating the problem of rendering two thing on tab -->
                                    <div
                                        :id="originalBody"
                                        class="tab-pane"
                                        role="tabpanel"
                                        aria-labelledby="pills-original-tab"
                                    >
                                        <SpeciesCommunitiesComponent
                                            v-if="
                                                species_community_original !=
                                                null
                                            "
                                            id="species_original"
                                            ref="species_communities_original"
                                            :species_community_original="
                                                species_community_original
                                            "
                                            :species_community="
                                                species_community_original
                                            "
                                            :is_internal="true"
                                            :is_readonly="true"
                                        >
                                            <!-- this prop is only send from split species form to make the original species readonly -->
                                        </SpeciesCommunitiesComponent>
                                    </div>
                                    <div
                                        v-for="(
                                            species, index
                                        ) in new_species_list"
                                        :id="'species-body-' + index"
                                        :key="'div' + species.id"
                                        class="tab-pane fade"
                                        role="tabpanel"
                                        :aria-labelledby="
                                            'pills-species-' + index + '-tab'
                                        "
                                    >
                                        <SpeciesSplitForm
                                            :id="'species-' + index"
                                            :ref="
                                                'species_communities_species' +
                                                index
                                            "
                                            :species_community="species"
                                            :species_original="
                                                species_community_original
                                            "
                                            :is_internal="true"
                                        >
                                        </SpeciesSplitForm>
                                    </div>
                                    <div
                                        v-if="
                                            species_community_original &&
                                            new_species_list &&
                                            new_species_list.length > 0
                                        "
                                        id="finalise-split-tab-pane"
                                        class="tab-pane"
                                        role="tabpanel"
                                        aria-labelledby="finalise-split"
                                    >
                                        <p class="border-bottom mb-3">
                                            <HelpText
                                                section_id="species_split_finalise"
                                            />
                                        </p>

                                        <p>
                                            You are about to split the following
                                            species:
                                        </p>

                                        <div class="border-bottom mb-3 pb-3">
                                            <span
                                                class="badge bg-light text-primary text-capitalize border p-2 fs-6"
                                                >{{
                                                    species_community_original.species_number
                                                }}
                                                <template
                                                    v-if="
                                                        species_community_original
                                                            .taxonomy_details
                                                            .scientific_name
                                                    "
                                                    >-
                                                    {{
                                                        species_community_original
                                                            .taxonomy_details
                                                            .scientific_name
                                                    }}</template
                                                ></span
                                            >
                                        </div>

                                        <p>Into the new species:</p>

                                        <div class="border-bottom mb-3 pb-3">
                                            <ul class="mb-3">
                                                <li
                                                    v-for="species in new_species_list"
                                                    :key="species.id"
                                                    class="text-secondary mb-3"
                                                >
                                                    <span
                                                        class="badge bg-light text-primary text-capitalize border p-2 fs-6 me-2"
                                                        >{{
                                                            species.species_number
                                                        }}
                                                        <template
                                                            v-if="
                                                                species.taxonomy_details &&
                                                                species
                                                                    .taxonomy_details
                                                                    .scientific_name
                                                            "
                                                            >-
                                                            {{
                                                                species
                                                                    .taxonomy_details
                                                                    .scientific_name
                                                            }}</template
                                                        >
                                                    </span>
                                                </li>
                                            </ul>
                                        </div>

                                        <button
                                            class="button btn btn-primary"
                                            :disabled="finalise_split_loading"
                                            @click.prevent="ok()"
                                        >
                                            <i class="bi bi-check2-circle"></i>
                                            Finalise Split
                                            <template
                                                v-if="finalise_split_loading"
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
    </div>
</template>

<script>
import { v4 as uuid } from 'uuid';
import modal from '@vue-utils/bootstrap-modal.vue';
import alert from '@vue-utils/alert.vue';
import SpeciesCommunitiesComponent from '@/components/form_species_communities.vue';
import SpeciesSplitForm from '@/components/form_species_split.vue';
import HelpText from '@/components/common/help_text.vue';

import { helpers, api_endpoints } from '@/utils/hooks.js';
export default {
    name: 'SpeciesSplit',
    components: {
        modal,
        alert,
        SpeciesCommunitiesComponent,
        SpeciesSplitForm,
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
            originalBody: 'originalBody' + uuid(),
            species2Body: 'species2Body' + uuid(),
            species_community_original: null,
            submitSpeciesSplit: false,
            isModalOpen: false,
            finalise_split_loading: false,
            new_species_list: [],
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
            return this.species_community_original != null
                ? 'Split Species ' +
                      this.species_community_original.species_number
                : 'Split Species';
        },
        species_split_form_url: function () {
            var vm = this;
            return `/api/species/${vm.species_community_original.id}/species_split_save.json`;
        },
    },
    mounted: function () {
        let vm = this;
        vm.form = document.forms.splitSpeciesForm;
        this.$nextTick(() => {
            vm.eventListeners();
        });
    },
    updated: function () {
        if (!this.finalise_split_loading) {
            //  to show the the added species active i.e the last Tab
            var lastTabEl = document.querySelector(
                '#split-pills-tab li:nth-last-child(3) a'
            );
            var lastTab = new bootstrap.Tab(lastTabEl);
            lastTab.show();
        }
    },
    methods: {
        tabClicked: function () {},
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
            if (vm.new_species_list.length > 0) {
                for (
                    var index = 0;
                    index < vm.new_species_list.length;
                    index++
                ) {
                    vm.removeSpecies(vm.new_species_list[index].id);
                }
            }
            vm.new_species_list = [];
            this.isModalOpen = false;
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
                            text: JSON.stringify(data),
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
                    vm.submitSpeciesSplit = false;
                    vm.saveError = true;
                    return false;
                }
            );
            return result;
        },
        can_submit: function () {
            let vm = this;
            let blank_fields = [];
            for (let index = 0; index < vm.new_species_list.length; index++) {
                if (
                    vm.new_species_list[index].taxonomy_id == null ||
                    vm.new_species_list[index].taxonomy_id == ''
                ) {
                    blank_fields.push(
                        ' Species ' +
                            vm.new_species_list[index].species_number +
                            ' Scientific Name is missing'
                    );
                }
                if (
                    vm.new_species_list[index].distribution.distribution ==
                        null ||
                    vm.new_species_list[index].distribution.distribution == ''
                ) {
                    blank_fields.push(
                        ' Species ' +
                            vm.new_species_list[index].species_number +
                            ' Distribution is missing'
                    );
                }
                if (
                    vm.new_species_list[index].regions == null ||
                    vm.new_species_list[index].regions == '' ||
                    vm.new_species_list[index].regions.length == 0
                ) {
                    blank_fields.push(
                        ' Species ' +
                            vm.new_species_list[index].species_number +
                            ' Region is missing'
                    );
                }
                if (
                    vm.new_species_list[index].districts == null ||
                    vm.new_species_list[index].districts == '' ||
                    vm.new_species_list[index].districts.length == 0
                ) {
                    blank_fields.push(
                        ' Species ' +
                            vm.new_species_list[index].species_number +
                            ' District is missing'
                    );
                }
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
                swal.fire({
                    title: 'Please fix following errors before submitting',
                    text: missing_data,
                    icon: 'error',
                    customClass: {
                        confirmButton: 'btn btn-primary',
                    },
                });
                return false;
            }

            vm.submitSpeciesSplit = true;
            swal.fire({
                title: 'Split Species',
                text: 'Are you sure you want to split this species?',
                icon: 'question',
                showCancelButton: true,
                confirmButtonText: 'Split Species',
                customClass: {
                    confirmButton: 'btn btn-primary',
                    cancelButton: 'btn btn-secondary',
                },
                reverseButtons: true,
            }).then(
                async (swalresult) => {
                    if (swalresult.isConfirmed) {
                        vm.finalise_split_loading = true;
                        for (
                            let index = 0;
                            index < vm.new_species_list.length;
                            index++
                        ) {
                            let new_species = vm.new_species_list[index];
                            //-- save new species before submit
                            let result =
                                await vm.save_before_submit(new_species);
                            if (result) {
                                // add the parent species to the new species object
                                new_species.parent_species =
                                    vm.species_community_original;
                                let payload = new Object();
                                Object.assign(payload, new_species);
                                let submit_url = helpers.add_endpoint_json(
                                    api_endpoints.species,
                                    new_species.id + '/split_new_species_submit'
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
                                        //-- to change status of original species only after all new split species are submitted
                                        if (
                                            index ==
                                            vm.new_species_list.length - 1
                                        ) {
                                            vm.submit_original_species();
                                        }
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
                                    }
                                );
                            }
                        }
                    } else {
                        vm.submitSpeciesSplit = false;
                    }
                },
                () => {
                    vm.submitSpeciesSplit = false;
                }
            );
        },
        submit_original_species: function () {
            let vm = this;
            let payload = new Object();
            Object.assign(payload, vm.species_community_original);
            let submit_url = helpers.add_endpoint_json(
                api_endpoints.species,
                vm.species_community_original.id + '/change_status_historical'
            );
            fetch(submit_url, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(payload),
            }).then(
                async (response) => {
                    vm.species_community_original = await response.json();
                    vm.$router.push({
                        name: 'internal-species-communities-dash',
                    });
                },
                (err) => {
                    swal.fire({
                        title: 'Submit Error',
                        text: helpers.apiVueResourceError(err),
                        icon: 'error',
                        customClass: {
                            confirmButton: 'btn btn-primary',
                        },
                    });
                }
            );
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
        addSpecies: function () {
            let vm = this;
            swal.fire({
                title: 'Add Another Species',
                text: 'Are you sure you want to add another species to the split?',
                icon: 'question',
                showCancelButton: true,
                confirmButtonText: 'Add Another Species',
                reverseButtons: true,
                customClass: {
                    confirmButton: 'btn btn-primary',
                    cancelButton: 'btn btn-secondary',
                },
            }).then(async (swalresult) => {
                if (swalresult.isConfirmed) {
                    let newSpeciesId = null;
                    try {
                        const createUrl = api_endpoints.species + '/';
                        let payload = new Object();
                        payload.group_type_id =
                            vm.species_community_original.group_type_id;
                        payload.parent_species_id =
                            vm.species_community_original.id;
                        fetch(createUrl, {
                            method: 'POST',
                            headers: {
                                'Content-Type': 'application/json',
                            },
                            body: JSON.stringify(payload),
                        }).then(
                            async (response) => {
                                const data = await response.json();
                                newSpeciesId = data.id;
                                fetch(
                                    `/api/species/${newSpeciesId}/internal_species.json`
                                ).then(
                                    async (response) => {
                                        const data = await response.json();
                                        let species_obj = data.species_obj;
                                        //---documents array added to store the select document ids in from the child component
                                        species_obj.documents = [];
                                        //---threats array added to store the select threat ids in from the child component
                                        species_obj.threats = [];
                                        vm.new_species_list.push(species_obj); //--temp species_obj
                                    },
                                    (err) => {
                                        console.log(err);
                                    }
                                );
                            },
                            (error) => {
                                console.log(error);
                            }
                        );
                    } catch (err) {
                        console.log(err);
                        if (this.is_internal) {
                            return err;
                        }
                    }
                }
            });
        },
        eventListeners: function () {
            let vm = this;
            $('#splitSpecies .nav-pills').on('click', 'span', function () {
                let species_obj = vm.new_species_list[$(this).attr('id')];
                swal.fire({
                    title: 'Remove Species',
                    text: `Are you sure you want to remove species ${species_obj.species_number} from the split?`,
                    icon: 'question',
                    showCancelButton: true,
                    confirmButtonText: 'Remove Species',
                    reverseButtons: true,
                    customClass: {
                        confirmButton: 'btn btn-primary',
                        cancelButton: 'btn btn-secondary',
                    },
                }).then(async (swalresult) => {
                    if (swalresult.isConfirmed) {
                        vm.removeSpecies(species_obj.id);
                        vm.new_species_list.splice($(this).attr('id'), 1);
                    }
                });
            });
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
