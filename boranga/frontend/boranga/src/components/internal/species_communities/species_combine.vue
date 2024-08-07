<template lang="html">
    <div id="combineSpecies">
        <modal transition="modal fade" @ok="ok()" @cancel="cancel()" :title="title" extraLarge id="myModal">
            <div class="container-fluid">
                <div class="row">
                    <form class="form-horizontal" name="combineSpeciesForm">
                        <alert :show.sync="showError" type="danger"><strong>{{ errorString }}</strong></alert>
                        <div>
                            <div class="col-md-12">
                                <ul v-if="is_internal" class="nav nav-pills" id="combine-pills-tab" role="tablist">
                                    <li class="nav-item">
                                        <a class="nav-link" id="pills-new-species-tab" data-bs-toggle="pill"
                                            :href="'#' + newSpeciesBody" role="tab" :aria-controls="newSpeciesBody"
                                            aria-selected="true">
                                            New Species {{
                                                this.new_combine_species ? this.new_combine_species.species_number : '' }}
                                        </a>
                                    </li>
                                    <li class="nav-item" v-for="(species, index) in original_species_combine_list"
                                        :key="'li' + species.id">
                                        <a class="nav-link" :id="'pills-species-' + index + '-tab'"
                                            data-bs-toggle="pill" :href="'#species-body-' + index" role="tab"
                                            :aria-controls="'species-body-' + index" aria-selected="false">
                                            {{ species.species_number }}<span v-if="index > 0" class="ms-2"
                                                @click="removeCombineSpecies(species)" :id=index><i
                                                    class="bi bi-trash3-fill"></i></span>
                                            <!-- can delete the original species except the current original species , so check index>0 -->
                                        </a>
                                    </li>
                                    <li class="nav-item">
                                        <a class="nav-link" href="#" id="combineSpeciesBtnAdd"
                                            @click.prevent="addSpeciesToCombine()"><i class="bi bi-window-plus"></i> Add
                                            Another Species</a>
                                    </li>
                                    <li class="nav-item">
                                        <a class="nav-link" id="finalise-combine" data-bs-toggle="pill"
                                            href="#finalise-combine-tab-pane" role="tab"
                                            aria-controls="finalise-combine-tab-pane" aria-selected="false"><i
                                                class="bi bi-check2-circle"></i>
                                            Finalise Combine</a>
                                    </li>
                                </ul>
                                <div class="tab-content border p-3" id="combine-pills-tabContent">
                                    <div class="tab-pane" :id="newSpeciesBody" role="tabpanel"
                                        aria-labelledby="pills-new-species-tab">
                                        <SpeciesCombineForm v-if="new_combine_species && new_combine_species.id"
                                            ref="species_communities_new" :species_community.sync="new_combine_species"
                                            :original_species_combine_list="original_species_combine_list"
                                            id="new_combine_species" :is_internal="true">
                                        </SpeciesCombineForm>
                                    </div>
                                    <div v-for="(species, index) in original_species_combine_list"
                                        :key="'div' + species.id" class="tab-pane fade" :id="'species-body-' + index"
                                        role="tabpanel" :aria-labelledby="'pills-species' + index + '-tab'">
                                        <SpeciesCommunitiesComponent :ref="'species_communities_species' + index"
                                            :species_community_original="species" :species_community.sync="species"
                                            :id="'species-' + index" :is_internal="true" :is_readonly="true">
                                        </SpeciesCommunitiesComponent>
                                    </div>
                                    <div v-if="new_combine_species && original_species_combine_list && original_species_combine_list.length > 0"
                                        class="tab-pane" id="finalise-combine-tab-pane" role="tabpanel"
                                        aria-labelledby="finalise-combine">
                                        <p class="border-bottom mb-3 pb-3">Add in some help text for users here</p>

                                        <p>
                                            You are about to combine the following species:
                                        </p>

                                        <div class="mb-3">
                                            <li v-for="(species, index) in original_species_combine_list"
                                            :key="species.id" class="text-secondary mb-3">
                                            <span
                                                class="badge bg-light text-primary text-capitalize border p-2 fs-6 me-2">{{
                                                    species.species_number }} - {{ species.taxonomy_details.scientific_name
                                                }}</span>
                                                </li>
                                        </div>

                                        <p>
                                            Into the new species:
                                        </p>

                                        <div class="border-bottom mb-3 pb-3">
                                            <span class="badge bg-light text-primary text-capitalize border p-2 fs-6">{{
                                                new_combine_species.species_number }} <template
                                                    v-if="new_combine_species.taxonomy_details && new_combine_species.taxonomy_details.scientific_name">- {{
                                                        new_combine_species.taxonomy_details.scientific_name }}</template></span>
                                        </div>

                                        <button class="button btn btn-primary" @click.prevent="ok()"
                                            :disabled="finalise_combine_loading"><i class="bi bi-check2-circle"></i>
                                            Finalise
                                            Combine <template v-if="finalise_combine_loading"><span
                                                    class="spinner-border spinner-border-sm" role="status"
                                                    aria-hidden="true"></span>
                                                <span class="visually-hidden">Loading...</span></template></button>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </form>
                </div>
            </div>

            <div slot="footer">
                <button type="button" class="btn btn-secondary me-2" @click="cancel">Cancel</button>
            </div>
        </modal>

        <AddCombineSpecies ref="addCombineSpecies"></AddCombineSpecies>
    </div>
