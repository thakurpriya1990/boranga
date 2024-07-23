<template lang="html">
    <div id="splitSpecies">
        <modal transition="modal fade" @ok="ok()" @cancel="cancel()" :title="title" large id="myModal">
            <div class="container-fluid">
                <div class="row">
                    <form class="form-horizontal" name="splitSpeciesForm">
                        <alert :show.sync="showError" type="danger"><strong>{{ errorString }}</strong></alert>
                        <div>
                            <div class="col-md-12">
                                <ul v-if="is_internal" class="nav nav-pills mb-3" id="split-pills-tab" role="tablist">
                                    <li class="nav-item">
                                        <a class="nav-link" id="pills-original-tab" data-bs-toggle="pill"
                                            :href="'#' + originalBody" role="tab" :aria-controls="originalBody"
                                            aria-selected="true">
                                            Original {{
                                                this.species_community_original ? this.species_community_original.species_number:''
                                            }}
                                        </a>
                                    </li>

                                    <li class="nav-item" v-for="(species, index) in new_species_list"
                                        :key="'li' + species.id">
                                        <a class="nav-link" :id="'pills-species-' + index + '-tab'"
                                            data-bs-toggle="pill" :href="'#species-body-' + index" role="tab"
                                            :aria-controls="'species-body-' + index" aria-selected="false">
                                            {{ species.species_number }}
                                        </a><span :id=index>x</span>
                                    </li>
                                    <li>
                                        <a href="#" id="btnAdd"><i class="icon-plus-sign-alt"></i>Add</a>
                                    </li>
                                </ul>
                                <div class="tab-content" id="split-pills-tabContent">
                                    <!-- the fade show active was creating the problem of rendering two thing on tab -->
                                    <div class="tab-pane" :id="originalBody" role="tabpanel"
                                        aria-labelledby="pills-original-tab">
                                        <SpeciesCommunitiesComponent v-if="species_community_original != null"
                                            ref="species_communities_original"
                                            :species_community.sync="species_community_original" id="species_original"
                                            :is_internal="true" :is_readonly="true">
                                            <!-- this prop is only send from split species form to make the original species readonly -->
                                        </SpeciesCommunitiesComponent>
                                    </div>
                                    <div v-for="(species, index) in new_species_list" :key="'div' + species.id"
                                        class="tab-pane fade" :id="'species-body-' + index" role="tabpanel"
                                        :aria-labelledby="'pills-species-' + index + '-tab'">
                                        <SpeciesSplitForm :ref="'species_communities_species' + index"
                                            :species_community.sync="species"
                                            :species_original="species_community_original" :id="'species-' + index"
                                            :is_internal="true">
                                        </SpeciesSplitForm>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </form>
                </div>
            </div>
            <div slot="footer">
                <button type="button" class="btn btn-secondary me-2" @click="cancel">Cancel</button>
                <button v-if="submitSpeciesSplit" class="btn btn-primary pull-right" style="margin-top:5px;"
                    disabled>Submit&nbsp;<i class="fa fa-circle-o-notch fa-spin fa-fw"></i></button>
                <button v-else class="btn btn-primary" @click.prevent="ok()"
                    :disabled="submitSpeciesSplit">Submit</button>
            </div>
        </modal>
    </div>
</template>

