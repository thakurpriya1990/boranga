<template lang="html">
    <div id="speciesOccurrence">
        <FormSection :formCollapse="false" label="Occurrence" Index="occurrence">
            <div class="row mb-3">
                <label for="" class="col-sm-3 control-label">Occurrence Name:</label>
                <div class="col-sm-9">
                    <textarea class="form-control" :disabled="isReadOnly" rows="1" id="occurrence_name" placeholder=""
                        v-model="occurrence_obj.occurrence_name" />
                </div>
            </div>
            <div class="row mb-3">
                <label for="" class="col-sm-3 control-label">Scientific Name:</label>
                <div class="col-sm-9" :id="select_scientific_name">
                    <select :disabled="isReadOnly" :id="scientific_name_lookup" :name="scientific_name_lookup"
                        :ref="scientific_name_lookup" class="form-control" />
                </div>
            </div>
            <div class="row mb-3">
                <label for="" class="col-sm-3 control-label">Common Name:</label>
                <div class="col-sm-9">
                    <textarea :disabled="true" class="form-control" rows="1" id="common_name" placeholder=""
                        v-model="common_name" />
                </div>
            </div>
            <div class="row mb-3">
                <label for="" class="col-sm-3 control-label">Occurrence Source:</label>
                <div class="col-sm-9" :id="select_occurrence_source">
                    <select :disabled="isReadOnly" :id="occurrence_source_lookup" :name="occurrence_source_lookup"
                        :ref="occurrence_source_lookup" class="form-control" />
                </div>
            </div>
            <div class="row mb-3">
                <label for="" class="col-sm-3 control-label">Wild Status:</label>
                <div class="col-sm-9" :id="select_wild_status">
                    <select :disabled="isReadOnly" :id="wild_status_lookup" :name="wild_status_lookup"
                        :ref="wild_status_lookup" class="form-control" />
                </div>
            </div>
            <div class="row mb-3">
                <label for="" class="col-sm-3 control-label">Comments:</label>
                <div class="col-sm-9">
                    <textarea class="form-control" :disabled="isReadOnly" id="occurrence_comments" placeholder=""
                        v-model="occurrence_obj.comment" rows="4"/>
                </div>
            </div>

            <ContactDatatable ref="contact_datatable" :occurrence_obj="occurrence_obj"
                :is_external="is_external" :is-read-only="isReadOnly"
                @refreshOccurrence="refreshOccurrence()">
            </ContactDatatable>

            <RelatedReports :isReadOnly="isReadOnly" :occurrence_obj=occurrence_obj />
        </FormSection>
    </div>
</template>

<script>
import FormSection from '@/components/forms/section_toggle.vue';
import ContactDatatable from './contact_datatable.vue';
import RelatedReports from '@/components/common/occurrence/occ_related_ocr_table.vue'
import {
    api_endpoints,
    helpers
}
    from '@/utils/hooks'

