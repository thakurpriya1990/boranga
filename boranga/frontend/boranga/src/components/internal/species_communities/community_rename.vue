<template lang="html">
    <div id="rename-community">
        <modal
            id="rename-community-modal"
            transition="modal fade"
            :title="title"
            extra-large
            @ok="ok()"
            @cancel="close"
        >
            <div class="container-fluid">
                <div class="row">
                    <alert
                        type="primary"
                        class="d-flex align-items-center py-1 mb-3"
                    >
                        <div class="float-start pe-3">
                            <span class="align-middle"
                                ><i
                                    class="bi bi-info-circle-fill text-primary fs-4"
                                ></i
                            ></span>
                        </div>
                        <ul class="list-group list-group-flush">
                            <li class="list-group-item bg-transparent">
                                All fields, document and threats will be copied
                                from
                                <span class="fw-bold"
                                    >{{
                                        species_community_original.community_number
                                    }}
                                    -
                                    {{
                                        species_community_original
                                            .taxonomy_details.community_name
                                    }}</span
                                >
                                to the new community record
                            </li>
                            <li class="list-group-item bg-transparent">
                                Please modify the taxonomy details for the new
                                community then click 'Finalise Rename Community'
                            </li>
                            <li class="list-group-item bg-transparent">
                                <span class="fw-bold"
                                    >{{
                                        species_community_original.community_number
                                    }}
                                    -
                                    {{
                                        species_community_original
                                            .taxonomy_details.community_name
                                    }}</span
                                >
                                will be made historical but may be reopened
                                later if required
                            </li>
                        </ul>
                    </alert>
                </div>
                <div class="row">
                    <FormSection
                        v-if="new_community"
                        :form-collapse="false"
                        label="New Community Taxonomy Information"
                        Index="new-community"
                    >
                        <form
                            class="form-horizontal"
                            name="rename-community-form"
                        >
                            <alert v-if="errors" type="danger"
                                ><strong>{{ errors }}</strong></alert
                            >
                            <div class="row border-bottom mb-4 pb-3">
                                <label
                                    for=""
                                    class="col-sm-3 control-label fw-bold"
                                ></label>
                                <div class="col-sm-6">
                                    <button
                                        class="btn btn-primary float-end"
                                        @click.prevent="resetForm"
                                    >
                                        Reset form
                                    </button>
                                </div>
                                <div class="col-sm-3">
                                    <button
                                        class="btn btn-primary w-100"
                                        @click.prevent="
                                            populateFromOriginalCommunity
                                        "
                                    >
                                        Populate all from
                                        {{
                                            species_community_original.community_number
                                        }}
                                    </button>
                                </div>
                            </div>
                            <div class="row mb-3">
                                <label
                                    for=""
                                    class="col-sm-3 control-label fw-bold"
                                    >Community Name:
                                    <span class="text-danger">*</span></label
                                >
                                <div class="col-sm-6">
                                    <textarea
                                        id="community_name"
                                        ref="community_name"
                                        v-model="
                                            new_community.taxonomy_details
                                                .community_name
                                        "
                                        class="form-control"
                                        rows="1"
                                        placeholder=""
                                    />
                                </div>
                            </div>
                            <div class="row mb-3">
                                <label
                                    for=""
                                    class="col-sm-3 control-label fw-bold"
                                    >Community ID:
                                    <span class="text-danger">*</span></label
                                >
                                <div class="col-sm-6">
                                    <input
                                        id="community_migrated_id"
                                        ref="community_migrated_id"
                                        v-model="
                                            new_community.taxonomy_details
                                                .community_migrated_id
                                        "
                                        type="text"
                                        class="form-control"
                                        placeholder=""
                                    />
                                </div>
                            </div>
                            <div class="row mb-3">
                                <label for="" class="col-sm-3 control-label"
                                    >Community Description:</label
                                >
                                <div class="col-sm-6">
                                    <textarea
                                        id="community_description"
                                        v-model="
                                            new_community.taxonomy_details
                                                .community_description
                                        "
                                        class="form-control"
                                        rows="2"
                                        placeholder=""
                                    />
                                </div>
                                <div class="col-sm-3">
                                    <button
                                        v-if="
                                            species_community_original
                                                .taxonomy_details
                                                .community_description
                                        "
                                        class="btn btn-primary w-100"
                                        @click.prevent="
                                            new_community.taxonomy_details.community_description =
                                                species_community_original.taxonomy_details.community_description
                                        "
                                    >
                                        Populate from
                                        {{
                                            species_community_original.community_number
                                        }}
                                    </button>
                                </div>
                            </div>
                            <div class="row mb-3">
                                <label for="" class="col-sm-3 control-label"
                                    >Previous Name:</label
                                >
                                <div class="col-sm-6">
                                    <textarea
                                        id="community_previous_name"
                                        v-model="
                                            new_community.taxonomy_details
                                                .previous_name
                                        "
                                        class="form-control"
                                        placeholder=""
                                    />
                                </div>
                                <div class="col-sm-3">
                                    <button
                                        v-if="
                                            species_community_original
                                                .taxonomy_details.previous_name
                                        "
                                        class="btn btn-primary w-100"
                                        @click.prevent="
                                            new_community.taxonomy_details.previous_name =
                                                species_community_original.taxonomy_details.previous_name
                                        "
                                    >
                                        Populate from
                                        {{
                                            species_community_original.community_number
                                        }}
                                    </button>
                                </div>
                            </div>
                            <div class="row mb-3">
                                <label for="" class="col-sm-3 control-label"
                                    >Name Authority:</label
                                >
                                <div class="col-sm-6">
                                    <textarea
                                        id="name_authority"
                                        v-model="
                                            new_community.taxonomy_details
                                                .name_authority
                                        "
                                        rows="1"
                                        class="form-control"
                                        placeholder=""
                                    />
                                </div>
                                <div class="col-sm-3">
                                    <button
                                        v-if="
                                            species_community_original
                                                .taxonomy_details.name_authority
                                        "
                                        class="btn btn-primary w-100"
                                        @click.prevent="
                                            new_community.taxonomy_details.name_authority =
                                                species_community_original.taxonomy_details.name_authority
                                        "
                                    >
                                        Populate from
                                        {{
                                            species_community_original.community_number
                                        }}
                                    </button>
                                </div>
                            </div>
                            <div class="row mb-3">
                                <label for="" class="col-sm-3 control-label"
                                    >Name Comments:</label
                                >
                                <div class="col-sm-6">
                                    <textarea
                                        id="community_comment"
                                        v-model="
                                            new_community.taxonomy_details
                                                .name_comments
                                        "
                                        class="form-control"
                                        placeholder=""
                                    />
                                </div>
                                <div class="col-sm-3">
                                    <button
                                        v-if="
                                            species_community_original
                                                .taxonomy_details.name_comments
                                        "
                                        class="btn btn-primary w-100"
                                        @click.prevent="
                                            new_community.taxonomy_details.name_comments =
                                                species_community_original.taxonomy_details.name_comments
                                        "
                                    >
                                        Populate from
                                        {{
                                            species_community_original.community_number
                                        }}
                                    </button>
                                </div>
                            </div>
                            <div class="row mb-2">
                                <div class="col-sm-3"></div>
                                <div class="col-sm-9">
                                    <button
                                        class="btn btn-primary float-end mt-2"
                                        :disabled="
                                            !new_community.taxonomy_details
                                                .community_name ||
                                            !new_community.taxonomy_details
                                                .community_migrated_id
                                        "
                                        @click.prevent="finaliseRenameCommunity"
                                    >
                                        <i class="bi bi-check2-circle"></i>
                                        Finalise Rename Community<template
                                            v-if="finaliseCommunityLoading"
                                        >
                                            <span
                                                class="spinner-border spinner-border-sm"
                                                role="status"
                                                aria-hidden="true"
                                            ></span>
                                            <span class="visually-hidden"
                                                >Loading...</span
                                            ></template
                                        >
                                    </button>
                                </div>
                            </div>
                        </form>
                    </FormSection>
                    <FormSection
                        :form-collapse="false"
                        :label="`Original Community - ${species_community_original.community_number} - ${species_community_original.taxonomy_details.community_name}`"
                        Index="original-community"
                    >
                        <div>
                            <div class="col-md-12">
                                <FormSpeciesCommunities
                                    v-if="species_community_original"
                                    id="rename_community"
                                    ref="rename_community"
                                    :species_community_original="
                                        species_community_original
                                    "
                                    :species_community="
                                        species_community_original
                                    "
                                    :is_internal="true"
                                    :is_readonly="true"
                                    :rename_species="true"
                                >
                                    // rename=true used to make only taxon
                                    select editable on form
                                </FormSpeciesCommunities>
                            </div>
                        </div>
                    </FormSection>
                </div>
            </div>
            <template #footer>
                <div>
                    <button
                        type="button"
                        class="btn btn-secondary"
                        @click="close"
                    >
                        Cancel
                    </button>
                </div>
            </template>
        </modal>
    </div>
