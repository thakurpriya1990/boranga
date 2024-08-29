<template>
    <div class="container gx-4" id="occurence-report-bulk-import-schema">
        <div v-if="schema" class="row mb-2">
            <div class="col">
                <div class="mb-4">
                    <h2 class="text-capitalize">Occurrence Report Bulk Import Schema</h2>
                </div>
                <div class="mb-3">
                    <alert type="primary">
                        <i class="bi bi-info-circle-fill text-primary fs-4 help-text-popover me-2"></i>
                        Some help text about defining a bulk import schema
                    </alert>
                </div>
                <div class="mb-3">
                    <div class="card">
                        <div class="card-body">
                            <div class="mb-1">
                                <div class="container mb-0 pb-2">
                                    <div class="row">
                                        <div class="col-6">
                                            <h4 class="text-capitalize">{{ schema.group_type_display }} Bulk Import
                                                Schema <span class="badge bg-secondary ms-3">Version: {{ schema.version
                                                    }}</span></h4>
                                        </div>
                                        <div class="col-6 d-flex justify-content-end">
                                            <input type="text" class="form-control w-25 me-3" placeholder="Add tag"
                                                @keydown="addTag" />
                                            <button role="button" class="btn btn-primary me-2"
                                                @click.prevent="validateSchema()"><i
                                                    class="bi bi-card-checklist me-1"></i> Validate Schema</button>
                                            <a role="button" class="btn btn-primary"
                                                :href="`http://internalhost:9060/api/occurrence_report_bulk_import_schemas/${schema.id}/preview_import_file/`"><i
                                                    class="bi bi-filetype-xlsx me-1"></i> Preview .xlsx File</a>
                                        </div>
                                    </div>
                                </div>
                            </div>
                            <div class="border-bottom mb-3">
                                <div class="container mb-1 pb-3">
                                    <div class="row">
                                        <label for="schema-name" class="col-sm-1 col-form-label">Name</label>
                                        <div class="col-sm-4">
                                            <input type="text" class="form-control" id="schema-name" ref="schema-name"
                                                v-model="schema.name" aria-describedby="schema-name-help"
                                                placeholder="Enter Schema Name" autofocus>
                                        </div>
                                        <label for="schema-tags" class="col-sm-1 col-form-label">Tags</label>
                                        <div class="col-sm-6 d-flex align-items-center">
                                            <template v-if="schema.tags && schema.tags.length > 0">
                                                <span class="badge bg-info fs-6 me-2"
                                                    v-for="(tag, index) in schema.tags" :key="tag">{{ tag }}<i
                                                        class="bi bi-x-circle-fill ps-2" role="button"
                                                        @click="removeTag(index)"></i></span>
                                            </template>
                                            <template v-else>
                                                <span class="text-muted">No tags added</span>
                                            </template>
                                        </div>
                                    </div>
                                </div>
                            </div>
                            <div class="mb-3">
                                <div class="container">
                                    <div class="row">
                                        <div class="col-4">
                                            <div class="card">
                                                <div class="card-body">
                                                    <h5 class="card-title border-bottom pb-3 mb-3">
                                                        <i class="bi bi-filetype-xlsx text-success me-3"></i>Columns
                                                        <span class="text-muted ms-2 fs-6">(.xlsx)</span>
                                                    </h5>
                                                    <div class="">
                                                        <table class="table table-bordered table-hover table-sm">
                                                            <tbody>
                                                                <tr v-for="(column, index) in schema.columns"
                                                                    :class="selectedColumn == column ? 'active' : ''"
                                                                    @click="selectColumn(column)" role="button">
                                                                    <th style="width:5%" class="text-center">{{ index +
                                                                        1 }}
                                                                    </th>
                                                                    <th class="ps-3" style="width:40%">{{
                                                                        column.xlsx_column_header_name }}
                                                                        <span class="text-danger"
                                                                            title="Mandatory Column"
                                                                            v-if="column.xlsx_data_validation_allow_blank == false">*</span>
                                                                    </th>
                                                                    <td class="text-muted text-center"
                                                                        style="width:10%">
                                                                        <i class="bi bi-eye-fill" role="button"></i>
                                                                    </td>
                                                                </tr>
                                                                <tr class="border-bottom-0"
                                                                    :class="schema.columns.length == 0 ? 'border-top-0' : ''"
                                                                    @click.prevent="addNewColumn" role="button">
                                                                    <th class="border-0 ps-3 pt-2 text-muted"
                                                                        colspan="2">Add <template
                                                                            v-if="schema.columns.length == 0">a</template><template
                                                                            v-else>Another</template> Column</th>
                                                                    <td class="border-0 text-muted text-center pt-2"><i
                                                                            class="bi bi-plus-circle-fill text-success"
                                                                            role="button"></i>
                                                                    </td>
                                                                </tr>
                                                            </tbody>
                                                        </table>
                                                    </div>
                                                </div>
                                            </div>
                                        </div>
                                        <div class="col-8">
                                            <div v-if="addEditMode && selectedColumn" class="mb-3">
                                                <div class="card">
                                                    <div class="card-body">
                                                        <h5 class="card-title border-bottom pb-2 mb-3">
                                                            Selected Column Details
                                                        </h5>
                                                        <form @submit.prevent="" class="needs-validation" novalidate>
                                                            <div class="row d-flex align-items-center mb-2">
                                                                <label for="inputEmail3"
                                                                    class="col-sm-4 col-form-label">Django Import
                                                                    Model</label>
                                                                <div class="col-sm-8 ">
                                                                    <select class="form-select form-select-sm"
                                                                        aria-label="Group Type"
                                                                        ref="django-import-model"
                                                                        v-model="selectedColumn.django_import_content_type"
                                                                        @change="selectDjangoImportContentType">
                                                                        <option value="">Select Django Model</option>
                                                                        <option
                                                                            v-for="djangoContentType in djangoContentTypes"
                                                                            :value="djangoContentType.id">{{
                                                                                djangoContentType.model_verbose_name }}
                                                                        </option>
                                                                    </select>
                                                                </div>
                                                            </div>
                                                            <div v-if="selectedContentType"
                                                                class="row d-flex align-items-center mb-2">
                                                                <label for="inputEmail3"
                                                                    class="col-sm-4 col-form-label">Django Import
                                                                    Field</label>
                                                                <div class="col-sm-8 ">
                                                                    <select class="form-select form-select-sm"
                                                                        aria-label="Group Type"
                                                                        ref="django-import-field"
                                                                        v-model="selectedColumn.django_import_field_name"
                                                                        @change="selectDjangoImportField">
                                                                        <option value="">Select Django Model</option>
                                                                        <option
                                                                            v-for="modelField in selectedContentType.model_fields"
                                                                            :value="modelField.name">
                                                                            {{
                                                                                modelField.display_name }} ({{
                                                                                modelField.type }})
                                                                        </option>
                                                                    </select>
                                                                </div>
                                                            </div>
                                                            <template v-if="selectedField">
                                                                <div class="row d-flex align-items-center mb-2">
                                                                    <label for="inputEmail3"
                                                                        class="col-sm-4 col-form-label">Column
                                                                        Name</label>
                                                                    <div class="col-sm-8 ">
                                                                        <div class="input-group input-group-sm">
                                                                            <input type="text" class="form-control"
                                                                                name="column-name" id="column-name"
                                                                                ref="column-name"
                                                                                aria-describedby="helpId" placeholder=""
                                                                                v-model="selectedColumn.xlsx_column_header_name" />
                                                                        </div>
                                                                    </div>
                                                                </div>
                                                                <div class="row d-flex align-items-center mb-2">
                                                                    <label for="inputEmail3"
                                                                        class="col-sm-4 col-form-label">Django
                                                                        Field
                                                                        Type</label>
                                                                    <div class="col-sm-8 ">
                                                                        <div class="input-group input-group-sm">
                                                                            <input type="text" class="form-control"
                                                                                name="" id="" aria-describedby="helpId"
                                                                                placeholder="" disabled
                                                                                :value="selectedField.type" />
                                                                        </div>
                                                                    </div>
                                                                </div>
                                                                <div class="row d-flex align-items-center mb-2">
                                                                    <label for="inputEmail3"
                                                                        class="col-sm-4 col-form-label">Excel
                                                                        Validation
                                                                        Type</label>
                                                                    <div class="col-sm-8 ">
                                                                        <div class="input-group input-group-sm">
                                                                            <input type="text"
                                                                                class="form-control form-control-sm"
                                                                                name="" id="" aria-describedby="helpId"
                                                                                placeholder="" disabled
                                                                                :value="selectedField.xlsx_validation_type ? selectedField.xlsx_validation_type : 'None'" />
                                                                            <template
                                                                                v-if="selectedField.xlsx_validation_type == 'date'">
                                                                                <span class="input-group-text"
                                                                                    id="datetime-format">Format:</span>
                                                                                <span class="input-group-text"
                                                                                    id="datetime-format-mask">DD/MM/YYYY
                                                                                    HH:MM:SS</span>
                                                                            </template>
                                                                            <template
                                                                                v-if="selectedField.xlsx_validation_type == 'list' && selectedField.choices && selectedField.choices.length > 0">
                                                                                <button class="btn btn-primary"
                                                                                    data-bs-toggle="modal"
                                                                                    data-bs-target="#preview-choices"><i
                                                                                        class="bi bi-search"
                                                                                        role="button"></i> Preview
                                                                                    List Choices</button>
                                                                                <div class="modal fade"
                                                                                    id="preview-choices"
                                                                                    data-bs-backdrop="static"
                                                                                    data-bs-keyboard="false"
                                                                                    tabindex="-1"
                                                                                    aria-labelledby="preview-choices-label"
                                                                                    aria-hidden="true">
                                                                                    <div class="modal-dialog">
                                                                                        <div class="modal-content">
                                                                                            <div class="modal-header">
                                                                                                <h5 class="modal-title"
                                                                                                    id="preview-choices-label">
                                                                                                    {{
                                                                                                        selectedField.display_name
                                                                                                    }} List
                                                                                                    Choices
                                                                                                </h5>
                                                                                                <button type="button"
                                                                                                    class="btn-close"
                                                                                                    data-bs-dismiss="modal"
                                                                                                    aria-label="Close"></button>
                                                                                            </div>
                                                                                            <div class="modal-body">
                                                                                                <div
                                                                                                    class="table-responsive">
                                                                                                    <table
                                                                                                        class="table table-bordered table-hover table-sm">
                                                                                                        <tbody>
                                                                                                            <tr v-for="choice in selectedField.choices"
                                                                                                                class="">
                                                                                                                <td>{{
                                                                                                                    choice[0]
                                                                                                                }}
                                                                                                                </td>
                                                                                                            </tr>
                                                                                                        </tbody>
                                                                                                    </table>
                                                                                                </div>
                                                                                            </div>
                                                                                            <div class="modal-footer">
                                                                                                <button type="button"
                                                                                                    class="btn btn-secondary"
                                                                                                    data-bs-dismiss="modal">Close</button>
                                                                                            </div>
                                                                                        </div>
                                                                                    </div>
                                                                                </div>
                                                                            </template>
                                                                        </div>
                                                                    </div>
                                                                </div>
                                                                <div v-if="selectedField.xlsx_validation_type"
                                                                    class="row mb-2">
                                                                    <label for="inputEmail3"
                                                                        class="col-sm-4 col-form-label">Excel Data
                                                                        Validations<i
                                                                            id="pre-import-validation-help-text"
                                                                            class="bi bi-info-circle-fill text-primary ms-2"
                                                                            data-bs-toggle="popover"
                                                                            data-bs-trigger="hover focus"
                                                                            data-bs-content="Basic validations embedded in the .xlsx file"
                                                                            data-bs-placement="top"></i></label>
                                                                    <div class="col-sm-4">
                                                                        <div class="input-group input-group-sm mb-2">
                                                                            <span class="input-group-text"
                                                                                id="allow-blank-label">Allow
                                                                                Blank</span>
                                                                            <select class="form-select w-50"
                                                                                aria-label="Allow Blank"
                                                                                aria-describedby="allow-blank-label"
                                                                                :disabled="!selectedField.allow_null"
                                                                                v-model="selectedColumn.xlsx_data_validation_allow_blank">
                                                                                <option :value="true">Yes</option>
                                                                                <option :value="false">No</option>
                                                                            </select>
                                                                        </div>
                                                                        <div class="input-group input-group-sm mb-2">
                                                                            <span class="input-group-text"
                                                                                id="basic-addon1">Max
                                                                                Length</span>
                                                                            <input type="text" class="form-control"
                                                                                aria-label="Max Length"
                                                                                aria-describedby="basic-addon1"
                                                                                :value="selectedField.max_length ? selectedField.max_length : 'N/A'"
                                                                                disabled>
                                                                        </div>
                                                                    </div>
                                                                </div>
                                                            </template>
                                                            <div v-if="showValidationFields" class="row mb-2">
                                                                <label for="inputEmail3"
                                                                    class="col-sm-4 col-form-label">Django
                                                                    Validations<i id="pre-import-validation-help-text"
                                                                        class="bi bi-info-circle-fill text-primary ms-2"
                                                                        data-bs-toggle="popover"
                                                                        data-bs-trigger="hover focus"
                                                                        data-bs-content="More advanced validation that occurs during the import process"
                                                                        data-bs-placement="top"></i></label>
                                                                <div class="col-sm-8">
                                                                    <fieldset class="border p-2 mb-2">
                                                                        <div class="input-group input-group-sm mb-2">
                                                                            <span class="input-group-text w-25"
                                                                                id="type">
                                                                                Type</span>
                                                                            <input type="text" disabled
                                                                                class="form-control"
                                                                                placeholder="Username"
                                                                                aria-label="Username"
                                                                                aria-describedby="lookup-model"
                                                                                value="Django Foreign Key Lookup">
                                                                        </div>
                                                                        <div class="input-group input-group-sm mb-2">
                                                                            <span class="input-group-text w-25"
                                                                                id="lookup-model">
                                                                                Lookup Model</span>
                                                                            <input type="text" disabled
                                                                                class="form-control"
                                                                                placeholder="Username"
                                                                                aria-label="Username"
                                                                                aria-describedby="lookup-model"
                                                                                value="Species">
                                                                        </div>
                                                                        <div class="input-group input-group-sm mb-1">
                                                                            <span class="input-group-text w-25"
                                                                                id="lookup-field">
                                                                                Lookup Field</span>
                                                                            <select class="form-select"
                                                                                aria-label="Group Type">
                                                                                <option :value="null">Select a Lookup
                                                                                    Field</option>
                                                                            </select>
                                                                        </div>
                                                                    </fieldset>
                                                                </div>
                                                            </div>
                                                            <div class="border-top pt-3 d-flex justify-content-end">
                                                                <button class="btn btn-primary btn-sm me-2"
                                                                    @click.prevent="save()"><i
                                                                        class="bi bi-floppy-fill me-1"></i> Save
                                                                    Column <template v-if="saving"><span
                                                                            class="spinner-border spinner-border-sm ms-2"
                                                                            role="status" aria-hidden="true"></span>
                                                                        <span
                                                                            class="visually-hidden">Loading...</span></template></button>
                                                                <button class="btn btn-danger btn-sm"
                                                                    v-if="!selectedColumn.id"
                                                                    @click.prevent="cancelAddingColumn(selectedColumn)"><i
                                                                        class="bi bi-x-circle-fill me-1"></i>
                                                                    Cancel
                                                                    Adding
                                                                    Column</button>
                                                                <button v-else class="btn btn-danger btn-sm"
                                                                    @click.prevent="removeColumn(selectedColumn)"><i
                                                                        class="bi bi-trash3-fill me-1"></i> Delete
                                                                    Column</button>
                                                            </div>
                                                        </form>
                                                    </div>
                                                </div>
                                            </div>
                                            <div v-else>
                                                <div class="card">
                                                    <div class="card-body">
                                                        <h5 class="card-title border-bottom pb-2 mb-3">
                                                            No Column Selected
                                                        </h5>
                                                        <div>
                                                            <alert type="info"><i
                                                                    class="bi bi-arrow-left-square-fill me-2"></i>
                                                                Select a column from the left panel
                                                                to view it's details
                                                            </alert>
                                                        </div>
                                                    </div>
                                                </div>
                                            </div>
                                        </div>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
        <div class="navbar fixed-bottom" style="background-color: rgb(245, 245, 245);">
            <div class="container">
                <div class="col-md-6">
                    <div class="col-md-6"><a role="button" class="btn btn-primary me-2 float-start"
                            href="/internal/occurrence_report/bulk_import_schema/">Return to Dashboard </a>
                    </div>
                </div>
                <div class="col-md-6 text-end"><button class="btn btn-primary me-2 float-end"
                        @click.prevent="save()">Save and
                        Continue <template v-if="saving"><span class="spinner-border spinner-border-sm ms-2"
                                role="status" aria-hidden="true"></span>
                            <span class="visually-hidden">Loading...</span></template></button><button
                        class="btn btn-primary me-2 float-end" @click.prevent="saveAndExit()">Save and Exit <template
                            v-if="saving"><span class="spinner-border spinner-border-sm ms-2" role="status"
                                aria-hidden="true"></span>
                            <span class="visually-hidden">Loading...</span>
                        </template></button></div>
            </div>
        </div>
    </div>
