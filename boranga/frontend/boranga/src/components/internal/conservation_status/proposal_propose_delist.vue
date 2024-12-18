<template lang="html">
    <div id="proposal-proposed-delist">
        <modal
            transition="modal fade"
            :title="title"
            large
            @ok="validateForm()"
            @cancel="cancel()"
        >
            <div class="container-fluid">
                <div class="row">
                    <form
                        id="delistForm"
                        class="form-horizontal needs-validation"
                        name="delistForm"
                        novalidate
                    >
                        <alert v-if="errorString" type="danger"
                            ><strong>{{ errorString }}</strong></alert
                        >
                        <div class="col-sm-12">
                            <div class="form-group">
                                <div class="row mb-3">
                                    <div class="col-sm-12">
                                        <label
                                            class="control-label"
                                            for="efective_to"
                                            >Effective To</label
                                        >
                                        <input
                                            id="efective_to"
                                            ref="efective_to"
                                            v-model="delist.effective_to"
                                            type="date"
                                            style="width: 70%"
                                            class="form-control"
                                            name="efective_to"
                                            :max="
                                                new Date()
                                                    .toISOString()
                                                    .split('T')[0]
                                            "
                                            required
                                        />
                                        <div class="invalid-feedback">
                                            Please provide an effective to date.
                                        </div>
                                    </div>
                                </div>
                                <div class="row mb-3">
                                    <div class="col-sm-12">
                                        <label class="control-label" for="Name"
                                            >Reason for proposing to
                                            delist</label
                                        >
                                        <textarea
                                            id="reason"
                                            ref="reason"
                                            v-model="delist.reason"
                                            style="width: 70%"
                                            class="form-control"
                                            name="reason"
                                            required
                                        ></textarea>
                                        <div class="invalid-feedback">
                                            Please provide a reason for
                                            proposing to delist.
                                        </div>
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
                        v-if="delistingProposal"
                        type="button"
                        disabled
                        class="btn btn-primary"
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
                        @click="validateForm()"
                    >
                        Propose Delist
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
    name: 'ProposeDelistProposal',
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
            delist: {
                effective_to: new Date().toISOString().split('T')[0],
            },
            delistingProposal: false,
            errorString: '',
        };
    },
    computed: {
        title: function () {
            return `Propose Delist Conservation Status CS${this.conservation_status_id}`;
        },
    },
    watch: {
        isModalOpen: function (val) {
            if (val) {
                this.$nextTick(() => {
                    this.$refs['efective_to'].focus();
                });
            }
        },
    },
    mounted: function () {
        let vm = this;
        vm.form = document.forms.delistForm;
    },
    methods: {
        cancel: function () {
            this.close();
        },
        close: function () {
            this.isModalOpen = false;
            this.delist = {
                effective_to: new Date().toISOString().split('T')[0],
            };
            this.errorString = '';
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
            vm.errorString = '';
            let delist = JSON.parse(JSON.stringify(vm.delist));
            vm.delistingProposal = true;
            if (vm.processing_status == 'Approved') {
                fetch(
                    helpers.add_endpoint_json(
                        api_endpoints.conservation_status,
                        vm.conservation_status_id + '/propose_delist'
                    ),
                    {
                        method: 'PATCH',
                        headers: { 'Content-Type': 'application/json' },
                        body: JSON.stringify(delist),
                    }
                )
                    .then(async (response) => {
                        const data = await response.json();
                        if (!response.ok) {
                            vm.errorString = data;
                            return;
                        }
                        vm.close();
                        vm.$emit('refreshFromResponse', response);
                        vm.$router.push({
                            path: '/internal/conservation-status/',
                        }); //Navigate to dashboard after propose delist.
                    })
                    .finally(() => {
                        vm.delistingProposal = false;
                    });
            } else {
                vm.close();
            }
        },
    },
};
</script>
<style scoped>
.error {
    color: red;
}
</style>
