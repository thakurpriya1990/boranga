<template lang="html">
    <div class="container">
        <form :action="ocr_proposal_form_url" method="post" name="new_ocr_proposal" enctype="multipart/form-data">

            <div v-if="!ocr_proposal_readonly">
                <div v-if="hasAmendmentRequest" class="row">
                    <div class="col-lg-12 pull-right">
                        <FormSection :formCollapse="false"
                            label="One or more amendments have been requested for this Occurrence Report"
                            Index="amendment_request" customColor="red">
                            <ul class="list-group list-group-numbered ps-2">
                                <li v-for="a in amendment_request"
                                    class="list-group-item d-flex justify-content-between align-items-start">
                                    <div class="ms-4 me-auto">
                                        <div><span class="fw-bold">Reason:</span> {{ a.reason }}</div>
                                        <p v-for="t in splitText(a.text)">{{ t }}</p>
                                        <template
                                            v-if="a.amendment_request_documents && a.amendment_request_documents.length > 0">
                                            <div class="fw-bold mb-1">Documents:</div>
                                            <ul class="list-group list-group-numbered mb-2">
                                                <li v-for="document in a.amendment_request_documents"
                                                    class="list-group-item">
                                                    <i class="bi bi-file-earmark-text-fill text-secondary"></i> <a
                                                        :href="document._file" target="_blank">{{
                                                            document.name }}</a>
                                                </li>
                                            </ul>
                                        </template>
                                    </div>
                                </li>
                            </ul>
                        </FormSection>
                    </div>
                </div>
            </div>

            <div v-if="occurrence_report_obj" id="scrollspy-heading" class="col-lg-12">
                <h4>Occurrence Report - {{ display_group_type }}: {{ occurrence_report_obj.occurrence_report_number }}
                </h4>
            </div>

            <ProposalOccurrenceReport v-if="occurrence_report_obj" :occurrence_report_obj="occurrence_report_obj"
                id="OccurrenceReportStart" :canEditStatus="canEditStatus" :is_external="true" ref="occurrence_report"
                @refreshFromResponse="refreshFromResponse">
            </ProposalOccurrenceReport>

            <div>
                <input type="hidden" name="csrfmiddlewaretoken" :value="csrf_token" />
                <input type='hidden' name="occurrence_report_id" :value="1" />
                <div class="row" style="margin-bottom: 50px">
                    <div class="container">
                        <div class="row" style="margin-bottom: 50px">
                            <div class="navbar fixed-bottom" style="background-color: #f5f5f5;">
                                <div v-if="occurrence_report_obj && !occurrence_report_obj.readonly" class="container">
                                    <div class="col-md-12 text-end" style="margin-top:5px">
                                        <button v-if="savingOCRProposal" type="button" class="btn btn-primary me-2"
                                            disabled>Save
                                            and Continue&nbsp;
                                            <i class="fa fa-circle-o-notch fa-spin fa-fw"></i></button>
                                        <input v-else type="button" @click.prevent="save" class="btn btn-primary me-2"
                                            value="Save and Continue" :disabled="saveExitOCRProposal || submitting" />

                                        <button v-if="saveExitOCRProposal" type="button" class="btn btn-primary me-2"
                                            disabled>Save
                                            and Exit&nbsp;
                                            <i class="fa fa-circle-o-notch fa-spin fa-fw"></i></button>
                                        <input v-else type="button" @click.prevent="save_exit"
                                            class="btn btn-primary me-2" value="Save and Exit"
                                            :disabled="savingOCRProposal || submitting" />

                                        <button v-if="submitting" type="button" class="btn btn-primary" disabled>{{
                                            submit_text() }}&nbsp;
                                            <i class="fa fa-circle-o-notch fa-spin fa-fw"></i></button>
                                        <input v-else type="button" @click.prevent="submit" class="btn btn-primary"
                                            :value="submit_text()"
                                            :disabled="saveExitOCRProposal || savingOCRProposal" />
                                        <input id="save_and_continue_btn" type="hidden" @click.prevent="save_wo_confirm"
                                            class="btn btn-primary" value="Save Without Confirmation" />
                                    </div>
                                </div>
                                <div v-else class="container">
                                    <p class="pull-right" style="margin-top:5px;">
                                        <router-link class="btn btn-primary"
                                            :to="{ name: 'external-occurrence_report-dash' }">Back
                                            to
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
import ProposalOccurrenceReport from '@/components/form_occurrence_report.vue'
import FormSection from '@/components/forms/section_toggle.vue';
import {
    api_endpoints,
    helpers
}
    from '@/utils/hooks'
