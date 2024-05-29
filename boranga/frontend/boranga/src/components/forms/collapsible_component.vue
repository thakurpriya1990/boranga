<template lang="html">
    <div class="toggle_filters_wrapper rounded mb-3">
        <div data-bs-toggle="collapse" :data-bs-target="'#' + target_elem_id" :id="button_elem_id"
            class="toggle_filters_button collapsed d-flex align-items-center" @click="toggle_filters_button_clicked">
            <div class="me-auto ps-1 title">{{ component_title }}</div>
            <div class="me-2">
                <i :id="warning_icon_id" :title="warning_icon_title"
                    class="fa-solid fa-exclamation-circle fa-2x filter_warning_icon"></i>
            </div>
            <div class="me-2">
                <i :id="chevron_elem_id" class="rotate_icon fa-solid fa-chevron-down"></i>
            </div>
        </div>

        <div class="collapse border-top mt-1" :id="target_elem_id" :class="collapsed ? 'collapse' : 'collapse show'"
            :aria-expanded="collapsed ? 'false' : 'true'">
            <slot></slot>
        </div>
    </div>
</template>

<script>
import { v4 as uuid } from 'uuid';
export default {
    name: "CollapsibleComponent",
    props: {
        component_title: {
            type: String,
            required: false,
            default: '',
        },
        collapsed: {
            type: Boolean,
            default: true,
        },
    },
    watch: {
        filters_expanded: function () {
            let chevron_icon = $('#' + this.chevron_elem_id)
            if (this.filters_expanded) {
                chevron_icon.addClass('chev_rotated')
            } else {
                chevron_icon.removeClass('chev_rotated')
            }
        }
    },
    data: function () {
        return {
            target_elem_id: 'target_elem_' + uuid(),
            button_elem_id: 'button_elem_' + uuid(),
            chevron_elem_id: 'chevron_elem_' + uuid(),
            warning_icon_id: 'warning_elem_' + uuid(),
            warning_icon_title: '',
            display_icon: false,
            filters_expanded: null,
        }
    },
    methods: {
        toggle_filters_button_clicked: function (e) {
            // Bootstrap add a 'collapsed' class name to the element
            let filters_expanded_when_clicked = $('#' + this.button_elem_id).hasClass('collapsed')
            this.filters_expanded = !filters_expanded_when_clicked
        },
        show_warning_icon: function (show) {
            let warning_icon = $('#' + this.warning_icon_id)
            if (show) {
                warning_icon.css('opacity', 1)
                this.warning_icon_title = 'filter(s) applied'
            } else {
                warning_icon.css('opacity', 0)
                this.warning_icon_title = ''
            }
        },
    },
    mounted: function () {
        this.$nextTick(function () {
            this.$emit('created')
        })
    },
}
</script>

<style lang="css" scoped>
.toggle_filters_wrapper {
    background: #efefee;
    padding: 0.5em;
    display: grid;
    color: #505050;
}

.toggle_filters_wrapper .form-group {
    margin-top: 0.6em;
    margin-bottom: 0.6em;
    padding-left: 0.4em;
    padding-right: 0.4em;
}

.toggle_filters_wrapper .form-group .form-select,
.toggle_filters_wrapper .form-group .form-control {
    color: #6c757d;
}

.toggle_filters_button {
    cursor: pointer;
}

.filter_warning_icon {
    color: #ffc107;
    transition: 0.5s;
}

.rotate_icon {
    transition: 0.5s;
}

.chev_rotated {
    transform: rotate(180deg);
}

.title,
.rotate_icon {
    color: #505050;
}
</style>
