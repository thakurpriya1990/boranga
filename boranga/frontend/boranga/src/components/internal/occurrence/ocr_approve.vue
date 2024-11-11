<template lang="html">
    <div id="internal-ocr-approve-request">
        <modal id="ocr-approve-modal" transition="modal fade" @ok="ok()" ok-text="Approve" @cancel="close()"
            :title="`Approve ${occurrence_report_number}`" large>
            <div class="container">
                <form id="approve-form">

                    <div v-if="approval_details.occurrence" class="mb-3 row">
                        <label for="occurrence" class="col-sm-4 col-form-label">Add to Existing
                            Occurrence</label>
                        <div class="col-sm-8">
                            <span class="badge bg-primary fs-6 p-2">
                                {{ approval_details.occurrence_number }} -
                                {{ approval_details.occurrence_name }}
                            </span>
                        </div>
                    </div>
                    <template v-else>
                        <div class="mb-3 row">
                            <label for="create_new_occurrence" class="col-sm-4 col-form-label">New Occurrence
                                Name</label>
                            <div class="col-sm-8">
                                <input type="text" readonly class="form-control-plaintext" id="proposed_by"
                                    :value="approval_details.new_occurrence_name">
                            </div>
                        </div>
                    </template>

                    <div class="mb-3 row">
                        <label for="proposed_by" class="col-sm-4 col-form-label">Proposed By</label>
                        <div class="col-sm-8">
                            <input type="text" readonly class="form-control-plaintext" id="proposed_by"
                                :value="approval_details.officer_name">
                        </div>
                    </div>

                    <div class="mb-3 row">
                        <label for="details_from_assessor" class="col-sm-4 col-form-label">Details from Assessor</label>
                        <div class="col-sm-8">
                            <input type="text" readonly class="form-control-plaintext" id="details_from_assessor"
                                v-model="approval_details.details">
                        </div>
                    </div>

                </form>
            </div>
        </modal>
    </div>
</template>

<script>
import modal from '@vue-utils/bootstrap-modal.vue'
import alert from '@vue-utils/alert.vue'

import { helpers, api_endpoints } from "@/utils/hooks.js"
export default {
    name: 'ocr-approve',
    components: {
        modal,
        alert,
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
        }
    },
    data: function () {
        return {
            isModalOpen: false,
            form: null,
            errorString: '',
        }
    },
    watch: {
        isModalOpen: function (value) {
            if (value) {
                this.$nextTick(() => {
                    $(this.$refs.occurrence_name_lookup_approve).select2('open');
                });
            }
        }
    },
    computed: {
        proposeApproveButtonDisabled: function () {
            return !this.approve.create_new_occurrence && !this.approve.occurrence;
        },
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
                icon: "question",
                showCancelButton: true,
                confirmButtonText: 'Approve',
                customClass: {
                    confirmButton: 'btn btn-primary',
                    cancelButton: 'btn btn-secondary me-2',
                },
                reverseButtons: true,
            }).then((swalresult) => {
                if (swalresult.isConfirmed) {
                    vm.$http.post(helpers.add_endpoint_join(api_endpoints.occurrence_report, '/' + (vm.occurrence_report_id + '/approve/')), JSON.stringify(vm.approve))
                        .then((response) => {
                            swal.fire({
                                title: 'Occurrence Report Successfully Approved',
                                text: `Occurrence Report: ${vm.occurrence_report_number} has been successfully approved.`,
                                icon: 'success',
                                customClass: {
                                    confirmButton: 'btn btn-primary',
                                },
                            });
                            vm.$router.push({
                                name: 'internal-occurrence-dash'
                            });
                        }, (error) => {
                            console.log(error);
                            vm.errorString = helpers.apiVueResourceError(error);
                            vm.amendingProposal = true;
                        });
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
            $(vm.$refs.occurrence_name_lookup_approve).select2({
                width: '100%',
                minimumInputLength: 2,
                dropdownParent: $("#occurrence_name_lookup_approve_form_group_id"),
                theme: 'bootstrap-5',
                allowClear: true,
                placeholder: "Search Name of Occurrence",
                ajax: {
                    url: api_endpoints.occurrence_name_lookup,
                    dataType: 'json',
                    data: function (params) {
                        var query = {
                            term: params.term,
                            type: 'public',
                            group_type_id: vm.group_type_id,
                        }
                        return query;
                    },
                },
            }).
                on("select2:select", function (e) {
                    vm.approve.occurrence_id = e.params.data.id;
                    vm.approve.occurrence_name = e.params.data.text;
                }).
                on("select2:open", function (e) {
                    const searchField = $('[aria-controls="select2-occurrence_name_lookup_approve-results"]')
                    searchField[0].focus();
                }).
                on("select2:unselect", function (e) {
                    vm.approve.occurrence_id = null;
                    vm.approve.occurrence_name = null;
                });
        },
    },
    mounted: function () {
        this.form = document.forms['approve-form'];
        this.initialiseOccurrenceNameLookup();
    }
}
</script>
