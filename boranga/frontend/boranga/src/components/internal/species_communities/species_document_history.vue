<template lang="html">
    <div id="speciesDocumentHistory">
        <modal
            transition="modal fade"
            :title="'Species '+ speciesId +' - Document ' + documentId + ' - History ' "
            :large="true"
            :full="true"
            :showOK="false"
            cancel-text="Close"
            @cancel="close()"
        >
            <div class="container-fluid">
                <div class="row">
                    <alert v-if="errorString" type="danger"
                        ><strong>{{ errorString }}</strong></alert>
                    <div class="col-sm-12">
                        <div class="form-group">
                            <div class="row">
                                <div v-if="documentId" class="col-lg-12">
                                    <datatable
                                        :id="datatable_id"
                                        ref="history_datatable"
                                        :dt-options="datatable_options"
                                        :dt-headers="datatable_headers"
                                    />
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </modal>
    </div>
</template>
<script>
import modal from '@vue-utils/bootstrap-modal.vue';
import alert from '@vue-utils/alert.vue';
import { helpers, api_endpoints, constants, utils } from '@/utils/hooks.js';
import datatable from '@/utils/vue/datatable.vue';
import { v4 as uuid } from 'uuid';

export default {
    name: 'SpeciesDocumentHistory',
    components: {
        modal,
        alert,
        datatable,
    },
    props: {
        documentId: {
            type: Number,
            required: true,
        },
        speciesId: {
            type: Number,
            required: true,
        },
    },
    data: function () {
        return {
            datatable_id: 'history-datatable-' + uuid(),
            documentDetails: {
            },
            isModalOpen: false,
            errorString: '',
            successString: '',
            success: false,
        };
    },
    computed: {
        csrf_token: function () {
            return helpers.getCookie('csrftoken');
        },
        datatable_headers: function () {
            return [
                'Revision Number',
                'Revision Date',
                'Category',
                'Sub Category',
                'Document',
                'Description',
                'Action',
            ];
        },
        column_data: function () {
            return {
                // 0. data
                data: 'data.data',
                orderable: false,
                searchable: false,
                visible: false,
                render: function (row, type, full) {
                    return full.data.data.speciesdocument;
                },
                name: 'data',
            };
        },
        column_id: function () {
            return {
                // 1. ID
                data: 'data.data.speciesdocument.pk',
                orderable: false,
                searchable: false,
                visible: false,
                render: function (row, type, full) {
                    return full.data.speciesdocument.pk;
                },
                name: 'id',
            };
        },
        column_number: function () {
            return {
                // 2. Number
                data: 'data.data.speciesdocument.fields.document_number',
                orderable: false,
                searchable: false, 
                visible: false,
                render: function (row, type, full) {
                    return full.data.speciesdocument.fields.document_number;
                },
                name: 'document_number',
            };
        },
        column_revision_id: function () {
            return {
                
                data: 'revision_id',
                orderable: true,
                searchable: true, 
                visible: true,
                render: function (row, type, full) {
                    return full.revision_id;
                },
                name: 'revision_id',
            };
        },
        column_revision_date: function () {
            return {
                
                data: 'date_created',
                orderable: true,
                searchable: true, 
                visible: true,
                render: function (row, type, full) {
                    return full.date_created;
                },
                name: 'revision_date',
            };
        },
        column_category: function () {
            return {
                //data: 'data.data.speciesdocument.fields.document_category', 
                data: 'data.data.documentcategory.fields.document_category_name', //TODO: disable this, for testing only
                defaultContent: '',
                orderable: false, //TODO: make orderable when done testing foreign fields
                searchable: true, 
                visible: true,
                render: function (row, type, full) {
                    //return full.data.speciesdocument.fields.document_category;
                    if (full.data.documentcategory !== undefined) {
                        return full.data.documentcategory.fields.document_category_name;
                    } else {
                        return ''
                    }
                },
                name: 'document_category_name',
            };
        },
        column_sub_category: function () {
            return {
                
                data: 'data.data.speciesdocument.fields.document_sub_category',
                defaultContent: '',
                orderable: true,
                searchable: false, 
                visible: true,
                render: function (row, type, full) {
                    return full.data.speciesdocument.fields.document_sub_category;
                },
                name: 'document_sub_category',
            };
        },
        column_file: function () {
            return {
                // 3. File
                data: 'data.data.speciesdocument.fields.name',
                defaultContent: '',
                orderable: false,
                searchable: true, 
                visible: true,
                mRender: function (row, type, full) {
                    let links='';
                    if(full.data.speciesdocument.fields.visible){
                        links+='<a href="/private-media/'+ full.data.speciesdocument.fields._file+'" target="_blank"><p>' + full.data.speciesdocument.fields.name + '</p></a>' ;
                    }else{
                        links+='<s>'+ full.data.speciesdocument.fields.name +'</s>';
                    }
                    return links;
                },
                name: 'name',
            };
        },
        column_description: function () {
            return {
                // 4. Description
                data: 'data.data.speciesdocument.fields.description',
                defaultContent: '',
                orderable: false,
                searchable: true, 
                visible: true,
                render: function (row, type, full) {
                    return full.data.speciesdocument.fields.description;
                },
                name: 'description',
            };
        },
        column_action: function () {
            return {
                data: 'revision_id',
                orderable: false,
                searchable: false,
                visible: true,
                'render': function(data, type, full){
                    let links = "";
                    return links;
                }
            };
        },
        datatable_options: function () {
            let vm = this;
            let columns = [
                vm.column_revision_id,
                vm.column_revision_date,
                vm.column_category,
                vm.column_sub_category,
                vm.column_file,
                vm.column_description,
                vm.column_action,
            ];
            let buttons = [
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
            ];
            return {
                autoWidth: false,
                language: {
                    processing: constants.DATATABLE_PROCESSING_HTML,
                },
                responsive: true,
                searching: true,
                ordering: true,
                order: [[0, 'desc']],
                serverSide: true,
                ajax: {
                    url: api_endpoints.lookup_history_species_document(this.documentId)+"?format=datatables",
                    dataSrc: 'data',
                },
                dom: 'lBfrtip',
                buttons,
                columns: columns,
                processing: true,
            };
        },
    },
    methods: {
        close: function () {
            this.errorString = '';
            this.isModalOpen = false;
            $('.has-error').removeClass('has-error');
        },
    },
};
</script>