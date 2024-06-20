<template lang="html">
    <div id="communityOccurrence">
        <FormSection :formCollapse="false" label="Occurrence" Index="occurrence">
            <div class="row mb-3">
                <label for="" class="col-sm-3 control-label">Occurrence Name:</label>
                <div class="col-sm-9">
                    <textarea class="form-control" :disabled="isReadOnly" rows="1" id="occurrence_name" placeholder=""
                        v-model="occurrence_obj.occurrence_name" />
                </div>
            </div>
            <div class="row mb-3">
                <label for="" class="col-sm-3 control-label">Community Name:</label>
                <div class="col-sm-9" :id="select_community_name">
                    <select :disabled="isReadOnly" :id="community_name_lookup" :name="community_name_lookup"
                        :ref="community_name_lookup" class="form-control" />
                </div>
            </div>
            <div class="row mb-3">
                <label for="" class="col-sm-3 control-label">Occurrence Source:</label>
                <div v-for="source in occurrence_source_list" class="col-sm-auto">
                    <input :disabled="isReadOnly" type="checkbox" v-model="occurrence_obj.occurrence_source" v-bind:value="source[0]" v-bind:id="source[1]">
                    {{ source[1] }}
                </div>
            </div>
            <div class="row mb-3">
                <label for="" class="col-sm-3 control-label">Wild Status:</label>
                <div class="col-sm-9">
                    <select :disabled="isReadOnly" 
                        class="form-select" 
                        v-model="occurrence_obj.wild_status">
                        <option value="" selected disabled>Select Wild Status</option>
                        <option v-for="option in wild_status_list" :value="option.id" :key="option.id">
                            {{ option.name }}
                        </option>
                    </select>
                </div>
            </div>
            <div class="row mb-3">
                <label for="" class="col-sm-3 control-label">Comments:</label>
                <div class="col-sm-9">
                    <textarea class="form-control" :disabled="isReadOnly" id="occurrence_comments" placeholder=""
                        v-model="occurrence_obj.comment" />
                </div>
            </div>
            <ContactDatatable ref="contact_datatable" :occurrence_obj="occurrence_obj"
                :is-read-only="isReadOnly" @refreshOccurrence="refreshOccurrence()">
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
}
    from '@/utils/hooks'

export default {
    name: 'CommunityOccurrence',
    props: {
        occurrence_obj: {
            type: Object,
            required: true
        },
    },
    data: function () {
        let vm = this;
        return {
            community_name_lookup: 'community_name_lookup' + vm.occurrence_obj.id,
            select_community_name: "select_community_name" + vm.occurrence_obj.id,
            occ_profile_dict: {},
            community_list: [],
            wild_status_list: [],
            occurrence_source_list: [],
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
        initialiseCommunityNameLookup: function () {
            let vm = this;
            $(vm.$refs[vm.community_name_lookup]).select2({
                minimumInputLength: 2,
                dropdownParent: $("#" + vm.select_community_name),
                "theme": "bootstrap-5",
                allowClear: true,
                placeholder: "Select Community Name",
                ajax: {
                    url: api_endpoints.community_name_lookup,
                    dataType: 'json',
                    data: function (params) {
                        var query = {
                            term: params.term,
                            type: 'public',
                            group_type_id: vm.occurrence_obj.group_type_id,
                            cs_community: true,
                            cs_community_status: vm.occurrence_obj.processing_status,
                        }
                        return query;
                    },
                },
            }).
                on("select2:select", function (e) {
                    var selected = $(e.currentTarget);
                    let data = e.params.data.id;
                    vm.occurrence_obj.community = data;
                    vm.occurrence_obj.community_id = data.id;
                    vm.community_display = e.params.data.text;
                    vm.taxon_previous_name = e.params.data.taxon_previous_name;
                }).
                on("select2:unselect", function (e) {
                    var selected = $(e.currentTarget);
                    vm.occurrence_obj.community_id = null
                    vm.community_display = '';
                    vm.taxon_previous_name = '';
                }).
                on("select2:open", function (e) {
                    const searchField = $('[aria-controls="select2-' + vm.community_name_lookup + '-results"]')
                    searchField[0].focus();
                });
        },
        getCommunityDisplay: function () {
            let vm = this;
            for (let choice of vm.community_list) {
                if (choice.id === vm.occurrence_obj.community) {
                    var newOption = new Option(choice.name, choice.id, false, true);
                    $('#' + vm.community_name_lookup).append(newOption);
                    vm.community_display = choice.name;
                    vm.taxon_previous_name = choice.taxon_previous_name;
                }
            }
        },
        eventListeners: function () {
            let vm = this;

        },
    },
    created: async function () {
        let vm = this;
        let action = this.$route.query.action;
        let dict_url = action == "view" ? api_endpoints.occ_profile_dict + '?group_type=' + vm.occurrence_obj.group_type + '&action=' + action :
            api_endpoints.occ_profile_dict + '?group_type=' + vm.occurrence_obj.group_type
        vm.$http.get(dict_url).then((response) => {
            vm.occ_profile_dict = response.body;
            vm.community_list = vm.occ_profile_dict.community_list;
            vm.wild_status_list = vm.occ_profile_dict.wild_status_list;
            vm.occurrence_source_list = vm.occ_profile_dict.occurrence_source_list;
            this.getCommunityDisplay();

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
