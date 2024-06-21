<template lang="html">
    <div id="occurrenceCombine">
        <modal
            transition="modal fade"
            :title="'Combine Occurrences'"
            :large="true"
            :full="true"
            :showOK="false"
            cancel-text="Close"
            @cancel="close()"
        >

        <!--OCC Selection Drop Down-->
        <div class="row mb-3" id="occurrence_name_lookup_form_group_id">
            <label class="col-sm-3 control-label" for="occurrence_name_lookup">
                Add Occurrence:
            </label>
            <div class="col-sm-6">
                <select id="occurrence_name_lookup"
                name="occurrence_name_lookup"
                ref="occurrence_name_lookup" class="form-control"
                />
            </div>
            <div class="col-sm-3">
                <button type="button" class="btn btn-primary" @click="addOccurrence">Add</button>
            </div>
        </div>
        <!--OCC Selection Table-->
        <div class="row mb-3">
        <OccurrenceCombineSelect :selectedOccurrences="selectedOccurrences" :selectedOccurrenceIds="selectedOccurrenceIds" :mainOccurrenceId="main_occurrence_obj.id"/>
        </div>

        <!--OCC Tabs-->
        <div class="row mb-3">
            <div class="col-md-12">
                <ul id="pills-tab" class="nav nav-pills" role="tablist">
                    <li class="nav-item">
                        <a id="pills-occurrence-tab" class="nav-link active" data-bs-toggle="pill" :href="'#' + occurrenceBody"
                            role="tab" :aria-controls="occurrenceBody" aria-selected="true" @click="tabClicked()">
                            Occurrence
                        </a>
                    </li>
                    <li class="nav-item">
                        <a id="pills-location-tab" class="nav-link" data-bs-toggle="pill" :href="'#' + locationBody"
                            role="tab" aria-selected="false" @click="tabClicked()">
                            Location
                        </a>
                    </li>
                    <li class="nav-item">
                        <a id="pills-habitat-tab" class="nav-link" data-bs-toggle="pill" :href="'#' + habitatBody"
                            role="tab" aria-selected="false" @click="tabClicked()">
                            Habitat
                        </a>
                    </li>
                    <li class="nav-item">
                        <a id="pills-observation-tab" class="nav-link" data-bs-toggle="pill" :href="'#' + observationBody"
                            role="tab" aria-selected="false" @click="tabClicked()">
                            Observation
                        </a>
                    </li>
                    <li class="nav-item">
                        <a id="pills-documents-tab" class="nav-link" data-bs-toggle="pill" :href="'#' + documentBody"
                            role="tab" aria-selected="false" @click="tabClicked()">
                            Documents
                        </a>
                    </li>
                    <li class="nav-item">
                        <a id="pills-threats-tab" class="nav-link" data-bs-toggle="pill" :href="'#' + threatBody" role="tab"
                            aria-selected="false" @click="tabClicked()">
                            Threats
                        </a>
                    </li>
                </ul>
                <div id="pills-tabContent" class="tab-content">
                    <div :id="occurrenceBody" class="tab-pane fade show active" role="tabpanel"
                        aria-labelledby="pills-occurrence-tab">
                        <!--Main OCC Form-->
                        <FormSection :formCollapse="false" label="Occurrence" Index="combine_occurrence">
                            Main OCC Form
                        </FormSection>
                        <!--Key Contacts Table-->
                        <FormSection :formCollapse="true" label="Key Contacts" Index="combine_keyContacts">
                            Key Contacts Table
                        </FormSection>
                    </div>
                    <div :id="locationBody" class="tab-pane fade" role="tabpanel"
                    aria-labelledby="pills-location-tab">
                        <!--Location Form-->
                        <FormSection :formCollapse="false" label="Location" Index="combine_location">
                            Location Form
                        </FormSection>
                    </div>
                    <div :id="habitatBody" class="tab-pane fade" role="tabpanel" aria-labelledby="pills-habitat-tab">
                        <!--Habitat Composition Form-->
                        <FormSection :formCollapse="true" label="Habitat Composition" Index="combine_habitat_composition">
                            Habitat Composition Form
                        </FormSection>
                        <!--Habitat Condition Form-->
                        <FormSection :formCollapse="true" label="Habitat Condition" Index="combine_habitat_condition">
                            Habitat Condition Form
                        </FormSection>
                        <!--Vegetation Structure Form-->
                        <FormSection :formCollapse="true" label="Vegetation Structure" Index="combine_vegetation_structure">
                            Vegetation Structure Form
                        </FormSection>
                        <!--Fire History Form-->
                        <FormSection :formCollapse="true" label="Fire History" Index="combine_fire_history">
                            Fire History Form
                        </FormSection>
                        <!--Associated Species Form-->
                        <FormSection :formCollapse="true" label="Associated Species" Index="combine_associated_species">
                            Associated Species Form
                        </FormSection>
                    </div>
                    <div :id="observationBody" class="tab-pane fade" role="tabpanel"
                        aria-labelledby="pills-observation-tab">
                        <!--Observation Details Form-->
                        <FormSection :formCollapse="true" label="Observation Details" Index="combine_observation_details">
                            Observation Details Form
                        </FormSection>
                        <!--Animal Observation Form (fauna only)-->
                        <FormSection :formCollapse="true" label="Animal Observation" Index="combine_animal_observation">
                            Animal Observation Form
                        </FormSection>
                        <!--Plant Count Form (flora only)-->
                        <FormSection :formCollapse="true" label="Plant Count" Index="combine_plant_count">
                            <br/>Plant Count Form
                        </FormSection>
                        <!--Identification Form-->
                        <FormSection :formCollapse="true" label="Identification" Index="combine_identification">
                            <br/>Identification Form
                        </FormSection>
                    </div>
                    <div :id="documentBody" class="tab-pane fade" role="tabpanel" aria-labelledby="pills-documents-tab">
                        <!--Documents Table-->
                        <FormSection :formCollapse="false" label="Documents" Index="combine_documents">
                            Documents Table
                        </FormSection>
                    </div>
                    <div :id="threatBody" class="tab-pane fade" role="tabpanel" aria-labelledby="pills-threats-tab">
                        <!--Threats Table-->
                        <FormSection :formCollapse="false" label="Threats" Index="combine_threats">
                            Threats Table
                        </FormSection>
                    </div>
                </div>
            </div>
        </div>           

        </modal>
    </div>
