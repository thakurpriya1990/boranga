<template lang="html">
    <div class="border p-3">
        <div v-if="has_uploaded_docs">
            <div class="row">
                <div class="col-sm-6">
                    <label class="control-label pull-left" for="Name">Uploaded Documents</label>
                </div>
                <div class="col-sm-6">
                    <div class="input-group date" ref="due_date" style="width: 70%;">
                        <div v-for="v in uploaded_documents" class="row">
                            <span>
                                <a :href="v._file" target="_blank">{{ v.name }}</a> &nbsp;
                                <a @click="delete_document(v)" class="fa fa-trash-o" title="Remove file"
                                    :filename="v.name" style="cursor: pointer; color:red;"></a>
                            </span>
                        </div>
                    </div>
                </div>
            </div>
        </div>
        <div>
            <div class="row">
                <div class="col-sm-12">
                    <div v-for="n in repeat">
                        <div v-if="isRepeatable || (!isRepeatable && num_documents() == 0)">
                            <span class="btn btn-primary btn-file">
                                <i class="bi bi-file-earmark-arrow-up me-1"></i>
                                <input :name="name" type="file" :data-que="n" :accept="fileTypes"
                                    @change="handleChange($event)" :required="isRequired" />
                                <template v-if="isRepeatable">
                                    Attach <template v-if="isRepeatable && files && files.length > 0">Another
                                    </template>Document
                                </template>
                                <template v-else>
                                    <template v-if="files && files.length > 0">
                                        Replace Document
                                    </template>
                                    <template v-else>
                                        Attach Document
                                    </template>
                                </template>
                            </span>
                        </div>
                    </div>
                </div>
            </div>
        </div>
        <div v-if="files && files.length > 0" class="mt-3 pt-3 border-top">
            <div class="mt-3">
                <ul class="list-group" :class="isRepeatable ? 'list-group-numbered' : ''">
                    <li v-for="v in files" class="list-group-item">
                        <i class="bi bi-file-earmark-text-fill text-secondary"></i> {{ v.name }} &nbsp;
                        <a @click="pop_file(v)" class="bi bi-trash" title="Remove file" :filename="v.name"
                            style="cursor: pointer; color:red;"></a>
                    </li>
                </ul>
            </div>
        </div>
        <span v-if="show_spinner"><span class="spinner-border spinner-border-sm" role="status"
                aria-hidden="true"></span>
            <span class="visually-hidden">Loading...</span></span>
    </div>
</template>

<script>
import {
    helpers
}
    from '@/utils/hooks'

