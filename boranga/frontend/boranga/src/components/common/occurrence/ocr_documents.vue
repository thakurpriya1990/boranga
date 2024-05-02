<template lang="html">
    <div id="ocr_documents">
        <FormSection :formCollapse="false" label="Documents" Index="documents">
            <small style="color: red;"><br>(Do not upload Management or Recovery Plans here)</small>
            <form class="form-horizontal" action="index.html" method="post">
                <div class="col-sm-12">
                    <div class="text-end" v-show="can_user_edit_doc">
                        <button type="button" class="btn btn-primary mb-2 " @click.prevent="newDocument">
                            <i class="fa-solid fa-circle-plus"></i>
                                Add Document
                        </button>
                    </div>
                </div>
                <div>
                    <datatable ref="documents_datatable" :id="panelBody" :dtOptions="documents_options"
                    :dtHeaders="documents_headers"/>
                </div>
            </form>
        </FormSection>
        <DocumentDetail ref="document_detail" @refreshFromResponse="refreshFromResponse" :url="ocr_document_url"></DocumentDetail>
        <div v-if="occurenceReportDocumentHistoryId">
            <OccurenceReportDocumentHistory
                ref="ocr_document_history"
                :key="occurenceReportDocumentHistoryId"
                :document-id="occurenceReportDocumentHistoryId"
                :occurrence-report-id="occurrence_report_obj.id"
            />
        </div>
    </div>
</template>
<script>
import Vue from 'vue'
import datatable from '@vue-utils/datatable.vue';
import DocumentDetail from '@/components/common/add_document.vue'
import FormSection from '@/components/forms/section_toggle.vue';
import OccurenceReportDocumentHistory from '../../internal/occurrence/ocr_document_history.vue';
import {
    constants,
    api_endpoints,
    helpers,
}
from '@/utils/hooks'


