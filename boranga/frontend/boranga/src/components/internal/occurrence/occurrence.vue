<template lang="html">
    <div class="container" id="internal-occurence-detail">
        <div class="row" style="padding-bottom: 50px;">
            <div v-if="occurrence" class="col">
                <h3>Occurrence: {{ occurrence.occurrence_number }} - <span class="text-capitalize">{{ display_group_type
                        }}</span></h3>
                    <h4 v-if="occurrence.combined_occurrence" class="text-muted mb-3">
                    Combined in to Occurrence:
                    <template>
                        OCC{{ occurrence.combined_occurrence_id }} <small><a
                                :href="`/internal/occurrence/${occurrence.combined_occurrence_id}?group_type_name=${occurrence.group_type}&action=view`"
                                target="_blank"><i class="bi bi-box-arrow-up-right"></i></a></small>
                    </template>
                </h4>
                <div class="row pb-4">
                    <div v-if="!comparing" class="col-md-3">

                        <CommsLogs :comms_url="comms_url" :logs_url="logs_url" :comms_add_url="comms_add_url"
                            :disable_add_entry="false" class="mb-3" />

                        <Submission v-if="canSeeSubmission" :submitter_first_name="submitter_first_name"
                            :submitter_last_name="submitter_last_name" :lodgement_date="occurrence.lodgement_date"
                            class="mb-3" />

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
                                        <div class="col-sm-12 top-buffer-s">
                                            <template v-if="hasUserEditMode">
                                                <div class="row">
                                                    <div class="col-sm-12">
                                                        <strong>Action</strong><br />
                                                    </div>
                                                </div>
                                                <div v-if="isDraft" class="row">
                                                    <div class="col-sm-12">
                                                        <button style="width:80%;" class="btn btn-primary mb-2"
                                                            @click.prevent="activateOccurrence()">Activate</button><br />
                                                    </div>
                                                </div>
                                                <div v-else class="row">
                                                    <div v-if="canLock" class="col-sm-12">
                                                        <button style="width:80%;" class="btn btn-primary mb-2"
                                                            @click.prevent="lockOccurrence()">Lock</button><br />
                                                    </div>
                                                    <div class="col-sm-12">
                                                        <button style="width:80%;" class="btn btn-primary mb-2"
                                                            @click.prevent="splitOccurrence()">Split</button><br />
                                                    </div>
                                                    <div class="col-sm-12">
                                                        <button style="width:80%;" class="btn btn-primary mb-2"
                                                            @click.prevent="combineOccurrence()">Combine</button><br />
                                                    </div>
                                                    <div v-if="canClose" class="col-sm-12">
                                                        <button style="width:80%;" class="btn btn-primary mb-2"
                                                            @click.prevent="closeOccurrence()">Close</button><br />
                                                    </div>
                                                </div>
                                            </template>
                                            <template v-else-if="canUnlock">
                                                <div class="row">
                                                    <div class="col-sm-12">
                                                        <strong>Action</strong><br />
                                                    </div>
                                                </div>
                                                <div class="col-sm-12">
                                                    <button style="width:80%;" class="btn btn-primary mb-2"
                                                        @click.prevent="unlockOccurrence()">Unlock</button><br />
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

                                <ProposalOccurrence v-if="occurrence" :occurrence_obj="occurrence" id="OccurrenceStart"
                                    ref="occurrence" @refreshFromResponse="refreshFromResponse">
                                </ProposalOccurrence>

                                <input type="hidden" name="csrfmiddlewaretoken" :value="csrf_token" />
                                <input type='hidden' name="occurrence_id" :value="1" />
                                <div class="row" style="margin-bottom: 50px">
                                    <div class="navbar fixed-bottom" style="background-color: #f5f5f5;">
                                        <div v-if="hasUserEditMode" class="container">
                                            <div class="col-md-12 text-end">
                                                <button v-if="savingOccurrence" class="btn btn-primary pull-right"
                                                    style="margin-top:5px;" disabled>Save Changes&nbsp;
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
        <!-- <OccurrenceSplit ref="occurrence_split" :occurrence="occurrence" :is_internal="true"
            @refreshFromResponse="refreshFromResponse" />-->
        <OccurrenceCombine v-if="occurrence" ref="occurrence_combine" :main_occurrence_obj="occurrence" :is_internal="true"
            @refreshFromResponse="refreshFromResponse" :key="combine_key"/>
    </div>

