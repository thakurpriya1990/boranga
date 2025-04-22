<template lang="html">
    <div id="internal-occurence-detail" class="container">
        <div class="row" style="padding-bottom: 50px">
            <div v-if="occurrence" class="col">
                <h3>
                    Occurrence: {{ occurrence.occurrence_number }} -
                    <span class="text-capitalize">{{
                        display_group_type
                    }}</span>
                </h3>
                <h4
                    v-if="occurrence.combined_occurrence"
                    class="text-muted mb-3"
                >
                    Combined in to Occurrence: OCC{{
                        occurrence.combined_occurrence_id
                    }}
                    <small
                        ><a
                            :href="`/internal/occurrence/${occurrence.combined_occurrence_id}?group_type_name=${occurrence.group_type}&action=view`"
                            target="_blank"
                            ><i class="bi bi-box-arrow-up-right"></i></a
                    ></small>
                </h4>
                <div class="row pb-4">
                    <div v-if="!comparing" class="col-md-3">
                        <CommsLogs
                            :comms_url="comms_url"
                            :logs_url="logs_url"
                            :comms_add_url="comms_add_url"
                            :disable_add_entry="!occurrence.can_add_log"
                            class="mb-3"
                        />

                        <Submission
                            v-if="canSeeSubmission"
                            :submitter_first_name="submitter_first_name"
                            :submitter_last_name="submitter_last_name"
                            :lodgement_date="occurrence.lodgement_date"
                            class="mb-3"
                        />

                        <div class="card card-default sticky-top">
                            <div class="card-header">Workflow</div>
                            <div class="card-body card-collapse">
                                <strong>Status</strong><br />
                                {{ occurrence.processing_status }}
                            </div>
                            <div class="card-body border-top">
                                <div class="col-sm-12">
                                    <template v-if="hasUserEditMode">
                                        <div class="row mb-2">
                                            <div class="col-sm-12">
                                                <strong>Action</strong><br />
                                            </div>
                                        </div>
                                        <div v-if="isDraft" class="row">
                                            <div class="col-sm-12">
                                                <button
                                                    style="width: 80%"
                                                    class="btn btn-primary mb-2"
                                                    @click.prevent="
                                                        activateOccurrence()
                                                    "
                                                >
                                                    Activate</button
                                                ><br />
                                            </div>
                                        </div>
                                        <div v-else class="row">
                                            <div
                                                v-if="canLock"
                                                class="col-sm-12"
                                            >
                                                <button
                                                    style="width: 80%"
                                                    class="btn btn-primary mb-2"
                                                    @click.prevent="
                                                        lockOccurrence()
                                                    "
                                                >
                                                    Lock</button
                                                ><br />
                                            </div>
                                            <div
                                                v-if="canClose"
                                                class="col-sm-12"
                                            >
                                                <button
                                                    style="width: 80%"
                                                    class="btn btn-primary mb-2"
                                                    @click.prevent="
                                                        splitOccurrence()
                                                    "
                                                >
                                                    Split</button
                                                ><br />
                                            </div>
                                            <div
                                                v-if="canClose"
                                                class="col-sm-12"
                                            >
                                                <button
                                                    style="width: 80%"
                                                    class="btn btn-primary mb-2"
                                                    @click.prevent="
                                                        combineOccurrence()
                                                    "
                                                >
                                                    Combine</button
                                                ><br />
                                            </div>
                                        </div>
                                    </template>
                                    <template v-else-if="canUnlock">
                                        <div class="row mb-2">
                                            <div class="col-sm-12">
                                                <strong>Action</strong><br />
                                            </div>
                                        </div>
                                        <div class="col-sm-12">
                                            <button
                                                style="width: 80%"
                                                class="btn btn-primary mb-2"
                                                @click.prevent="
                                                    unlockOccurrence()
                                                "
                                            >
                                                Unlock</button
                                            ><br />
                                        </div>
                                    </template>
                                    <template v-else-if="canReopen">
                                        <div class="row mb-2">
                                            <div class="col-sm-12">
                                                <button
                                                    style="width: 80%"
                                                    class="btn btn-primary mb-2"
                                                    @click.prevent="
                                                        reopenOccurrence()
                                                    "
                                                >
                                                    Reopen</button
                                                ><br />
                                            </div>
                                        </div>
                                    </template>
                                </div>
                            </div>
                        </div>
                    </div>
                    <div class="col-md-9">
                        <form
                            :action="occurrence_form_url"
                            method="post"
                            name="occurrence"
                            enctype="multipart/form-data"
                        >
                            <ProposalOccurrence
                                v-if="occurrence"
                                id="OccurrenceStart"
                                ref="occurrence"
                                :occurrence_obj="occurrence"
                                @refresh-from-response="refreshFromResponse"
                            >
                            </ProposalOccurrence>

                            <input
                                type="hidden"
                                name="csrfmiddlewaretoken"
                                :value="csrf_token"
                            />
                            <input
                                type="hidden"
                                name="occurrence_id"
                                :value="1"
                            />
                            <div class="row" style="margin-bottom: 50px">
                                <div
                                    class="navbar fixed-bottom"
                                    style="background-color: #f5f5f5"
                                >
                                    <div class="container">
                                        <div class="col-md-6">
                                            <button
                                                class="btn btn-primary me-2 pull-left"
                                                style="margin-top: 5px"
                                                @click.prevent="
                                                    returnToDashboard
                                                "
                                            >
                                                Return to Dashboard
                                            </button>
                                        </div>
                                        <div
                                            v-if="hasUserEditMode"
                                            class="col-md-6 text-end"
                                        >
                                            <button
                                                v-if="savingOccurrence"
                                                class="btn btn-primary pull-right"
                                                style="margin-top: 5px"
                                                disabled
                                            >
                                                Save Changes
                                                <span
                                                    class="spinner-border spinner-border-sm"
                                                    role="status"
                                                    aria-hidden="true"
                                                ></span>
                                                <span class="visually-hidden"
                                                    >Loading...</span
                                                >
                                            </button>
                                            <button
                                                v-else
                                                class="btn btn-primary pull-right"
                                                style="margin-top: 5px"
                                                @click.prevent="save()"
                                            >
                                                Save Changes
                                            </button>
                                        </div>
                                    </div>
                                </div>
                            </div>
                        </form>
                    </div>
                </div>
            </div>
        </div>
        <!-- <OccurrenceSplit ref="occurrence_split" :occurrence="occurrence" :is_internal="true"
            @refreshFromResponse="refreshFromResponse" />-->
        <OccurrenceCombine
            v-if="occurrence"
            ref="occurrence_combine"
            :key="combine_key"
            :main_occurrence_obj="occurrence"
            :is_internal="true"
            @refresh-from-response="refreshFromResponse"
        />
    </div>
