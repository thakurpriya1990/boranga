<template>
    <FormSection
        :form-collapse="false"
        label="Conservation Status"
        Index="conservationstatus"
    >
        <form>
            <div v-if="is_internal" class="row mb-3">
                <label
                    for="conservation_status_number"
                    class="col-sm-4 col-form-label"
                    >Conservation Status Number:</label
                >
                <div class="col-sm-8">
                    <a
                        :href="`/internal/conservation-status/${conservation_status.id}`"
                        target="_blank"
                        class="btn btn-primary"
                        >{{ conservation_status.conservation_status_number
                        }}<i class="bi bi-box-arrow-up-right ps-2"></i
                    ></a>
                </div>
            </div>
            <fieldset disabled>
                <div
                    v-if="conservation_status.wa_legislative_list"
                    class="row mb-3"
                >
                    <label
                        for="wa_legislative_list"
                        class="col-sm-4 col-form-label"
                        >WA Legislative List</label
                    >
                    <div class="col-sm-8">
                        <input
                            id="wa_legislative_list"
                            class="form-control"
                            :value="conservation_status.wa_legislative_list"
                        />
                    </div>
                </div>
                <div
                    v-if="conservation_status.wa_legislative_category"
                    class="row mb-3"
                >
                    <label
                        for="wa_legislative_category"
                        class="col-sm-4 col-form-label"
                        >WA Legislative Category</label
                    >
                    <div class="col-sm-8">
                        <input
                            id="wa_legislative_category"
                            class="form-control"
                            :value="conservation_status.wa_legislative_category"
                        />
                    </div>
                </div>
                <div
                    v-if="conservation_status.wa_priority_category"
                    class="row mb-3"
                >
                    <label
                        for="wa_priority_category"
                        class="col-sm-4 col-form-label"
                        >WA Priority Category</label
                    >
                    <div class="col-sm-8">
                        <input
                            id="wa_priority_category"
                            class="form-control"
                            :value="conservation_status.wa_priority_category"
                        />
                    </div>
                </div>
                <div
                    v-if="
                        conservation_status.commonwealth_conservation_category
                    "
                    class="row mb-3"
                >
                    <label
                        for="commonwealth_conservation_category"
                        class="col-sm-4 col-form-label"
                        >Commonwealth Conservation List</label
                    >
                    <div class="col-sm-8">
                        <input
                            id="commonwealth_conservation_category"
                            class="form-control"
                            :value="
                                conservation_status.commonwealth_conservation_category
                            "
                        />
                    </div>
                </div>
                <div
                    v-if="conservation_status.other_conservation_assessment"
                    class="row mb-3"
                >
                    <label
                        for="other_conservation_assessment"
                        class="col-sm-4 col-form-label"
                        >Other Conservation Assessment</label
                    >
                    <div class="col-sm-8">
                        <input
                            id="other_conservation_assessment"
                            class="form-control"
                            :value="
                                conservation_status.other_conservation_assessment
                            "
                        />
                    </div>
                </div>
                <div
                    v-if="conservation_status.conservation_criteria"
                    class="row pb-3 mb-3 border-bottom"
                >
                    <label
                        for="conservation_criteria"
                        class="col-sm-4 col-form-label"
                        >Conservation Criteria</label
                    >
                    <div class="col-sm-8">
                        <input
                            id="conservation_criteria"
                            class="form-control"
                            :value="conservation_status.conservation_criteria"
                        />
                    </div>
                </div>
                <div class="row mt-3 mb-1">
                    <label for="" class="col-sm-4 col-form-label"
                        >Conservation Status under review?</label
                    >
                    <div class="col-sm-8 d-flex align-items-center">
                        <template v-if="conservation_status.under_review"
                            >Yes</template
                        >
                        <template v-else> No </template>
                    </div>
                </div>
            </fieldset>
        </form>
    </FormSection>
</template>

<script>
import FormSection from '@/components/forms/section_toggle.vue';

export default {
    name: 'BasicConservationStatus',
    components: {
        FormSection,
    },
    props: {
        conservation_status: {
            type: Object,
            default: null,
        },
        is_internal: {
            type: Boolean,
            default: false,
        },
    },
};
</script>
