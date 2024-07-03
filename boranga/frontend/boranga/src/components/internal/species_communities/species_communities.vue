<template lang="html">
    <div v-if="species_community" class="container" id="internalSpeciesCommunity">
        <div class="row" style="padding-bottom: 50px;">
            <h3>{{ display_group_type }} {{ display_number }} - {{ display_name }}</h3>
            <div v-if="!comparing" class="col-md-3">
                <!-- TODO -->
                <template>
                    <div class="">
                        <div class="card card-default mb-3">
                            <div class="card-header">
                                Image
                            </div>
                            <div class="card-body">
                                <template>
                                    <div class="row mb-2 pb-2">
                                        <div v-if="!uploadingImage && speciesCommunitiesImage" class="col">
                                            <img :src="speciesCommunitiesImage" class="img-fluid rounded" />
                                        </div>
                                        <div v-else
                                            class="d-flex bg-light bg-gradient justify-content-center align-content-middle"
                                            style="height:200px">
                                            <div class="align-self-center text-muted">No Image Uploaded</div>
                                        </div>
                                    </div>
                                    <div v-if="hasUserEditMode" class="row border-top pt-3 mb-2">
                                        <div class="col">
                                            <div class="d-flex justify-content-center">
                                                <div class="text-muted">Image Actions</div>
                                            </div>
                                        </div>
                                    </div>
                                    <div v-if="hasUserEditMode" class="row">
                                        <div class="col">
                                            <div class="d-flex align-items-center flex-column">
                                                <label v-if="!speciesCommunitiesImage" for="image-upload" role="button"
                                                    class="btn btn-primary btn-sm w-50 mb-2 text-start"><i
                                                        class="bi bi-upload me-3"></i>
                                                    Upload</label>
                                                <input id="image-upload" class="d-none" type="file"
                                                    ref="speciesCommunitiesImage" @change="uploadImage">
                                                <button class="btn btn-secondary btn-sm w-50 mb-2 text-start"
                                                    @click="showReinstateImageModal"><i
                                                        class="bi bi-clock-history me-3"></i> Reinstate</button>
                                                <template v-if="!uploadingImage && speciesCommunitiesImage">
                                                    <label for="image-upload" role="button"
                                                        class="btn btn-primary btn-sm w-50 mb-2 text-start"><i
                                                            class="bi bi-pencil-fill me-3"></i>
                                                        Replace</label>
                                                    <input id="image-upload" class="d-none" type="file"
                                                        ref="speciesCommunitiesImage" @change="uploadImage">

                                                    <button @click="confirmDiscardImage"
                                                        class="btn btn-danger btn-sm w-50 mb-2 text-start"><i
                                                            class="bi bi-trash3-fill me-3"></i>
                                                        Discard</button>
                                                </template>
                                                <button v-if="uploadingImage"
                                                    class="btn btn-primary btn-sm w-50 mb-2 text-start">
                                                    <span class="spinner-border spinner-border-sm me-3" role="status"
                                                        aria-hidden="true"></span>
                                                    Uploading
                                                    <span class="visually-hidden">Loading...</span>
                                                </button>
                                            </div>
                                        </div>
                                    </div>
                                </template>
                            </div>
                        </div>
                    </div>
                </template>

                <CommsLogs :comms_url="comms_url" :logs_url="logs_url" :comms_add_url="comms_add_url"
                    :disable_add_entry="false" class="mb-3" />

                <Submission v-if="canSeeSubmission" :submitter_first_name="submitter_first_name"
                    :submitter_last_name="submitter_last_name" :lodgement_date="species_community.lodgement_date"
                    class="mb-3" />

                <div class="top-buffer-s">
                    <div class="card card-default">
                        <div class="card-header">
                            Workflow
                        </div>
                        <div class="card-body">
                            <div class="row">
                                <div class="col-sm-12">
                                    <strong>Status</strong><br />
                                    {{ species_community.processing_status }} <span v-if="isActive"> -
                                        {{ species_community.publishing_status.public_status }}</span>
                                </div>
                            </div>
                        </div>
                        <div v-if='hasUserEditMode' class="card-body border-top">
                            <div class="row">
                                <div class="col-sm-12">
                                    <div class="col-sm-12 top-buffer-s">
                                        <div class="row">
                                            <div class="col-sm-12">
                                                <strong>Action</strong><br />
                                            </div>
                                        </div>
                                        <div class="row" v-if="!isCommunity">
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
                                        <div class="row" v-if="isActive">
                                            <div class="col-sm-12" v-if="!isPublic">
                                                <button style="width:80%;" class="btn btn-primary top-buffer-s"
                                                    @click.prevent="makePublic()">Make Public</button><br />
                                            </div>
                                            <div class="col-sm-12" v-else>
                                                <button style="width:80%;" class="btn btn-primary top-buffer-s"
                                                    @click.prevent="makePrivate()">Make Private</button><br />
                                            </div>
                                        </div>
                                        <div v-if="canDiscard">
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
                                        </div>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
            <div class="col-md-9">
                <div class="row">
                    <template>
                        <div class="">
                            <div class="row">
                                <form :action="species_community_form_url" method="post" name="new_species"
                                    enctype="multipart/form-data">
                                    <ProposalSpeciesCommunities ref="species_communities"
                                        :species_community="species_community"
                                        :species_community_original="species_community_original"
                                        id="speciesCommunityStart" :is_internal="true"
                                        :is_readonly="species_community.readonly">
                                    </ProposalSpeciesCommunities>
                                    <input type="hidden" name="csrfmiddlewaretoken" :value="csrf_token" />
                                    <input type='hidden' name="species_community_id" :value="1" />
                                    <div class="row" style="margin-bottom: 50px">
                                        <div class="navbar fixed-bottom" style="background-color: #f5f5f5;">
                                            <div v-if="species_community.can_user_edit" class="container">
                                                <div class="col-md-12 text-end">
                                                    <button v-if="savingSpeciesCommunity"
                                                        class="btn btn-primary me-2 pull-right" style="margin-top:5px;"
                                                        disabled>Save and Continue&nbsp;
                                                        <i class="fa fa-circle-o-notch fa-spin fa-fw"></i></button>
                                                    <button v-else class="btn btn-primary me-2 ull-right"
                                                        style="margin-top:5px;" @click.prevent="save()"
                                                        :disabled="saveExitSpeciesCommunity || submitSpeciesCommunity">Save
                                                        and Continue</button>

                                                    <button v-if="saveExitSpeciesCommunity"
                                                        class="btn btn-primary me-2 pull-right" style="margin-top:5px;"
                                                        disabled>Save and Exit&nbsp;
                                                        <i class="fa fa-circle-o-notch fa-spin fa-fw"></i></button>
                                                    <button v-else class="btn btn-primary me-2 pull-right"
                                                        style="margin-top:5px;" @click.prevent="save_exit()"
                                                        :disabled="savingSpeciesCommunity || submitSpeciesCommunity">Save
                                                        and Exit</button>

                                                    <button v-if="submitSpeciesCommunity"
                                                        class="btn btn-primary pull-right" style="margin-top:5px;"
                                                        disabled>Submit&nbsp;
                                                        <i class="fa fa-circle-o-notch fa-spin fa-fw"></i></button>
                                                    <button v-else class="btn btn-primary pull-right"
                                                        style="margin-top:5px;" @click.prevent="submit()"
                                                        :disbaled="saveExitSpeciesCommunity || savingSpeciesCommunity">Submit</button>
                                                </div>
                                            </div>
                                            <div v-else-if="hasUserEditMode" class="container">
                                                <div class="col-md-12 text-end">
                                                    <button v-if="savingSpeciesCommunity"
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
                            </div>
                        </div>
                    </template>
                </div>
            </div>
        </div>
        <SpeciesSplit ref="species_split" :species_community="species_community" :is_internal="true"
            @refreshFromResponse="refreshFromResponse" />
        <SpeciesCombine ref="species_combine" :species_community="species_community" :is_internal="true"
            @refreshFromResponse="refreshFromResponse" />
        <SpeciesRename ref="species_rename" :species_community_original="species_community" :is_internal="true"
            @refreshFromResponse="refreshFromResponse" />
        <MakePublic ref="make_public" :species_community="species_community"
            :species_community_original="species_community_original" :is_internal="true"
            @refreshFromResponse="refreshFromResponse" />
        <ReinstateImage ref="reinstateImage" title="Reinstate Species Image" :imageHistoryUrl="image_history_url"
            @reinstateImage="reinstateImage" />
    </div>
