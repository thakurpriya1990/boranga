<template>
    <div class="container gx-4" id="occurence-report-bulk-import-schema">
        <div class="row mb-2">
            <div class="col">
                <div class="mb-4">
                    <h2 class="text-capitalize">Occurrence Report Bulk Import Schemas</h2>
                </div>
                <div class="mb-3">
                    <div class="card">
                        <div class="card-body">
                            <form id="bulk-import-form" class="needs-validation" no-validate>
                                <div class="mb-3">
                                    <label for="schema-version" class="form-label">Group Type</label>
                                    <select class="form-select text-secondary w-25" id="schema-version"
                                        ref="schema-version" v-model="group_type" aria-label="Select Schema Version"
                                        @change="fetchBulkSchemas">
                                        <option :value="null" selected>Select Group Type</option>
                                        <option value="flora">Flora</option>
                                        <option value="fauna">Fauna</option>
                                        <option value="community">Community</option>
                                    </select>
                                </div>
                            </form>
                            <div>
                                <button v-if="group_type" class="btn btn-primary float"><i class="bi bi-plus-circle-fill"></i> Create New Version</button>
                            </div>
                        </div>
                    </div>
                </div>
                <div class="mb-3">
                    <div v-if="bulkSchemas && bulkSchemas.length > 0" class="table-responsive">
                        <table class="table table-sm">
                            <thead>
                                <tr>
                                    <th scope="col">Version</th>
                                    <th scope="col">Created</th>
                                    <th scope="col">Updated</th>
                                    <th scope="col">Actions</th>
                                </tr>
                            </thead>
                            <tbody class="text-muted">
                                <tr v-for="schema in bulkSchemas" class="">
                                    <td>{{ schema.version }}</td>
                                    <td>{{ new Date(schema.datetime_created).toLocaleDateString() }} {{ new
                                        Date(schema.datetime_created).toLocaleTimeString() }}</td>
                                    <td>{{ new Date(schema.datetime_updated).toLocaleDateString() }} {{ new
                                        Date(schema.datetime_updated).toLocaleTimeString() }}</td>
                                    <td>
                                        <a class="btn btn-sm btn-primary my-0 me-2" role="button"
                                            :href="`/internal/occurrence_report/bulk_import_schema/${schema.id}`"><i
                                                class="bi bi-pencil-fill me-2"></i> Edit</a>
                                        <button class="btn btn-sm btn-primary my-0"><i class="bi bi-copy me-2"></i> Create a Copy</button>
                                    </td>
                                </tr>
                            </tbody>
                        </table>
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
    name: 'OccurrenceReportBulkImportSchemaList',
    data() {
        return {
            group_type: null,
            bulkSchemas: null,
        }
    },
    components: {
        alert
    },
    methods: {
        fetchBulkSchemas() {
            if (!this.group_type) {
                this.bulkSchemas = null
                return
            }
            this.$http.get(api_endpoints.occurrence_report_bulk_import_schemas_by_group_type, {
                params: {
                    group_type: this.group_type
                }
            })
                .then(response => {
                    this.bulkSchemas = response.data
                })
                .catch(error => {
                    console.error(error)
                })
        }
    },
}
</script>
