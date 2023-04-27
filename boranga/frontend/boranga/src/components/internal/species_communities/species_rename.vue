<template lang="html">
    <div id="renameSpecies">
        <modal transition="modal fade" @ok="ok()" @cancel="cancel()" :title="title" large id="myModal">
            <div class="container-fluid">
                <div class="row">
                    <form class="form-horizontal" name="renameSpeciesForm">
                        <alert :show.sync="showError" type="danger"><strong>{{errorString}}</strong></alert>
                        <div>
                            <div class="col-md-12">
                                <SpeciesCommunitiesComponent v-if="new_rename_species!=null"
                                            ref="rename_species" 
                                            :species_community.sync="new_rename_species"
                                            id="rename_species" 
                                            :is_internal="true"
                                            :is_readonly="true"
                                            :rename_species="true"> //  rename=true used to make only taxon select editable on form
                                </SpeciesCommunitiesComponent>
                            </div>
                        </div>
                    </form>
                </div>
            </div>

            <div slot="footer">
                <!-- <button type="button" class="btn btn-default" @click="ok">Submit</button> -->
                <button v-if="submitSpeciesRename" class="btn btn-primary pull-right" style="margin-top:5px;" disabled >Submit&nbsp;<i class="fa fa-circle-o-notch fa-spin fa-fw"></i></button>
                <button v-else class="btn btn-default" @click.prevent="ok()" :disabled="submitSpeciesRename">Submit</button>
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
    name:'SpeciesRename',
    components:{
        modal,
        alert,
        FileField2,
        SpeciesCommunitiesComponent,
    },
    props:{
        species_community_original: {
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
            newSpeciesBody: 'newSpeciesBody' + vm._uid,
            speciesBody: 'speciesBody' + vm._uid,
            new_rename_species:null,
            submitSpeciesRename:false,
            isModalOpen:false,
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
            return this.new_rename_species!=null?'Rename Species '+this.species_community_original.species_number + ' to ' +this.new_rename_species.species_number:'';
        },
    },
    methods:{
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
            let vm =this;
            vm.discardSpecies(vm.new_rename_species.id);
            this.isModalOpen = false;
            this.errors = false;
        },
        discardSpecies:function (species_id) {
            let vm = this;
            try{
                vm.$http.delete(api_endpoints.discard_species_proposal(species_id));
            }
            catch (err) {
                console.log(err);
                if (this.is_internal) {
                    return err;
                }
            }
        },
        save_before_submit: async function(new_species) {
            //console.log('save before submit');
            let vm = this;
            vm.saveError=false;

            let payload = new Object();
            Object.assign(payload, new_species);
            const result = await vm.$http.post(`/api/species/${new_species.id}/species_save.json`,payload).then(res=>{
                return true;
            },err=>{
                        var errorText=helpers.apiVueResourceError(err); 
                        swal(
                                'Submit Error',
                                errorText,
                                'error'
                            )
                        vm.submitSpeciesRename=false;
                        vm.saveError=true;
                        return false;
            });
            return result;
        },
        sendData:async function(){
            let vm = this;

            // var missing_data= vm.can_submit();
            // if(missing_data!=true){
            //     swal({
            //         title: "Please fix following errors before submitting",
            //         text: missing_data,
            //         type:'error'
            //     })
            //     //vm.paySubmitting=false;
            //     return false;
            // }
            if(vm.new_rename_species.taxonomy_id && vm.new_rename_species.taxonomy_id == vm.species_community_original.taxonomy_id){
                swal({
                            title: "Please fix following errors",
                            text: "Species To Rename already exists",
                            type:'error'
                    })
            }
            else{
                vm.submitSpeciesRename=true;
                swal({
                    title: "Submit",
                    text: "Are you sure you want to submit this Species Rename?",
                    type: "question",
                    showCancelButton: true,
                    confirmButtonText: "submit"
                }).then(async () => {
                    //---save and submit the new rename species
                    let new_species = vm.new_rename_species;
                    //-- save new species before submit
                    let result = await vm.save_before_submit(new_species);
                    if(!vm.saveError){
                        // add the parent species to the new species object
                        new_species.parent_species=[vm.species_community_original];
                        let payload = new Object();
                        Object.assign(payload, new_species);
                        // TODO May be need to create another submit method for rename as the mail and action could be different
                        let submit_url = helpers.add_endpoint_json(api_endpoints.species,new_species.id+'/rename_new_species_submit')
                        vm.$http.post(submit_url,payload).then(res=>{
                            vm.new_species = res.body;
                            vm.$router.push({
                                name: 'internal-species-communities-dash'
                            });
                            //vm.submit_original_species();
                        },err=>{
                            swal(
                                'Submit Error',
                                helpers.apiVueResourceError(err),
                                'error'
                            )
                            vm.saveError=true;
                        });
                    }

                },(error) => {
                    vm.submitSpeciesRename=false;
                });
            }
        },
        // the below not used as the original species has already been send in the  rename_new_species_submit method
        // submit_original_species: function(){
        //     let vm=this;
        //     let payload = new Object();
        //     Object.assign(payload, vm.species_community_original);
        //     let submit_url = helpers.add_endpoint_json(api_endpoints.species,vm.species_community_original.id+'/change_status_historical')
        //     vm.$http.post(submit_url,payload).then(res=>{
        //         vm.species_community_original = res.body;
        //         // TODO Not sure where it should go after the split process
        //         vm.$router.push({
        //             name: 'internal-species-communities-dash'
        //         });
        //     },err=>{
        //         swal(
        //             'Submit Error',
        //             helpers.apiVueResourceError(err),
        //             'error'
        //         )
        //     });
        // },
        // eventListeners:function () {
        //     let vm = this;
        // },
   },
   mounted:function () {
        let vm =this;
        vm.form = document.forms.renameSpeciesForm;
        //vm.addFormValidations();
        this.$nextTick(()=>{
            vm.eventListeners();
        });
   },
   created:function() {
        let vm = this;
        this.$nextTick(()=>{
        });
   }
}
</script>

<style lang="css" scoped>

</style>