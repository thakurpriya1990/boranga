<template lang="html">
    <div id="speciesStatus">
        <FormSection :formCollapse="false" label="Conservation Status" Index="conservation_status"
            :isShowComment="isShowComment" :has_comment_value="has_comment_value"
            v-on:toggleComment="toggleComment($event)" :displayCommentSection="!is_external">
            <div v-if="!is_external">
                <div v-show="isShowComment">
                    <!-- Assessor Deficiencies and comment box -->
                    <div class="row mb-3" v-if="deficiencyVisibility">
                        <label for="" class="col-sm-4 col-form-label">Deficiencies:</label>
                        <div class="col-sm-8">
                            <textarea :disabled="deficiency_readonly" class="form-control" rows="3"
                                id="assessor_deficiencies" placeholder=""
                                v-model="conservation_status_obj.deficiency_data" />
                        </div>
                    </div>
                    <div class="row mb-3" v-if="assessorCommentVisibility">
                        <label for="" class="col-sm-4 col-form-label">Assessor:</label>
                        <div class="col-sm-8">
                            <textarea :disabled="assessor_comment_readonly" class="form-control" rows="3"
                                id="assessor_comment" placeholder="" v-model="conservation_status_obj.assessor_data" />
                        </div>
                    </div>
                    <!-- Assessor Deficiencies and comment box -->
                    <div v-if="referral_comments_boxes.length > 0">
                        <div v-for="ref in referral_comments_boxes">
                            <div class="row mb-3" v-if="ref.box_view">
                                <label for="" class="col-sm-4 col-form-label">{{ ref.label }}:</label>
                                <div class="col-sm-8">
                                    <textarea v-if='!ref.readonly' :disabled="ref.readonly" :name="ref.name"
                                        class="form-control" rows="3" placeholder=""
                                        v-model="referral.referral_comment" />
                                    <textarea v-else :disabled="ref.readonly" :name="ref.name" :value="ref.value"
                                        class="form-control" rows="" placeholder="" />
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
            <div class="row mb-3">
                <label for="" class="col-sm-4 col-form-label">Scientific Name:</label>
                <div class="col-sm-8" :id="select_scientific_name">
                    <select :disabled="isReadOnly" :id="scientific_name_lookup" :name="scientific_name_lookup"
                        :ref="scientific_name_lookup" class="form-control" />
                </div>
            </div>
            <div class="row mb-3">
                <label for="" class="col-sm-4 col-form-label"></label>
                <div class="col-sm-8">
                    <textarea disabled class="form-control" rows="3" id="species_display" v-model="species_display" />
                </div>
            </div>
            <div v-if="taxon_previous_name" class="row mb-3">
                <label for="" class="col-sm-4 col-form-label">Previous Name:</label>
                <div class="col-sm-8">
                    <input readonly type="text" class="form-control" id="previous_name" placeholder=""
                        v-model="taxon_previous_name" />
                </div>
            </div>
            <div class="row mb-3 border-top pt-3">
                <h5 class="text-muted mb-4">Administrative Information</h5>
                <label for="wa_legislative_list" class="col-sm-4 col-form-label">Change Type:</label>
                <div class="col-sm-8">
                    <select :disabled="isReadOnly" class="form-select" v-model="conservation_status_obj.change_code_id"
                        id="change_code" @change="filterWALegislativeCategories($event)">
                        <option :value="null">Select the appropriate Change type</option>
                        <option v-for="option in change_code_list" :value="option.id" v-bind:key="option.id">
                            {{ option.code }}
                        </option>
                    </select>
                </div>
            </div>
            <div class="row mb-3">
                <label for="applicable-workflow" class="col-sm-4 col-form-label">Applicable Workflow:</label>
                <div class="col-sm-8">
                    <select id="applicable-workflow" v-model="conservation_status_obj.approval_level"
                        class="form-select">
                        <option :value="null">Select Appropriate Workflow</option>
                        <option :value="'intermediate'">Intermediate</option>
                        <option :value="'ministerial'">Ministerial</option>
                    </select>
                </div>
            </div>
            <div class="row mb-3">
                <div class="col-sm-4"></div>
                <label for="start-date" class="col-sm-2 col-form-label">Start Date:</label>
                <div class="col-sm-2">
                    <input type="date" readonly placeholder="DD/MM/YYYY" class="form-control" id="start-date"
                        v-model="conservation_status_obj.cs_start_date" />
                </div>
                <label for="first-listed-date" class="col-sm-2 col-form-label">First Listed Date:</label>
                <div class="col-sm-2">
                    <input type="date" readonly placeholder="DD/MM/YYYY" class="form-control" id="first-listed-date"
                        v-model="conservation_status_obj.listing_date" />
                </div>
            </div>
            <div class="row mb-3">
                <div class="col-sm-4"></div>
                <label for="review-date" class="col-sm-2 col-form-label">Review Date:</label>
                <div class="col-sm-2">
                    <input type="date" readonly placeholder="DD/MM/YYYY" class="form-control" id="review-date"
                        v-model="conservation_status_obj.review_date" />
                </div>
                <label for="end-date" class="col-sm-2 col-form-label">End Date:</label>
                <div class="col-sm-2">
                    <input type="date" readonly placeholder="DD/MM/YYYY" class="form-control" id="end-date"
                        v-model="conservation_status_obj.cs_end_date" />
                </div>
            </div>
            <div class="row mb-3 border-top pt-3">
                <h5 class="text-muted mb-4"><template v-if="conservation_list_proposed">Proposed
                    </template>Conservation
                    Status</h5>
                <label for="proposed_wa_legislative_list" class="col-sm-4 col-form-label">WA Legislative List:</label>
                <div class="col-sm-8">
                    <select :disabled="isReadOnly" class="form-select"
                        v-model="conservation_status_obj.wa_legislative_list_id" id="proposed_wa_legislative_list"
                        @change="filterWALegislativeCategories($event)">
                        <option :value="null" disabled>Select the appropriate WA Legislative List</option>
                        <option v-for="option in wa_legislative_lists" :value="option.id" v-bind:key="option.id">
                            {{ option.code }}
                        </option>
                    </select>
                </div>
            </div>
            <div v-if="conservation_status_obj.wa_legislative_list_id" class="row mb-3">
                <label for="proposed_wa_legislative_category" class="col-sm-4 col-form-label">WA Legislative Category:</label>
                <div class="col-sm-8">
                    <select :disabled="isReadOnly" class="form-select"
                        v-model="conservation_status_obj.wa_legislative_category_id" id="proposed_wa_legislative_category">
                        <option :value="null" disabled>Select the appropriate WA Legislative Category</option>
                        <option v-for="option in filtered_wa_legislative_categories" :value="option.id"
                            v-bind:key="option.id">
                            {{ option.code }}
                        </option>
                    </select>
                </div>
            </div>
            <div class="row mb-3">
                <label for="proposed_wa_priority_list" class="col-sm-4 col-form-label">WA Priority List:</label>
                <div class="col-sm-8">
                    <select :disabled="isReadOnly" class="form-select"
                        v-model="conservation_status_obj.wa_priority_list_id" id="proposed_wa_priority_list"
                        @change="filterWAPriorityCategories($event)">
                        <option :value="null" disabled>Select the appropriate WA Priority List</option>
                        <option v-for="option in wa_priority_lists" :value="option.id" v-bind:key="option.id">
                            {{ option.code }}
                        </option>
                    </select>
                </div>
            </div>
            <div v-if="conservation_status_obj.wa_priority_list_id" class="row mb-3">
                <label for="proposed_wa_priority_category" class="col-sm-4 col-form-label">WA Priority Category:</label>
                <div class="col-sm-8">
                    <select :disabled="isReadOnly" class="form-select"
                        v-model="conservation_status_obj.wa_priority_category_id" id="proposed_wa_priority_category">
                        <option :value="null" disabled>Select the appropriate WA Priority Category</option>
                        <option v-for="option in filtered_wa_priority_categories" :value="option.id"
                            v-bind:key="option.id">
                            {{ option.code }}
                        </option>
                    </select>
                </div>
            </div>
            <div class="row mb-3">
                <label for="proposed_commonwealth_conservation_list" class="col-sm-4 col-form-label">Commonwealth Conservation List:</label>
                <div class="col-sm-8">
                    <select :disabled="isReadOnly" class="form-select"
                        v-model="conservation_status_obj.commonwealth_conservation_list_id" id="proposed_commonwealth_conservation_list"
                        @change="filterWAPriorityCategories($event)">
                        <option :value="null" disabled>Select a Commonwealth Conservation List if Applicable
                        </option>
                        <option v-for="option in commonwealth_conservation_lists" :value="option.id"
                            v-bind:key="option.id">
                            {{ option.code }}
                        </option>
                    </select>
                </div>
            </div>
            <div class="row mb-3">
                <label for="proposed_international_conservation" class="col-sm-4 col-form-label">International
                    Conservation:</label>
                <div class="col-sm-8">
                    <input :disabled="isReadOnly" type="text" class="form-control" id="proposed_international_conservation"
                        placeholder="Enter International Conservation Details if Applicable"
                        v-model="conservation_status_obj.international_conservation" />
                </div>
            </div>
            <div class="row mb-3">
                <label for="proposed_conservation_criteria" class="col-sm-4 col-form-label">Conservation Criteria:</label>
                <div class="col-sm-8">
                    <input :disabled="isReadOnly" type="text" class="form-control" id="proposed_conservation_criteria"
                        placeholder="Enter Conservation Criteria if Applicable"
                        v-model="conservation_status_obj.conservation_criteria" />
                </div>
            </div>
            <template v-if="canViewCurrentList && conservation_status_obj.current_conservation_status">
                <div class="row mb-3 border-top pt-3">
                    <h5 class="text-muted mb-4">Current Conservation
                        Status</h5>
                    <label for="current_wa_legislative_list" class="col-sm-4 col-form-label">WA Legislative List:</label>
                    <div class="col-sm-8">
                        <select :disabled="true" class="form-select"
                            v-model="conservation_status_obj.current_conservation_status.wa_legislative_list_id"
                            id="current_wa_legislative_list" @change="filterWALegislativeCategories($event)">
                            <option v-for="option in wa_legislative_lists" :value="option.id" v-bind:key="option.id">
                                {{ option.code }}
                            </option>
                        </select>
                    </div>
                </div>
                <div v-if="conservation_status_obj.current_conservation_status.wa_legislative_list_id" class="row mb-3">
                    <label for="current_wa_legislative_category" class="col-sm-4 col-form-label">WA Legislative Category:</label>
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
                <div class="row mb-3">
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
                <div v-if="conservation_status_obj.current_conservation_status.wa_priority_list_id" class="row mb-3">
                    <label for="current_wa_priority_category" class="col-sm-4 col-form-label">WA Priority Category:</label>
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
                <div class="row mb-3">
                    <label for="current_commonwealth_conservation_list" class="col-sm-4 col-form-label">Commonwealth Conservation List:</label>
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
                <div class="row mb-3">
                    <label for="current_international_conservation" class="col-sm-4 col-form-label">International
                        Conservation:</label>
                    <div class="col-sm-8">
                        <input :disabled="true" type="text" class="form-control" id="current_international_conservation"
                            v-model="conservation_status_obj.current_conservation_status.international_conservation" />
                    </div>
                </div>
                <div class="row mb-3">
                    <label for="current_conservation_criteria" class="col-sm-4 col-form-label">Conservation Criteria:</label>
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
                    <label for="recommended_wa_legislative_list" class="col-sm-4 col-form-label">WA Legislative List:</label>
                    <div class="col-sm-8">
                        <select :disabled="true" class="form-select"
                            v-model="conservation_status_obj.recommended_wa_legislative_list_id"
                            id="recommended_wa_legislative_list">
                            <option v-for="option in wa_legislative_lists" :value="option.id" v-bind:key="option.id">
                                {{ option.code }}
                            </option>
                        </select>
                    </div>
                </div>
                <div v-if="conservation_status_obj.recommended_wa_legislative_list_id" class="row mb-3">
                    <label for="recommended_wa_legislative_category" class="col-sm-4 col-form-label">WA Legislative Category:</label>
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
                    <label for="recommended_wa_priority_list" class="col-sm-4 col-form-label">WA Priority List:</label>
                    <div class="col-sm-8">
                        <select :disabled="true" class="form-select"
                            v-model="conservation_status_obj.recommended_wa_priority_list_id" id="recommended_wa_priority_list">
                            <option v-for="option in wa_priority_lists" :value="option.id" v-bind:key="option.id">
                                {{ option.code }}
                            </option>
                        </select>
                    </div>
                </div>
                <div v-if="conservation_status_obj.recommended_wa_priority_list_id" class="row mb-3">
                    <label for="recommended_wa_priority_category" class="col-sm-4 col-form-label">WA Priority Category:</label>
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
                    <label for="recommended_commonwealth_conservation_list" class="col-sm-4 col-form-label">Commonwealth Conservation List:</label>
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
                    <label for="recommended_international_conservation" class="col-sm-4 col-form-label">International
                        Conservation:</label>
                    <div class="col-sm-8">
                        <input :disabled="true" type="text" class="form-control" id="recommended_international_conservation"
                            v-model="conservation_status_obj.recommended_international_conservation" />
                    </div>
                </div>
                <div class="row mb-3">
                    <label for="recommended_conservation_criteria" class="col-sm-4 col-form-label">Conservation Criteria:</label>
                    <div class="col-sm-8">
                        <input :disabled="true" type="text" class="form-control" id="recommended_conservation_criteria"
                            v-model="conservation_status_obj.recommended_conservation_criteria" />
                    </div>
                </div>
            </template>
            <div class="row mb-3">
                <label for="comment" class="col-sm-4 col-form-label">Comment:</label>
                <div class="col-sm-8">
                    <textarea :disabled="isReadOnly" class="form-control" rows="3" id="comment" placeholder=""
                        v-model="conservation_status_obj.comment" />
                </div>
            </div>
            <!-- TODO Do we need to show the effective dates and approval document to external user -->
            <div class="row mb-3" v-if="isStatusApproved && is_external == false">
                <label for="" class="col-sm-4 col-form-label">Effective From Date:</label>
                <div class="col-sm-8">
                    <input :disabled="conservation_status_obj.readonly" type="date" class="form-control"
                        placeholder="DD/MM/YYYY" id="effective_from_date"
                        v-model="conservation_status_obj.conservationstatusissuanceapprovaldetails.effective_from_date">
                </div>
            </div>
            <div class="row mb-3" v-if="isStatusApproved && is_external == false">
                <label for="" class="col-sm-4 col-form-label">Effective To Date:</label>
                <div class="col-sm-8">
                    <input :disabled="conservation_status_obj.readonly" type="date" class="form-control"
                        placeholder="DD/MM/YYYY" id="effective_to_date"
                        v-model="conservation_status_obj.conservationstatusissuanceapprovaldetails.effective_to_date">
                </div>
            </div>
            <div class="row mb-3" v-if="isStatusApproved && is_external == false">
                <label for="" class="col-sm-4 col-form-label">Approval document:</label>
                <div class="col-sm-8">
                    <p v-if="conservation_status_obj.conservation_status_approval_document">
                        <strong><a :href="conservation_status_obj.conservation_status_approval_document[1]"
                                target="_blank">{{
                                    conservation_status_obj.conservation_status_approval_document[0] }}</a></strong>
                    </p>
                </div>
            </div>
        </FormSection>
    </div>
