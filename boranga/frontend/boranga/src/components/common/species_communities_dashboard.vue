<template id="proposal_dashboard">
   <!-- <div class="row">
        <div class="col-sm-12">
            <div class="panel panel-default"> 
                 <div class="panel-heading">
                     <h3 class="panel-title"><h3>Species and Communities</h3><small v-if="is_external">View existing applications and lodge new ones</small> 
                        <a :href="'#'+pBody" data-toggle="collapse"  data-parent="#userInfo" expanded="true" :aria-controls="pBody">
                            <span class="glyphicon glyphicon-chevron-up pull-right "></span>
                        </a>
                    </h3>
                </div> -->

                <!-- <div class="panel-body collapse in" :id="pBody"> -->
                <FormSection v-bind:label="filterSpecies" Index="species_and_communities">
                    <div class="row">
                            <div class="col-md-3">
                                <div class="form-group">
                                    <label for="">Species/Community</label>
                                    <select class="form-control" v-model="filterSpecies">
                                    <!-- <select class="form-control"> -->
                                        <option value="Flora">Flora</option>
                                        <option value="Fauna">Fauna</option>
                                        <option value="Community">Community</option>
                                        <!-- <option v-for="s in group_types" :value="s">{{s}}</option> -->
                                    </select>
                                </div>
                            </div>
                    </div>
                    <CollapsibleFilters ref="collapsible_filters" @created="collapsible_component_mounted" label= "Filter">
                        <div class="row">
                            <div class="col-md-3">
                                <div class="form-group">
                                    <label for="">Group Name</label>
                                    <select class="form-control" v-model="filterProposalStatus">
                                        <option value="All">All</option>
                                        <option v-for="s in group_types" :value="s">{{s}}</option>
                                    </select>
                                </div>
                            </div>
                            <div class="col-md-3">
                                <div class="form-group">
                                    <label for="">Scientific Name</label>
                                    <select class="form-control" v-model="filterProposalStatus">
                                        <option value="All">All</option>
                                        <option v-for="s in approval_status" :value="s">{{s}}</option>
                                    </select>
                                </div>
                            </div>
                            <div class="col-md-3">
                                <div class="form-group">
                                    <label for="">Non-current Name</label>
                                    <select class="form-control" v-model="filterApplicationType">
                                        <option value="All">All</option>
                                        <option v-for="s in application_types" :value="s">{{s}}</option>
                                    </select>
                                </div>
                            </div>
                            <div class="col-md-3">
                                <div class="form-group">
                                    <label for="">Status</label>
                                    <select class="form-control" v-model="filterApplicationType">
                                        <option value="All">All</option>
                                        <option v-for="s in application_types" :value="s">{{s}}</option>
                                    </select>
                                </div>
                            </div>

                            <div v-if="is_external" class="col-md-6">
                                <router-link  style="margin-top:25px;" class="btn btn-primary pull-right" :to="{ name: 'apply_proposal' }">New Application</router-link>
                            </div>
                        </div>
                    </CollapsibleFilters>

                    <div class="row">
                    <div class="col-lg-12">
                        <datatable
                                ref="proposal_datatable"
                                :id="datatable_id"
                                :dtOptions="datatable_options"
                                :dtHeaders="datatable_headers"
                            />
                    </div>
                    </div>
                </FormSection>
                <!-- </div> -->
<!--            </div>
        </div>
    </div> -->
