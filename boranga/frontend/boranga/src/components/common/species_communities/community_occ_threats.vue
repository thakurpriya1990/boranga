<template lang="html">
    <div id="community_occ_threats">
        <div>
            <datatable ref="threats_datatable" :id="panelBody" :dtOptions="threats_options"
            :dtHeaders="threats_headers"/>
        </div>

        <ThreatDetail ref="threat_detail" @refreshFromResponse="refreshFromResponse" :url="occ_threat_url"></ThreatDetail>
        <div v-if="occConservationThreatHistoryId">
            <ConservationThreatHistory
                ref="occ_conservation_threat_history"
                :key="occConservationThreatHistoryId"
                :threat-id="occConservationThreatHistoryId"
            />
        </div>
    </div>
</template>
<script>
import Vue from 'vue'
import datatable from '@vue-utils/datatable.vue';
import ThreatDetail from '@/components/common/species_communities/add_threat.vue'
import ConservationThreatHistory from '../../internal/occurrence/occ_conservation_threat_history.vue';
import {
    constants,
    api_endpoints,
    helpers,
}
from '@/utils/hooks'


export default {
        name: 'OCCThreats',
        props:{
            community_obj:{
                type: Object,
                required:true
            },
        },
        data:function () {
            let vm = this;
            return{
                uuid:0,
                occConservationThreatHistoryId: null,
                showExisting: false,
                threatBody: "threatBody"+ vm._uid,
                panelBody: "community-threats-"+ vm._uid,
                values:null,
                occ_threat_url: api_endpoints.occ_threat,
                threats_headers:['Number', 'Original Report','Category', 'Date Observed', 'Threat Agent', 'Comments',
                                'Current Impact', 'Potential Impact', 'Threat Source','Action'],
                threats_options:{
                    autowidth: false,
                    language:{
                        processing: constants.DATATABLE_PROCESSING_HTML
                    },
                    responsive: true,
                    searching: true,
                    //  to show the "workflow Status","Action" columns always in the last position
                    columnDefs: [
                        { responsivePriority: 1, targets: 0 },
                        { responsivePriority: 2, targets: -1 },
                    ],
                    ajax:{
                        "url": helpers.add_endpoint_json(api_endpoints.community,vm.community_obj.id+'/occurrence_threats'),
                        "dataSrc": ''
                    },
                    oorder: [[0, 'desc']],
                    dom: "<'d-flex align-items-center'<'me-auto'l>fB>" +
                     "<'row'<'col-sm-12'tr>>" +
                     "<'d-flex align-items-center'<'me-auto'i>p>",
                    buttons:[
                        {
                            extend: 'excel',
                            text: '<i class="fa-solid fa-download"></i> Excel',
                            className: 'btn btn-primary me-2 rounded',
                            exportOptions: {
                                orthogonal: 'export'
                            }
                        },
                        {
                            extend: 'csv',
                            text: '<i class="fa-solid fa-download"></i> CSV',
                            className: 'btn btn-primary rounded',
                            exportOptions: {
                                orthogonal: 'export'
                            }
                        },
                    ],
                    columns: [
                        {
                            data: "threat_number",
                            orderable: true,
                            searchable: true,
                            mRender: function(data,type,full){
                                if(full.visible){
                                    return "OCC" + full.occurrence + " - " + full.threat_number;
                                }
                                else{
                                    return '<s>'+ "OCC" + full.occurrence + " - " + full.threat_number + '</s>'
                                }
                            },

                        },
                        {
                            data: "original_report",
                            orderable: true,
                            searchable: true,
                            mRender: function(data,type,full){
                                if(full.visible && full.original_report != null){
                                    return full.original_report + " - " + full.original_threat;
                                }
                                else{
                                    return ""
                                }
                            },

                        },
                        {
                            data: "threat_category",
                            orderable: true,
                            searchable: true,
                            mRender: function(data,type,full){
                                if(full.visible){
                                    return full.threat_category;
                                }
                                else{
                                    return '<s>'+ full.threat_category + '</s>'
                                }
                            },

                        },
                        {
                            data: "date_observed",
                            mRender:function (data,type,full){
                                if(full.visible){
                                    return data != '' && data != null ? moment(data).format('DD/MM/YYYY'):'';
                                }
                                else{
                                    return data != '' && data != null ? '<s>'+ moment(data).format('DD/MM/YYYY'):'' + '</s>'
                                }
                            }
                        },
                        {
                            data: "threat_agent",
                            orderable: true,
                            searchable: true,
                            mRender: function(data,type,full){
                                if(full.visible){
                                    return full.threat_agent;
                                }
                                else{
                                    return '<s>'+ full.threat_agent + '</s>'
                                }
                            },

                        },
                        {
                            data: "comment",
                            orderable: true,
                            searchable: true,
                            'render': function(value, type, full){
                                let result = helpers.dtPopover(value, 30, 'hover');
                                if(full.visible){
                                    return type=='export' ? value : result;
                                }
                                else{
                                    return type=='export' ? '<s>' + value + '</s>' : '<s>' + result + '</s>';
                                }
                            },
                        },
                        {
                            data: "current_impact_name",
                            orderable: true,
                            searchable: true,
                            mRender: function(data,type,full){
                                if(full.visible){
                                    return full.current_impact_name;
                                }
                                else{
                                    return '<s>'+ full.current_impact_name + '</s>'
                                }
                            },

                        },
                        {
                            data: "potential_impact_name",
                            orderable: true,
                            searchable: true,
                            mRender: function(data,type,full){
                                if(full.visible){
                                    return full.potential_impact_name;
                                }
                                else{
                                    return '<s>'+ full.potential_impact_name + '</s>'
                                }
                            },
                        },
                        {
                            data: "source",
                            orderable: true,
                            searchable: true,
                            mRender: function(data,type,full){
                                if(full.visible){
                                    return full.source;
                                }
                                else{
                                    return '<s>'+ full.source + '</s>'
                                }
                            },

                        },
                        {
                            data: "id",
                            mRender:function (data,type,full){
                                let links = '';
                                if(full.visible){
                                    links +=  `<a href='#${full.id}' data-view-threat='${full.id}'>View</a><br/>`;
                                    links += `<a href='#' data-history-threat='${full.id}'>History</a><br>`;
                                }
                                else{
                                    links += `<a href='#' data-history-threat='${full.id}'>History</a><br>`;
                                }
                                return links;
                            }
                        },
                    ],
                    processing:true,
                    drawCallback: function() {
                    helpers.enablePopovers();
                },
                initComplete: function() {
                        helpers.enablePopovers();
                        // another option to fix the responsive table overflow css on tab switch
                        // vm.$refs.threats_datatable.vmDataTable.draw('page');
                        setTimeout(function (){
                            vm.adjust_table_width();
                        },100);
                    },
                }
            }
        },
        components: {
            datatable,
            ThreatDetail,
            ConservationThreatHistory,
        },
        methods:{
            viewThreat: function(id){
                let vm=this;
                this.$refs.threat_detail.threat_id = id;
                this.$refs.threat_detail.threat_action='view';
                Vue.http.get(helpers.add_endpoint_json(api_endpoints.occ_threat,id)).then((response) => {
                      this.$refs.threat_detail.threatObj=response.body;
                      this.$refs.threat_detail.threatObj.date_observed =  response.body.date_observed != null && response.body.date_observed != undefined ? moment(response.body.date_observed).format('yyyy-MM-DD'): '';
                    },
                  err => {
                            console.log(err);
                      });
                this.$refs.threat_detail.isModalOpen = true;
            },
            historyThreat: function(id){
                this.occConservationThreatHistoryId = parseInt(id);
                this.uuid++;
                this.$nextTick(() => {
                    this.$refs.occ_conservation_threat_history.isModalOpen = true;
                });
            },
            updatedThreats(){
                this.$refs.threats_datatable.vmDataTable.ajax.reload();
            },
            addEventListeners:function (){
                let vm=this;
                vm.$refs.threats_datatable.vmDataTable.on('click', 'a[data-view-threat]', function(e) {
                    e.preventDefault();
                    var id = $(this).attr('data-view-threat');
                    vm.viewThreat(id);
                });
                vm.$refs.threats_datatable.vmDataTable.on('click', 'a[data-history-threat]', function(e) {
                    e.preventDefault();
                    var id = $(this).attr('data-history-threat');
                    vm.historyThreat(id);
                });
                vm.$refs.threats_datatable.vmDataTable.on('childRow.dt', function (e, settings) {
                    helpers.enablePopovers();
                });
            },
            refreshFromResponse: function(){
                this.$refs.threats_datatable.vmDataTable.ajax.reload();
            },
            adjust_table_width: function(){
                if (this.$refs.threats_datatable !== undefined) {this.$refs.threats_datatable.vmDataTable.columns.adjust().responsive.recalc();}
            },
        },
        mounted: function(){
            let vm = this;
            this.$nextTick(() => {
                vm.addEventListeners();
        });
        }
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
</style>
