import { constants, api_endpoints, helpers } from '@/utils/hooks';
import Vue from 'vue' ;

export default {
    fetchUrl: async function (url, options) {
        return new Promise((resolve, reject) => {
            let f = options === undefined ? Vue.http.get(url) : vm.$http.get(url, options);
            f.then(async (response) => {
                const data = await response.json();
                if (!response.ok) {
                    let error =
                        (data.constructor.name === 'Array' && data) ||
                        (data && data.message) ||
                        response.statusText;
                    console.error(error);
                    reject(error);
                }
                resolve(data);
            }
            ,(error) => {
                console.error(`There was an error fetching from ${url}`, error);
                error = new Error(constants.ERRORS.NETWORK_ERROR);
                reject(error);
            })
        });
    },
};