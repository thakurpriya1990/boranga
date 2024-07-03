<template lang="html">
    <div id="occurrence_tenure_modal">
        <modal
            transition="modal fade"
            :title="modalTitle"
            large
            @ok="ok()"
            @cancel="cancel()"
        >
            <div class="container-fluid">
                <div class="row">
                    <form class="form-horizontal" name="modalForm">
                        <alert :show.sync="showError" type="danger"
                            ><strong>{{ errorString }}</strong></alert
                        >
                        <alert
                            v-if="change_warning && !isReadOnly"
                            type="warning"
                            ><strong>{{ change_warning }}</strong></alert
                        >
                        <!-- <div class="col-sm-12">
                            <div class="form-group">
                                <div class="row mb-3">
                                    <div class="col-sm-3">
                                        <label class="control-label pull-left"
                                            >Site Name</label
                                        >
                                    </div>
                                    <div class="col-sm-9">
                                        <textarea v-model="siteObj.site_name">
                                            :disabled="isReadOnly"
                                            rows="1"
                                            class="form-control"
                                        </textarea>
                                    </div>
                                </div>
                            </div>
                            <div class="row mb-3">
                                <label for="" class="col-sm-3 control-label"
                                    >Point Coordinate :</label
                                >
                                <div class="col-sm-4">
                                    <input
                                        id="point_coord1"
                                        v-model="siteObj.point_coord1"
                                        :disabled="isReadOnly"
                                        type="decimal"
                                        class="form-control"
                                        placeholder=""
                                    />
                                </div>
                                -
                                <div class="col-sm-4">
                                    <input
                                        id="point_coord2"
                                        v-model="siteObj.point_coord2"
                                        :disabled="isReadOnly"
                                        type="decimal"
                                        class="form-control"
                                        placeholder=""
                                    />
                                </div>
                            </div>
                            <div class="row mb-3">
                                <div class="col-sm-3">
                                    <label class="control-label pull-left"
                                        >Site Type</label
                                    >
                                </div>
                                <div class="col-sm-9">
                                    <select v-model="siteObj.site_type">
                                        :disabled="isReadOnly"
                                        class="form-select"
                                        <option
                                            v-for="site in site_type_list"
                                            :key="site.id"
                                            :value="site.id"
                                        >
                                            {{ site.name }}
                                        </option>
                                    </select>
                                </div>
                            </div>
                            <div class="form-group">
                                <div class="row mb-3">
                                    <div class="col-sm-3">
                                        <label class="control-label pull-left"
                                            >Occurrence Reports</label
                                        >
                                    </div>
                                    <div class="col-sm-9">
                                        <div
                                            id="select_occurrence_reports"
                                            class="form-group"
                                        >
                                            <select
                                                ref="occurrence_report_select"
                                                v-model="
                                                    siteObj.related_occurrence_reports
                                                "
                                                :disabled="isReadOnly"
                                                style="width: 100%"
                                                class="form-select input-sm"
                                            >
                                                <option
                                                    v-for="option in occurrence_obj.occurrence_reports"
                                                    :key="option.id"
                                                    :value="option.id"
                                                >
                                                    {{
                                                        option.occurrence_report_number
                                                    }}
                                                </option>
                                            </select>
                                        </div>
                                    </div>
                                </div>
                            </div>
                            <div class="form-group">
                                <div class="row mb-3">
                                    <div class="col-sm-3">
                                        <label class="control-label pull-left"
                                            >Comments</label
                                        >
                                    </div>
                                    <div class="col-sm-9">
                                        <textarea
                                            v-model="siteObj.comments"
                                            :disabled="isReadOnly"
                                            rows="2"
                                            class="form-control"
                                        >
                                        </textarea>
                                    </div>
                                </div>
                            </div>
                        </div> -->
                    </form>
                </div>
            </div>
            <div slot="footer">
                <button
                    type="button"
                    class="btn btn-secondary me-2"
                    @click="cancel"
                >
                    Cancel
                </button>
                <template v-if="modal_action != 'view'">
                    <template v-if="object_id">
                        <button
                            v-if="updatingEntry"
                            type="button"
                            disabled
                            class="btn btn-primary fa fa-spinnner fa-spin"
                            @click="ok"
                        >
                            </i> Updating</button>
                        <button v-else type="button" class="btn btn-primary" @click="ok">Update</button>
                    </template>
                    <template v-else>
                        <button v-if="addingEntry" type="button" disabled class="btn btn-primary" @click="ok"><i
                                class="fa fa-spinner fa-spin"></i> Adding</button>
                        <button v-else type="button" class="btn btn-primary" @click="ok">Add Entry</button>
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
    name: 'OccurrenceTenureDatatable',
    components: {
        modal,
        alert
    },
    props: {
        url: {
            type: String,
            required: true
        },
        title: {
            type: String,
            required: false,
            default: 'Object'
        },
        change_warning: {
            type: String,
            required: false
        },
        // occurrence_obj: {
        //     type: Object,
        //     required: false
        // },
        occurrenceId: {
            type: Number,
            required: true
        },
    },
    data: function () {
        let vm = this;
        return {
            isModalOpen: false,
            form: null,
            object_id: String,
            modal_action: String,
            tenureObj: {},
            // siteObj: {
            //     related_occurrence_reports: [],
            // },
            addingEntry: false,
            updatingEntry: false,
            validation_form: null,
            type: '1',
            errors: false,
            errorString: '',
            successString: '',
            success: false,
            // site_type_list: [],
        }
    },
    computed: {
        showError: function () {
            const vm = this;
            return vm.errors;
        },
        modalTitle: function () {
            var action = this.modal_action;
            if (typeof action === "string" && action.length > 0) {
                let capitalizedAction = action.charAt(0).toUpperCase() + action.slice(1);
                return `${capitalizedAction} ${this.title}`;
            } else {
                return `Invalid ${this.title} action`; // Or handle the error in an appropriate way
            }
        },
        isReadOnly: function () {
            return this.modal_action === "view" ? true : false;
        }
    },
    watch: {
        // siteObj: function () {
        //     let vm = this;
        //     vm.reinitialiseOCRLookup()
        // }
    },
    created: async function () {
        // let res = await this.$http.get('/api/occurrence_sites/site_list_of_values/');
        // let site_list_of_values_res = {};
        // Object.assign(site_list_of_values_res, res.body);
        // this.site_type_list = site_list_of_values_res.site_type_list;
        // this.site_type_list.splice(0, 0,
        //     {
        //         id: null,
        //         name: null,
        //     });
    },
    mounted: function () {
        let vm = this;
        vm.form = document.forms.modalForm;

        this.$nextTick(() => {
            // vm.eventListeners();
            // vm.initialiseOCRSelect();
        });
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
            // this.siteObj = {
            //     related_occurrence_reports: [],
            // };
            this.errors = false;
            $('.has-error').removeClass('has-error');
        },
        // reinitialiseOCRLookup: function () {
        //     let vm = this;
        //     vm.$nextTick(() => {
        //         $(vm.$refs.occurrence_report_select).select2('destroy');
        //         vm.initialiseOCRSelect();
        //     });
        // },
        // initialiseOCRSelect: function () {
        //     let vm = this;
        //     // Initialise select2 for proposed Conservation Criteria
        //     $(vm.$refs.occurrence_report_select).select2({
        //         "theme": "bootstrap-5",
        //         dropdownParent: $("#select_occurrence_reports"),
        //         allowClear: true,
        //         multiple: true,
        //         placeholder: "Select Occurrence Report",
        //     }).
        //         on("select2:select", function (e) {
        //             var selected = $(e.currentTarget);
        //             vm.siteObj.related_occurrence_reports = selected.val();
        //         }).
        //         on("select2:unselect", function (e) {
        //             var selected = $(e.currentTarget);
        //             vm.siteObj.related_occurrence_reports = selected.val();
        //         });
        // },
        sendData: function () {
            let vm = this;
            vm.errors = false;
            let siteObj = JSON.parse(JSON.stringify(vm.siteObj));
            let formData = new FormData()

            if (vm.siteObj.id) {
                vm.updatingEntry = true;
                formData.append('data', JSON.stringify(siteObj));
                vm.$http.put(helpers.add_endpoint_json(vm.url, siteObj.id), formData, {
                    emulateJSON: true,
                }).then((response) => {
                    vm.updatingEntry = false;
                    vm.$parent.updatedSites();
                    vm.close();
                }, (error) => {
                    vm.errors = true;
                    vm.errorString = helpers.apiVueResourceError(error);
                    vm.updatingEntry = false;
                });
            } else {
                vm.addingEntry = true;
                formData.append('data', JSON.stringify(siteObj));
                vm.$http.post(vm.url, formData, {
                    emulateJSON: true,
                }).then((response) => {
                    vm.addingEntry = false;
                    vm.close();
                    vm.$parent.updatedSites();
                }, (error) => {
                    vm.errors = true;
                    vm.addingEntry = false;
                    vm.errorString = helpers.apiVueResourceError(error);
                });
            }
        },
        eventListeners: function () {
            let vm = this;
        }
    }
}
</script>
