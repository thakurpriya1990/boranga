<template lang="html">
    <div id="site_detail">
        <modal transition="modal fade" @ok="ok()" @cancel="cancel()" :title="title" large>
            <div class="container-fluid">
                <div class="row">
                    <form class="form-horizontal" name="siteForm">
                        <alert v-if="showError" type="danger"><strong>{{ errorString }}</strong></alert>
                        <alert v-if="change_warning && !isReadOnly" type="warning"><strong>{{ change_warning }}</strong>
                        </alert>
                        <div class="col-sm-12">
                            <div class="form-group">
                                <div class="row mb-3">
                                    <div class="col-sm-3">
                                        <label class="control-label pull-left">Site Name</label>
                                    </div>
                                    <div class="col-sm-9">
                                        <textarea :disabled="isReadOnly" rows=1 class="form-control"
                                            v-model="siteObj.site_name">
                                        </textarea>
                                    </div>
                                </div>
                            </div>
                            <div class="row mb-3">
                                <label for="" class="col-sm-3 control-label">Point Coordinate (Lat-Long)</label>
                                <div class="col-sm-4">
                                    <input id="point_coord2" :disabled="isReadOnly" type="decimal" class="form-control"
                                        placeholder="" v-model="siteObj.point_coord2" />
                                </div>
                                -
                                <div class="col-sm-4">
                                    <input id="point_coord1" :disabled="isReadOnly" type="decimal" class="form-control"
                                        placeholder="" v-model="siteObj.point_coord1" />
                                </div>
                            </div>
                            <div class="row mb-3">
                                <div class="col-sm-3">
                                    <label class="control-label pull-left">Datum</label>
                                </div>
                                <div class="col-sm-9">
                                    <template v-if="!isReadOnly">
                                        <template
                                            v-if="datum_list && datum_list.length > 0 && siteObj.datum && !datum_list.map((d) => d.srid).includes(siteObj.datum)">
                                            <input type="text" v-if="siteObj.datum_name" class="form-control mb-3"
                                                :value="siteObj.datum_name + ' (Now Archived)'" disabled />
                                            <div class="mb-3 text-muted">
                                                Change datum to:
                                            </div>
                                        </template>
                                        <select class="form-select" v-model="siteObj.datum">
                                            <option v-for="datum in datum_list" :value="datum.srid"
                                                v-bind:key="datum.srid">
                                                {{ datum.name }}
                                            </option>
                                        </select>
                                    </template>
                                    <template v-else>
                                        <input class="form-control" type="text" :disabled="isReadOnly"
                                            v-model="siteObj.datum_name" />
                                    </template>
                                </div>
                            </div>
                            <div class="row mb-3">
                                <div class="col-sm-3">
                                    <label class="control-label pull-left">Site Type</label>
                                </div>
                                <div class="col-sm-9">
                                    <template v-if="!isReadOnly">
                                        <template
                                            v-if="site_type_list && site_type_list.length > 0 && siteObj.site_type && !site_type_list.map((d) => d.id).includes(siteObj.site_type)">
                                            <input type="text" v-if="siteObj.site_type_name" class="form-control mb-3"
                                                :value="siteObj.site_type_name + ' (Now Archived)'" disabled />
                                            <div class="mb-3 text-muted">
                                                Change site type to:
                                            </div>
                                        </template>
                                        <select class="form-select" v-model="siteObj.site_type">
                                            <option v-for="site_type in site_type_list" :value="site_type.id"
                                                v-bind:key="site_type.id">
                                                {{ site_type.name }}
                                            </option>
                                        </select>
                                    </template>
                                    <template v-else>
                                        <input class="form-control" type="text" :disabled="isReadOnly"
                                            v-model="siteObj.site_type_name" />
                                    </template>
                                </div>
                            </div>
                            <div class="form-group">
                                <div class="row mb-3">
                                    <div class="col-sm-3">
                                        <label class="control-label pull-left">Occurrence Reports</label>
                                    </div>
                                    <div class="col-sm-9">
                                        <div class="form-group" id="select_occurrence_reports">
                                            <select :disabled="isReadOnly" style="width:100%;"
                                                class="form-select input-sm" ref="occurrence_report_select"
                                                v-model="siteObj.related_occurrence_reports">
                                                <option v-for="option in occurrence_obj.occurrence_reports"
                                                    :value="option.id" :key="option.id">
                                                    {{ option.occurrence_report_number }}
                                                </option>
                                            </select>
                                        </div>
                                    </div>
                                </div>
                            </div>
                            <div class="form-group">
                                <div class="row mb-3">
                                    <div class="col-sm-3">
                                        <label class="control-label pull-left">Comments</label>
                                    </div>
                                    <div class="col-sm-9">
                                        <textarea :disabled="isReadOnly" rows=2 class="form-control"
                                            v-model="siteObj.comments">
            </textarea>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </form>
                </div>
            </div>
            <div slot="footer">
                <button type="button" class="btn btn-secondary me-2" @click="cancel">Cancel</button>
                <template v-if="site_action != 'view'">
                    <template v-if="site_id">
                        <button type="button" v-if="updatingSite" disabled class="btn btn-primary" @click="ok">Updating
                            <span class="spinner-border spinner-border-sm" role="status" aria-hidden="true"></span>
                            <span class="visually-hidden">Loading...</span></button>
                        <button type="button" v-else class="btn btn-primary" @click="ok">Update</button>
                    </template>
                    <template v-else>
                        <button type="button" v-if="addingSite" disabled class="btn btn-primary" @click="ok">Adding
                            <span class="spinner-border spinner-border-sm" role="status" aria-hidden="true"></span>
                            <span class="visually-hidden">Loading...</span></button>
                        <button type="button" v-else class="btn btn-primary" @click="ok">Add Site</button>
                    </template>
                </template>
            </div>
        </modal>
    </div>