export default {
    props: {
        proposal_id: null,
        required_doc_id: null,
        name: String,
        label: String,
        id: String,
        isRequired: String,
        value: {
            default: function () {
                return null;
            }
        },
        fileTypesOrig: {
            default: function () {
                var file_types =
                    "image/*," +
                    "video/*," +
                    "audio/*," +
                    "application/pdf,text/csv,application/msword,application/vnd.ms-excel,application/x-msaccess," +
                    "application/x-7z-compressed,application/x-bzip,application/x-bzip2,application/zip," +
                    ".dbf,.gdb,.gpx,.prj,.shp,.shx," +
                    ".json,.kml,.gpx";
                return file_types;
            }
        },
        fileTypes: {
            default: function () {
                return [
                    "image/*",
                    "video/*",
                    "audio/*",
                    "application/pdf",
                    "text/csv",
                    "application/msword",
                    "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
                    "application/vnd.ms-excel",
                    "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                    "application/x-msaccess",
                    "application/x-7z-compressed",
                    "application/x-bzip",
                    "application/x-bzip2",
                    "application/zip",
                    ".dbf",
                    ".gdb",
                    ".gpx",
                    ".prj",
                    ".shp",
                    ".shx",
                    ".json",
                    ".kml",
                    ".gpx"
                ].join(',');
            }
        },

        isRepeatable: Boolean,
        readonly: Boolean,
        delete_url: String,
        uploaded_documents: Array,
    },
    components: {},
    data: function () {
        return {
            repeat: 1,
            files: [],
            _files: [
                {
                    'file': null,
                    'name': ''
                }
            ],
            showingComment: false,
            show_spinner: false,
            documents: [],
            filename: null,
        }
    },
    computed: {
        csrf_token: function () {
            return helpers.getCookie('csrftoken')
        },
        has_uploaded_docs: function () {
            return this.uploaded_documents && this.uploaded_documents.length > 0;
        }
    },
    methods: {
        reset_files() {
            this.files = [];
        },
        toggleComment() {
            this.showingComment = !this.showingComment;
        },
        handleChange: function (e) {
            let vm = this;
            if (vm.isRepeatable) {
                let el = $(e.target).attr('data-que');
                let avail = $('input[name=' + e.target.name + ']');

                avail = [...avail.map(id => {
                    return $(avail[id]).attr('data-que');
                })];
                avail.pop();
                if (vm.repeat == 1) {
                    vm.repeat += 1;
                } else {
                    if (avail.indexOf(el) < 0) {
                        vm.repeat += 1;
                    }
                }
                $(e.target).css({ 'display': 'none' });
                $(e.target.parentElement).css({ 'display': 'none' });//to hide <span> element btn-link
            } else {
                vm.files = [];
            }
            vm.add_file(e)
        },
        add_file(e) {
            let vm = this;
            var file_updated = false;
            for (var idx in vm.files) {
                for (var key in vm.files[idx]) {
                    var name = vm.files[idx][key];
                    if (name == e.target.files[0].name) {
                        // replace the file with new one with same name
                        vm.files[idx]['file'] = e.target.files[0];
                        file_updated = true;
                    }
                }
            }

            if (!file_updated) {
                vm.files.push({ name: e.target.files[0].name, file: e.target.files[0] });
            }
        },
        pop_file(v) {
            /* pops file from the local files array - client side (before it has been saved to the server) */
            let vm = this;
            for (var idx in vm.files) {
                for (var key in vm.files[idx]) {
                    var name = vm.files[idx][key];
                    if (name == v.name) {
                        // Remove the file from the array
                        vm.files.splice(idx, 1);
                        return;
                    }
                }
            }

            if (!file_updated) {
                vm.files.push({ name: e.target.files[0].name, file: e.target.files[0] });
            }
        },
        delete_document: function (file) {
            /* deletes, previously saved file, from the server */
            let vm = this;
            vm.show_spinner = true;
            var data = { id: file.id, name: file.name }

            swal({
                title: "Delete Document",
                text: "Are you sure you want to delete this document?",
                type: "question",
                showCancelButton: true,
                confirmButtonText: 'Delete Document',
                customClass: {
                    confirmButton: 'btn btn-primary',
                    cancelButton: 'btn btn-secondary me-2',
                },
                reverseButtons: true,
            }).then(() => {
                vm.$http.post(vm.delete_url, data, {
                    emulateJSON: true,
                }).then((response) => {
                    vm.uploaded_documents = response.body;
                    vm.$emit('refreshFromResponse', response.body);
                    vm.show_spinner = false;
                }, err => {
                    console.log(err);
                });
            }, (error) => {
            });
        },
        num_documents: function () {
            let vm = this;
            if (vm.documents) {
                return vm.documents.length;
            }
            return 0;
        },
    },
    mounted: function () {
    }
}

</script>

<style scoped lang="css">
input {
    box-shadow: none;
}

.btn-file {
    position: relative;
    overflow: hidden;
}

.btn-file input[type=file] {
    position: absolute;
    top: 0;
    right: 0;
    min-width: 100%;
    min-height: 100%;
    font-size: 100px;
    text-align: right;
    filter: alpha(opacity=0);
    opacity: 0;
    outline: none;
    background: white;
    cursor: inherit;
    display: block;
}
</style>