<script>
import Vue from 'vue'
import modal from '@vue-utils/bootstrap-modal.vue'
import alert from '@vue-utils/alert.vue'
import FileField2 from '@/components/forms/filefield.vue'
import SpeciesCommunitiesComponent from '@/components/form_species_communities.vue'
import SpeciesSplitForm from '@/components/form_species_split.vue'
import { helpers, api_endpoints } from "@/utils/hooks.js"
export default {
    name: 'SpeciesSplit',
    components: {
        modal,
        alert,
        FileField2,
        SpeciesCommunitiesComponent,
        SpeciesSplitForm,
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
            originalBody: 'originalBody' + vm._uid,
            species2Body: 'species2Body' + vm._uid,
            species_community_original: null,
            submitSpeciesSplit: false,
            isModalOpen: false,
            new_species_list: [],
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
            return this.species_community_original != null ? 'Split Species ' + this.species_community_original.species_number : 'Split Species';
        },
        species_split_form_url: function () {
            var vm = this;
            return `/api/species/${vm.species_community_original.id}/species_split_save.json`;
        },
    },
    methods: {
        tabClicked: function () {
        },
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
            if (vm.new_species_list.length > 0) {
                for (var index = 0; index < vm.new_species_list.length; index++) {
                    vm.removeSpecies((vm.new_species_list[index]).id);
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
                    },                });
                vm.submitSpeciesSplit = false;
                vm.saveError = true;
                return false;
            });
            return result;
        },
        can_submit: function () {
            let vm = this;
            let blank_fields = []
            for (let index = 0; index < vm.new_species_list.length; index++) {
                if (vm.new_species_list[index].taxonomy_id == null || vm.new_species_list[index].taxonomy_id == '') {
                    blank_fields.push('Species ' + vm.new_species_list[index].species_number + ' Scientific Name is missing')
                }
                if (vm.new_species_list[index].distribution.distribution == null || vm.new_species_list[index].distribution.distribution == '') {
                    blank_fields.push('Distribution is missing')
                }
                if (vm.new_species_list[index].regions == null || vm.new_species_list[index].regions == '' || vm.new_species_list[index].regions.length==0) {
                    blank_fields.push('Region is missing')
                }
                if (vm.new_species_list[index].districts == null || vm.new_species_list[index].districts == ''|| vm.new_species_list[index].districts.length == 0) {
                    blank_fields.push('District is missing')
                }
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
                    },                })
                return false;
            }

            vm.submitSpeciesSplit = true;
            swal.fire({
                title: "Submit",
                text: "Are you sure you want to submit this Species Spit?",
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
                    for (let index = 0; index < vm.new_species_list.length; index++) {
                        let new_species = vm.new_species_list[index]
                        //-- save new species before submit
                        let result = await vm.save_before_submit(new_species);
                        if (result) {
                            // add the parent species to the new species object
                            new_species.parent_species = [vm.species_community_original];
                            let payload = new Object();
                            Object.assign(payload, new_species);
                            let submit_url = helpers.add_endpoint_json(api_endpoints.species, new_species.id + '/split_new_species_submit')
                            vm.$http.post(submit_url, payload).then(res => {
                                vm.new_species = res.body;
                                //-- to change status of original species only after all new split species are submitted
                                if (index == vm.new_species_list.length - 1) {
                                    vm.submit_original_species();
                                }
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
                } else {
                    vm.submitSpeciesSplit = false;
                }
            }, (error) => {
                vm.submitSpeciesSplit = false;
            });
        },
        submit_original_species: function () {
            let vm = this;
            let payload = new Object();
            Object.assign(payload, vm.species_community_original);
            let submit_url = helpers.add_endpoint_json(api_endpoints.species, vm.species_community_original.id + '/change_status_historical')
            vm.$http.post(submit_url, payload).then(res => {
                vm.species_community_original = res.body;
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
                    },                });
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
        eventListeners: function () {
            let vm = this;
            $(".nav-pills").on("click", "span", function () {
                let species_obj = vm.new_species_list[$(this).attr('id')];
                vm.removeSpecies(species_obj.id);
                vm.new_species_list.splice($(this).attr('id'), 1);
            });

            $('#btnAdd').click(function (e) {
                let newSpeciesId = null
                try {
                    const createUrl = api_endpoints.species + "/";
                    let payload = new Object();
                    payload.group_type_id = vm.species_community_original.group_type_id;
                    payload.parent_species_id = vm.species_community_original.id;
                    Vue.http.post(createUrl, payload).then(resp => {
                        newSpeciesId = resp.body.id;
                        Vue.http.get(`/api/species/${newSpeciesId}/internal_species.json`).then(res => {
                            let species_obj = res.body.species_obj;
                            //---documents array added to store the select document ids in from the child component
                            species_obj.documents = []
                            //---threats array added to store the select threat ids in from the child component
                            species_obj.threats = []
                            vm.new_species_list.push(species_obj); //--temp species_obj
                        },
                            err => {
                                console.log(err);
                            });
                    }, (error) => {
                        console.log(error);
                    });
                }
                catch (err) {
                    console.log(err);
                    if (this.is_internal) {
                        return err;
                    }
                }
            });

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
        //  to show the the added species active i.e the last Tab
        var lastTabEl = document.querySelector('#split-pills-tab li:nth-last-child(2) a')
        var lastTab = new bootstrap.Tab(lastTabEl)
        lastTab.show();
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
