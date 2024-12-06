<template lang="html">
    <div id="internal-conservation-status-proposal-defer">
        <modal id="defer-cs-modal" transition="modal fade" @ok="ok()" @cancel="close()"
            :title="`Defer CS${conservation_status.id} `" okText="Defer" large>
            <div class="container-fluid">
                <div class="row">
                    <form class="form-horizontal needs-validation" id="defer-form" name="defer-form" novalidate>
                        <alert v-if="errors" type="danger"><strong>{{ errors }}</strong></alert>
                        <div class="col-sm-12">
                            <div class="row mb-3">
                                <div class="col">
                                    <div class="form-group">
                                        <label class="control-label mb-3" for="reason">Reason / Comments</label>
                                        <textarea class="form-control" id="reason" name="reason" ref="reason" required
                                            v-model="reason"></textarea>
                                        <div class="invalid-feedback">
                                            Please enter the reason for deferring the Conservation Status Proposal.
                                        </div>
                                    </div>
                                </div>
                            </div>
                            <div class="row mb-3">
                                <div class="col">
                                    <alert type="warning">
                                        Entering a review date is not mandatory but is
                                        highly recommended
                                        to ensure that the Conservation Status Proposal is reviewed in a timely manner.
                                    </alert>
                                </div>
                            </div>
                            <div class=" row mb-3">
                                <div class="col">
                                    <div class="form-group">
                                        <label class="control-label mb-3" for="review-due-date">Review Due Date</label>
                                        <input type="date" class="form-control" id="review-due-date"
                                            name="review-due-date" ref="review-due-date" v-model="reviewDueDate" />
                                    </div>
                                </div>
                            </div>
                        </div>
                    </form>
                </div>
            </div>
        </modal>
    </div>
</template>

<script>
import modal from '@vue-utils/bootstrap-modal.vue'
import alert from '@vue-utils/alert.vue'
import { helpers, api_endpoints } from "@/utils/hooks.js"

export default {
    name: 'defer',
    components: {
        modal,
        alert,
    },
    props: {
        conservation_status: {
            type: Object,
        },
    },
    data: function () {
        return {
            reason: null,
            reviewDueDate: null,
            isModalOpen: false,
            errors: null,
        }
    },
    emits: ['refreshFromResponse'],
    watch: {
        isModalOpen: function (val) {
            if (val) {
                this.$nextTick(() => {
                    $(this.$refs.reason).focus();
                    this.reviewDueDate = this.conservation_status.review_due_date;
                });
            }
        }
    },
    methods: {
        ok: function () {
            let vm = this;
            var form = document.getElementById('defer-form');
            if (form.checkValidity()) {
                vm.defer();
            } else {
                form.classList.add('was-validated');
                $('#defer-form').find(':invalid').first().focus();
            }
            return false;
        },
        close: function () {
            this.reason = null;
            this.errors = null;
            this.isModalOpen = false;
        },
        defer: function () {
            let vm = this;
            vm.errors = null;
            let data = { 'review_due_date': vm.reviewDueDate, 'reason': vm.reason }
            fetch(api_endpoints.defer_cs_proposal(vm.conservation_status.id), {
                method: 'PATCH',
                headers: { 'Content-Type': 'application/json', },
                body: JSON.stringify(data),
            })
                .then((response) => {
                    vm.$emit('refreshFromResponse', response);
                    this.close();
                }, (error) => {
                    swal.fire({
                        title: 'Application Error',
                        text: helpers.apiVueResourceError(error),
                        icon: 'error',
                        customClass: {
                            confirmButton: 'btn btn-primary',
                        },
                    });
                });
        },
    },
}
</script>
