<template lang="html">
    <div id="occurrenceCombineSelect">
        <datatable ref="occurrences_datatable" :id="panelBody" :dtOptions="occurrences_options"
                    :dtHeaders="occurrences_headers" :key="tableKey"/>

        <div v-if="sectionOCCId">
            <SectionModal
                ref="section_modal"
                :key="sectionOCCId"
                :sectionTypeDisplay="sectionTypeFormatted"
                :sectionType="section_type"
                :occNumber="sectionOCCId"
                :sectionObj="sectionObj"
            />
        </div>
    </div>
</template>

<script>
import Vue from 'vue'
import datatable from '@vue-utils/datatable.vue';
import {constants,api_endpoints,helpers} from '@/utils/hooks'
import SectionModal from '@/components/common/occurrence/occ_section_modal.vue'

export default {
    name: 'OccurrenceCombineSelect',
    props: {
        selectedOccurrences: {
            type: Array,
            required: true
        },
        selectedOccurrenceIds: {
            type: Array,
            required: true
        },
        mainOccurrenceId: {
            type: Number,
            required: true
        },
        section_type: {
            type: String,
            required: false,
            default: "",
        },
        occ_chosen_section: {
            type: Number,
            required: false,
        },
    },
    data:function () {
        let vm = this;

        let headers = ["Number", "Name", "Action"];
        let columns = [
                    {
                        data: "occurrence_number",
                    },
                    {
                        data: "occurrence_name",
                    },
                    {
                        data: "id",
                        mRender:function (data,type,full){
                            let links = '';
                            if (vm.section_type === "" || vm.section_type === undefined) {
                                links += `<a href='/internal/occurrence/${full.id}' target="_blank">View</a><br>`;
                                
                                if (full.id != vm.mainOccurrenceId) {
                                    links += `<a href='#' data-remove-occurrence='${full.id}'>Remove</a><br>`;
                                }
                            } else {
                                links += `<a href='#' data-view-section='${full.id}'>View Section</a><br>`;
                            }

                            return links;
                        }
                    },
                ]
        
        if (vm.section_type !== "" && vm.section_type !== undefined) {
            headers.push("");
            columns.push({
                data: "id",
                mRender:function (data,type,full){
                    if (vm.occ_chosen_section !== undefined && vm.occ_chosen_section == full.id) {
                        return `<input id='${full.id}' type="radio" data-section-radio='${full.id}' checked>`
                    } else {
                        return `<input id='${full.id}' type="radio" data-section-radio='${full.id}'>`
                    }
                }
            })
        }

        return{
            tableKey: 0,
            panelBody: "occ-combine-select-"+vm._uid,
            sectionTypeFormatted: null,
            sectionObj: null,
            sectionOCCId: null,
            occurrences_headers:headers,
            occurrences_options:{
                autowidth: true,
                language:{
                    processing: constants.DATATABLE_PROCESSING_HTML
                },
                paging: false,
                responsive: true,
                columnDefs: [
                    { responsivePriority: 1, targets: 0 },
                    { responsivePriority: 2, targets: -1 },
                ],
                data: vm.selectedOccurrences,
                order: [],
                buttons:[],
                searching: false,
                dom: "<'d-flex align-items-center'<'me-auto'l>fB>" +
                        "<'row'<'col-sm-12'tr>>" +
                        "<'d-flex align-items-center'<'me-auto'i>p>",
                columns: columns,
            },
        }
    },
    components: {
        datatable,
        SectionModal,
    },
    methods: {
        removeOccurrence: function(id) {
            let vm=this;
            if (vm.selectedOccurrenceIds.includes(parseInt(id))) {
                for (var i = 0; i < vm.selectedOccurrenceIds.length; i++) {
                    if (vm.selectedOccurrenceIds[i] == id) {
                        vm.selectedOccurrenceIds.splice(i, 1);
                        break
                    }
                }
                for (var i = 0; i < vm.selectedOccurrences.length; i++) {
                    if (vm.selectedOccurrences[i].id == id) {
                        vm.selectedOccurrences.splice(i, 1);
                        break
                    }
                }
            }
        },
        viewSection:function (id) {
            let vm=this;
            //get occ object with id
            Vue.http.get(helpers.add_endpoint_json(api_endpoints.occurrence,id)).then((response) => {
                let occObj=response.body;

                vm.sectionObj = occObj[vm.section_type];
                vm.sectionOCCId = id;
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
            vm.$refs.occurrences_datatable.vmDataTable.on('change', 'input[data-section-radio]', function(e) {
                e.preventDefault();
                var id = $(this).attr('data-section-radio');
                vm.$emit("updateChosenSection",id, vm.section_type);
                vm.selectedOccurrences.forEach(occ=> {
                    let radio = vm.$refs.occurrences_datatable.vmDataTable.$("#"+occ.id);
                    if (radio.attr('data-section-radio') != $(this).attr('data-section-radio')) {
                        radio.prop('checked', false);
                    }
                });
            });
            vm.$refs.occurrences_datatable.vmDataTable.on('click', 'a[data-view-section]', function(e) {
                e.preventDefault();
                var id = $(this).attr('data-view-section');
                vm.viewSection(id);
            });     
            vm.$refs.occurrences_datatable.vmDataTable.on('click', 'a[data-remove-occurrence]', function(e) {
                e.preventDefault();
                var id = $(this).attr('data-remove-occurrence');
                vm.removeOccurrence(id);
            });
        }
    },
    watch: {
        selectedOccurrences: function() {
            let vm = this;
            vm.tableKey++;
            this.$nextTick(() => {
                vm.addEventListeners();
            });
        }
    },
    mounted: function(){
        let vm = this;
        this.$nextTick(() => {
            vm.addEventListeners();
        });
    },
}

</script>