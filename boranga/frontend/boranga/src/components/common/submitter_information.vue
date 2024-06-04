<template>
    <div id="submitter-information">
        <FormSection :formCollapse="false" label="Submitter Information" Index="submitter_information">
            <form id="submitter-information-form" class="needs-validation" novalidate>
                <fieldset :disabled="disabled">
                    <div class="row mb-3">
                        <label for="submitter_category" class="col-sm-2 col-form-label fw-bold">Category <span
                                class="text-danger">*</span></label>
                        <div class="col-sm-6">
                            <select class="form-select" id="submitter_category" ref="submitter_category"
                                v-model="submitter_information.submitter_category" required>
                                <option :value="null" disabled>Please select a submitter category</option>
                                <option v-for="submitter_category in submitter_categories"
                                    :value="submitter_category.id">{{
                                        submitter_category.name }}</option>
                            </select>
                        </div>
                    </div>
                    <div class="row mb-3">
                        <label for="name" class="col-sm-2 col-form-label">Name</label>
                        <div class="col-sm-6">
                            <input type="text" maxlength="100" class="form-control" id="name"
                                v-model="submitter_information.name">
                        </div>
                    </div>
                    <div class="row mb-3 pb-3 border-bottom">
                        <label for="contact_details" class="col-sm-2 col-form-label">Contact Details</label>
                        <div class="col-sm-6">
                            <textarea class="form-control" id="contact_details"
                                v-model="submitter_information.contact_details" rows="4" />
                        </div>
                    </div>
                    <div class="row" :class="show_organisation_information ? 'mb-3' : ''">
                        <label for="" class="col-sm-4 col-form-label">Are you submitting on behalf of an
                            organisation?</label>
                        <div class="col-sm-6 d-flex align-items-center">
                            <div class="form-check form-check-inline" @click="checkOrganisationDetails">
                                <input type="radio" class="form-check-input" id="organisation_no"
                                    v-model="submitting_on_behalf_of_organisation" value="no"
                                    :disabled="organisation_details_entered">
                                <label for="name" class="form-check-label">No</label>
                            </div>
                            <div class="form-check form-check-inline">
                                <input type="radio" class="form-check-input" id="organisation_yes"
                                    v-model="submitting_on_behalf_of_organisation" value="yes"
                                    @change.prevent="focusOrganisation">
                                <label for="name" class="form-check-label">Yes</label>
                            </div>
                        </div>
                    </div>
                    <template v-if="show_organisation_information">
                        <div class="row mb-3">
                            <label for="organisation" class="col-sm-2 col-form-label">Organisation</label>
                            <div class="col-sm-6">
                                <input type="text" maxlength="100" class="form-control" id="organisation"
                                    ref="organisation" v-model="submitter_information.organisation">
                            </div>
                        </div>
                        <div v-if="show_organisation_information" class="row mb-3">
                            <label for="position" class="col-sm-2 col-form-label">Position / Role</label>
                            <div class="col-sm-6">
                                <input type="text" maxlength="100" class="form-control" id="position"
                                    v-model="submitter_information.position">
                            </div>
                        </div>
                    </template>
                </fieldset>
            </form>
        </FormSection>
    </div>
</template>

<script>
import FormSection from '@/components/forms/section_toggle.vue';

import { api_endpoints } from '@/utils/hooks.js'
import { readonly } from 'vue';

export default {
    name: 'SubmitterInformation',
    props: {
        submitter_information: {
            type: Object,
            default: null,
        },
        disabled: {
            type: Boolean,
            default: false,
        },
    },
    components: {
        FormSection,
    },
    data: function () {
        return {
            submitter_categories: null,
            submitting_on_behalf_of_organisation: 'no',
        }
    },
    computed: {
        organisation_details_entered: function () {
            return !!(this.submitter_information.organisation || this.submitter_information.position);
        },
        show_organisation_information: function () {
            return this.submitting_on_behalf_of_organisation == 'yes' || this.organisation_details_entered
        },
    },
    methods: {
        focusOrganisation() {
            this.$nextTick(() => {
                this.$refs.organisation.focus();
            });
        },
        fetchSubmitterCategories: function () {
            fetch(api_endpoints.submitter_categories)
                .then(async response => {
                    this.submitter_categories = await response.json();
                })
                .catch(error => {
                    console.log(error);
                });
        },
        saveSubmitterInformation: function () {
            this.$http.put(api_endpoints.save_submitter_information, this.submitter_information)
                .then(response => response.json())
                .then(data => {
                    console.log(data);
                })
                .catch(error => {
                    console.log(error);
                });
        },
        checkOrganisationDetails: function () {
            if (this.organisation_details_entered) {
                swal.fire({
                    title: 'Remove Organisation Details',
                    text: "To change the answer to 'No' please remove the organisation details first.",
                    icon: 'info',
                    customClass: {
                        confirmButton: 'btn btn-primary',
                    },
                })
            }
        },
    },
    created() {
        this.fetchSubmitterCategories();
        if (this.show_organisation_information) {
            this.submitting_on_behalf_of_organisation = 'yes';
        }
    },
    mounted() {
        let vm = this;
        var form = document.getElementById('submitter-information-form')
        form.addEventListener('change', function (event) {
            if (!form.checkValidity()) {
                event.preventDefault()
                event.stopPropagation()
                form.classList.add('was-validated')
            } else {
                vm.saveSubmitterInformation();
            }
        }, false)
    }
}
</script>
