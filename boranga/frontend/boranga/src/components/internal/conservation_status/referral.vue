<template lang="html">
    <div v-if="conservation_status_obj" class="container" id="internalCSReferral">
        <div class="row" style="padding-bottom: 50px;">
            <h3>{{ display_number }} - {{ display_name }}</h3>

            <div class="col-md-3">

                <Submission :submitter_first_name="submitter_first_name" :submitter_last_name="submitter_last_name"
                    :lodgement_date="conservation_status_obj.lodgement_date" class="mt-3" />

                <div class="mt-3">
                    <div class="card card-default">
                        <div class="card-header">
                            Workflow
                        </div>
                        <div class="card-body">
                            <strong>Status</strong><br />
                            {{ conservation_status_obj.processing_status }}
                        </div>
                    </div>
                </div>
            </div>
            <div class="col-md-9">
                <div class="row">
                    <template>
                        <div class="">
                            <div class="row">
                                <form :action="species_community_cs_form_url" method="post"
                                    name="new_conservation_status" enctype="multipart/form-data">
                                    <ProposalConservationStatus v-if="conservation_status_obj" ref="conservation_status"
                                        :conservation_status_obj="conservation_status_obj" :referral="referral">
                                    </ProposalConservationStatus>
                                    <input type="hidden" name="csrfmiddlewaretoken" :value="csrf_token" />
                                    <input type='hidden' name="conservation_status_id" :value="1" />
                                    <div class="row" style="margin-bottom: 50px">
                                        <div class="navbar fixed-bottom" style="background-color: #f5f5f5;"
                                            v-if="!conservation_status_obj.can_user_edit && !isFinalised">
                                            <div v-if="!isFinalised" class="container">
                                                <div class="col-md-12 text-end">
                                                    <button class="btn btn-primary pull-right" style="margin-top:5px;"
                                                        @click.prevent="save()">Save Changes</button>
                                                </div>
                                            </div>
                                        </div>
                                    </div>
                                </form>
                            </div>
                        </div>
                    </template>
                </div>
            </div>
        </div>
    </div>
</template>
<script>
import Vue from 'vue'
import datatable from '@vue-utils/datatable.vue'
import CommsLogs from '@common-utils/comms_logs.vue'
import Submission from '@common-utils/submission.vue'
import Workflow from '@common-utils/workflow.vue'
import CSMoreReferrals from '@common-utils/conservation_status/cs_more_referrals.vue'
import ProposalConservationStatus from '@/components/form_conservation_status.vue'
import {
    api_endpoints,
    helpers
}
    from '@/utils/hooks'
