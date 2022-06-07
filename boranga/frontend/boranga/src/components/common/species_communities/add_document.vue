<template lang="html">
    <div id="document_detail">
        <modal transition="modal fade" @ok="ok()" @cancel="cancel()" :title="title" large>
            <div class="container-fluid">
                <div class="row">
                    <form class="form-horizontal" name="documentForm">
                        <alert :show.sync="showError" type="danger"><strong>{{errorString}}</strong></alert>
                        <div class="col-sm-12">
                            <div class="form-group">
                                <div class="row modal-input-row">
                                    <div class="col-sm-3">
                                      <label class="control-label pull-left">Document Category</label>
                                    </div>
                                    <div class="col-sm-9">
                                      <select class="form-control" v-model="speciesDocument.document_category">
                                        <option  v-for="category in documentCategories" :value="category.id" v-bind:key="category.id">
                                          {{ category.name }} 
                                        </option>
                                      </select>
                                    </div>
                                </div>
                                <div class="row">
                                    <div class="col-sm-3">
                                      <label class="control-label pull-left">Description</label>
                                    </div>
                                    <div class="col-sm-9">
                                      <textarea class="form-control" v-model="speciesDocument.description">
                                      </textarea>                                
                                    </div>
                                </div>
                                <div class="row">
                                    <div class="col-sm-9">
                                        <div class="input-group date" ref="add_attachments" style="width: 70%;">
                                            <FileField2 ref="filefield" 
                                            :proposal_id="document_id" 
                                            :uploaded_documents="uploaded_document"
                                            :isRepeatable="false" 
                                            name="documents_file" 
                                            @refreshFromResponse="refreshFromResponse"/>
                                        </div>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </form>
                </div>
            </div>
            <div slot="footer">
                <template v-if="document_id">
                    <button type="button" v-if="updatingDocument" disabled class="btn btn-default" @click="ok"><i class="fa fa-spinnner fa-spin"></i> Updating</button>
                    <button type="button" v-else class="btn btn-default" @click="ok">Update</button>
                </template>
                <template v-else>
                    <button type="button" v-if="addingDocument" disabled class="btn btn-default" @click="ok"><i class="fa fa-spinner fa-spin"></i> Adding</button>
                    <button type="button" v-else class="btn btn-default" @click="ok">Add</button>
                </template>
                <button type="button" class="btn btn-default" @click="cancel">Cancel</button>
            </div>
        </modal>
    </div>
</template>

