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
        }
    },
    data:function () {
        let vm = this;
        return{
            panelBody: "threat-combine-select-"+vm._uid,
            checkedThreatNames: [],
            threats_headers:["Number", "Original Report", "Category", "Date Observed", "Threat Agent", "Current Impact", "Potential Impact", "Comments", "Action"],
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
                        data: "threat_number",
                    },
                    {
                        data: "occurrence_report_threat__occurrence_report__occurrence_report_number",
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
                            if (vm.combineThreatIds.includes(full.id)) {
                                return `<input id='${full.id}' data-threat-checkbox='${full.id}' threat-name='${full.threat_name}' type='checkbox' checked/>`
                            } else {
                                return `<input id='${full.id}' data-threat-checkbox='${full.id}' threat-name='${full.threat_name}' type='checkbox'/>`
                            }
                        },
                    },
                ]
            },
            drawCallback: function () {
                helpers.enablePopovers();
                setTimeout(function () {
                    vm.adjust_table_width();
                }, 100);
            },
            initComplete: function () {
                helpers.enablePopovers();
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
        adjust_table_width: function () {
            if (this.$refs.threats_datatable !== undefined) { this.$refs.threats_datatable.vmDataTable.columns.adjust().responsive.recalc() };
        },
        removeThreat: function(id) {
            let vm=this;   
            vm.combineThreatIds.splice(vm.combineThreatIds.indexOf(id), 1);
        }, 
        addThreat: function(id) {
            let vm=this;   
            vm.combineThreatIds.push(id);
        }, 
        addEventListeners:function (){
            let vm=this;     
            vm.$refs.threats_datatable.vmDataTable.on('change', 'input[data-threat-checkbox]', function(e) {
                e.preventDefault();
                var id = parseInt($(this).attr('data-threat-checkbox'));
                if($(this).prop('checked')) {
                    vm.addThreat(id);
                } else {
                    vm.removeThreat(id);
                }
            });
        }
    },
    mounted: function() {
        let vm = this;    
        this.$nextTick(() => {
            vm.addEventListeners();
        });
    },
}

</script>