</template>

<script>
    import modal from '@vue-utils/bootstrap-modal.vue';
    import FormSection from '@/components/forms/section_toggle.vue';
    import { helpers, api_endpoints } from "@/utils/hooks.js"
    import OccurrenceCombineSelect from './occurrence_combine_selection.vue'
    export default {
        name: 'OccurrenceCombine',
        props: {
            main_occurrence_obj: {
                type: Object,
                required: true
            },
        },
        components: {
            modal,
            OccurrenceCombineSelect,
            FormSection,
        },
        data: function () {
            let vm = this;
            return {
                reloadcount: 0,
                locationBody: 'locationBody' + vm._uid,
                habitatBody: 'habitatBody' + vm._uid,
                observationBody: 'observationBody' + vm._uid,
                threatBody: 'threatBody' + vm._uid,
                documentBody: 'documentBody' + vm._uid,
                occurrenceBody: 'occurrenceBody' + vm._uid,
                isModalOpen: false,
                selectedOccurrences: [this.main_occurrence_obj],
                selectedOccurrenceIds: [this.main_occurrence_obj.id],
                selectedAddOccurrence: null,
                occ_profile_dict: {},
                wild_status_list: [],
                occurrence_source_list: [],
                key_contact_ids: [],
                document_ids: [],
                threat_ids: [],
                occ_combine_data: {
                    combine_ids: [this.main_occurrence_obj.id],
                    combine_key_contact_ids: [],
                    combine_document_ids: [],
                    combine_threat_ids: [],
                    occurrence_name: this.main_occurrence_obj.occurrence_name,
                    occurrence_source: this.main_occurrence_obj.occurrence_source,
                    wild_status: this.main_occurrence_obj.wild_status,
                    review_due_date: this.main_occurrence_obj.review_due_date,
                    comment: this.main_occurrence_obj.comment,
                    chosen_location_section: this.main_occurrence_obj.id,
                    chosen_habitat_composition_section: this.main_occurrence_obj.id,
                    chosen_habitat_condition_section: this.main_occurrence_obj.id,
                    chosen_vegetation_structure_section: this.main_occurrence_obj.id,
                    chosen_fire_history_section: this.main_occurrence_obj.id,
                    chosen_associated_species_section: this.main_occurrence_obj.id,
                    chosen_observation_details: this.main_occurrence_obj.id,
                    chosen_animal_observation: this.main_occurrence_obj.id,
                    chosen_plant_count: this.main_occurrence_obj.id,
                    chosen_identification: this.main_occurrence_obj.id,
                },
            }
        },
        methods: {
            close: function () {
                this.errorString = '';
                this.isModalOpen = false;
                $('.has-error').removeClass('has-error');
            },
            tabClicked: function (param) {
                this.reloadcount = this.reloadcount + 1;
            },
            addOccurrence: function () {
                let vm = this;
                if (vm.selectedAddOccurrence != null &&
                !vm.selectedOccurrenceIds.includes(vm.selectedAddOccurrence.id)) {
                    vm.selectedOccurrenceIds.push(vm.selectedAddOccurrence.id);
                    vm.selectedOccurrences.push(vm.selectedAddOccurrence);
                }
                vm.selectedAddOccurrence = null;
                $(vm.$refs.occurrence_name_lookup).val(null).trigger("change");
            },
            getKeyContactIds: function() {
                let vm = this;
                let formData = new FormData()
                console.log(vm.selectedOccurrenceIds)
                formData.append("occurrence_ids", JSON.stringify(vm.selectedOccurrenceIds));
                //get all key contact ids for all OCCs
                vm.$http.post(
                    api_endpoints.combine_key_contacts_lookup, formData
                ).then((response) => {
                    //copy old list
                    let old_list = vm.key_contact_ids;
                    //add to main list
                    vm.key_contact_ids = response.body.id_list;
                    //remove ids from combine list if not in new list
                    vm.occ_combine_data.combine_key_contact_ids.forEach(id => {
                        if (!response.body.id_list.includes(id)) {
                            vm.occ_combine_data.combine_key_contact_ids.splice(indexOf(id), 1);
                        }
                    });
                    //add new ids to combine list if not in old list
                    response.body.id_list.forEach(id => {
                        if (!old_list.includes(id)) {
                            vm.occ_combine_data.combine_key_contact_ids.push(id);
                        }
                    });
                }, (error) => {
                    console.error(error);
                });                
            },
            getDocumentIds: function() {
                let vm = this;
                let formData = new FormData()
                formData.append("occurrence_ids", JSON.stringify(vm.selectedOccurrenceIds));
                //get all document ids for all OCCs
                vm.$http.post(
                    api_endpoints.combine_documents_lookup, formData
                ).then((response) => {
                    //copy old list
                    let old_list = vm.document_ids;
                    //add to main list
                    vm.document_ids = response.body.id_list;
                    //remove ids from combine list if not in new list
                    vm.occ_combine_data.combine_document_ids.forEach(id => {
                        if (!response.body.id_list.includes(id)) {
                            vm.occ_combine_data.combine_document_ids.splice(indexOf(id), 1);
                        }
                    });
                    //add new ids to combine list if not in old list
                    response.body.id_list.forEach(id => {
                        if (!old_list.includes(id)) {
                            vm.occ_combine_data.combine_document_ids.push(id);
                        }
                    });
                }, (error) => {
                    console.error(error);
                });
            },
            getThreatIds: function() {
                let vm = this;
                let formData = new FormData()
                formData.append("occurrence_ids", JSON.stringify(vm.selectedOccurrenceIds));
                //get all threat ids for all OCCs
                vm.$http.post(
                    api_endpoints.combine_threats_lookup, formData
                ).then((response) => {
                    //copy old list
                    let old_list = vm.threat_ids;
                    //add to main list
                    vm.threat_ids = response.body.id_list;
                    //remove ids from combine list if not in new list
                    vm.occ_combine_data.combine_threat_ids.forEach(id => {
                        if (!response.body.id_list.includes(id)) {
                            vm.occ_combine_data.combine_threat_ids.splice(indexOf(id), 1);
                        }
                    });
                    //add new ids to combine list if not in old list
                    response.body.id_list.forEach(id => {
                        if (!old_list.includes(id)) {
                            vm.occ_combine_data.combine_threat_ids.push(id);
                        }
                    });
                }, (error) => {
                    console.error(error);
                });
            },
            initialiseOccurrenceNameLookup: function () {
                let vm = this;
                $(vm.$refs.occurrence_name_lookup).select2({
                    width: '100%',
                    minimumInputLength: 2,
                    theme: 'bootstrap-5',
                    allowClear: true,
                    dropdownParent: $("#occurrence_name_lookup_form_group_id"),
                    placeholder: "Search Name of Occurrence",
                    ajax: {
                        url: api_endpoints.combine_occurrence_name_lookup,
                        dataType: 'json',
                        data: function (params) {
                            var query = {
                                term: params.term,
                                occurrence_id: vm.main_occurrence_obj.id,
                            }
                            return query;
                        },
                    },
                }).
                on("select2:select", function (e) {
                    vm.selectedAddOccurrence = e.params.data;
                }).
                on("select2:open", function (e) {
                    const searchField = $('[aria-controls="select2-occurrence_name_lookup-results"]')
                    searchField[0].focus();
                }).
                on("select2:unselect", function (e) {
                    console.log(e)
                    vm.selectedAddOccurrence = null;
                });
            },
        },
        created: async function () {
            let vm = this;
            let action = this.$route.query.action;

            //get key contact ids
            vm.getKeyContactIds();
            //get document ids
            vm.getDocumentIds();
            //get threat ids
            vm.getThreatIds();

            let dict_url = action == "view" ? api_endpoints.occ_profile_dict + '?group_type=' + vm.main_occurrence_obj.group_type + '&action=' + action :
                api_endpoints.occ_profile_dict + '?group_type=' + vm.main_occurrence_obj.group_type
            vm.$http.get(dict_url).then((response) => {
                vm.occ_profile_dict = response.body;
                vm.wild_status_list = vm.occ_profile_dict.wild_status_list;
                vm.occurrence_source_list = vm.occ_profile_dict.occurrence_source_list;
            }, (error) => {
                console.log(error);
            })
        },
        mounted: function () {
            this.initialiseOccurrenceNameLookup();
        },
        watch: {
            selectedOccurrenceIds: function() {
                let vm = this;
                vm.occ_combine_data.combine_ids = vm.selectedOccurrenceIds;
                //get key contact ids
                vm.getKeyContactIds();
                //get document ids
                vm.getDocumentIds();
                //get threat ids
                vm.getThreatIds();
            }
        },
    }
</script>