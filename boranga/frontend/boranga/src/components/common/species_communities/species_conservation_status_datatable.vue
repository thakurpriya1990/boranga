<template id="species_conservation_status">
    <div class="row">
        <div class="col-lg-12">
            <datatable ref="species_conservation_status_datatable" :id="'species-conservation-status-datatable-'+_uid" 
            :dtOptions="conservation_status_options" :dtHeaders="conservation_status_headers"/>
        </div>
    </div>
</template>
<script>
import {
    api_endpoints,
    helpers
}
from '@/utils/hooks'
import datatable from '@vue-utils/datatable.vue'

export default {
    name: 'SpeciesConservationStatusDatatable',
    props: {
        species:{
                type: Object,
                required:true
            },
    },
    data: function() {
        let vm = this;
        return {
            conservation_status_headers:["Conservation List","Conservation Category","Conservation Criteria","Criteria Version",
                                            "Effective Status Date","Action"],
            conservation_status_options:{
                autoWidth: false,
                language: {
                    processing: "<i class='fa fa-4x fa-spinner fa-spin'></i>"
                },
                responsive: true,
                ajax: {
                    "url": helpers.add_endpoint_json(api_endpoints.species, vm.species.id+'/get_conservation_status'),
                    "dataSrc": ''
                },
                order: [],
                dom: 'lBfrtip',
                buttons:[
                'excel', 'csv', ], //'copy'
                columns: [
                    {
                        data: "conservation_list",
                        'render': function(data, type, full){
                            if (full.conservation_list){
                                alert(full.conservation_list)
                                return full.conservation_list;
                            }
                            // Should not reach here
                            return ''
                        },
                    },
                    {
                        data: "conservation_category",
                        'render': function(data, type, full){
                            if (full.conservation_category){
                                return full.conservation_category;
                            }
                            // Should not reach here
                            return ''
                        },
                    },
                    {
                        data: "conservation_criteria",
                        'render': function(data, type, full){
                            if (full.conservation_criteria){
                                return full.conservation_criteria;
                            }
                            // Should not reach here
                            return ''
                        },
                    },
                    {
                        data: "conservation_criteria",
                        'render': function(data, type, full){
                            // Should not reach here
                            return ''
                        },
                    },
                    {
                        data: "conservation_criteria",
                        'render': function(data, type, full){
                            // Should not reach here
                            return ''
                        },
                    },
                    {
                        data: "conservation_list_id",
                        mRender:function (data,type,full) {
                            let links = '';
                            if (full.conservation_list_id){
                                //links +=  `<a href='/internal/species_communities/${full.id}'>View</a><br/>`;
                                links +=  `<a>View</a><br/>`;
                            }
                            return links;
                        },
                    },
                ],
                processing: true,
            }
        }
    },
    watch:{
    },
    components:{
        datatable,
    },
    computed:{
    },
    methods:{
        },
}
</script>
<style scoped>
.dataTables_wrapper .dt-buttons{
    float: right;
}
</style>
