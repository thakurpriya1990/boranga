<template lang="html">
    <div class="container">
        <div class="row">
            <div class="col-sm-12">
                <div class="row justify-content-center">
                    <div v-if="isCSProposal" class="col-9 p-3 border rounded">
                        <h3>
                            Conservation Status Proposal Submitted Successfully
                        </h3>
                        <div class="mb-3">
                            <strong
                                >Your
                                {{ conservation_status_obj.group_type }}
                                conservation status proposal has been
                                received.</strong
                            >
                        </div>

                        <table class="table table-sm w-50 mb-4">
                            <tbody>
                                <tr>
                                    <td><strong>Proposal Number:</strong></td>
                                    <td>
                                        {{
                                            conservation_status_obj.conservation_status_number
                                        }}
                                    </td>
                                </tr>
                                <tr>
                                    <td><strong>Date/Time:</strong></td>
                                    <td>
                                        {{
                                            formatDate(
                                                conservation_status_obj.lodgement_date
                                            )
                                        }}
                                    </td>
                                </tr>
                            </tbody>
                        </table>

                        <p>
                            You will receive a notification email if there is
                            any incomplete information or documents missing from
                            the proposal.
                        </p>

                        <router-link
                            :to="{ name: 'external-conservation-status-dash' }"
                            style="margin-top: 15px"
                            class="btn btn-primary"
                            >Return to Conservation Status
                            Dashboard</router-link
                        >
                    </div>
                    <div v-else class="col-9 p-3 border rounded">
                        >
                        <strong
                            >Sorry it looks like there isn't any application
                            currently in your session.</strong
                        >
                        <br /><router-link
                            :to="{ name: 'external-conservation-status-dash' }"
                            style="margin-top: 15px"
                            class="btn btn-primary"
                            >Return to Conservation Status
                            Dashboard</router-link
                        >
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>
<script>
import { api_endpoints } from '@/utils/hooks';
export default {
    data: function () {
        return {
            conservation_status_obj: {},
        };
    },
    computed: {
        isCSProposal: function () {
            return this.conservation_status_obj &&
                this.conservation_status_obj.id
                ? true
                : false;
        },
        application_type_flora: function () {
            return api_endpoints.group_type_flora;
        },
        application_type_fauna: function () {
            return api_endpoints.group_type_fauna;
        },
        application_type_community: function () {
            return api_endpoints.group_type_community;
        },
    },
    created: function () {
        if (!window.history.state.conservation_status_obj) {
            this.$router.push({
                name: 'external-conservation-status-dash',
            });
            return;
        }
        Object.assign(
            this.conservation_status_obj,
            JSON.parse(window.history.state.conservation_status_obj)
        );
    },
    methods: {
        formatDate: function (data) {
            return data ? moment(data).format('DD/MM/YYYY HH:mm:ss') : '';
        },
    },
};
</script>
