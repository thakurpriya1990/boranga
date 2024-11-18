<template lang="html">
    <div v-if="conservation_status_obj" class="container" id="internalCSReferral">
        <div class="row">
            <h3><span class="text-capitalize">{{ conservation_status_obj.group_type }}</span> {{
                conservation_status_obj.conservation_status_number }} - Referral</h3>
        </div>
        <div class="row">
            <div class="col-md-3">
                <Submission :submitter_first_name="submitter_first_name" :submitter_last_name="submitter_last_name"
                    :lodgement_date="conservation_status_obj.lodgement_date" class="mb-3" />
                <div class="card card-default sticky-top">
                    <div class="card-header">
                        Referral
                    </div>
                    <div class="card-body">
                        <strong>Status</strong><br />
                        {{ referral.processing_status }}
                    </div>
                    <template
                        v-if="!isFinalised && referral.referral == conservation_status_obj.current_assessor.id && referral.can_be_completed">
                        <div class="card-body border-top pb-0">
                            <strong>Referrer</strong>
                            <div class="alert alert-primary px-1 py-2 mt-2" role="alert">
                                <div class="mb-1">
                                    <i class="bi bi-person-fill"></i> {{ referral.sent_by.fullname }}
                                </div>
                                <div>
                                    <i class="bi bi-envelope"></i> <a :href="'mailto:' + referral.sent_by.email"
                                        target="_balnk">{{ referral.sent_by.email }}</a>
                                </div>
                            </div>
                        </div>
                        <div class="card-body border-top">
                            <strong>Referrer's Comments</strong>
                            <div class="mt-2">
                                <em class="text-muted">"{{ referral.text }}"</em>
                            </div>
                        </div>
                        <div class="card-body border-top">
                            <strong>Your Comments</strong><br />
                            <textarea id="your-comments" class="form-control" rows="6"
                                v-model="referral.referral_comment" autofocus></textarea>
                        </div>
                        <div class="card-body mt-2 border-top">
                            <div class="row mb-3">
                                <strong>Action</strong>
                            </div>
                            <div class="row">
                                <div class="col-sm-12">
                                    <button style="width:80%;" class="btn btn-primary"
                                        :disabled="conservation_status_obj.can_user_edit"
                                        @click.prevent="completeReferral">Complete Referral
                                        Task</button>
                                </div>
                            </div>
                        </div>
                    </template>
                </div>
            </div>
            <div class="col-md-9">
                <div class="row">
                    <template>
                        <div class="">
                            <div class="row">
                                <form :action="species_community_cs_form_url" method="post"
                                    name="new_conservation_status" enctype="multipart/form-data">
                                    <ProposalConservationStatus v-if="conservation_status_obj && profile"
                                        ref="conservation_status" :conservation_status_obj="conservation_status_obj"
                                        :referral="referral" :is_internal="profile.is_internal">
                                    </ProposalConservationStatus>
                                    <input type="hidden" name="csrfmiddlewaretoken" :value="csrf_token" />
                                    <input type='hidden' name="conservation_status_id" :value="1" />
                                    <div class="row" style="margin-bottom: 50px">
                                        <div class="navbar fixed-bottom" style="background-color: #f5f5f5;"
                                            v-if="!conservation_status_obj.can_user_edit && !isFinalised">
                                            <div v-if="!isFinalised" class="container">
                                                <div class="col-md-12 text-end">
                                                    <button class="btn btn-primary pull-right" style="margin-top:5px;"
                                                        @click.prevent="save()">Save
                                                        Changes</button>
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
import Submission from '@common-utils/submission.vue'
import ProposalConservationStatus from '@/components/form_conservation_status.vue'
import {
    api_endpoints,
    helpers
}
    from '@/utils/hooks'
export default {
    name: 'ConservationStatusReferral',
    data: function () {
        return {
            profile: null,
            savingConservationStatus: false,
            referral: null,
        }
    },
    components: {
        datatable,
        Submission,
        ProposalConservationStatus,
    },
    computed: {
        conservation_status_obj: function () {
            return this.referral != null && this.referral != 'undefined' ? this.referral.conservation_status : null;
        },
        csrf_token: function () {
            return helpers.getCookie('csrftoken')
        },
        species_community_cs_form_url: function () {
            return `/api/conservation_status/${this.conservation_status_obj.id}/conservation_status_save.json`;
        },
        species_community_cs_referral_form_url: function () {
            return `/api/cs_referrals/${this.referral.id}/conservation_status_referral_save.json`;
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
        isFinalised: function () {
            return !(this.referral != null && this.referral.processing_status == 'Awaiting');
        },
    },
    methods: {
        save: function () {
            let vm = this;
            vm.savingConservationStatus = true;
            let payload = new Object();
            Object.assign(payload, vm.referral);
            vm.$http.post(vm.species_community_cs_referral_form_url, payload).then(res => {
                swal.fire({
                    title: 'Saved',
                    text: 'Your changes have been saved',
                    icon: 'success',
                    customClass: {
                        confirmButton: 'btn btn-primary',
                    },
                });
                vm.savingConservationStatus = false;
            }, err => {
                vm.savingConservationStatus = false;
            });
        },
        refreshFromResponse: function (response) {
            let vm = this;
            vm.conservation_status_obj = helpers.copyObject(response.body);
        },
        completeReferral: function () {
            let vm = this;
            if ($('#your-comments').val().trim().length == 0) {
                swal.fire({
                    title: 'Referral Error',
                    text: 'Please provide a comment before completing the referral',
                    icon: 'error',
                    customClass: {
                        confirmButton: 'btn btn-primary',
                    },
                    didClose: function () {
                        $('#your-comments').focus();
                    }
                });
                return;
            }
            swal.fire({
                title: "Complete Referral",
                text: "Are you sure you want to complete this referral?",
                icon: "question",
                showCancelButton: true,
                confirmButtonText: 'Complete Referral',
                customClass: {
                    confirmButton: 'btn btn-primary',
                    cancelButton: 'btn btn-secondary'
                },
                reverseButtons: true
            }).then((result) => {
                if (result.isConfirmed) {
                    let payload = new Object();
                    Object.assign(payload, vm.referral);
                    vm.$http.post(vm.species_community_cs_referral_form_url, payload).then(res => {
                        vm.$http.patch(helpers.add_endpoint_json(api_endpoints.cs_referrals, vm.$route.params.referral_id + '/complete')).then(res => {
                            vm.referral = Object.assign({}, res.body);
                        },
                            error => {
                                swal.fire({
                                    title: 'Referral Error',
                                    text: helpers.apiVueResourceError(error),
                                    icon: 'error',
                                    customClass: {
                                        confirmButton: 'btn btn-primary',
                                    },
                                });
                            });

                    }, err => {
                        console.log(err);
                    });
                }
            }, (error) => {
                console.log(error);
            });
        },
        fetchReferral: function () {
            let vm = this;
            Vue.http.get(helpers.add_endpoint_json(api_endpoints.cs_referrals, vm.$route.params.referral_id)).then(res => {
                vm.referral = Object.assign({}, res.body);
            },
                err => {
                    console.log(err);
                });
        },
        fetchProfile() {
            this.$http.get(api_endpoints.profile)
                .then(response => {
                    this.profile = response.data
                })
                .catch(error => {
                    console.log(error)
                })
        },
    },
    created: function () {
        this.fetchProfile();
        if (!this.referral) {
            this.fetchReferral();
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
