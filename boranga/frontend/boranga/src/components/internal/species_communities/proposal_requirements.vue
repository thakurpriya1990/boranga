<template id="proposal_requirements">
    <div class="col-md-12">
        <div class="row">
            <div class="panel panel-default">
                <div class="panel-heading">
                    <h3 class="panel-title">Requirements
                        <a class="panelClicker" :href="'#'+panelBody" data-toggle="collapse"  data-parent="#userInfo" expanded="false" :aria-controls="panelBody">
                            <span class="glyphicon glyphicon-chevron-down pull-right "></span>
                        </a>
                        <small v-if="proposal.application_type==application_type_filming"><br>Only add requirements that are additional to the general conditions in the Commercial Filming Handbook <a :href="commercial_filming_handbook" target="_blank">here</a>. Please ensure each condition added references a specific park or district and is written in a format consistent with the handbook.</small>
                    </h3>
                </div>
                <div class="panel-body panel-collapse collapse in" :id="panelBody">
                    <form class="form-horizontal" action="index.html" method="post">
                        <div class="col-sm-12">
                            <button v-if="hasAssessorMode || hasReferralMode || hasDistrictAssessorMode" @click.prevent="addRequirement()" style="margin-bottom:10px;" class="btn btn-primary pull-right">Add Requirement</button>
                        </div>
                        <datatable ref="requirements_datatable" :id="'requirements-datatable-'+_uid" :dtOptions="requirement_options" :dtHeaders="requirement_headers"/>
                    </form>
                </div>
            </div>
        </div>
        <RequirementDetail ref="requirement_detail" :proposal_id="proposal.id" :requirements="requirements" :hasReferralMode="hasReferralMode" :referral_group="referral_group" :hasDistrictAssessorMode="hasDistrictAssessorMode" :district_proposal="district_proposal" :district="district"/>
    </div>
