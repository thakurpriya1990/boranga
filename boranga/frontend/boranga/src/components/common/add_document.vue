<template lang="html">
    <div id="document_detail">
        <modal transition="modal fade" @ok="ok()" @cancel="cancel()" :title="title" large>
            <div class="container-fluid">
                <div class="row">
                    <form class="form-horizontal" name="documentForm">
                        <alert :show.sync="showError" type="danger"><strong>{{ errorString }}</strong></alert>
                        <div class="col-sm-12">
                            <div class="form-group">
                                <div class="row mb-3">
                                    <div class="col-sm-3">
                                        <label for="document_category" class="control-label">Category</label>
                                    </div>
                                    <div class="col-sm-6">
                                        <select id="document_category" ref="document_category" class="form-select"
                                            v-model="documentObj.document_category" @change="filterSubCategory($event)">
                                            <option v-for="category in documentCategories" :value="category.id"
                                                v-bind:key="category.id">
                                                {{ category.name }}
                                            </option>
                                        </select>
                                    </div>
                                </div>
                                <div v-if="documentObj.document_category" class="row mb-3">
                                    <div class="col-sm-3">
                                        <label for="document_sub_category" class="control-label">Sub Category</label>
                                    </div>
                                    <div class="col-sm-6">
                                        <select id="document_sub_category" ref="document_sub_category"
                                            class="form-select" v-model="documentObj.document_sub_category"
                                            @change="focusDescription">
                                            <option v-for="sub_category in filteredDocumentSubCategories"
                                                :value="sub_category.id" v-bind:key="sub_category.id">
                                                {{ sub_category.name }}
                                            </option>
                                        </select>
                                    </div>
                                </div>
                                <div class="row mb-3">
                                    <div class="col-sm-3">
                                        <label for="description" class="control-label">Description</label>
                                    </div>
                                    <div class="col-sm-9">
                                        <textarea id="description" ref="description" class="form-control"
                                            v-model="documentObj.description">
                                      </textarea>
                                    </div>
                                </div>
                                <div v-if="documentObj.uploaded_date" class="row mb-3">
                                    <div class="col-sm-3">
                                        <label for="uploaded_date" class="control-label">Date/Time</label>
                                    </div>
                                    <div class="col-sm-9">
                                        <input disabled type="datetime-local" class="form-control" id="uploaded_date"
                                            name="uploaded_date" ref="uploaded_date"
                                            v-model="documentObj.uploaded_date" />
                                    </div>
                                </div>
                                <div v-if="showSubmitterCanAccess" class="row mb-3">
                                    <div class="col-sm-3">
                                        <label for="can_submitter_access" class="control-label">Submitter Can Access?
                                        </label>
                                    </div>
                                    <div class="col-sm-9">
                                        <div class="form-check form-check-inline">
                                            <label for="can_submitter_access_no" class="form-check-label">No</label>
                                            <input type="radio" class="form-check-input" id="can_submitter_access_no"
                                                name="can_submitter_access" ref="can_submitter_access_no"
                                                v-model="documentObj.can_submitter_access" :value="false" />
                                        </div>
                                        <div class="form-check form-check-inline">
                                            <label for="can_submitter_access_yes" class="form-check-label">Yes</label>
                                            <input type="radio" class="form-check-input" id="can_submitter_access_yes"
                                                name="can_submitter_access" ref="can_submitter_access_yes"
                                                v-model="documentObj.can_submitter_access" :value="true" />
                                        </div>
                                    </div>
                                </div>
                                <div class="row mb-3">
                                    <label for="documents_file" class="mb-3">Document</label>
                                    <div class="col">
                                        <FileField2 ref="filefield" :proposal_id="document_id"
                                            :uploaded_documents="uploaded_document" :isRepeatable="false"
                                            id="documents_file" name="documents_file"
                                            @refreshFromResponse="refreshFromResponse" />
                                    </div>
                                </div>
                            </div>
                        </div>
                    </form>
                </div>
            </div>
            <div slot="footer">
                <button type="button" class="btn btn-secondary me-2" @click="cancel">Cancel</button>
                <template v-if="document_id">
                    <button type="button" v-if="updatingDocument" disabled class="btn btn-primary" @click="ok">
                        Updating <span class="spinner-border spinner-border-sm" role="status" aria-hidden="true"></span>
                        <span class="visually-hidden">Loading...</span></button>
                    <button type="button" v-else class="btn btn-primary" @click="ok">Update</button>
                </template>
                <template v-else>
                    <button type="button" v-if="addingDocument" disabled class="btn btn-primary" @click="ok">Adding
                        <span class="spinner-border spinner-border-sm" role="status" aria-hidden="true"></span>
                        <span class="visually-hidden">Loading...</span></button>
                    <button type="button" v-else class="btn btn-primary" @click="ok">Add Document</button>
                </template>
            </div>
        </modal>
    </div>
</template>

