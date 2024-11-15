<template lang="html">
    <div id="internal-conservation-status-proposal-propose-for-agenda">
        <modal id="propose-for-agenda-modal" transition="modal fade" @ok="ok()" @cancel="close()"
            :title="`Propose CS${conservation_status_id} for Agenda`" okText="Propose for Agenda" large>
            <div class="container-fluid">
                <div class="row">
                    <form class="form-horizontal needs-validation" id="propose-for-agenda-form"
                        name="propose-for-agenda-form" novalidate>
                        <alert v-if="errors" type="danger"><strong>{{ errors }}</strong></alert>
                        <div class="col-sm-12">
                            <div class="row mb-3">
                                <div class="col">
                                    <div class="form-group">
                                        <label class="control-label mb-3" for="Name">Recommended Action (Decline or
                                            Approve) / Comments</label>
                                        <textarea class="form-control" name="assessor_comment" ref="assessor_comment"
                                            required v-model="assessor_comment"></textarea>
                                        <div class="invalid-feedback">
                                            Please enter your recommended action and any other comments.
                                        </div>
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
    name: 'ProposeForAgenda',
    components: {
        modal,
        alert,
    },
    props: {
        conservation_status_id: {
            type: Number,
        },
    },
    data: function () {
        return {
            assessor_comment: null,
            isModalOpen: false,
            errors: null,
        }
    },
    emits: ['refreshFromResponse'],
    watch: {
        isModalOpen: function (val) {
            if (val) {
                this.$nextTick(() => {
                    $(this.$refs.assessor_comment).focus();
                });
            }
        }
    },
    methods: {
        ok: function () {
            let vm = this;
            var form = document.getElementById('propose-for-agenda-form');
            if (form.checkValidity()) {
                vm.proposeForAgenda();
            } else {
                form.classList.add('was-validated');
                $('#propose-for-agenda-form').find(':invalid').first().focus();
            }
            return false;
        },
        close: function () {
            this.assessor_comment = null;
            this.errors = null;
            this.isModalOpen = false;
        },
        proposeForAgenda: function () {
            let vm = this;
            vm.$http.patch(helpers.add_endpoint_json(api_endpoints.conservation_status, vm.conservation_status_id + '/proposed_for_agenda'), { 'assessor_comment': vm.assessor_comment }).then((response) => {
                vm.$router.push({ path: '/internal/conservation-status/' });
            }, (error) => {
                vm.errors = true;
                vm.errorString = helpers.apiVueResourceError(error);
            });
        }
    },
}
</script>
