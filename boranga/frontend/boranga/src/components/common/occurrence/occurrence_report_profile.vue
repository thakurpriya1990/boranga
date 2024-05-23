<template lang="html">
    <div id="speciesOccurrenceReport">
        <FormSection :formCollapse="false" label="Occurrence Report" Index="occurrence_report">

            <div v-show="!isCommunity">
                <div class="row mb-3">
                    <label for="" class="col-sm-3 control-label">Scientific Name:</label>
                    <div :id="select_scientific_name" class="col-sm-9">
                        <select
                            :id="scientific_name_lookup"
                            :ref="scientific_name_lookup"
                            :disabled="isReadOnly"
                            :name="scientific_name_lookup"
                            class="form-control"
                        />
                    </div>
                </div>
                <div class="row mb-3">
                    <label for="" class="col-sm-3 control-label"></label>
                    <div class="col-sm-9">
                        <textarea
                            id="species_display"
                            v-model="species_display"
                            disabled
                            class="form-control"
                            rows="2"
                        />
                    </div>
                </div>
                <div class="row mb-3">
                    <label for="" class="col-sm-3 control-label">Previous Name:</label>
                    <div class="col-sm-9">
                        <input
                            id="previous_name"
                            v-model="taxon_previous_name"
                            readonly
                            type="text"
                            class="form-control"
                            placeholder=""
                        />
                    </div>
                </div>
            </div>

            <div v-show="isCommunity">
                <div class="row mb-3">
                    <label for="" class="col-sm-3 control-label">Community Name:</label>
                    <div :id="select_community_name" class="col-sm-9">
                        <select
                            :id="community_name_lookup"
                            :ref="community_name_lookup"
                            :disabled="isReadOnly"
                            :name="community_name_lookup"
                            class="form-control"
                        />
                    </div>
                </div>
                <div class="row mb-3">
                    <label for="" class="col-sm-3 control-label"></label>
                    <div class="col-sm-9">
                        <textarea
                            id="community_display"
                            v-model="community_display"
                            disabled
                            class="form-control"
                            rows="2"
                        />
                    </div>
                </div>
            </div>

            <div class="row mb-3">
                <label for="" class="col-sm-3 control-label"
                    >Site:</label
                >
                <div class="col-sm-9">
                    <textarea
                        id="site"
                        v-model="
                            occurrence_report_obj.site
                        "
                        :disabled="isReadOnly"
                        class="form-control"
                        rows="1"
                        placeholder=""
                    />
                </div>
            </div>

            <div class="row mb-3">
                <label for="" class="col-sm-3 control-label"
                    >Observation Date:</label
                >
                <div class="col-sm-9">
                    <input
                        v-model="
                            occurrence_report_obj.observation_date
                        "
                        :disabled="isReadOnly"
                        type="datetime-local"
                        class="form-control"
                        name="start_date"
                    />
                </div>
            </div>
            <!-- ------------Observer Detail section -->

            <ObserverDatatable
                ref="observer_datatable"
                :occurrence_report_obj="occurrence_report_obj"
                :is_external="is_external"
                :is-read-only="isReadOnly"
            ></ObserverDatatable>

        </FormSection>
    </div>
</template>

<script>
import { v4 as uuid } from 'uuid';
import Vue, { isReadonly } from 'vue' ;
import FormSection from '@/components/forms/section_toggle.vue';
import ObserverDatatable from './observer_datatable.vue';
import {
  api_endpoints,
  helpers
}
from '@/utils/hooks'
// require("select2/dist/css/select2.min.css");
// require("select2-bootstrap-5-theme/dist/select2-bootstrap-5-theme.min.css")

export default {
        name: 'SpeciesOccurrenceReport',
        props:{
            occurrence_report_obj:{
                type: Object,
                required:true
            },
            is_external: {
                type: Boolean,
                default: false,
            },
        },
        data:function () {
            let vm = this;
            return{
                uuid: null,
                scientific_name_lookup:
                    'scientific_name_lookup' + vm.occurrence_report_obj.id,
                select_scientific_name:
                    'select_scientific_name' + vm.occurrence_report_obj.id,
                community_name_lookup: 'community_name_lookup' + vm._uid,
                select_community_name: 'select_community_name' + vm._uid,
                isFauna:
                vm.occurrence_report_obj.group_type === 'fauna' ? true : false,
                isCommunity:
                    vm.occurrence_report_obj.group_type === 'community'
                        ? true
                        : false,
                species_list: [],
                species_display: '',
                community_display: '',
                taxon_previous_name: '',
            }
        },
        components: {
            FormSection,
            ObserverDatatable,
        },
        watch:{
        },
        methods:{
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
                                    cs_species: true,
                                    cs_species_status:
                                        vm.occurrence_report_obj.processing_status,
                                };
                                return query;
                            },
                            // results: function (data, page) { // parse the results into the format expected by Select2.
                            //     // since we are using custom formatting functions we do not need to alter remote JSON data
                            //     return {results: data};
                            // },
                        },
                    })
                    .on('select2:select', function (e) {
                        // eslint-disable-next-line no-unused-vars
                        var selected = $(e.currentTarget);
                        let data = e.params.data.id;
                        vm.occurrence_report_obj.species_id = data;
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
                for (let choice of vm.species_list) {
                    if (choice.id === vm.occurrence_report_obj.species_id) {
                        const newOption = new Option(
                            choice.name,
                            choice.id,
                            false,
                            true
                        );
                        $('#' + vm.scientific_name_lookup).append(newOption);
                        vm.species_display = choice.name;
                        vm.taxon_previous_name = choice.taxon_previous_name;
                    }
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
                            // results: function (data, page) { // parse the results into the format expected by Select2.
                            //     // since we are using custom formatting functions we do not need to alter remote JSON data
                            //     return {results: data};
                            // },
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
                for (let choice of this.community_list) {
                    if (choice.id === this.occurrence_report_obj.community_id) {
                        const newOption = new Option(
                            choice.name,
                            choice.id,
                            false,
                            true
                        );
                        $('#' + this.community_name_lookup).append(newOption);
                        this.community_display = choice.name;
                    }
                }
            },
            incrementComponentMapKey: function () {
                this.uuid = uuid();
            },
            eventListeners: function () {
                let vm = this;
            },
        },
        created: async function() {
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
                    vm.species_list = vm.cs_profile_dict.species_list;
                    this.getSpeciesDisplay();

                    vm.community_list = vm.cs_profile_dict.community_list;
                    this.getCommunityDisplay();
                },
                (error) => {
                    console.log(error);
                }
            );
        },
        computed: {
            isReadOnly: function(){
                //override for split reports
                if(this.is_readonly){
                    return this.is_readonly;
                }
                return this.occurrence_report_obj.readonly
            },
            csrf_token: function () {
                return helpers.getCookie('csrftoken');
            },
        },
        mounted: function(){
            let vm = this;
            this.$nextTick(() => {
                vm.eventListeners();
                vm.initialiseScientificNameLookup();
                vm.initialiseCommunityNameLookup();
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
    -webkit-box-shadow:  0px 0px 0px 0px #000;
            box-shadow:  0px 0px 0px 0px #000;
    }
    legend.scheduler-border {
    width:inherit; /* Or auto */
    padding:0 10px; /* To give a bit of padding on the left and right */
    border-bottom:none;
    }
    input[type=text], select {
        width: 100%;
        padding: 0.375rem 2.25rem 0.375rem 0.75rem;
    }
    input[type=number] {
        width: 50%;
    }
</style>

