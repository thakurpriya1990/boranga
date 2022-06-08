<template lang="html">
    <div id="species_documents">
        <FormSection :formCollapse="false" label="Documents" Index="documents">
            <small style="color: red;"><br>(Do not upload Management or Recovery Plans here)</small>
            <form class="form-horizontal" action="index.html" method="post">
                <div class="col-sm-12">
                    <button @click.prevent="addDocument()" style="margin-bottom:10px;float: right+;" class="btn btn-primary pull-right">
                        Add Document
                    </button>
                </div>

                <!-- <datatable ref="documents_datatable" :id="'documents-datatable-'+_uid" :dtOptions="documents_options"
                :dtHeaders="documents_headers"/> -->
            </form>

        </FormSection>
    </div>
</template>
<script>
import Vue from 'vue' 
import datatable from '@vue-utils/datatable.vue';
import FormSection from '@/components/forms/section_toggle.vue';
import {
  api_endpoints,
  helpers
}
from '@/utils/hooks'


export default {
        name: 'InternalSpeciesDocuments',
        props:{
            species_community:{
                type: Object,
                required:true
            },
        },
        data:function () {
            let vm = this;
            return{
                uuid:0,
                panelBody: "species-documents-"+vm._uid,
                values:null,
                datepickerOptions:{
                        format: 'DD/MM/YYYY',
                        showClear:true,
                        useCurrent:false,
                        keepInvalid:true,
                        allowInputToggle:true,
                },
                documents:[],
                documents_headers:[],
                documents_options:{
                    autowidth: false,
                    language:{
                        processing: "<i class='fa fa-4x fa-spinner'></i>"
                    },
                    responsive: true,
                    ajax:{
                        "url": helpers.add_endpoint_json(api_endpoints.species,vm.species_community.id+'/documents'),
                        "dataSrc": ''
                    },
                    order: [],
                    dom: 'lBfrtip',
                    buttons:[
                    'excel','csv', ],
                    columns: [
                        {

                        }
                    ],
                    processing:true,
                    initComplete: function() {

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
        watch:{
            
        },
        methods:{
            eventListeners:function (){
                let vm=this;
            },
        },
        mounted: function(){
            let vm = this;
        }
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

