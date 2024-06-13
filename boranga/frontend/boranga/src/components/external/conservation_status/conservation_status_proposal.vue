<template lang="html">
    <div class="container">
        <form :action="cs_proposal_form_url" method="post" name="new_cs_proposal" enctype="multipart/form-data">
            <div v-if="!cs_proposal_readonly">
                <div v-if="hasAmendmentRequest" class="row">
                    <div class="col-lg-12 pull-right">
                        <FormSection :formCollapse="false" label="An amendment has been requested for this Application"
                            Index="amendment_request" customColor="red">
                            <div v-for="a in amendment_request">
                                <p>Reason: {{ a.reason }}</p>
                                <p>Details:
                                <p v-for="t in splitText(a.text)">{{ t }}</p>
                                </p>
                            </div>
                        </FormSection>
                    </div>
                </div>
            </div>
            <div v-if="conservation_status_obj" id="scrollspy-heading" class="col-lg-12 mb-3">
                <h4>Conservation List - {{ display_group_type }} Application: {{
                    conservation_status_obj.conservation_status_number }}</h4>
            </div>
            <ProposalConservationStatus v-if="conservation_status_obj"
                :conservation_status_obj="conservation_status_obj" id="ConservationStatusStart"
                :canEditStatus="canEditStatus" :is_external="true" ref="conservation_status">
            </ProposalConservationStatus>
            <div>
                <input type="hidden" name="csrfmiddlewaretoken" :value="csrf_token" />
                <input type='hidden' name="conservation_status_id" :value="1" />

                <div class="row" style="margin-bottom: 50px">
                    <div class="container">
                        <div class="row" style="margin-bottom: 50px">
                            <div class="navbar fixed-bottom" style="background-color: #f5f5f5;">
                                <div v-if="conservation_status_obj && !conservation_status_obj.readonly"
                                    class="container">
                                    <div class="col-md-12 text-end" style="margin-top:5px">
                                        <button v-if="savingCSProposal" type="button" class="btn btn-primary me-2"
                                            disabled>Save and Continue&nbsp;
                                            <i class="fa fa-circle-o-notch fa-spin fa-fw"></i></button>
                                        <input v-else type="button" @click.prevent="save" class="btn btn-primary me-2"
                                            value="Save and Continue" :disabled="saveExitCSProposal || paySubmitting" />

                                        <button v-if="saveExitCSProposal" type="button" class="btn btn-primary me-2"
                                            disabled>Save and Exit&nbsp;
                                            <i class="fa fa-circle-o-notch fa-spin fa-fw"></i></button>
                                        <input v-else type="button" @click.prevent="save_exit"
                                            class="btn btn-primary me-2" value="Save and Exit"
                                            :disabled="savingCSProposal || paySubmitting" />

                                        <button v-if="paySubmitting" type="button" class="btn btn-primary" disabled>Submit&nbsp;
                                            <i class="fa fa-circle-o-notch fa-spin fa-fw"></i></button>
                                        <input v-else type="button" @click.prevent="submit" class="btn btn-primary"
                                            :value="'Submit'" :disabled="saveExitCSProposal || savingCSProposal" />
                                        <input id="save_and_continue_btn" type="hidden" @click.prevent="save_wo_confirm"
                                            class="btn btn-primary" value="Save Without Confirmation" />
                                    </div>
                                </div>
                                <div v-else class="container">
                                    <p class="pull-right" style="margin-top:5px;">
                                        <router-link class="btn btn-primary"
                                            :to="{ name: 'external-conservation_status-dash' }">Back to
                                            Dashboard</router-link>
                                    </p>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </form>
    </div>
</template>
<script>
import Vue from 'vue'
import ProposalConservationStatus from '@/components/form_conservation_status.vue'
import FormSection from '@/components/forms/section_toggle.vue';
import {
    api_endpoints,
    helpers
}
    from '@/utils/hooks'