</template>
<script>
import Vue from 'vue'
import datatable from '@vue-utils/datatable.vue'
import CommsLogs from '@common-utils/comms_logs.vue'
import Submission from '@common-utils/submission.vue'
import ProposalSpeciesCommunities from '@/components/form_species_communities.vue'
import SpeciesSplit from './species_split.vue'
import SpeciesCombine from './species_combine.vue'
import SpeciesRename from './species_rename.vue'
import MakePublic from './make_public.vue'
import ReinstateImage from '@common-utils/reinstate_image.vue'

import {
    api_endpoints,
    helpers
}
    from '@/utils/hooks'
export default {
    name: 'InternalSpeciesCommunity',
    data: function () {
        let vm = this;
        return {
            "species_community": null,
            "species_community_original": null,
            form: null,
            savingSpeciesCommunity: false,
            saveExitSpeciesCommunity: false,
            submitSpeciesCommunity: false,
            speciesCommunitiesImage: null,
            uploadingImage: false,
            isSaved: false,
            DATE_TIME_FORMAT: 'DD/MM/YYYY HH:mm:ss',
            comparing: false,
        }
    },
    components: {
        datatable,
        CommsLogs,
        Submission,
        ProposalSpeciesCommunities,
        SpeciesSplit,
        SpeciesCombine,
        SpeciesRename,
        MakePublic,
        ReinstateImage,
    },
    filters: {
        formatDate: function (data) {
            return data ? moment(data).format('DD/MM/YYYY HH:mm:ss') : '';
        }
    },
    watch: {
    },
    computed: {
        csrf_token: function () {
            return helpers.getCookie('csrftoken')
        },
        isCommunity: function () {
            return this.species_community.group_type === "community"
        },
        species_community_form_url: function () {
            return (this.species_community.group_type === "community") ?
                `/api/community/${this.species_community.id}/community_save.json` :
                `/api/species/${this.species_community.id}/species_save.json`;
        },
        species_community_submit_url: function () {
            return (this.species_community.group_type === "community") ?
                `community` :
                `species`;
        },
        display_group_type: function () {
            let group_type_string = this.species_community.group_type
            // to Capitalize only first character
            return group_type_string.charAt(0).toUpperCase() + group_type_string.slice(1);
        },
        display_number: function () {
            return (this.species_community.group_type === "community") ?
                this.species_community.community_number :
                this.species_community.species_number;
        },
        display_name: function () {
            return (this.species_community.group_type === "community") ?
                (this.species_community.taxonomy_details != null) ? this.species_community.taxonomy_details.community_migrated_id : '' :
                (this.species_community.taxonomy_details != null) ? this.species_community.taxonomy_details.scientific_name + " (" + this.species_community.taxonomy_details.taxon_name_id + ")" : '';
        },
        class_ncols: function () {
            return this.comparing ? 'col-md-12' : 'col-md-8';
        },
        submitter_first_name: function () {
            if (this.species_community && this.species_community.submitter) {
                return this.species_community.submitter.first_name
            } else {
                return ''
            }
        },
        submitter_last_name: function () {
            if (this.species_community && this.species_community.submitter) {
                return this.species_community.submitter.last_name
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
                return this.species_community && this.species_community.user_edit_mode ? true : false;
            }
            else {
                return false;
            }
        },
        isPublic: function () {
            return (this.species_community.group_type === "community") ?
                this.species_community.publishing_status.community_public ? true : false :
                this.species_community.publishing_status.species_public ? true : false;
        },
        isActive: function () {
            return this.species_community.processing_status === "Active" ? true : false;
        },
        canDiscard: function () {
            return this.species_community && this.species_community.processing_status === "Draft" ? true : false;
        },
        comms_url: function () {
            return (this.species_community.group_type === "community") ?
                helpers.add_endpoint_json(api_endpoints.community, this.$route.params.species_community_id + '/comms_log') :
                helpers.add_endpoint_json(api_endpoints.species, this.$route.params.species_community_id + '/comms_log');
        },
        comms_add_url: function () {
            return (this.species_community.group_type === "community") ?
                helpers.add_endpoint_json(api_endpoints.community, this.$route.params.species_community_id + '/add_comms_log') :
                helpers.add_endpoint_json(api_endpoints.species, this.$route.params.species_community_id + '/add_comms_log');
        },
        logs_url: function () {
            return (this.species_community.group_type === "community") ?
                helpers.add_endpoint_json(api_endpoints.community, this.$route.params.species_community_id + '/action_log') :
                helpers.add_endpoint_json(api_endpoints.species, this.$route.params.species_community_id + '/action_log');
        },
        image_history_url: function () {
            return this.species_community ? `/api/species/${this.species_community.id}/image_history/` : '';
        }
    },
    methods: {
        commaToNewline(s) {
            return s.replace(/[,;]/g, '\n');
        },
        uploadImage: function (event) {
            let vm = this;
            const files = event.target.files;
            const imageFile = files[0];
            if (!imageFile) {
                vm.uploadingImage = false;
                swal.fire({
                    title: 'Upload Image',
                    html: 'Please select an Image to upload.',
                    icon: 'error',
                    customClass: {
                        confirmButton: 'btn btn-primary',
                    },
                });
            } else {
                vm.uploadingImage = true;
                let data = new FormData();
                data.append('speciesCommunitiesImage', imageFile);

                if (this.species_community.group_type == 'community') {
                    var api_url = api_endpoints.community;
                }
                else {
                    var api_url = api_endpoints.species;
                }
                vm.$http.post(helpers.add_endpoint_json(api_url, (this.$route.params.species_community_id + '/upload_image')), data, {
                    emulateJSON: true
                }).then((response) => {
                    vm.uploadingImage = false;
                    vm.speciesCommunitiesImage = null;
                    vm.speciesCommunitiesImage = response.body.image_doc;
                    vm.species_community.image_doc = response.body.image_doc;
                }, (error) => {
                    console.log(error);
                    vm.uploadingImage = false;
                    vm.speciesCommunitiesImage = null;
                    let error_msg = '<br/>';
                    for (var key in error.body) {
                        error_msg += key + ': ' + error.body[key] + '<br/>';
                    }
                    swal.fire({
                        title: 'Upload ID',
                        html: 'There was an error uploading your ID.<br/>' + error_msg,
                        icon: 'error',
                        customClass: {
                            confirmButton: 'btn btn-primary',
                        },
                    });
                });
            }
        },
        showReinstateImageModal: function () {
            this.$refs.reinstateImage.isModalOpen = true;
        },
        reinstateImage: function (image) {
            let vm = this;
            if (this.species_community.group_type == 'community') {
                var api_url = api_endpoints.community;
            }
            else {
                var api_url = api_endpoints.species;
            }
            vm.$http.patch(helpers.add_endpoint_json(api_url, (this.$route.params.species_community_id + '/reinstate_image')), {
                pk: image.id
            }).then(() => {
                this.speciesCommunitiesImage = image.url;
                this.species_community.image_doc = image.url;
            }).catch((error) => {
                swal.fire({
                    title: 'Reinstate Image',
                    text: 'There was an error reinstating the image',
                    icon: 'error',
                    customClass: {
                        confirmButton: 'btn btn-primary',
                    },
                });
                console.log(error)
            })
        },
        confirmDiscardImage: function () {
            swal.fire({
                title: 'Discard Image',
                text: 'Are you sure you want to discard this image?',
                icon: 'question',
                showCancelButton: true,
                confirmButtonText: 'Discard',
                customClass: {
                    confirmButton: 'btn btn-primary',
                    cancelButton: 'btn btn-secondary'
                },
                reverseButtons: true
            }).then((swalresult) => {
                if (swalresult.isConfirmed) {
                    this.discardImage();
                }
            });
        },
        discardImage: async function () {
            let vm = this;
            if (this.species_community.group_type == 'community') {
                var api_url = api_endpoints.community;
            }
            else {
                var api_url = api_endpoints.species;
            }

            if (vm.speciesCommunitiesImage == null) {
                swal.fire({
                    title: 'Delete Image',
                    html: 'No Image uploaded.',
                    icon: 'error',
                    customClass: {
                        confirmButton: 'btn btn-primary',
                    },
                });
            } else {
                if (vm.species_community.image_doc) {
                    vm.$http.post(helpers.add_endpoint_json(api_url, (this.$route.params.species_community_id + '/delete_image')), {
                        emulateJSON: true
                    }).then((response) => {
                        vm.uploadingImage = false;
                        vm.speciesCommunitiesImage = null;
                        vm.speciesCommunitiesImage = response.body.image_doc;
                        vm.species_community.image_doc = response.body.image_doc;
                    }, (error) => {
                        console.log(error);
                        vm.uploadingImage = false;
                        vm.speciesCommunitiesImage = null;
                        let error_msg = '<br/>';
                        for (var key in error.body) {
                            error_msg += key + ': ' + error.body[key] + '<br/>';
                        }
                        swal.fire({
                            title: 'Delete Image',
                            html: 'There was an error deleting your image.<br/>' + error_msg,
                            icon: 'error',
                            customClass: {
                                confirmButton: 'btn btn-primary',
                            },
                        });
                    });
                }

            }
        },
        discardSpeciesProposal: function () {
            let vm = this;
            swal.fire({
                title: "Discard Proposal",
                text: "Are you sure you want to discard this proposal?",
                icon: "question",
                showCancelButton: true,
                confirmButtonText: 'Discard Proposal',
                customClass: {
                    confirmButton: 'btn btn-primary',
                    cancelButton: 'btn btn-secondary'
                },
                reverseButtons: true
            }).then((swalresult) => {
                if (swalresult.isConfirmed) {
                    vm.$http.patch(api_endpoints.discard_species_proposal(vm.species_community.id))
                        .then((response) => {
                            swal.fire({
                                title: 'Discarded',
                                text: 'The proposal has been discarded',
                                icon: 'success',
                                customClass: {
                                    confirmButton: 'btn btn-primary',
                                },
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
                    customClass: {
                        confirmButton: 'btn btn-primary',
                    },
                })
                return false;
            }
            vm.savingSpeciesCommunity = true;
            let payload = new Object();
            Object.assign(payload, vm.species_community);

            let was_public = "";
            if (vm.species_community.publishing_status.public_status === "Public") {
                was_public = " - record is now private"
            }

            await vm.$http.post(vm.species_community_form_url, payload).then(res => {
                vm.species_community = res.body;
                vm.species_community_original = helpers.copyObject(vm.species_community); //update original after save
                swal.fire({
                    title: "Saved",
                    text: "Your changes has been saved" + was_public,
                    icon: "success",
                    customClass: {
                        confirmButton: 'btn btn-primary',
                    },
                });
                vm.savingSpeciesCommunity = false;
                vm.isSaved = true;
            }, err => {
                var errorText = helpers.apiVueResourceError(err);
                swal.fire({
                    title: 'Save Error',
                    text: errorText,
                    icon: 'error',
                    customClass: {
                        confirmButton: 'btn btn-primary',
                    },
                });
                vm.savingSpeciesCommunity = false;
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
                    customClass: {
                        confirmButton: 'btn btn-primary',
                    },
                })
                //vm.paySubmitting=false;
                return false;
            }
            vm.saveExitSpeciesCommunity = true;
            await vm.save().then(() => {
                if (vm.isSaved === true) {
                    vm.$router.push({
                        name: 'internal-species-communities-dash'
                    });
                }
                else {
                    vm.saveExitSpeciesCommunity = false;
                }
            });
        },
        save_before_submit: async function (e) {
            //console.log('save before submit');
            let vm = this;
            vm.saveError = false;

            //only save if something has changed
            if (vm.can_submit("") != true) {
                return false;
            }

            let payload = new Object();
            Object.assign(payload, vm.species_community);
            const result = await vm.$http.post(vm.species_community_form_url, payload).then(res => {
                //return true;
            }, err => {
                var errorText = helpers.apiVueResourceError(err);
                swal.fire({
                    title: 'Submit Error',
                    //helpers.apiVueResourceError(err),
                    text: errorText,
                    icon: 'error',
                    customClass: {
                        confirmButton: 'btn btn-primary',
                    },
                })
                vm.submitSpeciesCommunity = false;
                vm.saveError = true;
                //return false;
            });
            return result;
        },
        can_submit: function (check_action) {
            let vm = this;

            if (check_action != 'submit') {
                //remove publishing status for check as it is handled separately
                let sc_no_ps = helpers.copyObject(vm.species_community);
                let sco_no_ps = helpers.copyObject(vm.species_community_original);

                sc_no_ps.publishing_status = undefined;
                sco_no_ps.publishing_status = undefined;

                if (helpers.checkForChange(sco_no_ps, sc_no_ps)) {
                    return ["No changes made"]
                }
            }

            let blank_fields = []
            if (vm.species_community.group_type == 'flora' || vm.species_community.group_type == 'fauna') {
                if (vm.species_community.taxonomy_id == null || vm.species_community.taxonomy_id == '') {
                    blank_fields.push(' Scientific Name is required')
                }
            }
            else {
                if (vm.species_community.taxonomy_details.community_name == null || vm.species_community.taxonomy_details.community_name == '') {
                    blank_fields.push(' Community Name is required')
                }
                if (vm.species_community.taxonomy_details.community_migrated_id == null || vm.species_community.taxonomy_details.community_migrated_id == '') {
                    blank_fields.push(' Community ID is required')
                }
            }
            if (check_action == 'submit') {
                //TODO add validation for fields required before submit
                if (vm.species_community.distribution.distribution == null || vm.species_community.distribution.distribution == '') {
                    blank_fields.push(' Distribution is required')
                }
                if (vm.species_community.regions == null || vm.species_community.regions.length == 0 || vm.species_community.regions == '') {
                    blank_fields.push(' Region is required')
                }
                if (vm.species_community.districts == null || vm.species_community.districts == '' || vm.species_community.districts.length == 0) {
                    blank_fields.push(' District is required')
                }
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
                    customClass: {
                        confirmButton: 'btn btn-primary',
                    },
                })
                //vm.paySubmitting=false;
                return false;
            }

            vm.submitSpeciesCommunity = true;
            swal.fire({
                title: "Submit",
                text: "Are you sure you want to submit this application?",
                icon: "question",
                showCancelButton: true,
                confirmButtonText: "submit",
                customClass: {
                    confirmButton: 'btn btn-primary',
                    cancelButton: 'btn btn-secondary',
                },
                reverseButtons: true
            }).then(async (swalresult) => {
                if (swalresult.isConfirmed) {
                    let result = await vm.save_before_submit()
                    if (!vm.saveError) {
                        let payload = new Object();
                        Object.assign(payload, vm.species_community);
                        let submit_url = this.species_community.group_type === "community" ?
                            helpers.add_endpoint_json(api_endpoints.community, vm.species_community.id + '/submit') :
                            helpers.add_endpoint_json(api_endpoints.species, vm.species_community.id + '/submit')
                        vm.$http.post(submit_url, payload).then(res => {
                            vm.species_community = res.body;
                            vm.species_community_original = helpers.copyObject(vm.species_community);
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
                                customClass: {
                                    confirmButton: 'btn btn-primary',
                                },
                            });
                        });
                    }
                }
            }, (error) => {
                vm.submitSpeciesCommunity = false;
            });
        },
        save_wo: function () {
            let vm = this;
            let formData = new FormData(vm.form);
            vm.$http.post(vm.proposal_form_url, formData).then(res => {
            }, err => {
            });
        },
        refreshFromResponse: function (response) {
            let vm = this;
            vm.species_community = helpers.copyObject(response.body);
            vm.species_community_original = copyObject(vm.species_community);
        },
        refreshSpeciesCommunity: function () {
            let vm = this;
            if (vm.species_community.group_type === 'flora' || vm.species_community.group_type === "fauna") {
                Vue.http.get(`/api/species/${vm.species_community.id}/internal_species.json`)
                    .then(res => {
                        vm.species_community = res.body.species_obj;
                        vm.species_community_original = helpers.copyObject(vm.species_community);
                        vm.speciesCommunitiesImage = vm.species_community.image_doc;
                    },
                        err => {
                            console.log(err);
                        });
            } else {
                Vue.http.get(`/api/community/${vm.species_community.id}/internal_community.json`)
                    .then(res => {
                        vm.species_community = res.body.community_obj;
                        vm.species_community_original = helpers.copyObject(vm.species_community);
                        vm.speciesCommunitiesImage = vm.species_community.image_doc;
                    },
                        err => {
                            console.log(err);
                        });
            }
        },
        splitSpecies: async function () {
            this.$refs.species_split.species_community_original = this.species_community;
            let newSpeciesId1 = null
            try {
                const createUrl = api_endpoints.species + "/";
                let payload = new Object();
                payload.group_type_id = this.species_community.group_type_id;
                let savedSpecies = await Vue.http.post(createUrl, payload);
                if (savedSpecies) {
                    newSpeciesId1 = savedSpecies.body.id;
                    Vue.http.get(`/api/species/${newSpeciesId1}/internal_species.json`).then(res => {
                        let species_obj = res.body.species_obj;
                        //--- to add empty documents array
                        species_obj.documents = []
                        //---empty threats array added to store the select threat ids in from the child component
                        species_obj.threats = []
                        this.$refs.species_split.new_species_list.push(species_obj); //--temp species_obj
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
                payload.group_type_id = this.species_community.group_type_id
                let savedSpecies = await Vue.http.post(createUrl, payload);
                if (savedSpecies) {
                    newSpeciesId2 = savedSpecies.body.id;
                    Vue.http.get(`/api/species/${newSpeciesId2}/internal_species.json`).then(res => {
                        let species_obj = res.body.species_obj;
                        // to add documents id array from original species
                        species_obj.documents = []
                        //---empty threats array added to store the select threat ids in from the child component
                        species_obj.threats = []
                        this.$refs.species_split.new_species_list.push(species_obj); //--temp species_obj
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
            this.$refs.species_combine.original_species_combine_list.push(this.species_community); //--push current original into the array
            let newSpeciesId = null
            try {
                const createUrl = api_endpoints.species + "/";
                let payload = new Object();
                payload.group_type_id = this.species_community.group_type_id;
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
            let newRenameSpecies = await Vue.http.get(`/api/species/${this.species_community.id}/rename_deep_copy.json`)
            if (newRenameSpecies) {
                rename_species_obj = newRenameSpecies.body.species_obj;
                this.$refs.species_rename.new_rename_species = rename_species_obj;
                this.$refs.species_rename.isModalOpen = true;
            }
        },
        makePublic: async function () {
            this.$refs.make_public.isModalOpen = true;
        },
        makePrivate: function () {
            let vm = this;
            let endpoint = api_endpoints.species;
            if (this.species_community.group_type === "community") {
                vm.species_community.publishing_status.community_public = false;
                endpoint = api_endpoints.community;
            } else {
                vm.species_community.publishing_status.species_public = false;
            }
            let data = JSON.stringify(vm.species_community.publishing_status)
            vm.$http.post(helpers.add_endpoint_json(endpoint, (vm.species_community.id + '/update_publishing_status')), data, {
                emulateJSON: true
            }).then((response) => {
                vm.updatingPublishing = false;
                vm.species_community.publishing_status = response.body;
                vm.species_community_original.publishing_status = helpers.copyObject(vm.species_community.publishing_status);
                swal.fire({
                    title: 'Saved',
                    text: 'Record has been made private',
                    icon: 'success',
                    customClass: {
                        confirmButton: 'btn btn-primary',
                    },
                });
            }, (error) => {
                var text = helpers.apiVueResourceError(error);
                swal.fire({
                    title: 'Error',
                    text: 'Publishing settings cannot be updated because of the following error: ' + text,
                    icon: 'error',
                    customClass: {
                        confirmButton: 'btn btn-primary',
                    },
                });
                vm.updatingPublishing = false;
            });
        }
    },
    created: function () {
        if (!this.species_community) {
            let end_point_type = 'species';
            if (this.$route.query.group_type_name === 'community') {
                end_point_type = 'community';
            }
            Vue.http.get(`/api/${end_point_type}/${this.$route.params.species_community_id}/internal_${end_point_type}.json`).then(res => {
                this.species_community = res.body[`${end_point_type}_obj`]; //--temp community_obj
                this.species_community_original = helpers.copyObject(this.species_community);
                this.speciesCommunitiesImage = this.species_community.image_doc;
            },
                err => {
                    console.log(err);
                });
        }
    },
    updated: function () {
        let vm = this;
        this.$nextTick(() => {
            vm.form = document.forms.new_species;
        });
    },
    beforeRouteEnter: function (to, from, next) {
        let end_point_type = 'species';
        if (to.query.group_type_name === 'community') {
            end_point_type = 'community';
        }
        Vue.http.get(`/api/${end_point_type}/${to.params.species_community_id}/internal_${end_point_type}.json`).then(res => {
            next(vm => {
                vm.species_community = res.body[`${end_point_type}_obj`]; //--temp community_obj
                vm.species_community_original = helpers.copyObject(vm.species_community);
                vm.speciesCommunitiesImage = vm.species_community.image_doc;
            });
        },
            err => {
                console.log(err);
            });
    },
}
</script>
<style scoped>
.top-buffer-s {
    margin-top: 10px;
}

.actionBtn {
    cursor: pointer;
}

.hidePopover {
    display: none;
}

.separator {
    border: 1px solid;
    margin-top: 15px;
    margin-bottom: 10px;
    width: 100%;
}
</style>