</template>

<script>
import FormSection from '@/components/forms/section_toggle.vue';
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
    data: function () {
        let vm = this;
        return {
            scientific_name_lookup: 'scientific_name_lookup' + vm.conservation_status_obj.id,
            select_scientific_name: "select_scientific_name" + vm.conservation_status_obj.id,
            isShowComment: false,
            //---to show fields related to Fauna
            isFauna: vm.conservation_status_obj.group_type === "fauna" ? true : false,
            //----list of values dictionary
            cs_profile_dict: {},
            species_list: [],
            wa_legislative_lists: [],
            wa_legislative_categories: [],
            wa_priority_lists: [],
            wa_priority_categories: [],
            commonwealth_conservation_lists: [],
            iucn_version_list: [],
            change_code_list: [],
            filtered_wa_legislative_categories: [],
            filtered_wa_priority_categories: [],
            filtered_recommended_wa_legislative_categories: [],
            referral_comments_boxes: [],
            // to display the species selected
            species_display: '',
            taxon_previous_name: '',
            //---Comment box attributes

            deficiency_readonly: !this.is_external && !this.conservation_status_obj.can_user_edit && this.conservation_status_obj.assessor_mode.assessor_level == 'assessor' && this.conservation_status_obj.assessor_mode.has_assessor_mode && !this.conservation_status_obj.assessor_mode.status_without_assessor ? false : true,
            assessor_comment_readonly: !this.is_external && !this.conservation_status_obj.can_user_edit && this.conservation_status_obj.assessor_mode.assessor_level == 'assessor' && this.conservation_status_obj.assessor_mode.has_assessor_mode && !this.conservation_status_obj.assessor_mode.status_without_assessor ? false : true,

        }
    },
    components: {
        FormSection,
    },
    computed: {
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
        isReadOnly: function () {
            return !this.conservation_status_obj.can_user_edit;
        },
        conservation_list_proposed: function () {
            return !(this.conservation_status_obj.processing_status == "Approved" || this.conservation_status_obj.processing_status == "DeListed")
        },
        conservation_criteria_label: function () {
            if (this.conservation_status_obj.processing_status == "Approved" || this.conservation_status_obj.processing_status == "DeListed") {
                return "Conservation Criteria";
            }
            else {
                if (this.conservation_status_obj.processing_status == "Draft") {
                    return "Propose Conservation Criteria";
                }
                else {
                    return "Proposed Conservation Criteria";
                }
            }
        },
        canViewCurrentList: function () {
            return (this.conservation_status_obj.processing_status == "Approved" || this.conservation_status_obj.processing_status == "DeListed") ? false : true;
        }
    },
    methods: {
        initialiseScientificNameLookup: function () {
            let vm = this;
            $(vm.$refs[vm.scientific_name_lookup]).select2({
                minimumInputLength: 2,
                dropdownParent: $("#" + vm.select_scientific_name),
                "theme": "bootstrap-5",
                allowClear: true,
                placeholder: "Select Scientific Name",
                ajax: {
                    url: api_endpoints.scientific_name_lookup,
                    dataType: 'json',
                    data: function (params) {
                        var query = {
                            term: params.term,
                            type: 'public',
                            group_type_id: vm.conservation_status_obj.group_type_id,
                            cs_species: true,
                            cs_species_status: vm.conservation_status_obj.processing_status,
                        }
                        return query;
                    },
                },
            }).
                on("select2:select", function (e) {
                    var selected = $(e.currentTarget);
                    let data = e.params.data.id;
                    vm.conservation_status_obj.species_id = e.params.data.id
                    vm.species_display = e.params.data.text;
                    vm.taxon_previous_name = e.params.data.taxon_previous_name;
                }).
                on("select2:unselect", function (e) {
                    var selected = $(e.currentTarget);
                    vm.conservation_status_obj.species_id = null
                    vm.species_display = '';
                    vm.taxon_previous_name = '';
                }).
                on("select2:open", function (e) {
                    const searchField = $('[aria-controls="select2-' + vm.scientific_name_lookup + '-results"]')
                    // move focus to select2 field
                    searchField[0].focus();
                });
        },
        getSpeciesDisplay: function () {
            let vm = this;
            for (let choice of vm.species_list) {
                if (choice.id === vm.conservation_status_obj.species_id) {
                    var newOption = new Option(choice.name, choice.id, false, true);
                    $('#' + vm.scientific_name_lookup).append(newOption);
                    vm.species_display = choice.name;
                    vm.taxon_previous_name = choice.taxon_previous_name;
                }
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
                this.filtered_wa_priority_categories = this.wa_priority_categories.filter((choice) => {
                    return choice.list_ids.includes(this.conservation_status_obj.wa_priority_list_id);
                });
                this.filtered_recommended_wa_legislative_categories = [];
                this.filtered_recommended_wa_legislative_categories = [{
                    id: null,
                    code: "",
                    conservation_list_id: null,
                }];
                for (let choice of this.wa_legislative_categories) {
                    if (choice.conservation_list_id === this.conservation_status_obj.recommended_conservation_list_id) {
                        this.filtered_recommended_wa_legislative_categories.push(choice);
                    }
                }
            });
        },
        generateReferralCommentBoxes: function () {
            var box_visibility = this.conservation_status_obj.assessor_mode.assessor_box_view
            var assessor_mode = this.conservation_status_obj.assessor_mode.assessor_level
            if (!this.conservation_status_obj.can_user_edit) {
                var current_referral_present = false;
                $.each(this.conservation_status_obj.latest_referrals, (i, v) => {
                    var referral_name = `comment-field-Referral-${v.referral_obj.email}`;
                    var referral_visibility = assessor_mode == 'referral' && this.conservation_status_obj.assessor_mode.assessor_can_assess && this.referral.referral == v.referral_obj.id ? false : true;
                    var referral_label = `${v.referral_obj.fullname}`;
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
        //------fetch list of values according to action
        let action = this.$route.query.action;
        let dict_url = action == "view" ? api_endpoints.cs_profile_dict + '?group_type=' + vm.conservation_status_obj.group_type + '&action=' + action :
            api_endpoints.cs_profile_dict + '?group_type=' + vm.conservation_status_obj.group_type
        vm.$http.get(dict_url).then((response) => {
            vm.cs_profile_dict = response.body;
            vm.species_list = vm.cs_profile_dict.species_list;

            vm.wa_legislative_lists = vm.cs_profile_dict.wa_legislative_lists;
            vm.wa_legislative_categories = vm.cs_profile_dict.wa_legislative_categories;
            vm.wa_priority_lists = vm.cs_profile_dict.wa_priority_lists;
            vm.wa_priority_categories = vm.cs_profile_dict.wa_priority_categories;
            vm.commonwealth_conservation_lists = vm.cs_profile_dict.commonwealth_conservation_lists;

            vm.iucn_version_list = vm.cs_profile_dict.iucn_version_list;
            vm.change_code_list = vm.cs_profile_dict.change_code_list;
            this.getSpeciesDisplay();
            this.filterWALegislativeCategories();
            this.filterRecommendedWALegislativeCategories();
            if (!vm.is_external) {
                this.generateReferralCommentBoxes();
            }
        }, (error) => {
            console.log(error);
        })
    },
    mounted: function () {
        let vm = this;
        this.$nextTick(() => {
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
