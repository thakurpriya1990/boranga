<template lang="html">
    <div id="species_combine_documents">
        <FormSection :formCollapse="false" label="Documents" :Index="documentBody">
            <form class="form-horizontal" action="index.html" method="post">
                <div class="col-sm-12 form-check form-check-inline">
                    <input class="form-check-input" type="radio" :id="'doc_select_all'+species_original.id" name="documentSelect" value="selectAll" @click="selectDocumentOption($event)"/>
                    <label class="form-check-label">Copy all documents from Species {{species_original.species_number}}</label>
                </div>
                <div class="col-sm-12 form-check form-check-inline mb-3">
                    <input class="form-check-input" type="radio" :id="'doc_select_individual'+species_original.id" name="documentSelect" value="individual" @click="selectDocumentOption($event)"/>
                    <label class="form-check-label">Decide per document</label>
                </div>
                <div>
                    <datatable ref="documents_datatable" :id="panelBody" :dtOptions="documents_options"
                    :dtHeaders="documents_headers"/>
                </div>
            </form>
        </FormSection>
    </div>
</template>
<script>
import Vue from 'vue'
import datatable from '@vue-utils/datatable.vue';
import FormSection from '@/components/forms/section_toggle.vue';
import {
    constants,
    api_endpoints,
    helpers,
}
from '@/utils/hooks'


export default {
        name: 'SpeciesCombineDocuments',
        props:{
            species_community:{
                type: Object,
                required:true
            },
            species_original:{
                type: Object,
                required:true
            },
        },
        data:function () {
            let vm = this;
            return{
                uuid:0,
                documentBody: 'documentBody' + vm._uid,
                panelBody: "species-combine-documents-"+vm._uid,
                values:null,
                // to store all the documents of original on first load.
                original_species_documents:[],
                species_document_url: api_endpoints.species_documents,
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
                        "url": helpers.add_endpoint_json(api_endpoints.species,vm.species_original.id+'/documents'),
                        "dataSrc": ''
                    },
                    order: [],
                    dom: "<'d-flex align-items-center'<'me-auto'l>fB>" +
                         "<'row'<'col-sm-12'tr>>" +
                         "<'d-flex align-items-center'<'me-auto'i>p>",
                    buttons:[
                        {
                            extend: 'excel',
                            title: 'Boranga Species Combine Documents Excel Export',
                            text: '<i class="fa-solid fa-download"></i> Excel',
                            className: 'btn btn-primary me-2 rounded',
                            exportOptions: {
                                orthogonal: 'export'
                            }
                        },
                        {
                            extend: 'csv',
                            title: 'Boranga Species Combine Documents CSV Export',
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
                                if(full.active)
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
                                if(full.active){
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
                                if(full.active){
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
                                if(full.active){
                                    let value = full.name;
                                    let result = helpers.dtPopoverSplit(value, 30, 'hover');
                                    links+='<span><a href="'+ full._file+'" target="_blank">' + result.text + '</a> ' + result.link + '</span>';
                                }else{
                                    let value = full.name;
                                    let result = helpers.dtPopover(value, 30, 'hover');
                                    links += type == 'export' ? value : '<s>' + result + '</s>';
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
                                if(full.active){
                                    return type=='export' ? value : result;
                                }else{
                                    return type=='export' ? value : '<s>'+ result + '</s>';
                                }
                            },
                        },
                        {
                            data: "uploaded_date",
                            mRender:function (data,type,full){
                                if(full.active){
                                    return data != '' && data != null ? moment(data).format('DD/MM/YYYY HH:mm'):'';
                                }else{
                                    return data != '' && data != null ? '<s>'+ moment(data).format('DD/MM/YYYY HH:mm') + '</s>':'';
                                }
                            }
                        },
                        {
                            data: "id",
                            mRender:function (data,type,full){
                                // to store the original species documents for the use of radio btn options on first load so that no need to call api to get the documents ids
                                if(!vm.original_species_documents.includes(full.id)){
                                    vm.original_species_documents.push(full.id)
                                };

                                if(vm.species_community.documents.includes(full.id)){
                                    return `<input class='form-check-input' type="checkbox" id="document_chkbox-${vm.species_community.id}-${full.id}" data-add-document="${full.id}"  checked>`;
                                }
                                else{
                                    return `<input class='form-check-input' type="checkbox" id="document_chkbox-${vm.species_community.id}-${full.id}" data-add-document="${full.id}">`;
                                }
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
        },
        computed: {
        },
        methods:{
            selectDocumentOption(e){
                let vm=this;
                //--fetch the value of selected radio btn
                let selected_option=e.target.value;
                //----set the selected value to the original species object so as to get the data when tab is reloaded/refreshed
                vm.species_original.document_selection = selected_option;

                if(selected_option == "selectAll"){
                    //---first need to delete the original_species_documents from the new_arr if added from the "Decide individual" option to avoid duplication
                    vm.species_community.documents = vm.species_community.documents.filter(x => vm.original_species_documents.indexOf(x) == -1);  //--"filter" used to delete one array from another
                    //-- copy all original species documents to new species documents array
                    //---use '...' spread operator to add one arr elemnents to other
                    vm.species_community.documents.push(...vm.original_species_documents);
                    this.$refs.documents_datatable.vmDataTable.ajax.reload();
                }
                else if(selected_option == "individual"){
                    //----empty only the current original species array from the new species array as will contain other original combine species document_id's as well
                    vm.species_community.documents = vm.species_community.documents.filter(x => vm.original_species_documents.indexOf(x) == -1); //--"filter" used to delete one array from another
                    // vm.species_community.documents=[];
                    this.$refs.documents_datatable.vmDataTable.ajax.reload();
                }
            },
            addEventListeners:function (){
                let vm=this;
                vm.$refs.documents_datatable.vmDataTable.on('click', 'input[data-add-document]', function(e) {
                    //e.preventDefault();
                    let id = $(this).attr('data-add-document');
                    let chkbox = $(this).attr('id');
                    if($("#"+chkbox).is(':checked')== true){
                        if(!vm.species_community.documents.includes(id)){
                            vm.species_community.documents.push(parseInt(id));
                        }
                    }
                    else{
                        let doc_arr=vm.species_community.documents;
                        //---remove document id from array (for this arr.splice is used)
                        var index = doc_arr.indexOf(id);
                        vm.species_community.documents.splice(index,1);
                    }
                });
                vm.$refs.documents_datatable.vmDataTable.on('childRow.dt', function (e, settings) {
                    helpers.enablePopovers();
                });
            },
            adjust_table_width: function(){
                if (this.$refs.documents_datatable !== undefined) {this.$refs.documents_datatable.vmDataTable.columns.adjust().responsive.recalc();}
            },
        },
        mounted: function(){
            let vm = this;
            this.$nextTick(() => {
                if(vm.species_original.document_selection !== undefined && vm.species_original.document_selection !== null){

                    if(vm.species_original.document_selection === "selectAll"){
                        document.getElementById('doc_select_all'+vm.species_original.id).checked=true;
                    }
                    else{
                        document.getElementById('doc_select_individual'+vm.species_original.id).checked=true;
                    }
                }
                vm.addEventListeners();
            });
        },

    }
</script>

<style lang="css" scoped>
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