<script>
import FileField2 from '@/components/forms/filefield2.vue'
import modal from '@vue-utils/bootstrap-modal.vue'
import alert from '@vue-utils/alert.vue'
import { helpers, api_endpoints } from "@/utils/hooks.js"
export default {
    name: 'Document-Detail',
    components: {
        FileField2,
        modal,
        alert
    },
    props: {
        url: {
            type: String,
            required: true
        },
        is_internal: {
            type: Boolean,
            default: false
        },
    },
    data: function () {
        let vm = this;
        return {
            isModalOpen: false,
            form: null,
            document_id: String,
            document_action: String,
            documentObj: Object,
            uploaded_document: [],
            documentCategories: [],
            documentSubCategories: [],
            filteredDocumentSubCategories: [],
            addingDocument: false,
            updatingDocument: false,
            validation_form: null,
            type: '1',
            errors: false,
            errorString: '',
            successString: '',
            success: false,
            validDate: false,
            title: null,
        }
    },
    watch: {
        isModalOpen: function (val) {
            if (val) {
                this.$nextTick(() => {
                    this.$refs.document_category.focus();
                });
            }
        },
    },
    computed: {
        showError: function () {
            var vm = this;
            return vm.errors;
        },
        showSubmitterCanAccess: function () {
            return this.is_internal && Object.hasOwn(this.documentObj, 'can_submitter_access');
        }
    },
    methods: {
        focusDescription: function () {
            this.$nextTick(() => {
                this.$refs['description'].focus();
            });
        },
        refreshFromResponse: function (updated_docs) {
            //this.documentObj= updated_docs; TODO: This is being referenced. It should do something or be removed.
        },
        filterSubCategory: function (event) {
            this.$nextTick(() => {
                if (event) {
                    this.documentObj.document_sub_category = null; //-----to remove the previous selection
                }
                this.filteredDocumentSubCategories = [];
                this.filteredDocumentSubCategories = [{
                    id: null,
                    name: "",
                    category_id: null,
                }];
                //---filter sub categories as per category selected
                for (let choice of this.documentSubCategories) {
                    if (choice.category_id === this.documentObj.document_category) {
                        this.filteredDocumentSubCategories.push(choice);
                    }
                }
                if (this.$refs['document_sub_category']) {
                    this.$refs['document_sub_category'].focus();
                }
            });
        },
        fetchSubCategory: function (category_id) {
            this.$nextTick(() => {
                this.filteredDocumentSubCategories = [];
                this.filteredDocumentSubCategories = [{
                    id: null,
                    name: "",
                    category_id: null,
                }];
                //---filter sub categories as per category selected
                for (let choice of this.documentSubCategories) {
                    if (choice.category_id === category_id) {
                        this.filteredDocumentSubCategories.push(choice);
                    }
                }
            });
        },
        ok: function () {
            let vm = this;
            if ($(vm.form).valid()) {
                vm.sendData();
                vm.$refs.filefield.reset_files();
            }
        },
        cancel: function () {
            this.close()
            this.$refs.filefield.reset_files();
        },
        close: function () {
            this.isModalOpen = false;
            this.documentObj = {};
            this.$refs.filefield.files = [{ file: null, name: '' }];
            this.$refs.filefield.reset_files();
            this.errors = false;
            $('.has-error').removeClass('has-error');
        },
        sendData: function () {
            let vm = this;
            vm.errors = false;
            let documentObj = JSON.parse(JSON.stringify(vm.documentObj));
            let formData = new FormData()

            // Add files to formData
            var files = vm.$refs.filefield.files;
            $.each(files, function (idx, v) {
                var file = v['file'];
                var filename = v['name'];
                var name = 'file-' + idx;
                formData.append(name, file, filename);
            });
            documentObj.num_files = files.length;

            if (vm.documentObj.id) {
                vm.updatingDocument = true;
                formData.append('data', JSON.stringify(documentObj));
                vm.$http.put(helpers.add_endpoint_json(vm.url, documentObj.id), formData, {
                    emulateJSON: true,
                }).then((response) => {
                    vm.updatingDocument = false;
                    vm.$parent.updatedDocuments();
                    vm.close();
                }, (error) => {
                    vm.errors = true;
                    vm.errorString = helpers.apiVueResourceError(error);
                    vm.updatingDocument = false;
                });
            } else {
                vm.addingDocument = true;
                formData.append('data', JSON.stringify(documentObj));
                vm.$http.post(vm.url, formData, {
                    emulateJSON: true,
                }).then((response) => {
                    vm.addingDocument = false;
                    vm.close();
                    vm.$parent.updatedDocuments();
                }, (error) => {
                    vm.errors = true;
                    vm.addingDocument = false;
                    vm.errorString = helpers.apiVueResourceError(error);
                });
            }
        },
        eventListeners: function () {
            let vm = this;
        }
    },
    created: async function () {
        this.$http.get(api_endpoints.document_categories_dict).then(response => {
            let document_dict = response.body;
            this.documentCategories = document_dict.document_category_list;
            // blank entry allows user to clear selection
            this.documentCategories.splice(0, 0,
                {
                    id: "",
                    name: "",
                });
            // documentSubCategories
            this.documentSubCategories = document_dict.document_sub_category_list;
            this.filterSubCategory();
        }, (error) => {
            console.log(error);
        })
    },
    mounted: function () {
        let vm = this;
        vm.form = document.forms.documentForm;
        this.$nextTick(() => {
            vm.eventListeners();
        });
    }
}
</script>
