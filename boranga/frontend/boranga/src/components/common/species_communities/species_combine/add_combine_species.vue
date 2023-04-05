<template lang="html">
    <div id="addCombineSpecies">
        <modal transition="modal fade" @ok="ok()" @cancel="cancel()" :title="title" large id="myAddSpeciesToCombineModal">
            <div class="container-fluid">
                <div class="row">
                    <form class="form-horizontal" name="addSpeciesToCombine">
                        <alert :show.sync="showError" type="danger"><strong>{{errorString}}</strong></alert>
                        <div>
                            <div class="row mb-3">
                                <label for="" class="col-sm-3 control-label">Species:</label>
                                <div class="col-sm-9">
                                    <select class="form-select" 
                                        v-model="combineSpeciesId" id="scientific_name">
                                        <option v-for="s in species_list" :value="s.id" :key="s.id">{{s.id}} - {{s.scientific_name}}</option>
                                    </select>
                                </div>
                            </div>
                        </div>
                    </form>
                </div>
            </div>
            <div slot="footer">
                <!-- <button type="button" class="btn btn-default" @click="ok">Submit</button> -->
                <button class="btn btn-default" @click.prevent="ok()">ok</button>
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
import {helpers,api_endpoints} from "@/utils/hooks.js"
export default {
    name:'AddCombineSpecies',
    components:{
        modal,
        alert,
    },
    data:function () {
        let vm = this;
        return {
            isModalOpen:false,
            form:null,
            errors: false,
            errorString: '',
            species_list: [],
            combineSpeciesId: null,
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
            return 'Select Species To Combine';
        },
    },
    methods:{
        ok:function () {
            let vm =this;
            if($(vm.form).valid()){
                vm.addSpeciesToCombineList()
            }
        },
        cancel:function () {
            this.close()
        },
        close:function () {
            let vm =this;
            //vm.original_species_combine_list=[];
            this.isModalOpen = false;
            this.errors = false;
        },
        addSpeciesToCombineList: function (){
            let vm = this;
            try {
                Vue.http.get(`/api/species/${vm.combineSpeciesId}/internal_species.json`).then(res => {
                    let species_obj=res.body.species_obj;
                    // user should not select the same ID if already exists in the array to combine
                    let hasSpecies=false;
                    for (const species of vm.$parent.original_species_combine_list){
                        if(species.id === species_obj.id){
                            hasSpecies=true;
                        }
                    }
                    if(hasSpecies==true){
                        swal({
                            title: "Please fix following errors",
                            text: "Species To combine already exists",
                            type:'error'
                        })
                    }
                    else{
                        vm.$parent.original_species_combine_list.push(species_obj); //--temp species_obj
                    }
                },
                err => {
                console.log(err);
                });
            }
            catch (err) {
                console.log(err);
                if (this.is_internal) {
                    return err;
                }
            }
            this.close()
        },
    },
    mounted:function () {
        let vm =this;
        vm.form = document.forms.addSpeciesToCombine;
        //vm.addFormValidations();
        this.$nextTick(()=>{
        });
   },
   created:async function() {
        let vm = this;
        //-----fetch species_list
        // TODO will need the species filtered with status current, etc. 
        const res = await Vue.http.get('/api/species/species_list.json');
        vm.species_list= res.body.data;
   }
}
</script>

<style lang="css" scoped>
    
</style>
