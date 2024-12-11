<template lang="html">
    <div id="proposal-proposed-decline">
        <modal
            transition="modal fade"
            :title="title"
            large
            @ok="ok()"
            @cancel="cancel()"
        >
            <div class="container-fluid">
                <div class="row">
                    <form class="form-horizontal" name="declineForm">
                        <alert v-if="showError" type="danger"
                            ><strong>{{ errorString }}</strong></alert
                        >
                        <div class="col-sm-12">
                            <div class="form-group">
                                <div class="row mb-3">
                                    <div class="col-sm-12">
                                        <label class="control-label" for="Name"
                                            >Details</label
                                        >
                                        <textarea
                                            ref="reason"
                                            v-model="decline.reason"
                                            style="width: 70%"
                                            class="form-control"
                                            name="reason"
                                        ></textarea>
                                    </div>
                                </div>
                            </div>
                            <div class="form-group">
                                <div class="row" mb-3>
                                    <div class="col-sm-12">
                                        <label class="control-label" for="Name"
                                            >CC email</label
                                        >
                                        <input
                                            v-model="decline.cc_email"
                                            type="text"
                                            style="width: 70%"
                                            class="form-control"
                                            name="cc_email"
                                        />
                                    </div>
                                </div>
                            </div>
                        </div>
                    </form>
                </div>
            </div>
            <template #footer>
                <div>
                    <button
                        type="button"
                        class="btn btn-secondary me-2"
                        @click="cancel"
                    >
                        Cancel
                    </button>
                    <button
                        v-if="decliningProposal"
                        type="button"
                        disabled
                        class="btn btn-primary"
                        @click="ok"
                    >
                        Processing
                        <span
                            class="spinner-border spinner-border-sm"
                            role="status"
                            aria-hidden="true"
                        ></span>
                        <span class="visually-hidden">Loading...</span>
                    </button>
                    <button
                        v-else
                        type="button"
                        class="btn btn-primary"
                        @click="ok"
                    >
                        Decline
                    </button>
                </div>
            </template>
        </modal>
    </div>
</template>

<script>
import modal from '@vue-utils/bootstrap-modal.vue';
import alert from '@vue-utils/alert.vue';
import { helpers, api_endpoints } from '@/utils/hooks.js';
export default {
    name: 'DeclineProposal',
    components: {
        modal,
        alert,
    },
    props: {
        conservation_status_id: {
            type: Number,
            required: true,
        },
        processing_status: {
            type: String,
            required: true,
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
        };
    },
    computed: {
        showError: function () {
            var vm = this;
            return vm.errors;
        },
        title: function () {
            return `Decline Conservation Status CS${this.conservation_status_id}`;
        },
    },
    watch: {
        isModalOpen: function (val) {
            if (val) {
                this.$nextTick(() => {
                    this.$refs['reason'].focus();
                });
            }
        },
    },
    mounted: function () {
        let vm = this;
        vm.form = document.forms.declineForm;
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
        },
        sendData: function () {
            let vm = this;
            vm.errors = false;
            let decline = JSON.parse(JSON.stringify(vm.decline));
            vm.decliningProposal = true;
            if (
                vm.processing_status == 'With Assessor' ||
                vm.processing_status == 'On Agenda'
            ) {
                fetch(
                    helpers.add_endpoint_json(
                        api_endpoints.conservation_status,
                        vm.conservation_status_id + '/final_decline'
                    ),
                    {
                        method: 'POST',
                        headers: {
                            'Content-Type': 'application/json',
                        },
                        body: JSON.stringify(decline),
                    }
                ).then(
                    (response) => {
                        vm.decliningProposal = false;
                        vm.close();
                        vm.$emit('refreshFromResponse', response);
                        vm.$router.push({
                            path: '/internal/conservation-status/',
                        }); //Navigate to dashboard after propose decline.
                    },
                    (error) => {
                        vm.errors = true;
                        vm.decliningProposal = false;
                        vm.errorString = helpers.apiVueResourceError(error);
                    }
                );
            }
        },
    },
};
</script>
