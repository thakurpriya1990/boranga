<template>
    <div class="card card-default">
        <div class="card-header">Submission</div>
        <div class="card-body py-2">
            <strong>Created by</strong><br />
            {{ submitter_first_name }}
            {{ submitter_last_name }}
            <span v-if="is_new_contributor" class="badge bg-warning"
                ><i class="bi bi-person-plus-fill"></i> New Contributor</span
            >
        </div>
        <div v-if="datetime_created" class="card-body border-top py-2">
            <strong>Created on</strong><br />
            {{ formatDateDay(datetime_created) }}
            <span class="fw-light">at</span>
            {{ formatDateTime(datetime_created) }}
        </div>
        <div v-if="datetime_scheduled" class="card-body border-top py-2">
            <strong>Scheduled on</strong><br />
            {{ formatDateDay(datetime_scheduled) }}
            <span class="fw-light">at</span>
            {{ formatDateTime(datetime_scheduled) }}
        </div>
        <div v-if="datetime_completed" class="card-body border-top py-2">
            <strong>Marked as Completed on</strong><br />
            {{ formatDateDay(datetime_completed) }}
            <span class="fw-light">at</span>
            {{ formatDateTime(datetime_completed) }}
        </div>
        <div v-if="enableHistory" class="card-body border-top py-2">
            <table class="table small-table">
                <tbody>
                    <tr>
                        <th>Lodgement</th>
                        <th>Date</th>
                        <th>Action</th>
                    </tr>
                </tbody>
            </table>
        </div>
    </div>
</template>

<script>
export default {
    name: 'MeetingSidePanel',
    props: {
        submitter_first_name: {
            type: String,
            default: '',
        },
        submitter_last_name: {
            type: String,
            default: '',
        },
        datetime_created: {
            type: String,
            default: null,
        },
        datetime_scheduled: {
            type: String,
            default: null,
        },
        datetime_completed: {
            type: String,
            default: null,
        },
        is_new_contributor: {
            type: Boolean,
            default: false,
        },
        enableHistory: {
            type: Boolean,
            default: false,
        },
    },
    methods: {
        formatDateDay: function (data) {
            return data ? moment(data).format('DD/MM/YYYY') : '';
        },
        formatDateTime: function (data) {
            return data ? moment(data).format('HH:mm:ss A') : '';
        },
    },
};
</script>
