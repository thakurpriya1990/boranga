<template lang="html">
    <div id="internal-ocr-approve-request">
        <modal
            id="ocr-approve-modal"
            transition="modal fade"
            ok-text="Approve"
            :title="`Approve ${occurrence_report_number}`"
            large
            @ok="ok()"
            @cancel="close()"
        >
            <div class="container">
                <form id="approve-form">
                    <div
                        v-if="approval_details.occurrence"
                        class="row mb-3 border-bottom"
                    >
                        <label
                            for="occurrence"
                            class="col-sm-4 col-form-label fw-bold"
                            >Add to Existing Occurrence</label
                        >
                        <div class="col-sm-8">
                            <span class="badge bg-primary fs-6 p-2">
                                {{ approval_details.occurrence_number }} -
                                {{ approval_details.occurrence_name }}
                            </span>
                        </div>
                    </div>
                    <template v-else>
                        <div class="row mb-3 border-bottom">
                            <label
                                for="create_new_occurrence"
                                class="col-sm-4 col-form-label fw-bold"
                                >New Occurrence Name</label
                            >
                            <div class="col-sm-8 d-flex align-items-center">
                                {{ approval_details.new_occurrence_name }}
                            </div>
                        </div>
                    </template>

                    <div class="row mb-3 border-bottom">
                        <label
                            for="proposed_by"
                            class="col-sm-4 col-form-label fw-bold"
                            >Proposed By</label
                        >
                        <div class="col-sm-8 d-flex align-items-center">
                            {{ approval_details.officer_name }}
                        </div>
                    </div>

                    <div class="row mb-3 border-bottom">
                        <label
                            for="details_from_assessor"
                            class="col-sm-4 col-form-label fw-bold"
                            >Details from Assessor</label
                        >
                        <div class="col-sm-8 d-flex align-items-center">
                            {{ approval_details.details }}
                        </div>
                    </div>

                    <div class="row mb-3 border-bottom">
                        <label
                            for="details_from_assessor"
                            class="col-sm-4 col-form-label fw-bold"
                            >Copy Occurrence Report Comments to
                            Occurrence?</label
                        >
                        <div class="col-sm-8 d-flex align-items-center">
                            <i
                                class="bi bi-check-lg h4 text-success"
                                v-if="
                                    approval_details.copy_ocr_comments_to_occ_comments
                                "
                            ></i>
                            <i class="bi bi-x-lg h4 text-error" v-else></i>
                        </div>
                    </div>

                    <div class="row">
                        <label
                            class="col-sm-4 col-form-label fw-bold"
                            for="cc_email"
                            >CC email</label
                        >
                        <div class="col-sm-8">
                            {{ approval_details.cc_email }}
                        </div>
                    </div>
                </form>
            </div>
        </modal>
    </div>
</template>

<script>
import modal from '@vue-utils/bootstrap-modal.vue';

import { helpers, api_endpoints } from '@/utils/hooks.js';
export default {
    name: 'OcrApprove',
    components: {
        modal,
    },
    props: {
        occurrence_report_id: {
            type: Number,
        },
        occurrence_report_number: {
            type: String,
        },
        group_type_id: {
            type: Number,
        },
        approval_details: {
            type: Object,
        },
    },
    data: function () {
        return {
            isModalOpen: false,
            form: null,
            errorString: '',
        };
    },
    computed: {
        proposeApproveButtonDisabled: function () {
            return (
                !this.approve.create_new_occurrence && !this.approve.occurrence
            );
        },
    },
    watch: {
        isModalOpen: function (value) {
            if (value) {
                this.$nextTick(() => {
                    $(this.$refs.occurrence_name_lookup_approve).select2(
                        'open'
                    );
                });
            }
        },
    },
    mounted: function () {
        this.form = document.forms['approve-form'];
        this.initialiseOccurrenceNameLookup();
    },
    methods: {
        ok: function () {
            let vm = this;
            if (vm.form.checkValidity()) {
                vm.proposeApprove();
            } else {
                vm.form.reportValidity();
            }
        },
        close: function () {
            this.isModalOpen = false;
            this.errorString = '';
        },
        proposeApprove: function () {
            let vm = this;
            let confirmation = `Are you sure you want to approve occurrence report ${vm.occurrence_report_number}`;
            if (!this.approval_details.occurrence) {
                confirmation += ` (and create a new occurrence based on it)?`;
            } else {
                confirmation += ` (and add it to the existing occurrence ${vm.approval_details.occurrence_name})?`;
            }
            swal.fire({
                title: `Approve Occurrence Report ${vm.occurrence_report_number}`,
                text: confirmation,
                icon: 'question',
                showCancelButton: true,
                confirmButtonText: 'Approve',
                customClass: {
                    confirmButton: 'btn btn-primary',
                    cancelButton: 'btn btn-secondary me-2',
                },
                reverseButtons: true,
            }).then((swalresult) => {
                if (swalresult.isConfirmed) {
                    fetch(
                        helpers.add_endpoint_join(
                            api_endpoints.occurrence_report,
                            '/' + (vm.occurrence_report_id + '/approve/')
                        ),
                        {
                            method: 'POST',
                            headers: {
                                'Content-Type': 'application/json',
                            },
                            body: JSON.stringify(vm.approve),
                        }
                    ).then(
                        () => {
                            swal.fire({
                                title: 'Occurrence Report Successfully Approved',
                                text: `Occurrence Report: ${vm.occurrence_report_number} has been successfully approved.`,
                                icon: 'success',
                                customClass: {
                                    confirmButton: 'btn btn-primary',
                                },
                            });
                            vm.$router.push({
                                name: 'internal-occurrence-dash',
                            });
                        },
                        (error) => {
                            console.log(error);
                            vm.errorString = helpers.apiVueResourceError(error);
                            vm.amendingProposal = true;
                        }
                    );
                }
            });
        },
        resetSelectedOccurrence: function () {
            this.approve.occurrence_id = null;
            this.approve.occurrence_name = '';
        },
        reinitialiseOccurrenceNameLookup: function () {
            let vm = this;
            vm.$nextTick(() => {
                $(vm.$refs.occurrence_name_lookup_approve).select2('destroy');
                vm.initialiseOccurrenceNameLookup();
            });
        },
        initialiseOccurrenceNameLookup: function () {
            let vm = this;
            $(vm.$refs.occurrence_name_lookup_approve)
                .select2({
                    width: '100%',
                    minimumInputLength: 2,
                    dropdownParent: $(
                        '#occurrence_name_lookup_approve_form_group_id'
                    ),
                    theme: 'bootstrap-5',
                    allowClear: true,
                    placeholder: 'Search Name of Occurrence',
                    ajax: {
                        url: api_endpoints.occurrence_name_lookup,
                        dataType: 'json',
                        data: function (params) {
                            var query = {
                                term: params.term,
                                type: 'public',
                                group_type_id: vm.group_type_id,
                            };
                            return query;
                        },
                    },
                })
                .on('select2:select', function (e) {
                    vm.approve.occurrence_id = e.params.data.id;
                    vm.approve.occurrence_name = e.params.data.text;
                })
                .on('select2:open', function () {
                    const searchField = $(
                        '[aria-controls="select2-occurrence_name_lookup_approve-results"]'
                    );
                    searchField[0].focus();
                })
                .on('select2:unselect', function () {
                    vm.approve.occurrence_id = null;
                    vm.approve.occurrence_name = null;
                });
        },
    },
};
</script>
