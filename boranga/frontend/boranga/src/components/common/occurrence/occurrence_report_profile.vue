<template lang="html">
    <div id="speciesOccurrenceReport">
        <FormSection :formCollapse="false" label="Occurrence Report" Index="occurrence_report">
            <template v-if="!is_external">
                <CollapsibleComponent component_title="Assessment Comments" ref="assessment_comments"
                    :collapsed="false">
                    <div class="row">
                        <div class="col rounded">
                            <div class="row">
                                <div class="col">
                                    <div class="form-floating m-3">
                                        <textarea :disabled="deficiency_readonly" class="form-control"
                                            id="assessor_deficiencies" placeholder="Deficiency Comments"
                                            v-model="occurrence_report_obj.deficiency_data" />
                                        <label for="assessor_deficiencies" class="form-label">Deficiency
                                            Comments</label>
                                    </div>
                                </div>
                            </div>
                            <div class="row">
                                <div class="col">
                                    <div class="form-floating m-3 mt-1">
                                        <textarea :disabled="assessor_comment_readonly" class="form-control" rows="3"
                                            id="assessor_comment" placeholder="Assessor Comments"
                                            v-model="occurrence_report_obj.assessor_data" />
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
                                    <template v-for="ref in referral_comments_boxes">
                                        <div class="row mb-3">
                                            <div class="col">
                                                <div class="form-floating m-3 mt-1">
                                                    <textarea v-if='!ref.readonly' :disabled="true" :id="ref.name"
                                                        :name="ref.name" class="form-control" :placeholder="ref.label"
                                                        v-model="referral.referral_comment" />
                                                    <textarea v-else :disabled="true" :name="ref.name"
                                                        :value="ref.value || ''" class="form-control"
                                                        :placeholder="ref.label" />
                                                    <label :for="ref.name" class="form-label">{{ ref.label
                                                        }}</label>
                                                </div>
                                            </div>
                                        </div>
                                    </template>
                                </div>
                            </div>
                        </div>
                    </div>
                </CollapsibleComponent>
            </template>
            <div v-show="!isCommunity">
                <div class="row mb-3">
                    <label for="" class="col-sm-3 control-label fw-bold">Scientific Name: <span class="text-danger">*</span></label>
                    <div :id="select_scientific_name" class="col-sm-9">
                        <select :id="scientific_name_lookup" :ref="scientific_name_lookup" :disabled="isReadOnly"
                            :name="scientific_name_lookup" class="form-control" />
                    </div>
                </div>
                <div class="row mb-3">
                    <label for="" class="col-sm-3 control-label"></label>
                    <div class="col-sm-9">
                        <textarea id="species_display" v-model="species_display" disabled class="form-control"
                            rows="2" />
                    </div>
                </div>
                <div class="row mb-3">
                    <label for="" class="col-sm-3 control-label">Previous Name:</label>
                    <div class="col-sm-9">
                        <input id="previous_name" v-model="taxon_previous_name" readonly type="text"
                            class="form-control" placeholder="" />
                    </div>
                </div>
            </div>
            <div v-show="isCommunity">
                <div class="row mb-3">
                    <label for="" class="col-sm-3 control-label">Community Name:</label>
                    <div :id="select_community_name" class="col-sm-9">
                        <select :id="community_name_lookup" :ref="community_name_lookup" :disabled="isReadOnly"
                            :name="community_name_lookup" class="form-control" />
                    </div>
                </div>
                <div class="row mb-3">
                    <label for="" class="col-sm-3 control-label"></label>
                    <div class="col-sm-9">
                        <textarea id="community_display" v-model="community_display" disabled class="form-control"
                            rows="2" />
                    </div>
                </div>
            </div>
            <div class="row mb-3">
                <label for="" class="col-sm-3 control-label">Site:</label>
                <div class="col-sm-9">
                    <textarea id="site" v-model="occurrence_report_obj.site
                        " :disabled="isReadOnly" class="form-control" rows="1" placeholder="" />
                </div>
            </div>
            <div class="row mb-3">
                <label for="" class="col-sm-3 control-label fw-bold">Observation Date: <span class="text-danger">*</span></label>
                <div class="col-sm-9">
                    <input v-model="occurrence_report_obj.observation_date
                        " :disabled="isReadOnly" type="datetime-local" class="form-control" name="start_date"
                        @change="formatObservationDate()" />
                </div>
            </div>
            <ObserverDatatable ref="observer_datatable" :occurrence_report_obj="occurrence_report_obj"
                :is_external="is_external" :is-read-only="isReadOnly"
                :show_observer_contact_information="show_observer_contact_information"
                @refreshOccurrenceReport="refreshOccurrenceReport()">
            </ObserverDatatable>
        </FormSection>
    </div>
</template>

<script>
import { v4 as uuid } from 'uuid';
import FormSection from '@/components/forms/section_toggle.vue';
import ObserverDatatable from './observer_datatable.vue';
import CollapsibleComponent from '@/components/forms/collapsible_component.vue'

import {
    api_endpoints,
    helpers
}
    from '@/utils/hooks'