export default {
    name: 'SpeciesOccurrence',
    props: {
        occurrence_obj: {
            type: Object,
            required: true
        },
    },
    data: function () {
        let vm = this;
        return {
            scientific_name_lookup: 'scientific_name_lookup' + vm._uid,
            select_scientific_name: "select_scientific_name" + vm._uid,
            occurrence_source_lookup: 'occurrence_source_lookup' + vm._uid,
            select_occurrence_source: "select_occurrence_source" + vm._uid,
            wild_status_lookup: 'wild_status_lookup' + vm._uid,
            select_wild_status: "select_wild_status" + vm._uid,
            common_name: null,
            occ_profile_dict: {},
            species_list: [],
            source_list: [],
            wild_status_list: [],
        }
    },
    components: {
        FormSection,
        RelatedReports,
        ContactDatatable,
    },
    watch: {
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
                            group_type_id: vm.occurrence_obj.group_type_id,
                            has_species: true,
                        }
                        return query;
                    },
                    // results: function (data, page) { // parse the results into the format expected by Select2.
                    //     // since we are using custom formatting functions we do not need to alter remote JSON data
                    //     return {results: data};
                    // },
                },
            }).
                on("select2:select", function (e) {
                    var selected = $(e.currentTarget);
                    let data = e.params.data.id;
                    vm.occurrence_obj.species = e.params.data.species_id;
                    //vm.occurrence_obj.species_id = data.species_id;
                    vm.species_display = e.params.data.text;
                    vm.taxon_previous_name = e.params.data.taxon_previous_name;
                    vm.common_name = e.params.data.common_name;
                }).
                on("select2:unselect", function (e) {
                    var selected = $(e.currentTarget);
                    vm.occurrence_obj.species = null;
                    //vm.occurrence_obj.species_id = null
                    vm.species_display = '';
                    vm.taxon_previous_name = '';
                    vm.common_name = '';
                }).
                on("select2:open", function (e) {
                    const searchField = $('[aria-controls="select2-' + vm.scientific_name_lookup + '-results"]')
                    // move focus to select2 field
                    searchField[0].focus();
                });
        },
        initialiseOccurrenceSourceLookup: function () {
            let vm = this;
            $(vm.$refs[vm.occurrence_source_lookup]).select2({
                minimumInputLength: 2,
                dropdownParent: $("#" + vm.select_occurrence_source),
                "theme": "bootstrap-5",
                allowClear: true,
                placeholder: "Select Occurrence Source",
                ajax: {
                    url: api_endpoints.occurrence_source_lookup,
                    dataType: 'json',
                    data: function (params) {
                        var query = {
                            term: params.term,
                            type: 'public',
                        }
                        return query;
                    },
                },
            }).
                on("select2:select", function (e) {
                    var selected = $(e.currentTarget);
                    let data = e.params.data.id;
                    vm.occurrence_obj.occurrence_source = data;
                }).
                on("select2:unselect", function (e) {
                    var selected = $(e.currentTarget);
                    vm.occurrence_obj.occurrence_source = null;
                }).
                on("select2:open", function (e) {
                    const searchField = $('[aria-controls="select2-' + vm.occurrence_source_lookup + '-results"]')
                    // move focus to select2 field
                    searchField[0].focus();
                });
        },
        initialiseWildStatusLookup: function () {
            let vm = this;
            $(vm.$refs[vm.wild_status_lookup]).select2({
                minimumInputLength: 2,
                dropdownParent: $("#" + vm.select_wild_status),
                "theme": "bootstrap-5",
                allowClear: true,
                placeholder: "Select Wild Status",
                ajax: {
                    url: api_endpoints.wild_status_lookup,
                    dataType: 'json',
                    data: function (params) {
                        var query = {
                            term: params.term,
                            type: 'public',
                        }
                        return query;
                    },
                },
            }).
                on("select2:select", function (e) {
                    var selected = $(e.currentTarget);
                    let data = e.params.data.id;
                    vm.occurrence_obj.wild_status = data;
                }).
                on("select2:unselect", function (e) {
                    var selected = $(e.currentTarget);
                    vm.occurrence_obj.wild_status = null;
                }).
                on("select2:open", function (e) {
                    const searchField = $('[aria-controls="select2-' + vm.wild_status_lookup + '-results"]')
                    // move focus to select2 field
                    searchField[0].focus();
                });
        },
        getSpeciesDisplay: function () {
            let vm = this;
            if (vm.occurrence_obj.species != null) {
                let species_display_url = api_endpoints.species_display +
                    "?species_id=" + vm.occurrence_obj.species
                vm.$http.get(species_display_url).then(
                    (response) => {
                        var newOption = new Option(response.body.name, response.body.id, false, true);
                        $('#' + vm.scientific_name_lookup).append(newOption);
                        vm.species_display = response.body.name;
                        vm.taxon_previous_name = response.body.taxon_previous_name;
                        vm.common_name = response.body.common_name;
                    })
            }
            /*for(let choice of vm.species_list){
                    if(choice.id === vm.occurrence_obj.species)
                    {
                        var newOption = new Option(choice.name, choice.id, false, true);
                        $('#'+ vm.scientific_name_lookup).append(newOption);
                        vm.species_display = choice.name;
                        vm.taxon_previous_name = choice.taxon_previous_name;
                        vm.common_name = choice.common_name;
                    }
                }*/
        },
        getSourceDisplay: function () {
            let vm = this;
            for (let choice of vm.source_list) {
                if (choice.id === vm.occurrence_obj.occurrence_source) {
                    var newOption = new Option(choice.name, choice.id, false, true);
                    $('#' + vm.occurrence_source_lookup).append(newOption);
                }
            }
        },
        getWildStatusDisplay: function () {
            let vm = this;
            for (let choice of vm.wild_status_list) {
                console.log(choice, vm.occurrence_obj.wild_status)
                if (choice.id === vm.occurrence_obj.wild_status) {
                    var newOption = new Option(choice.name, choice.id, false, true);
                    $('#' + vm.wild_status_lookup).append(newOption);
                }
            }
        },
        eventListeners: function () {
            let vm = this;

        },
    },
    created: async function () {
        let vm = this;
        //------fetch list of values according to action
        let action = this.$route.query.action;
        let dict_url = action == "view" ? api_endpoints.occ_profile_dict + '?group_type=' + vm.occurrence_obj.group_type + '&action=' + action :
            api_endpoints.occ_profile_dict + '?group_type=' + vm.occurrence_obj.group_type
        vm.$http.get(dict_url).then((response) => {
            vm.occ_profile_dict = response.body;
            vm.species_list = vm.occ_profile_dict.species_list;
            vm.source_list = vm.occ_profile_dict.source_list;
            vm.wild_status_list = vm.occ_profile_dict.wild_status_list;
            this.getSpeciesDisplay();
            this.getSourceDisplay();
            this.getWildStatusDisplay();

        }, (error) => {
            console.log(error);
        })
    },
    computed: {
        isReadOnly: function () {
            return !(this.occurrence_obj.can_user_edit);
        },
    },
    mounted: function () {
        let vm = this;
        this.$nextTick(() => {
            vm.eventListeners();
            vm.initialiseScientificNameLookup();
            vm.initialiseOccurrenceSourceLookup();
            vm.initialiseWildStatusLookup();
        });
    },
}
</script>

<style lang="css" scoped>
/*ul, li {
        zoom:1;
        display: inline;
    }*/
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
