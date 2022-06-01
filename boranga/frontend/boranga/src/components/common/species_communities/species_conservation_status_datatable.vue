<template id="species_community_conservation_status">
    <div>
            <datatable 
            ref="conservation_status_datatable" 
            :id="datatable_id" 
            :dtOptions="conservation_status_options" 
            :dtHeaders="conservation_status_headers"/>
    </div>
</template>
<script>
import {
    api_endpoints,
    helpers
}
from '@/utils/hooks'
import "babel-polyfill"
import datatable from '@/utils/vue/datatable.vue'

export default {
    name: 'SpeciesConservationStatusDatatable',
    props: {
        species_community:{
                type: Object,
                required:true
            },
    },
    data: function() {
        let vm = this;
        return {

            datatable_id: 'species_community-conservation-status-datatable-'+vm._uid,
            conservation_status_headers:[
                    "Conservation List",
                    "Conservation Category",
                    "Conservation Criteria",
                    "Action",
                    "Effective Status Date",
            ],
            conservation_status_options:{
                columns: [
                    {
                        data: "conservation_list",
                        mRender: function(data, type, row){
                            if (data.conservation_list){
                                return data.conservation_list;
                            }
                            // Should not reach here
                            return '';
                        },
                    },
                    {
                        data: "conservation_category",
                        mRender: function(data, type, row){
                            if (data.conservation_category){
                                return data.conservation_category;
                            }
                            // Should not reach here
                            return '';
                        },
                    },
                    {
                        data: "conservation_criteria",
                        mRender: function(data, type, row){
                            if (data.conservation_criteria){
                                return data.conservation_criteria;
                            }
                            // Should not reach here
                            return '';
                        },
                    },
                    {
                        data: "conservation_list_id",
                        mRender:function (data,type,row) {
                            let links = '';
                            if (data.conservation_list_id){
                                //links +=  `<a href='/internal/species_communities/${full.id}'>View</a><br/>`;
                                links +=  `<a>View</a><br/>`;
                            }
                            return links;
                        },
                    },
                    {
                        data: "effective_status_date",
                        mRender: function(data, type, row){
                            if (data.effective_status_date){
                                return data.effective_status_date;
                            }
                            // Should not reach here
                            return '';
                        },
                    },
                ],
                processing: true,
            }
        }
    },
    components:{
        datatable,
    },
    computed:{
    },
    methods:{
        constructConservationStatusTable: function(){
            this.$refs.conservation_status_datatable.vmDataTable.clear().draw();
            if(this.species_community.conservation_status){
                for(let i=0; i<this.species_community.conservation_status.length; i++){
                    this.addConservationStatusToTable(this.species_community.conservation_status[i]);
                }
            }
        },
        addConservationStatusToTable: function(conservationStatus){
            this.$refs.conservation_status_datatable.vmDataTable.row.add({
                conservation_list: conservationStatus,
                conservation_category: conservationStatus,
                conservation_criteria: conservationStatus,
                conservation_list_id: conservationStatus,
                effective_status_date: conservationStatus,
            }).draw();
        }
    },
    created: function() {
        this.$nextTick(() => {
            if(this.species_community.conservation_status){
                this.constructConservationStatusTable();
            }
        });
    },
}
</script>
<style scoped>
.dt-buttons{
    float: right;
}
.collapse-icon {
    cursor: pointer;
}
.collapse-icon::before {
    top: 5px;
    left: 4px;
    height: 14px;
    width: 14px;
    border-radius: 14px;
    line-height: 14px;
    border: 2px solid white;
    line-height: 14px;
    content: '-';
    color: white;
    background-color: #d33333;
    display: inline-block;
    box-shadow: 0px 0px 3px #444;
    box-sizing: content-box;
    text-align: center;
    text-indent: 0 !important;
    font-family: 'Courier New', Courier monospace;
    margin: 5px;
}
.expand-icon {
    cursor: pointer;
}
.expand-icon::before {
    top: 5px;
    left: 4px;
    height: 14px;
    width: 14px;
    border-radius: 14px;
    line-height: 14px;
    border: 2px solid white;
    line-height: 14px;
    content: '+';
    color: white;
    background-color: #337ab7;
    display: inline-block;
    box-shadow: 0px 0px 3px #444;
    box-sizing: content-box;
    text-align: center;
    text-indent: 0 !important;
    font-family: 'Courier New', Courier monospace;
    margin: 5px;
}

</style>
