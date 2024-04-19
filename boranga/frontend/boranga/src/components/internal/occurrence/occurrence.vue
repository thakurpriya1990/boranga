<template lang="html">
    <div class="container" id="internal-occurence-detail">
        <div class="row" style="padding-bottom: 50px;">
            <div v-if="occurrence" class="col">
                <h3>Occurrence: {{ occurrence.occurrence_number }} - {{ display_group_type }}</h3>
                <div class="row pb-4">
                <div v-if="!comparing" class="col-md-3">

                    <CommsLogs :comms_url="comms_url" :logs_url="logs_url" :comms_add_url="comms_add_url"
                        :disable_add_entry="false" class="mb-2" />

                    <Submission v-if="canSeeSubmission" :submitter_first_name="submitter_first_name"
                        :submitter_last_name="submitter_last_name" :lodgement_date="occurrence.lodgement_date"
                        class="mb-2" />

                    <div>
                        <div class="card card-default">
                            <div class="card-header">
                                Workflow
                            </div>
                            <div class="card-body card-collapse">
                                <div class="row">
                                    <div class="col-sm-12">
                                        <strong>Status</strong><br />
                                        {{ occurrence.processing_status }}
                                    </div>
                                    <div class="col-sm-12">
                                        <div class="separator"></div>
                                    </div>
                                    <div v-if='!isCommunity' class="col-sm-12 top-buffer-s">
                                        <template v-if="hasUserEditMode">
                                            <div class="row">
                                                <div class="col-sm-12">
                                                    <strong>Action</strong><br />
                                                </div>
                                            </div>
                                            <div class="row">
                                                <div class="col-sm-12">
                                                    <button style="width:80%;" class="btn btn-primary top-buffer-s"
                                                        @click.prevent="splitSpecies()">Split</button><br />
                                                </div>
                                                <div class="col-sm-12">
                                                    <button style="width:80%;" class="btn btn-primary top-buffer-s"
                                                        @click.prevent="combineSpecies()">Combine</button><br />
                                                </div>
                                                <div class="col-sm-12">
                                                    <button style="width:80%;" class="btn btn-primary top-buffer-s"
                                                        @click.prevent="renameSpecies()">Rename</button><br />
                                                </div>
                                            </div>
                                        </template>
                                        <template v-if="canDiscard">
                                            <div class="row">
                                                <div class="col-sm-12">
                                                    <strong>Action</strong><br />
                                                </div>
                                            </div>
                                            <div class="row">
                                                <div class="col-sm-12">
                                                    <button style="width:80%;" class="btn btn-primary top-buffer-s"
                                                        @click.prevent="discardSpeciesProposal()">Discard</button><br />
                                                </div>
                                            </div>
                                        </template>
                                    </div>
                                </div>
                            </div>

                        </div>
                    </div>
                </div>
                <div class="col-md-9">
                    <template>
                        <form :action="occurrence_form_url" method="post" name="occurrence"
                            enctype="multipart/form-data">

                            <ProposalOccurrence v-if="occurrence" :occurrence_obj="occurrence"
                                id="OccurrenceStart" :canEditStatus="false"
                                ref="occurrence" @refreshFromResponse="refreshFromResponse">
                            </ProposalOccurrence>

                            <input type="hidden" name="csrfmiddlewaretoken" :value="csrf_token" />
                            <input type='hidden' name="occurrence_id" :value="1" />
                            <div class="row" style="margin-bottom: 50px">
                                <div class="navbar fixed-bottom" style="background-color: #f5f5f5;">
                                    <div v-if="occurrence.can_user_edit" class="container">
                                        <div class="col-md-12 text-end">
                                            <button v-if="savingOccurrence"
                                                class="btn btn-primary me-2 pull-right"
                                                style="margin-top:5px;" disabled>Save and Continue&nbsp;
                                                <i class="fa fa-circle-o-notch fa-spin fa-fw"></i></button>
                                            <button v-else class="btn btn-primary me-2 ull-right"
                                                style="margin-top:5px;" @click.prevent="save()"
                                                :disabled="saveExitOccurrence || submitOccurrence">Save
                                                and Continue</button>

                                            <button v-if="saveExitOccurrence"
                                                class="btn btn-primary me-2 pull-right"
                                                style="margin-top:5px;" disabled>Save and Exit&nbsp;
                                                <i class="fa fa-circle-o-notch fa-spin fa-fw"></i></button>
                                            <button v-else class="btn btn-primary me-2 pull-right"
                                                style="margin-top:5px;" @click.prevent="save_exit()"
                                                :disabled="savingOccurrence || submitOccurrence">Save
                                                and Exit</button>

                                            <button v-if="submitOccurrence"
                                                class="btn btn-primary pull-right" style="margin-top:5px;"
                                                disabled>Submit&nbsp;
                                                <i class="fa fa-circle-o-notch fa-spin fa-fw"></i></button>
                                            <button v-else class="btn btn-primary pull-right"
                                                style="margin-top:5px;" @click.prevent="submit()"
                                                :disbaled="saveExitOccurrence || savingOccurrence">Submit</button>
                                        </div>
                                    </div>
                                    <div v-else-if="hasUserEditMode" class="container">
                                        <div class="col-md-12 text-end">
                                            <button v-if="savingOccurrence"
                                                class="btn btn-primary pull-right" style="margin-top:5px;"
                                                disabled>Save Changes&nbsp;
                                                <i class="fa fa-circle-o-notch fa-spin fa-fw"></i></button>
                                            <button v-else class="btn btn-primary pull-right"
                                                style="margin-top:5px;" @click.prevent="save()">Save
                                                Changes</button>
                                        </div>
                                    </div>
                                </div>
                            </div>
                        </form>
                    </template>
                </div>
                </div>
            </div>
        </div>
        <!-- <SpeciesSplit ref="species_split" :occurrence="occurrence" :is_internal="true"
            @refreshFromResponse="refreshFromResponse" />
        <SpeciesCombine ref="species_combine" :occurrence="occurrence" :is_internal="true"
            @refreshFromResponse="refreshFromResponse" />
        <SpeciesRename ref="species_rename" :occurrence_original="occurrence" :is_internal="true"
            @refreshFromResponse="refreshFromResponse" /> -->
    </div>

