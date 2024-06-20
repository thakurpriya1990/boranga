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
        <div class="row" id="occurrence_name_lookup_form_group_id">
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

        <!--Main OCC Form-->

        <!--Key Contacts Table-->

        <!--OCC Tabs-->

        </modal>
    </div>
</template>

<script>
    import modal from '@vue-utils/bootstrap-modal.vue';
    import { helpers, api_endpoints } from "@/utils/hooks.js"
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
        },
        data: function () {
            return {
                isModalOpen: false,
                selectedOccurrences: [this.main_occurrence_obj],
                selectedOccurrenceIds: [this.main_occurrence_obj.id],
                selectedAddOccurrence: null,
                occ_profile_dict: {},
                wild_status_list: [],
                occurrence_source_list: [],
            }
        },
        methods: {
            close: function () {
                this.errorString = '';
                this.isModalOpen = false;
                $('.has-error').removeClass('has-error');
            },
            addOccurrence: function () {
                let vm = this;
                console.log(vm.selectedOccurrenceIds);
                if (!vm.selectedOccurrenceIds.includes(vm.selectedAddOccurrence.id)) {
                    vm.selectedOccurrenceIds.push(vm.selectedAddOccurrence.id);
                    vm.selectedOccurrences.push(vm.selectedAddOccurrence);
                }
                console.log(vm.selectedOccurrences);
                vm.selectedAddOccurrence = null;
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
                    vm.selectedAddOccurrence = null;
                });
            },
        },
        created: async function () {
            let vm = this;
            let action = this.$route.query.action;
            let dict_url = action == "view" ? api_endpoints.occ_profile_dict + '?group_type=' + vm.occurrence_obj.group_type + '&action=' + action :
                api_endpoints.occ_profile_dict + '?group_type=' + vm.occurrence_obj.group_type
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
        }
    }
</script>