</template>

<script>
import modal from '@vue-utils/bootstrap-modal.vue';
import alert from '@vue-utils/alert.vue';
import FormSpeciesCommunities from '@/components/form_species_communities.vue';
import FormSection from '@/components/forms/section_toggle.vue';
import { api_endpoints } from '@/utils/hooks.js';

export default {
    name: 'CommunityRename',
    components: {
        modal,
        alert,
        FormSection,
        FormSpeciesCommunities,
    },
    props: {
        species_community_original: {
            type: Object,
            required: true,
        },
        is_internal: {
            type: Boolean,
            required: true,
        },
    },
    data: function () {
        return {
            new_community: null,
            isModalOpen: false,
            finaliseCommunityLoading: false,
            errors: null,
        };
    },
    computed: {
        original_community_display: function () {
            return `${this.species_community_original.community_number} - ${this.species_community_original.taxonomy_details.community_name}`;
        },
        title: function () {
            return `Rename Community ${this.original_community_display}`;
        },
    },
    watch: {
        isModalOpen: function (val) {
            if (val) {
                this.$nextTick(() => {
                    this.new_community = structuredClone(
                        this.species_community_original
                    );
                    this.new_community.id = null;
                    this.new_community.community_number = '';
                    this.new_community.taxonomy_details.community_id = null;
                    this.new_community.taxonomy_details.community_name = null;
                    this.new_community.taxonomy_details.community_migrated_id =
                        null;
                    this.new_community.taxonomy_details.previous_name =
                        this.species_community_original.taxonomy_details.community_name;
                    this.$nextTick(() => {
                        this.$refs.community_name.focus();
                    });
                });
            }
        },
    },
    methods: {
        resetForm: function () {
            this.new_community.taxonomy_details.community_name = '';
            this.new_community.taxonomy_details.community_migrated_id = '';
            this.new_community.taxonomy_details.community_description = '';
            this.new_community.taxonomy_details.previous_name =
                this.species_community_original.taxonomy_details.community_name;
            this.new_community.taxonomy_details.name_authority = '';
            this.new_community.taxonomy_details.name_comments = '';
            this.$refs.community_name.focus();
        },
        populateFromOriginalCommunity: function () {
            this.new_community.taxonomy_details.community_name =
                this.species_community_original.taxonomy_details.community_name;
            this.new_community.taxonomy_details.community_migrated_id =
                this.species_community_original.taxonomy_details.community_migrated_id;
            this.new_community.taxonomy_details.community_description =
                this.species_community_original.taxonomy_details.community_description;
            this.new_community.taxonomy_details.previous_name =
                this.species_community_original.taxonomy_details.previous_name;
            this.new_community.taxonomy_details.name_authority =
                this.species_community_original.taxonomy_details.name_authority;
            this.new_community.taxonomy_details.name_comments =
                this.species_community_original.taxonomy_details.name_comments;
            this.$refs.community_name.focus();
        },
        close: function () {
            this.isModalOpen = false;
        },
        finaliseRenameCommunity: function () {
            let vm = this;
            if (
                this.new_community.taxonomy_details.community_name ===
                this.species_community_original.taxonomy_details.community_name
            ) {
                swal.fire({
                    title: `Community name must be different from the original community`,
                    icon: 'error',
                    customClass: {
                        confirmButton: 'btn btn-primary',
                    },
                    didClose: () => {
                        vm.$refs.community_name.focus();
                    },
                });
                return;
            }
            if (
                this.new_community.taxonomy_details.community_migrated_id ===
                this.species_community_original.taxonomy_details
                    .community_migrated_id
            ) {
                swal.fire({
                    title: `Community ID must be different from the original community`,
                    icon: 'error',
                    customClass: {
                        confirmButton: 'btn btn-primary',
                    },
                    didClose: () => {
                        vm.$refs.community_migrated_id.focus();
                    },
                });
                return;
            }
            swal.fire({
                title: `Rename Community`,
                text: `Are you sure you want to rename community ${this.species_community_original.taxonomy_details.community_name} to ${this.new_community.taxonomy_details.community_name}?`,
                icon: 'question',
                showCancelButton: true,
                confirmButtonText: 'Rename Community',
                reverseButtons: true,
                customClass: {
                    confirmButton: 'btn btn-primary',
                    cancelButton: 'btn btn-secondary',
                },
            })
                .then((swalresult) => {
                    vm.finaliseCommunityLoading = true;
                    if (swalresult.isConfirmed) {
                        fetch(
                            api_endpoints.rename_community(
                                vm.species_community_original.id
                            ),
                            {
                                method: 'POST',
                                headers: {
                                    'Content-Type': 'application/json',
                                },
                                body: JSON.stringify(
                                    vm.new_community.taxonomy_details
                                ),
                            }
                        )
                            .then(async (response) => {
                                console.log(response);
                                if (response.status === 200) {
                                    return response.json();
                                } else {
                                    throw new Error(
                                        'Failed to rename community'
                                    );
                                }
                            })
                            .then((new_community_json) => {
                                console.log(new_community_json);
                                vm.$router.push({
                                    name: 'internal-species-communities',
                                    params: {
                                        species_community_id:
                                            new_community_json.id,
                                    },
                                    query: {
                                        group_type_name:
                                            new_community_json.group_type,
                                    },
                                });
                                vm.$router.go();
                                vm.isModalOpen = false;
                            })
                            .catch(async (response) => {
                                this.errors = await response.json();
                            });
                    }
                })
                .finally(() => {
                    vm.finaliseCommunityLoading = false;
                });
        },
    },
};
</script>
