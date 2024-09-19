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
                                        ref="schema-version" v-model="groupType" aria-label="Select Schema Version"
                                        @change="fetchBulkSchemas">
                                        <option :value="null" selected>Select Group Type</option>
                                        <option v-for="groupType in groupTypes" :value="groupType.id">{{
                                            groupType.name.charAt(0).toUpperCase() + groupType.name.substring(1) }}
                                        </option>
                                    </select>
                                </div>
                            </form>
                            <div>
                                <button v-if="groupType" class="btn btn-primary float" @click="createNewVersion"><i
                                        class="bi bi-plus-circle-fill"></i> Create New Version</button>
                            </div>
                        </div>
                    </div>
                </div>
                <div class="mb-3">
                    <div v-if="bulkSchemas && bulkSchemas.length > 0" class="table-responsive">
                        <table class="table table-sm">
                            <thead>
                                <tr>
                                    <th scope="col" style="width: 40px;">Version</th>
                                    <th scope="col" style="width: 250px;">Name</th>
                                    <th scope="col" style="width: 260px;">Tags</th>
                                    <th scope="col" style="width: 170px;">Created</th>
                                    <th scope="col" style="width: 170px;">Updated</th>
                                    <th scope="col">Actions</th>
                                </tr>
                            </thead>
                            <tbody class="text-muted">
                                <tr v-for="schema in bulkSchemas" class="">
                                    <td>{{ schema.version }}</td>
                                    <td class="text-truncate text-align-end" style="max-width: 300px;"
                                        :title="schema.name">{{
                                            schema.name }}</td>
                                    <td class="text-truncate"><span class="badge bg-info fs-6 me-2"
                                            v-for="(tag, index) in schema.tags.slice(0, 2)" :key="tag">{{ tag }}</span>
                                        <span v-if="schema.tags.length > 2"
                                            :title="String(schema.tags).replace(/,/g, ', ')" @click.prevent="">+{{
                                            schema.tags.length - 2 }}</span>
                                    </td>
                                    <td>{{ new
                                        Date(schema.datetime_created).toLocaleDateString() }} {{ new
                                            Date(schema.datetime_created).toLocaleTimeString() }}</td>
                                    <td>{{ new
                                        Date(schema.datetime_updated).toLocaleDateString() }} {{ new
                                            Date(schema.datetime_updated).toLocaleTimeString() }}</td>
                                    <td>
                                        <a class="btn btn-sm btn-primary my-0 me-2" role="button"
                                            :href="`/internal/occurrence_report/bulk_import_schema/${schema.id}`"><i
                                                class="bi bi-pencil-fill me-2"></i> Edit</a>
                                        <button class="btn btn-sm btn-primary my-0"
                                            @click.prevent="copySchema(schema.id)"><i class="bi bi-copy me-2"></i>
                                            Create a Copy</button>
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
            groupTypes: null,
            groupType: null,
            bulkSchemas: null,
        }
    },
    components: {
        alert
    },
    methods: {
        fetchGroupTypes() {
            this.$http.get(api_endpoints.group_types_dict)
                .then(response => {
                    this.groupTypes = response.data
                })
                .catch(error => {
                    console.error(error)
                })
        },
        fetchBulkSchemas() {
            if (!this.groupType) {
                this.bulkSchemas = null
                return
            }
            localStorage.setItem('ocr-bulk-import-group-type', this.groupType)
            this.$http.get(api_endpoints.occurrence_report_bulk_import_schemas, {
                params: {
                    group_type: this.groupType
                }
            })
                .then(response => {
                    this.bulkSchemas = response.data.results
                })
                .catch(error => {
                    console.error(error)
                })
        },
        copySchema(id) {
            this.$http.post(`${api_endpoints.occurrence_report_bulk_import_schemas}${id}/copy/`)
                .then(response => {
                    if (response.status === 201) {
                        swal.fire({
                            title: 'Success',
                            text: 'Schema copied successfully',
                            icon: 'success',
                            showConfirmButton: false,
                            timer: 1500
                        })
                        this.$router.push(`/internal/occurrence_report/bulk_import_schema/${response.data.id}`)
                    }
                })
                .catch(error => {
                    console.error(error)
                })
        },
        createNewVersion() {
            this.$http.post(api_endpoints.occurrence_report_bulk_import_schemas, {
                group_type: this.groupType
            })
                .then(response => {
                    if (response.status === 201) {
                        swal.fire({
                            title: 'Success',
                            text: 'New version created successfully',
                            icon: 'success',
                            showConfirmButton: false,
                            timer: 1500
                        })
                        this.$router.push(`/internal/occurrence_report/bulk_import_schema/${response.data.id}`)
                    }
                })
                .catch(error => {
                    console.error(error)
                })
        }
    },
    created() {
        this.fetchGroupTypes()
        if (localStorage.getItem('ocr-bulk-import-group-type')) {
            this.groupType = localStorage.getItem('ocr-bulk-import-group-type')
            this.fetchBulkSchemas()
        }
    }
}
</script>
