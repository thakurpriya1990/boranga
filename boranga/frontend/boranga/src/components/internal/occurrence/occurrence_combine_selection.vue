<template lang="html">
    <div id="occurrenceCombineSelect">
        <datatable ref="occurrences_datatable" :id="panelBody" :dtOptions="occurrences_options"
                    :dtHeaders="occurrences_headers" :key="tableKey"/>
    </div>
</template>

<script>
import datatable from '@vue-utils/datatable.vue';
import {constants} from '@/utils/hooks'

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
        }
    },
    data:function () {
        let vm = this;
        return{
            tableKey: 0,
            panelBody: "occ-combine-select-"+vm._uid,
            occurrences_headers:["Number", "Name", "Action"],
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
                data: this.selectedOccurrences,
                order: [],
                buttons:[],
                searching: false,
                dom: "<'d-flex align-items-center'<'me-auto'l>fB>" +
                        "<'row'<'col-sm-12'tr>>" +
                        "<'d-flex align-items-center'<'me-auto'i>p>",
                columns: [
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

                            links += `<a href='/internal/occurrence/${full.id}' target="_blank">View</a><br>`;
                            
                            if (full.id != vm.mainOccurrenceId) {
                                links += `<a href='#' data-remove-occurrence='${full.id}'>Remove</a><br>`;
                            }

                            return links;
                        }
                    },
                ]
            },
        }
    },
    components: {
        datatable,
    },
    methods: {
        removeOccurrence: function(id) {
            let vm=this;
            console.log(id);
            console.log(vm.selectedOccurrenceIds);
            if (vm.selectedOccurrenceIds.includes(parseInt(id))) {
                console.log(id);
                for (var i = 0; i < vm.selectedOccurrenceIds.length; i++) {
                    if (vm.selectedOccurrenceIds[i] == id) {
                        console.log(vm.selectedOccurrenceIds[i])
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
                console.log(vm.selectedOccurrenceIds);
            }
        }, 
        addEventListeners:function (){
            let vm=this;
            
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