<template lang="html">
    <div id="occurrenceCombineDocuments">
        <datatable ref="documents_datatable" :id="panelBody" :dtOptions="documents_options"
                    :dtHeaders="documents_headers"/>
    </div>
</template>

<script>
import datatable from '@vue-utils/datatable.vue';
import {constants, helpers} from '@/utils/hooks'

export default {
    name: 'occurrenceCombineDocuments',
    props: {
        selectedDocuments: {
            type: Array,
            required: true
        },
        combineDocumentIds: {
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
            panelBody: "document-combine-select-"+vm._uid,
            documents_headers:["Occurrence", "Number", "Category", "Sub Category", "Document", "Description", "Date/Time", "Action"],
            documents_options:{
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
                data: vm.selectedDocuments,
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
                        data: "document_number",
                    },
                    {
                        data: "document_category__document_category_name",
                    },
                    {
                        data: "document_sub_category__document_sub_category_name",
                    },
                    {
                        data: "name",
                        mRender: function(data,type,full){
                            let links='';
                            let value = full.name;
                            let result = helpers.dtPopoverSplit(value, 30, 'hover');
                            links+='<span><a href="/private-media/'+ full._file+'" target="_blank">' + result.text + '</a> ' + result.link + '</span>';
                            return links;
                        },
                    },
                    {
                        data: "description",
                        'render': function(value, type, full){
                            let result = helpers.dtPopover(value, 30, 'hover');
                            return type=='export' ? value : result;
                        },
                    },
                    {
                        data: "uploaded_date",
                        mRender:function (data,type,full){
                            return data != '' && data != null ? moment(data).format('DD/MM/YYYY HH:mm'):'';
                        }
                    },
                    {
                        data: "id",
                        mRender:function (data,type,full){
                            if (vm.combineDocumentIds.includes(full.id)) {
                                if (full.occurrence__id == vm.mainOccurrenceId) {
                                    return `<input id='${full.id}' data-document-checkbox='${full.id}' type='checkbox' checked disabled/>`
                                } else {
                                    return `<input id='${full.id}' data-document-checkbox='${full.id}' type='checkbox' checked/>`
                                }
                            } else {
                                return `<input id='${full.id}' data-document-checkbox='${full.id}' type='checkbox'/>`
                            }
                        }
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
            if (this.$refs.documents_datatable !== undefined) { this.$refs.documents_datatable.vmDataTable.columns.adjust().responsive.recalc() };
            helpers.enablePopovers();
        },
        removeDocument: function(id) {
            let vm=this;   
            vm.combineDocumentIds.splice(vm.combineDocumentIds.indexOf(id), 1);
        }, 
        addDocument: function(id) {
            let vm=this;   
            vm.combineDocumentIds.push(id);
        }, 
        addEventListeners:function (){
            let vm=this;     
            vm.$refs.documents_datatable.vmDataTable.on('change', 'input[data-document-checkbox]', function(e) {
                e.preventDefault();
                var id = parseInt($(this).attr('data-document-checkbox'));
                if($(this).prop('checked')) {
                    vm.addDocument(id);
                } else {
                    vm.removeDocument(id);
                }
            });
            vm.$refs.documents_datatable.vmDataTable.on('draw', function(e) {
                helpers.enablePopovers();
            });
            vm.$refs.documents_datatable.vmDataTable.on('childRow.dt', function (e, settings) {
                helpers.enablePopovers();
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