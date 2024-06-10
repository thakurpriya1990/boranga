<template lang="html">
    <div id="observerDetail">
        <modal transition="modal fade" @ok="ok()" @cancel="cancel()" :title="title" large>
            <div class="container-fluid">
                <div class="row">
                    <form class="form-horizontal needs-validation" name="observerDetailForm" novalidate>
                        <alert :show.sync="showError" type="danger"><strong>{{ errorString }}</strong></alert>
                        <div class="col-sm-12">
                            <div class="form-group">
                                <div class="row modal-input-row mb-3">
                                    <div class="col-sm-3">
                                        <label class="control-label pull-left">Name</label>
                                    </div>
                                    <div class="col-sm-9">
                                        <input type="text" class="form-control" :disabled="isReadOnly"
                                            v-model="observerObj.observer_name" ref="observer_name" required />
                                    </div>
                                </div>
                                <div class="row mb-3">
                                    <div class="col-sm-3">
                                        <label class="control-label pull-left">Role</label>
                                    </div>
                                    <div class="col-sm-9">
                                        <input type="text" class="form-control" :disabled="isReadOnly"
                                            v-model="observerObj.role" />
                                    </div>
                                </div>
                                <div class="row mb-3">
                                    <div class="col-sm-3">
                                        <label class="control-label pull-left">Contact Details</label>
                                    </div>
                                    <div class="col-sm-9">
                                        <textarea class="form-control" id="contact_details"
                                            v-model="observerObj.contact" rows="4" />
                                    </div>
                                </div>
                                <div class="row mb-3">
                                    <div class="col-sm-3">
                                        <label class="control-label pull-left">Organisation</label>
                                    </div>
                                    <div class="col-sm-9">
                                        <input type="text" class="form-control" :disabled="isReadOnly"
                                            v-model="observerObj.organisation" />
                                    </div>
                                </div>
                                <div class="row mb-3">
                                    <div class="col-sm-3">
                                        <label class="control-label pull-left">Main Observer</label>
                                    </div>
                                    <div class="col-sm-9">
                                        <div class="form-check form-check-inline">
                                            <input :disabled="isReadOnly" id="mainObserverYes" class="form-check-input"
                                                type="radio" v-model="observerObj.main_observer" value="true">
                                            <label for="mainObserverYes" class="form-check-label">Yes</label>
                                        </div>
                                        <div class="form-check form-check-inline">
                                            <input :disabled="isReadOnly" id="mainObserverNo" class="form-check-input"
                                                type="radio" v-model="observerObj.main_observer" value="false">
                                            <label for="mainObserverNo" class="form-check-label">No</label>
                                        </div>
                                    </div>
                                </div>
                                <div v-if="!occurrence_report.has_main_observer" class="row mb-3">
                                    <div class="col-sm-3">
                                        <label class="control-label pull-left">&nbsp;</label>
                                    </div>
                                    <div class="col-sm-9">
                                        <button type="button" class="btn btn-primary mb-2" @click="clearForm">Clear
                                            Form</button><br />
                                        <button type="button" class="btn btn-primary" @click="populateWithSubmitterInformation()">Populate Form with Submitter Details</button>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </form>
                </div>
            </div>
            <div slot="footer">
                <button type="button" class="btn btn-secondary me-2" @click="cancel">Cancel</button>
                <template v-if="observer_detail_id">
                    <button type="button" v-if="updatingObserver" disabled class="btn btn-primary" @click="ok"><i
                            class="fa fa-spinnner fa-spin"></i> Updating</button>
                    <button type="button" v-else class="btn btn-primary" @click="ok">Update Observer</button>
                </template>
                <template v-else>
                    <button type="button" v-if="addingObserver" disabled class="btn btn-primary" @click="ok"><i
                            class="fa fa-spinner fa-spin"></i> Adding</button>
                    <button type="button" v-else class="btn btn-primary" @click="ok">Add Observer</button>
                </template>
            </div>
        </modal>
    </div>
</template>

<script>
import modal from '@vue-utils/bootstrap-modal.vue'
import alert from '@vue-utils/alert.vue'
import { helpers } from "@/utils/hooks.js"

