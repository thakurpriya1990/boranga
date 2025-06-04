<template lang="html">
    <div id="addCombineSpecies">
        <modal
            id="myAddSpeciesToCombineModal"
            transition="modal fade"
            :title="title"
            large
            @ok="ok()"
            @cancel="cancel()"
        >
            <div class="container-fluid">
                <div class="row">
                    <form class="form-horizontal" name="addSpeciesToCombine">
                        <alert v-if="errorString" type="danger"
                            ><strong>{{ errorString }}</strong></alert
                        >
                        <div>
                            <div class="row mb-3">
                                <label for="" class="col-sm-3 control-label"
                                    >Species:</label
                                >
                                <div
                                    :id="select_scientific_name"
                                    class="col-sm-9"
                                >
                                    <select
                                        :id="scientific_name_lookup"
                                        :ref="scientific_name_lookup"
                                        :name="scientific_name_lookup"
                                        class="form-control"
                                    />
                                </div>
                            </div>
                        </div>
                    </form>
                </div>
            </div>
            <template #footer>
                <div>
                    <button
                        type="button"
                        class="btn btn-secondary me-2"
                        @click="cancel"
                    >
                        Cancel
                    </button>
                    <button class="btn btn-primary" @click.prevent="ok()">
                        Confirm Selection
                    </button>
                </div>
            </template>
        </modal>
    </div>
</template>

<script>
import { v4 as uuid } from 'uuid';
import modal from '@vue-utils/bootstrap-modal.vue';
import alert from '@vue-utils/alert.vue';
import { helpers, api_endpoints } from '@/utils/hooks.js';
export default {
    name: 'AddCombineSpecies',
    components: {
        modal,
        alert,
    },
    data: function () {
        return {
            isModalOpen: false,
            form: null,
            errorString: '',
            species_list: [],
            combineSpeciesId: null,
            scientific_name_lookup: 'scientific_name_lookup' + uuid(),
            select_scientific_name: 'select_scientific_name' + uuid(),
        };
    },
    computed: {
        csrf_token: function () {
            return helpers.getCookie('csrftoken');
        },
        title: function () {
            return 'Select Species To Combine';
        },
    },
    mounted: function () {
        let vm = this;
        vm.form = document.forms.addSpeciesToCombine;

        this.$nextTick(() => {
            vm.initialiseScientificNameLookup();
        });
    },
    methods: {
        ok: function () {
            let vm = this;
            vm.form = document.forms.addSpeciesToCombine;
            if ($(vm.form).valid()) {
                vm.addSpeciesToCombineList();
            }
        },
        cancel: function () {
            this.close();
        },
        close: function () {
            this.isModalOpen = false;
            this.errorString = '';
        },
        addSpeciesToCombineList: function () {
            let vm = this;
            fetch(
                `/api/species/${vm.combineSpeciesId}/internal_species.json`
            ).then(async (response) => {
                const data = await response.json();
                if (!response.ok) {
                    swal.fire({
                        title: 'Please fix following errors',
                        text: JSON.stringify(data),
                        icon: 'error',
                        customClass: {
                            confirmButton: 'btn btn-primary',
                        },
                    });
                    return;
                }
                let species_obj = data.species_obj;
                // user should not able select the same ID if already exists in the array to combine
                let hasSpecies = false;
                for (const species of vm.$parent
                    .original_species_combine_list) {
                    if (species.id === species_obj.id) {
                        hasSpecies = true;
                    }
                }
                if (hasSpecies == true) {
                    swal.fire({
                        title: 'Please fix following errors',
                        text: 'Species To combine already exists',
                        icon: 'error',
                        customClass: {
                            confirmButton: 'btn btn-primary',
                        },
                    });
                } else {
                    vm.$parent.original_species_combine_list.push(species_obj); //--temp species_obj
                    $(vm.$refs[vm.scientific_name_lookup])
                        .val(null)
                        .trigger('change');
                }
            });
            this.close();
        },
        initialiseScientificNameLookup: function () {
            let vm = this;
            $(vm.$refs[vm.scientific_name_lookup])
                .select2({
                    minimumInputLength: 2,
                    dropdownParent: $('#' + vm.select_scientific_name),
                    theme: 'bootstrap-5',
                    allowClear: true,
                    placeholder: 'Select Species',
                    ajax: {
                        url: api_endpoints.scientific_name_lookup,
                        dataType: 'json',
                        data: function (params) {
                            var query = {
                                term: params.term,
                                type: 'public',
                                group_type_id:
                                    vm.$parent.species_community.group_type_id,
                                has_species: true,
                                active_only: true,
                            };
                            return query;
                        },
                    },
                })
                .on('select2:select', function (e) {
                    // let data = e.params.data.id;
                    let data = e.params.data.species_id;
                    vm.combineSpeciesId = data;
                })
                .on('select2:unselect', function () {
                    vm.combineSpeciesId = '';
                })
                .on('select2:open', function () {
                    const searchField = $(
                        '[aria-controls="select2-' +
                            vm.scientific_name_lookup +
                            '-results"]'
                    );
                    // move focus to select2 field
                    searchField[0].focus();
                });
        },
    },
};
</script>
