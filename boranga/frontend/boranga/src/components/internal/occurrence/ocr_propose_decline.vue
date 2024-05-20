<template lang="html">
    <div id="internal-ocr-propose-decline-request">
        <modal id="myModal" transition="modal fade" @ok="ok()" ok-text="Propose Decline" @cancel="close()"
            :title="`Propose Decline ${occurrence_report_number}`" large>
            <div class="container-fluid">
                <div class="row">
                    <form class="form-horizontal" name="propose-decline-form">
                        <alert v-if="errorString" type="danger"><strong>{{ errorString }}</strong></alert>
                        <label class="control-label mb-3" for="reason">Reason</label>
                        <textarea class="form-control" name="reason" v-model="propose_decline.reason" id="reason"
                            ref="reason" required></textarea>
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
    name: 'ocr-propose-decline',
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
            propose_decline: {
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
                vm.proposeDecline();
            } else {
                vm.form.reportValidity();
            }
        },
        close: function () {
            this.isModalOpen = false;
            this.propose_decline = {
                reason: '',
                occurrence_report: this.occurrence_report_id
            };
            this.errorString = '';
            $(this.$refs.reason).val(null).trigger('change');
            this.form.reset();
        },
        proposeDecline: function () {
            let vm = this;
            swal.fire({
                title: "Propose Decline Application",
                text: `Are you sure you want to propose to decline occurrence report ${vm.occurrence_report_number}?`,
                icon: "question",
                showCancelButton: true,
                confirmButtonText: 'Propose Decline',
                confirmButtonColor: '#d9534f',
                reverseButtons: true,
                buttonsStyling: false,
                customClass: {
                    confirmButton: 'btn btn-primary',
                    cancelButton: 'btn btn-secondary me-2',
                },
            }).then((swalresult) => {
                if (swalresult.isConfirmed) {
                    vm.$http.post(helpers.add_endpoint_join(api_endpoints.occurrence_report, '/' + (vm.occurrence_report_id + '/propose_decline/')), JSON.stringify(vm.propose_decline))
                        .then((response) => {
                            swal.fire({
                                title: 'Proposal to Decline Successful',
                                text: `Your proposal to decline occurrence report ${vm.occurrence_report_number} has been succuessfully submitted.`,
                                icon: 'success',
                                confirmButtonColor: '#226fbb',
                            }).then((result) => {
                                vm.$router.go();
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
        this.form = document.forms['propose-decline-form'];
    }
}
</script>
