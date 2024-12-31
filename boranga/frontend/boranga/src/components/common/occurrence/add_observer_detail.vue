<template lang="html">
    <div id="observerDetail">
        <modal
            v-if="observerObj"
            transition="modal fade"
            :title="title"
            large
            @ok="ok()"
            @cancel="close()"
        >
            <div class="container-fluid">
                <div class="row">
                    <form
                        class="form-horizontal needs-validation"
                        name="observerDetailForm"
                        novalidate
                    >
                        <alert v-if="errorString" type="danger"
                            ><strong>{{ errorString }}</strong></alert
                        >
                        <div class="col-sm-12">
                            <div class="form-group">
                                <div class="row mb-3">
                                    <div class="col-sm-3">
                                        <label class="control-label pull-left"
                                            >Name</label
                                        >
                                    </div>
                                    <div class="col-sm-9">
                                        <input
                                            ref="observer_name"
                                            v-model="observerObj.observer_name"
                                            type="text"
                                            class="form-control"
                                            :disabled="isReadOnly"
                                            required
                                            autofocus
                                        />
                                    </div>
                                </div>
                                <div class="row mb-3">
                                    <div class="col-sm-3">
                                        <label class="control-label pull-left"
                                            >Role</label
                                        >
                                    </div>
                                    <div class="col-sm-9">
                                        <input
                                            v-model="observerObj.role"
                                            type="text"
                                            class="form-control"
                                            :disabled="isReadOnly"
                                        />
                                    </div>
                                </div>
                                <div
                                    v-if="'contact' in observerObj"
                                    class="row mb-3"
                                >
                                    <div class="col-sm-3">
                                        <label class="control-label pull-left"
                                            >Contact Details</label
                                        >
                                    </div>
                                    <div class="col-sm-9">
                                        <textarea
                                            id="contact_details"
                                            v-model="observerObj.contact"
                                            class="form-control"
                                            :disabled="isReadOnly"
                                            rows="4"
                                        />
                                    </div>
                                </div>
                                <div class="row mb-3">
                                    <div class="col-sm-3">
                                        <label class="control-label pull-left"
                                            >Organisation</label
                                        >
                                    </div>
                                    <div class="col-sm-9">
                                        <input
                                            v-model="observerObj.organisation"
                                            type="text"
                                            class="form-control"
                                            :disabled="isReadOnly"
                                        />
                                    </div>
                                </div>
                                <div class="row mb-3">
                                    <div class="col-sm-3">
                                        <label class="control-label pull-left"
                                            >Main Observer</label
                                        >
                                    </div>
                                    <div class="col-sm-9">
                                        <div
                                            class="form-check form-check-inline"
                                        >
                                            <input
                                                id="mainObserverYes"
                                                v-model="
                                                    observerObj.main_observer
                                                "
                                                :disabled="
                                                    isReadOnly ||
                                                    (occurrence_report.has_main_observer &&
                                                        !observerObj.main_observer)
                                                "
                                                class="form-check-input"
                                                type="radio"
                                                value="true"
                                            />
                                            <label
                                                for="mainObserverYes"
                                                class="form-check-label"
                                                >Yes</label
                                            >
                                        </div>
                                        <div
                                            class="form-check form-check-inline"
                                        >
                                            <input
                                                id="mainObserverNo"
                                                v-model="
                                                    observerObj.main_observer
                                                "
                                                :disabled="
                                                    isReadOnly ||
                                                    (occurrence_report.has_main_observer &&
                                                        !observerObj.main_observer)
                                                "
                                                class="form-check-input"
                                                type="radio"
                                                value="false"
                                            />
                                            <label
                                                for="mainObserverNo"
                                                class="form-check-label"
                                                >No</label
                                            >
                                        </div>
                                    </div>
                                </div>
                                <div
                                    v-if="!occurrence_report.has_main_observer"
                                    class="row mb-3"
                                >
                                    <div class="col-sm-3">
                                        <label class="control-label pull-left"
                                            >&nbsp;</label
                                        >
                                    </div>
                                    <div v-if="!isReadOnly" class="col-sm-9">
                                        <button
                                            type="button"
                                            class="btn btn-primary mb-2"
                                            @click="clearForm"
                                        >
                                            Clear Form</button
                                        ><br />
                                        <button
                                            type="button"
                                            class="btn btn-primary"
                                            @click="
                                                populateWithSubmitterInformation()
                                            "
                                        >
                                            Populate Form with Submitter Details
                                        </button>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </form>
                </div>
            </div>
            <template #footer>
                <div>
                    <div>
                        <button
                            type="button"
                            class="btn btn-secondary me-2"
                            @click="close()"
                        >
                            <template v-if="isReadOnly">Close</template
                            ><template v-else>Cancel</template>
                        </button>
                        <template v-if="!isReadOnly">
                            <template v-if="observerObj.id">
                                <button
                                    v-if="updatingObserver"
                                    type="button"
                                    disabled
                                    class="btn btn-primary"
                                    @click="ok"
                                >
                                    Updating
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
                                    type="button"
                                    class="btn btn-primary"
                                    @click="ok"
                                >
                                    Update Observer
                                </button>
                            </template>
                            <template v-else>
                                <button
                                    v-if="addingObserver"
                                    type="button"
                                    disabled
                                    class="btn btn-primary"
                                    @click="ok"
                                >
                                    Adding
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
                                    type="button"
                                    class="btn btn-primary"
                                    @click="ok"
                                >
                                    Add Observer
                                </button>
                            </template>
                        </template>
                    </div>
                </div>
            </template>
        </modal>
    </div>
