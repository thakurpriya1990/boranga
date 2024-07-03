<template lang="html">
    <div id="occurrenceCombineThreats">
        <datatable ref="threats_datatable" :id="panelBody" :dtOptions="threats_options"
                    :dtHeaders="threats_headers"/>
    </div>
</template>

<script>
import datatable from '@vue-utils/datatable.vue';
import {constants, helpers} from '@/utils/hooks'

export default {
    name: 'occurrenceCombineThreats',
    props: {
        selectedThreats: {
            type: Array,
            required: true
        },
        combineThreatIds: {
            type: Array,
            required: true
        },
        mainOccurrenceId: {
            type: Number,
            required: true
        },
    },
    data:function () {
        let vm = this;
        return{
            checkedOriginalReports: [],
            panelBody: "threat-combine-select-"+vm._uid,
            threats_headers:["Occurrence", "Number", "Original Report", "Category", "Date Observed", "Threat Agent", "Current Impact", "Potential Impact", "Comments", "Action"],
            threats_options:{
                autowidth: true,
                language:{
                    processing: constants.DATATABLE_PROCESSING_HTML
                },
                paging: true,
                responsive: true,
                columnDefs: [
                    { responsivePriority: 1, targets: 0 },
                    { responsivePriority: 2, targets: -1 },
                ],
                data: vm.selectedThreats,
                order: [],
                buttons:[],
                searching: true,
                dom: "<'d-flex align-items-center'<'me-auto'l>fB>" +
                        "<'row'<'col-sm-12'tr>>" +
                        "<'d-flex align-items-center'<'me-auto'i>p>",
                columns: [
                    {
                        data: "occurrence__occurrence_number",
                    },
                    {
                        data: "threat_number",
                    },
                    {
                        data: "occurrence_report_threat__occurrence_report__occurrence_report_number",
                        mRender:function (data,type,full){
                            if (full.occurrence_report_threat__occurrence_report__occurrence_report_number) {
                                return full.occurrence_report_threat__occurrence_report__occurrence_report_number + ' - ' + full.occurrence_report_threat__threat_number;
                            }
                            return ""
                        }
                    },
                    {
                        data: "threat_category__name",
                    },
                    {
                        data: "date_observed",
                        mRender:function (data,type,full){
                            return data != '' && data != null ? moment(data).format('DD/MM/YYYY HH:mm'):'';
                        }
                    },
                    {
                        data: "threat_agent__name",
                    },
                    {
                        data: "current_impact__name",
                    },
                    {
                        data: "potential_impact__name",
                    },
                    {
                        data: "comment",
                        'render': function(value, type, full){
                            let result = helpers.dtPopover(value, 30, 'hover');
                            return type=='export' ? value : result;
                        },
                    },
                    {
                        data: "id",
                        mRender:function (data,type,full){
                            let original_threat = "";
                            if (full.occurrence_report_threat__threat_number != null) {
                                original_threat = `original-threat='${full.occurrence_report_threat__threat_number}'`
                            }
                            if (vm.combineThreatIds.includes(full.id)) {
                                if (full.occurrence__id == vm.mainOccurrenceId) {
                                    return `<input id='${full.id}' data-threat-checkbox='${full.id}' `+original_threat+` type='checkbox' checked disabled/>`
                                } else {
                                    return `<input id='${full.id}' data-threat-checkbox='${full.id}' `+original_threat+` type='checkbox' checked/>`
                                }
                            } else {
                                
                                if (vm.checkedOriginalReports.includes(full.occurrence_report_threat__threat_number)) {
                                    return `<input id='${full.id}' data-threat-checkbox='${full.id}' `+original_threat+` type='checkbox' disabled/>`
                                } else {
                                    return `<input id='${full.id}' data-threat-checkbox='${full.id}' `+original_threat+` type='checkbox'/>`
                                }
                            }
                        },
                    },
                ]
            },
            drawCallback: function () {
                setTimeout(function () {
                    vm.adjust_table_width();
                }, 100);
            },
            initComplete: function () {
                // another option to fix the responsive table overflow css on tab switch
                setTimeout(function () {
                    vm.adjust_table_width();
                }, 100);
            },
        }
    },
    components: {
        datatable,
    },
    methods: {
        getSelectedOriginalReports: function () {
            let vm=this;   
            let reports = []
            vm.selectedThreats.forEach(threat => {
                if (vm.combineThreatIds.includes(threat.id) && !reports.includes(threat.occurrence_report_threat__threat_number)) {
                    reports.push(threat.occurrence_report_threat__threat_number);
                }
            })
            vm.checkedOriginalReports = reports;
        },
        adjust_table_width: function () {
            if (this.$refs.threats_datatable !== undefined) { this.$refs.threats_datatable.vmDataTable.columns.adjust().responsive.recalc() };
            helpers.enablePopovers();
        },
        removeThreat: function(id) {
            let vm=this;   
            vm.combineThreatIds.splice(vm.combineThreatIds.indexOf(id), 1);
            vm.getSelectedOriginalReports();
        }, 
        addThreat: function(id) {
            let vm=this;   
            vm.combineThreatIds.push(id);
            vm.getSelectedOriginalReports();
        }, 
        addEventListeners:function (){
            let vm=this;     
            vm.$refs.threats_datatable.vmDataTable.on('change', 'input[data-threat-checkbox]', function(e) {
                e.preventDefault();
                var id = parseInt($(this).attr('data-threat-checkbox'));
                if($(this).prop('checked')) {
                    vm.addThreat(id);
                    vm.selectedThreats.forEach(threat=> {
                        let checkbox = vm.$refs.threats_datatable.vmDataTable.$("#"+threat.id);
                        if (id != checkbox.attr('data-threat-checkbox') && checkbox.attr('original-threat') !== undefined && checkbox.attr('original-threat') == $(this).attr('original-threat')) {
                            checkbox.prop('disabled', true);
                        }
                    });
                } else {
                    vm.removeThreat(id);
                    vm.selectedThreats.forEach(threat=> {
                        let checkbox = vm.$refs.threats_datatable.vmDataTable.$("#"+threat.id);
                        if (id != checkbox.attr('data-threat-checkbox') && checkbox.attr('original-threat') !== undefined && checkbox.attr('original-threat') == $(this).attr('original-threat')) {
                            checkbox.prop('disabled', false);
                        }
                    });
                }
            });
            vm.$refs.threats_datatable.vmDataTable.on('draw', function(e) {
                helpers.enablePopovers();
            });
            vm.$refs.threats_datatable.vmDataTable.on('childRow.dt', function (e, settings) {
                helpers.enablePopovers();
            });
        }
    },
    created: function(){
        let vm = this;    
        vm.getSelectedOriginalReports();
    },
    mounted: function() {
        let vm = this;    
        this.$nextTick(() => {
            vm.addEventListeners();
        });
    },
}

</script>