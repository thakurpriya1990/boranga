<template lang="html">
    <div id="related_ocr">
        <FormSection :formCollapse="false" label="Related Occurrence Reports" Index="related_ocr">
            <div>
                <datatable
                    ref="related_ocr_datatable"
                    :id="datatable_id"
                    :dtOptions="datatable_options"
                    :dtHeaders="datatable_headers"
                />
            </div>
        </FormSection>

        <div v-if="sectionOCRId">
            <SectionModal
                ref="section_modal"
                :key="sectionOCRId"
                :sectionType="sectionTypeFormatted"
                :ocrNumber="sectionOCRId"
                :sectionObj="sectionObj"
            />
        </div>
    </div>
</template>

<script>
import Vue from 'vue'
import { v4 as uuid } from 'uuid'
import datatable from '@/utils/vue/datatable.vue'
import FormSection from '@/components/forms/section_toggle.vue';
import CollapsibleFilters from '@/components/forms/collapsible_component.vue'
import SectionModal from '@/components/common/occurrence/section_modal.vue'
import {
    constants,
    api_endpoints,
    helpers,
}
from '@/utils/hooks'

export default {
    name: 'TableRelatedItems',
    components: {
        datatable,
        FormSection,
        CollapsibleFilters,
        SectionModal,
    },
    props: {
        occurrence_obj:{
            type: Object,
            required:true
        },
        section_type: {
            type: String,
            required: false,
            default: "",
        }
    },
    data() {
        let vm = this;
        return {
            uuid:0,
            datatable_id: uuid(),
            sectionOCRId: null,
            sectionTypeFormatted: null,
            sectionObj: null,
        }
    },
    computed: {
        column_number: function(){
            return {
                data: 'occurrence_report_number',
                orderable: true,
                searchable: true,
                visible: true,
            }
        },
        column_status: function(){
            return {
                data: 'processing_status_display',
                orderable: true,
                searchable: true,
                visible: true,

            }
        },
        column_submitter: function(){
            return {
                data: 'submitter',
                orderable: false,
                searchable: false,
                visible: true,
            }
        },     
        column_action: function(){
            return {
                //name: 'action',
                data: 'id',
                orderable: false,
                searchable: false,
                visible: true,
                'render': function(row, type, full){
                    let links = '';
                    links += `<a href='/internal/occurrence_report/${full.id}' target="_blank">View</a><br>`;
                    return links;
                }
            }
        },
        column_copy_action: function(){
            return {
                //name: 'action',
                data: 'id',
                orderable: false,
                searchable: false,
                visible: true,
                'render': function(row, type, full){
                    let links = '';
                    links += `<a href='#' data-view-section='${full.id}'>View Section</a><br>`;
                    return links;
                }
            }
        },
        datatable_options: function(){
            let vm = this

            let action = vm.column_action
            if (vm.section_type !== "")
            {
                action = vm.column_copy_action
            }

            let columns = [
                vm.column_number,
                vm.column_status,
                vm.column_submitter,
                action,
            ]
            return {
                autoWidth: false,
                language: {
                    processing: constants.DATATABLE_PROCESSING_HTML
                },
                responsive: true,
                //serverSide: true,
                searching: true,
                ordering: true,
                order: [[0, 'desc']],
                ajax: {
                    //"url": '/api/proposal/' + vm.proposal.id + '/get_related_items/',
                    "url": "/api/occurrence/" + this.occurrence_obj.id + "/get_related_occurrence_reports/",
                    "dataSrc": "",
                    // adding extra GET params for Custom filtering
                    "data": function ( d ) {
                        d.related_filter_type = vm.filterRelatedType
                    }
                },
                dom: 'lBfrtip',
                buttons:[ ],
                columns: columns,
                processing: true,
                initComplete: function(settings, json) {
                },
            }
        },
        datatable_headers: function(){
            return [
                //'id',
                'Number',
                'Status',
                'Submitter',
                'Action',
            ]
        },
    },
    methods:{
        viewSection:function (id) {
            let vm=this;
            //get ocr object with id
            Vue.http.get(helpers.add_endpoint_json(api_endpoints.occurrence_report,id)).then((response) => {
                let ocrObj=response.body;

                vm.sectionObj = ocrObj[vm.section_type];
                vm.sectionOCRId = id;
                vm.sectionTypeFormatted = vm.section_type.split('_')
                .map((s) => s.charAt(0).toUpperCase() + s.substring(1))
                .join(' ');

                this.$nextTick(() => {
                this.$refs.section_modal.isModalOpen = true;
                });
            },
            err => {
                console.log(err);
            });
            
        },
        addEventListeners:function (){
            let vm=this;
            vm.$refs.related_ocr_datatable.vmDataTable.on('click', 'a[data-view-section]', function(e) {
                e.preventDefault();
                var id = $(this).attr('data-view-section');
                vm.viewSection(id);
            });
        }
    },
    mounted: function(){
        let vm = this;
        this.$nextTick(() => {
            vm.addEventListeners();
        });
    }
}
</script>
