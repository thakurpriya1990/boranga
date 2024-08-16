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
                            <div class="mb-3">

                            </div>
                            <div class="input-group w-75 mb-3">
                                <input type="file" class="form-control" id="bulk-import-file" ref="bulk-import-file"
                                    aria-describedby="bulk-import-button" @change="bulkImportFileSelected"
                                    accept="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet">
                                <button v-if="bulkImportButtonVisible" class="btn btn-primary" id="bulk-import-button"
                                    @click.prevent="confirmBeginBulkImport"><i class="bi bi-download pe-2"></i>Queue
                                    Bulk
                                    Import</button>
                            </div>
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
                                            <th scope="col">Datetime Queued</th>
                                            <th scope="col">File Name</th>
                                            <th scope="col">File Size</th>
                                            <th scope="col">Row Count</th>
                                            <th scope="col"><i class="bi bi-hourglass-split"></i> Time Estimate</th>
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
                                            <th scope="col">Datetime Started</th>
                                            <th scope="col">File Name</th>
                                            <th scope="col">File Size</th>
                                            <th scope="col">Progress</th>
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
                                        <tr v-for="failedImport in failedImports" :id="`failed-import-${failedImport.id}`" class="">
                                            <td>{{ new Date(failedImport.datetime_started).toLocaleString() }}</td>
                                            <td class="text-truncate" style="max-width: 350px;">{{
                                                failedImport.file_name }}</td>
                                            <td>{{ failedImport.file_size_megabytes }} MB</td>
                                            <td class="text-end pe-3">{{ failedImport.rows ? failedImport.rows :
                                                'Not Counted' }}</td>
                                            <td>
                                                <button class="btn btn-sm btn-danger me-2"
                                                    data-bs-target="#staticBackdrop" data-bs-toggle="modal"
                                                    @click="selectedErrors = failedImport.error_message"><i class="bi bi-eye"></i>
                                                    View Errors</button>
                                                <button class="btn btn-sm btn-primary" @click.prevent="retryBulkImportTask(failedImport.id)"><i
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
                                            <th scope="col">Datetime Completed</th>
                                            <th scope="col">File Size</th>
                                            <th scope="col">Records Imported</th>
                                            <th scope="col">Total Time Taken</th>
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
            bulkImportButtonVisible: false,
            queuedImports: null,
            currentlyRunningImports: null,
            failedImports: null,
            completedImports: null,
            timer: null,
            currentlyRunningTimer: null,
            selectedErrors: '',
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
        bulkImportFileSelected(event) {
            console.log('Bulk Import File Selected');

            if (!event.target.files.length) {
                this.bulkImportButtonVisible = false;
                return;
            }

            // If there is a file call the initial import file check api end point
            const file = event.target.files[0];
            const formData = new FormData();
            formData.append('_file', file);

            this.$http.post(api_endpoints.occurrence_report_bulk_imports, formData).then((response) => {
                if (response.status === 200) {
                    // If there is a file then make the bulk import button visible
                    this.bulkImportButtonVisible = true;
                    console.log(response.body);
                }
            }, (error) => {
                console.log(error);
            });

            // If there are any issues with the file then display the errors or warnings above
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
            console.log('Queue Bulk Import');
            // Call the bulk import api end point
        },
        queueBulkImport() {
            // Call the api to add the import to the queue
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
        fetchImports() {
            this.fetchQueuedImports();
            this.fetchFailedImports();
            this.fetchCompletedImports();
        }
    },
    created() {
        this.fetchImports();
        this.fetchCurrentlyRunningImports();
    },
    mounted() {
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