export default {
    name: 'ExternalConservationStatusProposal',
    data: function () {
        return {
            "proposal": null,
            "conservation_status_obj": null,
            form: null,
            amendment_request: [],
            saveError: false,
            proposal_readonly: true,
            cs_proposal_readonly: true,
            hasAmendmentRequest: false,
            submitting: false,
            saveExitCSProposal: false,
            savingCSProposal: false,
            paySubmitting: false,
            newText: "",
            pBody: 'pBody',
            missing_fields: [],
            proposal_parks: null,
            isSaved: false,
        }
    },
    components: {
        ProposalConservationStatus,
        FormSection,
    },
    computed: {
        csrf_token: function () {
            return helpers.getCookie('csrftoken')
        },
        cs_proposal_form_url: function () {
            return (this.conservation_status_obj) ? `/api/conservation_status/${this.conservation_status_obj.id}/draft.json` : '';
        },
        application_fee_url: function () {
            return (this.proposal) ? `/application_fee/${this.proposal.id}/` : '';
        },
        proposal_submit_url: function () {
            return (this.proposal) ? `/api/proposal/${this.proposal.id}/submit.json` : '';
            //return this.submit();
        },
        canEditActivities: function () {
            return this.conservation_status_obj ? this.conservation_status_obj.can_user_edit : 'false';
        },
        canEditStatus: function () {
            return this.conservation_status_obj ? this.conservation_status_obj.can_user_edit : 'false';
        },
        canEditPeriod: function () {
            return this.proposal ? this.conservation_status_obj.can_user_edit : 'false';
        },
        application_type_tclass: function () {
            return api_endpoints.t_class;
        },
        application_type_filming: function () {
            return api_endpoints.filming;
        },
        application_type_event: function () {
            return api_endpoints.event;
        },
        display_group_type: function () {
            let group_type_string = this.conservation_status_obj.group_type
            // to Capitalize only first character
            return group_type_string.charAt(0).toUpperCase() + group_type_string.slice(1);
        },
    },
    methods: {
        set_formData: function (e) {
            let vm = this;
            let formData = new FormData(vm.form);
            return formData;
        },
        save: async function (e) {
            let vm = this;
            var missing_data = vm.can_submit("");
            if (missing_data != true) {
                swal.fire({
                    title: "Please fix following errors before saving",
                    text: missing_data,
                    icon: 'error',
                    confirmButtonColor: '#226fbb'
                })
                return false;
            }
            vm.savingCSProposal = true;
            vm.isSaved = false;
            let payload = new Object();
            Object.assign(payload, vm.conservation_status_obj);
            await vm.$http.post(vm.cs_proposal_form_url, payload).then(res => {
                swal.fire({
                    title: 'Proposal Saved',
                    text: 'Your conservation status proposal has been saved',
                    icon: 'success',
                    confirmButtonColor: '#226fbb'
                });;
                vm.savingCSProposal = false;
                vm.isSaved = true;
            }, err => {
                var errorText = helpers.apiVueResourceError(err);
                swal.fire({
                    title: 'Save Error',
                    text: errorText,
                    icon: 'error',
                    confirmButtonColor: '#226fbb'
                });
                vm.savingCSProposal = false;
                vm.isSaved = false;
            });
        },
        save_exit: async function (e) {
            let vm = this;
            var missing_data = vm.can_submit("");
            if (missing_data != true) {
                swal.fire({
                    title: "Please fix following errors before saving",
                    text: missing_data,
                    icon: 'error',
                    confirmButtonColor: '#226fbb'
                })
                return false;
            }
            this.submitting = true;
            this.saveExitCSProposal = true;
            await this.save(e).then(() => {
                if (vm.isSaved === true) {
                    // redirect back to dashboard
                    vm.$router.push({
                        name: 'external-conservation_status-dash'
                    });
                } else {
                    this.saveExitCSProposal = false;
                }
            });
        },
        save_wo_confirm: function (e) {
            let vm = this;
            let formData = vm.set_formData()

            vm.$http.post(vm.cs_proposal_form_url, formData);
        },
        save_before_submit: async function (e) {
            let vm = this;
            vm.saveError = false;

            let payload = new Object();
            Object.assign(payload, vm.conservation_status_obj);
            const result = await vm.$http.post(vm.cs_proposal_form_url, payload).then(res => {
            }, err => {
                var errorText = helpers.apiVueResourceError(err);
                swal.fire({
                    title: 'Submit Error',
                    text: errorText,
                    icon: 'error',
                    confirmButtonColor: '#226fbb'
                });
                vm.paySubmitting = false;
                vm.saveError = true;
            });
            return result;
        },
        setdata: function (readonly) {
            this.cs_proposal_readonly = readonly;
        },
        setAmendmentData: function (amendment_request) {
            this.amendment_request = amendment_request;

            if (amendment_request.length > 0)
                this.hasAmendmentRequest = true;

        },
        splitText: function (aText) {
            let newText = '';
            newText = aText.split("\n");
            return newText;

        },
        leaving: function (e) {
            let vm = this;
            var dialogText = 'You have some unsaved changes.';
            if (!vm.cs_proposal_readonly && !vm.submitting) {
                e.returnValue = dialogText;
                return dialogText;
            }
            else {
                return null;
            }
        },
        highlight_missing_fields: function () {
            let vm = this;
            for (var missing_field of vm.missing_fields) {
                $("#" + missing_field.id).css("color", 'red');
            }
        },
        validateConservationStatusListsCategories: function (blank_fields) {
            let required_fields = [
                { 'id': 'wa_legislative_list_id', 'display': 'WA Legislative List' },
                { 'id': 'wa_priority_list_id', 'display': 'WA Priority List' },
            ];
            for (let field of required_fields) {
                if (this.conservation_status_obj[field.id] != null && this.conservation_status_obj[field.id] != '') {
                    return blank_fields;
                }
            }
            blank_fields.push(`At least one of the following fields are required: ${required_fields.map(f => f.display).join(', ')}`);
            return blank_fields;
        },
        can_submit: function (check_action) {
            let vm = this;
            let blank_fields = []
            // TODO check blank
            blank_fields = vm.can_submit_conservation_status(check_action);

            if (blank_fields.length == 0) {
                return true;
            }
            else {
                return blank_fields;
            }
        },
        can_submit_conservation_status: function (check_action) {
            let vm = this;
            let blank_fields = []
            if (vm.conservation_status_obj.group_type == 'flora' || vm.conservation_status_obj.group_type == 'fauna') {
                if (vm.conservation_status_obj.species_taxonomy_id == null || vm.conservation_status_obj.species_taxonomy_id == '') {
                    blank_fields.push(' Scientific Name is required')
                }
            }
            else {
                if (vm.conservation_status_obj.community_id == null || vm.conservation_status_obj.community_id == '') {
                    blank_fields.push(' Community Name is required')
                }
            }
            if(!vm.conservation_status_obj.submitter_information.submitter_category){
                blank_fields.push(' Please select a submitter category')
            }
            if (check_action == "submit" && (vm.conservation_status_obj.species_taxonomy_id || vm.conservation_status_obj.community_id)) {
                vm.validateConservationStatusListsCategories(blank_fields)
                if (vm.conservation_status_obj.comment == null || vm.conservation_status_obj.comment == '') {
                    blank_fields.push(' Please enter some comments regarding your conservation status proposal.')
                }
            }

            return blank_fields
        },
        submit: function () {
            let vm = this;

            var missing_data = vm.can_submit("submit");
            if (missing_data != true) {
                swal.fire({
                    title: "Please fix following errors before submitting",
                    text: missing_data,
                    icon: 'error',
                    customClass: {
                        confirmButton: 'btn btn-primary',
                    },
                })
                return false;
            }

            // remove the confirm prompt when navigating away from window (on button 'Submit' click)
            vm.submitting = true;
            vm.paySubmitting = true;

            swal.fire({
                title: "Submit Proposal",
                text: "Are you sure you want to submit this conservation status proposal?",
                icon: "question",
                showCancelButton: true,
                confirmButtonText: "Submit Proposal",
                customClass: {
                    confirmButton: 'btn btn-primary',
                    cancelButton: 'btn btn-secondary',
                },
                reverseButtons: true,
            }).then(async (result) => {
                if (result.isConfirmed) {
                    let result = await vm.save_before_submit()
                    if (!vm.saveError) {
                        let payload = new Object();
                        Object.assign(payload, vm.conservation_status_obj);
                        vm.$http.post(helpers.add_endpoint_json(api_endpoints.conservation_status, vm.conservation_status_obj.id + '/submit'), payload).then(res => {
                            vm.conservation_status_obj = res.body;
                            vm.$router.push({
                                name: 'submit_cs_proposal',
                                params: { conservation_status_obj: vm.conservation_status_obj }
                            });
                        }, err => {
                            swal.fire({
                                title: 'Submit Error',
                                text: helpers.apiVueResourceError(err),
                                icon: 'error',
                                confirmButtonColor: '#226fbb'
                            });
                        });
                    }
                } else {
                    vm.submitting = false;
                    vm.paySubmitting = false;
                }
            }, (error) => {
                vm.submitting = true;
                vm.paySubmitting = false;
            });
        },
    },
    created: function () {
        if (!this.conservation_status_obj) {
            Vue.http.get(`/api/conservation_status/${this.$route.params.conservation_status_id}.json`).then(res => {
                this.conservation_status_obj = res.body;
            },
                err => {
                    console.log(err);
                });
        }
    },
    mounted: function () {
        let vm = this;
        vm.form = document.forms.new_cs_proposal;
        window.addEventListener('beforeunload', vm.leaving);
        window.addEventListener('onblur', vm.leaving);
    },
    beforeRouteEnter: function (to, from, next) {
        if (to.params.conservation_status_id) {
            let vm = this;
            Vue.http.get(`/api/conservation_status/${to.params.conservation_status_id}.json`).then(res => {
                next(vm => {
                    vm.conservation_status_obj = res.body;
                    vm.setdata(vm.conservation_status_obj.readonly);
                    Vue.http.get(helpers.add_endpoint_json(api_endpoints.conservation_status, to.params.conservation_status_id + '/amendment_request')).then((res) => {
                        vm.setAmendmentData(res.body);
                    },
                        err => {
                            console.log(err);
                        });
                });
            },
                err => {
                    console.log(err);
                });
        }
        else {
            Vue.http.post('/api/conservation_status.json').then(res => {
                next(vm => {
                    vm.conservation_status_obj = res.body;
                });
            },
                err => {
                    console.log(err);
                });
        }
    }
}
</script>
