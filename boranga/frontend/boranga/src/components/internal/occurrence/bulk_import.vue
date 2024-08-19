<template>
    <div class="container gx-4" id="occurence-report-bulk-import">
        <div class="row mb-2">
            <div class="col">
                <div class="mb-4">
                    <h2 class="text-capitalize">{{ title }}</h2>
                </div>
                <div class="mb-3">
                    <alert type="primary">
                        <i class="bi bi-info-circle-fill text-primary fs-4 help-text-popover me-2"></i>
                        Some information about the import process. Including a link to <a href="">an example template
                            .xlsx file</a>?
                    </alert>
                </div>
                <div class="mb-3">
                    <div class="card">
                        <div class="card-body">
                            <form id="bulk-import-form" class="needs-validation" no-validate>
                                <div class="mb-3">
                                    <label for="schema-version" class="form-label"><span class="fw-bold">Step 1:
                                        </span>Select the bulk import schema version to use:</label>
                                    <select class="form-select text-secondary w-50" id="schema-version"
                                        ref="schema-version" v-model="selected_schema_version"
                                        aria-label="Select Schema Version" @change="resetFileField">
                                        <option :value="null" selected>Select Bulk Import Schema Version</option>
                                        <option v-for="schema_version in schema_versions" :value="schema_version">{{
                                            getSchemaVersionText(schema_version) }}</option>
                                    </select>
                                </div>
                                <div v-if="selected_schema_version" class="border-top mb-3 pt-2">
                                    <label for="schema-version" class="form-label"><span class="fw-bold">Step 2:
                                        </span>Make sure your import file matches the schema:</label>
                                    <div>
                                        <table class="table table-sm table-bordered">
                                            <thead>
                                                <tr>
                                                    <th v-for="column in selected_schema_version.columns" scope="col">{{
                                                        column.xlsx_column_header_name }}</th>
                                                </tr>
                                            </thead>
                                            <tbody>
                                                <tr>
                                                    <td v-for="column in selected_schema_version.columns">{{
                                                        column.xlsx_data_validation_type ?
                                                        column.xlsx_data_validation_type : 'None' }}</td>
                                                </tr>
                                            </tbody>
                                        </table>
                                    </div>
                                    <div>
                                        <a :href="`/api/occurrence_report_bulk_import_schemas/${selected_schema_version.id}/preview_import_file/`"
                                            class="btn btn-primary" target="_blank"><i class="bi bi-filetype-xlsx"></i>
                                            Download Preview Bulk Import File</a>
                                    </div>
                                </div>
                                <div v-if="selected_schema_version" class="border-top w-75 mb-3 pt-2">
                                    <label for="bulk-import-file" class="form-label"><span class="fw-bold">Step 3:
                                        </span> Select the bulk import file (.xlsx)</label>
                                    <div class="input-group">
                                        <input type="file" class="form-control text-secondary"
                                            :class="importFileErrors ? 'is-invalid' : ''" id="bulk-import-file"
                                            ref="bulk-import-file" aria-describedby="bulk-import-button"
                                            @change="bulkImportFileSelected"
                                            accept="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet">
                                        <div v-if="importFileErrors" class="invalid-feedback">
                                            <ul>
                                                <li v-for="error in importFileErrors">{{ error }}</li>
                                            </ul>
                                        </div>
                                    </div>
                                </div>
                            </form>
                        </div>
                    </div>
                </div>
                <div v-if="queuedImports && queuedImports.length > 0" class="mb-3">
                    <div class="card">
                        <div class="card-body">
                            <h5 class="card-title text-secondary mb-3">Queued Imports</h5>
                            <div class="table-responsive">
                                <table class="table table-sm">
                                    <thead>
                                        <tr>
                                            <th scope="col"><i class="bi bi-clock text-secondary"></i> Datetime Queued
                                            </th>
                                            <th scope="col"><i class="bi bi-filetype-xlsx text-secondary"></i> File Name
                                            </th>
                                            <th scope="col"><i class="bi bi-hdd-fill text-secondary"></i> File Size</th>
                                            <th scope="col"><i class="bi bi-list-ol text-secondary"></i> Row Count</th>
                                            <th scope="col"><i class="bi bi-hourglass-split text-secondary"></i> Time
                                                Estimate</th>
                                        </tr>
                                    </thead>
                                    <tbody class="text-muted">
                                        <tr v-for="queuedImport in queuedImports" class="">
                                            <td>{{ new Date(queuedImport.datetime_queued).toLocaleString() }}</td>
                                            <td class="text-truncate" style="max-width: 350px;">{{
                                                queuedImport.file_name }}</td>
                                            <td>{{ queuedImport.file_size_megabytes }} MB</td>
                                            <td class="text-end pe-3">{{ queuedImport.rows ? queuedImport.rows : 'Not
                                                Counted' }}</td>
                                            <td>{{ queuedImport.estimated_processing_time_human_readable }}</td>
                                        </tr>
                                    </tbody>
                                </table>
                            </div>
                        </div>
                    </div>
                </div>
                <div v-if="currentlyRunningImports && currentlyRunningImports.length > 0" class="mb-3">
                    <div class="card currently-running">
                        <div class="card-body align-items-center">
                            <h5 class="card-title text-primary mb-3">Currently Running Imports
                                <span class="spinner-border spinner-border-sm me-3" role="status"
                                    aria-hidden="true"></span>
                                <span class="visually-hidden">Loading...</span>
                            </h5>
                            <div class="table-responsive">
                                <table class="table table-sm">
                                    <thead>
                                        <tr>
                                            <th scope="col"><i class="bi bi-clock text-primary"></i> Datetime Started
                                            </th>
                                            <th scope="col"><i class="bi bi-filetype-xlsx text-primary"></i> File Name
                                            </th>
                                            <th scope="col"><i class="bi bi-hdd-fill text-primary"></i> File Size</th>
                                            <th scope="col"><i class="bi bi-hourglass-split text-primary"></i> Progress
                                            </th>
                                        </tr>
                                    </thead>
                                    <tbody>
                                        <tr v-for="currentlyRunningImport in currentlyRunningImports" class="">
                                            <td>{{ new Date(currentlyRunningImport.datetime_started).toLocaleString() }}
                                            </td>
                                            <td>{{ currentlyRunningImport.file_name }}</td>
                                            <td>{{ currentlyRunningImport.file_size_megabytes }} MB</td>
                                            <td style="min-width: 200px;">
                                                <div class="progress">
                                                    <div class="progress-bar progress-bar-striped progress-bar-animated"
                                                        role="progressbar"
                                                        :style="`width: ${currentlyRunningImport.percentage_complete}%;`"
                                                        :aria-valuenow="currentlyRunningImport.percentage_complete"
                                                        aria-valuemin="0" aria-valuemax="100">{{
                                                            currentlyRunningImport.percentage_complete }}%
                                                    </div>
                                                </div>
                                            </td>
                                        </tr>
                                    </tbody>
                                </table>
                            </div>
                        </div>
                    </div>
                </div>
                <div v-if="failedImports && failedImports.length > 0" class="mb-3">
                    <div class="card border-danger">
                        <div class="card-body">
                            <h5 class="card-title text-danger mb-3"><i class="bi bi-list-checkme-2"></i>Failed Bulk
                                Imports</h5>
                            <div class="table-responsive">
                                <table class="table table-sm">
                                    <thead>
                                        <tr>
                                            <th scope="col">Datetime Started</th>
                                            <th scope="col">File Name</th>
                                            <th scope="col">File Size</th>
                                            <th scope="col">Records Imported</th>
                                            <th scope="col">Actions</th>
                                        </tr>
                                    </thead>
                                    <tbody>
                                        <tr v-for="failedImport in failedImports"
                                            :id="`failed-import-${failedImport.id}`" class="">
                                            <td>{{ new Date(failedImport.datetime_started).toLocaleString() }}</td>
                                            <td class="text-truncate" style="max-width: 350px;">{{
                                                failedImport.file_name }}</td>
                                            <td>{{ failedImport.file_size_megabytes }} MB</td>
                                            <td class="text-end pe-3">{{ failedImport.rows ? failedImport.rows :
                                                'Not Counted' }}</td>
                                            <td>
                                                <button class="btn btn-sm btn-danger me-2"
                                                    data-bs-target="#staticBackdrop" data-bs-toggle="modal"
                                                    @click="selectedErrors = failedImport.error_message"><i
                                                        class="bi bi-eye"></i>
                                                    View Errors</button>
                                                <button class="btn btn-sm btn-primary"
                                                    @click.prevent="retryBulkImportTask(failedImport.id)"><i
                                                        class="bi bi-arrow-clockwise"></i> Retry</button>
                                            </td>
                                        </tr>
                                    </tbody>
                                </table>
                            </div>
                            <p class="card-text text-center"><a href="">load more</a></p>
                        </div>
                    </div>
                    <!-- Modal -->
                    <div class="modal fade" id="staticBackdrop" data-bs-backdrop="static" data-bs-keyboard="false"
                        tabindex="-1" aria-labelledby="staticBackdropLabel" aria-hidden="true">
                        <div class="modal-dialog">
                            <div class="modal-content">
                                <div class="modal-header">
                                    <h5 class="modal-title" id="staticBackdropLabel">
                                        Bulk Import Task Errors</h5>
                                    <button type="button" class="btn-close" data-bs-dismiss="modal"
                                        aria-label="Close"></button>
                                </div>
                                <div class="modal-body">
                                    {{ selectedErrors }}
                                </div>
                                <div class="modal-footer">
                                    <button type="button" class="btn btn-secondary"
                                        data-bs-dismiss="modal">Dismiss</button>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
                <div v-if="completedImports && completedImports.length > 0" class="mb-3">
                    <div class="card border-success">
                        <div class="card-body">
                            <h5 class="card-title text-success mb-3"><i class="bi bi-list-checkme-2"></i>Completed Bulk
                                Imports</h5>
                            <div class="table-responsive">
                                <table class="table table-sm">
                                    <thead>
                                        <tr>
                                            <th scope="col"><i class="bi bi-clock-history text-success"></i> Datetime
                                                Completed</th>
                                            <th scope="col"><i class="bi bi-filetype-xlsx text-success"></i> File Name
                                            </th>
                                            <th scope="col"><i class="bi bi-list-ol text-success"></i> Records Imported
                                            </th>
                                            <th scope="col"><i class="bi bi-hourglass-bottom text-success"></i> Total
                                                Time Taken</th>
                                            <th scope="col">Actions</th>
                                        </tr>
                                    </thead>
                                    <tbody>
                                        <tr v-for="completedImport in completedImports" class="">
                                            <td>{{ new Date(completedImport.datetime_completed).toLocaleString() }}
                                            </td>
                                            <td class="text-truncate" style="max-width: 350px;">{{
                                                completedImport.file_name }}</td>
                                            <td class="">{{ completedImport.rows_processed
                                                }}</td>
                                            <td>{{ completedImport.total_time_taken_human_readable }}</td>
                                            <td>
                                                <button class="btn btn-sm btn-primary"
                                                    @click.prevent="revert(completedImport.id)"><i
                                                        class="bi bi-arrow-counterclockwise"></i> Revert &amp;
                                                    Archive</button>
                                            </td>
                                        </tr>
                                    </tbody>
                                </table>
                            </div>
                            <p class="card-text text-center"><a href="">load more</a></p>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>

<script>
import alert from '@vue-utils/alert.vue'

import { api_endpoints } from "@/utils/hooks.js"

export default {
    name: 'OccurrenceReportBulkImport',
    data() {
        return {
            form: null,
            queuedImports: null,
            currentlyRunningImports: null,
            failedImports: null,
            completedImports: null,
            timer: null,
            currentlyRunningTimer: null,
            selectedErrors: '',
            schema_versions: [],
            selected_schema_version: null,
            importFileErrors: null
        }
    },
    components: {
        alert
    },
    computed: {
        title: function () {
            return this.$route.query.group_type + ' Occurrence Report Bulk Import';
        }
    },
    methods: {
        getSchemaVersionText(schema_version) {
            return `Version: ${schema_version.version} (Created: ${new Date(schema_version.datetime_created).toLocaleDateString()} ${new Date(schema_version.datetime_created).toLocaleTimeString()}, Updated: ${new Date(schema_version.datetime_updated).toLocaleDateString()} ${new Date(schema_version.datetime_updated).toLocaleTimeString()})`;
        },
        resetFileField() {
            this.$nextTick(() => {
                this.importFileErrors = null;
                this.form.classList.remove('was-validated');
            });
        },
        bulkImportFileSelected(event) {
            this.importFileErrors = null;
            this.form.classList.remove('was-validated');

            // If there is a file call the initial import file check api end point
            const file = event.target.files[0];
            const formData = new FormData();
            formData.append('_file', file);

            this.$http.post(api_endpoints.occurrence_report_bulk_imports, formData).then((response) => {
                if (response.status >= 200 && response.status < 300) {
                    console.log(response.body);
                    this.importFileErrors = null;
                    this.form.classList.remove('was-validated');
                    this.$refs['bulk-import-file'].value = '';
                    swal.fire({
                        title: 'Bulk Import Added to Queue',
                        text: 'The bulk import of occurrence reports has been added to the queue for processing',
                        icon: 'success',
                        showCancelButton: false,
                        confirmButtonText: 'Ok',
                        customClass: {
                            confirmButton: 'btn btn-primary',
                        },
                    });
                } else {
                    this.importFileErrors = response.body;
                    this.$refs['bulk-import-file'].setCustomValidity('Invalid field');
                    this.form.classList.add('was-validated');
                }
            }, (error) => {
                this.importFileErrors = error.body;
                this.$refs['bulk-import-file'].setCustomValidity('Invalid field');
                this.form.classList.add('was-validated');
                console.log(error.body);
            });
        },
        confirmBeginBulkImport() {
            swal.fire({
                title: 'Are you sure?',
                text: 'You are you want to queue this bulk import of occurrence reports',
                icon: 'question',
                showCancelButton: true,
                confirmButtonText: 'Queue Bulk Import',
                cancelButtonText: 'Cancel',
                customClass: {
                    confirmButton: 'btn btn-primary',
                    cancelButton: 'btn btn-secondary'
                },
                reverseButtons: true
            }).then((result) => {
                if (result.isConfirmed) {
                    this.queueBulkImport();
                }
            });
        },
        fetchSchemas() {
            this.$http.get(`${api_endpoints.occurrence_report_bulk_import_schemas_by_group_type}?group_type=${this.$route.query.group_type}`).then((response) => {
                this.schema_versions = response.body;
            }, (error) => {
                console.log(error);
            });
        },
        fetchQueuedImports() {
            this.$http.get(`${api_endpoints.occurrence_report_bulk_imports}?processing_status=queued`).then((response) => {
                this.queuedImports = response.body.results;
            }, (error) => {
                console.log(error);
            });
        },
        fetchCurrentlyRunningImports() {
            this.$http.get(`${api_endpoints.occurrence_report_bulk_imports}?processing_status=started`).then((response) => {
                this.currentlyRunningImports = response.body.results;
            }, (error) => {
                console.log(error);
            });
        },
        fetchFailedImports() {
            this.$http.get(`${api_endpoints.occurrence_report_bulk_imports}?processing_status=failed&limit=3`).then((response) => {
                this.failedImports = response.body.results;
            }, (error) => {
                console.log(error);
            });
        },
        fetchCompletedImports() {
            this.$http.get(`${api_endpoints.occurrence_report_bulk_imports}?processing_status=completed&limit=3`).then((response) => {
                this.completedImports = response.body.results;
            }, (error) => {
                console.log(error);
            });
        },
        retryBulkImportTask(bulkImportTaskId) {
            // Call the api to retry the bulk import task
            this.$http.patch(`${api_endpoints.occurrence_report_bulk_imports}${bulkImportTaskId}/retry/`).then((response) => {
                console.log(response);
                // Remove the failed import from the failed imports list
                this.failedImports = this.failedImports.filter((failedImport) => {
                    return failedImport.id !== bulkImportTaskId;
                });
                this.fetchQueuedImports();
            }, (error) => {
                console.log(error);
            });
        },
        revert(bulkImportTaskId) {
            swal.fire({
                title: 'Revert and Archive',
                text: 'Are you sure you want to revert this bulk import of occurrence reports and archive it?',
                icon: 'question',
                showCancelButton: true,
                confirmButtonText: 'Revert and Archive',
                cancelButtonText: 'Cancel',
                customClass: {
                    confirmButton: 'btn btn-primary',
                    cancelButton: 'btn btn-secondary'
                },
                reverseButtons: true
            }).then((result) => {
                if (result.isConfirmed) {
                    // Call the api to revert the bulk import task
                    this.$http.patch(`${api_endpoints.occurrence_report_bulk_imports}${bulkImportTaskId}/revert/`).then((response) => {
                        console.log(response);
                        // Remove the completed import from the completed imports list
                        this.completedImports = this.completedImports.filter((completedImport) => {
                            return completedImport.id !== bulkImportTaskId;
                        });
                        this.fetchQueuedImports();
                    }, (error) => {
                        console.log(error);
                    });
                }
            });

        },
        fetchImports() {
            this.fetchQueuedImports();
            this.fetchFailedImports();
            this.fetchCompletedImports();
        }
    },
    created() {
        this.fetchSchemas();
        this.fetchImports();
        this.fetchCurrentlyRunningImports();
    },
    mounted() {
        this.form = document.getElementById('bulk-import-form');
        this.timer = setInterval(() => {
            this.fetchImports()
        }, 5000)
        this.currentlyRunningTimer = setInterval(() => {
            this.fetchCurrentlyRunningImports()
        }, 1000)
    },
    beforeDestroy() {
        clearInterval(this.timer)
        clearInterval(this.currentlyRunningTimer)
    }
}
</script>
<style scoped>
div.currently-running {
    border-color: rgba(34, 111, 187, 1);
    animation: border-pulsate 1s infinite;
}

@keyframes border-pulsate {
    0% {
        border-color: rgba(34, 111, 187, 1)
    }

    50% {
        border-color: rgba(34, 111, 187, 0)
    }

    100% {
        border-color: rgba(34, 111, 187, 1)
    }
}
</style>
