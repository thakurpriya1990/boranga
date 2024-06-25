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
                            <div class="row mb-3">
                                <label for="" class="col-sm-3 control-label">Occurrence Name:</label>
                                <div class="col-sm-9">
                                    <select id="combine_occurrence_name" ref="combine_occurrence_name" class="form-select"
                                        v-model="occ_combine_data.occurrence_name" :key="occ_form_key">
                                        <option v-for="occurrence in selectedOccurrences" :value="occurrence.id"
                                            v-bind:key="occurrence.id">
                                            {{occurrence.occurrence_number}}: {{occurrence.occurrence_name}}
                                        </option>
                                    </select>
                                </div>
                            </div>
                            <div v-if="main_occurrence_obj.group_type=='flora' || main_occurrence_obj.group_type=='fauna'" class="row mb-3">
                                <label for="" class="col-sm-3 control-label">Scientific Name:</label>
                                <div class="col-sm-9">
                                    <textarea disabled class="form-control" rows="1" v-model="main_occurrence_obj.scientific_name"/>
                                </div>
                            </div>
                            <div v-else class="row mb-3">
                                <label for="" class="col-sm-3 control-label">Community Name:</label>
                                <div class="col-sm-9">
                                    <textarea disabled class="form-control" rows="1" v-model="main_occurrence_obj.community_name"/>
                                </div>
                            </div>
                            <div class="row mb-3">
                                <label for="" class="col-sm-3 control-label">Occurrence Source:</label>
                                <div class="col-sm-9">
                                    <select id="combine_occurrence_source" ref="combine_occurrence_source" class="form-select"
                                        v-model="occ_combine_data.occurrence_source" :key="occ_form_key">
                                        <option v-for="occurrence in selectedOccurrences" :value="occurrence.id"
                                            v-bind:key="occurrence.id">
                                            {{occurrence.occurrence_number}}: 
                                            <span v-for="source in occurrence.occurrence_source">
                                                <span v-for="occ_source in occurrence_source_list">                                                    
                                                    <span v-if="occ_source[0] == source">{{occ_source[1]}}</span>             
                                                </span>
                                                <span v-if="source != occurrence.occurrence_source[occurrence.occurrence_source.length-1]">, </span>
                                            </span>
                                        </option>
                                    </select>
                                </div>
                            </div>
                            <div class="row mb-3">
                                <label for="" class="col-sm-3 control-label">Wild Status:</label>
                                <div class="col-sm-9">
                                    <select id="combine_wild_status" ref="combine_wild_status" class="form-select"
                                        v-model="occ_combine_data.wild_status" :key="occ_form_key">
                                        <option v-for="occurrence in selectedOccurrences" :value="occurrence.id"
                                            v-bind:key="occurrence.id">
                                            {{occurrence.occurrence_number}}:
                                            <span v-for="wild_status in wild_status_list">
                                            <span v-if="wild_status.id == occurrence.wild_status">{{wild_status.name}}</span>
                                            </span>
                                        </option>
                                    </select>
                                </div>
                            </div>
                            <div class="row mb-3">
                                <label for="" class="col-sm-3 control-label">Review Due Date:</label>
                                <div class="col-sm-9">
                                    <select id="combine_review_due_date" ref="combine_review_due_date" class="form-select"
                                        v-model="occ_combine_data.review_due_date" :key="occ_form_key">
                                        <option v-for="occurrence in selectedOccurrences" :value="occurrence.id"
                                            v-bind:key="occurrence.id">
                                            {{occurrence.occurrence_number}}: {{occurrence.review_due_date}}
                                        </option>
                                    </select>
                                </div>
                            </div>
                            <div class="row mb-3">
                                <label for="" class="col-sm-3 control-label">Comment:</label>
                                <div class="col-sm-9">
                                    <select id="combine_comment" ref="combine_comment" class="form-select"
                                        v-model="occ_combine_data.comment" :key="occ_form_key">
                                        <option v-for="occurrence in selectedOccurrences" :value="occurrence.id"
                                            v-bind:key="occurrence.id">
                                            {{occurrence.occurrence_number}}: {{occurrence.comment}}
                                        </option>
                                    </select>
                                </div>
                            </div>
                        </FormSection>
                        <!--Key Contacts Table-->
                        <FormSection :formCollapse="true" label="Key Contacts" Index="combine_keyContacts" @toggle-collapse="toggleKeyContacts">
                            <div class="row mb-3">
                            <OccurrenceCombineContacts 
                            :selectedKeyContacts="key_contacts" 
                            :combineKeyContactIds="occ_combine_data.combine_key_contact_ids" 
                            :key="contact_table_key" 
                            ref="key_contacts_section"/>
                            </div>
                        </FormSection>
                    </div>
                    <div :id="locationBody" class="tab-pane fade" role="tabpanel"
                    aria-labelledby="pills-location-tab">
                        <!--Location Form-->
                        <FormSection :formCollapse="false" label="Location" :subtitle="' - OCC'+occ_combine_data.chosen_location_section" Index="combine_location">
                            <div class="row mb-3">
                            <OccurrenceCombineSelect :occ_chosen_section="occ_combine_data.chosen_location_section" :section_type="'location'" :selectedOccurrences="selectedOccurrences" :selectedOccurrenceIds="selectedOccurrenceIds" :mainOccurrenceId="main_occurrence_obj.id" @updateChosenSection="updateChosenSection"/>
                            </div>
                        </FormSection>
                    </div>
                    <div :id="habitatBody" class="tab-pane fade" role="tabpanel" aria-labelledby="pills-habitat-tab">
                        <!--Habitat Composition Form-->
                        <FormSection :formCollapse="true" label="Habitat Composition" :subtitle="' - OCC'+occ_combine_data.chosen_habitat_composition_section" Index="combine_habitat_composition">
                            <div class="row mb-3">
                            <OccurrenceCombineSelect :occ_chosen_section="occ_combine_data.chosen_habitat_composition_section" :section_type="'habitat_composition'" :selectedOccurrences="selectedOccurrences" :selectedOccurrenceIds="selectedOccurrenceIds" :mainOccurrenceId="main_occurrence_obj.id" @updateChosenSection="updateChosenSection"/>
                            </div>
                        </FormSection>
                        <!--Habitat Condition Form-->
                        <FormSection :formCollapse="true" label="Habitat Condition" :subtitle="' - OCC'+occ_combine_data.chosen_habitat_condition_section" Index="combine_habitat_condition">
                            <div class="row mb-3">
                            <OccurrenceCombineSelect :occ_chosen_section="occ_combine_data.chosen_habitat_condition_section" :section_type="'habitat_condition'" :selectedOccurrences="selectedOccurrences" :selectedOccurrenceIds="selectedOccurrenceIds" :mainOccurrenceId="main_occurrence_obj.id" @updateChosenSection="updateChosenSection"/>
                            </div>
                        </FormSection>
                        <!--Vegetation Structure Form-->
                        <FormSection :formCollapse="true" label="Vegetation Structure" :subtitle="' - OCC'+occ_combine_data.chosen_vegetation_structure_section" Index="combine_vegetation_structure">
                            <div class="row mb-3">
                            <OccurrenceCombineSelect :occ_chosen_section="occ_combine_data.chosen_vegetation_structure_section" :section_type="'vegetation_structure'" :selectedOccurrences="selectedOccurrences" :selectedOccurrenceIds="selectedOccurrenceIds" :mainOccurrenceId="main_occurrence_obj.id" @updateChosenSection="updateChosenSection"/>
                            </div>
                        </FormSection>
                        <!--Fire History Form-->
                        <FormSection :formCollapse="true" label="Fire History" :subtitle="' - OCC'+occ_combine_data.chosen_fire_history_section" Index="combine_fire_history">
                            <div class="row mb-3">
                            <OccurrenceCombineSelect :occ_chosen_section="occ_combine_data.chosen_fire_history_section" :section_type="'fire_history'" :selectedOccurrences="selectedOccurrences" :selectedOccurrenceIds="selectedOccurrenceIds" :mainOccurrenceId="main_occurrence_obj.id" @updateChosenSection="updateChosenSection"/>
                            </div>
                        </FormSection>
                        <!--Associated Species Form-->
                        <FormSection :formCollapse="true" label="Associated Species" :subtitle="' - OCC'+occ_combine_data.chosen_associated_species_section" Index="combine_associated_species">
                            <div class="row mb-3">
                            <OccurrenceCombineSelect :occ_chosen_section="occ_combine_data.chosen_associated_species_section" :section_type="'associated_species'" :selectedOccurrences="selectedOccurrences" :selectedOccurrenceIds="selectedOccurrenceIds" :mainOccurrenceId="main_occurrence_obj.id" @updateChosenSection="updateChosenSection"/>
                            </div>
                        </FormSection>
                    </div>
                    <div :id="observationBody" class="tab-pane fade" role="tabpanel"
                        aria-labelledby="pills-observation-tab">
                        <!--Observation Details Form-->
                        <FormSection :formCollapse="true" label="Observation Details" :subtitle="' - OCC'+occ_combine_data.chosen_observation_detail_section" Index="combine_observation_details">
                            <div class="row mb-3">
                            <OccurrenceCombineSelect :occ_chosen_section="occ_combine_data.chosen_observation_detail_section" :section_type="'observation_detail'" :selectedOccurrences="selectedOccurrences" :selectedOccurrenceIds="selectedOccurrenceIds" :mainOccurrenceId="main_occurrence_obj.id" @updateChosenSection="updateChosenSection"/>
                            </div>
                        </FormSection>
                        <!--Animal Observation Form (fauna only)-->
                        <FormSection v-if="main_occurrence_obj.group_type=='fauna'" :formCollapse="true" label="Animal Observation" :subtitle="' - OCC'+occ_combine_data.chosen_animal_observation_section" Index="combine_animal_observation">
                            <div class="row mb-3">
                            <OccurrenceCombineSelect :occ_chosen_section="occ_combine_data.chosen_animal_observation_section" :section_type="'animal_observation'" :selectedOccurrences="selectedOccurrences" :selectedOccurrenceIds="selectedOccurrenceIds" :mainOccurrenceId="main_occurrence_obj.id" @updateChosenSection="updateChosenSection"/>
                            </div>
                        </FormSection>
                        <!--Plant Count Form (flora only)-->
                        <FormSection v-if="main_occurrence_obj.group_type=='flora'" :formCollapse="true" label="Plant Count" :subtitle="' - OCC'+occ_combine_data.chosen_plant_count_section" Index="combine_plant_count">
                            <div class="row mb-3">
                            <OccurrenceCombineSelect :occ_chosen_section="occ_combine_data.chosen_plant_count_section" :section_type="'plant_count'" :selectedOccurrences="selectedOccurrences" :selectedOccurrenceIds="selectedOccurrenceIds" :mainOccurrenceId="main_occurrence_obj.id" @updateChosenSection="updateChosenSection"/>
                            </div>
                        </FormSection>
                        <!--Identification Form-->
                        <FormSection :formCollapse="true" label="Identification" :subtitle="' - OCC'+occ_combine_data.chosen_identification_section" Index="combine_identification">
                            <div class="row mb-3">
                            <OccurrenceCombineSelect :occ_chosen_section="occ_combine_data.chosen_identification_section" :section_type="'identification'" :selectedOccurrences="selectedOccurrences" :selectedOccurrenceIds="selectedOccurrenceIds" :mainOccurrenceId="main_occurrence_obj.id" @updateChosenSection="updateChosenSection"/>
                            </div>
                        </FormSection>
                    </div>
                    <div :id="documentBody" class="tab-pane fade" role="tabpanel" aria-labelledby="pills-documents-tab">
                        <!--Documents Table-->
                        <FormSection :formCollapse="false" label="Documents" Index="combine_documents" @toggle-collapse="toggleDocuments">
                            <div class="row mb-3">
                            <OccurrenceCombineDocuments
                            :selectedDocuments="documents" 
                            :combineDocumentIds="occ_combine_data.combine_document_ids" 
                            :key="document_table_key" 
                            ref="documents_section"/>
                            </div>
                        </FormSection>
                    </div>
                    <div :id="threatBody" class="tab-pane fade" role="tabpanel" aria-labelledby="pills-threats-tab">
                        <!--Threats Table-->
                        <FormSection :formCollapse="false" label="Threats" Index="combine_threats">
                            <div class="row mb-3">
                            <OccurrenceCombineThreats
                            :selectedThreats="threats" 
                            :combineThreatIds="occ_combine_data.combine_threat_ids" 
                            :key="threat_table_key" 
                            ref="threats_section"/>
                            </div>
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
    import OccurrenceCombineContacts from './occurrence_combine_contacts.vue'
    import OccurrenceCombineDocuments from './occurrence_combine_documents.vue'
    import OccurrenceCombineThreats from './occurrence_combine_threats.vue'
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
            OccurrenceCombineContacts,
            OccurrenceCombineDocuments,
            OccurrenceCombineThreats,
        },
        data: function () {
            let vm = this;
            return {
                occ_form_key: 0,
                contact_table_key: 0,
                document_table_key: 0,
                threat_table_key: 0,
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
                key_contacts: [],
                documents: [],
                threats: [],
                occ_combine_data: {
                    combine_ids: [this.main_occurrence_obj.id],
                    combine_key_contact_ids: [],
                    combine_document_ids: [],
                    combine_threat_ids: [],
                    occurrence_name: this.main_occurrence_obj.id,
                    occurrence_source: this.main_occurrence_obj.id,
                    wild_status: this.main_occurrence_obj.id,
                    review_due_date: this.main_occurrence_obj.id,
                    comment: this.main_occurrence_obj.id,
                    chosen_location_section: this.main_occurrence_obj.id,
                    chosen_habitat_composition_section: this.main_occurrence_obj.id,
                    chosen_habitat_condition_section: this.main_occurrence_obj.id,
                    chosen_vegetation_structure_section: this.main_occurrence_obj.id,
                    chosen_fire_history_section: this.main_occurrence_obj.id,
                    chosen_associated_species_section: this.main_occurrence_obj.id,
                    chosen_observation_detail_section: this.main_occurrence_obj.id,
                    chosen_animal_observation_section: this.main_occurrence_obj.id,
                    chosen_plant_count_section: this.main_occurrence_obj.id,
                    chosen_identification_section: this.main_occurrence_obj.id,
                },
            }
        },
        methods: {
            toggleKeyContacts: function () {
                let vm = this;
                vm.$refs.key_contacts_section.adjust_table_width();
            },
            toggleDocuments: function () {
                let vm = this;
                vm.$refs.documents_section.adjust_table_width();
            },
            toggleThreats: function () {
                let vm = this;
                vm.$refs.threats_section.adjust_table_width();
            },
            updateChosenSection: function (id, sectionType) {
                let vm = this;
                vm.occ_combine_data["chosen_"+sectionType+"_section"] = parseInt(id);
                console.log(vm.occ_combine_data["chosen_"+sectionType+"_section"]);
            },
            close: function () {
                this.errorString = '';
                this.isModalOpen = false;
                $('.has-error').removeClass('has-error');
            },
            tabClicked: function (param) {
                let vm = this;
                this.reloadcount++;
                this.occ_form_key++;
                this.contact_table_key++;
                this.document_table_key++;
                this.threat_table_key++;

                setTimeout(function () {
                    vm.toggleDocuments();
                    vm.toggleThreats();
                }, 200); //set to 200 due to the tab fade (TODO: consider better handling of this)
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
                vm.occ_form_key++;
            },
            checkFormValues: function () {
                let vm = this;

                if (!vm.selectedOccurrenceIds.includes(vm.occ_combine_data.chosen_location_section)) {
                    vm.occ_combine_data.chosen_location_section = vm.main_occurrence_obj.id;
                }
                if (!vm.selectedOccurrenceIds.includes(vm.occ_combine_data.chosen_habitat_composition_section)) {
                    vm.occ_combine_data.chosen_habitat_composition_section = vm.main_occurrence_obj.id;
                }
                if (!vm.selectedOccurrenceIds.includes(vm.occ_combine_data.chosen_habitat_condition_section)) {
                    vm.occ_combine_data.chosen_habitat_condition_section = vm.main_occurrence_obj.id;
                }
                if (!vm.selectedOccurrenceIds.includes(vm.occ_combine_data.chosen_vegetation_structure_section)) {
                    vm.occ_combine_data.chosen_vegetation_structure_section = vm.main_occurrence_obj.id;
                }
                if (!vm.selectedOccurrenceIds.includes(vm.occ_combine_data.chosen_fire_history_section)) {
                    vm.occ_combine_data.chosen_fire_history_section = vm.main_occurrence_obj.id;
                }
                if (!vm.selectedOccurrenceIds.includes(vm.occ_combine_data.chosen_associated_species_section)) {
                    vm.occ_combine_data.chosen_associated_species_section = vm.main_occurrence_obj.id;
                }
                if (!vm.selectedOccurrenceIds.includes(vm.occ_combine_data.chosen_observation_detail_section)) {
                    vm.occ_combine_data.chosen_observation_detail_section = vm.main_occurrence_obj.id;
                }
                if (!vm.selectedOccurrenceIds.includes(vm.occ_combine_data.chosen_animal_observation_section)) {
                    vm.occ_combine_data.chosen_animal_observation_section = vm.main_occurrence_obj.id;
                }   
                if (!vm.selectedOccurrenceIds.includes(vm.occ_combine_data.chosen_plant_count_section)) {
                    vm.occ_combine_data.chosen_plant_count_section = vm.main_occurrence_obj.id;
                }
                if (!vm.selectedOccurrenceIds.includes(vm.occ_combine_data.chosen_identification_section)) {
                    vm.occ_combine_data.chosen_identification_section = vm.main_occurrence_obj.id;
                }

                if (!vm.selectedOccurrenceIds.includes(vm.occ_combine_data.occurrence_name)) {
                    vm.occ_combine_data.occurrence_name = vm.main_occurrence_obj.id;
                }
                if (!vm.selectedOccurrenceIds.includes(vm.occ_combine_data.occurrence_source)) {
                    vm.occ_combine_data.occurrence_source = vm.main_occurrence_obj.id;
                }
                if (!vm.selectedOccurrenceIds.includes(vm.occ_combine_data.wild_status)) {
                    vm.occ_combine_data.wild_status = vm.main_occurrence_obj.id;
                }
                if (!vm.selectedOccurrenceIds.includes(vm.occ_combine_data.review_due_date)) {
                    vm.occ_combine_data.review_due_date = vm.main_occurrence_obj.id;
                }
                if (!vm.selectedOccurrenceIds.includes(vm.occ_combine_data.comment)) {
                    vm.occ_combine_data.comment = vm.main_occurrence_obj.id;
                }

            },
            getKeyContactIds: function() {
                let vm = this;
                let formData = new FormData()
                formData.append("occurrence_ids", JSON.stringify(vm.selectedOccurrenceIds));
                //get all key contact ids for all OCCs
                vm.$http.post(
                    api_endpoints.combine_key_contacts_lookup, formData
                ).then((response) => {
                    //copy old list
                    let old_list = vm.key_contact_ids;
                    //add to main list
                    vm.key_contact_ids = response.body.id_list;
                    vm.key_contacts = response.body.values_list;

                    let contact_names = {};
                    let taken_names = [];
                    vm.key_contacts.forEach(contact => {
                        if (vm.occ_combine_data.combine_key_contact_ids.includes(contact.id)) {
                            taken_names.push(contact.contact_name);
                        }
                        contact_names[contact.id] = contact.contact_name;
                    });

                    //remove ids from combine list if not in new list
                    vm.occ_combine_data.combine_key_contact_ids.forEach(id => {
                        if (!vm.key_contact_ids.includes(id)) {
                            vm.occ_combine_data.combine_key_contact_ids.splice(vm.occ_combine_data.combine_key_contact_ids.indexOf(id), 1);
                        }
                    });

                    //add new ids to combine list if not in old list - unless they share a name
                    response.body.id_list.forEach(id => {
                        if (!old_list.includes(id) && !taken_names.includes(contact_names[id])) {
                            vm.occ_combine_data.combine_key_contact_ids.push(id);      
                        }
                    });

                    vm.contact_table_key++;
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
                    vm.documents = response.body.values_list;
                    //remove ids from combine list if not in new list
                    vm.occ_combine_data.combine_document_ids.forEach(id => {
                        if (!response.body.id_list.includes(id)) {
                            vm.occ_combine_data.combine_document_ids.splice(vm.occ_combine_data.combine_document_ids.indexOf(id), 1);
                        }
                    });
                    //add new ids to combine list if not in old list
                    response.body.id_list.forEach(id => {
                        if (!old_list.includes(id)) {
                            vm.occ_combine_data.combine_document_ids.push(id);
                        }
                    });

                    vm.document_table_key++;
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
                    vm.threats = response.body.values_list;
                    //remove ids from combine list if not in new list
                    vm.occ_combine_data.combine_threat_ids.forEach(id => {
                        if (!response.body.id_list.includes(id)) {
                            vm.occ_combine_data.combine_threat_ids.splice(vm.occ_combine_data.combine_threat_ids.indexOf(id), 1);
                        }
                    });
                    //add new ids to combine list if not in old list
                    response.body.id_list.forEach(id => {
                        if (!old_list.includes(id)) {
                            vm.occ_combine_data.combine_threat_ids.push(id);
                        }
                    });
                    vm.threat_table_key++;
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
            
        },
        mounted: function () {
            this.initialiseOccurrenceNameLookup();
        },
        watch: {
            isModalOpen: function() {
                if (this.isModalOpen) {
                    let vm = this;

                    //get key contact ids
                    vm.getKeyContactIds();
                    //get document ids
                    vm.getDocumentIds();
                    //get threat ids
                    vm.getThreatIds();

                    let dict_url = api_endpoints.occ_profile_dict + '?group_type=' + vm.main_occurrence_obj.group_type
                    vm.$http.get(dict_url).then((response) => {
                        vm.occ_profile_dict = response.body;
                        vm.wild_status_list = vm.occ_profile_dict.wild_status_list;
                        vm.occurrence_source_list = vm.occ_profile_dict.occurrence_source_list;
                    }, (error) => {
                        console.log(error);
                    })
                }
            },
            selectedOccurrenceIds: function() {
                let vm = this;
                vm.occ_combine_data.combine_ids = vm.selectedOccurrenceIds;
                //get key contact ids
                vm.getKeyContactIds();
                //get document ids
                vm.getDocumentIds();
                //get threat ids
                vm.getThreatIds();
                //check form values
                vm.checkFormValues();
            },
        },
    }
</script>