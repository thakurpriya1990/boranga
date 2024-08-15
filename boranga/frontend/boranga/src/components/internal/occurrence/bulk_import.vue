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
                        Some information about the import process. Including a link to <a href="">an example template .xlsx file</a>?
                    </alert>
                </div>
                <div class="mb-3">
                    <div class="card">
                        <div class="card-body">
                            <div class="mb-3">

                            </div>
                            <div class="input-group w-75 mb-3">
                                <input type="file" class="form-control" id="bulk-import-file"
                                    aria-describedby="bulk-import-button" @change="bulkImportFileSelected"
                                    accept="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet">
                                <button v-if="bulkImportButtonVisible" class="btn btn-primary" id="bulk-import-button"
                                    @click.prevent="confirmBeginBulkImport"><i class="bi bi-download pe-2"></i>Queue Bulk
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
                                            <th scope="col">File Name</th>
                                            <th scope="col">File Size</th>
                                            <th scope="col">Row Count</th>
                                            <th scope="col"><i class="bi bi-hourglass-split"></i> Time Estimate</th>
                                        </tr>
                                    </thead>
                                    <tbody class="text-muted">
                                        <tr class="">
                                            <td>R1C2</td>
                                            <td>R1C3</td>
                                            <td>R1C3</td>
                                            <td>
                                                <div>
                                                    10 minutes
                                                </div>
                                            </td>
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
                                            <th scope="col">File Name</th>
                                            <th scope="col">File Size</th>
                                            <th scope="col">Row Count</th>
                                            <th scope="col">Progress</th>
                                        </tr>
                                    </thead>
                                    <tbody>
                                        <tr class="">
                                            <td>R1C2</td>
                                            <td>R1C3</td>
                                            <td>R1C3</td>
                                            <td>
                                                <div class="progress">
                                                    <div class="progress-bar" role="progressbar" style="width: 27%;"
                                                        aria-valuenow="27" aria-valuemin="0" aria-valuemax="100">27%
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
                <div v-if="completedImports && completedImports.length > 0">
                    <div class="card border-success">
                        <div class="card-body">
                            <h5 class="card-title text-success mb-3"><i class="bi bi-list-checkme-2"></i>Completed Bulk
                                Imports</h5>
                            <div class="table-responsive">
                                <table class="table table-sm">
                                    <thead>
                                        <tr>
                                            <th scope="col">File Name</th>
                                            <th scope="col">File Size</th>
                                            <th scope="col">Records Imported</th>
                                            <th scope="col">Date Completed</th>
                                        </tr>
                                    </thead>
                                    <tbody>
                                        <tr class="">
                                            <td>R1C2</td>
                                            <td>R1C3</td>
                                            <td>R1C3</td>
                                            <td>R1C3</td>
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

export default {
    name: 'OccurrenceReportBulkImport',
    data() {
        return {
            bulkImportButtonVisible: false,
            queuedImports: [],
            currentlyRunningImports: [],
            completedImports: []
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
        bulkImportFileSelected() {
            console.log('Bulk Import File Selected');

            // If there is a file then make the bulk import button visible
            this.bulkImportButtonVisible = true;

            // If there is a file call the initial import file check api end point

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
