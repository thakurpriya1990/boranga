<template id="species_documents_dashboard">
    <div>
        This is the dashboard
        <div class="row">
            <div class="col-lg-12">
                <datatable
                        ref="documents_datatable"
                        :id="datatable_id"
                        :dtOptions="datatable_options"
                        :dtHeaders="datatable_headers"
                />
            </div>
        </div>
    </div>
</template>
<script>
import Vue from 'vue'
import "babel-polyfill"
import datatable from '@/utils/vue/datatable.vue'
require("select2/dist/css/select2.min.css");
require("select2-bootstrap-theme/dist/select2-bootstrap.min.css");
import api_endpoints
from '@/utils/hooks'
export default {
    name: 'SpeciesDocumentsTable',
    props: {
        url:{
            type: String,
            required: true
        },
    },
    data() {
        let vm = this;
        return {
            datatable_id: 'documents-datatable-' + vm._uid,
        }
    },
    components:{
        datatable,
    },
    watch:{
    },
    computed: {
        datatable_headers: function() {
            return ['Number', 'Category', 'Document', 'Description', 'Date', 'Action']
                // These are yet to be sourced
                // Name Reference
                // Genetic
                // Biology
                // Ecology
                // Fire
                // Disease
        },
        column_number: function() {
            return {
                data: "id",
                orderable: true,
                searchable: true,
                visible: true,
                'render': function(data, type, record) {
                    if(record.id){
                        return record.id;
                    }
                    // Should not reach here
                    return 'XX'
                },
                name: "id",
            }
        },
        column_document_category: function(){
            return {
                data: "document_category",
                orderable: true,
                searchable: true,
                visible: true,
                'render': function(data, type, record){
                    if(full.document_category){
                        return full.document_category;
                    }
                    // Should not reach here
                    return 'XX'
                },
                name: "document_category",
            }
        },
        column_document: function(){
            return {
                data: "document",
                orderable: true,
                searchable: true,
                visible: true,
                'render': function(data, type, record){
                    if(full.document){
                        return full.document;
                    }
                    // Should not reach here
                    return 'XX'
                },
                name: "document",
            }
        },
        column_document_description: function(){
            return {
                data: "document_description",
                orderable: true,
                searchable: true,
                visible: true,
                'render': function(data, type, record){
                    if(full.document_description){
                        return full.document_description;
                    }
                    // Should not reach here
                    return 'XX'
                },
                name: "document_description",
            }
        },
        column_date_time: function(){
            return {
                data: "date_time",
                orderable: true,
                searchable: true,
                visible: true,
                'render': function(data, type, full){
                    if(full.date_time){
                        return full.date_time
                    }
                    // Should not reach here
                    return 'XX'
                },
                name: "date_time",
            }
        },
        column_action: function(){
            let vm = this
            return {
                // 9. Action
                data: "id",
                orderable: false,
                searchable: false,
                visible: true,
                'render': function(data, type, full){
                    let links = "";
                    if (!vm.is_external){
                        /*if(vm.check_assessor(full) && full.can_officer_process)*/
                        if(full.assessor_process){   
                                links +=  `<a href='/internal/species_communities/${full.id}'>Process</a><br/>`;    
                        }
                        else{
                            links +=  `<a href='/internal/species_communities/${full.id}'>View</a><br/>`;
                        }
                    }
                    else{
                        if (full.can_user_edit) {
                            links +=  `<a href='/external/species_communities/${full.id}'>Continue</a><br/>`;
                            links +=  `<a href='#${full.id}' data-discard-proposal='${full.id}'>Discard</a><br/>`;
                        }
                        else if (full.can_user_view) {
                            links +=  `<a href='/external/species_communities/${full.id}'>View</a>`;
                        }
                    }

                    links +=  `<a href='/internal/species_communities/${full.id}'>Edit</a><br/>`; // Dummy addition for Boranaga demo

                    return links;
                }
            }
        },
        datatable_options: function(){
            let vm = this

            let columns = []
            let search = null
            let buttons = []

            columns = [
                vm.column_number,
                vm.column_document_category,
                vm.column_document,
                vm.column_document_description,
                vm.column_date_time,
                vm.column_action,
            ]
            search = true
            buttons = [
                {
                    extend: 'excel',
                    exportOptions: {
                        columns: ':visible',
                    }
                },
                {
                    extend: 'csv',
                    exportOptions: {
                        columns: ':visible'
                    }
                },
            ]

            return {
                autoWidth: false,
                language: {
                    processing: "<i class='fa fa-4x fa-spinner fa-spin'></i>"
                },
                responsive: true,
                serverSide: true,
                searching: search,
                ajax: {
                    "url": this.url,
                    "dataSrc": 'data',
                },
                dom: 'lBfrtip',
                //buttons:[ ],
                buttons: buttons,
                columns: columns,
                processing: true,
                initComplete: function() {

                },
            }
        }
    },
    methods:{

    },

    mounted: function(){
        let vm = this;
        $( 'a[data-toggle="collapse"]' ).on( 'click', function () {
            var chev = $( this ).children()[ 0 ];
            window.setTimeout( function () {
                $( chev ).toggleClass( "glyphicon-chevron-down glyphicon-chevron-up" );
            }, 100 );
        });
        this.$nextTick(() => {

        });
    }
}
</script>
<style scoped>
    .dt-buttons{
        float: right;
    }
</style>
