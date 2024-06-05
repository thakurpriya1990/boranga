<template>
    <FormSection :formCollapse="false" label="Conservation Status" Index="conservationstatus">
        <form>
            <div class="row mb-3" v-if="is_internal">
                <label for="conservation_status_number" class="col-sm-4 col-form-label">Conservation Status
                    Number:</label>
                <div class="col-sm-8">
                    <a :href="`/internal/conservation_status/${conservation_status.id}`" target="_blank"
                        class="btn btn-primary">{{
                            conservation_status.conservation_status_number }}<i
                            class="bi bi-box-arrow-up-right ps-2"></i></a>
                </div>
            </div>
            </div>
            <fieldset disabled>
                <div class="row mb-3" v-if="conservation_status.wa_legislative_list">
                    <label for="wa_legislative_list" class="col-sm-4 col-form-label">WA Legislative List</label>
                    <div class="col-sm-8">
                        <input class="form-control" id="wa_legislative_list"
                            :value="conservation_status.wa_legislative_list" />
                    </div>
                </div>
                <div class="row mb-3" v-if="conservation_status.wa_legislative_category">
                    <label for="wa_legislative_category" class="col-sm-4 col-form-label">WA Legislative Category</label>
                    <div class="col-sm-8">
                        <input class="form-control" id="wa_legislative_category"
                            :value="conservation_status.wa_legislative_category" />
                    </div>
                </div>
                <div class="row mb-3" v-if="conservation_status.wa_priority_category">
                    <label for="wa_priority_category" class="col-sm-4 col-form-label">WA Priority Category</label>
                    <div class="col-sm-8">
                        <input class="form-control" id="wa_priority_category"
                            :value="conservation_status.wa_priority_category" />
                    </div>
                </div>
                <div class="row mb-3" v-if="conservation_status.commonwealth_conservation_list">
                    <label for="commonwealth_conservation_list" class="col-sm-4 col-form-label">Commonwealth
                        Conservation
                        List</label>
                    <div class="col-sm-8">
                        <input class="form-control" id="commonwealth_conservation_list"
                            :value="conservation_status.commonwealth_conservation_list" />
                    </div>
                </div>
                <div class="row mb-3" v-if="conservation_status.international_conservation">
                    <label for="international_conservation" class="col-sm-4 col-form-label">International
                        Conservation</label>
                    <div class="col-sm-8">
                        <input class="form-control" id="international_conservation"
                            :value="conservation_status.international_conservation" />
                    </div>
                </div>
                <div class="row pb-3 mb-3 border-bottom" v-if="conservation_status.conservation_criteria">
                    <label for="conservation_criteria" class="col-sm-4 col-form-label">Conservation Criteria</label>
                    <div class="col-sm-8">
                        <input class="form-control" id="conservation_criteria"
                            :value="conservation_status.conservation_criteria" />
                    </div>
                </div>
                <div class="row mt-3 mb-1">
                    <label for="" class="col-sm-4 col-form-label">Conservation Status under
                        review?</label>
                    <div class="col-sm-8 d-flex align-items-center">
                        <template v-if="conservation_status.under_review">Yes</template>
                        <template v-else>
                            No
                        </template>
                    </div>
                </div>
            </fieldset>
        </form>
    </FormSection>
</template>

<script>
import FormSection from '@/components/forms/section_toggle.vue';

export default {
    name: "BasicConservationStatus",
    props: {
        conservation_status: {
            type: Object,
            default: null
        },
        is_internal: {
            type: Boolean,
            default: false
        },
    },
    components: {
        FormSection
    },
}
</script>
