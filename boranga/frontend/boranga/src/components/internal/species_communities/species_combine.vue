<template lang="html">
    <div id="combineSpecies">
        <modal transition="modal fade" @ok="ok()" @cancel="cancel()" :title="title" large id="myModal">
            <div class="container-fluid">
                <div class="row">
                    <form class="form-horizontal" name="combineSpeciesForm">
                        <alert :show.sync="showError" type="danger"><strong>{{ errorString }}</strong></alert>
                        <div>
                            <div class="col-md-12">
                                <ul v-if="is_internal" class="nav nav-pills mb-3" id="combine-pills-tab" role="tablist">
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
                                            {{ species.species_number }}
                                            <!-- can delete the original species except the current original species , so check index>0 -->
                                        </a><span v-show="index > 0" :id="'removeCombineSpecies' + species"
                                            @click="removeCombineSpecies(species)">x</span>
                                    </li>
                                    <li>
                                        <a href="#" id="combineSpeciesBtnAdd" @click="addSpeciesToCombine()"><i
                                                class="icon-plus-sign-alt"></i>Add</a>
                                    </li>
                                </ul>
                                <div class="tab-content" id="combine-pills-tabContent">
                                    <div class="tab-pane" :id="newSpeciesBody" role="tabpanel"
                                        aria-labelledby="pills-new-species-tab">
                                        <SpeciesCombineForm v-if="new_combine_species != null"
                                            ref="species_communities_new" :species_community.sync="new_combine_species"
                                            :original_species_combine_list="original_species_combine_list"
                                            id="new_combine_species" :is_internal="true">
                                        </SpeciesCombineForm>
                                    </div>
                                    <div v-for="(species, index) in original_species_combine_list"
                                        :key="'div' + species.id" class="tab-pane fade" :id="'species-body-' + index"
                                        role="tabpanel" :aria-labelledby="'pills-species' + index + '-tab'">
                                        <SpeciesCommunitiesComponent :ref="'species_communities_species' + index"
                                            :species_community.sync="species" :id="'species-' + index"
                                            :is_internal="true" :is_readonly="true">
                                        </SpeciesCommunitiesComponent>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </form>
                </div>
            </div>

            <div slot="footer">
                <button type="button" class="btn btn-secondary me-2" @click="cancel">Cancel</button>
                <button v-if="submitSpeciesCombine" class="btn btn-primary pull-right" style="margin-top:5px;"
                    disabled>Submit&nbsp;<i class="fa fa-circle-o-notch fa-spin fa-fw"></i></button>
                <button v-else class="btn btn-primary" @click.prevent="ok()" :disabled="submitSpeciesCombine">Combine
                    Species</button>
            </div>
        </modal>

        <AddCombineSpecies ref="addCombineSpecies"></AddCombineSpecies>
    </div>
</template>

<script>
import modal from '@vue-utils/bootstrap-modal.vue'
import alert from '@vue-utils/alert.vue'
import FileField2 from '@/components/forms/filefield2.vue'
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
            submitSpeciesCombine: false,
            isModalOpen: false,
            original_species_combine_list: [],
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
                blank_fields.push('Species ' + vm.new_combine_species.species_number + ' Scientific Name is missing')
            }
            if (vm.new_combine_species.distribution.distribution == null || vm.new_combine_species.distribution.distribution == '') {
                blank_fields.push('Distribution is missing')
            }
            if (vm.new_combine_species.regions == null || vm.new_combine_species.regions == '' || vm.new_combine_species.regions.length==0) {
                blank_fields.push('Region is missing')
            }
            if (vm.new_combine_species.districts == null || vm.new_combine_species.districts == '' || vm.new_combine_species.districts.length==0) {
                blank_fields.push('District is missing')
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
                swal.fire({
                    title: "Please fix following errors before submitting",
                    text: missing_data,
                    icon: 'error',
                    customClass: {
                        confirmButton: 'btn btn-primary',
                    },
                })
                return false;
            }

            vm.submitSpeciesCombine = true;
            swal.fire({
                title: "Submit",
                text: "Are you sure you want to submit this Species Combine?",
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
                    //---save and submit the new combine species
                    let new_species = vm.new_combine_species;
                    //-- save new species before submit
                    let result = await vm.save_before_submit(new_species);
                    if (!vm.saveError) {
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
            //-- get the index of the tab species
            let species_index = vm.original_species_combine_list.indexOf(species);
            //--- the species from the array of that index
            vm.original_species_combine_list.splice(species_index, 1);
        },
        addSpeciesToCombine: function () {
            this.$refs.addCombineSpecies.isModalOpen = true;
        },
        eventListeners: function () {
            let vm = this;
        },
    },
    mounted: function () {
        let vm = this;
        vm.form = document.forms.combineSpeciesForm;
        this.$nextTick(() => {
            vm.eventListeners();
            // was added to set the first species Tab active but the updated() method overrides it
            var firstTabEl = document.querySelector('#combine-pills-tab li:nth-child(1) a')
            var firstTab = new bootstrap.Tab(firstTabEl)
            firstTab.show()
        });
    },
    created: function () {
        let vm = this;
        this.$nextTick(() => {
        });
    },
    updated: function () {
        //  to show the the added species active i.e the last Tab
        var lastTabEl = document.querySelector('#combine-pills-tab li:nth-last-child(2) a')
        var lastTab = new bootstrap.Tab(lastTabEl)
        lastTab.show()
    },
}
</script>

<style lang="css" scoped>
.section {
    text-transform: capitalize;
}

.list-group {
    margin-bottom: 0;
}

.fixed-top {
    position: fixed;
    top: 56px;
}

.nav-item {
    margin-bottom: 2px;
}

.nav-item>li>a {
    background-color: yellow !important;
    color: #fff;
}

.nav-item>li.active>a,
.nav-item>li.active>a:hover,
.nav-item>li.active>a:focus {
    color: white;
    background-color: blue;
    border: 1px solid #888888;
}

.admin>div {
    display: inline-block;
    vertical-align: top;
    margin-right: 1em;
}

.nav-pills .nav-link {
    border-bottom-left-radius: 0;
    border-bottom-right-radius: 0;
    border-top-left-radius: 0.5em;
    border-top-right-radius: 0.5em;
    margin-right: 0.25em;
}

.nav-pills .nav-link {
    background: lightgray;
}

.nav-pills .nav-link.active {
    background: gray;
}

.nav-pills>li {
    position: relative;
}

.nav-pills>li>a {
    display: inline-block;
}

.nav-pills>li>span {
    display: none;
    cursor: pointer;
    position: absolute;
    right: 6px;
    top: 8px;
    color: red;
}

.nav-pills>li:hover>span {
    display: inline-block;
}
</style>
