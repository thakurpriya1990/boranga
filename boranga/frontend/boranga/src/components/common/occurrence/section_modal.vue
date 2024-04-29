<template lang="html">
    <div id="section_details">
        <modal transition="modal fade" @ok="ok()" @cancel="close()" :title="'OCR ' + ocrNumber + ' ' + sectionType" large>
            <div class="container-fluid">
                <div class="row">
                    <FormSection :formCollapse="false" :label="sectionType">
                        <div class="card-body card-collapse">
                            <div v-for="(value,index) in sectionObj">
                                <div v-if="value && index != 'id' ">  
                                    <div v-if="typeof value == 'object'" class="row mb-3">
                                        <div v-for="(o_value,o_index) in value">
                                            <label class="col-sm-6 control-label">{{index}}.{{o_index}}:</label>
                                            <div class="col-sm-6">
                                            <input :disabled="true" type="text" class="form-control" :value=o_value>
                                            </div>
                                        </div>
                                    </div>
                                    <div v-else class="row mb-3">
                                        <label class="col-sm-6 control-label">{{index}}:</label>
                                        <div class="col-sm-6">
                                        <textarea :disabled="true" type="text" class="form-control">{{value}}</textarea>
                                        </div>
                                    </div>
                                </div>
                            </div>  
                        </div>            
                    </FormSection>
                </div>
            </div>
            <div slot="footer">
                <button type="button" class="btn btn-secondary me-2" @click="close">Close</button>
            </div>
        </modal>
    </div>
</template>

<script>
import modal from '@vue-utils/bootstrap-modal.vue'
import alert from '@vue-utils/alert.vue'
import FormSection from '@/components/forms/section_toggle.vue';
import { helpers } from "@/utils/hooks.js"
export default {
    name: 'SectionModal',
    components: {
        modal,
        alert,
        FormSection,
    },
    props: {
        sectionObj: {
            type: Object,
            required: true,
        },
        sectionType: {
            type: String,
            required:true,
        },
        ocrNumber: {
            type: String,
            required:true,
        }
    },
    data: function () {
        let vm = this;
        return {
            isModalOpen: false,
            form: null,
        }
    },
    methods: {
        close: function () {
            this.isModalOpen = false;
            this.errors = false;
            $('.has-error').removeClass('has-error');
        },
    }
}
</script>