export default {
    name: 'InternalConservationStatusReferral',
    data: function () {
        let vm = this;
        return {
            "original_conservation_status_obj": null,
            "loading": [],
            form: null,
            savingConservationStatus: false,
            department_users: [],
            selected_referral: '',
            referral_text: '',
            referral_comment: '',
            sendingReferral: false,
            DATE_TIME_FORMAT: 'DD/MM/YYYY HH:mm:ss',
            comms_url: helpers.add_endpoint_json(api_endpoints.conservation_status, vm.$route.params.conservation_status_id + '/comms_log'),
            logs_url: helpers.add_endpoint_json(api_endpoints.conservation_status, vm.$route.params.conservation_status_id + '/action_log'),
            comparing: false,
            initialisedSelects: false,
            referral: null,
        }
    },
    components: {
        datatable,
        CommsLogs,
        Submission,
        Workflow,
        ProposalConservationStatus,
        CSMoreReferrals,
    },
    filters: {
        formatDate: function (data) {
            return data ? moment(data).format('DD/MM/YYYY HH:mm:ss') : '';
        }
    },
    props: {
        referralId: {
            type: Number,
        },
    },
    computed: {
        conservation_status_obj: function () {
            return this.referral != null && this.referral != 'undefined' ? this.referral.conservation_status : null;
        },
        csrf_token: function () {
            return helpers.getCookie('csrftoken')
        },
        referralListURL: function () {
            return this.referral != null ? helpers.add_endpoint_json(api_endpoints.cs_referrals, this.referral.id + '/referral_list') : '';
        },
        species_community_cs_form_url: function () {
            return `/api/conservation_status/${this.conservation_status_obj.id}/conservation_status_save.json`;
        },
        species_community_cs_referral_form_url: function () {
            return `/api/cs_referrals/${this.referral.id}/conservation_status_referral_save.json`;
        },
        display_number: function () {
            return this.conservation_status_obj.conservation_status_number;
        },
        display_name: function () {
            return (this.conservation_status_obj.group_type === "community") ?
                this.conservation_status_obj.conservation_status_number :
                this.conservation_status_obj.conservation_status_number;
        },
        submitter_first_name: function () {
            if (this.conservation_status_obj.submitter) {
                return this.conservation_status_obj.submitter.first_name
            } else {
                return ''
            }
        },
        submitter_last_name: function () {
            if (this.conservation_status_obj.submitter) {
                return this.conservation_status_obj.submitter.last_name
            } else {
                return ''
            }
        },
        submitter_id: function () {
            if (this.conservation_status_obj.submitter) {
                return this.conservation_status_obj.submitter.id
            } else {
                return ''
            }
        },
        submitter_email: function () {
            if (this.conservation_status_obj.submitter) {
                return this.conservation_status_obj.submitter.email
            } else {
                return ''
            }
        },
        isFinalised: function () {
            return !(this.referral != null && this.referral.processing_status == 'Awaiting');
        },
        canLimitedAction: function () {
            if (this.conservation_status_obj.processing_status == 'With Approver') {
                return this.conservation_status_obj && (this.conservation_status_obj.processing_status == 'With Assessor' || this.conservation_status_obj.processing_status == 'With Referral') && !this.isFinalised && !this.conservation_status_obj.can_user_edit && (this.conservation_status_obj.current_assessor.id == this.conservation_status_obj.assigned_approver || this.conservation_status_obj.assigned_approver == null) && this.conservation_status_obj.assessor_mode.assessor_can_assess ? true : false;
            }
            else {
                return this.conservation_status_obj && (this.conservation_status_obj.processing_status == 'With Assessor' || this.conservation_status_obj.processing_status == 'With Referral') && !this.isFinalised && !this.conservation_status_obj.can_user_edit && (this.conservation_status_obj.current_assessor.id == this.conservation_status_obj.assigned_officer || this.conservation_status_obj.assigned_officer == null) && this.conservation_status_obj.assessor_mode.assessor_can_assess ? true : false;
            }
        },
        canAction: function () {
            if (this.conservation_status_obj.processing_status == 'With Approver') {
                return this.conservation_status_obj && (this.conservation_status_obj.processing_status == 'With Approver' || this.conservation_status_obj.processing_status == 'With Assessor') && !this.isFinalised && !this.conservation_status_obj.can_user_edit && (this.conservation_status_obj.current_assessor.id == this.conservation_status_obj.assigned_approver || this.conservation_status_obj.assigned_approver == null) && this.conservation_status_obj.assessor_mode.assessor_can_assess ? true : false;
            }
            else {
                return this.conservation_status_obj && (this.conservation_status_obj.processing_status == 'With Approver' || this.conservation_status_obj.processing_status == 'With Assessor') && !this.isFinalised && !this.conservation_status_obj.can_user_edit && (this.conservation_status_obj.current_assessor.id == this.conservation_status_obj.assigned_officer || this.conservation_status_obj.assigned_officer == null) && this.conservation_status_obj.assessor_mode.assessor_can_assess ? true : false;
            }
        },
        canAssess: function () {
            return this.conservation_status_obj && this.conservation_status_obj.assessor_mode.assessor_can_assess ? true : false;
        },
        hasAssessorMode: function () {
            return this.conservation_status_obj && this.conservation_status_obj.assessor_mode.has_assessor_mode ? true : false;
        },
    },
    methods: {
        commaToNewline(s) {
            return s.replace(/[,;]/g, '\n');
        },
        save: async function () {
            let vm = this;
            vm.savingConservationStatus = true;
            let payload = new Object();
            Object.assign(payload, vm.referral);
            vm.$http.post(vm.species_community_cs_referral_form_url, payload).then(res => {
                swal.fire({
                    title: 'Saved',
                    text: 'Your changes has been saved',
                    icon: 'success',
                    confirmButtonColor: '#226fbb'
                });
                vm.savingConservationStatus = false;
            }, err => {
                vm.savingConservationStatus = false;
            });
        },
        save_wo: function () {
            let vm = this;
            let payload = new Object();
            Object.assign(payload, vm.conservation_status_obj);
            vm.$http.post(vm.species_community_cs_form_url, payload).then(res => {
            }, err => {
            });
        },
        refreshFromResponse: function (response) {
            let vm = this;
            vm.conservation_status_obj = helpers.copyObject(response.body);
        },
        assignTo: function () {
            let vm = this;
            let unassign = true;
            let data = {};
            if (vm.conservation_status_obj.processing_status == 'With Approver') {
                unassign = vm.conservation_status_obj.assigned_approver != null && vm.conservation_status_obj.assigned_approver != 'undefined' ? false : true;
                data = { 'assessor_id': vm.conservation_status_obj.assigned_approver };
            }
            else {
                unassign = vm.conservation_status_obj.assigned_officer != null && vm.conservation_status_obj.assigned_officer != 'undefined' ? false : true;
                data = { 'assessor_id': vm.conservation_status_obj.assigned_officer };
            }
            if (!unassign) {
                vm.$http.post(helpers.add_endpoint_json(api_endpoints.conservation_status, (vm.conservation_status_obj.id + '/assign_to')), JSON.stringify(data), {
                    emulateJSON: true
                }).then((response) => {
                    vm.conservation_status_obj = response.body;
                    vm.original_conservation_status_obj = helpers.copyObject(response.body);
                    vm.updateAssignedOfficerSelect();
                }, (error) => {
                    vm.conservation_status_obj = helpers.copyObject(vm.original_conservation_status_obj)
                    vm.updateAssignedOfficerSelect();
                    swal.fire({
                        title: 'Application Error',
                        text: helpers.apiVueResourceError(error),
                        icon: 'error',
                        confirmButtonColor: '#226fbb'
                    });
                });
            }
            else {
                vm.$http.get(helpers.add_endpoint_json(api_endpoints.conservation_status, (vm.conservation_status_obj.id + '/unassign')))
                    .then((response) => {
                        vm.conservation_status_obj = response.body;
                        vm.original_conservation_status_obj = helpers.copyObject(response.body);
                        vm.updateAssignedOfficerSelect();
                    }, (error) => {
                        vm.conservation_status_obj = helpers.copyObject(vm.original_conservation_status_obj)
                        vm.updateAssignedOfficerSelect();
                        swal.fire({
                            title: 'Application Error',
                            text: helpers.apiVueResourceError(error),
                            icon: 'error',
                            confirmButtonColor: '#226fbb'
                        });
                    });
            }
        },
        updateAssignedOfficerSelect: function () {
            let vm = this;
            if (vm.conservation_status_obj.processing_status == 'With Approver') {
                $(vm.$refs.assigned_officer).val(vm.conservation_status_obj.assigned_approver);
                $(vm.$refs.assigned_officer).trigger('change');
            }
            else {
                $(vm.$refs.assigned_officer).val(vm.conservation_status_obj.assigned_officer);
                $(vm.$refs.assigned_officer).trigger('change');
            }
        },
        initialiseAssignedOfficerSelect: function (reinit = false) {
            let vm = this;
            if (reinit) {
                $(vm.$refs.assigned_officer).data('select2') ? $(vm.$refs.assigned_officer).select2('destroy') : '';
            }
            // Assigned officer select
            $(vm.$refs.assigned_officer).select2({
                "theme": "bootstrap-5",
                allowClear: true,
                placeholder: "Select Officer"
            }).
                on("select2:select", function (e) {
                    var selected = $(e.currentTarget);
                    if (vm.conservation_status_obj.processing_status == 'With Approver') {
                        vm.conservation_status_obj.assigned_approver = selected.val();
                    }
                    else {
                        vm.conservation_status_obj.assigned_officer = selected.val();
                    }
                    vm.assignTo();
                }).on("select2:unselecting", function (e) {
                    var self = $(this);
                    setTimeout(() => {
                        self.select2('close');
                    }, 0);
                }).on("select2:unselect", function (e) {
                    var selected = $(e.currentTarget);
                    if (vm.conservation_status_obj.processing_status == 'With Approver') {
                        vm.conservation_status_obj.assigned_approver = null;
                    }
                    else {
                        vm.conservation_status_obj.assigned_officer = null;
                    }
                    vm.assignTo();
                });
        },
        fetchDeparmentUsers: function () {
            let vm = this;
            vm.loading.push('Loading Department Users');
            vm.$http.get(api_endpoints.department_users).then((response) => {
                vm.department_users = response.body
                vm.loading.splice('Loading Department Users', 1);
            }, (error) => {
                console.log(error);
                vm.loading.splice('Loading Department Users', 1);
            })
        },
        initialiseSelects: function () {
            let vm = this;
            if (!vm.initialisedSelects) {
                $(vm.$refs.department_users).select2({
                    minimumInputLength: 2,
                    "theme": "bootstrap-5",
                    allowClear: true,
                    placeholder: "Select Referral",
                    ajax: {
                        url: api_endpoints.users_api + '/get_department_users/',
                        dataType: 'json',
                        data: function (params) {
                            var query = {
                                term: params.term,
                                type: 'public',
                            }
                            return query;
                        },
                    },
                })
                    .on("select2:select", function (e) {
                        let data = e.params.data.id;
                        vm.selected_referral = data;
                    })
                    .on("select2:unselect", function (e) {
                        var selected = $(e.currentTarget);
                        vm.selected_referral = null;
                    })
                vm.initialiseAssignedOfficerSelect();
                vm.initialisedSelects = true;
            }
        },
        sendReferral: function () {
            let vm = this;
            let formData = new FormData(vm.form);
            vm.sendingReferral = true;
            let payload = new Object();
            Object.assign(payload, vm.conservation_status_obj);
            vm.$http.post(vm.species_community_cs_form_url, payload).then(res => {

                let data = { 'email': vm.selected_referral, 'text': vm.referral_text };
                vm.$http.post(helpers.add_endpoint_json(api_endpoints.cs_referrals, (vm.referral.id + '/send_referral')), JSON.stringify(data), {
                    emulateJSON: true
                }).then((response) => {
                    vm.sendingReferral = false;
                    vm.referral = response.body;
                    swal.fire({
                        title: 'Referral Sent',
                        text: 'The referral has been sent to ' + vm.department_users.find(d => d.email == vm.selected_referral).name,
                        icon: 'success',
                        confirmButtonColor: '#226fbb'
                    });
                    $(vm.$refs.department_users).val(null).trigger("change");
                    vm.selected_referral = '';
                    vm.referral_text = '';
                }, (error) => {
                    console.log(error);
                    swal.fire({
                        title: 'Referral Error',
                        text: helpers.apiVueResourceError(error),
                        icon: 'error',
                        confirmButtonColor: '#226fbb'
                    });
                    vm.sendingReferral = false;
                });
            }, err => {
                console.log(err);
                vm.sendingReferral = false;
            });
        },
        remindReferral: function (r) {
            let vm = this;
            vm.$http.get(helpers.add_endpoint_json(api_endpoints.cs_referrals, r.id + '/remind')).then(response => {
                vm.fetchReferral(vm.referral.id);
                swal.fire({
                    title: 'Referral Reminder',
                    text: 'A reminder has been sent to ' + vm.department_users.find(d => d.id == r.referral).name,
                    icon: 'success',
                    confirmButtonColor: '#226fbb'
                });
            },
                error => {
                    swal.fire({
                        title: 'Referral Reminder Error',
                        text: helpers.apiVueResourceError(error),
                        icon: 'error',
                        confirmButtonColor: '#226fbb'
                    });
                });
        },
        recallReferral: function (r) {
            let vm = this;
            swal.fire({
                title: "Loading...",
                allowOutsideClick: false,
                allowEscapeKey: false,
                onOpen: () => {
                    swal.showLoading()
                }
            })

            vm.$http.get(helpers.add_endpoint_json(api_endpoints.cs_referrals, r.id + '/recall')).then(response => {
                swal.hideLoading();
                swal.close();
                vm.fetchReferral(vm.referral.id);
                swal.fire({
                    title: 'Referral Recall',
                    text: 'The referral has been recalled from ' + vm.department_users.find(d => d.id == r.referral).name,
                    icon: 'success',
                    confirmButtonColor: '#226fbb'
                });
            },
                error => {
                    swal.fire({
                        title: 'Referral Recall Error',
                        text: helpers.apiVueResourceError(error),
                        icon: 'error',
                        confirmButtonColor: '#226fbb'
                    });
                });
        },
        resendReferral: function (r) {
            let vm = this;
            vm.$http.get(helpers.add_endpoint_json(api_endpoints.cs_referrals, r.id + '/resend')).then(response => {
                vm.fetchReferral(vm.referral.id);
                swal.fire({
                    title: 'Referral Resent',
                    text: 'The referral has been resent to ' + vm.department_users.find(d => d.id == r.referral).name,
                    icon: 'success',
                    confirmButtonColor: '#226fbb'
                });
            },
                error => {
                    swal.fire({
                        title: 'Referral Resent Error',
                        text: helpers.apiVueResourceError(error),
                        icon: 'error',
                        confirmButtonColor: '#226fbb'
                    });
                });
        },
        fetchReferral: function () {
            let vm = this;
            Vue.http.get(helpers.add_endpoint_json(api_endpoints.cs_referrals, vm.referral.id)).then(res => {
                vm.referral = res.body;
            },
                err => {
                    console.log(err);
                });
        },
        completeReferral: function () {
            let vm = this;
            swal.fire({
                title: "Complete Referral",
                text: "Are you sure you want to complete this referral?",
                icon: "question",
                showCancelButton: true,
                confirmButtonText: 'Submit',
                confirmButtonColor: '#226fbb'
            }).then((result) => {
                if (result.isConfirmed) {
                    let payload = new Object();
                    Object.assign(payload, vm.referral);
                    vm.$http.post(vm.species_community_cs_referral_form_url, payload).then(res => {
                        vm.$http.get(helpers.add_endpoint_json(api_endpoints.cs_referrals, vm.$route.params.referral_id + '/complete')).then(res => {
                            vm.referral = res.body;
                        },
                            error => {
                                swal.fire({
                                    title: 'Referral Error',
                                    text: helpers.apiVueResourceError(error),
                                    icon: 'error',
                                    confirmButtonColor: '#226fbb'
                                });
                            });

                    }, err => {
                        console.log(err);
                    });
                }
            }, (error) => {
                console.log(error);
            });
        }
    },
    mounted: function () {
        let vm = this;
        vm.fetchDeparmentUsers();
    },
    updated: function () {
        let vm = this;
        this.$nextTick(() => {
            vm.initialiseSelects();
            vm.form = document.forms.new_conservation_status;
        });
    },
    created: function () {
        let vm = this;
        if (!vm.referral) {
            Vue.http.get(helpers.add_endpoint_json(api_endpoints.cs_referrals, this.$route.params.referral_id)).then(res => {
                vm.referral = res.body;
            },
                err => {
                    console.log(err);
                });
        }
    },
    beforeRouteEnter: function (to, from, next) {
        Vue.http.get(helpers.add_endpoint_json(api_endpoints.cs_referrals, to.params.referral_id)).then(res => {
            next(vm => {
                vm.referral = res.body;
            });
        },
            err => {
                console.log(err);
            });
    },
}
</script>
