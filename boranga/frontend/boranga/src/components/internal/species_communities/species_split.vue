<template lang="html">
    <div id="splitSpecies">
        <modal transition="modal fade" @ok="ok()" @cancel="cancel()" :title="title" large id="myModal">
            <div class="container-fluid">
                <div class="row">
                    <form class="form-horizontal" name="splitSpeciesForm">
                        <alert :show.sync="showError" type="danger"><strong>{{errorString}}</strong></alert>
                        <div>
                            <div class="col-md-12">

                                <ul v-if="is_internal" class="nav nav-pills mb-3" id="split_pills-tab" role="tablist">
                                    <li class="nav-item">
                                        <a 
                                            class="nav-link" 
                                            id="pills-original-tab" 
                                            data-bs-toggle="pill" 
                                            :href="'#' + originalBody" 
                                            role="tab" 
                                            :aria-controls="originalBody" 
                                            aria-selected="true">
                                            <!-- @click="tabClicked()"> -->
                                        Original
                                        </a>
                                    </li>
                                    <li class="nav-item">
                                        <a 
                                            class="nav-link" 
                                            id="pills-species1-tab" 
                                            data-bs-toggle="pill" 
                                            :href="'#' + species1Body" 
                                            role="tab" 
                                            :aria-controls="species1Body" 
                                            aria-selected="false">
                                            <!-- @click="tabClicked()"> -->
                                        Species 1
                                        </a><span>x</span>
                                    </li>
                                    <li class="nav-item">
                                        <a 
                                            class="nav-link" 
                                            id="pills-species2-tab" 
                                            data-bs-toggle="pill" 
                                            :href="'#' + species2Body" 
                                            role="tab" 
                                            :aria-controls="species2Body" 
                                            aria-selected="false">
                                            <!-- @click="tabClicked()"> -->
                                        Species 2
                                        </a>
                                        <span>x</span>
                                    </li>
                                    <li>
                                        <a href="#" id="btnAdd"><i class="icon-plus-sign-alt"></i>Add</a>
                                    </li>
                                </ul>
                                <div class="tab-content" id="split_pills-tabContent">
                                    <div class="tab-pane fade show active" :id="originalBody" role="tabpanel" aria-labelledby="pills-original-tab">
                                        <SpeciesCommunitiesComponent v-if="species_community_original!=null"
                                            ref="species_communities_original" 
                                            :species_community.sync="species_community_original" 
                                            id="species_original" 
                                            :is_internal="true">
                                        </SpeciesCommunitiesComponent>
                                    </div>
                                    <div class="tab-pane fade" :id="species1Body" role="tabpanel" aria-labelledby="pills-species1-tab">
                                        <SpeciesCommunitiesComponent v-if="new_species_list[0]!=null"
                                            ref="species_communities_species1" 
                                            :species_community.sync="new_species_list[0]" 
                                            id="species_one" 
                                            :is_internal="true">
                                        </SpeciesCommunitiesComponent>
                                    </div>
                                    <div class="tab-pane fade" :id="species2Body" role="tabpanel" aria-labelledby="pills-species2-tab">
                                        <SpeciesCommunitiesComponent v-if="new_species_list[1]!=null"
                                            ref="species_communities_species2" 
                                            :species_community.sync="new_species_list[1]" 
                                            id="species_two" 
                                            :is_internal="true">
                                        </SpeciesCommunitiesComponent>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </form>
                </div>
            </div>

            <div slot="footer">
                <!-- <button type="button" v-if="issuingApproval" disabled class="btn btn-default" @click="ok"><i class="fa fa-spinner fa-spin"></i> Processing</button> -->
                <button type="button" class="btn btn-default" @click="ok">Submit</button>
                <button type="button" class="btn btn-default" @click="cancel">Cancel</button>
            </div>
        </modal>
    </div>
</template>

