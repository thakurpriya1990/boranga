import { createApp } from 'vue';
import App from './App'
import router from './router'
import helpers from '@/utils/helpers'
import { extendMoment } from 'moment-range';

import 'datatables.net-bs5';
import 'datatables.net-buttons-bs5';
import 'datatables.net-responsive-bs5';
import 'datatables.net-buttons/js/dataTables.buttons.js';
const jsZip = require('jszip');
window.JSZip = jsZip;
import 'datatables.net-buttons/js/buttons.html5.js';
import 'select2';
import 'jquery-validation';

import 'sweetalert2/dist/sweetalert2.css';
import '@/../node_modules/@fortawesome/fontawesome-free/css/all.min.css';
import 'select2/dist/css/select2.min.css';
import 'select2-bootstrap-5-theme/dist/select2-bootstrap-5-theme.min.css';
import '@/../node_modules/datatables.net-bs5/css/dataTables.bootstrap5.min.css';
import '@/../node_modules/datatables.net-responsive-bs5/css/responsive.bootstrap5.min.css';

require('@/../node_modules/@fortawesome/fontawesome-free/css/all.min.css')
require('@/../node_modules/datatables.net-bs5/css/dataTables.bootstrap5.min.css')

extendMoment(moment);

// Add CSRF Token to every request
const customHeaders = new Headers({
    'X-CSRFToken': helpers.getCookie('csrftoken'),
});
const customHeadersJSON = new Headers({
    'X-CSRFToken': helpers.getCookie('csrftoken'),
    'Content-Type': 'application/json',
});

const app = createApp(App);

const fetch = window.fetch;
window.fetch = ((originalFetch) => {
    return (...args) => {
        if (args.length > 1) {
            if (typeof args[1].body === 'string') {
                args[1].headers = customHeadersJSON;
            } else {
                args[1].headers = customHeaders;
            }
        }
        const result = originalFetch.apply(this, args);
        return result;
    };
})(fetch);

app.use(router);
router.isReady().then(() => app.mount('#app'));
