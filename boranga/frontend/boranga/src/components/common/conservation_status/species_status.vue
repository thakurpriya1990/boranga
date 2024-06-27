<template lang="html">
    <div id="speciesStatus">
        <FormSection :formCollapse="false" label="Conservation Status" Index="conservation_status">
            <form @change="$emit('saveConservationStatus')">
                <template v-if="!is_external">
                    <CollapsibleComponent component_title="Assessment Comments" ref="assessment_comments"
                        :collapsed="false">
                        <div class="row">
                            <div class="col rounded">
                                <div class="row" v-if="deficiencyVisibility">
                                    <div class="col">
                                        <div class="form-floating m-3">
                                            <textarea :disabled="deficiency_readonly" class="form-control"
                                                id="assessor_deficiencies" placeholder="Deficiency Comments"
                                                v-model="conservation_status_obj.deficiency_data" />
                                            <label for="assessor_deficiencies" class="form-label">Deficiency
                                                Comments</label>
                                        </div>
                                    </div>
                                </div>
                                <div class="row" v-if="assessorCommentVisibility">
                                    <div class="col">
                                        <div class="form-floating m-3 mt-1">
                                            <textarea :disabled="assessor_comment_readonly" class="form-control"
                                                rows="3" id="assessor_comment" placeholder="Assessor Comments"
                                                v-model="conservation_status_obj.assessor_data" />
                                            <label for="" class="col-sm-4 col-form-label">Assessor Comments</label>
                                        </div>
                                    </div>
                                </div>
                                <div v-if="referral_comments_boxes.length > 0">
                                    <div>
                                        <div class="row mt-2">
                                            <div class="col ms-3">
                                                <h6 class="text-muted">Referral Comments</h6>
                                            </div>
                                        </div>
                                        <div v-for="ref in referral_comments_boxes" class="row mb-3"
                                            v-if="ref.box_view">
                                            <div class="col">
                                                <div class="form-floating m-3 mt-1">
                                                    <textarea v-if='!ref.readonly' :disabled="true"
                                                        :id="ref.name" :name="ref.name" class="form-control referral-comment-box"
                                                        :placeholder="ref.label" v-model="referral.referral_comment" />
                                                    <textarea v-else :disabled="ref.readonly" :name="ref.name"
                                                        :value="ref.value || ''" class="form-control referral-comment-box"
                                                        :placeholder="ref.label" />
                                                    <label :for="ref.name" class="form-label">{{ ref.label }}</label>
                                                </div>
                                            </div>
                                        </div>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </CollapsibleComponent>
                </template>
                <div class="row mb-3">
                    <label :for="scientific_name_lookup" class="col-sm-4 col-form-label fw-bold">Scientific Name: <span class="text-danger">*</span></label>
                    <div class="col-sm-8" :id="select_scientific_name">
                        <select :disabled="isReadOnly" :id="scientific_name_lookup" :name="scientific_name_lookup"
                            :ref="scientific_name_lookup" class="form-control" />
                    </div>
                </div>
                <div v-if="species_display" class="row mb-3">
                    <label for="species_display" class="col-sm-4 col-form-label"></label>
                    <div class="col-sm-8">
                        <textarea disabled class="form-control" rows="3" id="species_display"
                            v-model="species_display" />
                    </div>
                </div>
                <div v-if="taxon_previous_name" class="row mb-3">
                    <label for="previous_name" class="col-sm-4 col-form-label">Previous Name:</label>
                    <div class="col-sm-8">
                        <input readonly type="text" class="form-control" id="previous_name" placeholder=""
                            v-model="taxon_previous_name" />
                    </div>
                </div>
                <template v-if="show_administrative_information">
                    <div class="row mb-3 border-top pt-3">
                        <h5 class="text-muted mb-4">Administrative Information</h5>
                        <label for="change_code" class="col-sm-4 col-form-label fw-bold">Change Type <span
                                class="text-danger">*</span></label>
                        <div class="col-sm-8">
                            <select :disabled="isReadOnly" class="form-select"
                                v-model="conservation_status_obj.change_code_id" id="change_code">
                                <option :value="null">Select the appropriate Change type</option>
                                <option v-for="option in change_codes" :value="option.id" v-bind:key="option.id">
                                    {{ option.code }}
                                </option>
                            </select>
                        </div>
                    </div>
                    <div class="row mb-3">
                        <label for="approval_level" class="col-sm-4 col-form-label fw-bold">Applicable Workflow <span
                                class="text-danger">*</span></label>
                        <div class="col-sm-8">
                            <select id="approval_level" v-model="conservation_status_obj.approval_level"
                                class="form-select" :disabled="approval_level_disabled" @change="approvalLevelChanged">
                                <option :value="null">Select Appropriate Workflow</option>
                                <option :value="'intermediate'">Intermediate</option>
                                <option :value="'minister'">Ministerial</option>
                            </select>
                        </div>
                    </div>
                    <div v-if="conservation_status_obj.effective_from || conservation_status_obj.effective_to"
                        class="row mb-3 border-top pt-3">
                        <template v-if="conservation_status_obj.effective_from">
                            <label for="effective_from" class="col-sm-3 col-form-label">Effective From:</label>
                            <div class="col-sm-3">
                                <input type="date" placeholder="DD/MM/YYYY" class="form-control" id="effective_from"
                                    v-model="conservation_status_obj.effective_from" :disabled="true" />
                            </div>
                        </template>
                        <template v-if="conservation_status_obj.effective_to">
                            <label for="effective_to" class="col-sm-3 col-form-label">Effective to:</label>
                            <div class="col-sm-3">
                                <input type="date" readonly placeholder="DD/MM/YYYY" class="form-control"
                                    id="effective_to" v-model="conservation_status_obj.effective_to" :disabled="true" />
                            </div>
                        </template>
                    </div>
                    <div v-if="show_listing_and_review_due_date" class="row mb-3"
                        :class="conservation_status_obj.effective_from || conservation_status_obj.effective_to ? '' : 'border-top pt-3'">
                        <label for="listing_date" class="col-sm-3 col-form-label">Date First Listed:</label>
                        <div class="col-sm-3">
                            <input type="date" placeholder="DD/MM/YYYY" class="form-control" id="listing_date"
                                v-model="conservation_status_obj.listing_date"
                                :disabled="listing_and_review_due_date_disabled" />
                        </div>
                        <label for="review_due_date" class="col-sm-3 col-form-label">Review Due Date:</label>
                        <div class="col-sm-3">
                            <input type="date" placeholder="DD/MM/YYYY" class="form-control" id="review_due_date"
                                v-model="conservation_status_obj.review_due_date"
                                :disabled="listing_and_review_due_date_disabled" />
                        </div>
                    </div>
                </template>
                <template v-if="show_proposed_conservation_status">
                    <div class="row mb-3 border-top pt-3">
                        <h5 class="text-muted mb-4"><template v-if="conservation_list_proposed">Proposed
                            </template>Conservation
                            Status</h5>
                        <label for="proposed_wa_legislative_list" class="col-sm-4 col-form-label fw-bold">WA Legislative
                            List <span class="text-warning">*</span></label>
                        <div class="col-sm-8">
                            <select :disabled="isReadOnly" class="form-select"
                                v-model="conservation_status_obj.wa_legislative_list_id"
                                id="proposed_wa_legislative_list" @change="filterWALegislativeCategories($event)">
                                <option :value="null" disabled>Select the appropriate WA Legislative List</option>
                                <option v-for="option in wa_legislative_lists" :value="option.id"
                                    v-bind:key="option.id">
                                    {{ option.code }} - {{ option.label }}
                                </option>
                            </select>
                        </div>
                    </div>
                    <div v-if="conservation_status_obj.wa_legislative_list_id" class="row mb-3">
                        <label for="proposed_wa_legislative_category" class="col-sm-4 col-form-label">WA Legislative
                            Category:</label>
                        <div class="col-sm-8">
                            <select :disabled="isReadOnly" class="form-select"
                                v-model="conservation_status_obj.wa_legislative_category_id"
                                id="proposed_wa_legislative_category">
                                <option :value="null" disabled>Select the appropriate WA Legislative Category</option>
                                <option v-for="option in filtered_wa_legislative_categories" :value="option.id"
                                    v-bind:key="option.id">
                                    {{ option.code }} - {{ option.label }}
                                </option>
                            </select>
                        </div>
                    </div>
                    <div class="row mb-3">
                        <label for="proposed_wa_priority_list" class="col-sm-4 col-form-label fw-bold">WA Priority
                            List <span class="text-warning">*</span></label>
                        <div class="col-sm-8">
                            <select :disabled="isReadOnly" class="form-select"
                                v-model="conservation_status_obj.wa_priority_list_id" id="proposed_wa_priority_list"
                                @change="filterWAPriorityCategories($event)">
                                <option :value="null" disabled>Select the appropriate WA Priority List</option>
                                <option v-for="option in wa_priority_lists" :value="option.id" v-bind:key="option.id">
                                    {{ option.code }} - {{ option.label }}
                                </option>
                            </select>
                        </div>
                    </div>
                    <div v-if="conservation_status_obj.wa_priority_list_id" class="row mb-3">
                        <label for="proposed_wa_priority_category" class="col-sm-4 col-form-label">WA Priority
                            Category:</label>
                        <div class="col-sm-8">
                            <select :disabled="isReadOnly" class="form-select"
                                v-model="conservation_status_obj.wa_priority_category_id"
                                id="proposed_wa_priority_category">
                                <option :value="null" disabled>Select the appropriate WA Priority Category</option>
                                <option v-for="option in filtered_wa_priority_categories" :value="option.id"
                                    v-bind:key="option.id">
                                    {{ option.code }} - {{ option.label }}
                                </option>
                            </select>
                        </div>
                    </div>
                    <div class="row mb-3">
                        <label for="proposed_commonwealth_conservation_list"
                            class="col-sm-4 col-form-label">Commonwealth
                            Conservation
                            List:</label>
                        <div class="col-sm-8">
                            <select :disabled="isReadOnly" class="form-select"
                                v-model="conservation_status_obj.commonwealth_conservation_list_id"
                                id="proposed_commonwealth_conservation_list">
                                <option :value="null" disabled>Select a Commonwealth Conservation List if Applicable
                                </option>
                                <option v-for="option in commonwealth_conservation_lists" :value="option.id"
                                    v-bind:key="option.id">
                                    {{ option.code }} - {{ option.label }}
                                </option>
                            </select>
                        </div>
                    </div>
                    <div class="row mb-3">
                        <label for="proposed_international_conservation" class="col-sm-4 col-form-label">International
                            Conservation:</label>
                        <div class="col-sm-8">
                            <input :disabled="isReadOnly" type="text" class="form-control"
                                id="proposed_international_conservation"
                                placeholder="Enter International Conservation Details if Applicable"
                                v-model="conservation_status_obj.international_conservation" />
                        </div>
                    </div>
                    <div class="row mb-3">
                        <label for="proposed_conservation_criteria" class="col-sm-4 col-form-label">Conservation
                            Criteria:</label>
                        <div class="col-sm-8">
                            <input :disabled="isReadOnly" type="text" class="form-control"
                                id="proposed_conservation_criteria"
                                placeholder="Enter Conservation Criteria if Applicable"
                                v-model="conservation_status_obj.conservation_criteria" />
                        </div>
                    </div>
                    <div class="row mb-3">
                        <label for="comment" class="col-sm-4 col-form-label fw-bold">Comments <span
                                class="text-danger">*</span></label>
                        <div class="col-sm-8">
                            <textarea :disabled="isReadOnly" class="form-control" rows="3" id="comment" placeholder=""
                                v-model="conservation_status_obj.comment" />
                        </div>
                    </div>
                    <div v-if="!is_external" class="row mb-3">
                        <label for="conservation_status_under_review" class="col-sm-6 col-form-label">Is there a
                            Conservation Status
                            proposal under review?</label>
                        <div class="col-sm-6 d-flex align-items-center">
                            <div class="form-check form-check-inline">
                                Yes <input disabled type="radio" id="conservation_status_under_review_yes"
                                    class="form-check-input" name="conservation_status_under_review"
                                    v-model="isConservationStatusUnderReview" :value="true" />
                            </div>
                            <div class="form-check form-check-inline">
                                No <input disabled type="radio" id="conservation_status_under_review_no"
                                    class="form-check-input" name="conservation_status_under_review"
                                    v-model="isConservationStatusUnderReview" :value="false" />
                            </div>
                            <div
                                v-if="conservation_status_obj.conservation_status_under_review && conservation_status_obj.id != conservation_status_obj.conservation_status_under_review.id">
                                <div>
                                    <a :href="`/internal/conservation_status/${conservation_status_obj.conservation_status_under_review.id}`"
                                        target="_blank" class="btn btn-primary">{{
                                            conservation_status_obj.conservation_status_under_review.conservation_status_number
                                        }}<i class="bi bi-box-arrow-up-right ps-2"></i></a>
                                </div>
                            </div>
                        </div>
                    </div>
                </template>
                <template v-if="canViewCurrentList && conservation_status_obj.current_conservation_status">
                    <div class="row border-top pt-3">
                        <h5 class="text-muted mb-4">Current Conservation
                            Status</h5>
                    </div>
                    <div class="row mb-3">
                        <label for="conservation_status_number" class="col-sm-4 col-form-label">Conservation Status
                            Number:</label>
                        <div class="col-sm-8">
                            <a :href="`/internal/conservation_status/${conservation_status_obj.current_conservation_status.id}`"
                                target="_blank" class="btn btn-primary">{{
                                    conservation_status_obj.current_conservation_status.conservation_status_number }}<i
                                    class="bi bi-box-arrow-up-right ps-2"></i></a>
                        </div>
                    </div>
                    <div v-if="conservation_status_obj.current_conservation_status.wa_legislative_list_id"
                        class="row mb-3">
                        <label for="current_wa_legislative_list" class="col-sm-4 col-form-label">WA Legislative
                            List:</label>
                        <div class="col-sm-8">
                            <select :disabled="true" class="form-select"
                                v-model="conservation_status_obj.current_conservation_status.wa_legislative_list_id"
                                id="current_wa_legislative_list" @change="filterWALegislativeCategories($event)">
                                <option v-for="option in wa_legislative_lists" :value="option.id"
                                    v-bind:key="option.id">
                                    {{ option.code }}
                                </option>
                            </select>
                        </div>
                    </div>
                    <div v-if="conservation_status_obj.current_conservation_status.wa_legislative_category_id"
                        class="row mb-3">
                        <label for="current_wa_legislative_category" class="col-sm-4 col-form-label">WA Legislative
                            Category:</label>
                        <div class="col-sm-8">
                            <select :disabled="true" class="form-select"
                                v-model="conservation_status_obj.current_conservation_status.wa_legislative_category_id"
                                id="current_wa_legislative_category">
                                <option v-for="option in wa_legislative_categories" :value="option.id"
                                    v-bind:key="option.id">
                                    {{ option.code }}
                                </option>
                            </select>
                        </div>
                    </div>
                    <div v-if="conservation_status_obj.current_conservation_status.wa_priority_list_id"
                        class="row mb-3">
                        <label for="current_wa_priority_list" class="col-sm-4 col-form-label">WA Priority List:</label>
                        <div class="col-sm-8">
                            <select :disabled="true" class="form-select"
                                v-model="conservation_status_obj.current_conservation_status.wa_priority_list_id"
                                id="current_wa_priority_list" @change="filterWAPriorityCategories($event)">
                                <option v-for="option in wa_priority_lists" :value="option.id" v-bind:key="option.id">
                                    {{ option.code }}
                                </option>
                            </select>
                        </div>
                    </div>
                    <div v-if="conservation_status_obj.current_conservation_status.wa_priority_category_id"
                        class="row mb-3">
                        <label for="current_wa_priority_category" class="col-sm-4 col-form-label">WA Priority
                            Category:</label>
                        <div class="col-sm-8">
                            <select :disabled="true" class="form-select"
                                v-model="conservation_status_obj.current_conservation_status.wa_priority_category_id"
                                id="current_wa_priority_category">
                                <option v-for="option in wa_priority_categories" :value="option.id"
                                    v-bind:key="option.id">
                                    {{ option.code }}
                                </option>
                            </select>
                        </div>
                    </div>
                    <div v-if="conservation_status_obj.current_conservation_status.commonwealth_conservation_list_id"
                        class="row mb-3">
                        <label for="current_commonwealth_conservation_list" class="col-sm-4 col-form-label">Commonwealth
                            Conservation List:</label>
                        <div class="col-sm-8">
                            <select :disabled="true" class="form-select"
                                v-model="conservation_status_obj.current_conservation_status.commonwealth_conservation_list_id"
                                id="current_commonwealth_conservation_list">
                                <option v-for="option in commonwealth_conservation_lists" :value="option.id"
                                    v-bind:key="option.id">
                                    {{ option.code }}
                                </option>
                            </select>
                        </div>
                    </div>
                    <div v-if="conservation_status_obj.current_conservation_status.international_conservation"
                        class="row mb-3">
                        <label for="current_international_conservation" class="col-sm-4 col-form-label">International
                            Conservation:</label>
                        <div class="col-sm-8">
                            <input :disabled="true" type="text" class="form-control"
                                id="current_international_conservation"
                                v-model="conservation_status_obj.current_conservation_status.international_conservation" />
                        </div>
                    </div>
                    <div v-if="conservation_status_obj.current_conservation_status.conservation_criteria"
                        class="row mb-3">
                        <label for="current_conservation_criteria" class="col-sm-4 col-form-label">Conservation
                            Criteria:</label>
                        <div class="col-sm-8">
                            <input :disabled="true" type="text" class="form-control" id="current_conservation_criteria"
                                v-model="conservation_status_obj.current_conservation_status.conservation_criteria" />
                        </div>
                    </div>
                </template>
                <template v-if="conservation_status_obj.can_view_recommended">
                    <div class="row mb-3 border-top pt-3">
                        <h5 class="text-muted mb-4">Recommended Conservation
                            Status</h5>
                        <label for="recommended_wa_legislative_list" class="col-sm-4 col-form-label">WA Legislative
                            List:</label>
                        <div class="col-sm-8">
                            <select :disabled="true" class="form-select"
                                v-model="conservation_status_obj.recommended_wa_legislative_list_id"
                                id="recommended_wa_legislative_list">
                                <option v-for="option in wa_legislative_lists" :value="option.id"
                                    v-bind:key="option.id">
                                    {{ option.code }}
                                </option>
                            </select>
                        </div>
                    </div>
                    <div v-if="conservation_status_obj.recommended_wa_legislative_list_id" class="row mb-3">
                        <label for="recommended_wa_legislative_category" class="col-sm-4 col-form-label">WA Legislative
                            Category:</label>
                        <div class="col-sm-8">
                            <select :disabled="true" class="form-select"
                                v-model="conservation_status_obj.recommended_wa_legislative_category_id"
                                id="recommended_wa_legislative_category">
                                <option v-for="option in wa_legislative_categories" :value="option.id"
                                    v-bind:key="option.id">
                                    {{ option.code }}
                                </option>
                            </select>
                        </div>
                    </div>
                    <div class="row mb-3">
                        <label for="recommended_wa_priority_list" class="col-sm-4 col-form-label">WA Priority
                            List:</label>
                        <div class="col-sm-8">
                            <select :disabled="true" class="form-select"
                                v-model="conservation_status_obj.recommended_wa_priority_list_id"
                                id="recommended_wa_priority_list">
                                <option v-for="option in wa_priority_lists" :value="option.id" v-bind:key="option.id">
                                    {{ option.code }}
                                </option>
                            </select>
                        </div>
                    </div>
                    <div v-if="conservation_status_obj.recommended_wa_priority_list_id" class="row mb-3">
                        <label for="recommended_wa_priority_category" class="col-sm-4 col-form-label">WA Priority
                            Category:</label>
                        <div class="col-sm-8">
                            <select :disabled="true" class="form-select"
                                v-model="conservation_status_obj.recommended_wa_priority_category_id"
                                id="conservation_category">
                                <option v-for="option in wa_priority_categories" :value="option.id"
                                    v-bind:key="option.id">
                                    {{ option.code }}
                                </option>
                            </select>
                        </div>
                    </div>
                    <div class="row mb-3">
                        <label for="recommended_commonwealth_conservation_list"
                            class="col-sm-4 col-form-label">Commonwealth
                            Conservation List:</label>
                        <div class="col-sm-8">
                            <select :disabled="true" class="form-select"
                                v-model="conservation_status_obj.recommended_commonwealth_conservation_list_id"
                                id="recommended_commonwealth_conservation_list">
                                <option v-for="option in commonwealth_conservation_lists" :value="option.id"
                                    v-bind:key="option.id">
                                    {{ option.code }}
                                </option>
                            </select>
                        </div>
                    </div>
                    <div class="row mb-3">
                        <label for="recommended_international_conservation"
                            class="col-sm-4 col-form-label">International
                            Conservation:</label>
                        <div class="col-sm-8">
                            <input :disabled="true" type="text" class="form-control"
                                id="recommended_international_conservation"
                                v-model="conservation_status_obj.recommended_international_conservation" />
                        </div>
                    </div>
                    <div class="row mb-3">
                        <label for="recommended_conservation_criteria" class="col-sm-4 col-form-label">Conservation
                            Criteria:</label>
                        <div class="col-sm-8">
                            <input :disabled="true" type="text" class="form-control"
                                id="recommended_conservation_criteria"
                                v-model="conservation_status_obj.recommended_conservation_criteria" />
                        </div>
                    </div>
                </template>
                <template v-if="!is_external && isStatusApproved">
                    <div class="row border-top pt-3">
                        <label for="" class="col-sm-4 col-form-label">Approval document:</label>
                        <div class="col-sm-8">
                            <p class="col-form-label">
                                <template v-if="conservation_status_obj.conservation_status_approval_document">
                                    <strong><a :href="conservation_status_obj.conservation_status_approval_document[1]"
                                            target="_blank">{{
                                                conservation_status_obj.conservation_status_approval_document[0]
                                            }}</a></strong>
                                </template>
                                <template v-else>No approval document uploaded</template>
                            </p>
                        </div>
                    </div>
                </template>
            </form>
        </FormSection>
    </div>
