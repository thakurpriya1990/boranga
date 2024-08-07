<template>
    <div v-if="profile" class="container" id="internal-home">
        <h2 class="mb-4">
            Welcome back {{ profile ? profile.first_name : '' }}
        </h2>
        <div>
            <div class="row">
                <div class="col-4">
                    <div class="card">
                        <div class="card-body">
                            <h4 class="card-title mb-3">My Profile<i class="bi bi-person-fill ps-2 text-primary"></i></h4>
                            <div
                                class="table-responsive"
                            >
                                <table
                                    class="table table-sm "
                                >
                                    <tbody>
                                        <tr>
                                            <td scope="row" class="fw-bold">Name</td>
                                            <td>{{ profile.full_name }}</td>
                                        </tr>
                                        <tr>
                                            <td scope="row" class="fw-bold">Email</td>
                                            <td>{{ profile.email }}</td>
                                        </tr>
                                        <tr v-if="profile.phone_number">
                                            <td scope="row" class="fw-bold">Phone Number</td>
                                            <td>{{ profile.phone_number }}</td>
                                        </tr>
                                        <tr v-if="profile.mobile_number">
                                            <td scope="row" class="fw-bold">Mobile</td>
                                            <td>{{ profile.mobile_number }}</td>
                                        </tr>
                                    </tbody>
                                </table>
                                <a role="button" class="btn btn-primary btn-sm" href="/ledger-ui/accounts">
                                    Manage Account <i class="bi bi-person-gear"></i>
                                </a>
                            </div>
                        </div>
                    </div>
                </div>
                <div class="col-4">
                    <div class="card">
                        <div class="card-body">
                            <h4 class="card-title mb-3">My Area of Interest<i
                                    class="bi bi-search-heart ps-2 text-primary"></i></h4>
                            <div class="mb-4">
                                <select type="text" class="form-select text-muted" name="area-of-interest"
                                    id="area-of-interest" placeholder="Name" v-model="profile.area_of_interest"
                                    @change="updateAreaOfInterest">
                                    <option :value="null">No Specific Area</option>
                                    <option value="flora">Flora</option>
                                    <option value="fauna">Fauna</option>
                                    <option value="community">Communities</option>
                                </select>
                            </div>
                            <div id="emailHelp" class="form-text">
                                <p>This setting controls which tab will automatically be
                                    opened
                                    when browsing the Species and Communities, Conservation Status and Occurrences
                                    pages.</p>
                                <p>
                                    If you are planning to access more than one area regularly it is recommended
                                    that you leave this set as 'No Specific Area'
                                </p>
                            </div>
                        </div>
                    </div>
                </div>
                <div class="col-4">
                    <div class="card">
                        <div class="card-body">
                            <h4 class="card-title mb-3">My Groups<i class="bi bi-people-fill ps-2 text-primary"></i>
                            </h4>
                            <p class="card-text text-muted">You are a member of the following groups:</p>
                            <span v-for="group in profile.groups" class="badge bg-primary me-2 p-2 mb-2">{{ group
                                }}</span>
                            <div v-if="profile.is_superuser" class="mt-3">
                                <span class="badge bg-success me-2 p-2 mb-2">You are a Superuser</span>
                            </div>
                            <div v-if="profile.is_superuser">
                                <small class="text-muted">* Superusers are a member of every group by
                                    default</small>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>

<script>
import { api_endpoints } from '@/utils/hooks'

export default {
    name: 'Home',
    data() {
        return {
            profile: null,
        }
    },
    computed: {
        lastLogin: function () {
            if (!this.profile) {
                return '';
            }
            let localDate = new Date(this.profile.last_login);
            return `${localDate.toLocaleDateString()} at ${localDate.toLocaleTimeString()}`;
        }
    },
    methods: {
        updateAreaOfInterest: function () {
            let vm = this;
            vm.$http.patch(api_endpoints.save_area_of_interest, { area_of_interest: vm.profile.area_of_interest }).then(async (response) => {
                vm.profile.area_of_interest = await response.body.area_of_interest;
            }, (error) => {
                console.log(error);
            });
            // Reset default tabs for each page
            localStorage.removeItem('speciesCommunitiesActiveTab');
            localStorage.removeItem('conservationStatusActiveTab');
            localStorage.removeItem('occurrenceActiveTab');
        },
        fetchProfile: function () {
            let vm = this;
            vm.$http.get(api_endpoints.profile).then(async (response) => {
                vm.profile = await response.body;
            }, (error) => {

            });
        }
    },
    created: function () {
        // env variable is set in base.html template from django
        var user_is_authenticated = `${env['user_is_authenticated']}`
        if(user_is_authenticated.toString() === 'true') {
            this.fetchProfile();
        }
    }
}
</script>