</template>
<script>
import CommsLogs from '@common-utils/comms_logs.vue';
import Submission from '@common-utils/submission.vue';
import ProposalOccurrence from '@/components/form_occurrence.vue';

// import OccurrenceSplit from './occurrence_split.vue'
import OccurrenceCombine from './occurrence_combine.vue';
// import OccurrenceRename from './occurrence_rename.vue'

import { api_endpoints, helpers } from '@/utils/hooks';
export default {
    name: 'InternalOccurrenceDetail',
    components: {
        CommsLogs,
        Submission,
        ProposalOccurrence,
        // OccurrenceSplit,
        OccurrenceCombine,
    },
    filters: {
        formatDate: function (data) {
            return data ? moment(data).format('DD/MM/YYYY HH:mm:ss') : '';
        },
    },
    beforeRouteEnter: function (to, from, next) {
        //if (to.query.group_type_name === 'flora' || to.query.group_type_name === "fauna") {
        fetch(`/api/occurrence/${to.params.occurrence_id}/`).then(
            async (response) => {
                next(async (vm) => {
                    vm.occurrence = await response.json();
                });
            },
            (err) => {
                console.log(err);
            }
        );
    },
    data: function () {
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
        };
    },
    computed: {
        csrf_token: function () {
            return helpers.getCookie('csrftoken');
        },
        isCommunity: function () {
            return this.occurrence.group_type === 'community';
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
                return this.occurrence.submitter.first_name;
            } else {
                return '';
            }
        },
        submitter_last_name: function () {
            if (this.occurrence && this.occurrence.submitter) {
                return this.occurrence.submitter.last_name;
            } else {
                return '';
            }
        },
        canSeeSubmission: function () {
            //return this.proposal && (this.proposal.processing_status != 'With Assessor (Requirements)' && this.proposal.processing_status != 'With Approver' && !this.isFinalised)
            //return this.proposal && (this.proposal.processing_status != 'With Assessor (Requirements)')
            return true;
        },
        hasUserEditMode: function () {
            // Need to check for approved status as to show 'Save changes' button only when edit and not while view
            return this.occurrence && this.occurrence.can_user_edit
                ? true
                : false;
        },
        isDraft: function () {
            return this.occurrence &&
                this.occurrence.processing_status === 'Draft'
                ? true
                : false;
        },
        canLock: function () {
            return this.occurrence &&
                this.occurrence.processing_status === 'Active'
                ? true
                : false;
        },
        canUnlock: function () {
            return this.occurrence &&
                this.occurrence.processing_status === 'Locked'
                ? true
                : false;
        },
        canClose: function () {
            return this.occurrence &&
                this.occurrence.processing_status === 'Active'
                ? true
                : false;
        },
        canReopen: function () {
            return this.occurrence && this.occurrence.can_user_reopen
                ? true
                : false;
        },
        comms_url: function () {
            return helpers.add_endpoint_json(
                api_endpoints.occurrence,
                this.$route.params.occurrence_id + '/comms_log'
            );
        },
        comms_add_url: function () {
            return helpers.add_endpoint_json(
                api_endpoints.occurrence,
                this.$route.params.occurrence_id + '/add_comms_log'
            );
        },
        logs_url: function () {
            return helpers.add_endpoint_json(
                api_endpoints.occurrence,
                this.$route.params.occurrence_id + '/action_log'
            );
        },
    },
    created: function () {
        if (!this.occurrence) {
            this.fetchOccurrence();
        }
    },
    updated: function () {
        let vm = this;
        this.$nextTick(() => {
            vm.form = document.forms.occurrence;
        });
    },
    methods: {
        save: async function () {
            let vm = this;

            console.log(vm.occurrence);

            var missing_data = vm.can_submit('');
            vm.isSaved = false;
            if (missing_data != true) {
                swal.fire({
                    title: 'Please fix following errors before saving',
                    text: missing_data.toString().replace(',', ', '),
                    icon: 'error',
                    customClass: {
                        confirmButton: 'btn btn-primary',
                    },
                });
                return false;
            }
            vm.savingOccurrence = true;

            // add map geometry to the occurrence
            if (vm.$refs.occurrence.$refs.occ_location.$refs.component_map) {
                vm.$refs.occurrence.$refs.occ_location.$refs.component_map.setLoadingMap(
                    true
                );
                const occ_geometry =
                    vm.$refs.occurrence.$refs.occ_location.OccGeometryFromMap();
                vm.occurrence.occ_geometry = JSON.stringify(occ_geometry);
                vm.occurrence.site_geometry =
                    vm.$refs.occurrence.$refs.occ_location.$refs.component_map.getJSONFeatures(
                        'site_layer'
                    );
            }

            let payload = new Object();
            Object.assign(payload, vm.occurrence);
            await fetch(vm.occurrence_form_url, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(payload),
            }).then(async (response) => {
                const data = await response.json();
                if (!response.ok) {
                    swal.fire({
                        title: 'Save Error',
                        text: JSON.stringify(data),
                        icon: 'error',
                        customClass: {
                            confirmButton: 'btn btn-primary',
                        },
                    });
                    vm.savingOccurrence = false;
                    vm.isSaved = false;
                    vm.$refs.occurrence.$refs.occ_location.$refs.component_map.setLoadingMap(
                        false
                    );
                    return;
                }
                swal.fire({
                    title: 'Saved',
                    text: 'Your changes have been saved',
                    icon: 'success',
                    customClass: {
                        confirmButton: 'btn btn-primary',
                    },
                });
                vm.savingOccurrence = false;
                vm.isSaved = true;

                // Update the occurrence object with the response data
                vm.original_occurrence = helpers.copyObject(data);
                vm.occurrence = helpers.copyObject(data);
                vm.combine_key++;

                vm.$refs.occurrence.$refs.occ_location.$refs.component_map.setLoadingMap(
                    false
                );
                vm.$refs.occurrence.$refs.occ_location.incrementComponentMapKey();
                vm.$refs.occurrence.$refs.occ_location.refreshDatatables();
            });
        },
        save_exit: async function () {
            let vm = this;
            var missing_data = vm.can_submit('');
            if (missing_data != true) {
                swal.fire({
                    title: 'Please fix following errors before saving',
                    text: missing_data.toString().replace(',', ', '),
                    icon: 'error',
                    customClass: {
                        confirmButton: 'btn btn-primary',
                    },
                });
                //vm.paySubmitting=false;
                return false;
            }
            vm.saveExitOccurrence = true;
            await vm.save().then(() => {
                if (vm.isSaved === true) {
                    vm.$router.push({
                        name: 'internal-occurrence-dash',
                    });
                } else {
                    vm.saveExitOccurrence = false;
                }
            });
        },
        save_before_submit: async function () {
            let vm = this;
            vm.saveError = false;

            let payload = new Object();
            Object.assign(payload, vm.occurrence);
            const result = await fetch(vm.occurrence_form_url, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(payload),
            }).then(
                async () => {
                    //return true;
                },
                (err) => {
                    var errorText = helpers.apiVueResourceError(err);
                    swal.fire({
                        title: 'Submit Error',
                        //helpers.apiVueResourceError(err),
                        text: errorText,
                        icon: 'error',
                        customClass: {
                            confirmButton: 'btn btn-primary',
                        },
                    });
                    vm.submitOccurrence = false;
                    vm.saveError = true;
                    //return false;
                }
            );
            return result;
        },
        can_submit: function () {
            let vm = this;
            let blank_fields = [];
            if (!vm.occurrence.occurrence_name) {
                blank_fields.push('Occurrence Name is missing');
            }
            if (
                vm.occurrence.group_type == 'flora' ||
                vm.occurrence.group_type == 'fauna'
            ) {
                if (
                    vm.occurrence.species == null ||
                    vm.occurrence.species == ''
                ) {
                    blank_fields.push('Scientific Name is missing');
                }
            } else {
                if (
                    vm.occurrence.community == null ||
                    vm.occurrence.community == ''
                ) {
                    blank_fields.push('Community Name is missing');
                }
            }
            if (blank_fields.length == 0) {
                return true;
            } else {
                return blank_fields;
            }
        },
        submit: async function () {
            let vm = this;

            var missing_data = vm.can_submit('submit');
            missing_data = missing_data.replace(',', ', ');
            if (missing_data != true) {
                swal.fire({
                    title: 'Please fix following errors before submitting',
                    text: missing_data.toString().replace(',', ', '),
                    icon: 'error',
                    customClass: {
                        confirmButton: 'btn btn-primary',
                    },
                });
                //vm.paySubmitting=false;
                return false;
            }

            vm.submitOccurrence = true;
            swal.fire({
                title: 'Submit Occurrence',
                text: 'Are you sure you want to submit this Occurrence?',
                icon: 'question',
                showCancelButton: true,
                confirmButtonText: 'submit',
                customClass: {
                    confirmButton: 'btn btn-primary',
                    cancelButton: 'btn btn-secondary',
                },
                reverseButtons: true,
            }).then(
                async (swalresult) => {
                    if (swalresult.isConfirmed) {
                        await vm.save_before_submit();
                        if (!vm.saveError) {
                            let payload = new Object();
                            Object.assign(payload, vm.occurrence);
                            const submit_url = helpers.add_endpoint_json(
                                api_endpoints.occurrence,
                                vm.occurrence.id + '/submit'
                            );
                            fetch(submit_url, {
                                method: 'POST',
                                headers: {
                                    'Content-Type': 'application/json',
                                },
                                body: JSON.stringify(payload),
                            }).then(
                                async (response) => {
                                    vm.occurrence = await response.json();
                                    vm.$router.push({
                                        name: 'internal-occurrence-dash',
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
                        }
                    }
                },
                () => {
                    vm.submitOccurrence = false;
                }
            );
        },
        returnToDashboard: function () {
            let vm = this;
            vm.$router.push({
                name: 'internal-occurrence-dash',
            });
        },
        refreshFromResponse: async function (response) {
            let vm = this;
            const data = await response.json();
            vm.original_occurrence = helpers.copyObject(data);
            vm.occurrence = helpers.copyObject(data);
            vm.combine_key++;
        },
        activateOccurrence: async function () {
            await fetch(`/api/occurrence/${this.occurrence.id}/activate.json`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
            }).then(async (response) => {
                if (!response.ok) {
                    const data = await response.json();
                    swal.fire({
                        title: 'Activate Error',
                        text: data,
                        icon: 'error',
                        customClass: {
                            confirmButton: 'btn btn-primary',
                        },
                    });
                    return;
                }
                swal.fire({
                    title: 'Activated',
                    text: 'Occurrence has been Activated',
                    icon: 'success',
                    customClass: {
                        confirmButton: 'btn btn-primary',
                    },
                }).then(async () => {
                    this.$router.go(this.$router.currentRoute);
                });
            });
        },
        lockOccurrence: async function () {
            await fetch(
                `/api/occurrence/${this.occurrence.id}/lock_occurrence.json`,
                {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                }
            ).then(
                async () => {
                    swal.fire({
                        title: 'Locked',
                        text: 'Occurrence has been Locked',
                        icon: 'success',
                        customClass: {
                            confirmButton: 'btn btn-primary',
                        },
                    }).then(async () => {
                        this.$router.go(this.$router.currentRoute);
                    });
                },
                (err) => {
                    var errorText = helpers.apiVueResourceError(err);
                    swal.fire({
                        title: 'Lock Error',
                        text: errorText,
                        icon: 'error',
                        customClass: {
                            confirmButton: 'btn btn-primary',
                        },
                    });
                }
            );
        },
        unlockOccurrence: async function () {
            await fetch(
                `/api/occurrence/${this.occurrence.id}/unlock_occurrence.json`,
                {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                }
            ).then(
                async () => {
                    swal.fire({
                        title: 'Unlocked',
                        text: 'Occurrence has been Unlocked',
                        icon: 'success',
                        customClass: {
                            confirmButton: 'btn btn-primary',
                        },
                    }).then(async () => {
                        this.$router.go(this.$router.currentRoute);
                    });
                },
                (err) => {
                    var errorText = helpers.apiVueResourceError(err);
                    swal.fire({
                        title: 'Unlock Error',
                        text: errorText,
                        icon: 'error',
                        customClass: {
                            confirmButton: 'btn btn-primary',
                        },
                    });
                }
            );
        },
        closeOccurrence: async function () {
            let vm = this;
            swal.fire({
                title: 'Close',
                text: 'Are you sure you want to close this Occurrence?',
                icon: 'question',
                showCancelButton: true,
                confirmButtonText: 'Close Occurrence',
                customClass: {
                    confirmButton: 'btn btn-primary',
                    cancelButton: 'btn btn-secondary',
                },
                reverseButtons: true,
            }).then(async (swalresult) => {
                if (swalresult.isConfirmed) {
                    await fetch(
                        `/api/occurrence/${this.occurrence.id}/close_occurrence.json`,
                        {
                            method: 'POST',
                            headers: {
                                'Content-Type': 'application/json',
                            },
                        }
                    ).then(
                        async () => {
                            swal.fire({
                                title: 'Closed',
                                text: 'Occurrence has been Closed',
                                icon: 'success',
                                customClass: {
                                    confirmButton: 'btn btn-primary',
                                },
                            }).then(async () => {
                                vm.$router.push({
                                    name: 'internal-occurrence-dash',
                                });
                            });
                        },
                        (err) => {
                            var errorText = helpers.apiVueResourceError(err);
                            swal.fire({
                                title: 'Close Error',
                                text: errorText,
                                icon: 'error',
                                customClass: {
                                    confirmButton: 'btn btn-primary',
                                },
                            });
                        }
                    );
                }
            });
        },
        reopenOccurrence: async function () {
            swal.fire({
                title: 'Reopen',
                text: 'Are you sure you want to reopen this Occurrence?',
                icon: 'question',
                showCancelButton: true,
                confirmButtonText: 'Reopen Occurrence',
                customClass: {
                    confirmButton: 'btn btn-primary',
                    cancelButton: 'btn btn-secondary',
                },
                reverseButtons: true,
            }).then(async (swalresult) => {
                if (swalresult.isConfirmed) {
                    await fetch(
                        `/api/occurrence/${this.occurrence.id}/reopen_occurrence.json`,
                        {
                            method: 'POST',
                            headers: {
                                'Content-Type': 'application/json',
                            },
                        }
                    ).then(
                        async () => {
                            swal.fire({
                                title: 'Reopened',
                                text: 'Occurrence has been Reopened',
                                icon: 'success',
                                customClass: {
                                    confirmButton: 'btn btn-primary',
                                },
                            }).then(async () => {
                                this.$router.go(this.$router.currentRoute);
                            });
                        },
                        (err) => {
                            var errorText = helpers.apiVueResourceError(err);
                            swal.fire({
                                title: 'Reopen Error',
                                text: errorText,
                                icon: 'error',
                                customClass: {
                                    confirmButton: 'btn btn-primary',
                                },
                            });
                        }
                    );
                }
            });
        },
        splitOccurrence: async function () {
            //this.$refs.occurrence_split.isModalOpen = true;
        },
        combineOccurrence: async function () {
            this.$refs.occurrence_combine.isModalOpen = true;
        },
        fetchOccurrence: function () {
            let vm = this;
            fetch(`/api/occurrence/${this.$route.params.occurrence_id}/`).then(
                async (response) => {
                    vm.occurrence = await response.json();
                },
                (err) => {
                    console.log(err);
                }
            );
        },
    },
};
</script>
