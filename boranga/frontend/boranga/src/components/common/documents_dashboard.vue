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
import "babel-polyfill"
import datatable from '@/utils/vue/datatable.vue'
import FormSection from '@/components/forms/section_toggle.vue'
import Vue from 'vue'
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
        group_type_name:{
            type: String,
            required: true
        },
        url:{
            type: String,
            required: true
        },
        filterFloraScientificName_cache: {
            type: String,
            required: false,
            default: 'filterFloraScientificName',
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
        FormSection,
    },
    watch:{
    },
    computed: {
        datatable_headers: function() {
            if (this.is_external){
                return ['Number', 'Category', 'Document', 'Description', 'Date', 'Action']
            }
            if (this.is_internal){
                return ['Document', 'Description',]
            }
        },
        column_number: function() {
            return {
                data: "conservation_status",
                orderable: true,
                searchable: true,
                visible: true,
                'render': function(data, type, record){
                    if(false){
                        return full.conservation_status;
                    }
                    // Dummy data for now
                    return 'DBCA-0000001'
                },
                name: "conservation_status",
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
        // These are yet to be sourced
        // Name Reference
        // Genetic
        // Biology
        // Ecology
        // Fire
        // Disease









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
        column_common_name: function(){
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
        column_wa_conservation_status: function(){
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
        column_genera: function(){
            return {
                // 6. Genera
                data: "genera",
                orderable: true,
                searchable: true,
                visible: true,
                'render': function(data, type, full){
                    if(full.genera){
                        return full.genera;
                    }
                    // Should not reach here
                    return ''
                },
                name: "genera",
            }
        },
        column_region: function(){
            return {
                // 7. Region
                data: "region",
                orderable: true,
                searchable: false, // handles by filter_queryset override method - class ProposalFilterBackend
                visible: true,
                'render': function(data, type, full){
                    if (full.region){
                        return full.region
                    }
                    // Should not reach here
                    return ''
                },
                name: "region",
            }
        },
        column_district: function(){
            return {
                // 8. District
                data: "district",
                orderable: true,
                searchable: false, // handles by filter_queryset override method - class ProposalFilterBackend
                visible: true,
                'render': function(data, type, full){
                    if (full.district){
                        return full.district
                    }
                    // Should not reach here
                    return ''
                },
                name: "district",
            }
        },
        column_workflow_status: function(){
            return {
                // 9. Workflow Status
                data: "processing_status",
                orderable: true,
                searchable: true,
                visible: true,
                'render': function(data, type, full){
                    if (full.processing_status){
                        return full.processing_status;
                    }
                    // Should not reach here
                    return ''
                },
                name: "processing_status",
            }
        },
        column_action: function(){
            let vm = this
            return {
                // 10. Action
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
            if(vm.is_external){
                columns = [
                    vm.column_id,
                    vm.column_number,
                    vm.column_scientific_name,
                    vm.column_common_name,
                    vm.column_wa_conservation_status,
                    vm.column_genera,
                    vm.column_region,
                    vm.column_district,
                    vm.column_workflow_status,
                    vm.column_action,
                ]
                search = false
                buttons = []
            }
            if(vm.is_internal){
                columns = [
                    vm.column_id,
                    vm.column_number,
                    vm.column_scientific_name,
                    vm.column_common_name,
                    vm.column_wa_conservation_status,
                    vm.column_genera,
                    vm.column_region,
                    vm.column_district,
                    vm.column_workflow_status,
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
                //lengthMenu: [ [10, 25, 50, 100, -1], [10, 25, 50, 100, "All"] ],
                responsive: true,
                serverSide: true,
                searching: search,
                ajax: {
                    "url": this.url,
                    "dataSrc": 'data',

                    // adding extra GET params for Custom filtering
                    "data": function ( d ) {
                        d.filter_group_type = vm.group_type_name;
                        d.filter_scientific_name = vm.filterFloraScientificName;
                        d.filter_common_name = vm.filterCommonName;
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
        collapsible_component_mounted: function(){
            this.$refs.collapsible_filters.show_warning_icon(this.filterApplied)
        },

        fetchFilterLists: function(){
            let vm = this;

            vm.$http.get(api_endpoints.scientific_names_dict+ '?group_type_name=' + vm.group_type_name).then((response) => {
                vm.species_list= response.body;
                //vm.proposal_status = vm.level == 'internal' ? response.body.processing_status_choices: response.body.customer_status_choices;
                //vm.proposal_status = vm.level == 'internal' ? vm.internal_status: vm.external_status;
            },(error) => {
                console.log(error);
            })
        },

        discardProposal:function (proposal_id) {
            let vm = this;
            swal({
                title: "Discard Application",
                text: "Are you sure you want to discard this proposal?",
                type: "warning",
                showCancelButton: true,
                confirmButtonText: 'Discard Application',
                confirmButtonColor:'#d9534f'
            }).then(() => {
                vm.$http.delete(api_endpoints.discard_proposal(proposal_id))
                .then((response) => {
                    swal(
                        'Discarded',
                        'Your proposal has been discarded',
                        'success'
                    )
                    vm.$refs.flora_datatable.vmDataTable.ajax.reload();
                }, (error) => {
                    console.log(error);
                });
            },(error) => {

            });
        },
        addEventListeners: function(){
            let vm = this;
            // External Discard listener
            vm.$refs.flora_datatable.vmDataTable.on('click', 'a[data-discard-proposal]', function(e) {
                e.preventDefault();
                var id = $(this).attr('data-discard-proposal');
                vm.discardProposal(id);
            });
        },
        initialiseSearch:function(){
            this.submitterSearch();
        },
        submitterSearch:function(){
            let vm = this;
            vm.$refs.flora_datatable.table.dataTableExt.afnFiltering.push(
                function(settings,data,dataIndex,original){
                    let filtered_submitter = vm.filterProposalSubmitter;
                    if (filtered_submitter == 'All'){ return true; } 
                    return filtered_submitter == original.submitter.email;
                }
            );
        },
        fetchProfile: function(){
            let vm = this;
            /*Vue.http.get(api_endpoints.profile).then((response) => {
                vm.profile = response.body;
                vm.is_payment_admin=response.body.is_payment_admin;
                              
            },(error) => {
                console.log(error);
                
            })*/
        },

        check_assessor: function(proposal){
            let vm = this;
            if (proposal.assigned_officer)
                {
                    { if(proposal.assigned_officer== vm.profile.full_name)
                        return true;
                    else
                        return false;
                }
            }
            else{
                 var assessor = proposal.allowed_assessors.filter(function(elem){
                    return(elem.id=vm.profile.id)
                });
                
                if (assessor.length > 0)
                    return true;
                else
                    return false;
              
            }
            
        },
    },


    mounted: function(){
        this.fetchFilterLists();
        this.fetchProfile();
        let vm = this;
        $( 'a[data-toggle="collapse"]' ).on( 'click', function () {
            var chev = $( this ).children()[ 0 ];
            window.setTimeout( function () {
                $( chev ).toggleClass( "glyphicon-chevron-down glyphicon-chevron-up" );
            }, 100 );
        });
        this.$nextTick(() => {
            vm.initialiseSearch();
            vm.addEventListeners();
        });
    }
}
</script>
<style scoped>
.dt-buttons{
    float: right;
}
</style>
