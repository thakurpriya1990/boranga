import api from './api.js';
import { helpers } from '@/utils/hooks';

export default {
    fetchProposal: function (id) {
        return new Promise((resolve, reject) => {
            fetch(helpers.add_endpoint_json(api.proposals, id)).then(
                (response) => {
                    resolve(response.body);
                },
                (error) => {
                    reject(error);
                }
            );
        });
    },
    fetchOrganisations: function () {
        return new Promise((resolve, reject) => {
            fetch(api.organisations).then(
                (response) => {
                    resolve(response.body);
                },
                (error) => {
                    reject(error);
                }
            );
        });
    },
    fetchCountries: function () {
        return new Promise((resolve, reject) => {
            fetch(api.countries).then(
                (response) => {
                    resolve(response.body);
                },
                (error) => {
                    reject(error);
                }
            );
        });
    },
    fetchOrganisation: function (id) {
        return new Promise((resolve, reject) => {
            fetch(helpers.add_endpoint_json(api.organisations, id)).then(
                (response) => {
                    resolve(response.body);
                },
                (error) => {
                    reject(error);
                }
            );
        });
    },
    fetchUser: function (id) {
        return new Promise((resolve, reject) => {
            fetch(helpers.add_endpoint_json(api.users, id)).then(
                (response) => {
                    resolve(response.body);
                },
                (error) => {
                    reject(error);
                }
            );
        });
    },
    fetchOrgRequestPending: function (id) {
        return new Promise((resolve, reject) => {
            fetch(
                helpers.add_endpoint_json(
                    api.users,
                    id + '/pending_org_requests'
                )
            ).then(
                (response) => {
                    resolve(response.body);
                },
                (error) => {
                    reject(error);
                }
            );
        });
    },
    fetchProfile: function () {
        return new Promise((resolve, reject) => {
            fetch(api.profile).then(
                (response) => {
                    resolve(response.body);
                },
                (error) => {
                    reject(error);
                }
            );
        });
    },
};
