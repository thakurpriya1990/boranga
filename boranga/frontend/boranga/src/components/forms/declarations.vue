<template lang="html">
    <div class="form-group">
        <label :id="id">
            <input
                ref="Checkbox"
                :name="name"
                type="checkbox"
                data-parsley-required
                :checked="isChecked"
                :required="isRequired"
                @change="handleDeclaration"
            />
            {{ label }}
        </label>

        <template v-if="help_text">
            <p class="help-block">{{ help_text }}</p>
        </template>
        <template v-if="help_text_url">
            <HelpTextUrl
                :help_text_url="help_text_assessor_url"
                assessor-mode="{assessorMode}"
                is-for-assessor="{true}"
            />
        </template>
    </div>
</template>

<script>
export default {
    props: [
        'name',
        'label',
        'id',
        'help_text',
        'handleDeclaration',
        'isRequired',
        'help_text_url',
    ],
    computed: {
        isChecked: function () {
            return this.value == 'on';
        },
    },
    mounted: function () {
        let vm = this;
        if (vm.isChecked) {
            var input = this.$refs.Checkbox;
            var e = document.createEvent('HTMLEvents');
            e.initEvent('change', true, true);
            input.dispatchEvent(e);
        }
    },
};
</script>

<style lang="css"></style>
