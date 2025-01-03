<template lang="html">
    <div id="section_details">
        <modal
            transition="modal fade"
            :title="'OCR ' + ocrNumber + ' ' + sectionTypeDisplay"
            large
            @ok="ok()"
            @cancel="close()"
        >
            <div class="container-fluid">
                <div class="row">
                    <FormSection
                        :form-collapse="false"
                        :label="sectionTypeDisplay"
                    >
                        <div class="card-body card-collapse">
                            <div
                                v-for="(value, index) in sectionObjExpanded"
                                :key="index"
                            >
                                <div v-if="value && index != 'id'">
                                    <div v-if="typeof value == 'object'">
                                        <div
                                            v-for="(o_value, o_index) in value"
                                            :key="o_index"
                                            class="row mb-3"
                                        >
                                            <label
                                                class="col-sm-6 control-label"
                                                >{{ index }}.{{
                                                    o_index
                                                }}:</label
                                            >
                                            <div class="col-sm-6">
                                                <input
                                                    :disabled="true"
                                                    type="text"
                                                    class="form-control"
                                                    :value="o_value"
                                                />
                                            </div>
                                        </div>
                                    </div>
                                    <div v-else>
                                        <div class="row mb-3">
                                            <label
                                                class="col-sm-6 control-label"
                                                >{{ index }}:</label
                                            >
                                            <div class="col-sm-6">
                                                <textarea
                                                    :disabled="true"
                                                    type="text"
                                                    class="form-control"
                                                    v-bind:value="value"
                                                ></textarea>
                                            </div>
                                        </div>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </FormSection>
                </div>
            </div>
            <template #footer>
                <div>
                    <button
                        type="button"
                        class="btn btn-secondary me-2"
                        @click="close"
                    >
                        Close
                    </button>
                </div>
            </template>
        </modal>
    </div>
</template>

<script>
import modal from '@vue-utils/bootstrap-modal.vue';
import FormSection from '@/components/forms/section_toggle.vue';
import { api_endpoints } from '@/utils/hooks';
export default {
    name: 'SectionModal',
    components: {
        modal,
        FormSection,
    },
    props: {
        sectionObj: {
            type: Object,
            required: true,
        },
        sectionType: {
            type: String,
            required: true,
        },
        sectionTypeDisplay: {
            type: String,
            required: true,
        },
        ocrNumber: {
            type: String,
            required: true,
        },
    },
    data: function () {
        let vm = this;
        return {
            isModalOpen: false,
            form: null,
            sectionObjExpanded: vm.sectionObj,
        };
    },
    mounted: function () {
        let vm = this;
        this.$nextTick(() => {
            vm.fetchSectionData();
        });
    },
    methods: {
        close: function () {
            this.isModalOpen = false;
            this.errors = false;
            $('.has-error').removeClass('has-error');
        },
        fetchSectionData: function () {
            let vm = this;
            if (vm.sectionObj.occurrence_report_id !== undefined) {
                fetch(
                    api_endpoints.lookup_ocr_section_values(
                        vm.sectionType,
                        vm.sectionObj.occurrence_report_id
                    )
                ).then(
                    async (response) => {
                        vm.sectionObjExpanded = await response.json();
                    },
                    (error) => {
                        console.log(error);
                    }
                );
            }
        },
    },
};
</script>