</template>

<script>
import modal from '@vue-utils/bootstrap-modal.vue';
import alert from '@vue-utils/alert.vue';
import { helpers } from '@/utils/hooks.js';

export default {
    name: 'ObserverDetail',
    components: {
        modal,
        alert,
    },
    props: {
        url: {
            type: String,
            required: true,
        },
        occurrence_report: {
            type: Object,
            required: true,
        },
    },
    data: function () {
        return {
            isModalOpen: false,
            form: null,
            observer_detail_action: String,
            observerObj: null,
            addingObserver: false,
            updatingObserver: false,
            errorString: '',
        };
    },
    computed: {
        title: function () {
            var action = this.observer_detail_action;
            if (typeof action === 'string' && action.length > 0) {
                var capitalizedAction =
                    action.charAt(0).toUpperCase() + action.slice(1);
                return `${capitalizedAction} Observer of ${this.occurrence_report.occurrence_report_number}`;
            } else {
                return 'Invalid Observer detail action'; // Or handle the error in an appropriate way
            }
        },
        isReadOnly: function () {
            return this.observer_detail_action === 'view' ? true : false;
        },
    },
    watch: {
        isModalOpen: function (val) {
            if (val) {
                this.$nextTick(() => {
                    if (this.$refs.observer_name) {
                        this.$refs.observer_name.focus();
                    }
                    if (this.observer_detail_action === 'add') {
                        if (!this.occurrence_report.has_main_observer) {
                            this.populateWithSubmitterInformation();
                        }
                        this.observerObj.main_observer =
                            !this.occurrence_report.has_main_observer;
                    }
                });
            }
        },
    },
    methods: {
        ok: function () {
            let vm = this;
            if ($(document.forms.observerDetailForm).valid()) {
                vm.sendData();
            }
        },
        close: function () {
            this.isModalOpen = false;
            this.observerObj = null;
            this.errorString = '';
            $('.has-error').removeClass('has-error');
        },
        sendData: function () {
            let vm = this;
            vm.errorString = '';
            let observerObj = JSON.parse(JSON.stringify(vm.observerObj));
            let formData = new FormData();

            if (vm.observerObj.id) {
                vm.updatingObserver = true;
                formData.append('data', JSON.stringify(observerObj));
                fetch(helpers.add_endpoint_json(vm.url, observerObj.id), {
                    method: 'PUT',
                    body: formData,
                })
                    .then(async (response) => {
                        const data = await response.json();
                        if (!response.ok) {
                            vm.errorString = data;
                            return;
                        }
                        vm.$parent.updatedObserverDetails();
                        vm.close();
                    })
                    .finally(() => {
                        vm.updatingObserver = false;
                    });
            } else {
                vm.addingObserver = true;
                formData.append('data', JSON.stringify(observerObj));
                fetch(vm.url, {
                    method: 'POST',
                    body: formData,
                })
                    .then(async (response) => {
                        const data = await response.json();
                        if (!response.ok) {
                            vm.errorString = data;
                            return;
                        }
                        vm.$parent.updatedObserverDetails();
                        vm.close();
                    })
                    .finally(() => {
                        vm.addingObserver = false;
                    });
            }
        },
        populateWithSubmitterInformation: function () {
            let observerObj = {
                occurrence_report: this.occurrence_report.id,
                main_observer: true,
                observer_name: '',
                contact: '',
                organisation: '',
                role: '',
            };
            observerObj = { ...observerObj, ...this.observerObj };
            console.log(this.occurrence_report.submitter_information);
            observerObj.observer_name =
                this.occurrence_report.submitter_information.name;
            observerObj.contact =
                this.occurrence_report.submitter_information.contact_details;
            if (this.occurrence_report.submitter_information.organisation) {
                observerObj.organisation =
                    this.occurrence_report.submitter_information.organisation;
            }
            if (this.occurrence_report.submitter_information.position) {
                observerObj.role =
                    this.occurrence_report.submitter_information.position;
            }
            this.observerObj = Object.assign({}, observerObj);
        },
        clearForm: function () {
            this.observerObj = {
                id: this.observerObj.id ? this.observerObj.id : null,
                occurrence_report: this.occurrence_report.id,
                main_observer: true,
                contact: '',
            };
            this.$refs.observer_name.focus();
        },
    },
};
</script>
