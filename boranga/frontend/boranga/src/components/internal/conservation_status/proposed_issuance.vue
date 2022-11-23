<template lang="html">
    <div id="proposedIssuanceApproval">
        <modal transition="modal fade" @ok="ok()" @cancel="cancel()" :title="title" large>
            <div class="container-fluid">
                <div class="row">
                    <form class="form-horizontal" name="approvalForm">
                        <alert :show.sync="showError" type="danger"><strong>{{errorString}}</strong></alert>
                        <div class="col-sm-12">
                            <div class="form-group">
                                <div class="row mb-3">
                                    <div class="col-sm-4">
                                        <label v-if="processing_status == 'With Approver'" class="control-label pull-left"  for="Name">Effective From Date</label>
                                        <label v-else class="control-label pull-left"  for="Name">Proposed Effective From Date</label>
                                    </div>
                                    <div class="col-sm-8">
                                        <div class="input-group date" style="width: 70%;">
                                            <input type="date" class="form-control" ref="start_date" placeholder="DD/MM/YYYY" v-model="approval.effective_from_date">
                                            <!-- <span class="input-group-addon">
                                                <span class="glyphicon glyphicon-calendar"></span>
                                            </span> -->
                                        </div>
                                    </div>
                                </div>
                                <div class="row" v-show="showstartDateError">
                                    <alert  class="col-sm-12" type="danger"><strong>{{startDateErrorString}}</strong></alert>
                    
                                </div>
                            </div>
                            <div class="form-group">
                                <div class="row mb-3">
                                    <div class="col-sm-4">
                                        <label v-if="processing_status == 'With Approver'" class="control-label pull-left"  for="Name">Effective To Date</label>
                                        <label v-else class="control-label pull-left"  for="Name">Proposed Effective To Date</label>
                                    </div>
                                    <div class="col-sm-8">
                                        <div class="input-group date" style="width: 70%;">
                                            <!--<input type="text" class="form-control" name="due_date" placeholder="DD/MM/YYYY" v-model="approval.expiry_date" :disabled="is_amendment">-->
                                            <input type="date" class="form-control" ref="due_date" placeholder="DD/MM/YYYY" v-model="approval.effective_to_date">
                                            <!-- <span class="input-group-addon">
                                                <span class="glyphicon glyphicon-calendar"></span>
                                            </span> -->
                                        </div>
                                    </div>
                                </div>
                                <div class="row" v-show="showtoDateError">
                                    <alert  class="col-sm-12" type="danger"><strong>{{toDateErrorString}}</strong></alert>
                    
                                </div>
                                
                            </div>
                            <div class="form-group">
                                <div class="row mb-3">
                                    <div class="col-sm-4">
                                        <label v-if="processing_status == 'With Approver'" class="control-label pull-left"  for="Name">Details</label>
                                        <label v-else class="control-label pull-left"  for="Name">Proposed Details</label>
                                    </div>
                                    <div class="col-sm-8">
                                        <textarea name="approval_details" class="form-control" style="width:70%;" v-model="approval.details"></textarea>
                                    </div>
                                </div>
                            </div>
                            <div class="form-group">
                                <div class="row mb-3">
                                    <div class="col-sm-4">
                                        <label v-if="processing_status == 'With Approver'" class="control-label pull-left"  for="Name">CC email</label>
                                        <label v-else class="control-label pull-left"  for="Name">Proposed CC email</label>
                                    </div>
                                    <div class="col-sm-8">
                                            <input type="text" class="form-control" name="approval_cc" style="width:70%;" v-model="approval.cc_email">
                                    </div>
                                </div>
                            </div>
                        </div>
                    </form>
                </div>
            </div>

            <!-- <p v-if="can_preview">Click <a href="#" @click.prevent="preview">here</a> to preview the licence document.</p> -->

            <div slot="footer">
                <button type="button" v-if="issuingApproval" disabled class="btn btn-default" @click="ok"><i class="fa fa-spinner fa-spin"></i> Processing</button>
                <button type="button" v-else class="btn btn-default" @click="ok">Ok</button>
                <button type="button" class="btn btn-default" @click="cancel">Cancel</button>
            </div>
        </modal>
    </div>
