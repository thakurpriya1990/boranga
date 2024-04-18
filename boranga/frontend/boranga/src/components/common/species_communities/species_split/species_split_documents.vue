<template lang="html">
    <div id="species_split_documents">
        <FormSection :formCollapse="false" label="Documents" :Index="documentBody">
            <form class="form-horizontal" action="index.html" method="post">
                <div class="col-sm-12">
                    <input class="form-check-input" type="radio" :id="'doc_select_all'+species_community.id" name="documentSelect" value="selectAll" @click="selectDocumentOption($event)"/>
                    <label>Copy all documents to Species {{species_community.species_number}}</label>
                </div>
                <div class="col-sm-12">
                    <input class="form-check-input" type="radio" :id="'doc_select_individual'+species_community.id" name="documentSelect" value="individual" @click="selectDocumentOption($event)"/>
                    <label>Decide per document</label>
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
        name: 'SpeciesSplitDocuments',
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
                panelBody: "species-split-documents-"+vm._uid,
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
                //----set the selected value to the parent variable so as to get the data when tab is reloaded/refreshed
                vm.$parent.document_selection=selected_option;

                if(selected_option == "selectAll"){
                    //-- copy all original species documents to new species documents array
                    vm.species_community.documents=vm.original_species_documents;
                    this.$refs.documents_datatable.vmDataTable.ajax.reload();
                }
                else if(selected_option == "individual"){
                    //----empty the array to later select individual
                    vm.species_community.documents=[];
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
            },
            adjust_table_width: function(){
                this.$refs.documents_datatable.vmDataTable.columns.adjust().responsive.recalc();
            },
        },
        mounted: function(){
            let vm = this;
            this.$nextTick(() => {
                vm.addEventListeners();
                //vm.initialiseSearch();
                if(vm.$parent.document_selection!=null){

                    if(vm.$parent.document_selection==="selectAll"){
                        //alert(vm.$parent.document_selection)
                        document.getElementById('doc_select_all'+vm.species_community.id).checked=true;
                    }
                    else{
                        //alert(vm.$parent.document_selection)
                        document.getElementById('doc_select_individual'+vm.species_community.id).checked=true;
                        //$('#doc_select_individual').checked=true;
                    }
                }

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
