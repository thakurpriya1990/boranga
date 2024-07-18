<template lang="html">
    <div id="proposal-proposed-delist">
        <modal transition="modal fade" @ok="validateForm()" @cancel="cancel()" :title="title" large>
            <div class="container-fluid">
                <div class="row">
                    <form class="form-horizontal needs-validation" id="delistForm" name="delistForm" novalidate>
                        <alert :show.sync="showError" type="danger"><strong>{{ errorString }}</strong></alert>
                        <div class="col-sm-12">
                            <div class="form-group">
                                <div class="row mb-3">
                                    <div class="col-sm-12">
                                        <label class="control-label" for="efective_to">Effective To</label>
                                        <input type="date" style="width: 70%;" class="form-control" id="efective_to"
                                            name="efective_to" ref="efective_to" v-model="delist.effective_to"
                                            :max="new Date().toISOString().split('T')[0]" required />
                                        <div class="invalid-feedback">
                                            Please provide an effective to date.
                                        </div>
                                    </div>
                                </div>
                                <div class="row mb-3">
                                    <div class="col-sm-12">
                                        <label class="control-label" for="Name">Reason for proposing to delist</label>
                                        <textarea style="width: 70%;" class="form-control" id="reason" name="reason"
                                            ref="reason" v-model="delist.reason" required></textarea>
                                        <div class="invalid-feedback">
                                            Please provide a reason for proposing to delist.
                                        </div>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </form>
                </div>
            </div>
            <div slot="footer">
                <button type="button" class="btn btn-secondary me-2" @click="cancel">Cancel</button>
                <button type="button" v-if="delistingProposal" disabled class="btn btn-primary">Processing <span
                        class="spinner-border spinner-border-sm" role="status" aria-hidden="true"></span>
                    <span class="visually-hidden">Loading...</span></button>
                <button type="button" v-else class="btn btn-primary" @click="validateForm()">Propose Delist</button>
            </div>
        </modal>
    </div>
</template>

<script>
import modal from '@vue-utils/bootstrap-modal.vue'
import alert from '@vue-utils/alert.vue'
import { helpers, api_endpoints } from "@/utils/hooks.js"
const calculateDefaultDate = () => {
    const now = new Date();
    now.setHours(9, 0, 0, 0);  // Set time to 9:00 AM

    const year = now.getFullYear();
    const month = String(now.getMonth() + 1).padStart(2, '0'); // Months are zero-indexed
    const day = String(now.getDate()).padStart(2, '0');
    const hours = String(now.getHours()).padStart(2, '0');
    const minutes = String(now.getMinutes()).padStart(2, '0');

    return `${year}-${month}-${day}T${hours}:${minutes}`;
};
export default {
    name: 'Propose-Delist-Proposal',
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
            delist: {
                effective_to: new Date().toISOString().split('T')[0]
            },
            delistingProposal: false,
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
                    this.$refs['efective_to'].focus();
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
            return `Propose Delist Conservation Status CS${this.conservation_status_id}`;
        }
    },
    methods: {
        cancel: function () {
            this.close();
        },
        close: function () {
            this.isModalOpen = false;
            this.delist = { effective_to: new Date().toISOString().split('T')[0] };
            this.errors = false;
            $('.was-validated').removeClass('was-validated');
        },
        validateForm: function () {
            let vm = this;
            if (vm.form.checkValidity()) {
                vm.sendData();
            } else {
                vm.form.classList.add('was-validated');
                $('#delistForm').find(':invalid').first().focus();
            }
            return false;
        },
        sendData: function () {
            let vm = this;
            vm.errors = false;
            let delist = JSON.parse(JSON.stringify(vm.delist));
            vm.delistingProposal = true;
            if (vm.processing_status == 'Approved') {
                vm.$http.patch(helpers.add_endpoint_json(api_endpoints.conservation_status, vm.conservation_status_id + '/propose_delist'), JSON.stringify(delist), {
                    emulateJSON: true,
                }).then((response) => {
                    vm.delistingProposal = false;
                    vm.close();
                    vm.$emit('refreshFromResponse', response);
                    vm.$router.push({ path: '/internal/conservation-status/' }); //Navigate to dashboard after propose delist.
                }, (error) => {
                    vm.errors = true;
                    vm.delistingProposal = false;
                    vm.errorString = helpers.apiVueResourceError(error);
                });
            } else {
                vm.close();
            }
        },
    },
    mounted: function () {
        let vm = this;
        vm.form = document.forms.delistForm;
    }
}
</script>
<style scoped>
.error {
    color: red;
}
</style>
