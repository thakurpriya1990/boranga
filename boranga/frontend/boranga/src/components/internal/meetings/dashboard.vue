<template>
    <div id="internalMeetDash" class="container">
        <FormSection :form-collapse="false" label="Meetings" Index="meeting">
            <MeetingsDashTable
                ref="meetings_table"
                level="internal"
                :url="meetings_url"
            />
        </FormSection>
    </div>
</template>
<script>
import FormSection from '@/components/forms/section_toggle.vue';
import MeetingsDashTable from './meetings_datatable.vue';
import { api_endpoints } from '@/utils/hooks';
export default {
    name: 'InternalMeetingsDashboard',
    components: {
        MeetingsDashTable,
        FormSection,
    },
    data() {
        return {
            meetings_url: api_endpoints.meetings_paginated,
        };
    },
};
</script>