export default {
    name: 'ExternalOccurrenceReportProposal',
    data: function () {
        return {
            "proposal": null,
            "occurrence_report_obj": null,
            "loading": [],
            form: null,
            amendment_request: [],
            saveError: false,
            ocr_proposal_readonly: true,
            hasAmendmentRequest: false,
            submitting: false,
            saveExitOCRProposal: false,
            savingOCRProposal: false,
            paySubmitting: false,
            newText: "",
            pBody: 'pBody',
            missing_fields: [],
            isSaved: false,
        }
    },
    components: {
        ProposalOccurrenceReport,
        FormSection,
    },
    computed: {
        isLoading: function () {
            return this.loading.length > 0
        },
        csrf_token: function () {
            return helpers.getCookie('csrftoken')
        },
        ocr_proposal_form_url: function () {
            return (this.occurrence_report_obj) ? `/api/occurrence_report/${this.occurrence_report_obj.id}/draft.json` : '';
        },
        canEditStatus: function () {
            return this.occurrence_report_obj ? this.occurrence_report_obj.can_user_edit : 'false';
        },
        display_group_type: function () {
            let group_type_string = this.occurrence_report_obj.group_type
            // to Capitalize only first character
            return group_type_string.charAt(0).toUpperCase() + group_type_string.slice(1);
        },
    },
    methods: {
        submit_text: function () {
            let vm = this;
            return 'Submit';
        },
        set_formData: function (e) {
            let vm = this;
            let formData = new FormData(vm.form);
            return formData;
        },
        save: async function () {
            let vm = this;
            var missing_data = vm.can_submit("");
            if (missing_data != true) {
                swal.fire({
                    title: "Please fix following errors before saving",
                    text: missing_data,
                    icon: 'error',
                    confirmButtonColor: '#226fbb',
                })
                return false;
            }
            vm.savingOCRProposal = true;
            vm.isSaved = false;
            // add map geometry to the occurrence_report_obj
            if (vm.$refs.occurrence_report.$refs.ocr_location.$refs.component_map) {
                vm.occurrence_report_obj.ocr_geometry = vm.$refs.occurrence_report.$refs.ocr_location.$refs.component_map.getJSONFeatures();

            }
            let payload = { proposal: vm.occurrence_report_obj };

            let deleted_features = this.$refs.occurrence_report.$refs.ocr_location.$refs.component_map.deletedFeaturesProperty();
            // Save right away if there are no deleted features, otherwise ask for confirmation
            let commence_saving = deleted_features.length == 0 ? true : false;

            let warning_text = `${deleted_features.length} ${deleted_features.length == 1 ? 'feature' : 'features'
                } will be deleted. Are you sure?`;
            if (deleted_features.length > 0) {
                await swal
                    .fire({
                        title: 'Save Report',
                        text: warning_text,
                        icon: 'warning',
                        showCancelButton: true,
                        confirmButtonText: 'Continue',
                    })
                    .then(async (result) => {
                        if (result.isConfirmed) {
                            // When Yes
                            commence_saving = true;
                        }
                    });
            }

            if (!commence_saving) {
                vm.savingOCRProposal = false;
                return;
            }

            if (vm.submitting) {
                // Provide an action to have the backend lock the geometry
                payload.action = 'submit';
            }
            const res = await vm.$http.post(vm.ocr_proposal_form_url, payload).then(res => {
                swal.fire({
                    title: 'Saved',
                    text: 'Your report has been saved',
                    icon: 'success',
                });
                vm.savingOCRProposal = false;
                const resData = res.data;
                this.occurrence_report_obj = Object.assign({}, resData);
                this.$nextTick(async () => {
                    this.$refs.occurrence_report.$refs.ocr_location.incrementComponentMapKey();
                });
                vm.isSaved = true;
                return resData;
            }, err => {
                var errorText = helpers.apiVueResourceError(err);
                swal.fire({
                    title: 'Save Error',
                    text: errorText,
                    icon: 'error',
                    confirmButtonColor: '#226fbb',
                });
                vm.savingOCRProposal = false;
                vm.isSaved = false;
            });
        },
        save_exit: async function () {
            let vm = this;
            // this.submitting = true;
            var missing_data = vm.can_submit("");
            if (missing_data != true) {
                swal.fire({
                    title: "Please fix following errors before saving",
                    text: missing_data,
                    icon: 'error',
                    confirmButtonColor: '#226fbb',
                })
                return false;
            }
            this.saveExitOCRProposal = true;
            // this also resolves the bug of not updating the datatable when router is pushed back to dashboard
            await this.save().then(() => {
                if (vm.isSaved === true) {
                    vm.$router.push({
                        name: 'external-occurrence_report-dash',
                    });
                } else {
                    this.saveExitOCRProposal = false;
                }
            });
        },
        save_wo_confirm: function (e) {
            let vm = this;
            let formData = vm.set_formData()

            vm.$http.post(vm.ocr_proposal_form_url, formData);
        },
        save_before_submit: async function (e) {
            console.log('save before submit');
            let vm = this;
            vm.saveError = false;
            // add map geometry to the occurrence_report_obj
            if (vm.$refs.occurrence_report.$refs.ocr_location.$refs.component_map) {
                vm.occurrence_report_obj.ocr_geometry = vm.$refs.occurrence_report.$refs.ocr_location.$refs.component_map.getJSONFeatures();

            }
            let payload = { proposal: vm.occurrence_report_obj };
            let deleted_features = this.$refs.occurrence_report.$refs.ocr_location.$refs.component_map.deletedFeaturesProperty();
            // Save right away if there are no deleted features, otherwise ask for confirmation
            let commence_saving = deleted_features.length == 0 ? true : false;

            let warning_text = `${deleted_features.length} ${deleted_features.length == 1 ? 'feature' : 'features'
                } will be deleted. Are you sure?`;
            if (deleted_features.length > 0) {
                await swal
                    .fire({
                        title: 'Save Report',
                        text: warning_text,
                        icon: 'warning',
                        showCancelButton: true,
                        confirmButtonText: 'Continue',
                    })
                    .then(async (result) => {
                        if (result.isConfirmed) {
                            // When Yes
                            commence_saving = true;
                        }
                    });
            }

            if (!commence_saving) {
                vm.submitting = false;
                return;
            }

            if (vm.submitting) {
                // Provide an action to have the backend lock the geometry
                payload.action = 'submit';
            }
            const result = await vm.$http.post(vm.ocr_proposal_form_url, payload).then(res => {
                this.$nextTick(async () => {
                    this.$refs.occurrence_report.$refs.ocr_location.incrementComponentMapKey();
                });
            }, err => {
                var errorText = helpers.apiVueResourceError(err);
                swal.fire({
                    title: 'Submit Error',
                    text: errorText,
                    icon: 'error',
                    confirmButtonColor: '#226fbb',
                });
                vm.submitting = false;
                vm.saveError = true;
            });
            return result;
        },
        setdata: function (readonly) {
            this.ocr_proposal_readonly = readonly;
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
            if (!vm.ocr_proposal_readonly && !vm.submitting) {
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
        validate: function () {
            let vm = this;

            // reset default colour
            for (var field of vm.missing_fields) {
                $("#" + field.id).css("color", '#515151');
            }
            vm.missing_fields = [];

            // get all required fields, that are not hidden in the DOM
            var required_fields = $('input[type=text]:required, textarea:required, input[type=checkbox]:required, input[type=radio]:required, input[type=file]:required, select:required').not(':hidden');

            // loop through all (non-hidden) required fields, and check data has been entered
            required_fields.each(function () {
                var id = 'id_' + this.name
                if (this.type == 'radio') {
                    if (!$("input[name=" + this.name + "]").is(':checked')) {
                        var text = $('#' + id).text()
                        console.log('radio not checked: ' + this.type + ' ' + text)
                        vm.missing_fields.push({ id: id, label: text });
                    }
                }

                if (this.type == 'checkbox') {
                    var id = 'id_' + this.classList['value']
                    if ($("[class=" + this.classList['value'] + "]:checked").length == 0) {
                        var text = $('#' + id).text()
                        console.log('checkbox not checked: ' + this.type + ' ' + text)
                        vm.missing_fields.push({ id: id, label: text });
                    }
                }

                if (this.type == 'select-one') {
                    if ($(this).val() == '') {
                        var text = $('#' + id).text()  // this is the (question) label
                        var id = 'id_' + $(this).prop('name'); // the label id
                        console.log('selector not selected: ' + this.type + ' ' + text)
                        vm.missing_fields.push({ id: id, label: text });
                    }
                }

                if (this.type == 'file') {
                    var num_files = $('#' + id).attr('num_files')
                    if (num_files == "0") {
                        var text = $('#' + id).text()
                        console.log('file not uploaded: ' + this.type + ' ' + this.name)
                        vm.missing_fields.push({ id: id, label: text });
                    }
                }

                if (this.type == 'text') {
                    if (this.value == '') {
                        var text = $('#' + id).text()
                        console.log('text not provided: ' + this.type + ' ' + this.name)
                        vm.missing_fields.push({ id: id, label: text });
                    }
                }

                if (this.type == 'textarea') {
                    if (this.value == '') {
                        var text = $('#' + id).text()
                        console.log('textarea not provided: ' + this.type + ' ' + this.name)
                        vm.missing_fields.push({ id: id, label: text });
                    }
                }
            });

            return vm.missing_fields.length
        },
        can_submit: function (check_action) {
            let vm = this;
            let blank_fields = []
            blank_fields = vm.can_submit_occurrence_report(check_action);

            if (blank_fields.length == 0) {
                return true;
            }
            else {
                return blank_fields;
            }

        },
        can_submit_occurrence_report: function (check_action) {
            let vm = this;
            let blank_fields = []
            if (vm.occurrence_report_obj.group_type == 'flora' || vm.occurrence_report_obj.group_type == 'fauna') {
                if (vm.occurrence_report_obj.species_id == null || vm.occurrence_report_obj.species_id == '') {
                    blank_fields.push(' Scientific Name is missing')
                }
            }
            else {
                if (vm.occurrence_report_obj.community_id == null || vm.occurrence_report_obj.community_id == '') {
                    blank_fields.push(' Community Name is missing')
                }
            }
            if (check_action == "submit") {
                //TODO add validation for fields required before submit
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
                    confirmButtonColor: '#226fbb',
                })
                return false;
            }

            // remove the confirm prompt when navigating away from window (on button 'Submit' click)
            vm.submitting = true;

            swal.fire({
                title: vm.submit_text() + " Report",
                text: "Are you sure you want to " + vm.submit_text().toLowerCase() + " this report?",
                icon: "question",
                showCancelButton: true,
                confirmButtonText: vm.submit_text(),
                confirmButtonColor: '#226fbb',
            }).then(async (swalresult) => {
                if (swalresult.isConfirmed) {
                    /* just save and submit - no payment required (probably application was pushed back by assessor for amendment */
                    let result = await vm.save_before_submit()
                    if (!vm.saveError) {
                        let payload = new Object();
                        Object.assign(payload, vm.occurrence_report_obj);
                        vm.$http.post(helpers.add_endpoint_json(api_endpoints.occurrence_report, vm.occurrence_report_obj.id + '/submit'), payload).then(res => {
                            vm.occurrence_report_obj = res.body;
                            vm.$router.push({
                                name: 'submit_ocr_proposal',
                                params: { occurrence_report_obj: vm.occurrence_report_obj }
                            });
                        }, err => {
                            swal.fire({
                                title: 'Submit Error',
                                text: helpers.apiVueResourceError(err),
                                icon: 'error',
                                confirmButtonColor: '#226fbb',
                            });
                        });
                    }
                }
            }, (error) => {
                vm.submitting = false;
            });
        },
        refreshFromResponse: function (data) {
            this.occurrence_report_obj = Object.assign({}, data);
        },
    },
    mounted: function () {
        let vm = this;
        vm.form = document.forms.new_ocr_proposal;
        window.addEventListener('beforeunload', vm.leaving);
        window.addEventListener('onblur', vm.leaving);
    },
    beforeRouteEnter: function (to, from, next) {
        if (to.params.occurrence_report_id) {
            let vm = this;
            Vue.http.get(`/api/occurrence_report/${to.params.occurrence_report_id}.json`).then(res => {
                next(vm => {
                    vm.loading.push('occurrence report proposal')
                    vm.occurrence_report_obj = res.body;
                    vm.loading.splice('fetching occurrence report proposal', 1);
                    vm.setdata(vm.occurrence_report_obj.readonly);

                    Vue.http.get(helpers.add_endpoint_json(api_endpoints.occurrence_report, to.params.occurrence_report_id + '/amendment_request')).then((res) => {

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
            Vue.http.post('/api/occurrence_report.json').then(res => {
                next(vm => {
                    vm.loading.push('fetching occurrence report proposal')
                    vm.occurrence_report_obj = res.body;
                    vm.loading.splice('fetching occurrence report proposal', 1);
                });
            },
                err => {
                    console.log(err);
                });
        }
    }
}
</script>
