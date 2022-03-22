<template id="species_documents_dashboard">
    <div>
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
import {
    api_endpoints,
    helpers
} from '@/utils/hooks'
export default {
    name: 'SpeciesDocumentsTable',
    props: {
        level:{
            type: String,
            required: true,
            validator:function(val) {
                let options = ['internal','referral','external'];
                return options.indexOf(val) != -1 ? true: false;
            }
        },
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
        is_external: function(){
            return this.level == 'external';
        },
        is_internal: function() {
            return this.level == 'internal'
        },
        is_referral: function(){
            return this.level == 'referral';
        },

        datatable_headers: function() {
            return ['Category', 'Document', 'Description', 'Date', 'Action', 'number', 'name_reference', 'genetic', 'biology', 'ecology', 'fire', 'disease']
        },
        column_document_category: function(){
            return {
                data: "document_category",
                orderable: true,
                searchable: true,
                visible: true,
                'render': function(data, type, species_document_obj){
                    if(species_document_obj.document_category){
                        return species_document_obj.document_category;
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
                'render': function(value, type){
                    var ellipsis = '...',
                        truncated = _.truncate(value, {
                            length: 30,
                            omission: ellipsis,
                            separator: ' '
                        }),
                        result = '<span>' + truncated + '</span>',
                        popTemplate = _.template('<a href="#" ' +
                            'role="button" ' +
                            'data-toggle="popover" ' +
                            'data-trigger="click" ' +
                            'data-placement="top auto"' +
                            'data-html="true" ' +
                            'data-content="<%= text %>" ' +
                            '>more</a>');
                    if (_.endsWith(truncated, ellipsis)) {
                        result += popTemplate({
                            text: value
                        });
                    }
                    //return result;
                    return type=='export' ? value : result;
                },
                'createdCell': helpers.dtPopoverCellFn,

                name: "document",
            }
        },
        column_document_description: function(){
            return {
                data: "document_description",
                orderable: true,
                searchable: true,
                visible: true,
                'render': function(value, type){
                    var ellipsis = '...',
                        truncated = _.truncate(value, {
                            length: 30,
                            omission: ellipsis,
                            separator: ' '
                        }),
                        result = '<span>' + truncated + '</span>',
                        popTemplate = _.template('<a href="#" ' +
                            'role="button" ' +
                            'data-toggle="popover" ' +
                            'data-trigger="click" ' +
                            'data-placement="top auto"' +
                            'data-html="true" ' +
                            'data-content="<%= text %>" ' +
                            '>more</a>');
                    if (_.endsWith(truncated, ellipsis)) {
                        result += popTemplate({
                            text: value
                        });
                    }
                    //return result;
                    return type=='export' ? value : result;
                },
                'createdCell': helpers.dtPopoverCellFn,
                name: "document_description",
            }
        },
        column_date_time: function(){
            return {
                data: "date_time",
                orderable: true,
                searchable: true,
                visible: true,
                'render': function(data, type, species_document_obj){
                    if(species_document_obj.date_time){
                        return species_document_obj.date_time
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
                data: "id",
                orderable: false,
                searchable: false,
                visible: true,
                'render': function(data, type, species_document_obj){
                    let links = "";
                    species_document_obj.assessor_process = true      // TODO: handle properly
                    species_document_obj.can_user_edit = true         // TODO: handle properly
                    species_document_obj.can_user_view = true         // TODO: handle properly
                    if (!vm.is_external){
                        if(species_document_obj.assessor_process){   
                                links +=  `<a href='/internal/species_communities/${species_document_obj.id}'>Process</a><br/>`;    
                        }
                        else{
                            links +=  `<a href='/internal/species_communities/${species_document_obj.id}'>View</a><br/>`;
                        }
                    }
                    else{
                        if (species_document_obj.can_user_edit) {
                            links +=  `<a href='/external/species_communities/${species_document_obj.id}'>Continue</a><br/>`;
                            links +=  `<a href='#${species_document_obj.id}' data-discard-proposal='${species_document_obj.id}'>Discard</a><br/>`;
                        }
                        else if (species_document_obj.can_user_view) {
                            links +=  `<a href='/external/species_communities/${species_document_obj.id}'>View</a>`;
                        }
                    }

                    links +=  `<a href='/internal/species_communities/${species_document_obj.id}'>Edit</a><br/>`; // Dummy addition for Boranaga demo

                    return links;
                }
            }
        },
        column_number: function(){
            return {
                data: "number",
                orderable: true,
                searchable: true,
                visible: true,
                'render': function(data, type, species_document_obj){
                    if(species_document_obj){
                        return species_document_obj.id
                    }
                    // Should not reach here
                    return 'XX'
                },
                name: "number",
            }
        },
        column_name_reference: function(){
            return {
                data: "name_reference",
                orderable: true,
                searchable: true,
                visible: true,
                'render': function(data, type, species_document_obj){
                    if(species_document_obj.name_reference){
                        return species_document_obj.name_reference
                    }
                    // Should not reach here
                    return "XX"
                },
                name: "name_reference",
            }
        },
        column_genetic: function(){
            return {
                data: "genetic",
                orderable: true,
                searchable: true,
                visible: true,
                'render': function(data, type, species_document_obj){

                    if(species_document_obj.genetic){
                        return species_document_obj.genetic
                    }
                    // Should not reach here
                    return 'XX'
                },
                name: "genetic",
            }
        },
        column_biology: function(){
            return {
                data: "biology",
                orderable: true,
                searchable: true,
                visible: true,
                'render': function(data, type, species_document_obj){

                    if(species_document_obj.biology){
                        return species_document_obj.biology
                    }
                    // Should not reach here
                    return 'XX'
                },
                name: "biology",
            }   
        },
        column_ecology: function(){
            return {
                data: "ecology",
                orderable: true,
                searchable: true,
                visible: true,
                'render': function(data, type, species_document_obj){

                    if(species_document_obj.ecology){
                        return species_document_obj.ecology
                    }
                    // Should not reach here
                    return 'XX'
                },
                name: "ecology",
            }  
        },
        column_fire: function(){
            return {
                data: "fire",
                orderable: true,
                searchable: true,
                visible: true,
                'render': function(data, type, species_document_obj){

                    if(species_document_obj.fire){
                        return species_document_obj.fire
                    }
                    // Should not reach here
                    return 'XX'
                },
                name: "fire",
            }  
        },
        column_disease: function(){
            return {
                data: "disease",
                orderable: true,
                searchable: true,
                visible: true,
                'render': function(data, type, species_document_obj){

                    if(species_document_obj.disease){
                        return species_document_obj.disease
                    }
                    // Should not reach here
                    return 'XX'
                },
                name: "disease",
            } 
        },
        datatable_options: function(){
            let vm = this

            let columns = []
            let search = null
            let buttons = []

            columns = [
                vm.column_document_category,
                vm.column_document,
                vm.column_document_description,
                vm.column_date_time,
                vm.column_action,
                vm.column_number,
                vm.column_name_reference,
                vm.column_genetic,
                vm.column_biology,
                vm.column_ecology,
                vm.column_fire,
                vm.column_disease,
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
