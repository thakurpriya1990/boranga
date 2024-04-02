<template lang="html">
    <div id="speciesDocumentHistory">
        <modal
            transition="modal fade"
            :title="'Species Document History'"
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
                'id',
                'Number',
                'Category',
                'Sub Category',
                'Document',
                'Description',
                 //'Action',
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
                    return full.data.data[0];
                },
                name: 'data',
            };
        },
        column_id: function () {
            return {
                // 1. ID
                data: 'data.data[0].pk',
                orderable: false,
                searchable: false,
                visible: false,
                render: function (row, type, full) {
                    return full.data[0].pk;
                },
                name: 'id',
            };
        },
        column_number: function () {
            return {
                // 2. Number
                data: 'data.data[0].fields.document_number',
                orderable: true,
                searchable: false, 
                visible: true,
                render: function (row, type, full) {
                    return full.data[0].fields.document_number;
                },
                name: 'document_number',
            };
        },
        column_category: function () {
            return {
                
                data: 'data.data[0].fields.document_category',
                orderable: true,
                searchable: false, 
                visible: true,
                render: function (row, type, full) {
                    return full.data[0].fields.document_category;
                },
                name: 'document_category',
            };
        },
        column_sub_category: function () {
            return {
                
                data: 'data.data[0].fields.document_sub_category',
                orderable: true,
                searchable: false, 
                visible: true,
                render: function (row, type, full) {
                    return full.data[0].fields.document_sub_category;
                },
                name: 'document_sub_category',
            };
        },
        column_file: function () {
            return {
                // 3. File
                data: 'data.data[0].fields.name',
                orderable: false,
                searchable: true, 
                visible: true,
                mRender: function (row, type, full) {
                    let links='';
                    if(full.data[0].fields.visible){
                        links+='<a href="/private-media/'+ full.data[0].fields._file+'" target="_blank"><p>' + full.data[0].fields.name + '</p></a>' ;
                    }else{
                        links+='<s>'+ full.data[0].fields.name +'</s>';
                    }
                    return links;
                },
                name: 'name',
            };
        },
        column_description: function () {
            return {
                // 4. Description
                data: 'data.data[0].fields.description',
                orderable: false,
                searchable: true, 
                visible: true,
                render: function (row, type, full) {
                    return full.data[0].fields.description;
                },
                name: 'description',
            };
        },
        datatable_options: function () {
            let vm = this;
            let columns = [
                vm.column_id,
                vm.column_number,
                vm.column_category,
                vm.column_sub_category,
                vm.column_file,
                vm.column_description,
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
    created: function () {
        //this.fetchDocumentDetails();
    },
    methods: {
        close: function () {
            this.errorString = '';
            this.isModalOpen = false;
            $('.has-error').removeClass('has-error');
        },
        //fetchDocumentDetails: async function () {
        //    let vm = this;
        //    let url = api_endpoints.lookup_history_species_document(this.documentId)+"?format=datatables";
        //    utils
        //        .fetchUrl(url)
        //        .then((data) => {
        //            vm.documentDetails = Object.assign({}, data);
        //        })
        //        .catch((error) => {
        //            this.errorMessage = constants.ERRORS.API_ERROR;
        //            console.error(`Error fetching document details: ${error}`);
        //        });
        //},
    },
};
</script>