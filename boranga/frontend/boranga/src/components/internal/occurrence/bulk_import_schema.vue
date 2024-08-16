<template>
    <div class="container gx-4" id="occurence-report-bulk-import-schema">
        <div class="row mb-2">
            <div class="col">
                <div class="mb-4">
                    <h2 class="text-capitalize">Occurrence Report Bulk Import Schema</h2>
                </div>
                <div class="mb-3">
                    <alert type="primary">
                        <i class="bi bi-info-circle-fill text-primary fs-4 help-text-popover me-2"></i>
                        Some information about defining a bulk import schema...
                    </alert>
                </div>
                <div class="mb-3">
                    <div class="card">
                        <div class="card-body">
                            <div class="border-bottom mb-3">
                                <h4>Schema (Version: 1.0)</h4>
                            </div>
                            <div class="border-bottom mb-3">
                                <form>
                                    <div class="row mb-3">
                                        <label for="group-type" class="col-sm-2 col-form-label">Group Type</label>
                                        <select class="form-select w-25" aria-label="Group Type">
                                            <option value="1">Flora</option>
                                        </select>
                                    </div>
                                </form>
                            </div>
                            <div class="mb-3">
                                <label for="exampleFormControlInput1" class="form-label fs-5"><i
                                        class="bi bi-filetype-xlsx text-success me-3"></i>Excel preview <span
                                        class="text-muted ms-2 fs-6">(.xlsx)</span></label>
                                <div class="">
                                    <table class="table table-bordered table-hover table-sm w-50">
                                        <tbody>
                                            <tr>
                                                <th style="width:5%" class="text-center">1</th>
                                                <th class="ps-3" style="width:40%">Migrated From ID</th>
                                                <td class="text-muted text-center" style="width:15%">
                                                    <i class="bi bi-pencil-square text-primary me-2" role="button"></i>
                                                    <i class="bi bi-trash3-fill text-danger" role="button"></i>
                                                </td>
                                            </tr>
                                            <tr class="">
                                                <th class="text-center">2</th>
                                                <th class="ps-3">Scientific Name</th>
                                                <td class="text-muted text-center">
                                                    <i class="bi bi-pencil-square text-primary me-2" role="button"></i>
                                                    <i class="bi bi-trash3-fill text-danger" role="button"></i>
                                                </td>
                                            </tr>
                                            <tr class="">
                                                <th class="text-center">2</th>
                                                <th class="ps-3">Scientific Name</th>
                                                <td class="text-muted text-center"><i
                                                        class="bi bi-pencil-square text-primary me-2" role="button"></i>
                                                    <i class="bi bi-trash3-fill text-danger" role="button"></i>
                                                </td>
                                            </tr>
                                            <tr class="">
                                                <th class="text-center">3</th>
                                                <th class="ps-3">Observation Date</th>
                                                <td class="text-muted text-center"><i
                                                        class="bi bi-pencil-square text-primary me-2" role="button"></i>
                                                    <i class="bi bi-trash3-fill text-danger" role="button"></i>
                                                </td>
                                            </tr>
                                            <tr class="">
                                                <th class="text-center">4</th>
                                                <th class="ps-3">Location Description</th>
                                                <td class="text-muted text-center"><i
                                                        class="bi bi-pencil-square text-primary me-2" role="button"></i>
                                                    <i class="bi bi-trash3-fill text-danger" role="button"></i>
                                                </td>
                                            </tr>
                                            <tr class="">
                                                <th class="text-center">5</th>
                                                <th class="ps-3">Add New Column</th>
                                                <td class="text-muted text-center"><i
                                                        class="bi bi-plus-circle-fill text-success" role="button"></i>
                                                </td>
                                            </tr>
                                        </tbody>
                                    </table>
                                </div>
                            </div>
                            <div class="mb-3">
                                <div class="card" style="width:60%">
                                    <div class="card-body">
                                        <h4 class="card-title border-bottom mb-3">Scientific Name</h4>
                                        <form>
                                            <div class="row d-flex align-items-center mb-2">
                                                <label for="inputEmail3" class="col-sm-4 col-form-label">Django Import
                                                    Model</label>
                                                <div class="col-sm-8 ">
                                                    <select class="form-select form-select-sm" aria-label="Group Type">
                                                        <option value="1">Occurrence Report</option>
                                                    </select>
                                                </div>
                                            </div>
                                            <div class="row d-flex align-items-center mb-2">
                                                <label for="inputEmail3" class="col-sm-4 col-form-label">Django Import
                                                    Field</label>
                                                <div class="col-sm-8 ">
                                                    <select class="form-select form-select-sm" aria-label="Group Type">
                                                        <option value="1">Species</option>
                                                    </select>
                                                </div>
                                            </div>
                                            <div class="row d-flex align-items-center mb-2">
                                                <label for="inputEmail3" class="col-sm-4 col-form-label">Django
                                                    Type</label>
                                                <div class="col-sm-8 ">
                                                    <div class="input-group input-group-sm">
                                                        <input type="text" class="form-control" name="" id=""
                                                            aria-describedby="helpId" placeholder="" disabled
                                                            value="ForeignKey" />
                                                    </div>
                                                </div>
                                            </div>
                                            <div class="row d-flex align-items-center mb-2">
                                                <label for="inputEmail3" class="col-sm-4 col-form-label">Excel
                                                    Type</label>
                                                <div class="col-sm-8 ">
                                                    <div class="input-group input-group-sm">
                                                        <input type="text" class="form-control form-control-sm" name=""
                                                            id="" aria-describedby="helpId" placeholder="" disabled
                                                            value="None (String)" />
                                                    </div>
                                                </div>
                                            </div>
                                            <div class="row mb-2">
                                                <label for="inputEmail3" class="col-sm-4 col-form-label">Pre Import
                                                    Validations<i id="pre-import-validation-help-text"
                                                        class="bi bi-info-circle-fill text-primary ms-2"
                                                        data-bs-toggle="popover" data-bs-trigger="hover focus"
                                                        data-bs-content="Basic validations embedded in the .xlsx file"
                                                        data-bs-placement="top"></i></label>
                                                <div class="col-sm-8 ">
                                                    <div class="input-group input-group-sm mb-2">
                                                        <span class="input-group-text" id="basic-addon1">Allow
                                                            Blank</span>
                                                        <input type="text" class="form-control" placeholder="Username"
                                                            aria-label="Username" aria-describedby="basic-addon1"
                                                            disabled value="No">
                                                    </div>
                                                    <div class="input-group input-group-sm mb-2">
                                                        <span class="input-group-text" id="basic-addon1">Max
                                                            Length</span>
                                                        <input type="text" class="form-control" placeholder="Username"
                                                            aria-label="Username" aria-describedby="basic-addon1"
                                                            value="512 Characters" disabled>
                                                    </div>
                                                </div>
                                            </div>
                                            <div class="row mb-2">
                                                <label for="inputEmail3" class="col-sm-4 col-form-label">Import
                                                    Validations<i id="pre-import-validation-help-text"
                                                        class="bi bi-info-circle-fill text-primary ms-2"
                                                        data-bs-toggle="popover" data-bs-trigger="hover focus"
                                                        data-bs-content="More advanced validation that occurs during the import process"
                                                        data-bs-placement="top"></i></label>
                                                <div class="col-sm-8">
                                                    <fieldset class="border p-2 mb-2">
                                                        <div class="input-group input-group-sm mb-2">
                                                            <span class="input-group-text w-25" id="basic-addon1">
                                                                Type</span>
                                                            <select class="form-select form-select-sm"
                                                                aria-label="Group Type">
                                                                <option value="1">Django Lookup</option>
                                                            </select>
                                                            <span class="input-group-text" id="basic-addon1">
                                                                <i class="bi bi-trash3-fill text-danger float-end"
                                                            role="button"></i></span>
                                                        </div>
                                                        <div class="input-group input-group-sm mb-2">
                                                            <span class="input-group-text w-25" id="basic-addon1">
                                                                Lookup Model</span>
                                                            <select class="form-select" aria-label="Group Type">
                                                                <option value="1">Species</option>
                                                            </select>
                                                        </div>
                                                        <div class="input-group input-group-sm mb-1">
                                                            <span class="input-group-text w-25" id="basic-addon1">
                                                                Lookup Field</span>
                                                            <select class="form-select" aria-label="Group Type">
                                                                <option value="1">taxonomy__scientific_name</option>
                                                            </select>
                                                        </div>
                                                    </fieldset>
                                                    <div class="float-end" style="width:15px">

                                                    </div>
                                                    <div class="input-group input-group-sm mb-2">
                                                        <button class="btn btn-primary"><i
                                                                class="bi bi-plus-circle-fill me-2"
                                                                role="button"></i>Add Another</button>
                                                    </div>
                                                </div>
                                            </div>
                                        </form>
                                    </div>
                                </div>
                            </div>
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
    name: 'OccurrenceReportBulkImportSchema',
    data() {
        return {

        }
    },
    components: {
        alert
    },
    computed: {

    },
    methods: {

    },
    created() {

    },
    mounted() {
        // enable all bootstrap 5 popovers
        var popoverTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="popover"]'))
        var popoverList = popoverTriggerList.map(function (popoverTriggerEl) {
            return new bootstrap.Popover(popoverTriggerEl)
        })
    },
    beforeDestroy() {

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
</style>