<script>
//import $ from 'jquery'
//import FileField from '@/components/forms/file.vue'
import Vue from 'vue'
import FileField2 from '@/components/forms/filefield2.vue'
import modal from '@vue-utils/bootstrap-modal.vue'
import alert from '@vue-utils/alert.vue'
import {helpers,api_endpoints} from "@/utils/hooks.js"
export default {
    name:'Document-Detail',
    components:{
        FileField2,
        modal,
        alert
    },
    props:{
        document_id: {
            type: String,
            required: true
        },
        document_action:{
            type: String,
            required: true
        },
    },
    data:function () {
        let vm = this;
        return {
            isModalOpen:false,
            form:null,
            speciesDocument: Object,
            uploaded_document: [],
            /*speciesDocument: {
                id: '',
                species_id: vm.species_community_id,
                input_name: 'species_doc',
                description: '',
                document_category: '',
            },*/
            documentCategories: [],
            addingDocument: false,
            updatingDocument: false,
            validation_form: null,
            type: '1',
            errors: false,
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
            validDate: false,
        }
    },
    computed: {
        showError: function() {
            var vm = this;
            return vm.errors;
        },
        delete_url: function() {
            //return (this.requirement.id) ? '/api/proposal_requirements/'+this.requirement.id+'/delete_document/' : '';
        },
        title: function(){
            return this.document_action == 'add' ? 'Add a new Document' : 'Edit a Document';
        },

    },
    watch: {

    },
    methods:{
        refreshFromResponse: function(updated_docs){
            //this.speciesDocument= updated_docs;
        },
        /*initialiseRequirement: function(){
            this.requirement = {
                due_date: '',
                standard: true,
                recurrence: false,
                recurrence_pattern: '1',
                proposal: vm.proposal_id,
                referral_group:vm.referral_group
            }
        },*/
        ok:function () {
            let vm =this;
            if($(vm.form).valid()){
                vm.sendData();
                vm.$refs.filefield.reset_files();
            }
        },
        cancel:function () {
            this.close()
            this.$refs.filefield.reset_files();
        },
        close:function () {
            this.isModalOpen = false;
            this.speciesDocument = {};
            this.$refs.filefield.files = [{file:null, name:''}];
            this.$refs.filefield.reset_files();
            this.errors = false;
            $('.has-error').removeClass('has-error');
            //this.documentForm.resetForm();
        },
        fetchSpeciesDocument: function(vid) {
            let vm=this;
            Vue.http.get(helpers.add_endpoint_json(api_endpoints.species_documents,vid)).then((res) => {
                      vm.speciesDocument=res.body; 
                      vm.uploaded_document = [res.body];
                      
                },
              err => { 
                        console.log(err);
                  });
        },
        sendData:function(){
            let vm = this;
            vm.errors = false;
            let speciesDocument = JSON.parse(JSON.stringify(vm.speciesDocument));
            let formData = new FormData()

            // Add files to formData
            var files = vm.$refs.filefield.files;
            $.each(files, function (idx, v) {
                var file = v['file'];
                var filename = v['name'];
                var name = 'file-' + idx;
                formData.append(name, file, filename);
            });
            speciesDocument.num_files = files.length;
            //speciesDocument.input_name = 'species_doc';
            //speciesDocument.species_id = vm.species_community_id;

            if (vm.speciesDocument.id){
                console.log(vm.speciesDocument.id+"update")
                vm.updatingDocument = true;
                //vm.$http.put(helpers.add_endpoint_json(api_endpoints.proposal_requirements,requirement.id),JSON.stringify(requirement),{
                //requirement.update = true;
                formData.append('data', JSON.stringify(speciesDocument));
                vm.$http.put(helpers.add_endpoint_json(api_endpoints.species_documents,speciesDocument.id), formData,{
                        emulateJSON:true,
                    }).then((response)=>{
                        vm.updatingDocument = false;
                        vm.$parent.updatedDocuments();
                        vm.close();
                    },(error)=>{
                        vm.errors = true;
                        vm.errorString = helpers.apiVueResourceError(error);
                        vm.updatingDocument = false;
                    });
            } else {
                console.log(vm.speciesDocument.id+"add")
                vm.addingDocument = true;
                //vm.$http.post(api_endpoints.proposal_requirements,JSON.stringify(requirement),{
                //requirement.update = false;
                formData.append('data', JSON.stringify(speciesDocument));
                vm.$http.post(api_endpoints.species_documents, formData,{
                        emulateJSON:true,
                    }).then((response)=>{
                        vm.addingDocument = false;
                        vm.close();
                        vm.$parent.updatedDocuments();
                    },(error)=>{
                        vm.errors = true;
                        vm.addingDocument = false;
                        vm.errorString = helpers.apiVueResourceError(error);
                    });
            }
        },
       eventListeners:function () {
            let vm = this;
            // Initialise Date Picker
           /* $(vm.$refs.due_date).datetimepicker(vm.datepickerOptions);
            $(vm.$refs.due_date).on('dp.change', function(e){
                if ($(vm.$refs.due_date).data('DateTimePicker').date()) {
                    vm.requirement.due_date =  e.date.format('DD/MM/YYYY');
                }
                else if ($(vm.$refs.due_date).data('date') === "") {
                    vm.requirement.due_date = "";
                }
             });*/
        }
   },
   created: async function () {
        // documentCategories
        let returned_categories = await this.$http.get('/api/document_categories/document_category_choices/');
        Object.assign(this.documentCategories, returned_categories.body);
        // blank entry allows user to clear selection
        this.documentCategories.splice(0, 0, 
            {
              id: "", 
              name: "",
            });
   },
   mounted:function () {
        let vm =this;
        vm.form = document.forms.documentForm;
        this.$nextTick(()=>{
            vm.eventListeners();
        });
        //vm.speciesDocument = vm.$refs.filefield.uploaded_documents;
   }
}
</script>

<style lang="css">
    .modal-input-row {
        margin-bottom: 20px;
    }
</style>
