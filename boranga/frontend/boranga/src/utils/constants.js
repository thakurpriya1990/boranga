module.exports = {
    PROPOSAL_STATUS: {
        DRAFT: { ID: 'draft', TEXT: 'Draft' },
        AMENDMENT_REQUIRED: { ID: 'amendment_required', TEXT: 'Amendment Required' },
        WITH_ASSESSOR: { ID: 'with_assessor', TEXT: 'With Assessor' },
        WITH_APPROVER: { ID: 'with_approver', TEXT: 'Proposed DeListed' },
        WITH_REFERRAL: { ID: 'with_referral', TEXT: 'With Referral' },
        APPROVED: { ID: 'approved', TEXT: 'Approved' },
        DECLINED: { ID: 'declined', TEXT: 'Declined' },
        DISCARDED: { ID: 'discarded', TEXT: 'Discarded' },
    },
    GROUPS: {
        CONSERVATION_STATUS_ASSESSORS: 'Conservation Status Assessors',
        CONSERVATION_STATUS_APPROVERS: 'Conservation Status Approvers',
        DJANGO_ADMIN: 'Django Admin',
        EXTERNAL_CONTRIBUTORS: 'External Contributors',
        INTERNAL_CONTRIBUTORS: 'Internal Contributors',
        OCCURRENCE_APPROVERS: 'Occurrence Approvers',
        OCCURRENCE_ASSESSORS: 'Occurrence Assessors',
        READ_ONLY_USERS: 'Read Only Users',
        SPECIES_AND_COMMUNITIES_APPROVERS: 'Species and Communities Approvers',
    },
    DATATABLE_PROCESSING_HTML:
        '<div class="d-flex justify-content-center"><div class="d-flex spinner-border text-primary my-4" role="status"><span class="visually-hidden">Loading...</span></div></div>',
}