</template>

<script>

import modal from '@vue-utils/bootstrap-modal.vue'
import alert from '@vue-utils/alert.vue'
import { helpers } from "@/utils/hooks.js"
export default {
    name: 'Site-Detail',
    components: {
        modal,
        alert
    },
    props: {
        url: {
            type: String,
            required: true
        },
        change_warning: {
            type: String,
            required: false
        },
        occurrence_obj: {
            type: Object,
            required: false
        },
    },
    data: function () {
        let vm = this;
        return {
            isModalOpen: false,
            form: null,
            site_id: String,
            site_action: String,
            siteObj: {
                related_occurrence_reports: [],
            },
            addingSite: false,
            updatingSite: false,
            validation_form: null,
            type: '1',
            errors: false,
            errorString: '',
            successString: '',
            success: false,
            site_type_list: [],
            datum_list: [],
        }
    },
    computed: {
        showError: function () {
            var vm = this;
            return vm.errors;
        },
        title: function () {
            var action = this.site_action;
            if (typeof action === "string" && action.length > 0) {
                var capitalizedAction = action.charAt(0).toUpperCase() + action.slice(1);
                return capitalizedAction + " Site";
            } else {
                return "Invalid site action"; // Or handle the error in an appropriate way
            }
        },
        isReadOnly: function () {
            return this.site_action === "view" ? true : false;
        }
    },
    methods: {
        ok: function () {
            let vm = this;
            if ($(vm.form).valid()) {
                vm.sendData();
            }
        },
        cancel: function () {
            this.close()
        },
        close: function () {
            this.isModalOpen = false;
            this.siteObj = {
                related_occurrence_reports: [],
            };
            this.errors = false;
            $('.has-error').removeClass('has-error');
        },
        reinitialiseOCRLookup: function () {
            let vm = this;
            vm.$nextTick(() => {
                $(vm.$refs.occurrence_report_select).select2('destroy');
                vm.initialiseOCRSelect();
            });
        },
        initialiseOCRSelect: function () {
            let vm = this;
            // Initialise select2 for proposed Conservation Criteria
            $(vm.$refs.occurrence_report_select).select2({
                "theme": "bootstrap-5",
                dropdownParent: $("#select_occurrence_reports"),
                allowClear: true,
                multiple: true,
                placeholder: "Select Occurrence Report",
            }).
                on("select2:select", function (e) {
                    var selected = $(e.currentTarget);
                    vm.siteObj.related_occurrence_reports = selected.val();
                }).
                on("select2:unselect", function (e) {
                    var selected = $(e.currentTarget);
                    vm.siteObj.related_occurrence_reports = selected.val();
                });
        },
        sendData: function () {
            let vm = this;
            vm.errors = false;
            let siteObj = JSON.parse(JSON.stringify(vm.siteObj));
            let formData = new FormData()

            if (vm.siteObj.id) {
                vm.updatingSite = true;
                formData.append('data', JSON.stringify(siteObj));
                fetch(helpers.add_endpoint_json(vm.url, siteObj.id), {
                    method: 'PUT',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify(formData)
                }).then((response) => {
                    vm.updatingSite = false;
                    vm.$parent.updatedSites();
                    vm.close();
                }, (error) => {
                    vm.errors = true;
                    vm.errorString = helpers.apiVueResourceError(error);
                    vm.updatingSite = false;
                });
            } else {
                vm.addingSite = true;
                formData.append('data', JSON.stringify(siteObj));
                fetch(vm.url, {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify(formData)
                }).then((response) => {
                    vm.addingSite = false;
                    vm.close();
                    vm.$parent.updatedSites();
                }, (error) => {
                    vm.errors = true;
                    vm.addingSite = false;
                    vm.errorString = helpers.apiVueResourceError(error);
                });
            }
        },
        eventListeners: function () {
            let vm = this;
        }
    },
    created: async function () {
        let response = await fetch('/api/occurrence_sites/site_list_of_values/');
        const data = await response.json();
        let site_list_of_values_res = {};
        Object.assign(site_list_of_values_res, data);
        this.site_type_list = site_list_of_values_res.site_type_list;
        this.site_type_list.splice(0, 0,
            {
                id: null,
                name: null,
            });
        this.datum_list = site_list_of_values_res.datum_list;
        this.datum_list.splice(0, 0,
            {
                srid: null,
                name: null,
            });
    },
    watch: {
        siteObj: function () {
            let vm = this;
            vm.reinitialiseOCRLookup()
        }
    },
    mounted: function () {
        let vm = this;
        vm.form = document.forms.siteForm;

        this.$nextTick(() => {
            vm.eventListeners();
            vm.initialiseOCRSelect();
        });
    }
}
</script>
