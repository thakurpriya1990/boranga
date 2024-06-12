<template>
    <div class="card card-default">
        <div class="card-header">
            Submission
        </div>
        <div class="card-body py-2">
            <strong>Submitted by</strong><br />
            {{ submitter_first_name }}
            {{ submitter_last_name }}
            <span v-if="is_new_contributor" class="badge bg-warning"><i class="bi bi-person-plus-fill"></i> New
                Contributor</span>
        </div>
        <div v-if="lodgement_date" class="card-body border-top py-2">
            <strong>Lodged on</strong>
            {{ lodgement_date | formatDate }}
        </div>
        <div v-if="enableHistory" class="card-body border-top py-2">
            <table class="table small-table">
                <tr>
                    <th>Lodgement</th>
                    <th>Date</th>
                    <th>Action</th>
                </tr>
            </table>
        </div>
    </div>
</template>

<script>
export default {
    name: 'Submission',
    props: {
        submitter_first_name: {
            type: String,
            default: '',
        },
        submitter_last_name: {
            type: String,
            default: '',
        },
        lodgement_date: {
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
    filters: {
        formatDate: function (data) {
            return data ? moment(data).format('DD/MM/YYYY HH:mm:ss') : '';
        }
    },
}
</script>
