<template lang="html">
    <div id="renameSpecies">
        <modal
            id="species-rename-modal"
            transition="modal fade"
            :title="title"
            extra-large
            @ok="ok()"
            @cancel="cancel()"
        >
            <div class="container-fluid">
                <div class="row">
                    <form class="form-horizontal" name="renameSpeciesForm">
                        <alert v-if="errorString" type="danger"
                            ><strong>{{ errorString }}</strong></alert
                        >
                        <div>
                            <div class="col-md-12">
                                <SpeciesCommunitiesComponent
                                    v-if="new_rename_species != null"
                                    id="rename_species"
                                    ref="rename_species"
                                    :species_community_original="
                                        new_rename_species
                                    "
                                    :species_community="new_rename_species"
                                    :is_internal="true"
                                    :is_readonly="true"
                                    :rename_species="true"
                                >
                                    // rename=true used to make only taxon
                                    select editable on form
                                </SpeciesCommunitiesComponent>
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
                    <button
                        v-if="submitSpeciesRename"
                        class="btn btn-primary pull-right"
                        style="margin-top: 5px"
                        disabled
                    >
                        Submit
                        <span
                            class="spinner-border spinner-border-sm"
                            role="status"
                            aria-hidden="true"
                        ></span>
                        <span class="visually-hidden">Loading...</span>
                    </button>
                    <button
                        v-else
                        class="btn btn-primary"
                        :disabled="submitSpeciesRename"
                        @click.prevent="ok()"
                    >
                        Rename Species
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
import { helpers, api_endpoints } from '@/utils/hooks.js';
export default {
    name: 'SpeciesRename',
    components: {
        modal,
        alert,
        SpeciesCommunitiesComponent,
    },
    props: {
        species_community_original: {
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
            new_rename_species: null,
            submitSpeciesRename: false,
            isModalOpen: false,
            form: null,
            errorString: '',
        };
    },
    computed: {
        csrf_token: function () {
            return helpers.getCookie('csrftoken');
        },
        title: function () {
            return this.new_rename_species != null
                ? 'Rename Species ' +
                      this.species_community_original.species_number +
                      ' to ' +
                      this.new_rename_species.species_number
                : '';
        },
    },
    mounted: function () {
        let vm = this;
        vm.form = document.forms.renameSpeciesForm;
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
            vm.removeSpecies(vm.new_rename_species.id);
            this.isModalOpen = false;
            this.errorString = '';
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
        save_before_submit: async function (new_species) {
            let vm = this;
            vm.saveError = false;
            let payload = new Object();
            Object.assign(payload, new_species);
            const result = await fetch(
                `/api/species/${new_species.id}/species_save.json`,
                {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify(payload),
                }
            )
                .then(async (response) => {
                    const data = await response.json();
                    if (!response.ok) {
                        swal.fire({
                            title: 'Submit Error',
                            text: JSON.stringify(data),
                            icon: 'error',
                            customClass: {
                                confirmButton: 'btn btn-primary',
                            },
                        });
                        return;
                    }
                    return true;
                })
                .finally(() => {
                    vm.submitSpeciesRename = false;
                });
            return result;
        },
        sendData: async function () {
            let vm = this;
            if (!vm.new_rename_species.taxonomy_id) {
                swal.fire({
                    title: 'Please fix following errors',
                    text: 'Please select a species by searching for the scientific name',
                    icon: 'error',
                    customClass: {
                        confirmButton: 'btn btn-primary',
                    },
                });
                return false;
            }

            if (
                vm.new_rename_species.taxonomy_id &&
                vm.new_rename_species.taxonomy_id ==
                    vm.species_community_original.taxonomy_id
            ) {
                swal.fire({
                    title: 'Please fix following errors',
                    text: 'Species To Rename already exists',
                    icon: 'error',
                    customClass: {
                        confirmButton: 'btn btn-primary',
                    },
                });
            } else {
                vm.submitSpeciesRename = true;
                swal.fire({
                    title: 'Rename Species',
                    text: 'Are you sure you want to rename this species?',
                    icon: 'question',
                    showCancelButton: true,
                    confirmButtonText: 'Rename Species',
                    customClass: {
                        confirmButton: 'btn btn-primary',
                        cancelButton: 'btn btn-secondary',
                    },
                    reverseButtons: true,
                })
                    .then(async (swalresult) => {
                        if (swalresult.isConfirmed) {
                            //---save and submit the new rename species
                            let new_species = vm.new_rename_species;
                            //-- save new species before submit
                            await vm.save_before_submit(new_species);
                            if (!vm.saveError) {
                                // add the parent species to the new species object
                                new_species.parent_species =
                                    vm.species_community_original;
                                let payload = new Object();
                                Object.assign(payload, new_species);
                                let submit_url = helpers.add_endpoint_json(
                                    api_endpoints.species,
                                    new_species.id +
                                        '/rename_new_species_submit'
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
                                    }
                                );
                            }
                        }
                    })
                    .finally(() => {
                        vm.submitSpeciesRename = false;
                    });
            }
        },
    },
};
</script>
