<template lang="html">
    <div id="proposedIssuanceApproval">
        <modal transition="modal fade" @ok="ok()" @cancel="cancel()" :title="title" large>
            <div class="container-fluid">
                <div class="row">
                    <form class="form-horizontal" name="approvalForm">
                        <alert :show.sync="showError" type="danger"><strong>{{errorString}}</strong></alert>
                        <alert type="danger" v-if="!isEffectiveDateValid"><strong>Please select Effective To Date that is after Effective From Date</strong></alert>
                        <div class="col-sm-12">
                            <div class="form-group">
                                <div class="row mb-3">
                                    <div class="col-sm-4">
                                        <!-- <label v-if="processing_status == 'With Approver'" class="control-label pull-left"  for="Name">Effective From Date</label>
                                        <label v-else class="control-label pull-left"  for="Name">Proposed Effective From Date</label> -->
                                        <label class="control-label pull-left"  for="Name">Effective From Date</label>
                                    </div>
                                    <div class="col-sm-8">
                                        <div class="input-group date" style="width: 70%;">
                                            <input type="date" class="form-control" ref="start_date" placeholder="DD/MM/YYYY" v-model="approval.effective_from_date"
                                            @change="validateEffectiveFromDate($event)">
                                            <!-- <span class="input-group-addon">
                                                <span class="glyphicon glyphicon-calendar"></span>
                                            </span> -->
                                        </div>
                                        <small style="color: red;" v-show="showstartDateError">This field is required</small>
                                    </div>
                                </div>
                               
                            </div>
                            <div class="form-group">
                                <div class="row mb-3">
                                    <div class="col-sm-4">
                                        <!-- <label v-if="processing_status == 'With Approver'" class="control-label pull-left"  for="Name">Effective To Date</label>
                                        <label v-else class="control-label pull-left"  for="Name">Proposed Effective To Date</label> -->
                                        <label class="control-label pull-left"  for="Name">Effective To Date</label>
                                    </div>
                                    <div class="col-sm-8">
                                        <div class="input-group date" style="width: 70%;">
                                            <!--<input type="text" class="form-control" name="due_date" placeholder="DD/MM/YYYY" v-model="approval.expiry_date" :disabled="is_amendment">-->
                                            <input type="date" class="form-control" ref="due_date" placeholder="DD/MM/YYYY" v-model="approval.effective_to_date"
                                            @change="validateEffectiveToDate($event)">
                                            <!-- <span class="input-group-addon">
                                                <span class="glyphicon glyphicon-calendar"></span>
                                            </span> -->
                                        </div>
                                        <small style="color: red;" v-show="showtoDateError">This field is required</small>
                                    </div>
                                </div>
                               
                                
                            </div>
                            <div class="form-group">
                                <div class="row mb-3">
                                    <div class="col-sm-4">
                                        <!-- <label v-if="processing_status == 'With Approver'" class="control-label pull-left"  for="Name">Details</label>
                                        <label v-else class="control-label pull-left"  for="Name">Proposed Details</label> -->
                                        <label class="control-label pull-left"  for="Name">Details</label>
                                    </div>
                                    <div class="col-sm-8">
                                        <textarea name="approval_details" ref="approval_details" class="form-control" style="width:70%;" v-model="approval.details"
                                        @blur="validateDetails($event)"></textarea>
                                        <small style="color: red;" v-show="showDetailsError">This field is required</small>
                                    </div>
                                </div>
                            </div>
                            <div class="form-group">
                                <div class="row mb-3">
                                    <div class="col-sm-4">
                                        <!-- <label v-if="processing_status == 'With Approver'" class="control-label pull-left"  for="Name">CC email</label>
                                        <label v-else class="control-label pull-left"  for="Name">Proposed CC email</label> -->
                                        <label class="control-label pull-left"  for="Name">CC email</label>
                                    </div>
                                    <div class="col-sm-8">
                                            <input type="text" class="form-control" name="approval_cc" style="width:70%;" v-model="approval.cc_email">
                                    </div>
                                </div>
                            </div>
                            <!-- <div class="form-group" v-if="processing_status == 'With Approver'"> -->
                            <div class="form-group" v-if="processing_status == 'With Assessor' || processing_status == 'Ready For Agenda'">
                                <div class="row mb-3">
                                    <div class="col-sm-4">
                                        <label class="control-label pull-left" >Approval Document</label>
                                    </div>
                                    <div class="col-sm-8">
                                        <FileField2
                                        ref="filefield"
                                        :proposal_id="conservation_status_id"
                                        :isRepeatable="false"
                                        name="cs_approval_file"/>
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
import FileField2 from '@/components/forms/filefield2.vue'
import {helpers,api_endpoints} from "@/utils/hooks.js"
export default {
    name:'Proposed-Approval',
    components:{
        modal,
        alert,
        FileField2,
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
            uploadedFile: null,
            state: 'proposed_approval',
            issuingApproval: false,
            validation_form: null,
            errors: false,
            showtoDateError:false,
            showstartDateError:false,
            showDetailsError:false,
            errorString: '',
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
        isEffectiveDateValid: function () {
            if(this.approval.effective_from_date && this.approval.effective_to_date){
                const fromDate = new Date(this.approval.effective_from_date);
                const toDate = new Date(this.approval.effective_to_date);
                return fromDate < toDate;
            }
            else{
                return true;
            }
        },
        title: function(){
            // return this.processing_status == 'With Approver' ? 'Approve Conservation Status' : 'Propose to approve Conservation Status';
            return 'Approve Conservation Status';
        },
        // is_amendment: function(){
        //     return this.proposal_type == 'Amendment' ? true : false;
        // },
        can_preview: function(){
            return (this.processing_status == 'With Approver' || 'With Assessor (Requirements)') && this.approval.effective_from_date && this.approval.effective_to_date ? true : false;
        },
        // delete_url: function() {
        //     return (this.approval.id) ? '/api/cs_amendment_request/'+this.approval.id+'/delete_document/' : '';
        // }
    },
    methods:{
        ok:function () {
            let vm =this;
            let errors = vm.isError();
            if(!errors && vm.isEffectiveDateValid){
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
                let formData = new FormData()
                var files = vm.$refs.filefield.files;
                // $.each(files, function (idx, v) {
                //     var file = v['file'];
                //     var filename = v['name'];
                //     var name = 'file-' + idx;
                //     formData.append(name, file, filename);
                //     formData.append('proposal_approval_document', vm.uploadedFile)
                // });
                //no need to use above loop for files as restricted to add only one approval document
                vm.uploadedFile =  files.length>0 ? files[0].file : null;
                formData.append('proposal_approval_document', vm.uploadedFile)
                formData.append('data', JSON.stringify(approval));

                vm.$http.post(helpers.add_endpoint_json(api_endpoints.conservation_status,vm.conservation_status_id+'/final_approval'),formData,{
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
        validateEffectiveFromDate: function(event){
            let vm = this;
            const value = event.target.value;
            if(!value){
                vm.showstartDateError = true;
            }
            else{
                vm.showstartDateError = false;
            }
        },
        validateEffectiveToDate: function(event){
            let vm = this;
            const value = event.target.value;
            if(!value){
                vm.showtoDateError = true;
            }
            else{
                vm.showtoDateError = false;
            }
        },
        validateDetails: function(event){
            let vm = this;
            const value = event.target.value;
            if(!value){
                vm.showDetailsError = true;
            }
            else{
                vm.showDetailsError = false;
            }
        },        
        isError: function () {
            let vm = this;
            let hasError = false;
            if(!vm.approval.effective_from_date){
                vm.showstartDateError = true;
                hasError = true;
            }
            if(!vm.approval.effective_to_date){
                vm.showtoDateError = true;
                hasError = true;
            }
            if(!vm.approval.details || vm.approval.details == ""){
                vm.showDetailsError = true;
                hasError = true;
            }
            return hasError;
        },
       eventListeners:function () {
            let vm = this;
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