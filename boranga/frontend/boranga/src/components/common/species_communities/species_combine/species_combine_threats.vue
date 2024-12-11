<template lang="html">
    <div id="species_split_threats">
        <FormSection :form-collapse="false" label="Threats" :Index="threatBody">
            <form class="form-horizontal" action="index.html" method="post">
                <div class="col-sm-12 form-check form-check-inline">
                    <input
                        :id="'threat_select_all' + species_original.id"
                        class="form-check-input"
                        type="radio"
                        name="threatSelect"
                        value="selectAll"
                        @click="selectThreatOption($event)"
                    />
                    <label class="form-check-label"
                        >Copy all threats from Species
                        {{ species_original.species_number }}</label
                    >
                </div>
                <div class="col-sm-12 form-check form-check-inline mb-3">
                    <input
                        :id="'threat_select_individual' + species_original.id"
                        class="form-check-input"
                        type="radio"
                        name="threatSelect"
                        value="individual"
                        @click="selectThreatOption($event)"
                    />
                    <label class="form-check-label">Decide per threat</label>
                </div>
                <div>
                    <datatable
                        :id="panelBody"
                        ref="threats_datatable"
                        :dt-options="threats_options"
                        :dt-headers="threats_headers"
                    />
                </div>
            </form>
        </FormSection>
    </div>
</template>
<script>
import datatable from '@vue-utils/datatable.vue';
import FormSection from '@/components/forms/section_toggle.vue';
import { constants, api_endpoints, helpers } from '@/utils/hooks';