</template>
<script>
import Vue from 'vue'
import datatable from '@vue-utils/datatable.vue'
import CommsLogs from '@common-utils/comms_logs.vue'
import Submission from '@common-utils/submission.vue'
import ProposalOccurrence from '@/components/form_occurrence.vue'

// import OccurrenceSplit from './occurrence_split.vue'
import OccurrenceCombine from './occurrence_combine.vue'
// import OccurrenceRename from './occurrence_rename.vue'

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
            combine_key: 0,

            DATE_TIME_FORMAT: 'DD/MM/YYYY HH:mm:ss',
            comparing: false,
        }
    },
    components: {
        datatable,
        CommsLogs,
        Submission,
        ProposalOccurrence,
        // OccurrenceSplit,
        OccurrenceCombine,
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
            return `/api/occurrence/${this.occurrence.id}/occurrence_save.json`;
        },
        occurrence_submit_url: function () {
            return `occurrence`;
        },
        display_group_type: function () {
            if (this.occurrence && this.occurrence.group_type) {
                return this.occurrence.group_type;
            }
            return '';
        },
        display_number: function () {
            return this.occurrence.occurrence_number;
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
            return this.occurrence && this.occurrence.can_user_edit ? true : false;
        },
        isDraft: function () {
            return this.occurrence && this.occurrence.processing_status === "Draft" ? true : false;
        },
        canLock: function () {
            return this.occurrence && this.occurrence.processing_status === "Active" ? true : false;
        },
        canUnlock: function () {
            return this.occurrence && this.occurrence.processing_status === "Locked" ? true : false;
        },
        //TODO: can we close locked? should we only close locked?
        canClose: function () {
            return this.occurrence && this.occurrence.processing_status === "Active" ? true : false;
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
        save: async function () {
            let vm = this;

            console.log(vm.occurrence);

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
            vm.savingOccurrence = true;

            // add map geometry to the occurrence
            if (vm.$refs.occurrence.$refs.occ_location.$refs.component_map) {
                vm.$refs.occurrence.$refs.occ_location.$refs.component_map.setLoadingMap(
                    true
                );
                vm.occurrence.occ_geometry =
                    vm.$refs.occurrence.$refs.occ_location.$refs.component_map.getJSONFeatures();
            }

            let payload = new Object();
            Object.assign(payload, vm.occurrence);
            await vm.$http.post(vm.occurrence_form_url, payload).then(res => {
                swal.fire({
                    title: "Saved",
                    text: "Your changes has been saved",
                    icon: "success",
                    customClass: {
                        confirmButton: 'btn btn-primary',
                    },
                });
                vm.savingOccurrence = false;
                vm.isSaved = true;
                vm.refreshFromResponse(res);
                vm.$refs.occurrence.$refs.occ_location.$refs.component_map.setLoadingMap(false);
                vm.$refs.occurrence.$refs.occ_location.incrementComponentMapKey();
                vm.$refs.occurrence.$refs.occ_location.refreshDatatables();
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
                vm.savingOccurrence = false;
                vm.isSaved = false;
                vm.$refs.occurrence.$refs.occ_location.$refs.component_map.setLoadingMap(false);
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
            vm.saveExitOccurrence = true;
            await vm.save().then(() => {
                if (vm.isSaved === true) {
                    vm.$router.push({
                        name: 'internal-occurrence-dash'
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
                    customClass: {
                        confirmButton: 'btn btn-primary',
                    },
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
                if (vm.occurrence.species == null || vm.occurrence.species == '') {
                    blank_fields.push('Scientific Name is missing')
                }
            }
            else {
                if (vm.occurrence.community == null || vm.occurrence.community == '') {
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
                    customClass: {
                        confirmButton: 'btn btn-primary',
                    },
                })
                //vm.paySubmitting=false;
                return false;
            }

            vm.submitOccurrence = true;
            swal.fire({
                title: "Submit Occurrence",
                text: "Are you sure you want to submit this Occurrence?",
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
                    let result = await vm.save_before_submit()
                    if (!vm.saveError) {
                        let payload = new Object();
                        Object.assign(payload, vm.occurrence);
                        helpers.add_endpoint_json(api_endpoints.occurrence, vm.occurrence.id + '/submit');
                        vm.$http.post(submit_url, payload).then(res => {
                            vm.occurrence = res.body;
                            vm.$router.push({
                                name: 'internal-occurrence-dash'
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
                vm.submitOccurrence = false;
            });
        },
        refreshFromResponse: function (response) {
            let vm = this;
            vm.original_occurrence = helpers.copyObject(response.body);
            vm.occurrence = helpers.copyObject(response.body);
            vm.combine_key++;
        },
        activateOccurrence: async function () {
            let vm = this;
            await vm.$http.post(`/api/occurrence/${this.occurrence.id}/activate.json`).then(res => {
                swal.fire({
                    title: "Activated",
                    text: "Occurrence has been Activated",
                    icon: "success",
                    customClass: {
                        confirmButton: 'btn btn-primary',
                    },
                }).then(async (swalresult) => {
                    this.$router.go(this.$router.currentRoute);
                });
            }, err => {
                var errorText = helpers.apiVueResourceError(err);
                swal.fire({
                    title: 'Activate Error',
                    text: errorText,
                    icon: 'error',
                    customClass: {
                        confirmButton: 'btn btn-primary',
                    },
                });
            });
        },
        lockOccurrence: async function () {
            let vm = this;
            await vm.$http.post(`/api/occurrence/${this.occurrence.id}/lock_occurrence.json`).then(res => {
                swal.fire({
                    title: "Locked",
                    text: "Occurrence has been Locked",
                    icon: "success",
                    customClass: {
                        confirmButton: 'btn btn-primary',
                    },
                }).then(async (swalresult) => {
                    this.$router.go(this.$router.currentRoute);
                });
            }, err => {
                var errorText = helpers.apiVueResourceError(err);
                swal.fire({
                    title: 'Lock Error',
                    text: errorText,
                    icon: 'error',
                    customClass: {
                        confirmButton: 'btn btn-primary',
                    },
                });
            });
        },
        unlockOccurrence: async function () {
            let vm = this;
            await vm.$http.post(`/api/occurrence/${this.occurrence.id}/unlock_occurrence.json`).then(res => {
                swal.fire({
                    title: "Unlocked",
                    text: "Occurrence has been Unlocked",
                    icon: "success",
                    customClass: {
                        confirmButton: 'btn btn-primary',
                    },
                }).then(async (swalresult) => {
                    this.$router.go(this.$router.currentRoute);
                });
            }, err => {
                var errorText = helpers.apiVueResourceError(err);
                swal.fire({
                    title: 'Unlock Error',
                    text: errorText,
                    icon: 'error',
                    customClass: {
                        confirmButton: 'btn btn-primary',
                    },
                });
            });
        },
        closeOccurrence: async function () {
            let vm = this;
            swal.fire({
                title: "Close",
                text: "Are you sure you want to close this Occurrence? This cannot be undone.",
                icon: "question",
                showCancelButton: true,
                confirmButtonText: "Close Occurrence",
                customClass: {
                    confirmButton: 'btn btn-primary',
                    cancelButton: 'btn btn-secondary',
                },
                reverseButtons: true,
            }).then(async (swalresult) => {
                if (swalresult.isConfirmed) {
                    await vm.$http.post(`/api/occurrence/${this.occurrence.id}/close_occurrence.json`).then(res => {
                        swal.fire({
                            title: "Closed",
                            text: "Occurrence has been Closed",
                            icon: "success",
                            customClass: {
                                confirmButton: 'btn btn-primary',
                            },
                        }).then(async (swalresult) => {
                            vm.$router.push({
                                name: 'internal-occurrence-dash'
                            });
                        });
                    }, err => {
                        var errorText = helpers.apiVueResourceError(err);
                        swal.fire({
                            title: 'Close Error',
                            text: errorText,
                            icon: 'error',
                            customClass: {
                                confirmButton: 'btn btn-primary',
                            },
                        });
                    });
                }
            });
        },
        splitOccurrence: async function () {
            //this.$refs.occurrence_split.isModalOpen = true;
        },
        combineOccurrence: async function () {
            this.$refs.occurrence_combine.isModalOpen = true;
        },
    },
    updated: function () {
        let vm = this;
        this.$nextTick(() => {
            vm.form = document.forms.occurrence;
        });
    },
    beforeRouteEnter: function (to, from, next) {
        //if (to.query.group_type_name === 'flora' || to.query.group_type_name === "fauna") {
        Vue.http.get(`/api/occurrence/${to.params.occurrence_id}/`).then(res => {
            next(vm => {
                vm.occurrence = res.body;
            });
        },
            err => {
                console.log(err);
            });
    },
}
</script>