<script>
//import $ from 'jquery'
import Vue from 'vue'
import { createApp, h } from 'vue';
import modal from '@vue-utils/bootstrap-modal.vue'
import alert from '@vue-utils/alert.vue'
import FileField2 from '@/components/forms/filefield2.vue'
import SpeciesCommunitiesComponent from '@/components/form_species_communities.vue'
import {helpers,api_endpoints} from "@/utils/hooks.js"
export default {
    name:'SpeciesSplit',
    components:{
        modal,
        alert,
        FileField2,
        SpeciesCommunitiesComponent,
    },
    props:{
        species_community: {
            type: Object,
            required: true
        },
        is_internal: {
            type: Boolean,
            required: true
        },
    },
    data:function () {
        let vm = this;
        return {
            originalBody: 'originalBody' + vm._uid,
            species1Body: 'species1Body' + vm._uid,
            species2Body: 'species2Body' + vm._uid,
            species_community_original:null,
            isModalOpen:false,
            reloadcount:0,
            reloadcount1:1,
            reloadcount2:2,
            new_species_list:[],
            form:null,
            errors: false,
            errorString: '',
        }
    },
    computed: {
        csrf_token: function() {
          return helpers.getCookie('csrftoken')
        },
        showError: function() {
            var vm = this;
            return vm.errors;
        },
        title: function(){
            //return this.processing_status == 'With Approver' ? 'Approve Conservation Status' : 'Propose to approve Conservation Status';
            return this.species_community_original!=null? 'Split Species '+this.species_community_original.species_number : 'Split Species';
        },
    },
    methods:{
        //----function to resolve datatable exceeding beyond the div
        createTabs: function(){
            let vm=this;
            console.log(this.new_species_list.length);
            for(let i=0; i<=this.new_species_list.length; i++){
                console.log("loop"+i)
                var nextTab = $('#split_pills-tab li').length+1;
                console.log(nextTab)
                let speciesBody= 'speciesBody'+ nextTab + vm._uid;
                // create the tab
                $('<li class="nav-item"><a class="nav-link" id="pills-species'+ nextTab +'-tab" data-bs-toggle="pill" :href="#'+speciesBody+'" role="tab" aria-controls="'+speciesBody+'" aria-selected="true"> Species '+nextTab+'</a></li>').appendTo('#split_pills-tab');

                // create the tab content
                $('<div class="tab-pane fade" :id="'+speciesBody+'" role="tabpanel" aria-labelledby="pills-species'+ nextTab +'-tab"></div>').appendTo('.tab-content');
                // <SpeciesCommunitiesComponent ref="species_communities_species'+ nextTab+' :species_community.sync='+vm.new_species_list[i]+' id="species'+ nextTab+' :is_internal="true"></SpeciesCommunitiesComponent> 

                // make the new tab active
                // $('#tabs a:last').tab('show');

            }

        },
        tabClicked: function(){
        },
        ok:function () {
            let vm =this;
            if($(vm.form).valid()){
                vm.sendData();
                //vm.$router.push({ path: '/internal' });
            }
        },
        cancel:function () {
            this.close()
        },
        close:function () {
            this.isModalOpen = false;
            //this.approval = {};
            this.errors = false;
        },
        sendData:function(){
             let vm = this;
        },
        eventListeners:function () {
            let vm = this;
            $(".nav-pills").on("click", "span", function () {
                var anchor = $(this).siblings('a');
                $(anchor.attr('href')).remove();
                $(this).parent().remove();
                $(".nav-pills li").children('a').first().click();
            });

            $('#btnAdd').click(function (e) {
                var nextTab = $('#split_pills-tab li').length+1;
                console.log(vm.new_species_list[0])
                let speciesBody= 'speciesBody'+ nextTab + vm._uid;
                // create the tab
                $('<li class="nav-item"><a class="nav-link" id="pills-species'+ nextTab +'-tab" data-bs-toggle="pill" :href="#'+speciesBody+'" role="tab" aria-controls="'+speciesBody+'" aria-selected="true"> Species '+nextTab+'</a></li>').appendTo('#split_pills-tab');
                let i=0;
                // create the tab content
                $('<div class="tab-pane fade" :id="'+speciesBody+'" role="tabpanel" aria-labelledby="pills-species'+ nextTab +'-tab"></div>').appendTo('.tab-content');

                let species_data_app = createApp(SpeciesCommunitiesComponent, {
                        // props
                        ref: 'species_communities_species'+ nextTab,
                        species_community: vm.new_species_list[0],
                        id: 'species'+ nextTab,
                        is_internal: true,
                    })
                
                species_data_app.mount('#' + speciesBody)

                // <SpeciesCommunitiesComponent ref="species_communities_species'+ nextTab+' :species_community.sync='+vm.new_species_list[i]+' id="species'+ nextTab+' :is_internal="true"></SpeciesCommunitiesComponent> 

            });
                    
        },
   },
   mounted:function () {
        let vm =this;
        vm.form = document.forms.splitSpeciesForm;
        //vm.addFormValidations();
        this.$nextTick(()=>{
            //vm.createTabs();
            vm.eventListeners();
        });
   },
   created:function() {
        let vm = this;
        this.$nextTick(()=>{
            //vm.createTabs();
        });
   }
}
</script>

<style lang="css" scoped>
    .section{
        text-transform: capitalize;
    }
    .list-group{
        margin-bottom: 0;
    }
    .fixed-top{
        position: fixed;
        top:56px;
    }

    .nav-item {
        margin-bottom: 2px;
    }

    .nav-item>li>a {
        background-color: yellow !important;
        color: #fff;
    }

    .nav-item>li.active>a, .nav-item>li.active>a:hover, .nav-item>li.active>a:focus {
      color: white;
      background-color: blue;
      border: 1px solid #888888;
    }

        .admin > div {
          display: inline-block;
          vertical-align: top;
          margin-right: 1em;
        }
    .nav-pills .nav-link {
        border-bottom-left-radius: 0;
        border-bottom-right-radius: 0;
        border-top-left-radius: 0.5em;
        border-top-right-radius: 0.5em;
        margin-right: 0.25em;
    }
    .nav-pills .nav-link {
        background: lightgray;
    }
    .nav-pills .nav-link.active {
        background: gray;
    }
    .nav-pills > li {
    position:relative;    
    }

    .nav-pills > li > a {
        display:inline-block;
    }

    .nav-pills > li > span {
        display:none;
        cursor:pointer;
        position:absolute;
        right: 6px;
        top: 8px;
        color: red;
    }

    .nav-pills > li:hover > span {
        display: inline-block;
    }
</style>