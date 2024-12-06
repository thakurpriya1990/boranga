<template lang="html">
    <div id="proposedIssuanceApproval">
        <modal transition="modal fade" @ok="ok()" @cancel="cancel()" :title="title" large>
            <div class="container-fluid">
                <div class="row">
                    <form class="form-horizontal" name="approvalForm">
                        <alert v-if="showError" type="danger"><strong>{{ errorString }}</strong></alert>
                        <alert type="danger" v-if="!isEffectiveDateValid"><strong>Please select Effective To Date that
                                is after Effective From Date</strong></alert>
                        <div class="col-sm-12">
                            <div class="form-group">
                                <div class="row mb-3">
                                    <div class="col-sm-4">
                                        <label class="control-label pull-left" for="Name">Effective From Date</label>
                                    </div>
                                    <div class="col-sm-8">
                                        <div class="input-group date" style="width: 70%;">
                                            <input type="date" class="form-control" ref="start_date"
                                                v-model="approval.effective_from_date">
                                        </div>
                                        <small style="color: red;" v-show="showstartDateError">This field is
                                            required</small>
                                    </div>
                                </div>
                            </div>
                            <div class="form-group">
                                <div class="row mb-3">
                                    <div class="col-sm-4">
                                        <label class="control-label pull-left" for="Name">Details</label>
                                    </div>
                                    <div class="col-sm-8">
                                        <textarea name="approval_details" ref="approval_details" class="form-control"
                                            style="width:70%;" v-model="approval.details"
                                            @blur="validateDetails($event)"></textarea>
                                        <small style="color: red;" v-show="showDetailsError">This field is
                                            required</small>
                                    </div>
                                </div>
                            </div>
                            <div class="form-group">
                                <div class="row mb-3">
                                    <div class="col-sm-4">
                                        <label class="control-label pull-left" for="Name">CC email</label>
                                    </div>
                                    <div class="col-sm-8">
                                        <input type="text" class="form-control" name="approval_cc" style="width:70%;"
                                            v-model="approval.cc_email">
                                    </div>
                                </div>
                            </div>
                            <div class="form-group"
                                v-if="processing_status == 'With Assessor' || processing_status == 'On Agenda'">
                                <div class="row mb-3">
                                    <div class="col-sm-4">
                                        <label class="control-label pull-left">Approval Document</label>
                                    </div>
                                    <div class="col-sm-8">
                                        <FileField2 ref="filefield" :proposal_id="conservation_status_id"
                                            :isRepeatable="false" name="cs_approval_file" />
                                    </div>
                                </div>
                            </div>
                        </div>
                    </form>
                </div>
            </div>
            <div slot="footer">
                <button type="button" class="btn btn-secondary me-2" @click="cancel">Cancel</button>
                <button type="button" v-if="issuingApproval" disabled class="btn btn-primary" @click="ok">Processing
                    <span class="spinner-border spinner-border-sm" role="status" aria-hidden="true"></span>
                    <span class="visually-hidden">Loading...</span></button>
                <button type="button" v-else class="btn btn-primary" @click="ok">{{ ok_button_text }}</button>
            </div>
        </modal>
    </div>
</template>

<script>

