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
import {
    api_endpoints,
} 
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
            if (this.is_external){
                return ['Document', 'Description',]
            }
            if (this.is_internal){
                return ['Number', 'Category', 'Document', 'Description', 'Date', 'Action']
                // These are yet to be sourced
                // Name Reference
                // Genetic
                // Biology
                // Ecology
                // Fire
                // Disease
            }
        },
        column_number: function() {
            return {
                data: "id",
                orderable: true,
                searchable: true,
                visible: true,
                'render': function(data, type, record){
                    if(false){
                        return record.id;
                    }
                    // Dummy data for now
                    return 'DBCA-0000001'
                },
                name: "id",
            }
        },
        column_category: function(){
            return {
                data: "conservation_status",
                orderable: true,
                searchable: true,
                visible: true,
                'render': function(data, type, record){
                    if(full.conservation_status){
                        return full.conservation_status;
                    }
                    // Should not reach here
                    return ''
                },
                name: "conservation_status",
            }
        },
        column_document: function(){
            return {
                data: "conservation_status",
                orderable: true,
                searchable: true,
                visible: true,
                'render': function(data, type, record){
                    if(full.conservation_status){
                        return full.conservation_status;
                    }
                    // Should not reach here
                    return ''
                },
                name: "conservation_status",
            }
        },
        column_description: function(){
            return {
                // 3. Scientific Name
                data: "scientific_name",
                orderable: true,
                searchable: true,
                visible: true,
                'render': function(value, type){
                        var ellipsis = '...',
                                truncated = _.truncate(value, {
                                    length: 25,
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
                name: "scientific_name",
            }
        },
        column_date: function(){
            return {
                // 4. Common Name
                data: "common_name",
                orderable: true,
                searchable: true,
                visible: true,
                'render': function(data, type, full){
                    if(full.common_name){
                        return full.common_name
                    }
                    // Should not reach here
                    return ''
                },
                name: "common_name",
            }
        },
        column_action: function(){
            return {
                // 5. Conservation Status
                data: "conservation_status",
                orderable: true,
                searchable: true,
                visible: true,
                'render': function(data, type, full){
                    if(full.conservation_status){
                        return full.conservation_status;
                    }
                    // Should not reach here
                    return ''
                },
                name: "conservation_status",
            }
        },
        datatable_options: function(){
            let vm = this

            let columns = []
            let search = null
            let buttons = []
            if(vm.is_external){
                columns = [
                    vm.column_document,
                    vm.column_description,
                ]
                search = false
                buttons = []
            }
            if(vm.is_internal){
                columns = [
                    vm.column_number,
                    vm.column_category,
                    vm.column_document,
                    vm.column_description,
                    vm.column_date,
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
            }

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

                    // adding extra GET params for Custom filtering
                    "data": function ( d ) {
                        d.is_internal = vm.is_internal;
                    }
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