</template>

<script>
//import $ from 'jquery'
import modal from '@vue-utils/bootstrap-modal.vue'
import alert from '@vue-utils/alert.vue'
import {helpers,api_endpoints} from "@/utils/hooks.js"
export default {
    name:'Proposed-Approval',
    components:{
        modal,
        alert
    },
    props:{
        conservation_status_id: {
            type: Number,
            required: true
        },
        processing_status: {
            type: String,
            required: true
        },
        // proposal_type: {
        //     type: String,
        //     required: true
        // }
    },
    data:function () {
        let vm = this;
        return {
            isModalOpen:false,
            form:null,
            approval: {},
            state: 'proposed_approval',
            issuingApproval: false,
            validation_form: null,
            errors: false,
            toDateError:false,
            startDateError:false,
            errorString: '',
            toDateErrorString:'',
            startDateErrorString:'',
            successString: '',
            success:false,
            datepickerOptions:{
                format: 'DD/MM/YYYY',
                showClear:true,
                useCurrent:false,
                keepInvalid:true,
                allowInputToggle:true
            },
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
        showtoDateError: function() {
            var vm = this;
            return vm.toDateError;
        },
        showstartDateError: function() {
            var vm = this;
            return vm.startDateError;
        },
        title: function(){
            return this.processing_status == 'With Approver' ? 'Approve Conservation Status' : 'Propose to approve Conservation Status';
        },
        // is_amendment: function(){
        //     return this.proposal_type == 'Amendment' ? true : false;
        // },
        can_preview: function(){
            return (this.processing_status == 'With Approver' || 'With Assessor (Requirements)') && this.approval.effective_from_date && this.approval.effective_to_date ? true : false;
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
            this.isModalOpen = false;
            this.approval = {};
            this.errors = false;
            // this.toDateError = false;
            // this.startDateError = false;
            // $('.has-error').removeClass('has-error');
            // $(this.$refs.due_date).data('DateTimePicker').clear();
            // $(this.$refs.start_date).data('DateTimePicker').clear();
            // this.validation_form.resetForm();
        },
        sendData:function(){
            let vm = this;
            vm.errors = false;
            let approval = JSON.parse(JSON.stringify(vm.approval));
            vm.issuingApproval = true;
            if (vm.state == 'proposed_approval'){
                vm.$http.post(helpers.add_endpoint_json(api_endpoints.conservation_status,vm.conservation_status_id+'/proposed_approval'),JSON.stringify(approval),{
                        emulateJSON:true,
                    }).then((response)=>{
                        vm.issuingApproval = false;
                        vm.close();
                        vm.$emit('refreshFromResponse',response);
                        vm.$router.push({ path: '/internal/conservation-status/' }); //Navigate to dashboard page after Propose issue.
                    },(error)=>{
                        vm.errors = true;
                        vm.issuingApproval = false;
                        vm.errorString = helpers.apiVueResourceError(error);
                    });
            }
            else if (vm.state == 'final_approval'){
                vm.$http.post(helpers.add_endpoint_json(api_endpoints.conservation_status,vm.conservation_status_id+'/final_approval'),JSON.stringify(approval),{
                        emulateJSON:true,
                    }).then((response)=>{
                        vm.issuingApproval = false;
                        vm.close();
                        vm.$emit('refreshFromResponse',response);
                    },(error)=>{
                        vm.errors = true;
                        vm.issuingApproval = false;
                        vm.errorString = helpers.apiVueResourceError(error);
                    });
            }
            
        },
        addFormValidations: function() {
            let vm = this;
            vm.validation_form = $(vm.form).validate({
                rules: {
                    start_date:"required",
                    due_date:"required",
                    approval_details:"required",
                },
                messages: {
                },
                showErrors: function(errorMap, errorList) {
                    $.each(this.validElements(), function(index, element) {
                        var $element = $(element);
                        $element.attr("data-original-title", "").parents('.form-group').removeClass('has-error');
                    });
                    // destroy tooltips on valid elements
                    $("." + this.settings.validClass).tooltip("destroy");
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
       eventListeners:function () {
            let vm = this;
            // Initialise Date Picker
            // $(vm.$refs.due_date).datetimepicker(vm.datepickerOptions);
            // $(vm.$refs.due_date).on('dp.change', function(e){
            //     if ($(vm.$refs.due_date).data('DateTimePicker').date()) {
            //         if ($(vm.$refs.due_date).data('DateTimePicker').date() < $(vm.$refs.start_date).data('DateTimePicker').date()){
            //             vm.toDateError = true;
            //             vm.toDateErrorString = 'Please select Effective To date that is after Effective From date';
            //             vm.approval.effective_to_date = ""
            //         }
            //         else{
            //             vm.toDateError = false;
            //             vm.toDateErrorString = '';
            //             vm.approval.effective_to_date =  e.date.format('DD/MM/YYYY');
            //         }
            //     }
            //     else if ($(vm.$refs.due_date).data('date') === "") {
            //         vm.approval.effective_to_date = "";
            //     }
            //  });
            // $(vm.$refs.start_date).datetimepicker(vm.datepickerOptions);
            // $(vm.$refs.start_date).on('dp.change', function(e){
            //     if ($(vm.$refs.start_date).data('DateTimePicker').date()) {
            //         if (($(vm.$refs.due_date).data('DateTimePicker').date()!= null)&& ($(vm.$refs.due_date).data('DateTimePicker').date() < $(vm.$refs.start_date).data('DateTimePicker').date())){
            //             vm.startDateError = true;
            //             vm.startDateErrorString = 'Please select Effective From date that is before Effective To date';
            //             vm.approval.effective_from_date = ""
            //         }
            //         else{
            //             vm.startDateError = false;
            //             vm.startDateErrorString = '';
            //             vm.approval.effective_from_date =  e.date.format('DD/MM/YYYY');
            //         }
            //     }
            //     else if ($(vm.$refs.start_date).data('date') === "") {
            //         vm.approval.effective_from_date = "";
            //     }
            //  });

             //--------Priya
            $(vm.$refs.due_date).on('change', function(e){
                if ($(vm.$refs.due_date)!=null) {
                    if (new Date($(vm.$refs.due_date.value)) < Date.parse($(vm.$refs.start_date.value))){
                        vm.toDateError = true;
                        vm.toDateErrorString = 'Please select Effective To date that is after Effective From date';
                        vm.approval.effective_to_date = ""
                    }
                    else{
                        vm.toDateError = false;
                        vm.toDateErrorString = '';
                        vm.approval.effective_to_date =  vm.$refs.due_date;
                    }
                }
                else if ($(vm.$refs.due_date) === "") {
                    vm.approval.effective_to_date = "";
                }
             });
            $(vm.$refs.start_date).on('change', function(e){
                if ($(vm.$refs.start_date)!=null) {
                    if (($(vm.$refs.due_date)!= null) && (Date.parse($(vm.$refs.due_date.value)) < Date.parse($(vm.$refs.start_date.value)))){
                        vm.startDateError = true;
                        vm.startDateErrorString = 'Please select Effective From date that is before Effective To date';
                        vm.approval.effective_from_date = ""
                    }
                    else{
                        vm.startDateError = false;
                        vm.startDateErrorString = '';
                        vm.approval.effective_from_date =  vm.$refs.start_date;
                    }
                }
                else if ($(vm.$refs.start_date) === "") {
                    vm.approval.effective_from_date = "";
                }
            });
       }
   },
   mounted:function () {
        let vm =this;
        vm.form = document.forms.approvalForm;
        //vm.addFormValidations();
        this.$nextTick(()=>{
            //vm.eventListeners();
        });
   }
}
</script>

<style lang="css">
</style>