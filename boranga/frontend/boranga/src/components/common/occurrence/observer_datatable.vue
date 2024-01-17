<template lang="html">
    <div id="observerTable">
        <div class="row mb-3">
            <label for="" class="col-sm-3 control-label fw-bold">Observation Details:</label>
            <div class="col-sm-9 text-end">
                <button :disabled="isReadOnly" type="button" class="btn btn-primary mb-2 " @click.prevent="newObserverDetail">
                    <i class="fa-solid fa-circle-plus"></i>
                        Add Observer
                </button>
            </div>
        </div>
        <div class="row mb-3">
            <datatable ref="observer_detail_datatable" id="observerDetailTable" :dtOptions="observer_detail_options"
            :dtHeaders="observer_detail_headers"/>
        </div>
        <ObserverDetail ref="observer_detail" @refreshFromResponse="refreshFromResponse" :url="observer_detail_url"></ObserverDetail>
    </div>
</template>
<script>
import Vue from 'vue' ;
import datatable from '@vue-utils/datatable.vue';
import ObserverDetail from './add_observer_detail.vue'
import {
  api_endpoints,
  helpers
}
from '@/utils/hooks'
// require("select2/dist/css/select2.min.css");
// require("select2-bootstrap-5-theme/dist/select2-bootstrap-5-theme.min.css")

export default {
        name: 'ObserverTable',
        props:{
            occurrence_report_obj:{
                type: Object,
                required:true
            },
            is_external:{
              type: Boolean,
              default: false
            },
            isReadOnly:{
              type: Boolean,
              default: false
            },
        },
        data:function () {
            let vm = this;
            return{
                observer_detail_url: api_endpoints.observer_detail,
                observer_detail_headers:['Contact Name','Observer Role', 'Contact Detail', 'Organisation', 'Main Observer', 'Action'],
                observer_detail_options:{
                    autowidth: false,
                    language:{
                        processing: "<i class='fa fa-4x fa-spinner'></i>"
                    },
                    responsive: true,
                    searching: true,
                    //  to show the "workflow Status","Action" columns always in the last position
                    columnDefs: [
                        { responsivePriority: 1, targets: 0 },
                        { responsivePriority: 2, targets: -1 },
                    ],
                    ajax:{
                        "url": helpers.add_endpoint_json(api_endpoints.occurrence_report,vm.occurrence_report_obj.id+'/observer_details'),
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
                            data: "observer_name",
                            orderable: true,
                            searchable: true,
                            mRender: function(data,type,full){
                                return full.observer_name;
                            },

                        },
                        {
                            data: "role",
                            orderable: true,
                            searchable: true,
                            mRender: function(data,type,full){
                                return full.role;
                            },
                        },
                        {
                            data: "contact",
                            orderable: true,
                            searchable: true,
                            mRender: function(data,type,full){
                                return full.contact;
                            },
                        },
                        {
                            data: "organisation",
                            orderable: true,
                            searchable: true,
                            mRender: function(data,type,full){
                                return full.organisation;
                            },
                        },
                        {
                            data: "main_observer",
                            orderable: true,
                            searchable: true,
                            mRender: function(data,type,full){
                                return full.main_observer;
                            },
                        },
                        {
                            data: "id",
                            mRender:function (data,type,full){
                                let links = '';
                                links +=  `<a href='#${full.id}' data-view-observer_det='${full.id}'>View</a><br/>`;
                                links +=  `<a href='#${full.id}' data-edit-observer_det='${full.id}'>Edit</a><br/>`;
                                links += `<a href='#' data-delete-observer_det='${full.id}'>Delete</a><br>`;

                                return links;
                            }
                        },
                    ],
                    processing:true,
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
            ObserverDetail,
        },
        computed: {
        },
        watch:{
        },
        methods:{
            eventListeners:function (){
                let vm = this;
                vm.$refs.observer_detail_datatable.vmDataTable.on('click', 'a[data-edit-observer_det]', function(e) {
                    e.preventDefault();
                    var id = $(this).attr('data-edit-observer_det');
                    vm.editObserverDetail(id);
                });
                vm.$refs.observer_detail_datatable.vmDataTable.on('click', 'a[data-view-observer_det]', function(e) {
                    e.preventDefault();
                    var id = $(this).attr('data-view-observer_det');
                    vm.viewObserverDetail(id);
                });
                // External Discard listener
                vm.$refs.observer_detail_datatable.vmDataTable.on('click', 'a[data-delete-observer_det]', function(e) {
                    e.preventDefault();
                    var id = $(this).attr('data-delete-observer_det');
                    vm.deleteObserverDetail(id);
                });
            },
            refreshFromResponse: function(){
                let vm = this;
                vm.$refs.observer_detail_datatable.vmDataTable.ajax.reload();
            },
            adjust_table_width: function(){
                let vm = this;
                vm.$refs.observer_detail_datatable.vmDataTable.columns.adjust().responsive.recalc();
            },
            newObserverDetail: function(){
                let vm=this;
                this.$refs.observer_detail.observer_detail_id = '';
                //----for adding new observer
                var new_observer_detail={
                    occurrence_report: vm.occurrence_report_obj.id,
                    observer_name:  '',
                    role: '',
                    contact: '',
                    organisation: '',
                    main_observer: null,
                }
                this.$refs.observer_detail.observerObj=new_observer_detail;
                this.$refs.observer_detail.observer_detail_action='add';
                this.$refs.observer_detail.isModalOpen = true;
            },
            editObserverDetail: function(id){
                let vm=this;
                this.$refs.observer_detail.observer_detail_id = id;
                this.$refs.observer_detail.observer_detail_action='edit';
                Vue.http.get(helpers.add_endpoint_json(api_endpoints.observer_detail,id)).then((response) => {
                      this.$refs.observer_detail.observerObj=response.body; 
                    },
                  err => { 
                            console.log(err);
                      });
                this.$refs.observer_detail.isModalOpen = true;
            },
            viewObserverDetail: function(id){
                let vm=this;
                this.$refs.observer_detail.observer_detail_id = id;
                this.$refs.observer_detail.observer_detail_action='view';
                Vue.http.get(helpers.add_endpoint_json(api_endpoints.observer_detail,id)).then((response) => {
                      this.$refs.observer_detail.observerObj=response.body; 
                    },
                  err => { 
                            console.log(err);
                      });
                this.$refs.observer_detail.isModalOpen = true;
            },
            deleteObserverDetail: function(id){
                let vm=this;
                swal.fire({
                    title: "Discard Observer",
                    text: "Are you sure you want to discard this Observer?",
                    icon: "warning",
                    showCancelButton: true,
                    confirmButtonText: 'Discard Observer',
                    confirmButtonColor:'#d9534f'
                }).then((result) => {
                    if(result.isConfirmed){
                        vm.$http.delete(api_endpoints.discard_observer_detail(id))
                        .then((response) => {
                            swal.fire({
                                title: 'Discarded',
                                text: 'The Observer has been discarded',
                                icon: 'success',
                                confirmButtonColor:'#226fbb',
                            });
                            vm.$refs.observer_detail_datatable.vmDataTable.ajax.reload();
                        }, (error) => {
                            console.log(error);
                        });
                    }
                },(error) => {

                });
            },
            updatedObserverDetails(){
                this.$refs.observer_detail_datatable.vmDataTable.ajax.reload();
            },
        },
        created: async function() {
            let vm=this;
        },
        mounted: function(){
            let vm = this;
            this.$nextTick(()=>{
                vm.eventListeners();
            });
        },
    }
</script>

<style lang="css" scoped>
</style>