export default {
    name: 'SpeciesOccurrenceReport',
    props: {
        occurrence_report_obj: {
            type: Object,
            required: true
        },
        referral: {
            type: Object,
            required: false
        },
        is_external: {
            type: Boolean,
            default: false,
        },
        show_observer_contact_information: {
            type: Boolean,
            default: true,
        },
    },
    emits: ['refreshOccurrenceReport'],
    data: function () {
        let vm = this;
        return {
            uuid: null,
            scientific_name_lookup:
                'scientific_name_lookup' + vm._uid,
            select_scientific_name:
                'select_scientific_name' + vm._uid,
            community_name_lookup: 'community_name_lookup' + vm._uid,
            select_community_name: 'select_community_name' + vm._uid,
            isFauna:
                vm.occurrence_report_obj.group_type === 'fauna' ? true : false,
            isCommunity:
                vm.occurrence_report_obj.group_type === 'community'
                    ? true
                    : false,
            species_display: '',
            community_display: '',
            taxon_previous_name: '',
            referral_comments_boxes: [],
        }
    },
    components: {
        FormSection,
        ObserverDatatable,
        CollapsibleComponent
    },
    watch: {
        "occurrence_report_obj.observation_date": function () {
            let vm=this;
            if(vm.isFauna){
                if(vm.occurrence_report_obj && vm.occurrence_report_obj.plant_count){
                    vm.occurrence_report_obj.animal_observation.count_date=vm.occurrence_report_obj.observation_date
                }
            }
            else{
                if(vm.occurrence_report_obj && vm.occurrence_report_obj.plant_count){
                    vm.occurrence_report_obj.animal_observation.count_date=vm.occurrence_report_obj.observation_date
                }
            }       
        }
    },
    methods: {
        initialiseScientificNameLookup: function () {
            let vm = this;
            $(vm.$refs[vm.scientific_name_lookup])
                .select2({
                    minimumInputLength: 2,
                    dropdownParent: $('#' + vm.select_scientific_name),
                    theme: 'bootstrap-5',
                    allowClear: true,
                    placeholder: 'Select Scientific Name',
                    ajax: {
                        url: api_endpoints.scientific_name_lookup,
                        dataType: 'json',
                        data: function (params) {
                            var query = {
                                term: params.term,
                                type: 'public',
                                group_type_id:
                                    vm.occurrence_report_obj.group_type_id,
                                has_species: true,
                            };
                            return query;
                        },
                    },
                })
                .on('select2:select', function (e) {
                    // eslint-disable-next-line no-unused-vars
                    var selected = $(e.currentTarget);
                    let data = e.params.data.id;
                    vm.occurrence_report_obj.species_id = e.params.data.species_id;
                    vm.species_display = e.params.data.text;
                    vm.taxon_previous_name = e.params.data.taxon_previous_name;
                })
                .on('select2:unselect', function (e) {
                    // eslint-disable-next-line no-unused-vars
                    var selected = $(e.currentTarget);
                    vm.occurrence_report_obj.species_id = null;
                    vm.species_display = '';
                    vm.taxon_previous_name = '';
                })
                // eslint-disable-next-line no-unused-vars
                .on('select2:open', function (e) {
                    const searchField = $(
                        '[aria-controls="select2-' +
                        vm.scientific_name_lookup +
                        '-results"]'
                    );
                    // move focus to select2 field
                    searchField[0].focus();
                });
        },
        getSpeciesDisplay: function () {
            let vm = this;
            if (vm.occurrence_report_obj.species_taxonomy_id != null) {
                let species_display_url = api_endpoints.species_display + "?taxon_id=" + vm.occurrence_report_obj.species_taxonomy_id
                vm.$http.get(species_display_url).then(
                    (response) => {
                        var newOption = new Option(response.body.name, response.body.id, false, true);
                        $('#' + vm.scientific_name_lookup).append(newOption);
                        vm.species_display = response.body.name
                        vm.taxon_previous_name = response.body.taxon_previous_name
                    })
            }
        },
        initialiseCommunityNameLookup: function () {
            let vm = this;
            $(vm.$refs[vm.community_name_lookup])
                .select2({
                    minimumInputLength: 2,
                    dropdownParent: $('#' + vm.select_community_name),
                    theme: 'bootstrap-5',
                    allowClear: true,
                    placeholder: 'Select Community Name',
                    ajax: {
                        url: api_endpoints.community_name_lookup,
                        dataType: 'json',
                        data: function (params) {
                            var query = {
                                term: params.term,
                                type: 'public',
                                cs_community: true,
                            };
                            return query;
                        },
                    },
                })
                .on('select2:select', function (e) {
                    // eslint-disable-next-line no-unused-vars
                    var selected = $(e.currentTarget);
                    let data = e.params.data.id;
                    vm.occurrence_report_obj.community_id = data;
                    vm.community_display = e.params.data.text;
                })
                .on('select2:unselect', function (e) {
                    // eslint-disable-next-line no-unused-vars
                    var selected = $(e.currentTarget);
                    vm.occurrence_report_obj.community_id = null;
                    vm.community_display = '';
                })
                // eslint-disable-next-line no-unused-vars
                .on('select2:open', function (e) {
                    const searchField = $(
                        '[aria-controls="select2-' +
                        vm.community_name_lookup +
                        '-results"]'
                    );
                    // move focus to select2 field
                    searchField[0].focus();
                });
        },
        getCommunityDisplay: function () {
            let vm = this;
            if (vm.occurrence_report_obj?.community_id) {
                let community_display_url = api_endpoints.community_display +
                    "?community_id=" + vm.occurrence_report_obj.community_id
                vm.$http.get(community_display_url).then(
                    (response) => {
                        var newOption = new Option(response.body.name, response.body.id, false, true);
                        $('#' + vm.community_name_lookup).append(newOption);
                        vm.community_display = response.body.name
                    })
            }
        },
        incrementComponentMapKey: function () {
            this.uuid = uuid();
        },
        eventListeners: function () {
            let vm = this;
        },
        formatObservationDate: function () {
            if (this.occurrence_report_obj.observation_date === "") {
                this.occurrence_report_obj.observation_date = null;
            }
        },
        has_comment_value: function () {
            let has_value = false;
            // TODO need to add assessor comment value as well
            for (let i = 0; i < this.referral_comments_boxes.length; i++) {
                if (Object.hasOwn(this.referral_comments_boxes[i], 'value')) {
                    if (
                        this.referral_comments_boxes[i].value != null &&
                        this.referral_comments_boxes[i].value != undefined &&
                        this.referral_comments_boxes[i].value != ''
                    ) {
                        has_value = true;
                    }
                }
            }
            return has_value;
        },
        generateReferralCommentBoxes: function () {
            console.log('generateReferralCommentBoxes')
            var box_visibility =
                this.occurrence_report_obj.assessor_mode.assessor_box_view;
            var assessor_mode =
                this.occurrence_report_obj.assessor_mode.assessor_level;
            if (!this.occurrence_report_obj.can_user_edit) {
                // eslint-disable-next-line no-unused-vars
                let current_referral_present = false;
                console.log(this.occurrence_report_obj.referrals)

                $.each(this.occurrence_report_obj.referrals, (i, v) => {
                    console.log(v)
                    var referral_name = `comment-field-Referral-${v.referral.email}`;
                    var referral_visibility =
                        assessor_mode == 'referral' &&
                            this.occurrence_report_obj.assessor_mode
                                .assessor_can_assess &&
                            this.referral.referral == v.referral.id
                            ? false
                            : true;
                    var referral_label = `${v.referral.fullname}`;
                    var referral_comment_val = `${v.referral_comment}`;
                    this.referral_comments_boxes.push({
                        box_view: box_visibility,
                        name: referral_name,
                        label: referral_label,
                        readonly: referral_visibility,
                        value: referral_comment_val,
                    });
                });
            }
        },
        refreshOccurrenceReport: function () {
            this.$emit('refreshOccurrenceReport');
        },
    },
    created: async function () {
        let vm = this;
        this.uuid = uuid();
        //------fetch list of values according to action
        let action = this.$route.query.action;
        let dict_url =
            action == 'view'
                ? api_endpoints.cs_profile_dict +
                '?group_type=' +
                vm.occurrence_report_obj.group_type +
                '&action=' +
                action
                : api_endpoints.cs_profile_dict +
                '?group_type=' +
                vm.occurrence_report_obj.group_type;
        vm.$http.get(dict_url).then(
            (response) => {
                vm.cs_profile_dict = response.body;
                if (!vm.isCommunity) {
                    this.getSpeciesDisplay();
                }
                else {
                    this.getCommunityDisplay();
                }
            },
            (error) => {
                console.log(error);
            }
        );
        if (!vm.is_external) {
            this.generateReferralCommentBoxes();
        }
    },
    computed: {
        isReadOnly: function () {
            //override for split reports
            if (this.is_readonly) {
                return this.is_readonly;
            }
            return this.occurrence_report_obj.readonly
        },
        csrf_token: function () {
            return helpers.getCookie('csrftoken');
        },
        deficiency_readonly: function () {
            return !this.is_external &&
                !this.occurrence_report_obj.can_user_edit &&
                this.occurrence_report_obj.assessor_mode.assessor_level == 'assessor' &&
                this.occurrence_report_obj.assessor_mode.has_assessor_mode &&
                !this.occurrence_report_obj.assessor_mode.status_without_assessor ? false : true;
        },
        assessor_comment_readonly: function () {
            return !this.is_external &&
                !this.occurrence_report_obj.can_user_edit &&
                this.occurrence_report_obj.assessor_mode.assessor_level == 'assessor' &&
                this.occurrence_report_obj.assessor_mode.has_assessor_mode &&
                !this.occurrence_report_obj.assessor_mode.status_without_assessor ? false : true
        },
    },
    mounted: function () {
        let vm = this;
        if (!vm.is_external && vm.$refs.assessment_comments) {
            vm.$refs.assessment_comments.show_warning_icon(false);
        }
        this.$nextTick(() => {
            vm.eventListeners();
            vm.initialiseScientificNameLookup();
            vm.initialiseCommunityNameLookup();
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