</template>
<script>
import {
    api_endpoints,
    constants,
    helpers
}
from '@/utils/hooks'
import datatable from '@vue-utils/datatable.vue'
import RequirementDetail from './proposal_add_requirement.vue'
export default {
    name: 'InternalProposalRequirements',
    props: {
        proposal: Object,
        hasReferralMode:{
            type:Boolean,
            default: false
        },
        hasDistrictAssessorMode:{
            type:Boolean,
            default: false
        },
        referral_group:{
            type:Number,
            default: null
        },
        district_proposal:{
            type:Number,
            default: null

        },
        district:{
            type:Number,
            default: null

        }
    },
    data: function() {
        let vm = this;
        return {
            global_settings:[],
            panelBody: "proposal-requirements-"+vm._uid,
            requirements: [],
            requirement_headers:["Requirement","Due Date","Recurrence","Action","Order","Documents"],
            requirement_options:{
                autoWidth: false,
                language: {
                    processing: constants.DATATABLE_PROCESSING_HTML
                },
                responsive: true,
                ajax: {
                    "url": helpers.add_endpoint_json(api_endpoints.proposals,vm.proposal.id+'/requirements'),
                    "dataSrc": ''
                },
                order: [],
                dom: 'lBfrtip',
                // buttons:[
                // 'excel', 'csv', ], //'copy'
                buttons:[
                {
                    extend: 'excelHtml5',
                    text:"Excel",
                    exportOptions:{
                        orthogonal:'export'
                    }
                },
                {
                    extend: 'csv',
                    text:"CSV",
                    exportOptions:{
                        orthogonal:'export'
                    }
                }
                ], //'copy'
                columns: [
                    {
                        data: "requirement",
                        //orderable: false,
                        'render': function (value, type) {
                            var ellipsis = '...',
                                truncated = _.truncate(value, {
                                    length: 25,
                                    omission: ellipsis,
                                    separator: ' '
                                }),
                                result = '<span>' + truncated + '</span>',
                                popTemplate = _.template('<a href="#" ' +
                                    'role="button" ' +
                                    'data-toggle="popover" ' +
                                    'data-trigger="click" ' +
                                    'data-placement="top auto"' +
                                    'data-html="true" ' +
                                    'data-content="<%= text %>" ' +
                                    '>more</a>');
                            if (_.endsWith(truncated, ellipsis)) {
                                result += popTemplate({
                                    text: value
                                });
                            }

                            //return result;
                            return type=='export' ? value : result;
                        },
                        'createdCell': helpers.dtPopoverCellFn,

                        /*'createdCell': function (cell) {
                            //TODO why this is not working?
                            // the call to popover is done in the 'draw' event
                            $(cell).popover();
                        }*/

                    },
                    {
                        data: "due_date",
                        mRender:function (data,type,full) {
                            return data != '' && data != null ? moment(data).format('DD/MM/YYYY'): '';
                        },
                        orderable: false
                    },
                    {
                        data: "recurrence",
                        mRender:function (data,type,full) {
                            if (full.recurrence){
                                switch(full.recurrence_pattern){
                                    case 1:
                                        return `Once per ${full.recurrence_schedule} week(s)`;
                                    case 2:
                                        return `Once per ${full.recurrence_schedule} month(s)`;
                                    case 3:
                                        return `Once per ${full.recurrence_schedule} year(s)`;
                                    default:
                                        return '';
                                }
                            }
                            return '';
                        },
                        orderable: false
                    },
                    {
                        mRender:function (data,type,full) {
                            let links = '';
                            if (vm.proposal.assessor_mode.has_assessor_mode){
                                if(full.copied_from==null)
                                {
                                    links +=  `<a href='#' class="editRequirement" data-id="${full.id}">Edit</a><br/>`;
                                }
                                //links +=  `<a href='#' class="editRequirement" data-id="${full.id}">Edit</a><br/>`;
                                links +=  `<a href='#' class="deleteRequirement" data-id="${full.id}">Delete</a><br/>`;
                            }
                            else if(vm.hasReferralMode && full.can_referral_edit){
                                    if(full.copied_from==null)
                                {
                                    links +=  `<a href='#' class="editRequirement" data-id="${full.id}">Edit</a><br/>`;
                                }
                                //links +=  `<a href='#' class="editRequirement" data-id="${full.id}">Edit</a><br/>`;
                                links +=  `<a href='#' class="deleteRequirement" data-id="${full.id}">Delete</a><br/>`;
                            }
                            else{
                                if(vm.hasDistrictAssessorMode && full.can_district_assessor_edit){
                                    if(full.copied_from==null)
                                {
                                    links +=  `<a href='#' class="editRequirement" data-id="${full.id}">Edit</a><br/>`;
                                }
                                //links +=  `<a href='#' class="editRequirement" data-id="${full.id}">Edit</a><br/>`;
                                links +=  `<a href='#' class="deleteRequirement" data-id="${full.id}">Delete</a><br/>`;
                                }
                            }
                            return links;
                        },
                        orderable: false
                    },
                    {
                        mRender:function (data,type,full) {
                            let links = '';
                            // TODO check permission to change the order
                            if (vm.proposal.assessor_mode.has_assessor_mode){
                                links +=  `<a class="dtMoveUp" data-id="${full.id}" href='#'><i class="fa fa-angle-up fa-2x"></i></a><br/>`;
                                links +=  `<a class="dtMoveDown" data-id="${full.id}" href='#'><i class="fa fa-angle-down fa-2x"></i></a><br/>`;
                            }
                            else{
                                if(vm.hasReferralMode && full.can_referral_edit){
                                    links +=  `<a class="dtMoveUp" data-id="${full.id}" href='#'><i class="fa fa-angle-up fa-2x"></i></a><br/>`;
                                    links +=  `<a class="dtMoveDown" data-id="${full.id}" href='#'><i class="fa fa-angle-down fa-2x"></i></a><br/>`;
                                }
                                else if(vm.hasDistrictAssessorMode && full.can_district_assessor_edit){
                                    links +=  `<a class="dtMoveUp" data-id="${full.id}" href='#'><i class="fa fa-angle-up fa-2x"></i></a><br/>`;
                                    links +=  `<a class="dtMoveDown" data-id="${full.id}" href='#'><i class="fa fa-angle-down fa-2x"></i></a><br/>`;
                                }
                            }
                            return links;
                        },
                        orderable: false
                    },
                    {
                        data: 'requirement_documents',
                        mRender:function (data,type,full) {
                            let links = '';
                            _.forEach(data, function (doc) {
                                links += '<a href="' + doc._file + '" target="_blank"><p>' + doc.name+ '</p></a><br>';
                            });
                            return links;
                        }
                    },

                ],
                processing: true,
                rowCallback: function ( row, data, index) {
                    if (data.copied_for_renewal && data.require_due_date && !data.due_date) {
                        $('td', row).css('background-color', 'Red');
                        vm.setApplicationWorkflowState(false)
                        //vm.$emit('refreshRequirements',false);
                    }
                },
                drawCallback: function (settings) {
                    $(vm.$refs.requirements_datatable.table).find('tr:last .dtMoveDown').remove();
                    $(vm.$refs.requirements_datatable.table).children('tbody').find('tr:first .dtMoveUp').remove();

                    // Remove previous binding before adding it
                    $('.dtMoveUp').unbind('click');
                    $('.dtMoveDown').unbind('click');

                    // Bind clicks to functions
                    $('.dtMoveUp').click(vm.moveUp);
                    $('.dtMoveDown').click(vm.moveDown);
                },
                preDrawCallback: function (settings) {
                    vm.setApplicationWorkflowState(true)
                    //vm.$emit('refreshRequirements',true);
                }
            }
        }
    },
    watch:{
        hasAssessorMode(){
            // reload the table
            this.updatedRequirements();
        }

    },
    components:{
        datatable,
        RequirementDetail
    },
    computed:{
        hasAssessorMode(){
            return this.proposal.assessor_mode.has_assessor_mode;
        },
        commercial_filming_handbook: function(){
                let vm=this;
                if(vm.global_settings){
                    for(var i=0; i<vm.global_settings.length; i++){
                        if(vm.global_settings[i].key=='commercial_filming_handbook'){
                            return vm.global_settings[i].value;
                        }
                    }
                }
                return '';
        },
        application_type_tclass: function(){
          return api_endpoints.t_class;
        },
        application_type_filming: function(){
          return api_endpoints.filming;
        },
        application_type_event: function(){
          return api_endpoints.event;
        }

    },
    methods:{
        fetchGlobalSettings: function(){
                let vm = this;
                vm.$http.get('/api/global_settings.json').then((response) => {
                    vm.global_settings = response.body;

                },(error) => {
                    console.log(error);
                } );
            },
        addRequirement(){
            this.$refs.requirement_detail.requirement.referral_group=this.referral_group;
            this.$refs.requirement_detail.requirement.district_proposal=this.district_proposal;
            this.$refs.requirement_detail.requirement.district=this.district;
            this.$refs.requirement_detail.isModalOpen = true;
        },
        removeRequirement(_id){
            let vm = this;
            swal({
                title: "Remove Requirement",
                text: "Are you sure you want to remove this requirement?",
                type: "warning",
                showCancelButton: true,
                confirmButtonText: 'Remove Requirement',
                confirmButtonColor:'#d9534f'
            }).then(() => {
                // vm.$http.delete(helpers.add_endpoint_json(api_endpoints.proposal_requirements,_id))
                // .then((response) => {
                //     vm.$refs.requirements_datatable.vmDataTable.ajax.reload();
                // }, (error) => {
                //     console.log(error);
                // });

                vm.$http.get(helpers.add_endpoint_json(api_endpoints.proposal_requirements,_id+'/discard'))
                .then((response) => {
                    vm.$refs.requirements_datatable.vmDataTable.ajax.reload();
                }, (error) => {
                    console.log(error);
                });

            },(error) => {
            });
        },
        fetchRequirements(){
            let vm = this;

            vm.$http.get(api_endpoints.proposal_standard_requirements).then((response) => {
                vm.requirements = response.body
            },(error) => {
                console.log(error);
            })
        },
        editRequirement(_id){
            let vm = this;
            vm.$http.get(helpers.add_endpoint_json(api_endpoints.proposal_requirements,_id)).then((response) => {
                this.$refs.requirement_detail.requirement = response.body;
                this.$refs.requirement_detail.requirement.due_date =  response.body.due_date != null && response.body.due_date != undefined ? moment(response.body.due_date).format('DD/MM/YYYY'): '';
                this.$refs.requirement_detail.requirement.referral_group=response.body.referral_group;
                this.$refs.requirement_detail.requirement.district_proposal=response.body.district_proposal;
                this.$refs.requirement_detail.requirement.district=response.body.district;
                this.$refs.requirement_detail.requirement.requirement_documents=response.body.requirement_documents;
                response.body.standard ? $(this.$refs.requirement_detail.$refs.standard_req).val(response.body.standard_requirement).trigger('change'): '';
                this.addRequirement();
            },(error) => {
                console.log(error);
            })
        },
        updatedRequirements(){
            this.$refs.requirements_datatable.vmDataTable.ajax.reload();
        },
        eventListeners(){
            let vm = this;
            vm.$refs.requirements_datatable.vmDataTable.on('click', '.deleteRequirement', function(e) {
                e.preventDefault();
                var id = $(this).attr('data-id');
                vm.removeRequirement(id);
            });
            vm.$refs.requirements_datatable.vmDataTable.on('click', '.editRequirement', function(e) {
                e.preventDefault();
                var id = $(this).attr('data-id');
                vm.editRequirement(id);
            });
        },
        sendDirection(req,direction){
            let movement = direction == 'down'? 'move_down': 'move_up';
            this.$http.get(helpers.add_endpoint_json(api_endpoints.proposal_requirements,req+'/'+movement)).then((response) => {
            },(error) => {
                console.log(error);

            })
        },
        moveUp(e) {
            // Move the row up
            let vm = this;
            e.preventDefault();
            var tr = $(e.target).parents('tr');
            vm.moveRow(tr, 'up');
            vm.sendDirection($(e.target).parent().data('id'),'up');
        },
        moveDown(e) {
            // Move the row down
            e.preventDefault();
            let vm = this;
            var tr = $(e.target).parents('tr');
            vm.moveRow(tr, 'down');
            vm.sendDirection($(e.target).parent().data('id'),'down');
        },
        moveRow(row, direction) {
            // Move up or down (depending...)
            var table = this.$refs.requirements_datatable.vmDataTable;
            var index = table.row(row).index();

            var order = -1;
            if (direction === 'down') {
              order = 1;
            }

            var data1 = table.row(index).data();
            data1.order += order;

            var data2 = table.row(index + order).data();
            data2.order += -order;

            table.row(index).data(data2);
            table.row(index + order).data(data1);

            table.page(0).draw(false);
        },
        setApplicationWorkflowState(bool){
            let vm=this;
            //vm.proposal.requirements_completed=bool;
            //console.log('child', bool);
            vm.$emit('refreshRequirements',bool);
        }
    },
    mounted: function(){
        let vm = this;
        this.fetchRequirements();
        vm.fetchGlobalSettings();
        vm.$nextTick(() => {
            this.eventListeners();
        });
    }
}
</script>
<style scoped>
.dataTables_wrapper .dt-buttons{
    float: right;
}
</style>
