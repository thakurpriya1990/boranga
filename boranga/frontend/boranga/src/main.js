import Vue from 'vue'
import resource from 'vue-resource'
import jszip from 'jszip';
import App from './App'
import router from './router'
import helpers from '@/utils/helpers'
import { extendMoment } from 'moment-range';

import 'datatables.net-bs5';
import 'datatables.net-buttons-bs5';
import 'datatables.net-responsive-bs5';
import 'datatables.net-buttons/js/dataTables.buttons.js';
import jsZip from 'jszip';
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

import api_endpoints from './api'

require('@/../node_modules/@fortawesome/fontawesome-free/css/all.min.css')
require('@/../node_modules/datatables.net-bs5/css/dataTables.bootstrap5.min.css')

extendMoment(moment);


Vue.config.devtools = true;
Vue.config.productionTip = false
Vue.use( resource );

// Add CSRF Token to every request
Vue.http.interceptors.push( function ( request, next ) {
  // modify headers
  if ( request.url != api_endpoints.countries ) {
    request.headers.set( 'X-CSRFToken', helpers.getCookie( 'csrftoken' ) );
  }

  // continue to next interceptor
  next();
} );


/* eslint-disable no-new */
new Vue( {
  el: '#app',
  router,
  template: '<App/>',
  components: {
    App
  }
} )
