<template lang="html">
    <div class="container">
        <div class="row">
            <div class="col-sm-12">
                <div class="row">
                    <div v-if="isCSProposal" class="col-sm-offset-3 col-sm-6 borderDecoration">
                        <div v-if="conservation_status_obj.group_type == application_type_flora">
                            <strong>Your flora conservation status proposal has been successfully submitted.</strong>
                            <br />
                        </div>
                        <div v-else-if="conservation_status_obj.group_type == application_type_fauna">
                            <strong>Your fauna conservation status proposal has been successfully submitted.</strong>
                            <br />
                        </div>
                        <div v-else-if="conservation_status_obj.group_type == application_type_community">
                            <strong>Your community conservation status proposal has been successfully
                                submitted.</strong>
                            <br />
                        </div>
                        <table>
                            <tr>
                                <td><strong>Proposal Number:</strong></td>
                                <td><strong>{{ conservation_status_obj.conservation_status_number }}</strong></td>
                            </tr>
                            <tr>
                                <td><strong>Date/Time:</strong></td>
                                <td><strong> {{ conservation_status_obj.lodgement_date | formatDate }}</strong></td>
                            </tr>
                        </table>
                        <br />
                        <label>You will receive a notification email if there is any incomplete information or documents
                            missing from the proposal.</label>
                        <router-link :to="{ name: 'external-conservation_status-dash' }" style="margin-top:15px;"
                            class="btn btn-primary">Back to home</router-link>
                    </div>
                    <div v-else class="col-sm-offset-3 col-sm-6 borderDecoration">
                        <strong>Sorry it looks like there isn't any application currently in your session.</strong>
                        <br /><router-link :to="{ name: 'external-conservation_status-dash' }" style="margin-top:15px;"
                            class="btn btn-primary">Back to home</router-link>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>
<script>
import {
    api_endpoints,
}
    from '@/utils/hooks'
export default {
    data: function () {
        let vm = this;
        return {
            "conservation_status_obj": {},
        }
    },
    computed: {
        isCSProposal: function () {
            return this.conservation_status_obj && this.conservation_status_obj.id ? true : false;
        },
        application_type_flora: function () {
            return api_endpoints.group_type_flora;
        },
        application_type_fauna: function () {
            return api_endpoints.group_type_fauna;
        },
        application_type_community: function () {
            return api_endpoints.group_type_community;
        }
    },
    filters: {
        formatDate: function (data) {
            return data ? moment(data).format('DD/MM/YYYY HH:mm:ss') : '';
        }
    },
    mounted: function () {
        let vm = this;
        vm.form = document.forms.new_cs_proposal;
    },
    beforeRouteEnter: function (to, from, next) {
        next(vm => {
            vm.conservation_status_obj = to.params.conservation_status_obj;
            console.log(vm.conservation_status_obj)
        })
    }
}
</script>

<style lang="css" scoped>
.borderDecoration {
    border: 1px solid;
    border-radius: 5px;
    padding: 50px;
    margin-top: 70px;
}
</style>