</template>
<script>
import "babel-polyfill"
import datatable from '@/utils/vue/datatable.vue'
import CollapsibleFilters from '@/components/forms/collapsible_component.vue'
import FormSection from '@/components/forms/section_toggle.vue'
import Vue from 'vue'
require("select2/dist/css/select2.min.css");
require("select2-bootstrap-theme/dist/select2-bootstrap.min.css");
//require("babel-polyfill"); /* only one of 'import' or 'require' is necessary */
import {
    api_endpoints,
    helpers
}from '@/utils/hooks'
export default {
    name: 'ProposalTableDash',
    props: {
        level:{
            type: String,
            required: true,
            validator:function(val) {
                let options = ['internal','referral','external'];
                return options.indexOf(val) != -1 ? true: false;
            }
        },
        url:{
            type: String,
            required: true
        },
    },
    data() {
        let vm = this;
        return {
            pBody: 'pBody' + vm._uid,
            datatable_id: 'proposal-datatable-'+vm._uid,
     
            //Profile to check if user has access to process Proposal
            profile: {},
            is_payment_admin: false,
            
            // selected values for filtering
            filterSpecies: '',
            filterApplicationType: 'All',
            filterProposalStatus: 'All',
            filterProposalLodgedFrom: '',
            filterProposalLodgedTo: '',
            filterProposalSubmitter: 'All',

            dateFormat: 'DD/MM/YYYY',
            datepickerOptions:{
                format: 'DD/MM/YYYY',
                showClear:true,
                useCurrent:false,
                keepInvalid:true,
                allowInputToggle:true
            },
            // filtering options
            external_status:[
                {value: 'draft', name: 'Draft'},
                {value: 'with_assessor', name: 'Under Review'},
                {value: 'approved', name: 'Approved'},
                {value: 'declined', name: 'Declined'},
                {value: 'discarded', name: 'Discarded'},
                {value: 'awaiting_payment', name: 'Awaiting Payment'},
            ],
            internal_status:[
                {value: 'draft', name: 'Draft'},
                {value: 'with_assessor', name: 'With Assessor'},
                {value: 'on_hold', name: 'On Hold'},
                {value: 'with_qa_officer', name: 'With QA Officer'},
                {value: 'with_referral', name: 'With Referral'},
                {value: 'with_assessor_requirements', name: 'With Assessor (Requirements)'},
                {value: 'with_approver', name: 'With Approver'},
                {value: 'approved', name: 'Approved'},
                {value: 'declined', name: 'Declined'},
                {value: 'discarded', name: 'Discarded'},
                {value: 'awaiting_payment', name: 'Awaiting Payment'},
            ],
            proposal_submitters: [],
            proposal_status: [],

        }
    },
    components:{
        datatable,
        CollapsibleFilters,
        FormSection,
    },
    watch:{
        filterProposalSubmitter: function(){
            let vm = this;
            vm.$refs.proposal_datatable.vmDataTable.draw(); // This calls ajax() backend call.  This line is enough to search?  Do we need following lines...?
            /*if (vm.filterProposalSubmitter!= 'All') {
                vm.$refs.proposal_datatable.vmDataTable.columns(2).search(vm.filterProposalSubmitter).draw();
            } else {
                vm.$refs.proposal_datatable.vmDataTable.columns(2).search('').draw();
            }*/
        },
        filterSpecies: function() {
            let vm = this;
            if (vm.filterSpecies!= 'All') {
                vm.$refs.proposal_datatable.vmDataTable.columns(4).search(vm.filterSpecies).draw();
            } else {
                vm.$refs.proposal_datatable.vmDataTable.columns(4).search('').draw();
            }
        },
        filterProposalStatus: function() {
            let vm = this;
            if (vm.filterProposalStatus!= 'All') {
                vm.$refs.proposal_datatable.vmDataTable.columns(4).search(vm.filterProposalStatus).draw();
            } else {
                vm.$refs.proposal_datatable.vmDataTable.columns(4).search('').draw();
            }
        },
        filterApplicationType: function() {
            let vm = this;
            if (vm.filterApplicationType!= 'All') {
                vm.$refs.proposal_datatable.vmDataTable.columns(1).search(vm.filterApplicationType).draw();
            } else {
                vm.$refs.proposal_datatable.vmDataTable.columns(1).search('').draw();
            }
        },
        filterProposalLodgedFrom: function(){
            this.$refs.proposal_datatable.vmDataTable.draw();
        },
        filterProposalLodgedTo: function(){
            this.$refs.proposal_datatable.vmDataTable.draw();
        },
        filterApplied: function(){
            if (this.$refs.collapsible_filters){
                // Collapsible component exists
                this.$refs.collapsible_filters.show_warning_icon(this.filterApplied)
            }
        },
    },
    computed: {
        filterApplied: function(){
            if(this.filterApplicationType.toLowerCase() === 'all' && this.filterProposalStatus.toLowerCase() === 'all' && this.filterProposalLodgedFrom.toLowerCase() === '' && this.filterProposalLodgedTo.toLowerCase() === ''){
                return false
            } else {
                return true
            }
        },
        is_external: function(){
            return this.level == 'external';
        },
        is_internal: function() {
            return this.level == 'internal'
        },
        is_referral: function(){
            return this.level == 'referral';
        },
        datatable_headers: function(){
            if (this.is_external){
                return ['id', 'Number', 'Licence Type', 'Submitter', 'Applicant', 'Status', 'Lodged on', 'Action']
            }
            if (this.is_internal){
                return ['id', 'Number', 'Licence Type', 'Submitter', 'Applicant', 'Status', 'Lodged on', 'Assigned Officer', 'Action']
            }
        },
        column_id: function(){
            return {
                // 1. ID
                data: "id",
                orderable: false,
                searchable: false,
                visible: false,
                'render': function(data, type, full){
                    console.log(full)
                    return full.id
                }
            }
        },
        column_lodgement_number: function(){
            return {
                // 2. Lodgement Number
                data: "id",
                orderable: true,
                searchable: true,
                visible: true,
                'render': function(data, type, full){
                    return full.lodgement_number
                },
                name: "id, lodgement_number",
            }
        },
        column_application_type: function(){
            return {
                // 3. Application Type
                data: "application_type",
                orderable: true,
                searchable: true,
                visible: true,
                'render': function(data, type, full){
                    return full.application_type
                },
                name: "application_type__name",
            }
        },
        column_submitter: function(){
            return {
                // 4. Submitter
                data: "submitter",
                orderable: true,
                searchable: true,
                visible: true,
                'render': function(data, type, full){
                    if(data.first_name){
                        return `${data.first_name} ${data.last_name}`;
                    }
                    // Should not reach here
                    return ''
                },
                name: "submitter__email",
            }
        },
        column_applicant: function(){
            return {
                // 5. Applicant
                data: "applicant",
                orderable: true,
                searchable: true,
                visible: true,
                'render': function(data, type, full){
                    if(full.applicant){
                        return full.applicant;
                    }
                    // Should not reach here
                    return ''
                },
                name: "org_applicant__organisation__name, proxy_applicant__email, proxy_applicant__first_name, proxy_applicant__last_name",
            }
        },
        column_status: function(){
            return {
                // 6. Status
                data: "processing_status",
                orderable: true,
                searchable: true,
                visible: true,
                'render': function(data, type, full){
                    if(full.processing_status){
                        return full.processing_status;
                    }
                    // Should not reach here
                    return ''
                },
                name: "processing_status",
            }
        },
        column_lodged_on: function(){
            return {
                // 7. Lodged on
                data: "lodgement_date",
                orderable: true,
                searchable: false, // handles by filter_queryset override method - class ProposalFilterBackend
                visible: true,
                'render': function(data, type, full){
                    if (full.lodgement_date){
                        return moment(full.lodgement_date).format('DD/MM/YYYY');
                    }
                    // Should not reach here
                    return ''
                }
            }
        },
        column_assigned_officer: function(){
            return {
                // 8. Assigned Officer
                data: "assigned_officer",
                orderable: true,
                searchable: true,
                visible: true,
                'render': function(data, type, full){
                    if (full.assigned_officer){
                        return full.assigned_officer;
                    }
                    // Should not reach here
                    return ''
                },
                name: "assigned_officer__first_name,assigned_officer__last_name",
            }
        },
        column_action: function(){
            let vm = this
            return {
                // 9. Action
                data: "id",
                orderable: false,
                searchable: false,
                visible: true,
                'render': function(data, type, full){
                    let links = "";
                    if (!vm.is_external){
                        /*if(vm.check_assessor(full) && full.can_officer_process)*/
                        if(full.assessor_process){   
                                links +=  `<a href='/internal/species_communities/${full.id}'>Process</a><br/>`;    
                        }
                        else{
                            links +=  `<a href='/internal/species_communities/${full.id}'>View</a><br/>`;
                        }
                    }
                    else{
                        if (full.can_user_edit) {
                            links +=  `<a href='/external/species_communities/${full.id}'>Continue</a><br/>`;
                            links +=  `<a href='#${full.id}' data-discard-proposal='${full.id}'>Discard</a><br/>`;
                        }
                        else if (full.can_user_view) {
                            links +=  `<a href='/external/species_communities/${full.id}'>View</a>`;
                        }
                    }

                    links +=  `<a href='/internal/species_communities/${full.id}'>Edit</a><br/>`; // Dummy addition for Boranaga demo

                    return links;
                }
            }
        },
        datatable_options: function(){
            let vm = this

            let columns = []
            let search = null
            let buttons = []
            if(vm.is_external){
                columns = [
                    vm.column_id,
                    vm.column_lodgement_number,
                    vm.column_application_type,
                    vm.column_submitter,
                    vm.column_applicant,
                    vm.column_status,
                    vm.column_lodged_on,
                    vm.column_action,
                ]
                search = false
                buttons = []
            }
            if(vm.is_internal){
                columns = [
                    vm.column_id,
                    vm.column_lodgement_number,
                    vm.column_application_type,
                    vm.column_submitter,
                    vm.column_applicant,
                    vm.column_status,
                    vm.column_lodged_on,
                    vm.column_assigned_officer,
                    vm.column_action,
                ]
                search = true
                buttons = [
                    {
                        extend: 'excel',
                        exportOptions: {
                            columns: ':visible'
                        }
                    },
                    {
                        extend: 'csv',
                        exportOptions: {
                            columns: ':visible'
                        }
                    },
                ]
            }

            return {
                autoWidth: false,
                language: {
                    processing: "<i class='fa fa-4x fa-spinner fa-spin'></i>"
                },
                //lengthMenu: [ [10, 25, 50, 100, -1], [10, 25, 50, 100, "All"] ],
                responsive: true,
                serverSide: true,
                searching: search,
                ajax: {
                    "url": vm.url,
                    "dataSrc": 'data',

                    // adding extra GET params for Custom filtering
                    "data": function ( d ) {
                        d.date_from = vm.filterProposalLodgedFrom != '' && vm.filterProposalLodgedFrom != null ? moment(vm.filterProposalLodgedFrom, 'DD/MM/YYYY').format('YYYY-MM-DD'): '';
                        d.date_to = vm.filterProposalLodgedTo != '' && vm.filterProposalLodgedTo != null ? moment(vm.filterProposalLodgedTo, 'DD/MM/YYYY').format('YYYY-MM-DD'): '';
                    }
                },
                dom: 'lBfrtip',
                //buttons:[ ],
                buttons: buttons,

                columns: columns,
                processing: true,
                initComplete: function() {
                },
            }
        }
    
    },
    methods:{
        make_payment: function(fee_invoice_reference){
        //make_payment2: function(){
            vm.$http.post('/existing_invoice_payment/' + fee_invoice_reference).then((response) => {
                vm.res = response.body;
            },(error) => {
                console.log(error);
            })

        },
        make_payment2: function (fee_invoice_reference) {
            let vm = this;
            var form = document.forms.new_payment;
            if (vm.payment_method == 'existing_invoice') {
                form.action = '/existing_invoice_payment/' + fee_invoice_reference  + '/?method=' + vm.payment_method;
                form.submit();
            }
        },
        collapsible_component_mounted: function(){
            this.$refs.collapsible_filters.show_warning_icon(this.filterApplied)
        },

        fetchFilterLists: function(){
            let vm = this;

            //vm.$http.get('/api/list_proposal/filter_list/').then((response) => {
            vm.$http.get(api_endpoints.filter_list).then((response) => {
                vm.proposal_submitters = response.body.submitters;
                vm.application_types= response.body.application_types;
                //vm.proposal_status = vm.level == 'internal' ? response.body.processing_status_choices: response.body.customer_status_choices;
                vm.proposal_status = vm.level == 'internal' ? vm.internal_status: vm.external_status;
            },(error) => {
                console.log(error);
            })
            //console.log(vm.regions);
        },

        discardProposal:function (proposal_id) {
            let vm = this;
            swal({
                title: "Discard Application",
                text: "Are you sure you want to discard this proposal?",
                type: "warning",
                showCancelButton: true,
                confirmButtonText: 'Discard Application',
                confirmButtonColor:'#d9534f'
            }).then(() => {
                vm.$http.delete(api_endpoints.discard_proposal(proposal_id))
                .then((response) => {
                    swal(
                        'Discarded',
                        'Your proposal has been discarded',
                        'success'
                    )
                    vm.$refs.proposal_datatable.vmDataTable.ajax.reload();
                }, (error) => {
                    console.log(error);
                });
            },(error) => {

            });
        },
        addEventListeners: function(){
            let vm = this;
            // Initialise Proposal Date Filters
            $(vm.$refs.proposalDateToPicker).datetimepicker(vm.datepickerOptions);
            $(vm.$refs.proposalDateToPicker).on('dp.change', function(e){
                if ($(vm.$refs.proposalDateToPicker).data('DateTimePicker').date()) {
                    vm.filterProposalLodgedTo =  e.date.format('DD/MM/YYYY');
                }
                else if ($(vm.$refs.proposalDateToPicker).data('date') === "") {
                    vm.filterProposaLodgedTo = "";
                }
             });
            $(vm.$refs.proposalDateFromPicker).datetimepicker(vm.datepickerOptions);
            $(vm.$refs.proposalDateFromPicker).on('dp.change',function (e) {
                if ($(vm.$refs.proposalDateFromPicker).data('DateTimePicker').date()) {
                    vm.filterProposalLodgedFrom = e.date.format('DD/MM/YYYY');
                    $(vm.$refs.proposalDateToPicker).data("DateTimePicker").minDate(e.date);
                }
                else if ($(vm.$refs.proposalDateFromPicker).data('date') === "") {
                    vm.filterProposalLodgedFrom = "";
                }
            });
            // End Proposal Date Filters
            // External Discard listener
            vm.$refs.proposal_datatable.vmDataTable.on('click', 'a[data-discard-proposal]', function(e) {
                e.preventDefault();
                var id = $(this).attr('data-discard-proposal');
                vm.discardProposal(id);
            });
        },
        initialiseSearch:function(){
            this.submitterSearch();
            this.dateSearch();
        },
        submitterSearch:function(){
            let vm = this;
            vm.$refs.proposal_datatable.table.dataTableExt.afnFiltering.push(
                function(settings,data,dataIndex,original){
                    let filtered_submitter = vm.filterProposalSubmitter;
                    if (filtered_submitter == 'All'){ return true; } 
                    return filtered_submitter == original.submitter.email;
                }
            );
        },
        dateSearch:function(){
            let vm = this;
            vm.$refs.proposal_datatable.table.dataTableExt.afnFiltering.push(
                function(settings,data,dataIndex,original){
                    let from = vm.filterProposalLodgedFrom;
                    let to = vm.filterProposalLodgedTo;
                    let val = original.lodgement_date;

                    if ( from == '' && to == ''){
                        return true;
                    }
                    else if (from != '' && to != ''){
                        return val != null && val != '' ? moment().range(moment(from,vm.dateFormat),moment(to,vm.dateFormat)).contains(moment(val)) :false;
                    }
                    else if(from == '' && to != ''){
                        if (val != null && val != ''){
                            return moment(to,vm.dateFormat).diff(moment(val)) >= 0 ? true : false;
                        }
                        else{
                            return false;
                        }
                    }
                    else if (to == '' && from != ''){
                        if (val != null && val != ''){
                            return moment(val).diff(moment(from,vm.dateFormat)) >= 0 ? true : false;
                        }
                        else{
                            return false;
                        }
                    } 
                    else{
                        return false;
                    }
                }
            );
        },


        fetchProfile: function(){
            let vm = this;
            Vue.http.get(api_endpoints.profile).then((response) => {
                vm.profile = response.body;
                vm.is_payment_admin=response.body.is_payment_admin;
                              
            },(error) => {
                console.log(error);
                
            })
        },

        check_assessor: function(proposal){
            let vm = this;
            if (proposal.assigned_officer)
                {
                    { if(proposal.assigned_officer== vm.profile.full_name)
                        return true;
                    else
                        return false;
                }
            }
            else{
                 var assessor = proposal.allowed_assessors.filter(function(elem){
                    return(elem.id=vm.profile.id)
                });
                
                if (assessor.length > 0)
                    return true;
                else
                    return false;
              
            }
            
        },
    },


    mounted: function(){
        //this.fetchFilterLists();
        this.fetchProfile();
        let vm = this;
        $( 'a[data-toggle="collapse"]' ).on( 'click', function () {
            var chev = $( this ).children()[ 0 ];
            window.setTimeout( function () {
                $( chev ).toggleClass( "glyphicon-chevron-down glyphicon-chevron-up" );
            }, 100 );
        });
        this.$nextTick(() => {
            vm.initialiseSearch();
            vm.addEventListeners();
        });
    }
}
</script>
<style scoped>
.dt-buttons{
    float: right;
}
</style>
