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
        <div class="row">
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
            }
        },
        methods: {
            close: function () {
                this.errorString = '';
                this.isModalOpen = false;
                $('.has-error').removeClass('has-error');
            },
            addOccurrence: function () {
                console.log(this.selectedOccurrences);
            },
            initialiseOccurrenceNameLookup: function () {
                let vm = this;
                $(vm.$refs.occurrence_name_lookup).select2({
                    width: '100%',
                    minimumInputLength: 2,
                    theme: 'bootstrap-5',
                    allowClear: true,
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
                    
                }).
                on("select2:open", function (e) {
                   
                }).
                on("select2:unselect", function (e) {
                    
                });
            },
        },
        mounted: function () {
            this.initialiseOccurrenceNameLookup();
        }
    }
</script>