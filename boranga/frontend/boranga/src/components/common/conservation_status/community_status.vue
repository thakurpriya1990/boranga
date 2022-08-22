<template lang="html">
    <div id="communityStatus">
        <FormSection :formCollapse="false" label="Taxonomy" Index="taxonomy">
            <div class="row mb-3">
                <label for="" class="col-sm-3 control-label">Species:</label>
                <div class="col-sm-9">
                    <select style="width:100%;" class="form-select input-sm" multiple ref="species_select" 
                        v-model="conservation_status_obj.species" >
                        <option v-for="s in species_list" :value="s.id" >{{s.id}} - {{s.scientific_name}}</option>
                    </select>
                </div>
            </div>
            <div class="row mb-3">
                <label for="" class="col-sm-3 control-label">Community Name:</label>
                <div class="col-sm-9">
                    <select :disabled="conservation_status_obj.readonly" class="form-select" 
                        v-model="conservation_status_obj.community_name_id" id="community_name" 
                            @change="getCommunityNameDisplay()">
                        <option v-for="option in community_name_list" :value="option.id" v-bind:key="option.id">
                            {{ option.name }}                            
                        </option>
                    </select>
                </div>
            </div>
            <div class="row mb-3">
                <label for="" class="col-sm-3 control-label"></label>
                <div class="col-sm-9">
                    <textarea disabled class="form-control" rows="3" id="community_name_display" 
                    v-model="community_name_display"/>
                </div>
            </div>
            <div class="row mb-3">
                <label for="" class="col-sm-3 control-label">Community ID:</label>
                <div class="col-sm-9">
                    <input :disabled="conservation_status_obj.readonly" type="text" class="form-control" 
                    id="community_migrated_id" placeholder=""
                    v-model="conservation_status_obj.community_migrated_id"/>
                </div>
            </div>
            <div class="row mb-3">
                <label for="" class="col-sm-3 control-label">Community Description:</label>
                <div class="col-sm-9">
                    <textarea :disabled="conservation_status_obj.readonly" class="form-control" rows="3" id="community_description" placeholder=""
                    v-model="conservation_status_obj.community_description"/>
                </div>
            </div>
            <div class="row mb-3">
                <label for="" class="col-sm-3 control-label">Previous Name:</label>
                <div class="col-sm-9">
                    <textarea :disabled="conservation_status_obj.readonly" class="form-control" id="community_previous_name" placeholder="" v-model="conservation_status_obj.previous_name"/>
                </div>
            </div>
            <div class="row mb-3">
                <label for="" class="col-sm-3 control-label">Comments:</label>
                <div class="col-sm-9">
                    <textarea :disabled="conservation_status_obj.readonly" class="form-control" id="community_comment" placeholder="" v-model="conservation_status_obj.name_comments"/>
                </div>
            </div>
        </FormSection>
    </div>
</template>

<script>
import Vue from 'vue' ;
import FormSection from '@/components/forms/section_toggle.vue';
import {
  api_endpoints,
  helpers
}
from '@/utils/hooks'
require("select2/dist/css/select2.min.css");
require("select2-bootstrap-5-theme/dist/select2-bootstrap-5-theme.min.css")

export default {
        name: 'CommunityStatus',
        props:{
            conservation_status_obj:{
                type: Object,
                required:true
            },
        },
        data:function () {
            let vm = this;
            return{
                datepickerOptions:{
                    format: 'DD/MM/YYYY',
                    showClear:true,
                    useCurrent:false,
                    keepInvalid:true,
                    allowInputToggle:true,
                },
                species_list: [],
                community_profile_dict: {},
                community_name_list: [],
                community_name_display:'',
            }
        },
        components: {
            FormSection,
        },
        computed: {
        },
        watch:{
        },
        methods:{
            checkDate: function(){
                let vm=this;
                if(vm.$refs.last_data_curration_date.value){
                    vm.conservation_status_obj.last_data_curration_date = vm.$refs.last_data_curration_date.value;
                }
                else{
                    vm.conservation_status_obj.last_data_curration_date=null;
                }
            },
            getCommunityNameDisplay: function(){
                for(let choice of this.community_name_list){
                        if(choice.id === this.conservation_status_obj.community_name_id)
                        {
                          this.community_name_display = choice.name;
                        }
                    }
            },
            eventListeners:function (){
                let vm=this;

                var date= new Date()
                var today= new Date(date.getFullYear(), date.getMonth(), date.getDate());
            },
        },
        created: async function() {
            let vm = this;
            //-----fetch species_list
            const res = await Vue.http.get('/api/species/species_list.json');
            vm.species_list= res.body.data;
            //------fetch list of values
            const res_obj = await Vue.http.get('/api/community_profile_dict/');
            vm.community_profile_dict = res_obj.body;
            vm.community_name_list = vm.community_profile_dict.community_name_list;
            vm.community_name_list.splice(0,0,
                {
                    id: null,
                    name: null,
                });
            this.getCommunityNameDisplay();
        },
        mounted: function(){
            let vm = this;

            // Initialise select2 for Species
            $(vm.$refs.species_select).select2({
                "theme": "bootstrap-5",
                allowClear: true,
                placeholder:"Select Species",
                multiple: true,
            }).
            on("select2:select",function (e) {
                var selected = $(e.currentTarget);
                vm.conservation_status_obj.species = selected.val();
            }).
            on("select2:unselect",function (e) {
                var selected = $(e.currentTarget);
                vm.conservation_status_obj.species = selected.val();
            });
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
    input[type=text], select {
        width: 100%;
    }
</style>

