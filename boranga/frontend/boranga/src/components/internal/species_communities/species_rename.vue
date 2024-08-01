<template lang="html">
    <div id="renameSpecies">
        <modal transition="modal fade" @ok="ok()" @cancel="cancel()" :title="title" large id="myModal">
            <div class="container-fluid">
                <div class="row">
                    <form class="form-horizontal" name="renameSpeciesForm">
                        <alert :show.sync="showError" type="danger"><strong>{{ errorString }}</strong></alert>
                        <div>
                            <div class="col-md-12">
                                <SpeciesCommunitiesComponent v-if="new_rename_species != null" ref="rename_species"
                                    :species_community_original="new_rename_species"
                                    :species_community.sync="new_rename_species" id="rename_species" :is_internal="true"
                                    :is_readonly="true" :rename_species="true"> // rename=true used to make only taxon
                                    select editable on form
                                </SpeciesCommunitiesComponent>
                            </div>
                        </div>
                    </form>
                </div>
            </div>
            <div slot="footer">
                <button type="button" class="btn btn-secondary me-2" @click="cancel">Cancel</button>
                <button v-if="submitSpeciesRename" class="btn btn-primary pull-right" style="margin-top:5px;"
                    disabled>Submit <span class="spinner-border spinner-border-sm" role="status" aria-hidden="true"></span>
                    <span class="visually-hidden">Loading...</span></button>
                <button v-else class="btn btn-primary" @click.prevent="ok()"
                    :disabled="submitSpeciesRename">Rename Species</button>
            </div>
        </modal>
    </div>
</template>

<script>
import modal from '@vue-utils/bootstrap-modal.vue'
import alert from '@vue-utils/alert.vue'
import FileField2 from '@/components/forms/filefield.vue'
import SpeciesCommunitiesComponent from '@/components/form_species_communities.vue'
import { helpers, api_endpoints } from "@/utils/hooks.js"
export default {
    name: 'SpeciesRename',
    components: {
        modal,
        alert,
        FileField2,
        SpeciesCommunitiesComponent,
    },
    props: {
        species_community_original: {
            type: Object,
            required: true
        },
        is_internal: {
            type: Boolean,
            required: true
        },
    },
    data: function () {
        let vm = this;
        return {
            newSpeciesBody: 'newSpeciesBody' + vm._uid,
            speciesBody: 'speciesBody' + vm._uid,
            new_rename_species: null,
            submitSpeciesRename: false,
            isModalOpen: false,
            form: null,
            errors: false,
            errorString: '',
        }
    },
    computed: {
        csrf_token: function () {
            return helpers.getCookie('csrftoken')
        },
        showError: function () {
            var vm = this;
            return vm.errors;
        },
        title: function () {
            return this.new_rename_species != null ? 'Rename Species ' + this.species_community_original.species_number + ' to ' + this.new_rename_species.species_number : '';
        },
    },
    methods: {
        ok: function () {
            let vm = this;
            if ($(vm.form).valid()) {
                vm.sendData();
            }
        },
        cancel: function () {
            this.close()
        },
        close: function () {
            let vm = this;
            vm.removeSpecies(vm.new_rename_species.id);
            this.isModalOpen = false;
            this.errors = false;
        },
        removeSpecies: function (species_id) {
            let vm = this;
            try {
                // In this case we are allowing a http DELETE call to remove the species
                vm.$http.delete(api_endpoints.remove_species_proposal(species_id));
            }
            catch (err) {
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
            const result = await vm.$http.post(`/api/species/${new_species.id}/species_save.json`, payload).then(res => {
                return true;
            }, err => {
                var errorText = helpers.apiVueResourceError(err);
                swal.fire({
                    title: 'Submit Error',
                    text: errorText,
                    icon: 'error',
                    customClass: {
                        confirmButton: 'btn btn-primary',
                    },                });
                vm.submitSpeciesRename = false;
                vm.saveError = true;
                return false;
            });
            return result;
        },
        sendData: async function () {
            let vm = this;
            if (vm.new_rename_species.taxonomy_id && vm.new_rename_species.taxonomy_id == vm.species_community_original.taxonomy_id) {
                swal.fire({
                    title: "Please fix following errors",
                    text: "Species To Rename already exists",
                    icon: 'error',
                    customClass: {
                        confirmButton: 'btn btn-primary',
                    },                })
            }
            else {
                vm.submitSpeciesRename = true;
                swal.fire({
                    title: "Submit",
                    text: "Are you sure you want to submit this Species Rename?",
                    icon: "question",
                    showCancelButton: true,
                    confirmButtonText: "submit",
                    customClass: {
                        confirmButton: 'btn btn-primary',
                        cancelButton: 'btn btn-secondary',
                    },
                    reverseButtons: true,
                }).then(async (swalresult) => {
                    if (swalresult.isConfirmed) {
                        //---save and submit the new rename species
                        let new_species = vm.new_rename_species;
                        //-- save new species before submit
                        let result = await vm.save_before_submit(new_species);
                        if (!vm.saveError) {
                            // add the parent species to the new species object
                            new_species.parent_species = [vm.species_community_original];
                            let payload = new Object();
                            Object.assign(payload, new_species);
                            let submit_url = helpers.add_endpoint_json(api_endpoints.species, new_species.id + '/rename_new_species_submit')
                            vm.$http.post(submit_url, payload).then(res => {
                                vm.new_species = res.body;
                                vm.$router.push({
                                    name: 'internal-species-communities-dash'
                                });
                            }, err => {
                                swal.fire({
                                    title: 'Submit Error',
                                    text: helpers.apiVueResourceError(err),
                                    icon: 'error',
                                    customClass: {
                        confirmButton: 'btn btn-primary',
                    },                                });
                                vm.saveError = true;
                            });
                        }
                    }

                }, (error) => {
                    vm.submitSpeciesRename = false;
                });
            }
        },
    },
    mounted: function () {
        let vm = this;
        vm.form = document.forms.renameSpeciesForm;
    },
}
</script>