import modal from '@vue-utils/bootstrap-modal.vue'
import alert from '@vue-utils/alert.vue'
import FileField2 from '@/components/forms/filefield.vue'
import { helpers, api_endpoints } from "@/utils/hooks.js"
export default {
    name: 'Proposed-Approval',
    components: {
        modal,
        alert,
        FileField2,
    },
    props: {
        conservation_status_id: {
            type: Number,
            required: true
        },
        processing_status: {
            type: String,
            required: true
        },
    },
    data: function () {
        return {
            isModalOpen: false,
            approval: {
                'effective_from_date': new Date().toISOString().slice(0, 10),
            },
            uploadedFile: null,
            state: 'proposed_approval',
            issuingApproval: false,
            validation_form: null,
            errors: false,
            showtoDateError: false,
            showstartDateError: false,
            showDetailsError: false,
            errorString: '',
            successString: '',
            success: false,
            datepickerOptions: {
                format: 'DD/MM/YYYY',
                showClear: true,
                useCurrent: false,
                keepInvalid: true,
                allowInputToggle: true
            },
        }
    },
    watch: {
        isModalOpen: function (val) {
            if (val) {
                this.$nextTick(() => {
                    this.$refs.start_date.focus();
                });
            }
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
        isEffectiveDateValid: function () {
            if (this.approval.effective_from_date && this.approval.effective_to_date) {
                const fromDate = new Date(this.approval.effective_from_date);
                const toDate = new Date(this.approval.effective_to_date);
                return fromDate < toDate;
            }
            else {
                return true;
            }
        },
        ok_button_text: function () {
            if (this.state == 'proposed_approval') {
                return 'Propose to Approve';
            }
            return 'Approve';
        },
        title: function () {
            if (this.state == 'proposed_approval') {
                return `Propose to Approve Conservation Status CS${this.conservation_status_id}`;
            }
            return `Approve Conservation Status CS${this.conservation_status_id}`;
        },
        can_preview: function () {
            return (this.processing_status == 'Proposed DeListed' || 'With Assessor (Requirements)') && this.approval.effective_from_date && this.approval.effective_to_date ? true : false;
        },
    },
    methods: {
        ok: function () {
            let vm = this;
            let errors = vm.isError();
            if (!errors && vm.isEffectiveDateValid) {
                vm.sendData();
            }
        },
        cancel: function () {
            this.close()
        },
        close: function () {
            this.isModalOpen = false;
            this.approval = {
                'effective_from_date': new Date().toISOString().slice(0, 10),
            };
            this.errors = false;
        },
        sendData: function () {
            let vm = this;
            vm.errors = false;
            let approval = JSON.parse(JSON.stringify(vm.approval));
            vm.issuingApproval = true;
            if (vm.state == 'proposed_approval') {
                fetch(helpers.add_endpoint_json(api_endpoints.conservation_status, vm.conservation_status_id + '/proposed_approval'), {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify(approval)
                }).then((response) => {
                    vm.issuingApproval = false;
                    vm.close();
                    vm.$emit('refreshFromResponse', response);
                    vm.$router.push({ path: '/internal/conservation-status/' }); //Navigate to dashboard page after Propose issue.
                }, (error) => {
                    vm.errors = true;
                    vm.issuingApproval = false;
                    vm.errorString = helpers.apiVueResourceError(error);
                });
            }
            else if (vm.state == 'final_approval') {
                let formData = new FormData()
                var files = vm.$refs.filefield.files;
                vm.uploadedFile = files.length > 0 ? files[0].file : null;
                formData.append('proposal_approval_document', vm.uploadedFile)
                formData.append('data', JSON.stringify(approval));

                fetch(helpers.add_endpoint_json(api_endpoints.conservation_status, vm.conservation_status_id + '/final_approval'), {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: formData
                }).then((response) => {
                    vm.issuingApproval = false;
                    vm.close();
                    vm.$emit('refreshFromResponse', response);
                }, (error) => {
                    vm.errors = true;
                    vm.issuingApproval = false;
                    vm.errorString = helpers.apiVueResourceError(error);
                });
            }
        },
        validateEffectiveFromDate: function (event) {
            let vm = this;
            const value = event.target.value;
            if (!value) {
                vm.showstartDateError = true;
            }
            else {
                vm.showstartDateError = false;
            }
        },
        validateDetails: function (event) {
            let vm = this;
            const value = event.target.value;
            if (!value) {
                vm.showDetailsError = true;
            }
            else {
                vm.showDetailsError = false;
            }
        },
        isError: function () {
            let vm = this;
            let hasError = false;
            if (!vm.approval.effective_from_date) {
                vm.showstartDateError = true;
                hasError = true;
            }
            if (!vm.approval.details || vm.approval.details == "") {
                vm.showDetailsError = true;
                hasError = true;
            }
            return hasError;
        },
    },
}
</script>
