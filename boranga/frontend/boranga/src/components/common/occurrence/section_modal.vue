<template lang="html">
    <div id="section_details">
        <modal transition="modal fade" @ok="ok()" @cancel="close()" :title="title" large>
            <div class="container-fluid">
                <div class="row">

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
import { helpers } from "@/utils/hooks.js"
export default {
    name: 'SectionModal',
    components: {
        modal,
        alert,
    },
    props: {
        sectionObj: {
            type: Object,
            required: true,
        },
        sectionType: {
            type: String,
            required:true,
        }
    },
    data: function () {
        let vm = this;
        return {
            isModalOpen: false,
            form: null,
            sectionObj: null,
        }
    },
    methods: {
        close: function () {
            this.isModalOpen = false;
            this.sectionObj = {};
            this.errors = false;
            $('.has-error').removeClass('has-error');
        },
    }
}
</script>
