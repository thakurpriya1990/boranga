<template lang="html">
    <div id="internal-ocr-back-to-assessor">
        <modal id="back-to-assessor-modal" transition="modal fade" @ok="ok()" @cancel="cancel()" title="Back to Assessor"
            okText="Back to Assessor" large>
            <div class="container-fluid">
                <div class="row">
                    <form class="form-horizontal" name="back-to-assessor-form">
                        <alert v-if="errorString" type="danger"><strong>{{ errorString }}</strong></alert>
                        <div class="col-sm-12">
                            <div class="row mb-3">
                                <div class="col">
                                    <div class="form-group">
                                        <label class="control-label mb-3" for="reason">Reason</label>
                                        <textarea class="form-control" name="reason" v-model="back_to_assessor.reason"
                                            id="reason" ref="reason" required></textarea>
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
    name: 'back-to-assessor',
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
            back_to_assessor: {
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
        }
    },
    methods: {
        ok: function () {
            if (this.form.checkValidity()) {
                this.backToAssessor();
            } else {
                this.form.reportValidity();
            }
        },
        cancel: function () {
            this.close();
        },
        close: function () {
            this.isModalOpen = false;
            this.back_to_assessor = {
                reason: '',
            };
            this.errorString = '';
        },
        backToAssessor: function () {
            let vm = this;
            vm.errorString = '';
            fetch(api_endpoints.occurrence_report + `/${vm.occurrence_report_id}/back_to_assessor/`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(vm.back_to_assessor),
            }).then((response) => {
                swal.fire({
                    title: 'Sent Back',
                    text: `${vm.occurrence_report_number} has been sent back to the assessor with the provided reason.`,
                    icon: 'success',
                    customClass: {
                        confirmButton: 'btn btn-primary',
                    },
                }).then((result) => {
                    vm.$router.go();
                });

            }, (error) => {
                console.log(error);
                vm.errorString = helpers.apiVueResourceError(error);
            });
        },
    },
    mounted: function () {
        this.form = document.forms['back-to-assessor-form'];
    }
}
</script>
