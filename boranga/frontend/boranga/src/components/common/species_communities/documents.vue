<template lang="html">
<div class="row" id="userInfo">
    <div class="col-sm-12">
        <div class="panel panel-default">
            <div class="panel-heading">
                <h3>{{proposal.species_id}}</h3>
                <h3 class="panel-title">Document History <small></small>
                    <a class="panelClicker" :href="'#'+lBody" data-toggle="collapse"  data-parent="#userInfo" expanded="true" :aria-controls="lBody">
                        <span class="glyphicon glyphicon-chevron-up pull-right"></span>
                    </a>
                    <h2 class="panel-title" style="color: red;">(Do not upload Managment or Recovery Plans here)</h2>
                </h3>
            </div>
            <div class="panel-body collapse in" :id="lBody">
                <div class="" >                        
                    <div clas="form-horizontal col-sm-12 borderDecoration">
                        
                        <div class="form-group">
                            <div class="row">
                                <div>
                                    <button type="button" class="btn btn-primary plus-button" @click="showModal">
                                        Add Document
                                    </button>
                                </div>
                                <div>
                                    <AddSpeciesDocument ref="modal" v-show="isModalVisible" @close="closeModal" :species="proposal"/>
                                </div>
                                <DocumentsDashboard level="internal" :url="species_documents_url" /><br>
                            </div>
                        </div> 
                    </div>
                </div>
            </div>                
        </div>
    </div>
</div>
</template>

<script>
import AddSpeciesDocument from '@common-utils/add_species_document_form.vue'
import DocumentsDashboard from '@common-utils/documents_dashboard.vue'
export default {
        props:{
            proposal:{
                type: Object,
                required:true
            }
        },
        data:function () {
            let vm = this;
            return {
                species_documents_url: "/docs_api/species_documents/species_documents_list?species_id=" + this.proposal.species_id,
                lBody: 'lBody' + vm._uid,
                isModalVisible: false,
                
            };
        },
        components: {
            DocumentsDashboard,
            AddSpeciesDocument,
        },
        computed: {

        },
        watch:{

        },
        methods:{
            showModal() {
                this.isModalVisible = true;
            },
            closeModal() {
                this.isModalVisible = false;
            },
        },
        created: function () {

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
    .plus-button {
        background-color: #337ab7;
        border: none;
        border-radius: 5px;
        color: white;
        text-align: center;
        text-decoration: none;
        display: inline-block;
        font-size: 16px;
        margin: 4px 2px;
        height: 35px;
        vertical-align: bottom;
    }
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
    .plus-button {
        margin-left: 10px;
        margin-bottom: 20px;;
    }
</style>