</template>

<script>
import FormSection from '@/components/forms/section_toggle.vue';
import CollapsibleComponent from '@/components/forms/collapsible_component.vue'
import {
    api_endpoints,
}
    from '@/utils/hooks'

export default {
    name: 'SpeciesStatus',
    props: {
        conservation_status_obj: {
            type: Object,
            required: true
        },
        referral: {
            type: Object,
            required: false
        },
        is_external: {
            type: Boolean,
            default: false
        },
        canEditStatus: {
            type: Boolean,
            default: true
        },
    },
    emits: ['saveConservationStatus'],
    data: function () {
        let vm = this;
        return {
            scientific_name_lookup: 'scientific_name_lookup' + vm.conservation_status_obj.id,
            select_scientific_name: "select_scientific_name" + vm.conservation_status_obj.id,
            isShowComment: false,
            isFauna: vm.conservation_status_obj.group_type === "fauna" ? true : false,
            cs_profile_dict: {},
            wa_legislative_lists: [],
            wa_legislative_categories: [],
            wa_priority_lists: [],
            wa_priority_categories: [],
            commonwealth_conservation_lists: [],
            change_codes: [],
            filtered_wa_legislative_categories: [],
            filtered_wa_priority_categories: [],
            filtered_recommended_wa_legislative_categories: [],
            referral_comments_boxes: [],
            species_display: '',
            taxon_previous_name: '',
        }
    },
    components: {
        FormSection,
        CollapsibleComponent
    },
    computed: {
        show_administrative_information: function () {
            return !this.is_external &&
                this.conservation_status_obj.species_taxonomy_id &&
                this.conservation_status_obj.processing_status != "Draft";
        },
        show_proposed_conservation_status: function () {
            return this.conservation_status_obj.species_taxonomy_id;
        },
        show_listing_and_review_due_date: function () {
            return this.conservation_status_obj.listing_date ||
                this.conservation_status_obj.review_due_date ||
                this.conservation_status_obj.processing_status == "With Assessor";
        },
        listing_and_review_due_date_disabled: function () {
            return this.isReadOnly || this.conservation_status_obj.processing_status != "With Assessor"
        },
        approval_level_disabled: function () {
            return this.isReadOnly || !['With Assessor', 'With Referral'].includes(this.conservation_status_obj.processing_status);
        },
        deficiencyVisibility: function () {
            return this.conservation_status_obj.assessor_mode.assessor_box_view;
        },
        assessorCommentVisibility: function () {
            return this.conservation_status_obj.assessor_mode.assessor_box_view;
        },
        has_comment_value: function () {
            let has_value = false;
            // TODO need to add assessor comment value as well
            for (var i = 0; i < this.referral_comments_boxes.length; i++) {
                if (this.referral_comments_boxes[i].hasOwnProperty('value')) {
                    if (this.referral_comments_boxes[i].value != null && this.referral_comments_boxes[i].value != undefined && this.referral_comments_boxes[i].value != '') {
                        has_value = true;
                    }
                }
            }
            return has_value;
        },
        isStatusApproved: function () {
            return this.conservation_status_obj.processing_status == "Approved" ? true : false;
        },
        isAssignedOfficer: function () {
            if (['With Assessor', 'With Referral'].includes(this.conservation_status_obj.processing_status)) {
                return Boolean(this.conservation_status_obj.assigned_officer) &&
                    this.conservation_status_obj.assigned_officer == this.conservation_status_obj.current_assessor.id;
            }
            if (this.conservation_status_obj.processing_status != 'Draft') {
                return Boolean(this.conservation_status_obj.assigned_approver) &&
                    this.conservation_status_obj.assigned_approver == this.conservation_status_obj.current_assessor.id;
            }
            return false;
        },
        isReadOnly: function () {
            if (this.is_external) {
                return !this.conservation_status_obj.can_user_edit;
            } else if (
                this.conservation_status_obj.processing_status == "With Referral" &&
                this.referral
            ) {
                return true;
            } else {
                if (this.conservation_status_obj.processing_status == "Ready For Agenda") {
                    return true;
                }
                if (
                    (
                        this.conservation_status_obj.assessor_mode.assessor_can_assess &&
                        this.isAssignedOfficer) || this.conservation_status_obj.internal_user_edit) {
                    return false;
                }
            }

            return true;
        },
        conservation_list_proposed: function () {
            return !(this.conservation_status_obj.processing_status == "Approved" || this.conservation_status_obj.processing_status == "DeListed")
        },
        canViewCurrentList: function () {
            return (this.conservation_status_obj.processing_status == "Approved" || this.conservation_status_obj.processing_status == "DeListed") ? false : true;
        },
        isConservationStatusUnderReview: function () {
            return Boolean(this.conservation_status_obj.conservation_status_under_review);
        },
        deficiency_readonly: function () {
            return !this.is_external &&
                !this.conservation_status_obj.can_user_edit &&
                this.conservation_status_obj.assessor_mode.assessor_level == 'assessor' &&
                this.conservation_status_obj.assessor_mode.has_assessor_mode &&
                !this.conservation_status_obj.assessor_mode.status_without_assessor ? false : true;
        },
        assessor_comment_readonly: function () {
            return !this.is_external &&
                !this.conservation_status_obj.can_user_edit &&
                this.conservation_status_obj.assessor_mode.assessor_level == 'assessor' &&
                this.conservation_status_obj.assessor_mode.has_assessor_mode &&
                !this.conservation_status_obj.assessor_mode.status_without_assessor ? false : true
        },
    },
    methods: {
        approvalLevelChanged: function () {
            this.conservation_status_obj.effective_from = null;
        },
        initialiseScientificNameLookup: function () {
            let vm = this;
            $(vm.$refs[vm.scientific_name_lookup]).select2({
                minimumInputLength: 2,
                dropdownParent: $("#" + vm.select_scientific_name),
                "theme": "bootstrap-5",
                allowClear: true,
                placeholder: "Search for the Scientific Name of the Species",
                ajax: {
                    url: api_endpoints.scientific_name_lookup,
                    dataType: 'json',
                    data: function (params) {
                        var query = {
                            term: params.term,
                            type: 'public',
                            group_type_id: vm.conservation_status_obj.group_type_id,
                        }
                        return query;
                    },
                },
            }).
                on("select2:select", function (e) {
                    let data = e.params.data;
                    vm.conservation_status_obj.species_taxonomy_id = data.id
                    vm.species_display = data.text;
                    vm.taxon_previous_name = data.taxon_previous_name;
                }).
                on("select2:unselect", function (e) {
                    var selected = $(e.currentTarget);
                    vm.conservation_status_obj.species_taxonomy_id = null
                    vm.species_display = '';
                    vm.taxon_previous_name = '';
                }).
                on("select2:open", function (e) {
                    const searchField = $('[aria-controls="select2-' + vm.scientific_name_lookup + '-results"]')
                    // move focus to select2 field
                    searchField[0].focus();
                });
            if (!vm.conservation_status_obj.species_taxonomy_id) {
                vm.$nextTick(() => {
                    $(vm.$refs[vm.scientific_name_lookup]).select2('open');
                });
            }
        },
        getSpeciesDisplay: function () {
            let vm = this;
            if (vm.conservation_status_obj.species_taxonomy_id != null) {
                let species_display_url = api_endpoints.species_display + "?taxon_id=" + vm.conservation_status_obj.species_taxonomy_id
                vm.$http.get(species_display_url).then(
                    (response) => {
                        var newOption = new Option(response.body.name, response.body.id, false, true);
                        $('#' + vm.scientific_name_lookup).append(newOption);
                        vm.species_display = response.body.name
                        vm.taxon_previous_name = response.body.taxon_previous_name
                    })
            }
        },
        filterWALegislativeCategories: function (event) {
            this.$nextTick(() => {
                if (event) {
                    this.conservation_status_obj.wa_legislative_category_id = null;
                }

                this.filtered_wa_legislative_categories = this.wa_legislative_categories.filter((choice) => {
                    return choice.list_ids.includes(this.conservation_status_obj.wa_legislative_list_id);
                });
            });
        },
        filterWAPriorityCategories: function (event) {
            this.$nextTick(() => {
                if (event) {
                    this.conservation_status_obj.wa_priority_category_id = null;
                }

                this.filtered_wa_priority_categories = this.wa_priority_categories.filter((choice) => {
                    return choice.list_ids.includes(this.conservation_status_obj.wa_priority_list_id);
                });
            });
        },
        filterRecommendedWALegislativeCategories: function (event) {
            this.$nextTick(() => {
                if (event) {
                    this.conservation_status_obj.recommended_wa_legislative_category_id = null;
                }

                this.filtered_recommended_wa_legislative_categories = this.wa_priority_categories.filter((choice) => {
                    return choice.list_ids.includes(this.conservation_status_obj.recommended_wa_legislative_list_id);
                });
            });
        },
        filterRecommendedWAPriorityCategories: function (event) {
            this.$nextTick(() => {
                if (event) {
                    this.conservation_status_obj.recommended_wa_priority_category_id = null;
                }

                this.filtered_recommended_wa_priority_categories = this.wa_priority_categories.filter((choice) => {
                    return choice.list_ids.includes(this.conservation_status_obj.recommended_wa_priority_list_id);
                });
            });
        },
        generateReferralCommentBoxes: function () {
            var box_visibility = this.conservation_status_obj.assessor_mode.assessor_box_view
            var assessor_mode = this.conservation_status_obj.assessor_mode.assessor_level
            if (!this.conservation_status_obj.can_user_edit) {
                var current_referral_present = false;
                $.each(this.conservation_status_obj.referrals, (i, v) => {
                    var referral_name = `comment-field-Referral-${v.referral.email}`;
                    var referral_visibility = assessor_mode == 'referral' &&
                        this.conservation_status_obj.assessor_mode.assessor_can_assess &&
                        this.referral.referral == v.referral.id ? false : true;
                    var referral_label = `${v.referral.fullname}`;
                    var referral_comment_val = `${v.referral_comment}`;
                    this.referral_comments_boxes.push(
                        {
                            "box_view": box_visibility,
                            "name": referral_name,
                            "label": referral_label,
                            "readonly": referral_visibility,
                            "value": referral_comment_val,
                        }
                    )
                });
            }
        },
        toggleComment: function (updatedShowComment) {
            this.isShowComment = updatedShowComment;
        },
    },
    created: async function () {
        let vm = this;
        let action = this.$route.query.action;
        let dict_url = action == "view" ? api_endpoints.cs_profile_dict + '?group_type=' + vm.conservation_status_obj.group_type + '&action=' + action :
            api_endpoints.cs_profile_dict + '?group_type=' + vm.conservation_status_obj.group_type
        vm.$http.get(dict_url).then((response) => {
            vm.cs_profile_dict = response.body;
            vm.wa_legislative_lists = vm.cs_profile_dict.wa_legislative_lists;
            vm.wa_legislative_categories = vm.cs_profile_dict.wa_legislative_categories;
            vm.wa_priority_lists = vm.cs_profile_dict.wa_priority_lists;
            vm.wa_priority_categories = vm.cs_profile_dict.wa_priority_categories;
            vm.commonwealth_conservation_lists = vm.cs_profile_dict.commonwealth_conservation_lists;
            vm.change_codes = vm.cs_profile_dict.change_codes;
            this.getSpeciesDisplay();
            this.filterWALegislativeCategories();
            this.filterWAPriorityCategories();
            this.filterRecommendedWALegislativeCategories();
            this.filterRecommendedWAPriorityCategories();
            if (!vm.is_external) {
                this.generateReferralCommentBoxes();
            }
        }, (error) => {
            console.log(error);
        })
    },
    mounted: function () {
        let vm = this;
        if (!this.is_external && vm.$refs.assessment_comments) {
            vm.$refs.assessment_comments.show_warning_icon(false);
        }
        vm.$nextTick(() => {
            vm.initialiseScientificNameLookup();
        });
    },
}
</script>

<style lang="css" scoped>
fieldset.scheduler-border {
    border: 1px groove #ddd !important;
    padding: 0 1.4em 1.4em 1.4em !important;
    margin: 0 0 1.5em 0 !important;
    -webkit-box-shadow: 0px 0px 0px 0px #000;
    box-shadow: 0px 0px 0px 0px #000;
}

legend.scheduler-border {
    width: inherit;
    /* Or auto */
    padding: 0 10px;
    /* To give a bit of padding on the left and right */
    border-bottom: none;
}

input[type=text],
select {
    width: 100%;
    padding: 0.375rem 2.25rem 0.375rem 0.75rem;
}

input[type=number] {
    width: 50%;
}
</style>
