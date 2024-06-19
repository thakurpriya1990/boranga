<template lang="html">
    <div id="occurrenceCombine">
        <modal
            transition="modal fade"
            :title="'Combine Occurrences'"
            :large="true"
            :full="true"
            :showOK="false"
            cancel-text="Close"
            @cancel="close()"
        >
        </modal>
    </div>
</template>

<script>
    import modal from '@vue-utils/bootstrap-modal.vue';
    export default {
        name: 'OccurrenceCombine',
        components: {
            modal,
        },
        data: function () {
            return {
                isModalOpen: false,
            }
        },
        methods: {
            close: function () {
                this.errorString = '';
                this.isModalOpen = false;
                $('.has-error').removeClass('has-error');
            },
        }
    }
</script>