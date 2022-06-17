<template lang="html">
    <div id="species_threats">
        <FormSection :formCollapse="false" label="Threats" Index="threats">
            <form class="form-horizontal" action="index.html" method="post">
                <div class="col-sm-12">
                    <button @click.prevent="newThreat" style="margin-bottom:10px;" class="btn btn-primary pull-right">
                        Add Threat
                    </button>
                </div>
                <div>
                    <datatable ref="threats_datatable" :id="'threats-datatable-'+_uid" :dtOptions="threats_options"
                    :dtHeaders="threats_headers"/>
                </div>
            </form>
        </FormSection>
        <ThreatDetail ref="threat_detail" @refreshFromResponse="refreshFromResponse" :url="threat_url"></ThreatDetail>
    </div>
</template>
<script>
import Vue from 'vue' 
import datatable from '@vue-utils/datatable.vue';
import ThreatDetail from './add_threat.vue'
import FormSection from '@/components/forms/section_toggle.vue';
import {
  api_endpoints,
  helpers,
}
from '@/utils/hooks'


export default {
        name: 'SpeciesThreats',
        props:{
            species_community:{
                type: Object,
                required:true
            },
        },
        data:function () {
            let vm = this;
            return{
                uuid:0,
                panelBody: "species-threats-"+vm._uid,
                values:null,
                threat_url: api_endpoints.threat,
                threats_headers:['Number','Category', 'Threat Source', 'Date Observed','Action', 'Threat Agent', 'Comments',
                                'Current Impact?', 'Potential Impact?'],
                threats_options:{
                    autowidth: false,
                    language:{
                        processing: "<i class='fa fa-4x fa-spinner'></i>"
                    },
                    responsive: true,
                    ajax:{
                        "url": helpers.add_endpoint_json(api_endpoints.species,vm.species_community.id+'/threats'),
                        "dataSrc": ''
                    },
                    order: [],
                    dom: "<'d-flex align-items-center'<'me-auto'l>fB>" +
                     "<'row'<'col-sm-12'tr>>" +
                     "<'d-flex align-items-center'<'me-auto'i>p>",
                    buttons:[
                        {
                            extend: 'excel',
                            text: '<i class="fa-solid fa-download"></i> Excel',
                            className: 'btn btn-primary ml-2',
                            exportOptions: {
                                columns: ':visible',
                                orthogonal: 'export' 
                            }
                        },
                        {
                            extend: 'csv',
                            text: '<i class="fa-solid fa-download"></i> CSV',
                            className: 'btn btn-primary',
                            exportOptions: {
                                columns: ':visible',
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
                                return full.threat_number;
                            },

                        },
                        {
                            data: "threat_category_name",
                            orderable: true,
                            searchable: true,
                            mRender: function(data,type,full){
                                return full.threat_category_name;
                            },

                        },
                        {
                            data: "source",
                            orderable: true,
                            searchable: true,
                            mRender: function(data,type,full){
                                return full.source;
                            },

                        },
                        {
                            data: "date_observed",
                            mRender:function (data,type,full){
                                return data != '' && data != null ? moment(data).format('DD/MM/YYYY'):'';
                            }
                        },
                        {
                            data: "id",
                            mRender:function (data,type,full){
                                let links = '';
                                links +=  `<a href='#${full.id}' data-edit-threat='${full.id}'>Edit</a><br/>`;
                                links += `<a href='#' data-discard-threat='${full.id}'>Remove</a><br>`;
                                /*if(full.visible){
                                    links += `<a href='#' data-discard-document='${full.id}'>Remove</a><br>`;
                                }
                                else{
                                    links += `<a href='#' data-reinstate-document='${full.id}'>Reinstate</a><br>`;
                                }*/
                                return links;
                            }
                        },
                        {
                            data: "threat_agent",
                            orderable: true,
                            searchable: true,
                            mRender: function(data,type,full){
                                return full.threat_agent;
                            },

                        },
                        {
                            data: "comment",
                            orderable: true,
                            searchable: true,
                            'render': function(value, type, full){
                                let result = helpers.dtPopover(value, 30, 'hover');
                                return type=='export' ? value : result;
                            },
                        },
                        {
                            data: "current_impact_name",
                            orderable: true,
                            searchable: true,
                            mRender: function(data,type,full){
                                return full.current_impact_name;
                            },

                        },
                        {
                            data: "potential_impact_name",
                            orderable: true,
                            searchable: true,
                            mRender: function(data,type,full){
                                return full.potential_impact_name;
                            },
                        },
                    ],
                    processing:true,
                    initComplete: function() {
                        helpers.enablePopovers();
                    }, 
                }
            }
        },
        components: {
            FormSection,
            datatable,
            ThreatDetail,
        },
        computed: {
        },
        watch:{
            
        },
        methods:{
            newThreat: function(){
                let vm=this;
                this.$refs.threat_detail.threat_id = '';
                //----for adding new species Threat
                var new_species_threat_another={
                    species: vm.species_community.id,
                    source:  vm.species_community.id,
                    threat_category: '',
                    threat_agent: '',
                    comment: '',
                    current_impact: '',
                    potential_impact: '',
                    potential_threat_onset: '',
                    date_observed: null,
                }
                this.$refs.threat_detail.threatObj=new_species_threat_another;
                this.$refs.threat_detail.threat_action='add';
                this.$refs.threat_detail.isModalOpen = true;
            },
            editThreat: function(id){
                let vm=this;
                this.$refs.threat_detail.threat_id = id;
                this.$refs.threat_detail.threat_action='edit';
                Vue.http.get(helpers.add_endpoint_json(api_endpoints.threat,id)).then((response) => {
                      this.$refs.threat_detail.threatObj=response.body; 
                      this.$refs.threat_detail.threatObj.date_observed =  response.body.date_observed != null && response.body.date_observed != undefined ? moment(response.body.date_observed).format('yyyy-MM-DD'): '';
                    },
                  err => { 
                            console.log(err);
                      });
                this.$refs.threat_detail.isModalOpen = true;
            },
            /*discardThreat:function (id) {
                let vm = this;
                swal({
                    title: "Remove Threat",
                    text: "Are you sure you want to remove this Threat?",
                    type: "warning",
                    showCancelButton: true,
                    confirmButtonText: 'Remove Threat',
                    confirmButtonColor:'#d9534f'
                }).then(() => {
                    vm.$http.get(helpers.add_endpoint_json(api_endpoints.species_documents,id+'/discard'))
                    .then((response) => {
                        swal(
                            'Discarded',
                            'Your threat has been removed',
                            'success'
                        )
                        vm.$refs.threats_datatable.vmDataTable.ajax.reload();
                    }, (error) => {
                        console.log(error);
                    });
                },(error) => {

                });
            },
            /*reinstateDocument:function (id) {
                let vm = this;
                swal({
                    title: "Reinstate Document",
                    text: "Are you sure you want to Reinstate this Document?",
                    type: "question",
                    showCancelButton: true,
                    confirmButtonText: 'Reinstate Document',
                }).then(() => {
                    vm.$http.get(helpers.add_endpoint_json(api_endpoints.species_documents,id+'/reinstate'))
                    .then((response) => {
                        swal(
                            'Reinstated',
                            'Your document has been reinstated',
                            'success'
                        )
                        vm.$refs.documents_datatable.vmDataTable.ajax.reload();
                    }, (error) => {
                        console.log(error);
                    });
                },(error) => {

                });
            },*/
            updatedThreats(){
                this.$refs.threats_datatable.vmDataTable.ajax.reload();
            },
            addEventListeners:function (){
                let vm=this;
                vm.$refs.threats_datatable.vmDataTable.on('click', 'a[data-edit-threat]', function(e) {
                    e.preventDefault();
                    var id = $(this).attr('data-edit-threat');
                    vm.editThreat(id);
                });
                // External Discard listener
                vm.$refs.threats_datatable.vmDataTable.on('click', 'a[data-discard-threat]', function(e) {
                    e.preventDefault();
                    var id = $(this).attr('data-discard-threat');
                    vm.discardThreat(id);
                });
                // External Reinstate listener
                /*vm.$refs.threats_datatable.vmDataTable.on('click', 'a[data-reinstate-document]', function(e) {
                    e.preventDefault();
                    var id = $(this).attr('data-reinstate-threat');
                    vm.reinstateThreat(id);
                });*/
            },
            refreshFromResponse: function(){
                this.$refs.threats_datatable.vmDataTable.ajax.reload();
            },
        },
        mounted: function(){
            let vm = this;
            this.$nextTick(() => {
                vm.addEventListeners();
                //vm.initialiseSearch();
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