export default {
    name: 'ObserverDetail',
    components: {
        modal,
        alert
    },
    props: {
        url: {
            type: String,
            required: true
        },
        occurrence_report: {
            type: Object,
            required: true
        },
    },
    data: function () {
        let vm = this;
        return {
            isModalOpen: false,
            form: null,
            observer_detail_id: String,
            observer_detail_action: String,
            observerObj: {},
            addingObserver: false,
            updatingObserver: false,
            validation_form: null,
            type: '1',
            errors: false,
            errorString: '',
            successString: '',
            success: false,
            validDate: false,
        }
    },
    computed: {
        showError: function () {
            var vm = this;
            return vm.errors;
        },
        title: function () {
            var action = this.observer_detail_action;
            if (typeof action === "string" && action.length > 0) {
                var capitalizedAction = action.charAt(0).toUpperCase() + action.slice(1);
                return `${capitalizedAction} Observer to ${this.occurrence_report.occurrence_report_number}`;
            } else {
                return "Invalid Observer detail action"; // Or handle the error in an appropriate way
            }
        },
        isReadOnly: function () {
            return this.observer_detail_action === "view" ? true : false;
        }
    },
    watch: {
        isModalOpen: function (val) {
            if (val) {
                this.$nextTick(() => {
                    this.$refs.observer_name.focus();
                    if (this.occurrence_report.has_main_observer) {
                        this.observerObj.main_observer = false;
                    } else {
                        this.populateWithSubmitterInformation();
                    }
                });
            }
        }
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
            this.isModalOpen = false;
            this.observerObj = {};
            this.errors = false;
            $('.has-error').removeClass('has-error');
        },
        sendData: function () {
            let vm = this;
            vm.errors = false;
            let observerObj = JSON.parse(JSON.stringify(vm.observerObj));
            let formData = new FormData()

            if (vm.observerObj.id) {
                vm.updatingObserver = true;
                formData.append('data', JSON.stringify(observerObj));
                vm.$http.put(helpers.add_endpoint_json(vm.url, observerObj.id), formData, {
                    emulateJSON: true,
                }).then((response) => {
                    vm.updatingObserver = false;
                    vm.$parent.updatedObserverDetails();
                    vm.close();
                }, (error) => {
                    vm.errors = true;
                    vm.errorString = helpers.apiVueResourceError(error);
                    vm.updatingObserver = false;
                });
            } else {
                vm.addingObserver = true;
                formData.append('data', JSON.stringify(observerObj));
                vm.$http.post(vm.url, formData, {
                    emulateJSON: true,
                }).then((response) => {
                    vm.addingObserver = false;
                    vm.$parent.updatedObserverDetails();
                    vm.close();
                }, (error) => {
                    vm.errors = true;
                    vm.addingObserver = false;
                    vm.errorString = helpers.apiVueResourceError(error);
                });
            }
        },
        populateWithSubmitterInformation: function () {
            console.log('Populating with submitter information')
            let observerObj = {
                main_observer: true,
                observer_name: '',
                contact: '',
                organisation: '',
                role: '',
            };
            observerObj.observer_name = this.occurrence_report.submitter_information.name;
            observerObj.contact = this.occurrence_report.submitter_information.contact_details;
            if (this.occurrence_report.submitter_information.organisation) {
                observerObj.organisation = this.occurrence_report.submitter_information.organisation;
            }
            if (this.occurrence_report.submitter_information.position) {
                observerObj.role = this.occurrence_report.submitter_information.position;
            }
            this.observerObj = Object.assign({}, observerObj);
        },
        clearForm: function () {
            this.observerObj = { main_observer: true };
            this.$refs.observer_name.focus();
        },
    },
    mounted: function () {
        let vm = this;
        vm.form = document.forms.observerDetailForm;
    }
}
</script>

<style lang="css">
.modal-input-row {
    margin-bottom: 20px;
}

input[type=text],
select {
    padding: 0.375rem 2.25rem 0.375rem 0.75rem;
}
</style>
