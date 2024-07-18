<template lang="html">
    <div id="contactDetail">
        <modal transition="modal fade" @ok="ok()" @cancel="cancel()" :title="title" large>
            <div class="container-fluid">
                <div class="row">
                    <form class="form-horizontal needs-validation" name="contactDetailForm" novalidate>
                        <alert :show.sync="showError" type="danger"><strong>{{ errorString }}</strong></alert>
                        <div class="col-sm-12">
                            <div class="form-group">
                                <div class="row modal-input-row mb-3">
                                    <div class="col-sm-3">
                                        <label class="control-label pull-left">Name</label>
                                    </div>
                                    <div class="col-sm-9">
                                        <input type="text" class="form-control" :disabled="isReadOnly"
                                            v-model="contactObj.contact_name" ref="contact_name" required />
                                    </div>
                                </div>
                                <div class="row mb-3">
                                    <div class="col-sm-3">
                                        <label class="control-label pull-left">Role</label>
                                    </div>
                                    <div class="col-sm-9">
                                        <input type="text" class="form-control" :disabled="isReadOnly"
                                            v-model="contactObj.role" />
                                    </div>
                                </div>
                                <div class="row mb-3">
                                    <div class="col-sm-3">
                                        <label class="control-label pull-left">Contact Details</label>
                                    </div>
                                    <div class="col-sm-9">
                                        <textarea class="form-control" id="contact_details" :disabled="isReadOnly"
                                            v-model="contactObj.contact" rows="4" />
                                    </div>
                                </div>
                                <div class="row mb-3">
                                    <div class="col-sm-3">
                                        <label class="control-label pull-left">Organisation</label>
                                    </div>
                                    <div class="col-sm-9">
                                        <input type="text" class="form-control" :disabled="isReadOnly"
                                            v-model="contactObj.organisation" />
                                    </div>
                                </div>

                                <div class="row mb-3">
                                    <div class="col-sm-3">
                                        <label class="control-label pull-left">Notes</label>
                                    </div>
                                    <div class="col-sm-9">
                                        <textarea class="form-control" id="notes" :disabled="isReadOnly"
                                            v-model="contactObj.notes" rows="4" />
                                    </div>
                                </div>

                                <div class="row mb-3">
                                    <div class="col-sm-3">
                                        <label class="control-label pull-left">&nbsp;</label>
                                    </div>
                                    <div v-if="!isReadOnly" class="col-sm-9">
                                        <button type="button" class="btn btn-primary mb-2" @click="clearForm">Clear
                                            Form</button><br />
                                    </div>
                                </div>
                            </div>
                        </div>
                    </form>
                </div>
            </div>
            <div slot="footer">
                <div v-if="!isReadOnly">
                    <button type="button" class="btn btn-secondary me-2" @click="cancel">Cancel</button>
                    <template v-if="contact_detail_id">
                        <button type="button" v-if="updatingContact" disabled class="btn btn-primary" @click="ok">
                            Updating <span class="spinner-border spinner-border-sm" role="status"
                                aria-hidden="true"></span>
                            <span class="visually-hidden">Loading...</span></button>
                        <button type="button" v-else class="btn btn-primary" @click="ok">Update Contact</button>
                    </template>
                    <template v-else>
                        <button type="button" v-if="addingContact" disabled class="btn btn-primary" @click="ok">Adding
                            <span class="spinner-border spinner-border-sm" role="status" aria-hidden="true"></span>
                            <span class="visually-hidden">Loading...</span></button>
                        <button type="button" v-else class="btn btn-primary" @click="ok">Add Contact</button>
                    </template>
                </div>
            </div>
        </modal>
    </div>
</template>

<script>
import modal from '@vue-utils/bootstrap-modal.vue'
import alert from '@vue-utils/alert.vue'
import { helpers } from "@/utils/hooks.js"

export default {
    name: 'ContactDetail',
    components: {
        modal,
        alert
    },
    props: {
        url: {
            type: String,
            required: true
        },
        occurrence: {
            type: Object,
            required: true
        },
    },
    data: function () {
        let vm = this;
        return {
            isModalOpen: false,
            form: null,
            contact_detail_id: String,
            contact_detail_action: String,
            contactObj: {},
            addingContact: false,
            updatingContact: false,
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
            var action = this.contact_detail_action;
            if (typeof action === "string" && action.length > 0) {
                var capitalizedAction = action.charAt(0).toUpperCase() + action.slice(1);
                return `${capitalizedAction} Contact to ${this.occurrence.occurrence_number}`;
            } else {
                return "Invalid Contact detail action"; // Or handle the error in an appropriate way
            }
        },
        isReadOnly: function () {
            return this.contact_detail_action === "view" ? true : false;
        }
    },
    watch: {
        isModalOpen: function (val) {
            if (val) {
                this.$nextTick(() => {
                    this.$refs.contact_name.focus();
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
            this.contactObj = {};
            this.errors = false;
            $('.has-error').removeClass('has-error');
        },
        sendData: function () {
            let vm = this;
            vm.errors = false;
            let contactObj = JSON.parse(JSON.stringify(vm.contactObj));
            let formData = new FormData()

            if (vm.contactObj.id) {
                vm.updatingContact = true;
                formData.append('data', JSON.stringify(contactObj));
                vm.$http.put(helpers.add_endpoint_json(vm.url, contactObj.id), formData, {
                    emulateJSON: true,
                }).then((response) => {
                    vm.updatingContact = false;
                    vm.$parent.updatedContactDetails();
                    vm.close();
                }, (error) => {
                    vm.errors = true;
                    vm.errorString = helpers.apiVueResourceError(error);
                    vm.updatingContact = false;
                });
            } else {
                vm.addingContact = true;
                formData.append('data', JSON.stringify(contactObj));
                vm.$http.post(vm.url, formData, {
                    emulateJSON: true,
                }).then((response) => {
                    vm.addingContact = false;
                    vm.$parent.updatedContactDetails();
                    vm.close();
                }, (error) => {
                    vm.errors = true;
                    vm.addingContact = false;
                    vm.errorString = helpers.apiVueResourceError(error);
                });
            }
        },
        clearForm: function () {
            this.contactObj = {
                occurrence: this.occurrence.id
            };
            this.$refs.contact_name.focus();
        },
    },
    mounted: function () {
        let vm = this;
        vm.form = document.forms.contactDetailForm;
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
