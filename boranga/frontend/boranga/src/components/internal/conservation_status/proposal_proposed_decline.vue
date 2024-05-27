<template lang="html">
    <div id="proposal-proposed-decline">
        <modal transition="modal fade" @ok="ok()" @cancel="cancel()" :title="title" large>
            <div class="container-fluid">
                <div class="row">
                    <form class="form-horizontal" name="declineForm">
                        <alert :show.sync="showError" type="danger"><strong>{{ errorString }}</strong></alert>
                        <div class="col-sm-12">
                            <div class="form-group">
                                <div class="row mb-3">
                                    <div class="col-sm-12">
                                        <label class="control-label" for="Name">Details</label>
                                        <textarea style="width: 70%;" class="form-control" name="reason" ref="reason"
                                            v-model="decline.reason"></textarea>
                                    </div>
                                </div>
                            </div>
                            <div class="form-group">
                                <div class="row" mb-3>
                                    <div class="col-sm-12">
                                        <label class="control-label" for="Name">CC email</label>
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
                <button type="button" v-if="decliningProposal" disabled class="btn btn-primary" @click="ok"><i
                        class="fa fa-spinner fa-spin"></i> Processing</button>
                <button type="button" v-else class="btn btn-primary" @click="ok">Decline</button>
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
    watch: {
        isModalOpen: function (val) {
            if (val) {
                this.$nextTick(() => {
                    this.$refs['reason'].focus();
                });
            }
        }
    },
    computed: {
        showError: function () {
            var vm = this;
            return vm.errors;
        },
        title: function () {
            return `Decline Conservation Status CS${this.conservation_status_id}`;
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
            if (vm.processing_status == 'With Assessor' || vm.processing_status == 'Ready For Agenda') {
                vm.$http.post(helpers.add_endpoint_json(api_endpoints.conservation_status, vm.conservation_status_id + '/final_decline'), JSON.stringify(decline), {
                    emulateJSON: true,
                }).then((response) => {
                    vm.decliningProposal = false;
                    vm.close();
                    vm.$emit('refreshFromResponse', response);
                    vm.$router.push({ path: '/internal/conservation-status/' }); //Navigate to dashboard after propose decline.
                }, (error) => {
                    vm.errors = true;
                    vm.decliningProposal = false;
                    vm.errorString = helpers.apiVueResourceError(error);
                });
            }
        },
    },
    mounted: function () {
        let vm = this;
        vm.form = document.forms.declineForm;
    }
}
</script>
