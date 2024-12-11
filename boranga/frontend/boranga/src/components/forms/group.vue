<template lang="html">
    <div class="top-buffer bottom-buffer">
        <div class="panel panel-default">
            <div class="panel-body">
                <label :id="id" class="inline">{{ label }}</label>
                <!--<i data-toggle="tooltip" v-if="help_text" data-placement="right" class="fa fa-question-circle" :title="help_text"> &nbsp; </i>-->
                <template v-if="help_text">
                    <HelpText :help_text="help_text" />
                </template>

                <template v-if="help_text_url">
                    <HelpTextUrl :help_text_url="help_text_url" />
                </template>

                <a class="collapse-link-top pull-right" @click.prevent="expand"
                    ><span class="glyphicon glyphicon-chevron-down"></span
                ></a>
                <div
                    class="children-anchor-point collapse in"
                    style="padding-left: 0px"
                ></div>
                <span v-if="isPreviewMode" :class="{ hidden: isRemovable }">
                    <a :id="'remove_' + name">Remove {{ label }}</a>
                </span>
                <a
                    class="collapse-link-bottom pull-right"
                    @click.prevent="minimize"
                    ><span class="glyphicon glyphicon-chevron-up"></span
                ></a>
                <div
                    :class="{ row: true, collapse: true, in: isExpanded }"
                    style="margin-top: 10px"
                >
                    <div class="col-sm-12">
                        <slot></slot>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>

<script>
import HelpText from './help_text.vue';
import HelpTextUrl from './help_text_url.vue';
export default {
    name: 'Group',
    components: { HelpText, HelpTextUrl },
    props: [
        'label',
        'name',
        'id',
        'help_text',
        'help_text_url',
        'isRemovable',
        'isPreviewMode',
    ],
    data: function () {
        return {
            isExpanded: true,
        };
    },
    mounted: function () {
        $('[data-toggle="tooltip"]').tooltip();
    },
    methods: {
        expand: function () {
            this.isExpanded = true;
        },
        minimize: function () {
            this.isExpanded = false;
        },
    },
};
</script>

<style lang="css">
.collapse-link-top,
.collapse-link-bottom {
    cursor: pointer;
}
</style>
