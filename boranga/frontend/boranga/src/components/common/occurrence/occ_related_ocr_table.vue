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
    </div>
</template>

<script>
import { v4 as uuid } from 'uuid'
import { constants, helpers } from '@/utils/hooks'
import datatable from '@/utils/vue/datatable.vue'
import FormSection from '@/components/forms/section_toggle.vue';
import CollapsibleFilters from '@/components/forms/collapsible_component.vue'
export default {
    name: 'TableRelatedItems',
    components: {
        datatable,
        FormSection,
        CollapsibleFilters,
    },
    props: {
        occurrence_obj:{
            type: Object,
            required:true
        },
    },
    data() {
        let vm = this;
        return {
            datatable_id: uuid(),
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
        datatable_options: function(){
            let vm = this
            let columns = [
                vm.column_number,
                vm.column_status,
                vm.column_submitter,
                vm.column_action,
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
    mounted: function(){
        let vm = this;
    }
}
</script>
