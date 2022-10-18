<template lang="html">
    <div id="internal-conservation-status-proposal-amend">
        <modal id="myModal" transition="modal fade" @ok="ok()" @cancel="cancel()" title="Amendment Request" large>
            <div class="container-fluid">
                <div class="row">
                    <form class="form-horizontal" name="amendForm">
                        <alert :show.sync="showError" type="danger"><strong>{{errorString}}</strong></alert>
                        <div class="col-sm-12">
                            <div class="row">
                                <div class="col-sm-offset-2 col-sm-8">
                                    <div class="form-group">
                                        <label class="control-label pull-left"  for="Name">Reason</label>
                                        <select class="form-select" name="reason" ref="reason" v-model="amendment.reason">
                                            <option v-for="r in reason_choices" :value="r.key">{{r.value}}</option>
                                        </select>
                                    </div>
                                </div>
                            </div>
                            <div class="row">
                                <div class="col-sm-offset-2 col-sm-8">
                                    <div class="form-group">
                                        <label class="control-label pull-left"  for="Name">Details</label>
                                        <textarea class="form-control" name="name" v-model="amendment.text" id="amendment_text"></textarea>
                                    </div>
                                </div>
                            </div>
                            <div class="row">
                                <div class="col-sm-offset-2 col-sm-8">
                                    <div class="form-group">
                                        <div class="input-group date" ref="add_attachments" style="width: 70%;">
                                            <FileField2
                                            ref="filefield"
                                            :uploaded_documents="amendment.cs_amendment_request_documents"
                                            :delete_url="delete_url"
                                            :proposal_id="conservation_status_id"
                                            :isRepeatable="true"
                                            name="amendment_request_file"/>
                                        </div>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </form>
                </div>
            </div>
        </modal>
    </div>
</template>

<script>
import Vue from 'vue'
import modal from '@vue-utils/bootstrap-modal.vue'
import alert from '@vue-utils/alert.vue'
import FileField2 from '@/components/forms/filefield2.vue'

import {helpers, api_endpoints} from "@/utils/hooks.js"
export default {
    name:'amendment-request',
    components:{
        modal,
        alert,
        FileField2,
    },
    props:{
            conservation_status_id:{
                type:Number,
            },
    },
    data:function () {
        let vm = this;
        return {
            isModalOpen:false,
            form:null,
            amendment: {
            reason:'',
            reason_id: null,
            amendingProposal: false,
            conservation_status: vm.conservation_status_id,
            num_files: 0,
            input_name: 'amendment_request_doc',
            cs_amendment_request_documents: [], 
            },
            reason_choices: {},
            errors: false,
            errorString: '',
            validation_form: null,
        }
    },
    computed: {
        showError: function() {
            var vm = this;
            return vm.errors;
        },
        delete_url: function() {
            return (this.amendment.id) ? '/api/cs_amendment_request/'+this.amendment.id+'/delete_document/' : '';
        }
    },
    methods:{

        ok:function () {
            let vm =this;
            if($(vm.form).valid()){
                vm.sendData();
            }
        },
        cancel:function () {
            let vm = this;
            vm.close();
        },
        close:function () {
            this.isModalOpen = false;
            this.amendment = {
                reason: '',
                reason_id: null,
                conservation_status: this.conservation_status_id
            };
            this.errors = false;
            $(this.$refs.reason).val(null).trigger('change');
            $('.has-error').removeClass('has-error');
            
            this.validation_form.resetForm();
        },
        fetchAmendmentChoices: function(){
            let vm = this;
            vm.$http.get('/api/amendment_request_reason_choices.json').then((response) => {
                vm.reason_choices = response.body;
            },(error) => {
                console.log(error);
            } );
        },
        sendData:function(){
            let vm = this;
            vm.errors = false;
            let amendment = JSON.parse(JSON.stringify(vm.amendment));
            let formData = new FormData()
            var files = vm.$refs.filefield.files;
            $.each(files, function (idx, v) {
                var file = v['file'];
                var filename = v['name'];
                var name = 'file-' + idx;
                formData.append(name, file, filename);
            });
            amendment.num_files = files.length;
            amendment.input_name = 'amendment_request_doc';
            amendment.conservation_status = vm.conservation_status_id;
            amendment.update = true;

            formData.append('data', JSON.stringify(amendment));

            // vm.$http.post('/api/amendment_request.json',JSON.stringify(amendment),{
                vm.$http.post('/api/cs_amendment_request.json', formData,{
                        emulateJSON:true,
                    }).then((response)=>{
                        swal(
                             'Sent',
                             'An email has been sent to applicant with the request to amend this Application',
                             'success'
                        );
                        vm.amendingProposal = true;
                        vm.close();
                        //vm.$emit('refreshFromResponse',response);
                        Vue.http.get(`/api/conservation_status/${vm.conservation_status_id}/internal_conservation_status.json`).then((response)=>
                        {
                            vm.$emit('refreshFromResponse',response);

                        },(error)=>{
                            console.log(error);
                        });
                        vm.$router.push({ path: '/internal' }); //Navigate to dashboard after creating Amendment request

                    },(error)=>{
                        console.log(error);
                        vm.errors = true;
                        vm.errorString = helpers.apiVueResourceError(error);
                        vm.amendingProposal = true;

                    });
                

        },
        addFormValidations: function() {
            let vm = this;
            vm.validation_form = $(vm.form).validate({
                rules: {
                    reason: "required"
                    
                     
                },
                messages: {              
                    reason: "field is required",
                                         
                },
                showErrors: function(errorMap, errorList) {
                    $.each(this.validElements(), function(index, element) {
                        var $element = $(element);
                        $element.attr("data-original-title", "").parents('.form-group').removeClass('has-error');
                    });
                    // destroy tooltips on valid elements
                    // commented below (Priya) as gives error for .tooltipz
                    //$("." + this.settings.validClass).tooltip("destroy");
                    // add or update tooltips
                    for (var i = 0; i < errorList.length; i++) {
                        var error = errorList[i];
                        $(error.element)
                            .tooltip({
                                trigger: "focus"
                            })
                            .attr("data-original-title", error.message)
                            .parents('.form-group').addClass('has-error');
                    }
                }
            });
       },
       eventListerners:function () {
            let vm = this;
            
            // Intialise select2
            $(vm.$refs.reason).select2({
                "theme": "bootstrap-5",
                allowClear: true,
                placeholder:"Select Reason",
                dropdownParent: $('#myModal .modal-body'),
            }).
            on("select2:select",function (e) {
                var selected = $(e.currentTarget);
                vm.amendment.reason = selected.val();
                vm.amendment.reason_id = selected.val();
            }).
            on("select2:unselect",function (e) {
                var selected = $(e.currentTarget);
                vm.amendment.reason = selected.val();
                vm.amendment.reason_id = selected.val();
            });
        }
   },
   mounted:function () {
        let vm =this;
        vm.form = document.forms.amendForm;
        vm.fetchAmendmentChoices();
        vm.addFormValidations();
        this.$nextTick(()=>{  
            vm.eventListerners();
        });
    //console.log(validate);
   }
}
</script>

<style lang="css">

</style>