</template>
<script>
import Vue from 'vue'
import datatable from '@vue-utils/datatable.vue'
import CommsLogs from '@common-utils/comms_logs.vue'
import Submission from '@common-utils/submission.vue'
import Workflow from '@common-utils/workflow.vue'
import ProposalOccurrence from '@/components/form_occurrence.vue'

// import SpeciesSplit from './species_split.vue'
// import SpeciesCombine from './species_combine.vue'
// import SpeciesRename from './species_rename.vue'

import {
    api_endpoints,
    helpers
}
    from '@/utils/hooks'
export default {
    name: 'InternalOccurrenceDetail',
    data: function () {
        let vm = this;
        return {
            occurrence: null,
            form: null,
            savingOccurrence: false,
            saveExitOccurrence: false,
            submitOccurrence: false,
            imageURL: '',
            isSaved: false,


            DATE_TIME_FORMAT: 'DD/MM/YYYY HH:mm:ss',
            comparing: false,
        }
    },
    components: {
        datatable,
        CommsLogs,
        Submission,
        Workflow,
        ProposalOccurrence,
        // SpeciesSplit,
        // SpeciesCombine,
        // SpeciesRename,
    },
    filters: {
        formatDate: function (data) {
            return data ? moment(data).format('DD/MM/YYYY HH:mm:ss') : '';
        }
    },
    computed: {
        csrf_token: function () {
            return helpers.getCookie('csrftoken')
        },
        isCommunity: function () {
            return this.occurrence.group_type === "community"
        },
        occurrence_form_url: function () {
            return (this.occurrence.group_type === "community") ?
                `/api/community/${this.occurrence.id}/community_save.json` :
                `/api/species/${this.occurrence.id}/species_save.json`;
        },
        occurrence_submit_url: function () {
            return (this.occurrence.group_type === "community") ?
                `community` :
                `species`;
        },
        display_group_type: function () {
            let group_type_string = this.occurrence.group_type
            // to Capitalize only first character
            return group_type_string.charAt(0).toUpperCase() + group_type_string.slice(1);
        },
        display_number: function () {
            return (this.occurrence.group_type === "community") ?
                this.occurrence.community_number :
                this.occurrence.species_number;
        },
        display_name: function () {
            return (this.occurrence.group_type === "community") ?
                (this.occurrence.taxonomy_details != null) ? this.occurrence.taxonomy_details.community_migrated_id : '' :
                (this.occurrence.taxonomy_details != null) ? this.occurrence.taxonomy_details.scientific_name + " (" + this.occurrence.taxonomy_details.taxon_name_id + ")" : '';
        },
        submitter_first_name: function () {
            if (this.occurrence && this.occurrence.submitter) {
                return this.occurrence.submitter.first_name
            } else {
                return ''
            }
        },
        submitter_last_name: function () {
            if (this.occurrence && this.occurrence.submitter) {
                return this.occurrence.submitter.last_name
            } else {
                return ''
            }
        },
        canSeeSubmission: function () {
            //return this.proposal && (this.proposal.processing_status != 'With Assessor (Requirements)' && this.proposal.processing_status != 'With Approver' && !this.isFinalised)
            //return this.proposal && (this.proposal.processing_status != 'With Assessor (Requirements)')
            return true
        },
        hasUserEditMode: function () {
            // Need to check for approved status as to show 'Save changes' button only when edit and not while view
            if (this.$route.query.action == 'edit') {
                return this.occurrence && this.occurrence.user_edit_mode ? true : false;
            }
            else {
                return false;
            }
        },
        canDiscard: function () {
            return this.occurrence && this.occurrence.processing_status === "Draft" ? true : false;
        },
        comms_url: function () {
            return helpers.add_endpoint_json(api_endpoints.occurrence, this.$route.params.occurrence_id + '/comms_log')
        },
        comms_add_url: function () {
            return helpers.add_endpoint_json(api_endpoints.occurrence, this.$route.params.occurrence_id + '/add_comms_log')
        },
        logs_url: function () {
            return helpers.add_endpoint_json(api_endpoints.occurrence, this.$route.params.occurrence_id + '/action_log')
        },
    },
    methods: {
        discardSpeciesProposal: function () {
            let vm = this;
            swal.fire({
                title: "Discard Application",
                text: "Are you sure you want to discard this proposal?",
                icon: "warning",
                showCancelButton: true,
                confirmButtonText: 'Discard Application',
                confirmButtonColor: '#d9534f'
            }).then((swalresult) => {
                if (swalresult.isConfirmed) {
                    vm.$http.delete(api_endpoints.discard_species_proposal(vm.occurrence.id))
                        .then((response) => {
                            swal.fire({
                                title: 'Discarded',
                                text: 'Your proposal has been discarded',
                                icon: 'success',
                                confirmButtonColor: '#226fbb',
                            });
                            vm.$router.push({
                                name: 'internal-species-communities-dash'
                            });
                        }, (error) => {
                            console.log(error);
                        });
                }
            }, (error) => {

            });
        },
        save: async function () {
            let vm = this;
            var missing_data = vm.can_submit("");
            vm.isSaved = false;
            if (missing_data != true) {
                swal.fire({
                    title: "Please fix following errors before saving",
                    text: missing_data,
                    icon: 'error',
                    confirmButtonColor: '#226fbb'
                })
                return false;
            }
            vm.savingOccurrence = true;
            let payload = new Object();
            Object.assign(payload, vm.occurrence);
            await vm.$http.post(vm.occurrence_form_url, payload).then(res => {
                swal.fire({
                    title: "Saved",
                    text: "Your changes has been saved",
                    icon: "success",
                    confirmButtonColor: '#226fbb'
                });
                vm.savingOccurrence = false;
                vm.isSaved = true;
            }, err => {
                var errorText = helpers.apiVueResourceError(err);
                swal.fire({
                    title: 'Save Error',
                    text: errorText,
                    icon: 'error',
                    confirmButtonColor: '#226fbb'
                });
                vm.savingOccurrence = false;
                vm.isSaved = false;
            });
        },
        save_exit: async function (e) {
            let vm = this;
            var missing_data = vm.can_submit("");
            if (missing_data != true) {
                swal.fire({
                    title: "Please fix following errors before saving",
                    text: missing_data,
                    icon: 'error',
                    confirmButtonColor: '#226fbb'
                })
                //vm.paySubmitting=false;
                return false;
            }
            vm.saveExitOccurrence = true;
            await vm.save().then(() => {
                if (vm.isSaved === true) {
                    vm.$router.push({
                        name: 'internal-species-communities-dash'
                    });
                }
                else {
                    vm.saveExitOccurrence = false;
                }
            });
        },
        save_before_submit: async function (e) {
            //console.log('save before submit');
            let vm = this;
            vm.saveError = false;

            let payload = new Object();
            Object.assign(payload, vm.occurrence);
            const result = await vm.$http.post(vm.occurrence_form_url, payload).then(res => {
                //return true;
            }, err => {
                var errorText = helpers.apiVueResourceError(err);
                swal.fire({
                    title: 'Submit Error',
                    //helpers.apiVueResourceError(err),
                    text: errorText,
                    icon: 'error',
                    confirmButtonColor: '#226fbb'
                })
                vm.submitOccurrence = false;
                vm.saveError = true;
                //return false;
            });
            return result;
        },
        can_submit: function (check_action) {
            let vm = this;
            let blank_fields = []
            if (vm.occurrence.group_type == 'flora' || vm.occurrence.group_type == 'fauna') {
                if (vm.occurrence.taxonomy_id == null || vm.occurrence.taxonomy_id == '') {
                    blank_fields.push('Scientific Name is missing')
                }
            }
            else {
                if (vm.occurrence.taxonomy_details.community_name == null || vm.occurrence.taxonomy_details.community_name == '') {
                    blank_fields.push('Community Name is missing')
                }
            }
            if (check_action == 'submit') {
                //TODO add validation for fields required before submit
            }
            if (blank_fields.length == 0) {
                return true;
            }
            else {
                return blank_fields;
            }
        },
        submit: async function () {
            let vm = this;

            var missing_data = vm.can_submit("submit");
            if (missing_data != true) {
                swal.fire({
                    title: "Please fix following errors before submitting",
                    text: missing_data,
                    icon: 'error',
                    confirmButtonColor: '#226fbb'
                })
                //vm.paySubmitting=false;
                return false;
            }

            vm.submitOccurrence = true;
            swal.fire({
                title: "Submit",
                text: "Are you sure you want to submit this application?",
                icon: "question",
                showCancelButton: true,
                confirmButtonText: "submit",
                confirmButtonColor: '#226fbb'
            }).then(async (swalresult) => {
                if (swalresult.isConfirmed) {
                    let result = await vm.save_before_submit()
                    if (!vm.saveError) {
                        let payload = new Object();
                        Object.assign(payload, vm.occurrence);
                        let submit_url = this.occurrence.group_type === "community" ?
                            helpers.add_endpoint_json(api_endpoints.community, vm.occurrence.id + '/submit') :
                            helpers.add_endpoint_json(api_endpoints.species, vm.occurrence.id + '/submit')
                        vm.$http.post(submit_url, payload).then(res => {
                            vm.occurrence = res.body;
                            // vm.$router.push({
                            //     name: 'submit_cs_proposal',
                            //     params: { conservation_status_obj: vm.conservation_status_obj}
                            // });
                            // TODO router should push to submit_cs_proposal for internal side 
                            vm.$router.push({
                                name: 'internal-species-communities-dash'
                            });
                        }, err => {
                            swal.fire({
                                title: 'Submit Error',
                                text: helpers.apiVueResourceError(err),
                                icon: 'error',
                                confirmButtonColor: '#226fbb'
                            });
                        });
                    }
                }
            }, (error) => {
                vm.submitOccurrence = false;
            });
        },
        refreshFromResponse: function (response) {
            let vm = this;
            vm.original_occurrence = helpers.copyObject(response.body);
            vm.occurrence = helpers.copyObject(response.body);
        },
        splitSpecies: async function () {
            this.$refs.species_split.occurrence_original = this.occurrence;
            let newSpeciesId1 = null
            try {
                const createUrl = api_endpoints.species + "/";
                let payload = new Object();
                payload.group_type_id = this.occurrence.group_type_id;
                let savedSpecies = await Vue.http.post(createUrl, payload);
                if (savedSpecies) {
                    newSpeciesId1 = savedSpecies.body.id;
                    Vue.http.get(`/api/species/${newSpeciesId1}/internal_species.json`).then(res => {
                        let species_obj = res.body.species_obj;
                        //--- to add empty documents array
                        species_obj.documents = []
                        //---empty threats array added to store the select threat ids in from the child component
                        species_obj.threats = []
                        this.$refs.species_split.occurrence_list.push(species_obj); //--temp species_obj
                    },
                        err => {
                            console.log(err);
                        });
                }
            }
            catch (err) {
                console.log(err);
                if (this.is_internal) {
                    return err;
                }
            }
            let newSpeciesId2 = null
            try {
                const createUrl = api_endpoints.species + "/";
                let payload = new Object();
                payload.group_type_id = this.occurrence.group_type_id
                let savedSpecies = await Vue.http.post(createUrl, payload);
                if (savedSpecies) {
                    newSpeciesId2 = savedSpecies.body.id;
                    Vue.http.get(`/api/species/${newSpeciesId2}/internal_species.json`).then(res => {
                        let species_obj = res.body.species_obj;
                        // to add documents id array from original species
                        species_obj.documents = []
                        //---empty threats array added to store the select threat ids in from the child component
                        species_obj.threats = []
                        this.$refs.species_split.occurrence_list.push(species_obj); //--temp species_obj
                    },
                        err => {
                            console.log(err);
                        });
                }
            }
            catch (err) {
                console.log(err);
                if (this.is_internal) {
                    return err;
                }
            }
            this.$refs.species_split.isModalOpen = true;
        },
        combineSpecies: async function () {
            this.$refs.species_combine.original_species_combine_list.push(this.occurrence); //--push current original into the array
            let newSpeciesId = null
            try {
                const createUrl = api_endpoints.species + "/";
                let payload = new Object();
                payload.group_type_id = this.occurrence.group_type_id;
                let savedSpecies = await Vue.http.post(createUrl, payload);
                if (savedSpecies) {
                    newSpeciesId = savedSpecies.body.id;
                    Vue.http.get(`/api/species/${newSpeciesId}/internal_species.json`).then(res => {
                        let species_obj = res.body.species_obj;
                        //--- to add empty documents array
                        species_obj.documents = []
                        //---empty threats array added to store the selected threat ids in from the child component
                        species_obj.threats = []
                        this.$refs.species_combine.new_combine_species = species_obj; //---assign the new created species to the modal obj
                    },
                        err => {
                            console.log(err);
                        });
                }

            }
            catch (err) {
                console.log(err);
                if (this.is_internal) {
                    return err;
                }
            }
            this.$refs.species_combine.isModalOpen = true;
        },
        renameSpecies: async function () {
            let rename_species_obj = null;
            let newRenameSpecies = await Vue.http.get(`/api/species/${this.occurrence.id}/rename_deep_copy.json`)
            if (newRenameSpecies) {
                rename_species_obj = newRenameSpecies.body.species_obj;
                this.$refs.species_rename.new_rename_species = rename_species_obj;
                this.$refs.species_rename.isModalOpen = true;
            }
        }
    },
    updated: function () {
        let vm = this;
        this.$nextTick(() => {
            vm.form = document.forms.occurrence;
        });
    },
    beforeRouteEnter: function (to, from, next) {
        //if (to.query.group_type_name === 'flora' || to.query.group_type_name === "fauna") {
        Vue.http.get(`/api/occurrence_paginated/${to.params.occurrence_id}/`).then(res => {
            next(vm => {
                vm.occurrence = res.body;
            });
        },
        err => {
            console.log(err);
        });
        /*}
        else {
            Vue.http.get(`/api/community/${to.params.occurrence_id}/internal_community.json`).then(res => {
                next(vm => {
                    vm.occurrence = res.body;
                });
            },
                err => {
                    console.log(err);
                });
        }*/
    },
}
</script>
