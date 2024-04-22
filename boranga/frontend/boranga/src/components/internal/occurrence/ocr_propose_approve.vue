<template lang="html">
    <div id="internal-ocr-propose-approve-request">
        <modal id="myModal" transition="modal fade" @ok="ok()" ok-text="Propose Approve" @cancel="close()"
            :title="`Propose Approve ${occurrence_report_number}`" large>
            <div class="container">
                <form>
                    <div class="row mb-3">
                        <div class="col">
                            <div class="form-check form-check-inline">
                                <input class="form-check-input" type="radio" name="create_new_occurrence"
                                    id="create_new_occurrence_new" :value="true"
                                    v-model="propose_approve.create_new_occurrence" />
                                <label class="form-check-label" for="create_new_occurrence_new">Create New
                                    Occurrence</label>
                            </div>
                            <div class="form-check form-check-inline">
                                <input class="form-check-input" type="radio" name="create_new_occurrence"
                                    id="create_new_occurrence_existing" :value="false"
                                    v-model="propose_approve.create_new_occurrence" />
                                <label class="form-check-label" for="create_new_occurrence_existing">Add to Existing
                                    Occurrence</label>
                            </div>
                            <div v-if="!propose_approve.create_new_occurrence" class="mt-3">
                                Select Existing Occurrence:
                            </div>
                        </div>
                    </div>
                </form>
            </div>
        </modal>
    </div>
</template>

<script>
import modal from '@vue-utils/bootstrap-modal.vue'
import alert from '@vue-utils/alert.vue'

import { helpers, api_endpoints } from "@/utils/hooks.js"
export default {
    name: 'ocr-propose-approve',
    components: {
        modal,
        alert,
    },
    props: {
        occurrence_report_id: {
            type: Number,
        },
        occurrence_report_number: {
            type: String,
        },
    },
    data: function () {
        let vm = this;
        return {
            isModalOpen: false,
            form: null,
            propose_approve: {
                create_new_occurrence: true,
                reason: '',
            },
            errorString: '',
        }
    },
    watch: {
        isModalOpen: function (val) {
            if (val) {
                this.$nextTick(() => {
                    this.$refs.reason.focus();
                });
            }
        },
    },
    methods: {
        ok: function () {
            let vm = this;
            if (vm.form.checkValidity()) {
                vm.proposeApprove();
            } else {
                vm.form.reportValidity();
            }
        },
        close: function () {
            this.isModalOpen = false;
            this.propose_approve = {
                reason: '',
                occurrence_report: this.occurrence_report_id
            };
            this.errorString = '';
            $(this.$refs.reason).val(null).trigger('change');
            this.form.reset();
        },
        proposeApprove: function () {
            let vm = this;
            swal.fire({
                title: "Propose Approve Application",
                text: `Are you sure you want to propose to approve occurrence report ${vm.occurrence_report_number}?`,
                icon: "question",
                showCancelButton: true,
                confirmButtonText: 'Propose Approve',
                confirmButtonColor: '#d9534f',
                reverseButtons: true,
                buttonsStyling: false,
                customClass: {
                    confirmButton: 'btn btn-primary',
                    cancelButton: 'btn btn-secondary me-2',
                },
            }).then((swalresult) => {
                if (swalresult.isConfirmed) {
                    vm.$http.post(helpers.add_endpoint_join(api_endpoints.occurrence_report, '/' + (vm.occurrence_report_id + '/propose_approve/')), JSON.stringify(vm.propose_approve))
                        .then((response) => {
                            swal.fire({
                                title: 'Proposal to Approve Successful',
                                text: `Your proposal to approve occurrence report ${vm.occurrence_report_number} has been succuessfully submitted.`,
                                icon: 'success',
                                confirmButtonColor: '#226fbb',
                            });
                            vm.$router.push({
                                name: 'internal-occurrence-dash'
                            });
                        }, (error) => {
                            console.log(error);
                            vm.errorString = helpers.apiVueResourceError(error);
                            vm.amendingProposal = true;
                        });
                }
            });
        },
    },
    mounted: function () {
        this.form = document.forms['propose-approve-form'];
    }
}
</script>