export default {
    name: 'SpeciesCombineThreats',
    components: {
        FormSection,
        datatable,
    },
    props: {
        species_community: {
            type: Object,
            required: true,
        },
        species_original: {
            type: Object,
            required: true,
        },
    },
    data: function () {
        let vm = this;
        return {
            uuid: 0,
            threatBody: 'threatBody' + vm._uid,
            panelBody: 'species-combine-threats-' + vm._uid,
            values: null,
            // to store all the documents of original on first load.
            original_species_threats: [],
            threat_url: api_endpoints.threat,
            threats_headers: [
                'Number',
                'Category',
                'Threat Source',
                'Date Observed',
                'Threat Agent',
                'Comments',
                'Current Impact?',
                'Potential Impact?',
                'Action',
            ],
            threats_options: {
                autowidth: false,
                language: {
                    processing: constants.DATATABLE_PROCESSING_HTML,
                },
                responsive: true,
                searching: true,
                //  to show the "workflow Status","Action" columns always in the last position
                columnDefs: [
                    { responsivePriority: 1, targets: 0 },
                    { responsivePriority: 2, targets: -1 },
                ],
                ajax: {
                    url: helpers.add_endpoint_json(
                        api_endpoints.species,
                        vm.species_original.id + '/threats'
                    ),
                    dataSrc: '',
                },
                order: [[0, 'desc']],
                dom:
                    "<'d-flex align-items-center'<'me-auto'l>fB>" +
                    "<'row'<'col-sm-12'tr>>" +
                    "<'d-flex align-items-center'<'me-auto'i>p>",
                buttons: [
                    {
                        extend: 'excel',
                        title: 'Boranga Species Combine Threats Excel Export',
                        text: '<i class="fa-solid fa-download"></i> Excel',
                        className: 'btn btn-primary me-2 rounded',
                        exportOptions: {
                            orthogonal: 'export',
                        },
                    },
                    {
                        extend: 'csv',
                        title: 'Boranga Species Combine Threats CSV Export',
                        text: '<i class="fa-solid fa-download"></i> CSV',
                        className: 'btn btn-primary rounded',
                        exportOptions: {
                            orthogonal: 'export',
                        },
                    },
                ],
                columns: [
                    {
                        data: 'threat_number',
                        orderable: true,
                        searchable: true,
                        mRender: function (data, type, full) {
                            if (full.visible) {
                                return full.threat_number;
                            } else {
                                return '<s>' + full.threat_number + '</s>';
                            }
                        },
                    },
                    {
                        data: 'threat_category',
                        orderable: true,
                        searchable: true,
                        mRender: function (data, type, full) {
                            if (full.visible) {
                                return full.threat_category;
                            } else {
                                return '<s>' + full.threat_category + '</s>';
                            }
                        },
                    },
                    {
                        data: 'source',
                        orderable: true,
                        searchable: true,
                        mRender: function (data, type, full) {
                            if (full.visible) {
                                return full.source;
                            } else {
                                return '<s>' + full.source + '</s>';
                            }
                        },
                    },
                    {
                        data: 'date_observed',
                        mRender: function (data, type, full) {
                            if (full.visible) {
                                return data != '' && data != null
                                    ? moment(data).format('DD/MM/YYYY')
                                    : '';
                            } else {
                                return data != '' && data != null
                                    ? '<s>' + moment(data).format('DD/MM/YYYY')
                                    : '' + '</s>';
                            }
                        },
                    },
                    {
                        data: 'threat_agent',
                        orderable: true,
                        searchable: true,
                        mRender: function (data, type, full) {
                            if (full.visible) {
                                return full.threat_agent;
                            } else {
                                return '<s>' + full.threat_agent + '</s>';
                            }
                        },
                    },
                    {
                        data: 'comment',
                        orderable: true,
                        searchable: true,
                        render: function (value, type, full) {
                            let result = helpers.dtPopover(value, 30, 'hover');
                            if (full.visible) {
                                return type == 'export' ? value : result;
                            } else {
                                return type == 'export'
                                    ? '<s>' + value + '</s>'
                                    : '<s>' + result + '</s>';
                            }
                        },
                    },
                    {
                        data: 'current_impact_name',
                        orderable: true,
                        searchable: true,
                        mRender: function (data, type, full) {
                            if (full.visible) {
                                return full.current_impact_name;
                            } else {
                                return (
                                    '<s>' + full.current_impact_name + '</s>'
                                );
                            }
                        },
                    },
                    {
                        data: 'potential_impact_name',
                        orderable: true,
                        searchable: true,
                        mRender: function (data, type, full) {
                            if (full.visible) {
                                return full.potential_impact_name;
                            } else {
                                return (
                                    '<s>' + full.potential_impact_name + '</s>'
                                );
                            }
                        },
                    },
                    {
                        data: 'id',
                        mRender: function (data, type, full) {
                            // to store the original species documents for the use of radio btn options on first load so that no need to call api to get the documents ids
                            if (
                                !vm.original_species_threats.includes(full.id)
                            ) {
                                vm.original_species_threats.push(full.id);
                            }

                            if (
                                vm.species_community.threats.includes(full.id)
                            ) {
                                return `<input class='form-check-input' type="checkbox" id="threat_chkbox-${vm.species_community.id}-${full.id}" data-add-threat="${full.id}"  checked>`;
                            } else {
                                return `<input class='form-check-input' type="checkbox" id="threat_chkbox-${vm.species_community.id}-${full.id}" data-add-threat="${full.id}">`;
                            }
                        },
                    },
                ],
                processing: true,
                drawCallback: function () {
                    helpers.enablePopovers();
                },
                initComplete: function () {
                    helpers.enablePopovers();
                    // another option to fix the responsive table overflow css on tab switch
                    setTimeout(function () {
                        vm.adjust_table_width();
                    }, 100);
                },
            },
        };
    },
    computed: {},
    mounted: function () {
        let vm = this;
        this.$nextTick(() => {
            if (vm.species_original.threat_selection != null) {
                if (vm.species_original.threat_selection === 'selectAll') {
                    document.getElementById(
                        'threat_select_all' + vm.species_original.id
                    ).checked = true;
                } else {
                    document.getElementById(
                        'threat_select_individual' + vm.species_original.id
                    ).checked = true;
                }
            }
            vm.addEventListeners();
        });
    },
    methods: {
        selectThreatOption(e) {
            let vm = this;
            //--fetch the value of selected radio btn
            let selected_option = e.target.value;
            //----set the selected value to the original species object so as to get the data when tab is reloaded/refreshed
            vm.species_original.threat_selection = selected_option;

            if (selected_option == 'selectAll') {
                //---first need to delete the original_species_threats from the new_arr if added from the "Decide individual" option to avoid duplication
                vm.species_community.threats =
                    vm.species_community.threats.filter(
                        (x) => vm.original_species_threats.indexOf(x) == -1
                    ); //--"filter" used to delete one array from another
                //-- copy all original species threats to new species threats array
                //---use '...' spread operator to add one arr elemnents to other
                vm.species_community.threats.push(
                    ...vm.original_species_threats
                );
                this.$refs.threats_datatable.vmDataTable.ajax.reload();
            } else if (selected_option == 'individual') {
                //----empty only the current original species array from the new species array as will contain other original combine species threat_id's as well
                vm.species_community.threats =
                    vm.species_community.threats.filter(
                        (x) => vm.original_species_threats.indexOf(x) == -1
                    ); //--"filter" used to delete one array from another
                this.$refs.threats_datatable.vmDataTable.ajax.reload();
            }
        },
        addEventListeners: function () {
            let vm = this;
            vm.$refs.threats_datatable.vmDataTable.on(
                'click',
                'input[data-add-threat]',
                function () {
                    //e.preventDefault();
                    let id = $(this).attr('data-add-threat');
                    let chkbox = $(this).attr('id');
                    if ($('#' + chkbox).is(':checked') == true) {
                        if (!vm.species_community.threats.includes(id)) {
                            vm.species_community.threats.push(parseInt(id));
                        }
                    } else {
                        let threat_arr = vm.species_community.threats;
                        //---remove document id from array (for this arr.splice is used)
                        var index = threat_arr.indexOf(id);
                        vm.species_community.threats.splice(index, 1);
                    }
                }
            );
            vm.$refs.threats_datatable.vmDataTable.on(
                'childRow.dt',
                function () {
                    helpers.enablePopovers();
                }
            );
        },
        adjust_table_width: function () {
            if (this.$refs.threats_datatable !== undefined) {
                this.$refs.threats_datatable.vmDataTable.columns
                    .adjust()
                    .responsive.recalc();
            }
        },
    },
};
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
    width: inherit; /* Or auto */
    padding: 0 10px; /* To give a bit of padding on the left and right */
    border-bottom: none;
}
</style>