</template>

<script>
import modal from '@vue-utils/bootstrap-modal.vue'
import alert from '@vue-utils/alert.vue'
import FileField2 from '@/components/forms/filefield.vue'
import SpeciesCommunitiesComponent from '@/components/form_species_communities.vue'
import SpeciesCombineForm from '@/components/form_species_combine.vue'
import AddCombineSpecies from '@/components/common/species_communities/species_combine/add_combine_species.vue'
import { helpers, api_endpoints } from "@/utils/hooks.js"

export default {
    name: 'SpeciesCombine',
    components: {
        modal,
        alert,
        FileField2,
        SpeciesCommunitiesComponent,
        SpeciesCombineForm,
        AddCombineSpecies,
    },
    props: {
        species_community: {
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
            new_combine_species: null,
            new_combine_species_display: '',
            submitSpeciesCombine: false,
            isModalOpen: false,
            original_species_combine_list: [],
            finalise_combine_loading: false,
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
            //return this.processing_status == 'With Approver' ? 'Approve Conservation Status' : 'Propose to approve Conservation Status';
            return this.new_combine_species != null ? 'Combine Species ' : 'Combine Species';
        },
        species_split_form_url: function () {
            var vm = this;
            return `/api/species/${vm.new_combine_species.id}/species_split_save.json`;
        },
        combine_into_species_scientific_name: function () {
            return this.new_combine_species.scientific_name ? vm.new_combine_species.scientific_name : '';
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
            vm.removeSpecies(vm.new_combine_species.id);
            vm.original_species_combine_list = [];
            this.isModalOpen = false;
            this.errors = false;
        },
        save_before_submit: async function (new_species) {
            let vm = this;
            vm.saveError = false;

            let payload = new Object();
            Object.assign(payload, new_species);
            const result = await vm.$http.post(`/api/species/${new_species.id}/species_split_save.json`, payload).then(res => {
                return true;
            }, err => {
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
            });
            return result;
        },
        can_submit: function () {
            let vm = this;
            let blank_fields = []
            if (vm.new_combine_species.taxonomy_id == null || vm.new_combine_species.taxonomy_id == '') {
                blank_fields.push(' Species ' + vm.new_combine_species.species_number + ' Scientific Name is missing')
            }
            if (vm.new_combine_species.distribution.distribution == null || vm.new_combine_species.distribution.distribution == '') {
                blank_fields.push(' Distribution is missing')
            }
            if (vm.new_combine_species.regions == null || vm.new_combine_species.regions == '' || vm.new_combine_species.regions.length == 0) {
                blank_fields.push(' Region is missing')
            }
            if (vm.new_combine_species.districts == null || vm.new_combine_species.districts == '' || vm.new_combine_species.districts.length == 0) {
                blank_fields.push(' District is missing')
            }
            if (blank_fields.length == 0) {
                return true;
            }
            else {
                return blank_fields;
            }
        },
        sendData: async function () {
            let vm = this;
            var missing_data = vm.can_submit();
            if (missing_data != true) {
                await swal.fire({
                    title: "Please fix following errors before submitting",
                    text: missing_data,
                    icon: 'error',
                    customClass: {
                        confirmButton: 'btn btn-primary',
                    },
                })
                // was added to set the first species Tab active but the updated() method overrides it
                var firstTabEl = document.querySelector('#combine-pills-tab li:nth-child(1) a')
                var firstTab = bootstrap.Tab.getOrCreateInstance(firstTabEl)
                firstTab.show()
                return false;
            }

            vm.submitSpeciesCombine = true;
            swal.fire({
                title: "Combine Species",
                text: "Are you sure you want to combine those species?",
                icon: "question",
                showCancelButton: true,
                confirmButtonText: "Combine Species",
                customClass: {
                    confirmButton: 'btn btn-primary',
                    cancelButton: 'btn btn-secondary',
                },
                reverseButtons: true,
            }).then(async (swalresult) => {
                if (swalresult.isConfirmed) {
                    //---save and submit the new combine species
                    let new_species = vm.new_combine_species;
                    //-- save new species before submit
                    let result = await vm.save_before_submit(new_species);
                    if (!vm.saveError) {
                        vm.finalise_combine_loading = true;

                        // add the parent species array to the new species object
                        new_species.parent_species = vm.original_species_combine_list;
                        let payload = new Object();
                        Object.assign(payload, new_species);
                        let submit_url = helpers.add_endpoint_json(api_endpoints.species, new_species.id + '/combine_new_species_submit')
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
                                },
                            });
                            vm.saveError = true;
                        });
                    }
                }
            }, (error) => {
                vm.submitSpeciesCombine = false;
            });

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
        removeCombineSpecies: function (species) {
            let vm = this;
            swal.fire({
                title: "Remove Species",
                text: `Are you sure you want to remove species ${species.species_number} from this combine?`,
                icon: "question",
                showCancelButton: true,
                confirmButtonText: "Remove Species",
                customClass: {
                    confirmButton: 'btn btn-primary',
                    cancelButton: 'btn btn-secondary',
                },
                reverseButtons: true,
            }).then(async (swalresult) => {
                if (swalresult.isConfirmed) {
                    let species_index = vm.original_species_combine_list.indexOf(species);

                    // Show the closest species combine tab before removing the current one
                    var firstTabEl = document.querySelector('#combine-pills-tab li:nth-child(1) a')
                    var firstTab = new bootstrap.Tab(firstTabEl)

                    firstTab.show()
                    vm.original_species_combine_list.splice(species_index, 1);
                }
            });
        },
        addSpeciesToCombine: function () {
            this.$refs.addCombineSpecies.isModalOpen = true;
        },
    },
    mounted: function () {
        let vm = this;
        vm.form = document.forms.combineSpeciesForm;
        this.$nextTick(() => {
            // was added to set the first species Tab active but the updated() method overrides it
            var firstTabEl = document.querySelector('#combine-pills-tab li:nth-child(1) a')
            var firstTab = new bootstrap.Tab(firstTabEl)
            firstTab.show()
        });
    },
    updated: function () {
        if (!this.finalise_combine_loading) {
            //  to show the the added species active i.e the last Tab
            var mostRecentlyAddedSpeciesTabElement = document.querySelector('#combine-pills-tab li:nth-last-child(3) a')
            var mostRecentlyAddedSpeciesTab = new bootstrap.Tab(mostRecentlyAddedSpeciesTabElement)
            mostRecentlyAddedSpeciesTab.show()
        }
    },
}
</script>

<style scoped>
.bi.bi-trash3-fill:hover {
    cursor: pointer;
    color: red;
}
</style>
