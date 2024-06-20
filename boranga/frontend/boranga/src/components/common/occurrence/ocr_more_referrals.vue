<template id="ocr-more-referrals">
    <div>
        <a v-if="!isFinalised" ref="showRef" @click.prevent="" role="button" class="mt-2 float-end">Show All
            Referrals</a>
    </div>
</template>

<script>
import { constants, api_endpoints, helpers } from '@/utils/hooks'

export default {
    name: 'OccurrenceReportMoreReferrals',
    props: {
        isFinalised: {
            type: Boolean,
            required: true
        },
        canAction: {
            type: Boolean,
            required: true
        },
        occurrence_report_obj: {
            type: Object,
            required: true
        },
        referral_url: {
            type: String,
            default: null
        }
    },
    data() {
        let vm = this;
        return {
            table: null,
            dateFormat: 'DD/MM/YYYY HH:mm:ss',
            datatable_url: '',
            datatable_options: {
                language: {
                    processing: constants.DATATABLE_PROCESSING_HTML
                },
                responsive: true,
                deferRender: true,
                autowidth: true,
                processing: true,
                ajax: {
                    "url": this.referral_url,
                    "dataSrc": '',
                },
                columns: [
                    {
                        title: 'Sent On',
                        data: 'lodged_on',
                        render: function (date) {
                            return moment(date).format(vm.dateFormat);
                        }
                    },
                    {
                        title: 'Referral',
                        data: 'referral',
                        render: function (data, type, full) {
                            console.log(data);

                            return `<span>${data.first_name} ${data.last_name}</span>`;
                        }
                    },
                    {
                        title: 'Status',
                        data: 'processing_status'
                    },
                    {
                        title: 'Action',
                        data: 'id',
                        render: function (data, type, full) {
                            var result = '';
                            if (!vm.canAction) {
                                return result;
                            }
                            var user = full.referral.first_name + ' ' + full.referral.last_name;
                            if (full.processing_status == 'Awaiting') {
                                result = `<a href="" data-id="${data}" data-user="${user}" class="remindRef">Remind</a>/<a href="" data-id="${data}" data-user="${user}" class="recallRef">Recall</a>`;
                            }
                            else {
                                result = `<a href="" data-id="${data}" data-user="${user}" class="resendRef">Resend</a>`;
                            }
                            return result;
                        }
                    },
                    {
                        title: 'Referral Comments',
                        data: 'referral_comment',

                        'render': function (value) {
                            var ellipsis = '...',
                                truncated = _.truncate(value, {
                                    length: 20,
                                    omission: ellipsis,
                                    separator: ' '
                                }),
                                result = '<span>' + truncated + '</span>',
                                popTemplate = _.template('<a href="#" ' +
                                    'role="button" ' +
                                    'data-bs-toggle="popover" ' +
                                    'data-bs-trigger="click" ' +
                                    'data-bs-placement="top auto"' +
                                    'data-bs-html="true" ' +
                                    'data-bs-content="<%= text %>" ' +
                                    '>more</a>');
                            if (_.endsWith(truncated, ellipsis)) {
                                result += popTemplate({
                                    text: value
                                });
                            }

                            return result;
                        },
                    }
                ]
            },
        }
    },
    methods: {
        remindReferral: function (_id, user) {
            let vm = this;

            vm.$http.get(helpers.add_endpoint_json(api_endpoints.ocr_referrals, _id + '/remind')).then(response => {
                vm.$emit('refreshFromResponse', response);
                vm.table.ajax.reload();
                swal.fire({
                    title: 'Referral Reminder',
                    text: 'A reminder has been sent to ' + user,
                    icon: 'success',
                    confirmButtonColor: '#226fbb',
                });
            },
                error => {
                    swal.fire({
                        title: 'Remind Referral Error',
                        text: helpers.apiVueResourceError(error),
                        icon: 'error',
                        confirmButtonColor: '#226fbb'
                    });
                });
        },
        resendReferral: function (_id, user) {
            let vm = this;
            vm.$http.get(helpers.add_endpoint_json(api_endpoints.ocr_referrals, _id + '/resend')).then(response => {
                vm.$emit('refreshFromResponse', response);
                vm.table.ajax.reload();
                swal.fire({
                    title: 'Referral Resent',
                    text: 'The referral has been resent to ' + user,
                    icon: 'success',
                    confirmButtonColor: '#226fbb'
                });
            },
                error => {
                    swal.fire({
                        title: 'Resend Referral Error',
                        text: helpers.apiVueResourceError(error),
                        icon: 'error',
                        confirmButtonColor: '#226fbb'
                    });
                });
        },
        recallReferral: function (_id, user) {
            let vm = this;
            vm.$http.get(helpers.add_endpoint_json(api_endpoints.ocr_referrals, _id + '/recall')).then(response => {
                vm.$emit('refreshFromResponse', response);
                vm.table.ajax.reload();
                swal.fire({
                    title: 'Referral Recall',
                    text: 'The referral has been recalled from ' + user,
                    icon: 'success',
                    confirmButtonColor: '#226fbb'
                });
            },
                error => {
                    swal.fire({
                        title: 'Referral Recall Error',
                        text: helpers.apiVueResourceError(error),
                        icon: 'error',
                        confirmButtonColor: '#226fbb'
                    });
                });
        },
        initialiseTable: function () {
            // To allow table elements (ref: https://getbootstrap.com/docs/5.1/getting-started/javascript/#sanitizer)
            var myDefaultAllowList = bootstrap.Tooltip.Default.allowList
            myDefaultAllowList.table = []

            let vm = this;
            let table_id = 'cs-more-referrals-table' + vm._uid;
            let popover_name = 'popover-' + vm._uid;
            let my_content = '<table id="' + table_id + '" class="hover table table-striped table-bordered dt-responsive" cellspacing="0" width="100%"></table>'
            let my_template = '<div class="popover ' + popover_name + '" role="tooltip"><div class="popover-arrow" style="top:110px;"></div><h3 class="popover-header"></h3><div class="popover-body"></div></div>'
            let popover_elem = $(vm.$refs.showRef)[0]

            new bootstrap.Popover(popover_elem, {
                html: true,
                content: my_content,
                template: my_template,
                title: 'Referrals',
                container: 'body',
                placement: 'right',
                trigger: "click focus",
            })
            popover_elem.addEventListener('inserted.bs.popover', function () {
                console.log('in inserted.bs.popover')

                vm.table = $('#' + table_id).DataTable(vm.datatable_options);

                // activate popover when table is drawn.
                vm.table.on('draw.dt', function () {
                    var $tablePopover = $(this).find('[data-bs-toggle="popover"]');
                    if ($tablePopover.length > 0) {
                        $tablePopover.popover();
                        // the next line prevents from scrolling up to the top after clicking on the popover.
                        $($tablePopover).on('click', function (e) {
                            e.preventDefault();
                            return true;
                        });
                    }
                }).on('click', '.resendRef', function (e) {
                    e.preventDefault();
                    var _id = $(this).data('id');
                    var user = $(this).data('user');
                    vm.resendReferral(_id, user);
                }).on('click', '.recallRef', function (e) {
                    e.preventDefault();
                    var _id = $(this).data('id');
                    var user = $(this).data('user');
                    vm.recallReferral(_id, user);
                }).on('click', '.remindRef', function (e) {
                    e.preventDefault();
                    var _id = $(this).data('id');
                    var user = $(this).data('user');
                    vm.remindReferral(_id, user);
                });
            })
            popover_elem.addEventListener('shown.bs.popover', function () {
                console.log('in shown.bs.popover')

                var el = vm.$refs.showRef;
                var popoverheight = parseInt($('.' + popover_name).height());

                var popover_bounding_top = parseInt($('.' + popover_name)[0].getBoundingClientRect().top);
                var popover_bounding_bottom = parseInt($('.' + popover_name)[0].getBoundingClientRect().bottom);

                var el_bounding_top = parseInt($(el)[0].getBoundingClientRect().top);
                var el_bounding_bottom = parseInt($(el)[0].getBoundingClientRect().top);

                var diff = el_bounding_top - popover_bounding_top;

                var position = parseInt($('.' + popover_name).position().top);
                var pos2 = parseInt($(el).position().top) - 5;

                var x = diff + 5;
                $('.' + popover_name).children('.arrow').css('top', x + 'px');
            })
        },
    },
    mounted() {
        this.$nextTick(() => {
            let vm = this;
            // if loop given below to avoid error when referral completes his task
            if (!vm.isFinalised) {
                this.initialiseTable();
            }
        })
    },
}
</script>
