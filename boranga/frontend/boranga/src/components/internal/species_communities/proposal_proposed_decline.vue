<template lang="html">
    <div id="proposal-proposed-decline">
        <modal transition="modal fade" @ok="ok()" @cancel="cancel()" :title="title" large>
            <div class="container-fluid">
                <div class="row">
                    <form class="form-horizontal" name="declineForm">
                        <alert v-if="showError" type="danger"><strong>{{ errorString }}</strong></alert>
                        <div class="col-sm-12">
                            <div class="form-group">
                                <div class="row">
                                    <div class="col-sm-12">
                                        <label v-if=check_status() class="control-label" for="Name">Details</label>
                                        <label v-else class="control-label" for="Name">Provide Reason for the proposed
                                            decline </label>
                                        <textarea style="width: 70%;" class="form-control" name="reason"
                                            v-model="decline.reason"></textarea>
                                    </div>
                                </div>
                            </div>
                            <div class="form-group">
                                <div class="row">
                                    <div class="col-sm-12">
                                        <label v-if=check_status() class="control-label" for="Name">CC email</label>
                                        <label v-else class="control-label" for="Name">Proposed CC email</label>
                                        <input type="text" style="width: 70%;" class="form-control" name="cc_email"
                                            v-model="decline.cc_email" />
                                    </div>
                                </div>
                            </div>
                        </div>
                    </form>
                </div>
            </div>
            <div slot="footer">
                <button type="button" class="btn btn-secondary me-2" @click="cancel">Cancel</button>
                <button type="button" v-if="decliningProposal" disabled class="btn btn-primary" @click="ok">Processing
                    <span class="spinner-border spinner-border-sm" role="status" aria-hidden="true"></span>
                    <span class="visually-hidden">Loading...</span></button>
                <button type="button" v-else class="btn btn-primary" @click="ok">Ok</button>
            </div>
        </modal>
    </div>
</template>

<script>
import modal from '@vue-utils/bootstrap-modal.vue'
import alert from '@vue-utils/alert.vue'
import { helpers, api_endpoints } from "@/utils/hooks.js"
export default {
    name: 'Decline-Proposal',
    components: {
        modal,
        alert
    },
    props: {
        proposal_id: {
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
            form: null,
            decline: {},
            decliningProposal: false,
            errors: false,
            validation_form: null,
            errorString: '',
            successString: '',
            success: false,
        }
    },
    computed: {
        showError: function () {
            var vm = this;
            return vm.errors;
        },
        title: function () {
            return this.processing_status == 'With Approver' ? 'Decline' : 'Proposed Decline';
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
            this.close();
        },
        close: function () {
            this.isModalOpen = false;
            this.decline = {};
            this.errors = false;
            $('.has-error').removeClass('has-error');
            this.validation_form.resetForm();
        },
        check_status: function () {
            let vm = this;
            if (vm.processing_status == 'With Approver')
                return true;
            else
                return false;

        },
        sendData: function () {
            let vm = this;
            vm.errors = false;
            let decline = JSON.parse(JSON.stringify(vm.decline));
            vm.decliningProposal = true;
            if (vm.processing_status != 'With Approver') {
                fetch(helpers.add_endpoint_json(api_endpoints.proposals, vm.proposal_id + '/proposed_decline'), {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify(decline),
                }).then((response) => {
                    vm.decliningProposal = false;
                    vm.close();
                    vm.$emit('refreshFromResponse', response);
                    vm.$router.push({ path: '/internal' }); //Navigate to dashboard after propose decline.
                }, (error) => {
                    vm.errors = true;
                    vm.decliningProposal = false;
                    vm.errorString = helpers.apiVueResourceError(error);
                });
            }
            else {
                fetch(helpers.add_endpoint_json(api_endpoints.proposals, vm.proposal_id + '/final_decline'), {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify(decline),
                }).then((response) => {
                    vm.decliningProposal = false;
                    vm.close();
                    vm.$emit('refreshFromResponse', response);
                }, (error) => {
                    vm.errors = true;
                    vm.decliningProposal = false;
                    vm.errorString = helpers.apiVueResourceError(error);
                });
            }
        },
        addFormValidations: function () {
            let vm = this;
            vm.validation_form = $(vm.form).validate({
                rules: {
                    reason: "required",
                },
                messages: {
                    arrival: "field is required",
                    departure: "field is required",
                    campground: "field is required",
                    campsite: "field is required"
                },
                showErrors: function (errorMap, errorList) {
                    $.each(this.validElements(), function (index, element) {
                        var $element = $(element);
                        $element.attr("data-original-title", "").parents('.form-group').removeClass('has-error');
                    });
                    // destroy tooltips on valid elements
                    $("." + this.settings.validClass).tooltip("destroy");
                    // add or update tooltips
                    for (var i = 0; i < errorList.length; i++) {
                        var error = errorList[i];
                        $(error.element)
                            .tooltip({
                                trigger: "focus"
                            })
                            .attr("data-original-title", error.message)
                            .parents('.form-group').addClass('has-error');
                    }
                }
            });
        },
    },
    mounted: function () {
        let vm = this;
        vm.form = document.forms.declineForm;
        vm.addFormValidations();
    }
}
</script>

<style lang="css">
input[type=text],
select {
    padding: 0.375rem 2.25rem 0.375rem 0.75rem;
}
</style>
