<template lang="html">
    <div id="displayHistory">
        <modal
            transition="modal fade"
            :title="primary_model + ' History - Revision ' + revision_sequence"
            :large="true"
            :full="true"
            :showOK="false"
            cancel-text="Close"
            @cancel="close()">

            <div>
                <strong>Date Modified:</strong> {{ revision_date }}
            </div></br>
            <div v-for="(data, itemObjKey) in version_data">
                <div v-if="data.fields">
                <FormSection :formCollapse="false" :label="data.model_display_name+' - '+data.pk" :Index="itemObjKey+data.pk">
                    <div class="card-body card-collapse">
                        <div v-for="(value,index) in data.fields">
                            <div v-if="value" class="row-sm-12">  
                                <div v-if="typeof value == 'object'" class="col-sm-12">
                                    <div v-for="(o_value,o_index) in value">
                                        <label class="col-sm-6 control-label"><strong>{{index}}.{{o_index}}:</strong></label>
                                        <input :disabled="true" type="text" class="form-control col-sm-6" :value=o_value>
                                    </div>
                                </div>
                                <div v-else class="col-sm-12">
                                    <label class="col-sm-6 control-label"><strong>{{index}}:</strong></label>
                                    <input :disabled="true" type="text" class="form-control col-sm-6" :value=value>
                                </div>
                            </div>
                        </div>  
                    </div>            
                </FormSection>
                </div>
                <div v-else>
                    <div v-for="(sub_data) in data">
                    <FormSection :formCollapse="false" :label="sub_data.model_display_name+' - '+sub_data.pk" :Index="itemObjKey+sub_data.pk">
                        <div class="card-body card-collapse">
                            <div v-for="(value,index) in sub_data.fields">
                                <div v-if="value" class="row-sm-12">  
                                    <div v-if="typeof value == 'object'" class="col-sm-12">
                                        <div v-for="(o_value,o_index) in value">
                                            <label class="col-sm-6 control-label"><strong>{{index}}.{{o_index}}:</strong></label>
                                            <input :disabled="true" type="text" class="form-control col-sm-6" :value=o_value>
                                        </div>
                                    </div>
                                    <div v-else class="col-sm-12">
                                        <label class="col-sm-6 control-label"><strong>{{index}}:</strong></label>
                                        <input :disabled="true" type="text" class="form-control col-sm-6" :value=value>
                                    </div>
                                </div>
                            </div>  
                        </div>            
                    </FormSection>
                    </div>
                </div>
            </div>
        </modal>
    </div>
</template>

<script>
import Vue from 'vue'
import modal from '@vue-utils/bootstrap-modal.vue';
import FormSection from '@/components/forms/section_toggle.vue';
import {
  api_endpoints,
  helpers
}
from '@/utils/hooks'

export default {
    name:'DisplayHistory',
    components: {
        modal,
        FormSection,
    },
    props:{
        primary_model:{
            type: String,
            required:true
        },
        revision_id:{
            type: Number,
            required:true
        },
        revision_sequence:{
            type: Number,
            required:true
        },
    },

    data: function () {
        return {
            isModalOpen: false,
            errorString: '',
            version_data: [],
            revision_date: '',
        };
    },

    methods:{
        close: function () {
            this.errorString = '';
            this.isModalOpen = false;
            $('.has-error').removeClass('has-error');
        },
        fetchHistoryData: function(){
            let vm = this;
            vm.$http.get(api_endpoints.lookup_revision_versions(vm.primary_model,vm.revision_id))
            .then((response) => {
                vm.revision_date = response.body['date_created'];
                vm.version_data = response.body['version_data'];
            },(error) => {
                console.log(error);
            })
        },
    },
    mounted: function(){
        let vm = this;
        this.$nextTick(() => {
            vm.fetchHistoryData();
        });
    },
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
        padding: 0.375rem 2.25rem 0.375rem 0.75rem;
    }
    input[type=number]{
        width: 50%;
    }
    .interval-margin{
       margin-right: -100px;
    }
    .interval-range-true-input{
        width: 20%;
        margin-left: -80px;
    }
    .interval-range-true-choice{
        width: 20%;
    }
</style>