export default {
        name: 'OCRDocuments',
        props:{
            occurrence_report_obj:{
                type: Object,
                required:true
            },
            is_external:{
              type: Boolean,
              default: false
            },
            is_internal:{
              type: Boolean,
              default: false
            },
        },
        data:function () {
            let vm = this;
            return{
                uuid:0,
                occurenceReportDocumentHistoryId: null,
                panelBody: "ocr-documents-"+vm._uid,
                values:null,
                ocr_document_url: api_endpoints.occurrence_report_documents,
                documents_headers:['Number','Category', 'Sub Category','Document','Description','Date/Time','Action'],
                documents_options:{
                    autowidth: true,
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
                        "url": helpers.add_endpoint_json(api_endpoints.occurrence_report,vm.occurrence_report_obj.id+'/documents'),
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
                            data: "document_number",
                            orderable: true,
                            searchable: true,
                            mRender: function(data,type,full){
                                if(full.visible)
                                {
                                    return full.document_number;
                                }
                                else{
                                    return '<s>'+ full.document_number + '</s>'
                                }
                            },

                        },
                        {
                            data: "document_category_name",
                            orderable: true,
                            searchable: true,
                            mRender: function(data,type,full){
                                if(full.visible){
                                    return full.document_category_name;
                                }
                                else{
                                    return '<s>'+ full.document_category_name + '</s>'
                                }
                            },

                        },
                        {
                            data: "document_sub_category_name",
                            orderable: true,
                            searchable: true,
                            mRender: function(data,type,full){
                                if(full.visible){
                                    return full.document_sub_category_name;
                                }
                                else{
                                    return '<s>'+ full.document_sub_category_name + '</s>'
                                }
                            },

                        },
                        {
                            data: "name",
                            orderable: true,
                            searchable: true,
                            mRender: function(data,type,full){
                                let links='';
                                if(full.visible){
                                    links+='<a href="'+ full._file+'" target="_blank"><p>' + full.name + '</p></a>' ;
                                }else{
                                    links+='<s>'+ full.name +'</s>';
                                }
                                return links;
                            },

                        },
                        {
                            data: "description",
                            orderable: true,
                            searchable: true,
                            'render': function(value, type, full){
                                let result = helpers.dtPopover(value, 30, 'hover');
                                if(full.visible){
                                    return type=='export' ? value : result;
                                }else{
                                    return type=='export' ? value : '<s>'+ result + '</s>';
                                }
                            },
                        },
                        {
                            data: "uploaded_date",
                            mRender:function (data,type,full){
                                if(full.visible){
                                    return data != '' && data != null ? moment(data).format('DD/MM/YYYY HH:mm'):'';
                                }else{
                                    return data != '' && data != null ? '<s>'+ moment(data).format('DD/MM/YYYY HH:mm') + '</s>':'';
                                }
                            }
                        },
                        {
                            data: "id",
                            mRender:function (data,type,full){
                                let links = '';
                                // to restrict submitter to edit doc when the report is in workflow
                                if(vm.can_user_edit_doc){
                                    if(full.visible){
                                        links +=  `<a href='#${full.id}' data-edit-document='${full.id}'>Edit</a><br/>`;
                                        links += `<a href='#' data-discard-document='${full.id}'>Remove</a><br>`;
                                    }
                                    else{
                                        links += `<a href='#' data-reinstate-document='${full.id}'>Reinstate</a><br>`;
                                    }
                                    links += `<a href='#' data-history-document='${full.id}'>History</a><br>`;
                                }
                                else{
                                    if(full.visible){
                                        links +=  `<a href='#${full.id}'>Edit</a><br/>`;
                                        links += `<a href='#'>Remove</a><br>`;
                                    }
                                    else{
                                        links += `<a href='#'>Reinstate</a><br>`;
                                    }
                                    links += `<a href='#' data-history-document='${full.id}'>History</a><br>`;
                                }
                                return links;
                            }
                        },
                    ],
                    processing:true,
                    initComplete: function() {
                        helpers.enablePopovers();
                        // to fix the responsive table overflow css on tab switch
                        // vm.$refs.documents_datatable.vmDataTable.draw('page');
                        setTimeout(function (){
                            vm.adjust_table_width();
                        },100);
                    },
                }
            }
        },
        components: {
            FormSection,
            datatable,
            DocumentDetail,
            OccurenceReportDocumentHistory,
        },
        computed: {
            // to restrict submitter to add doc when the report is in workflow
            can_user_edit_doc: function(){
                return this.is_external && this.occurrence_report_obj.customer_status=="Draft";
            }
        },
        watch:{},
        methods:{
            newDocument: function(){
                let vm=this;
                this.$refs.document_detail.document_id = '';
                //this.$refs.edit_park.fetchPark(id);
                var new_document_another={
                    occurrence_report: vm.occurrence_report_obj.id,
                    input_name: 'occurrence_report_doc',
                    description: '',
                    document_category: '',
                    document_sub_category: '',
                    uploaded_date: null,
                }
                this.$refs.document_detail.documentObj=new_document_another;
                this.$refs.document_detail.uploaded_document=[];
                this.$refs.document_detail.document_action='add';
                this.$refs.document_detail.title='Add a new Document';
                this.$refs.document_detail.isModalOpen = true;
            },
            editDocument: function(id){
                let vm=this;
                this.$refs.document_detail.document_id = id;
                this.$refs.document_detail.document_action='edit';
                this.$refs.document_detail.title='Edit a Document';
                Vue.http.get(helpers.add_endpoint_json(api_endpoints.occurrence_report_documents,id)).then((response) => {
                      this.$refs.document_detail.documentObj=response.body;
                      this.$refs.document_detail.documentObj.uploaded_date =  response.body.uploaded_date != null && response.body.uploaded_date != undefined ? moment(response.body.uploaded_date).format('yyyy-MM-DDTHH:mm'): '';
                      this.$refs.document_detail.uploaded_document = [response.body];
                      //-----this method is called as it wasn't fetching subcategory
                      this.$refs.document_detail.fetchSubCategory(response.body.document_category);

                    },
                  err => {
                            console.log(err);
                      });
                //this.$refs.document_detail.fetchSpeciesDocument(id);
                this.$refs.document_detail.isModalOpen = true;
            },
            historyDocument: function(id){
                this.occurenceReportDocumentHistoryId = parseInt(id);
                this.uuid++;
                this.$nextTick(() => {
                    this.$refs.ocr_document_history.isModalOpen = true;
                });
            },
            discardDocument:function (id) {
                let vm = this;
                swal.fire({
                    title: "Remove Document",
                    text: "Are you sure you want to remove this Document?",
                    icon: "warning",
                    showCancelButton: true,
                    confirmButtonText: 'Remove Document',
                    confirmButtonColor:'#d9534f'
                }).then((result) => {
                    if(result.isConfirmed){
                        vm.$http.get(helpers.add_endpoint_json(api_endpoints.occurrence_report_documents,id+'/discard'))
                        .then((response) => {
                            swal.fire({
                                title: 'Discarded',
                                text: 'Your document has been removed',
                                icon: 'success',
                                confirmButtonColor:'#226fbb'
                            });
                            vm.$refs.documents_datatable.vmDataTable.ajax.reload();
                        }, (error) => {
                            console.log(error);
                        });
                    }
                },(error) => {

                });
            },
            reinstateDocument:function (id) {
                let vm = this;
                swal.fire({
                    title: "Reinstate Document",
                    text: "Are you sure you want to Reinstate this Document?",
                    icon: "question",
                    showCancelButton: true,
                    confirmButtonText: 'Reinstate Document',
                    confirmButtonColor:'#226fbb'
                }).then((result) => {
                    if(result.isConfirmed){
                        vm.$http.get(helpers.add_endpoint_json(api_endpoints.occurrence_report_documents,id+'/reinstate'))
                        .then((response) => {
                            swal.fire({
                                title: 'Reinstated',
                                text: 'Your document has been reinstated',
                                icon: 'success',
                                confirmButtonColor: '#226fbb'
                            });
                            vm.$refs.documents_datatable.vmDataTable.ajax.reload();
                        }, (error) => {
                            console.log(error);
                        });
                    }
                },(error) => {

                });
            },
            updatedDocuments(){
                this.$refs.documents_datatable.vmDataTable.ajax.reload();
            },
            addEventListeners:function (){
                let vm=this;
                vm.$refs.documents_datatable.vmDataTable.on('click', 'a[data-edit-document]', function(e) {
                    e.preventDefault();
                    var id = $(this).attr('data-edit-document');
                    vm.editDocument(id);
                });
                vm.$refs.documents_datatable.vmDataTable.on('click', 'a[data-history-document]', function(e) {
                    e.preventDefault();
                    var id = $(this).attr('data-history-document');
                    vm.historyDocument(id);
                });
                // External Discard listener
                vm.$refs.documents_datatable.vmDataTable.on('click', 'a[data-discard-document]', function(e) {
                    e.preventDefault();
                    var id = $(this).attr('data-discard-document');
                    vm.discardDocument(id);
                });
                // External Reinstate listener
                vm.$refs.documents_datatable.vmDataTable.on('click', 'a[data-reinstate-document]', function(e) {
                    e.preventDefault();
                    var id = $(this).attr('data-reinstate-document');
                    vm.reinstateDocument(id);
                });
            },
            refreshFromResponse: function(){
                this.$refs.documents_datatable.vmDataTable.ajax.reload();
            },
            adjust_table_width: function(){
                if (this.$refs.documents_datatable !== undefined) {this.$refs.documents_datatable.vmDataTable.columns.adjust().responsive.recalc()};
            },
        },
        mounted: function(){
            let vm = this;
            this.$nextTick(() => {
                vm.addEventListeners();
                //vm.initialiseSearch();
            });
        },

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
