<template lang="html">
    <div :id="'related_species'">
        <div class="row mb-3">
            <label for="" class="col-sm-3 control-label">NOMOS Lookup:</label>
            <div :id="select_scientific_name" class="col-sm-6">
                <select
                    :id="scientific_name_lookup"
                    :ref="scientific_name_lookup"
                    :disabled="isReadOnly"
                    :name="scientific_name_lookup"
                    class="form-control"
                />
            </div>
            <div class="col-sm-12">
                <div class="text-end">
                    <button
                        :disabled="isReadOnly || adding_species"
                        type="button"
                        class="btn btn-primary mb-2"
                        @click.prevent="addRelatedSpecies"
                    >
                        <i class="fa-solid fa-circle-plus"></i>
                        Add Related Species
                    </button>
                </div>
            </div>
        </div>

        <div>
            <datatable
                :id="datatable_id"
                ref="related_species_datatable"
                :dt-options="datatable_options"
                :dt-headers="datatable_headers"
            />
        </div>
    </div>
</template>

<script>
import { v4 as uuid } from 'uuid';
import datatable from '@/utils/vue/datatable.vue';
import { constants, api_endpoints, helpers } from '@/utils/hooks';

export default {
    name: 'TableRelatedSpecies',
    components: {
        datatable,
    },
    props: {
        occurrence_report_obj: {
            type: Object,
            required: true,
        },
        isReadOnly: {
            type: Boolean,
            default: false,
        },
    },
    data() {
        let vm = this;
        return {
            scientific_name_lookup:
                'scientific_name_lookup' + vm.occurrence_report_obj.id,
            select_scientific_name:
                'select_scientific_name' + vm.occurrence_report_obj.id,
            selected_scientific_name: null,
            adding_species: false,
            uuid: 0,
            datatable_id: uuid(),
        };
    },
    computed: {
        column_scientific_name: function () {
            return {
                data: 'scientific_name',
                orderable: true,
                searchable: true,
                visible: true,
                render: function (value, type) {
                    let result = helpers.dtPopover(value, 30, 'hover');
                    return type == 'export' ? value : result;
                },
            };
        },
        column_common_name: function () {
            return {
                data: 'common_name',
                orderable: true,
                searchable: true,
                visible: true,
                render: function (value, type) {
                    let result = helpers.dtPopover(value, 30, 'hover');
                    return type == 'export' ? value : result;
                },
            };
        },
        column_kingdom: function () {
            return {
                data: 'kingdom_name',
                orderable: true,
                searchable: true,
                visible: true,
                render: function (value, type) {
                    let result = helpers.dtPopover(value, 30, 'hover');
                    return type == 'export' ? value : result;
                },
            };
        },
        column_action: function () {
            let vm = this;
            return {
                data: 'id',
                orderable: false,
                searchable: false,
                visible: true,
                render: function (row, type, full) {
                    let links = '';
                    if (!vm.isReadOnly) {
                        links += `<a href='#' data-remove-related-species='${full.id}'>Remove</a><br>`;
                    }
                    return links;
                },
            };
        },
        datatable_options: function () {
            let vm = this;
            let columns = [
                vm.column_scientific_name,
                vm.column_common_name,
                vm.column_kingdom,
                vm.column_action,
            ];
            return {
                autoWidth: false,
                language: {
                    processing: constants.DATATABLE_PROCESSING_HTML,
                },
                responsive: true,
                //serverSide: true,
                searching: true,
                ordering: true,
                order: [[0, 'desc']],
                ajax: {
                    url:
                        '/api/occurrence_report/' +
                        this.occurrence_report_obj.id +
                        '/get_related_species/',
                    dataSrc: '',
                },
                dom: 'lBfrtip',
                buttons: [],
                columns: columns,
                processing: true,
            };
        },
        datatable_headers: function () {
            return ['Scientific Name', 'Common Name', 'Kingdom', 'Action'];
        },
    },
    mounted: function () {
        let vm = this;
        this.$nextTick(() => {
            vm.initialiseScientificNameLookup();
            vm.addEventListeners();
        });
    },
    methods: {
        reload: function () {
            let vm = this;
            vm.$refs.related_species_datatable.vmDataTable.ajax.reload();
        },
        addRelatedSpecies: function () {
            let vm = this;
            if (vm.selected_scientific_name && !vm.adding_species) {
                vm.adding_species = true;
                fetch(
                    '/api/occurrence_report/' +
                        this.occurrence_report_obj.id +
                        '/add_related_species?species=' +
                        vm.selected_scientific_name
                ).then(
                    async (response) => {
                        if (!response.ok) {
                            const data = await response.json();
                            swal.fire({
                                title: 'Error',
                                text: data,
                                icon: 'error',
                                customClass: {
                                    confirmButton: 'btn btn-primary',
                                },
                            });
                            return;
                        }
                        swal.fire({
                            title: 'Added',
                            text: 'Related Species has been added',
                            icon: 'success',
                            customClass: {
                                confirmButton: 'btn btn-primary',
                            },
                        });
                        vm.$refs.related_species_datatable.vmDataTable.ajax.reload();
                        vm.selected_scientific_name = null;
                        vm.adding_species = false;
                        if (
                            vm.occurrence_report_obj.processing_status ==
                            'Unlocked'
                        ) {
                            vm.$router.go();
                        }
                    },
                    (error) => {
                        console.log(error);
                        vm.adding_species = false;
                    }
                );
            }
        },
        removeRelatedSpecies: function (id) {
            let vm = this;
            swal.fire({
                title: 'Remove Related Species',
                text: 'Are you sure you want to remove this Related Species?',
                icon: 'question',
                showCancelButton: true,
                confirmButtonText: 'Remove Related Species',
                customClass: {
                    confirmButton: 'btn btn-primary',
                    cancelButton: 'btn btn-secondary',
                },
                reverseButtons: true,
            }).then((result) => {
                if (result.isConfirmed) {
                    fetch(
                        '/api/occurrence_report/' +
                            this.occurrence_report_obj.id +
                            '/remove_related_species?species=' +
                            id
                    ).then(
                        async (response) => {
                            if (!response.ok) {
                                const data = await response.json();
                                swal.fire({
                                    title: 'Error',
                                    text: data,
                                    icon: 'error',
                                    customClass: {
                                        confirmButton: 'btn btn-primary',
                                    },
                                });
                                return;
                            }
                            swal.fire({
                                title: 'Removed',
                                text: 'Related Species has been removed',
                                icon: 'success',
                                customClass: {
                                    confirmButton: 'btn btn-primary',
                                },
                            });
                            vm.$refs.related_species_datatable.vmDataTable.ajax.reload();
                            if (
                                vm.occurrence_report_obj.processing_status ==
                                'Unlocked'
                            ) {
                                vm.$router.go();
                            }
                        },
                        (error) => {
                            console.log(error);
                        }
                    );
                }
            });
        },
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
                    let data = e.params.data.id;
                    vm.selected_scientific_name = data;
                })
                .on('select2:unselect', function () {
                    vm.selected_scientific_name = null;
                })
                .on('select2:open', function () {
                    const searchField = $(
                        '[aria-controls="select2-' +
                            vm.scientific_name_lookup +
                            '-results"]'
                    );
                    // move focus to select2 field
                    searchField[0].focus();
                });
        },
        addEventListeners: function () {
            let vm = this;
            vm.$refs.related_species_datatable.vmDataTable.on(
                'click',
                'a[data-remove-related-species]',
                function (e) {
                    e.preventDefault();
                    var id = $(this).attr('data-remove-related-species');
                    vm.removeRelatedSpecies(id);
                }
            );
        },
    },
};
</script>
