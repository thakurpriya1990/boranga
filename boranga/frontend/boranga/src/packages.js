import { extendMoment } from 'moment-range';
import jszip from 'jszip';

//require( 'datatables.net' )();
require( 'datatables.net-bs5' )();
require( 'datatables.net-responsive-bs5' )(window, $);
//require( 'datatables.net-buttons/js/dataTables.buttons.js' )(window, $);
//require( 'datatables.net-buttons/js/buttons.html5.js' )(window, $, jszip);
require("datatables.net-responsive-bs5/css/responsive.bootstrap5.css");


require("sweetalert2/dist/sweetalert2.css");

require('jquery-validation');

extendMoment(moment);
