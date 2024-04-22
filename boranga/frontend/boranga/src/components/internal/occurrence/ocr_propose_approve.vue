<template lang="html">
    <div id="internal-ocr-propose-approve-request">
        <modal id="myModal" transition="modal fade" @ok="ok()" ok-text="Propose Approve" @cancel="close()"
            :title="`Propose Approve ${occurrence_report_number}`" large>
            <div class="container">
                <form id="propose-approve-form">
                    <div class="row mb-3">
                        <div class="col">
                            <div class="form-check form-check-inline">
                                <input class="form-check-input" type="radio" name="create_new_occurrence"
                                    id="create_new_occurrence_new" :value="true"
                                    v-model="propose_approve.create_new_occurrence" @change="resetSelectedOccurrence" />
                                <label class="form-check-label" for="create_new_occurrence_new">Create New
                                    Occurrence</label>
                            </div>
                            <div class="form-check form-check-inline">
                                <input class="form-check-input" type="radio" name="create_new_occurrence"
                                    id="create_new_occurrence_existing" :value="false"
                                    v-model="propose_approve.create_new_occurrence"
                                    @change="reinitialiseOccurrenceNameLookup" />
                                <label class="form-check-label" for="create_new_occurrence_existing">Add to Existing
                                    Occurrence</label>
                            </div>
                            <hr />
                            <div v-if="!propose_approve.create_new_occurrence" class="mt-3">
                                <div class="form-group" id="occurrence_name_lookup_propose_approve_form_group_id">
                                    <label class="mb-3" for="occurrence_name_lookup_propose_approve">Existing
                                        Occurrence:</label>
                                    <select id="occurrence_name_lookup_propose_approve"
                                        name="occurrence_name_lookup_propose_approve"
                                        ref="occurrence_name_lookup_propose_approve" class="form-control" required />
                                </div>
                            </div>
                            <div class="mt-3">
                                <label class="form-label" for="effective_from_date">Effective From</label>
                                <input type="date" class="form-control" id="effective_from_date" name="effective_from_date"
                                    v-model="propose_approve.effective_from_date" required />
                            </div>
                            <div class="mt-3">
                                <label class="form-label" for="effective_to_date">Effective To</label>
                                <input type="date" class="form-control" id="effective_to_date" name="effective_to_date"
                                    v-model="propose_approve.effective_to_date" required />
                            </div>
                            <div class="mt-3">
                                <label class="form-label" for="details">Details for Approver</label>
                                <textarea type="date" class="form-control" id="details" name="details"
                                    v-model="propose_approve.details" required></textarea>
                            </div>
                            <div class="mt-3">
                                some blurb to let the user know to go through the report and add sections to the
                                occurrence.
                            </div>
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
    name: 'ocr-propose-approve',
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
    },
    data: function () {
        return {
            isModalOpen: false,
            form: null,
            propose_approve: {
                occurrence_id: null,
                occurrence_name: '',
                create_new_occurrence: false,
                effective_from_date: '',
                effective_to_date: '',
                details: '',
            },
            errorString: '',
        }
    },
    watch: {
        isModalOpen: function (value) {
            if (value) {
                this.$nextTick(() => {
                    $(this.$refs.occurrence_name_lookup_propose_approve).select2('open');
                });
            }
        }
    },
    computed: {
        proposeApproveButtonDisabled: function () {
            return !this.propose_approve.create_new_occurrence && !this.propose_approve.occurrence;
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
            this.propose_approve = {
                occurrence_id: null,
                occurrence_name: '',
                create_new_occurrence: false,
                effective_from_date: '',
                effective_to_date: '',
                details: '',
                occurrence_report: this.occurrence_report_id
            };
            this.errorString = '';
            this.form.reset();
        },
        proposeApprove: function () {
            let vm = this;
            let confirmation = `Are you sure you want to propose to approve occurrence report ${vm.occurrence_report_number}`;
            if (this.propose_approve.create_new_occurrence) {
                confirmation += ` (and propose to create a new occurrence based on it)?`;
            } else {
                confirmation += ` (and propose to add it to the existing occurrence ${vm.propose_approve.occurrence_name})?`;
            }
            swal.fire({
                title: `Propose Approve Occurrence Report ${vm.occurrence_report_number}`,
                text: confirmation,
                icon: "question",
                showCancelButton: true,
                confirmButtonText: 'Propose Approve',
                confirmButtonColor: '#d9534f',
                reverseButtons: true,
                buttonsStyling: false,
                customClass: {
                    confirmButton: 'btn btn-primary',
                    cancelButton: 'btn btn-secondary me-2',
                },
            }).then((swalresult) => {
                if (swalresult.isConfirmed) {
                    vm.$http.post(helpers.add_endpoint_join(api_endpoints.occurrence_report, '/' + (vm.occurrence_report_id + '/propose_approve/')), JSON.stringify(vm.propose_approve))
                        .then((response) => {
                            swal.fire({
                                title: 'Proposal to Approve Successful',
                                text: `Your proposal to approve occurrence report ${vm.occurrence_report_number} has been succuessfully submitted.`,
                                icon: 'success',
                                confirmButtonColor: '#226fbb',
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
            this.propose_approve.occurrence_id = null;
            this.propose_approve.occurrence_name = '';
        },
        reinitialiseOccurrenceNameLookup: function () {
            let vm = this;
            vm.$nextTick(() => {
                $(vm.$refs.occurrence_name_lookup_propose_approve).select2('destroy');
                vm.initialiseOccurrenceNameLookup();
            });
        },
        initialiseOccurrenceNameLookup: function () {
            let vm = this;
            $(vm.$refs.occurrence_name_lookup_propose_approve).select2({
                width: '100%',
                minimumInputLength: 2,
                dropdownParent: $("#occurrence_name_lookup_propose_approve_form_group_id"),
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
                    vm.propose_approve.occurrence_id = e.params.data.id;
                    vm.propose_approve.occurrence_name = e.params.data.text;
                }).
                on("select2:open", function (e) {
                    const searchField = $('[aria-controls="select2-occurrence_name_lookup_propose_approve-results"]')
                    searchField[0].focus();
                }).
                on("select2:unselect", function (e) {
                    vm.propose_approve.occurrence_id = null;
                    vm.propose_approve.occurrence_name = null;
                });
        },
    },
    mounted: function () {
        this.form = document.forms['propose-approve-form'];
        this.initialiseOccurrenceNameLookup();
    }
}
</script>