</template>

<script>
import alert from '@vue-utils/alert.vue'

import { api_endpoints } from "@/utils/hooks.js"

export default {
    name: 'OccurrenceReportBulkImportSchema',
    data() {
        return {
            schema: null,
            djangoContentTypes: null,
            selectedColumn: null,
            selectedColumnIndex: null,
            selectedContentType: null,
            selectedField: null,
            addEditMode: false,
            newColumn: null,
            saving: false,
        }
    },
    components: {
        alert
    },
    computed: {
        showValidationFields() {
            return this.selectedColumn &&
                this.selectedColumn.xlsx_column_header_name &&
                this.selectedColumn.django_import_content_type &&
                this.selectedColumn.django_import_field_name && this.selectedField && this.selectedField.type === 'ForeignKey';
        },
    },
    methods: {
        fetchBulkImportSchema() {
            this.$http.get(`${api_endpoints.occurrence_report_bulk_import_schemas}${this.$route.params.bulk_import_schema_id}/`)
                .then(response => {
                    this.schema = response.data
                })
                .catch(error => {
                    console.error(error)
                })
        },
        fetchContentTypes() {
            this.$http.get(`${api_endpoints.content_types}`, {
                params: {
                    app_label: 'boranga',
                    search: 'occurrencereport'
                }
            })
                .then(response => {
                    this.djangoContentTypes = response.data.results
                    this.$http.get(`${api_endpoints.content_types}`, {
                        params: {
                            app_label: 'boranga',
                            search: 'ocr'
                        }
                    })
                        .then(response => {
                            this.djangoContentTypes.push(...response.data.results)
                            // this.removeAlreadySelectedFields();
                        })
                        .catch(error => {
                            console.error(error)
                        })
                })
                .catch(error => {
                    console.error(error)
                })
        },
        removeAlreadySelectedFields() {
            this.schema.columns.forEach(column => {
                this.djangoContentTypes.forEach(djangoContentType => {
                    if (column.django_import_content_type == djangoContentType.id) {
                        djangoContentType.model_fields = djangoContentType.model_fields.filter(
                            modelField => modelField.name !== column.django_import_field_name
                        )
                    }
                })
            })
        },
        selectDjangoImportContentType() {
            if (!this.selectedColumn.django_import_content_type) {
                this.selectedField = null
                this.selectedContentType = null
                this.$refs['django-import-field'].focus()
                return
            }
            this.selectedContentType = this.djangoContentTypes.filter(
                djangoContentType => djangoContentType.id == this.selectedColumn.django_import_content_type
            )[0]
            this.$nextTick(() => {
                this.enablePopovers();
                this.$refs['django-import-field'].focus()
            })
        },
        selectDjangoImportField() {
            if (!this.selectedColumn.django_import_field_name) {
                this.selectedField = null
                this.$refs['django-import-field'].focus()
                return
            }
            this.selectedField = this.selectedContentType.model_fields.filter(
                modelField => modelField.name == this.selectedColumn.django_import_field_name
            )[0]
            this.$nextTick(() => {
                this.enablePopovers();
                if (!this.selectedColumn.id) {
                    this.selectedColumn.xlsx_column_header_name = this.selectedField.display_name
                    this.selectedColumn.xlsx_data_validation_allow_blank = this.selectedField.allow_null
                }
                this.$refs['column-name'].focus()
            })
        },
        getNewColumnData() {
            return {
                id: null,
                schema: this.schema.id,
                django_import_content_type: '',
                django_import_field_name: '',
                xlsx_column_header_name: '',
                xlsx_data_validation_allow_blank: true,
                import_validations: []
            }
        },
        addNewColumn() {
            this.newColumn = Object.assign({}, this.getNewColumnData())
            this.schema.columns.push(this.newColumn)
            this.selectedContentType = null;
            this.selectedField = null;
            this.selectedColumn = this.newColumn
            this.selectedColumnIndex = this.schema.columns.indexOf(this.newColumn)
            this.addEditMode = true
            this.$nextTick(() => {
                this.enablePopovers();
                this.$refs['django-import-model'].focus()
            })
        },
        selectColumn(column) {
            this.selectedColumn = column
            this.selectedColumnIndex = this.schema.columns.indexOf(column)
            this.addEditMode = true
            this.$nextTick(() => {
                this.enablePopovers();
                if (this.selectedColumn.django_import_content_type) {
                    this.selectedContentType = this.djangoContentTypes.filter(
                        djangoContentType => djangoContentType.id == this.selectedColumn.django_import_content_type
                    )[0]
                    if (this.selectedColumn.django_import_field_name) {
                        this.selectedField = this.selectedContentType.model_fields.filter(
                            modelField => modelField.name == this.selectedColumn.django_import_field_name
                        )[0]
                    }
                }
                this.$refs['django-import-model'].focus()
            })
        },
        cancelAddingColumn(column) {
            this.schema.columns = this.schema.columns.filter(col => col !== column)
            this.selectedColumn = null
            this.selectedColumnIndex = null
            this.addEditMode = false
        },
        removeColumn(column) {
            let columnTitle = column.xlsx_column_header_name ? `Are you sure you want to delete column: ${column.xlsx_column_header_name}?` : `Are you sure you want to delete this column?`
            swal.fire({
                title: `Delete Column ${column.xlsx_column_header_name}`,
                text: columnTitle,
                icon: 'question',
                showCancelButton: true,
                confirmButtonText: 'Confirm Delete',
                cancelButtonText: 'Cancel',
                customClass: {
                    confirmButton: 'btn btn-primary',
                    cancelButton: 'btn btn-secondary me-2'
                },
                reverseButtons: true
            }).then((result) => {
                if (result.isConfirmed) {
                    this.schema.columns = this.schema.columns.filter(column => column !== this.selectedColumn)
                    this.selectedColumn = null
                    this.addEditMode = false

                    if (column.id) {
                        this.save()
                    }
                    this.fetchContentTypes();
                } else {
                    if (this.selectedColumn) {
                        this.$refs['django-import-model'].focus()
                    }
                }
            })
        },
        addTag(event) {
            if (event.key === 'Enter') {
                if(this.schema.tags.includes(event.target.value)) {
                    event.target.value = ''
                    return
                }
                this.schema.tags.push(event.target.value)
                this.save();
                event.target.value = ''
            }
        },
        removeTag(index) {
            this.schema.tags.splice(index, 1)
            this.save();
        },
        validateSchema() {
            swal.fire({
                title: 'Validate Schema',
                text: 'Not yet implemented',
                icon: 'warning',
                showCancelButton: false,
                cancelButtonText: 'Cancel',
                customClass: {
                    confirmButton: 'btn btn-primary',
                    cancelButton: 'btn btn-secondary me-2'
                },
            })
        },
        save() {
            this.saving = true;
            this.$http.put(`${api_endpoints.occurrence_report_bulk_import_schemas}${this.schema.id}/`, this.schema)
                .then(response => {
                    this.saving = false;
                    this.schema = Object.assign({}, response.data)
                    if (this.addEditMode) {
                        this.selectedColumn = this.schema.columns[this.selectedColumnIndex]
                    }
                })
                .catch(error => {
                    this.saving = false;
                    console.error(error)
                })
        },
        saveAndExit() {
            this.save()
            this.$router.push(`/internal/occurrence_report/bulk_import_schema/`)
        },
        enablePopovers() {
            // enable all bootstrap 5 popovers
            var popoverTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="popover"]'))
            popoverTriggerList.map(function (popoverTriggerEl) {
                return new bootstrap.Popover(popoverTriggerEl)
            })
        }
    },
    created() {
        this.fetchBulkImportSchema()
        this.fetchContentTypes()
    },
    onRouteEnter() {
        this.fetchBulkImportSchema()
        this.fetchContentTypes()
    }
}
</script>

<style scoped>
div.scroll {
    margin: 4px, 4px;
    padding: 4px;
    width: 100%;
    overflow-x: auto;
    overflow-y: hidden;
    white-space: nowrap;
}

tr.active {
    background: rgba(51, 170, 51, .4)
}
</style>
