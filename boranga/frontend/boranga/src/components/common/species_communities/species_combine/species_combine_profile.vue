<template lang="html">
    <div id="species_combine_profile">
        <FormSection :form-collapse="false" label="Taxonomy" :Index="taxonBody">
            <div class="row mb-3">
                <label for="" class="col-sm-3 control-label"
                    >Scientific Name:</label
                >
                <div :id="select_scientific_name" class="col-sm-8">
                    <select
                        :id="scientific_name_lookup"
                        :ref="scientific_name_lookup"
                        :disabled="isReadOnly"
                        :name="scientific_name_lookup"
                        class="form-control"
                    />
                </div>
            </div>
            <div class="row mb-3">
                <label for="" class="col-sm-3 control-label"></label>
                <div class="col-sm-8">
                    <textarea
                        id="species_display"
                        v-model="species_display"
                        disabled
                        class="form-control"
                        rows="3"
                    />
                </div>
            </div>
            <div class="row mb-3">
                <label for="" class="col-sm-3 control-label"
                    >Common Name:</label
                >
                <div class="col-sm-8">
                    <textarea
                        id="common_name"
                        v-model="common_name"
                        :disabled="true"
                        class="form-control"
                        rows="2"
                        placeholder=""
                    />
                </div>
            </div>
            <div class="row mb-3">
                <label for="" class="col-sm-3 control-label"
                    >Taxon Name ID:</label
                >
                <div class="col-sm-8">
                    <input
                        id="taxon_name_id"
                        v-model="taxon_name_id"
                        :disabled="true"
                        type="text"
                        class="form-control"
                        placeholder=""
                    />
                    <!-- gives error for the below when new species created as no taxonomy id is present -->
                    <!-- <input :disabled="true" type="text" class="form-control" id="taxon_name_id" placeholder=""
                    v-model="species_communities.taxonomy_details.taxon_name_id"/> -->
                </div>
            </div>
            <div class="row mb-3">
                <label for="" class="col-sm-3 control-label"
                    >Previous Name:</label
                >
                <div class="col-sm-8">
                    <input
                        id="previous_name"
                        v-model="taxon_previous_name"
                        :disabled="true"
                        type="text"
                        class="form-control"
                        placeholder=""
                    />
                </div>
            </div>
            <div class="row mb-3">
                <label for="" class="col-sm-3 control-label"
                    >Phylogenetic Group:</label
                >
                <div class="col-sm-8">
                    <textarea
                        id="phylogenetic_group"
                        v-model="phylogenetic_group"
                        :disabled="true"
                        class="form-control"
                        rows="1"
                        placeholder=""
                    />
                </div>
            </div>
            <div class="row mb-3">
                <label for="" class="col-sm-3 control-label">Family:</label>
                <div class="col-sm-8">
                    <textarea
                        id="family"
                        v-model="family"
                        :disabled="true"
                        rows="1"
                        class="form-control"
                        placeholder=""
                    />
                </div>
            </div>
            <div class="row mb-3">
                <label for="" class="col-sm-3 control-label">Genus:</label>
                <div class="col-sm-8">
                    <textarea
                        id="genus"
                        v-model="genus"
                        :disabled="true"
                        rows="1"
                        class="form-control"
                        placeholder=""
                    />
                </div>
            </div>
            <div class="row mb-3">
                <label for="" class="col-sm-3 control-label"
                    >Name Authority:</label
                >
                <div class="col-sm-8">
                    <textarea
                        id="name_authority"
                        v-model="name_authority"
                        :disabled="true"
                        rows="1"
                        class="form-control"
                        placeholder=""
                    />
                </div>
            </div>
            <div class="row mb-3">
                <label for="" class="col-sm-3 control-label"
                    >Name names comments:</label
                >
                <div class="col-sm-8">
                    <textarea
                        id="comment"
                        v-model="name_comments"
                        :disabled="true"
                        class="form-control"
                        rows="3"
                        placeholder=""
                    />
                </div>
            </div>
        </FormSection>
        <FormSection
            :form-collapse="false"
            label="Distribution"
            :Index="distributionBody"
        >
            <div class="row mb-3">
                <div
                    v-for="species in original_species_combine_list"
                    :key="species.id"
                    class="row mb-3"
                >
                    <label for="" class="col-sm-3 control-label"
                        >{{ species.species_number }} Distribution:</label
                    >
                    <div class="col-sm-8">
                        <textarea
                            v-model="species.distribution.distribution"
                            :disabled="true"
                            type="text"
                            class="form-control"
                            placeholder=""
                        />
                    </div>
                    <div class="col-sm-1">
                        <input
                            :id="'distribution' + species.id"
                            class="form-check-input"
                            type="checkbox"
                            name="distribution_chk"
                            @change="
                                checkDistributionInput(
                                    'distribution_chk',
                                    'distribution' + species.id,
                                    'distribution',
                                    species.distribution.distribution
                                )
                            "
                        />
                    </div>
                </div>
            </div>
            <div class="row mb-3">
                <label for="" class="col-sm-3 control-label"
                    >Distribution:</label
                >
                <div class="col-sm-9">
                    <textarea
                        id="distribution"
                        v-model="species_community.distribution.distribution"
                        :disabled="isReadOnly"
                        class="form-control"
                        rows="1"
                        placeholder=""
                    />
                </div>
            </div>
            <div>
                <div
                    v-for="species in original_species_combine_list"
                    :key="species.id"
                    class="row mb-3"
                >
                    <label for="" class="col-sm-3 control-label"
                        >{{ species.species_number }} Region:</label
                    >
                    <div class="col-sm-8">
                        <label for="" class="control-label">{{
                            getselectedRegionNames(species)
                        }}</label>
                    </div>
                    <div class="col-sm-1">
                        <!-- checkInput(checkbox_id , v-model object attribute of this field) -->
                        <input
                            :id="'regions_select_chk' + species.id"
                            class="form-check-input"
                            type="checkbox"
                            @change="
                                checkRegionDistrictInput(
                                    'regions_select_chk' + species.id,
                                    'regions',
                                    species,
                                    'regions_select'
                                )
                            "
                        />
                    </div>
                </div>
            </div>
            <div class="row mb-3">
                <label for="" class="col-sm-3 control-label">Region:</label>
                <div :id="select_regions" class="col-sm-8">
                    <select
                        ref="regions_select"
                        v-model="species_community.regions"
                        :disabled="isReadOnly"
                        style="width: 100%"
                        class="form-select input-sm"
                    >
                        <option value="" selected disabled>
                            Select region
                        </option>
                        <option
                            v-for="option in region_list"
                            :key="option.value"
                            :value="option.value"
                        >
                            {{ option.text }}
                        </option>
                    </select>
                </div>
            </div>
            <div>
                <div
                    v-for="species in original_species_combine_list"
                    :key="species.id"
                    class="row mb-3"
                >
                    <label for="" class="col-sm-3 control-label"
                        >{{ species.species_number }} District:</label
                    >
                    <div class="col-sm-8">
                        <label for="" class="control-label">{{
                            getselectedDistrictNames(species)
                        }}</label>
                    </div>
                    <div class="col-sm-1">
                        <!-- checkInput(checkbox_id , v-model object attribute of this field) -->
                        <input
                            :id="'districts_select_chk' + species.id"
                            class="form-check-input"
                            type="checkbox"
                            @change="
                                checkRegionDistrictInput(
                                    'districts_select_chk' + species.id,
                                    'districts',
                                    species,
                                    'districts_select'
                                )
                            "
                        />
                    </div>
                </div>
            </div>
            <div class="row mb-3">
                <label for="" class="col-sm-3 control-label">District:</label>
                <div :id="select_districts" class="col-sm-8">
                    <select
                        ref="districts_select"
                        v-model="species_community.districts"
                        :disabled="isReadOnly"
                        class="form-select"
                    >
                        <option value="" selected disabled>
                            Select district
                        </option>
                        <option
                            v-for="option in district_list"
                            :key="option.value"
                            :value="option.value"
                        >
                            {{ option.text }}
                        </option>
                    </select>
                </div>
            </div>
            <div>
                <div
                    v-for="species in original_species_combine_list"
                    :key="species.id"
                    class="row mb-3"
                >
                    <label for="" class="col-sm-3 control-label"
                        >{{ species.species_number }} Number of
                        Occurrences:</label
                    >
                    <div class="col-sm-8">
                        <input
                            id="no_of_occurrences_orig"
                            v-model="species.distribution.number_of_occurrences"
                            :disabled="true"
                            type="number"
                            class="form-control"
                            placeholder=""
                        />
                    </div>
                </div>
            </div>
            <div class="row mb-3">
                <label for="" class="col-sm-3 control-label"
                    >Number of Occurrences:</label
                >
                <div class="col-sm-6">
                    <input
                        id="no_of_occurrences"
                        v-model="
                            species_community.distribution.number_of_occurrences
                        "
                        :disabled="isReadOnly"
                        type="number"
                        class="form-control"
                        placeholder=""
                    />
                </div>
                <div class="col-sm-3">
                    <div class="form-check form-check-inline">
                        <input
                            v-model="species_community.distribution.noo_auto"
                            :disabled="isReadOnly"
                            type="radio"
                            value="true"
                            class="noo_auto form-check-input"
                            name="noo_auto"
                        />
                        <label class="form-check-label">auto</label>
                    </div>
                    <div class="form-check form-check-inline">
                        <input
                            v-model="species_community.distribution.noo_auto"
                            :disabled="isReadOnly"
                            type="radio"
                            value="false"
                            class="noo_auto form-check-input"
                            name="noo_auto"
                        />
                        <label class="form-check-label">manual</label>
                    </div>
                </div>
            </div>
            <div>
                <div
                    v-for="species in original_species_combine_list"
                    :key="species.id"
                    class="row mb-3"
                >
                    <label for="" class="col-sm-3 control-label"
                        >{{ species.species_number }} Extent of Occurrences
                        (km2):</label
                    >
                    <div class="col-sm-8">
                        <input
                            id="extent_of_occurrence_orig"
                            v-model="species.distribution.extent_of_occurrences"
                            :disabled="true"
                            type="number"
                            class="form-control"
                            placeholder=""
                        />
                    </div>
                </div>
            </div>
            <div class="row mb-3">
                <label for="" class="col-sm-3 control-label"
                    >Extent of Occurrence (km2):</label
                >
                <div class="col-sm-6">
                    <input
                        id="extent_of_occurrence"
                        v-model="
                            species_community.distribution.extent_of_occurrences
                        "
                        :disabled="isReadOnly"
                        type="number"
                        class="form-control"
                        placeholder=""
                    />
                </div>
                <div class="col-sm-3">
                    <div class="form-check form-check-inline">
                        <input
                            v-model="species_community.distribution.eoo_auto"
                            :disabled="isReadOnly"
                            type="radio"
                            value="true"
                            class="eoo_auto form-check-input"
                            name="eoo_auto"
                        />
                        <label class="form-check-label">auto</label>
                    </div>
                    <div class="form-check form-check-inline">
                        <input
                            v-model="species_community.distribution.eoo_auto"
                            :disabled="isReadOnly"
                            type="radio"
                            value="false"
                            class="eoo_auto form-check-input"
                            name="eoo_auto"
                        />
                        <label class="form-check-label">manual</label>
                    </div>
                </div>
            </div>
            <div>
                <div
                    v-for="species in original_species_combine_list"
                    :key="species.id"
                    class="row mb-3"
                >
                    <label for="" class="col-sm-3 control-label"
                        >{{ species.species_number }} Actual Area of
                        Occupancy<br />(km2):</label
                    >
                    <div class="col-sm-8">
                        <input
                            id="area_of_occupancy_actual_orig"
                            v-model="
                                species.distribution.area_of_occupancy_actual
                            "
                            :disabled="true"
                            type="number"
                            class="form-control"
                            placeholder=""
                        />
                    </div>
                </div>
            </div>
            <div class="row mb-3">
                <label for="" class="col-sm-3 control-label"
                    >Actual Area of Occupancy<br />(km2):</label
                >
                <div class="col-sm-6">
                    <input
                        id="area_of_occupancy_actual"
                        v-model="
                            species_community.distribution
                                .area_of_occupancy_actual
                        "
                        :disabled="isReadOnly"
                        type="number"
                        class="form-control"
                        placeholder=""
                    />
                </div>
                <div class="col-sm-3">
                    <div class="form-check form-check-inline">
                        <input
                            v-model="
                                species_community.distribution.aoo_actual_auto
                            "
                            :disabled="isReadOnly"
                            type="radio"
                            value="true"
                            class="aoo_actual_auto form-check-input"
                            name="aoo_actual_auto"
                        />
                        <label class="form-check-label">auto</label>
                    </div>
                    <div class="form-check form-check-inline">
                        <input
                            v-model="
                                species_community.distribution.aoo_actual_auto
                            "
                            :disabled="isReadOnly"
                            type="radio"
                            value="false"
                            class="aoo_actual_auto form-check-input"
                            name="aoo_actual_auto"
                        />
                        <label class="form-check-label">manual</label>
                    </div>
                </div>
            </div>
            <div>
                <div
                    v-for="species in original_species_combine_list"
                    :key="species.id"
                    class="row mb-3"
                >
                    <label for="" class="col-sm-3 control-label"
                        >{{ species.species_number }} Area of Occupancy<br />(km2):</label
                    >
                    <div class="col-sm-8">
                        <input
                            id="area_of_occupany_orig"
                            v-model="species.distribution.area_of_occupancy"
                            :disabled="true"
                            type="number"
                            class="form-control"
                            placeholder=""
                        />
                    </div>
                </div>
            </div>
            <div class="row mb-3">
                <label for="" class="col-sm-3 control-label"
                    >Area of Occupancy<br />(10km x 10km):</label
                >
                <div class="col-sm-6">
                    <input
                        id="area_of_occupany"
                        v-model="
                            species_community.distribution.area_of_occupancy
                        "
                        :disabled="isReadOnly"
                        type="number"
                        class="form-control"
                        placeholder=""
                    />
                </div>
            </div>
            <div>
                <div
                    v-for="species in original_species_combine_list"
                    :key="species.id"
                    class="row mb-3"
                >
                    <label for="" class="col-sm-3 control-label"
                        >{{ species.species_number }} Number of IUCN
                        Locations:</label
                    >
                    <div class="col-sm-8">
                        <input
                            id="no_of_iucn_locations"
                            v-model="
                                species.distribution.number_of_iucn_locations
                            "
                            :disabled="true"
                            type="number"
                            class="form-control"
                            placeholder=""
                        />
                    </div>
                </div>
            </div>
            <div class="row mb-3">
                <label for="" class="col-sm-3 control-label"
                    >Number of IUCN Locations:</label
                >
                <div class="col-sm-8">
                    <input
                        id="no_of_iucn_locations"
                        v-model="
                            species_community.distribution
                                .number_of_iucn_locations
                        "
                        :disabled="isReadOnly"
                        type="number"
                        class="form-control"
                        placeholder=""
                    />
                </div>
            </div>
        </FormSection>
        <!--
        <FormSection :formCollapse="false" label="Conservation Attributes" :Index="conservationBody">
            <div class="row mb-3">
                <div class="row mb-3" v-for="species in original_species_combine_list">
                    <label for="" class="col-sm-3 control-label">{{ species.species_number }} Habitat/Growth Form:</label>
                    <div class="col-sm-8">
                        <textarea :disabled="true" type="text" class="form-control" placeholder=""
                        v-model="species.conservation_attributes.habitat_growth_form"/>
                    </div>
                    <div class="col-sm-1">
                        <input class="form-check-input" type="checkbox" name="habitat_frm_chk" :id="'habitat_frm_chk'+species.id"
                        @change="checkConservationInput('habitat_frm_chk','habitat_frm_chk'+species.id,'habitat_growth_form',species.conservation_attributes.habitat_growth_form)" />
                    </div>
                </div>
            </div>
            <div class="row mb-3">
                <label for="" class="col-sm-3 control-label">Habitat/Growth Form:</label>
                <div class="col-sm-8">
                <textarea :disabled="isReadOnly" type="text" class="form-control"
                    id="habitat_new" placeholder="" v-model="species_community.conservation_attributes.habitat_growth_form" />
                </div>
            </div>

            <div v-show="!isFauna">
                <div class="row mb-3" v-for="species in original_species_combine_list">
                    <label for="" class="col-sm-3 control-label">{{ species.species_number }} Flowering Period:</label>
                   <div class="col-sm-8" :id="select_flowering_period_readonly">
                        <select :disabled="true"
                            style="width:100%;" class="form-select input-sm" multiple
                            ref="flowering_period_select_readonly"
                            v-model="species.conservation_attributes.flowering_period" >
                            <option v-for="option in period_list" :value="option.id" :key="option.id">
                                {{option.name}}
                            </option>
                        </select>
                    </div>
                    <div class="col-sm-1">
                        <input class="form-check-input" type="checkbox" name="flowering_prd_chk" :id="'flowering_prd_chk'+species.id"
                        @change="checkConservationInput('flowering_prd_chk','flowering_prd_chk'+species.id,'flowering_period',species.conservation_attributes.flowering_period, 'flowering_period_select')" />
                    </div>
                </div>
            </div>
            <div class="row mb-3" v-show="!isFauna">
                <label for="" class="col-sm-3 control-label">Flowering Period:</label>
                <div class="col-sm-8" :id="select_flowering_period">
                    <select :disabled="isReadOnly"
                        style="width:100%;" class="form-select input-sm" multiple
                        ref="flowering_period_select"
                        v-model="species_community.conservation_attributes.flowering_period" >
                        <option v-for="option in period_list" :value="option.id" :key="option.id">
                            {{option.name}}
                        </option>
                    </select>
                </div>
            </div>

            <div v-show="!isFauna">
                <div class="row mb-3" v-for="species in original_species_combine_list">
                    <label for="" class="col-sm-3 control-label">{{ species.species_number }} Fruiting Period:</label>
                    <div class="col-sm-8" :id="select_fruiting_period_readonly">
                        <select :disabled="true"
                            style="width:100%;" class="form-select input-sm" multiple
                            ref="fruiting_period_select_readonly"
                            v-model="species.conservation_attributes.fruiting_period" >
                            <option v-for="option in period_list" :value="option.id" :key="option.id">
                                {{option.name}}
                            </option>
                        </select>
                    </div>
                    <div class="col-sm-1">
                        <input class="form-check-input" type="checkbox" name="fruiting_prd_chk" :id="'fruiting_prd_chk'+species.id"
                        @change="checkConservationInput('fruiting_prd_chk','fruiting_prd_chk'+species.id,'fruiting_period',species.conservation_attributes.fruiting_period, 'fruiting_period_select')" />
                    </div>
                </div>
            </div>
            <div class="row mb-3" v-show="!isFauna">
                <label for="" class="col-sm-3 control-label">Fruiting Period:</label>
                <div class="col-sm-8" :id="select_fruiting_period">
                    <select :disabled="isReadOnly"
                        style="width:100%;" class="form-select input-sm" multiple
                        ref="fruiting_period_select"
                        v-model="species_community.conservation_attributes.fruiting_period" >
                        <option v-for="option in period_list" :value="option.id" :key="option.id">
                            {{option.name}}
                        </option>
                    </select>
                </div>
            </div>

            <div v-show="!isFauna">
                <div class="row mb-3" v-for="species in original_species_combine_list">
                    <label for="" class="col-sm-3 control-label">{{ species.species_number }} Flora Recruitment Type:</label>
                    <div class="col-sm-8">
                        <select :disabled="true" class="form-select"
                            v-model="species.conservation_attributes.flora_recruitment_type_id">
                            <option v-for="option in flora_recruitment_type_list" :value="option.id" v-bind:key="option.id">
                                {{ option.name }}
                            </option>
                        </select>
                    </div>
                    <div class="col-sm-1">
                        <input class="form-check-input" type="checkbox" name="flora_recruit_type_chk" :id="'flora_recruit_type_chk'+species.id"
                        @change="checkConservationInput('flora_recruit_type_chk','flora_recruit_type_chk'+species.id,'flora_recruitment_type_id', species.conservation_attributes.flora_recruitment_type_id)" />
                    </div>
                </div>
            </div>
            <div class="row mb-3" v-show="!isFauna">
                <label for="" class="col-sm-3 control-label">Flora Recruitment Type:</label>
                <div class="col-sm-8">
                    <select :disabled="isReadOnly" class="form-select"
                        v-model="species_community.conservation_attributes.flora_recruitment_type_id">
                        <option v-for="option in flora_recruitment_type_list" :value="option.id" v-bind:key="option.id">
                            {{ option.name }}
                        </option>
                    </select>
                </div>
            </div>

            <div v-show="!isFauna">
                <div class="row mb-3" v-for="species in original_species_combine_list">
                    <label for="" class="col-sm-3 control-label">{{ species.species_number }} Flora Recruitment Notes:</label>
                    <div class="col-sm-8">
                        <textarea :disabled="true" type="text" class="form-control"
                        id="recruitment_notes" placeholder=""
                        v-model="species.conservation_attributes.flora_recruitment_notes"/>
                    </div>
                    <div class="col-sm-1">
                        <input class="form-check-input" type="checkbox" name="flora_recruit_notes_chk" :id="'flora_recruit_notes_chk'+species.id"
                        @change="checkConservationInput('flora_recruit_notes_chk','flora_recruit_notes_chk'+species.id,'flora_recruitment_notes', species.conservation_attributes.flora_recruitment_notes)" />
                    </div>
                </div>
            </div>
            <div class="row mb-3" v-show="!isFauna">
                <label for="" class="col-sm-3 control-label">Flora Recruitment Notes:</label>
                <div class="col-sm-8">
                    <textarea :disabled="isReadOnly" type="text" class="form-control"
                    id="recruitment_notes" placeholder=""
                    v-model="species_community.conservation_attributes.flora_recruitment_notes"/>
                </div>
            </div>

            <div v-show="!isFauna">
                <div class="row mb-3" v-for="species in original_species_combine_list">
                    <label for="" class="col-sm-3 control-label">{{ species.species_number }} Seed Viability and Germination Info:</label>
                    <div class="col-sm-8">
                        <select :disabled="true" class="form-select"
                            v-model="species.conservation_attributes.seed_viability_germination_info_id">
                            <option v-for="option in seed_viability_germination_info_list" :value="option.id" v-bind:key="option.id">
                                {{ option.name }}
                            </option>
                        </select>
                    </div> - ->
                    <div class="col-sm-8">
                        <textarea :disabled="true" type="text" class="form-control" placeholder=""
                        v-model="species.conservation_attributes.seed_viability_germination_info"/>
                    </div>
                    <div class="col-sm-1">
                        <input class="form-check-input" type="checkbox" name="seed_viability_chk" :id="'seed_viability_chk'+species.id"
                        @change="checkConservationInput('seed_viability_chk','seed_viability_chk'+species.id, 'seed_viability_germination_info', species.conservation_attributes.seed_viability_germination_info)" />
                    </div>
                </div>
            </div>
            <div class="row mb-3" v-show="!isFauna">
                <label for="" class="col-sm-3 control-label">Seed Viability and Germination Info:</label>
                <div class="col-sm-8">
                    <!- - <select :disabled="isReadOnly" class="form-select"
                        v-model="species_community.conservation_attributes.seed_viability_germination_info_id">
                        <option v-for="option in seed_viability_germination_info_list" :value="option.id" v-bind:key="option.id">
                            {{ option.name }}
                        </option>
                    </select> - ->
                    <textarea :disabled="isReadOnly" type="text" class="form-control" placeholder=""
                        v-model="species_community.conservation_attributes.seed_viability_germination_info"/>
                </div>
            </div>

            <div v-show="!isFauna">
                <div class="row mb-3" v-for="species in original_species_combine_list">
                    <label for="" class="col-sm-3 control-label">{{ species.species_number }} Root Morphology:</label>
                    <div class="col-sm-8">
                        <select :disabled="true" class="form-select"
                            v-model="species.conservation_attributes.root_morphology_id">
                            <option v-for="option in root_morphology_list" :value="option.id" v-bind:key="option.id">
                                {{ option.name }}
                            </option>
                        </select>
                    </div>
                    <div class="col-sm-1">
                        <input class="form-check-input" type="checkbox" name="root_morphology_chk" :id="'root_morphology_chk'+species.id"
                        @change="checkConservationInput('root_morphology_chk','root_morphology_chk'+species.id,'root_morphology_id', species.conservation_attributes.root_morphology_id)" />
                    </div>
                </div>
            </div>
            <div class="row mb-3" v-show="!isFauna">
                <label for="" class="col-sm-3 control-label">Root Morphology:</label>
                <div class="col-sm-8">
                    <select :disabled="isReadOnly" class="form-select"
                        v-model="species_community.conservation_attributes.root_morphology_id">
                        <option v-for="option in root_morphology_list" :value="option.id" v-bind:key="option.id">
                            {{ option.name }}
                        </option>
                    </select>
                </div>
            </div>

            <div v-show="!isFauna">
                <div class="row mb-3" v-for="species in original_species_combine_list">
                    <label for="" class="col-sm-3 control-label">{{ species.species_number }} Pollinator Information:</label>
                    <div class="col-sm-8">
                        <!- - <select :disabled="true" class="form-select"
                            v-model="species.conservation_attributes.pollinator_information_id">
                            <option v-for="option in pollinator_info_list" :value="option.id" v-bind:key="option.id">
                                {{ option.name }}
                            </option>
                        </select> - ->
                        <textarea :disabled="true" type="text" class="form-control" placeholder=""
                        v-model="species.conservation_attributes.pollinator_information"/>
                    </div>
                    <div class="col-sm-1">
                        <input class="form-check-input" type="checkbox" name="pollinator_chk" :id="'pollinator_chk'+species.id"
                        @change="checkConservationInput('pollinator_chk','pollinator_chk'+species.id,'pollinator_information', species.conservation_attributes.pollinator_information)" />
                    </div>
                </div>
            </div>
            <div class="row mb-3" v-show="!isFauna">
                <label for="" class="col-sm-3 control-label">Pollinator Information:</label>
                <div class="col-sm-8">
                    <!- - <select :disabled="isReadOnly" class="form-select"
                        v-model="species_community.conservation_attributes.pollinator_information_id">
                        <option v-for="option in pollinator_info_list" :value="option.id" v-bind:key="option.id">
                            {{ option.name }}
                        </option>
                    </select> - ->
                    <textarea :disabled="isReadOnly" type="text" class="form-control" placeholder=""
                        v-model="species_community.conservation_attributes.pollinator_information"/>
                </div>
            </div>

            <div v-show="isFauna">
                <div class="row mb-3" v-for="species in original_species_combine_list">
                    <label for="" class="col-sm-3 control-label">{{ species.species_number }} Breeding Period:</label>
                    <div class="col-sm-8" :id="select_breeding_period_readonly">
                        <select :disabled="true"
                            style="width:100%;" class="form-select input-sm" multiple
                            ref="breeding_period_select_readonly"
                            v-model="species.conservation_attributes.breeding_period" >
                            <option v-for="option in period_list" :value="option.id" :key="option.id">
                                {{option.name}}
                            </option>
                        </select>
                    </div>
                    <div class="col-sm-1">
                        <input class="form-check-input" type="checkbox" name="breeding_prd_chk" :id="'breeding_prd_chk'+species.id"
                        @change="checkConservationInput('breeding_prd_chk','breeding_prd_chk'+species.id,'breeding_period', species.conservation_attributes.breeding_period, 'breeding_period_select')" />
                    </div>
                </div>
            </div>
            <div class="row mb-3" v-show="isFauna">
                <label for="" class="col-sm-3 control-label">Breeding Period:</label>
                <div class="col-sm-8" :id="select_breeding_period">
                    <select :disabled="isReadOnly"
                        style="width:100%;" class="form-select input-sm" multiple
                        ref="breeding_period_select"
                        v-model="species_community.conservation_attributes.breeding_period" >
                        <option v-for="option in period_list" :value="option.id" :key="option.id">
                            {{option.name}}
                        </option>
                    </select>
                </div>
            </div>

            <div v-show="isFauna">
                <div class="row mb-3" v-for="species in original_species_combine_list">
                    <label for="" class="col-sm-3 control-label">{{ species.species_number }} Fauna Breeding:</label>
                    <div class="col-sm-8">
                        <!- - <div v-for="option in fauna_breeding_list">
                            <input :disabled="true" class='form-check-input' type="radio" v-bind:value="option.id"
                                :id="'breeding_type_'+option.id"
                                v-model="species.conservation_attributes.fauna_breeding_id">
                            <label :for="'breeding_type_'+option.id">{{ option.name }}</label>
                        </div> - ->
                        <textarea :disabled="true" type="text" class="form-control" placeholder=""
                        v-model="species.conservation_attributes.fauna_breeding"/>
                    </div>
                    <div class="col-sm-1">
                        <input class="form-check-input" type="checkbox" name="breeding_type_chk" :id="'breeding_type_chk'+species.id"
                        @change="checkConservationInput('breeding_type_chk','breeding_type_chk'+species.id,'fauna_breeding', species.conservation_attributes.fauna_breeding)" />
                    </div>
                </div>
            </div>
            <div class="row mb-3" v-show="isFauna">
                <label for="" class="col-sm-3 control-label">Fauna Breeding:</label>
                <div class="col-sm-8">
                    <!- - <div v-for="option in fauna_breeding_list">
                        <input :disabled="isReadOnly" class='form-check-input' type="radio" v-bind:value="option.id"
                            :id="'breeding_type_'+option.id"
                            v-model="species_community.conservation_attributes.fauna_breeding_id">
                        <label :for="'breeding_type_'+option.id">{{ option.name }}</label>
                    </div> - ->
                    <textarea :disabled="isReadOnly" type="text" class="form-control" placeholder=""
                        v-model="species_community.conservation_attributes.fauna_breeding"/>
                </div>
            </div>

            <div v-show="isFauna">
                <div class="row mb-3" v-for="species in original_species_combine_list">
                    <label for="" class="col-sm-3 control-label">{{ species.species_number }} Fauna Reproductive capacity:</label>
                    <div class="col-sm-8">
                        <input :disabled="true" type="text" class="form-control"
                        id="fauna_reproductive_capacity" placeholder=""
                        v-model="species.conservation_attributes.fauna_reproductive_capacity"/>
                    </div>
                    <div class="col-sm-1">
                        <input class="form-check-input" type="checkbox" name="reproductive_cap_chk" :id="'reproductive_cap_chk'+species.id"
                        @change="checkConservationInput('reproductive_cap_chk','reproductive_cap_chk'+species.id,'fauna_reproductive_capacity', species.conservation_attributes.fauna_reproductive_capacity)" />
                    </div>
                </div>
            </div>
            <div class="row mb-3" v-show="isFauna">
                <label for="" class="col-sm-3 control-label">Fauna Reproductive capacity:</label>
                <div class="col-sm-8">
                    <input :disabled="isReadOnly" type="text" class="form-control"
                    id="fauna_reproductive_capacity" placeholder=""
                    v-model="species_community.conservation_attributes.fauna_reproductive_capacity"/>
                </div>
            </div>
            <div v-for="species in original_species_combine_list">
                <div class="row mb-3">
                    <label for="" class="col-sm-3 control-label">{{ species.species_number }} Time to Maturity:</label>
                    <div class="col-sm-8">
                        <input class="form-check-input" type="checkbox" :id="'time_to_maturity_range_original'+species.id"
                         disabled="true" />
                        <label for="" class="control-label">Range</label>
                    </div>
                    <div class="col-sm-1">
                        <input class="form-check-input" type="checkbox" name="maturity_time_chk" :id="'maturity_time_chk'+species.id"
                        @change="checkConservationInput('maturity_time_chk','maturity_time_chk'+species.id,'time_to_maturity', species.conservation_attributes.time_to_maturity_from,'',species.conservation_attributes.time_to_maturity_to,species.conservation_attributes.time_to_maturity_choice)" />
                    </div>
                </div>

                <div class="row mb-3" v-if="!isOriginalRangeChecked('time_to_maturity_range_original'+species.id, species.id,'time_to_maturity_to')">
                    <label for="" class="col-sm-3 control-label"></label>
                    <div class="col-sm-3 interval-margin">
                        <input disabled="true" type="number" class="form-control"
                        id="time_to_maturity_from" placeholder=""
                        v-model="species.conservation_attributes.time_to_maturity_from"/>
                    </div>
                    <div class="col-sm-2 interval-range-true-choice">
                        <select disabled="true" class="form-select"
                            v-model="species.conservation_attributes.time_to_maturity_choice">
                            <option v-for="option in interval_choice" :value="option.id" v-bind:key="option.id">
                                {{ option.name }}
                            </option>
                        </select>
                    </div>
                    <div class="col-sm-4">
                        <label for="" class="control-label">{{ intervalMonthsComputedOriginal(species.conservation_attributes.time_to_maturity_from, species.conservation_attributes.time_to_maturity_choice)}}</label>
                    </div>
                </div>
                <div class="row mb-3" v-else>
                        <label for="" class="col-sm-3 control-label"></label>
                        <label for="" class="col-sm-2 control-label">From:</label>
                        <div class="col-sm-2 interval-range-true-input">
                            <input disabled="true" type="number" class="form-control"
                            id="time_to_maturity_from" placeholder=""
                            v-model="species.conservation_attributes.time_to_maturity_from"/>
                        </div>
                        <label for="" class="col-sm-2 control-label">To:</label>
                        <div class="col-sm-2 interval-range-true-input">
                            <input disabled="true" type="number" class="form-control"
                            id="time_to_maturity_to" placeholder=""
                            v-model="species.conservation_attributes.time_to_maturity_to"/>
                        </div>
                        <div class="col-sm-2 interval-range-true-choice">
                            <select disabled="true" class="form-select"
                                v-model="species.conservation_attributes.time_to_maturity_choice">
                                <option v-for="option in interval_choice" :value="option.id" v-bind:key="option.id">
                                    {{ option.name }}
                                </option>
                            </select>
                        </div>
                </div>
            </div>
            <div class="row mb-3">
                <label for="" class="col-sm-3 control-label">Time to Maturity:</label>
                <div class="col-sm-3">
                    <input class="form-check-input" type="checkbox" id="time_to_maturity_range_new"
                        v-model="time_to_maturity_range_new" :disabled="isReadOnly" @change="handleTimeToMaturityRange()" />
                    <label for="" class="control-label">Range</label>
                </div>
                <label for="" class="col-sm-6 control-label" style="color: red;">{{ errors.time_to_maturity_error }}</label>
            </div>
            <div class="row mb-3" v-if="!time_to_maturity_range_new">
                <label for="" class="col-sm-3 control-label"></label>
                <div class="col-sm-3 interval-margin">
                    <input :disabled="isReadOnly" type="number" class="form-control"
                    id="time_to_maturity_from" placeholder="" @change="validateRange('time_to_maturity_from','time_to_maturity_to','time_to_maturity_choice','time_to_maturity_error')"
                    v-model="species_community.conservation_attributes.time_to_maturity_from"/>
                </div>
                <div class="col-sm-2 interval-range-true-choice">
                    <select :disabled="isReadOnly" class="form-select" @change="validateRange('time_to_maturity_from','time_to_maturity_to','time_to_maturity_choice','time_to_maturity_error')"
                        v-model="species_community.conservation_attributes.time_to_maturity_choice">
                        <option v-for="option in interval_choice" :value="option.id" v-bind:key="option.id">
                            {{ option.name }}
                        </option>
                    </select>
                </div>
                <div class="col-sm-4">
                    <label for="" class="control-label">{{ intervalMonthsComputedNew('time_to_maturity_from','time_to_maturity_choice') }}</label>
                </div>
            </div>
            <div class="row mb-3" v-else>
                    <label for="" class="col-sm-3 control-label"></label>
                    <label for="" class="col-sm-2 control-label">From:</label>
                    <div class="col-sm-2 interval-range-true-input">
                        <input :disabled="isReadOnly" type="number" class="form-control"
                        id="time_to_maturity_from" placeholder="" @change="validateRange('time_to_maturity_from','time_to_maturity_to','time_to_maturity_choice','time_to_maturity_error')"
                        v-model="species_community.conservation_attributes.time_to_maturity_from"/>
                    </div>
                    <label for="" class="col-sm-2 control-label">To:</label>
                    <div class="col-sm-2 interval-range-true-input">
                        <input :disabled="isReadOnly" type="number" class="form-control"
                        id="time_to_maturity_to" placeholder="" @change="validateRange('time_to_maturity_from','time_to_maturity_to','time_to_maturity_choice','time_to_maturity_error')"
                        v-model="species_community.conservation_attributes.time_to_maturity_to"/>
                    </div>
                    <div class="col-sm-2 interval-range-true-choice">
                        <select :disabled="isReadOnly" class="form-select" @change="validateRange('time_to_maturity_from','time_to_maturity_to','time_to_maturity_choice','time_to_maturity_error')"
                            v-model="species_community.conservation_attributes.time_to_maturity_choice">
                            <option v-for="option in interval_choice" :value="option.id" v-bind:key="option.id">
                                {{ option.name }}
                            </option>
                        </select>
                    </div>
            </div>
             <div v-for="species in original_species_combine_list">
                <div class="row mb-3">
                    <label for="" class="col-sm-3 control-label">{{ species.species_number }} Generation Length:</label>
                    <div class="col-sm-8">
                        <input class="form-check-input" type="checkbox" :id="'generation_length_range_original'+species.id"
                         disabled="true" />
                        <label for="" class="control-label">Range</label>
                    </div>
                    <div class="col-sm-1">
                        <input class="form-check-input" type="checkbox" name="generation_chk" :id="'generation_chk'+species.id"
                        @change="checkConservationInput('generation_chk','generation_chk'+species.id,'generation_length', species.conservation_attributes.generation_length_from,'',species.conservation_attributes.generation_length_to,species.conservation_attributes.generation_length_choice)" />
                    </div>
                </div>

                <div class="row mb-3" v-if="!isOriginalRangeChecked('generation_length_range_original'+species.id, species.id,'generation_length_to')">
                    <label for="" class="col-sm-3 control-label"></label>
                    <div class="col-sm-3 interval-margin">
                        <input disabled="true" type="number" class="form-control"
                        id="generation_length_from" placeholder=""
                        v-model="species.conservation_attributes.generation_length_from"/>
                    </div>
                    <div class="col-sm-2 interval-range-true-choice">
                        <select disabled="true" class="form-select"
                            v-model="species.conservation_attributes.generation_length_choice">
                            <option v-for="option in interval_choice" :value="option.id" v-bind:key="option.id">
                                {{ option.name }}
                            </option>
                        </select>
                    </div>
                    <div class="col-sm-4">
                        <label for="" class="control-label">{{ intervalMonthsComputedOriginal(species.conservation_attributes.generation_length_from, species.conservation_attributes.generation_length_choice)}}</label>
                    </div>
                </div>
                <div class="row mb-3" v-else>
                        <label for="" class="col-sm-3 control-label"></label>
                        <label for="" class="col-sm-2 control-label">From:</label>
                        <div class="col-sm-2 interval-range-true-input">
                            <input disabled="true" type="number" class="form-control"
                            id="generation_length_from" placeholder=""
                            v-model="species.conservation_attributes.generation_length_from"/>
                        </div>
                        <label for="" class="col-sm-2 control-label">To:</label>
                        <div class="col-sm-2 interval-range-true-input">
                            <input disabled="true" type="number" class="form-control"
                            id="generation_length_to" placeholder=""
                            v-model="species.conservation_attributes.generation_length_to"/>
                        </div>
                        <div class="col-sm-2 interval-range-true-choice">
                            <select disabled="true" class="form-select"
                                v-model="species.conservation_attributes.generation_length_choice">
                                <option v-for="option in interval_choice" :value="option.id" v-bind:key="option.id">
                                    {{ option.name }}
                                </option>
                            </select>
                        </div>
                </div>
            </div>
            <div class="row mb-3">
                <label for="" class="col-sm-3 control-label">Generation Length:</label>
                <div class="col-sm-3">
                    <input class="form-check-input" type="checkbox" id="generation_length_range_new"
                        v-model="generation_length_range_new" :disabled="isReadOnly" @change="handleGenerationLengthRange()" />
                    <label for="" class="control-label">Range</label>
                </div>
                <label for="" class="col-sm-6 control-label" style="color: red;">{{ errors.generation_length_error }}</label>
            </div>
            <div class="row mb-3" v-if="!generation_length_range_new">
                <label for="" class="col-sm-3 control-label"></label>
                <div class="col-sm-3 interval-margin">
                    <input :disabled="isReadOnly" type="number" class="form-control"
                    id="generation_length_from" placeholder="" @change="validateRange('generation_length_from','generation_length_to','generation_length_choice','generation_length_error')"
                    v-model="species_community.conservation_attributes.generation_length_from"/>
                </div>
                <div class="col-sm-2 interval-range-true-choice">
                    <select :disabled="isReadOnly" class="form-select" @change="validateRange('generation_length_from','generation_length_to','generation_length_choice','generation_length_error')"
                        v-model="species_community.conservation_attributes.generation_length_choice">
                        <option v-for="option in interval_choice" :value="option.id" v-bind:key="option.id">
                            {{ option.name }}
                        </option>
                    </select>
                </div>
                <div class="col-sm-4">
                    <label for="" class="control-label">{{ intervalMonthsComputedNew('generation_length_from','generation_length_choice') }}</label>
                </div>
            </div>
            <div class="row mb-3" v-else>
                    <label for="" class="col-sm-3 control-label"></label>
                    <label for="" class="col-sm-2 control-label">From:</label>
                    <div class="col-sm-2 interval-range-true-input">
                        <input :disabled="isReadOnly" type="number" class="form-control"
                        id="generation_length_from" placeholder="" @change="validateRange('generation_length_from','generation_length_to','generation_length_choice','generation_length_error')"
                        v-model="species_community.conservation_attributes.generation_length_from"/>
                    </div>
                    <label for="" class="col-sm-2 control-label">To:</label>
                    <div class="col-sm-2 interval-range-true-input">
                        <input :disabled="isReadOnly" type="number" class="form-control"
                        id="generation_length_to" placeholder="" @change="validateRange('generation_length_from','generation_length_to','generation_length_choice','generation_length_error')"
                        v-model="species_community.conservation_attributes.generation_length_to"/>
                    </div>
                    <div class="col-sm-2 interval-range-true-choice">
                        <select :disabled="isReadOnly" class="form-select" @change="validateRange('generation_length_from','generation_length_to','generation_length_choice','generation_length_error')"
                            v-model="species_community.conservation_attributes.generation_length_choice">
                            <option v-for="option in interval_choice" :value="option.id" v-bind:key="option.id">
                                {{ option.name }}
                            </option>
                        </select>
                    </div>
            </div>
            <div v-for="species in original_species_combine_list">
                <div class="row mb-3">
                    <label for="" class="col-sm-3 control-label">{{ species.species_number }} Average Lifespan:</label>
                    <div class="col-sm-8">
                        <input class="form-check-input" type="checkbox" :id="'average_lifespan_range_original'+species.id"
                         disabled="true" />
                        <label for="" class="control-label">Range</label>
                    </div>
                    <div class="col-sm-1">
                        <input class="form-check-input" type="checkbox" name="lifespan_chk" :id="'lifespan_chk'+species.id"
                        @change="checkConservationInput('lifespan_chk','lifespan_chk'+species.id,'average_lifespan', species.conservation_attributes.average_lifespan_from,'',species.conservation_attributes.average_lifespan_to,species.conservation_attributes.average_lifespan_choice)" />
                    </div>
                </div>

                <div class="row mb-3" v-if="!isOriginalRangeChecked('average_lifespan_range_original'+species.id, species.id,'average_lifespan_to')">
                    <label for="" class="col-sm-3 control-label"></label>
                    <div class="col-sm-3 interval-margin">
                        <input disabled="true" type="number" class="form-control"
                        id="average_lifespan_from" placeholder=""
                        v-model="species.conservation_attributes.average_lifespan_from"/>
                    </div>
                    <div class="col-sm-2 interval-range-true-choice">
                        <select disabled="true" class="form-select"
                            v-model="species.conservation_attributes.average_lifespan_choice">
                            <option v-for="option in interval_choice" :value="option.id" v-bind:key="option.id">
                                {{ option.name }}
                            </option>
                        </select>
                    </div>
                    <div class="col-sm-4">
                        <label for="" class="control-label">{{ intervalMonthsComputedOriginal(species.conservation_attributes.average_lifespan_from, species.conservation_attributes.average_lifespan_choice)}}</label>
                    </div>
                </div>
                <div class="row mb-3" v-else>
                        <label for="" class="col-sm-3 control-label"></label>
                        <label for="" class="col-sm-2 control-label">From:</label>
                        <div class="col-sm-2 interval-range-true-input">
                            <input disabled="true" type="number" class="form-control"
                            id="average_lifespan_from" placeholder=""
                            v-model="species.conservation_attributes.average_lifespan_from"/>
                        </div>
                        <label for="" class="col-sm-2 control-label">To:</label>
                        <div class="col-sm-2 interval-range-true-input">
                            <input disabled="true" type="number" class="form-control"
                            id="average_lifespan_to" placeholder=""
                            v-model="species.conservation_attributes.average_lifespan_to"/>
                        </div>
                        <div class="col-sm-2 interval-range-true-choice">
                            <select disabled="true" class="form-select"
                                v-model="species.conservation_attributes.average_lifespan_choice">
                                <option v-for="option in interval_choice" :value="option.id" v-bind:key="option.id">
                                    {{ option.name }}
                                </option>
                            </select>
                        </div>
                </div>
            </div>
            <div class="row mb-3">
                <label for="" class="col-sm-3 control-label">Average Lifespan:</label>
                <div class="col-sm-3">
                    <input class="form-check-input" type="checkbox" id="average_lifespan_range_new"
                        v-model="average_lifespan_range_new" :disabled="isReadOnly" @change="handleAverageLifespanRange()" />
                    <label for="" class="control-label">Range</label>
                </div>
                <label for="" class="col-sm-6 control-label" style="color: red;">{{ errors.average_lifespan_error }}</label>
            </div>
            <div class="row mb-3" v-if="!average_lifespan_range_new">
                <label for="" class="col-sm-3 control-label"></label>
                <div class="col-sm-3 interval-margin">
                    <input :disabled="isReadOnly" type="number" class="form-control"
                    id="average_lifespan_from" placeholder="" @change="validateRange('average_lifespan_from','average_lifespan_to','average_lifespan_choice','average_lifespan_error')"
                    v-model="species_community.conservation_attributes.average_lifespan_from"/>
                </div>
                <div class="col-sm-2 interval-range-true-choice">
                    <select :disabled="isReadOnly" class="form-select" @change="validateRange('average_lifespan_from','average_lifespan_to','average_lifespan_choice','average_lifespan_error')"
                        v-model="species_community.conservation_attributes.average_lifespan_choice">
                        <option v-for="option in interval_choice" :value="option.id" v-bind:key="option.id">
                            {{ option.name }}
                        </option>
                    </select>
                </div>
                <div class="col-sm-4">
                    <label for="" class="control-label">{{ intervalMonthsComputedNew('average_lifespan_from','average_lifespan_choice') }}</label>
                </div>
            </div>
            <div class="row mb-3" v-else>
                    <label for="" class="col-sm-3 control-label"></label>
                    <label for="" class="col-sm-2 control-label">From:</label>
                    <div class="col-sm-2 interval-range-true-input">
                        <input :disabled="isReadOnly" type="number" class="form-control"
                        id="average_lifespan_from" placeholder="" @change="validateRange('average_lifespan_from','average_lifespan_to','average_lifespan_choice','average_lifespan_error')"
                        v-model="species_community.conservation_attributes.average_lifespan_from"/>
                    </div>
                    <label for="" class="col-sm-2 control-label">To:</label>
                    <div class="col-sm-2 interval-range-true-input">
                        <input :disabled="isReadOnly" type="number" class="form-control"
                        id="average_lifespan_to" placeholder="" @change="validateRange('average_lifespan_from','average_lifespan_to','average_lifespan_choice','average_lifespan_error')"
                        v-model="species_community.conservation_attributes.average_lifespan_to"/>
                    </div>
                    <div class="col-sm-2 interval-range-true-choice">
                        <select :disabled="isReadOnly" class="form-select" @change="validateRange('average_lifespan_from','average_lifespan_to','average_lifespan_choice','average_lifespan_error')"
                            v-model="species_community.conservation_attributes.average_lifespan_choice">
                            <option v-for="option in interval_choice" :value="option.id" v-bind:key="option.id">
                                {{ option.name }}
                            </option>
                        </select>
                    </div>
            </div>

            <div v-for="species in original_species_combine_list">
                <div class="row mb-3">
                    <label for="" class="col-sm-3 control-label">{{ species.species_number }} Minimum Fire Interval:</label>
                    <div class="col-sm-8">
                        <input class="form-check-input" type="checkbox" :id="'minimum_fire_interval_range_original'+species.id"
                         disabled="true" />
                        <label for="" class="control-label">Range</label>
                    </div>
                    <div class="col-sm-1">
                        <input class="form-check-input" type="checkbox" name="fire_interval_chk" :id="'fire_interval_chk'+species.id"
                        @change="checkConservationInput('fire_interval_chk','fire_interval_chk'+species.id,'minimum_fire_interval', species.conservation_attributes.minimum_fire_interval_from,'',species.conservation_attributes.minimum_fire_interval_to,species.conservation_attributes.minimum_fire_interval_choice)" />
                    </div>
                </div>

                <div class="row mb-3" v-if="!isOriginalRangeChecked('minimum_fire_interval_range_original'+species.id, species.id,'minimum_fire_interval_to')">
                    <label for="" class="col-sm-3 control-label"></label>
                    <div class="col-sm-3 interval-margin">
                        <input disabled="true" type="number" class="form-control"
                        id="minimum_fire_interval_from" placeholder=""
                        v-model="species.conservation_attributes.minimum_fire_interval_from"/>
                    </div>
                    <div class="col-sm-2 interval-range-true-choice">
                        <select disabled="true" class="form-select"
                            v-model="species.conservation_attributes.minimum_fire_interval_choice">
                            <option v-for="option in interval_choice" :value="option.id" v-bind:key="option.id">
                                {{ option.name }}
                            </option>
                        </select>
                    </div>
                    <div class="col-sm-4">
                        <label for="" class="control-label">{{ intervalMonthsComputedOriginal(species.conservation_attributes.minimum_fire_interval_from, species.conservation_attributes.minimum_fire_interval_choice)}}</label>
                    </div>
                </div>
                <div class="row mb-3" v-else>
                        <label for="" class="col-sm-3 control-label"></label>
                        <label for="" class="col-sm-2 control-label">From:</label>
                        <div class="col-sm-2 interval-range-true-input">
                            <input disabled="true" type="number" class="form-control"
                            id="minimum_fire_interval_from" placeholder=""
                            v-model="species.conservation_attributes.minimum_fire_interval_from"/>
                        </div>
                        <label for="" class="col-sm-2 control-label">To:</label>
                        <div class="col-sm-2 interval-range-true-input">
                            <input disabled="true" type="number" class="form-control"
                            id="minimum_fire_interval_to" placeholder=""
                            v-model="species.conservation_attributes.minimum_fire_interval_to"/>
                        </div>
                        <div class="col-sm-2 interval-range-true-choice">
                            <select disabled="true" class="form-select"
                                v-model="species.conservation_attributes.minimum_fire_interval_choice">
                                <option v-for="option in interval_choice" :value="option.id" v-bind:key="option.id">
                                    {{ option.name }}
                                </option>
                            </select>
                        </div>
                </div>
            </div>
            <div class="row mb-3">
                <label for="" class="col-sm-3 control-label">Minimum Fire Interval:</label>
                <div class="col-sm-3">
                    <input class="form-check-input" type="checkbox" id="minimum_fire_interval_range_new"
                        v-model="minimum_fire_interval_range_new" :disabled="isReadOnly" @change="handleMinimumFireIntervalRange()" />
                    <label for="" class="control-label">Range</label>
                </div>
                <label for="" class="col-sm-6 control-label" style="color: red;">{{ errors.minimum_fire_interval_error }}</label>
            </div>
            <div class="row mb-3" v-if="!minimum_fire_interval_range_new">
                <label for="" class="col-sm-3 control-label"></label>
                <div class="col-sm-3 interval-margin">
                    <input :disabled="isReadOnly" type="number" class="form-control"
                    id="minimum_fire_interval_from" placeholder="" @change="validateRange('minimum_fire_interval_from','minimum_fire_interval_to','minimum_fire_interval_choice','minimum_fire_interval_error')"
                    v-model="species_community.conservation_attributes.minimum_fire_interval_from"/>
                </div>
                <div class="col-sm-2 interval-range-true-choice">
                    <select :disabled="isReadOnly" class="form-select" @change="validateRange('minimum_fire_interval_from','minimum_fire_interval_to','minimum_fire_interval_choice','minimum_fire_interval_error')"
                        v-model="species_community.conservation_attributes.minimum_fire_interval_choice">
                        <option v-for="option in interval_choice" :value="option.id" v-bind:key="option.id">
                            {{ option.name }}
                        </option>
                    </select>
                </div>
                <div class="col-sm-4">
                    <label for="" class="control-label">{{ intervalMonthsComputedNew('minimum_fire_interval_from','minimum_fire_interval_choice') }}</label>
                </div>
            </div>
            <div class="row mb-3" v-else>
                    <label for="" class="col-sm-3 control-label"></label>
                    <label for="" class="col-sm-2 control-label">From:</label>
                    <div class="col-sm-2 interval-range-true-input">
                        <input :disabled="isReadOnly" type="number" class="form-control"
                        id="minimum_fire_interval_from" placeholder="" @change="validateRange('minimum_fire_interval_from','minimum_fire_interval_to','minimum_fire_interval_choice','minimum_fire_interval_error')"
                        v-model="species_community.conservation_attributes.minimum_fire_interval_from"/>
                    </div>
                    <label for="" class="col-sm-2 control-label">To:</label>
                    <div class="col-sm-2 interval-range-true-input">
                        <input :disabled="isReadOnly" type="number" class="form-control"
                        id="minimum_fire_interval_to" placeholder="" @change="validateRange('minimum_fire_interval_from','minimum_fire_interval_to','minimum_fire_interval_choice','minimum_fire_interval_error')"
                        v-model="species_community.conservation_attributes.minimum_fire_interval_to"/>
                    </div>
                    <div class="col-sm-2 interval-range-true-choice">
                        <select :disabled="isReadOnly" class="form-select" @change="validateRange('minimum_fire_interval_from','minimum_fire_interval_to','minimum_fire_interval_choice','minimum_fire_interval_error')"
                            v-model="species_community.conservation_attributes.minimum_fire_interval_choice">
                            <option v-for="option in interval_choice" :value="option.id" v-bind:key="option.id">
                                {{ option.name }}
                            </option>
                        </select>
                    </div>
            </div>

            <div>
                <div class="row mb-3" v-for="species in original_species_combine_list">
                    <label for="" class="col-sm-3 control-label">{{ species.species_number }} Response to Fire:</label>
                    <div class="col-sm-8">
                        <textarea :disabled="true" type="text" class="form-control" id="response_to_fire" placeholder="" v-model="species.conservation_attributes.response_to_fire"/>
                    </div>
                    <div class="col-sm-1">
                        <!- - checkInput(checkbox_name,checkbox_id , v-model object attribute of this field) - ->
                        <input class="form-check-input" type="checkbox" name="fire_resp_chk" :id="'fire_resp_chk'+species.id"
                        @change="checkConservationInput('fire_resp_chk','fire_resp_chk'+species.id,'response_to_fire', species.conservation_attributes.response_to_fire)" />
                    </div>
                </div>
            </div>
            <div class="row mb-3">
                <label for="" class="col-sm-3 control-label">Response to Fire:</label>
                <div class="col-sm-8">
                    <textarea :disabled="isReadOnly" type="text" class="form-control" id="response_to_fire" placeholder="" v-model="species_community.conservation_attributes.response_to_fire"/>
                </div>
            </div>

            <div>
                <div class="row mb-3" v-for="species in original_species_combine_list">
                    <label for="" class="col-sm-3 control-label">{{ species.species_number }} Post Fire Habitat Interactions:</label>
                    <div class="col-sm-8">
                        <select :disabled="true" class="form-select"
                            v-model="species.conservation_attributes.post_fire_habitat_interaction_id">
                            <option v-for="option in post_fire_habitatat_interactions_list" :value="option.id" v-bind:key="option.id">
                                {{ option.name }}
                            </option>
                        </select>
                    </div>
                    <div class="col-sm-1">
                        <!- - checkInput(checkbox_name,checkbox_id , v-model object attribute of this field) - ->
                        <input class="form-check-input" type="checkbox" name="fire_habitat_chk" :id="'fire_habitat_chk'+species.id"
                        @change="checkConservationInput('fire_habitat_chk','fire_habitat_chk'+species.id,'post_fire_habitat_interaction_id', species.conservation_attributes.post_fire_habitat_interaction_id)" />
                    </div>
                </div>
            </div>
            <div class="row mb-3">
                <label for="" class="col-sm-3 control-label">Post Fire Habitat Interactions:</label>
                <div class="col-sm-8">
                    <select :disabled="isReadOnly" class="form-select"
                        v-model="species_community.conservation_attributes.post_fire_habitat_interaction_id">
                        <option v-for="option in post_fire_habitatat_interactions_list" :value="option.id" v-bind:key="option.id">
                            {{ option.name }}
                        </option>
                    </select>
                </div>
            </div>

            <div>
                <div class="row mb-3" v-for="species in original_species_combine_list">
                    <label for="" class="col-sm-3 control-label">{{ species.species_number }} Habitat:</label>
                    <div class="col-sm-8">
                        <textarea :disabled="true" type="text" class="form-control" id="habitat"
                        placeholder="" v-model="species.conservation_attributes.habitat"/>
                    </div>
                    <div class="col-sm-1">
                        <!- - checkInput(checkbox_name,checkbox_id , v-model object attribute of this field) - ->
                        <input class="form-check-input" type="checkbox" name="habitat_chk" :id="'habitat_chk'+species.id"
                        @change="checkConservationInput('habitat_chk','habitat_chk'+species.id,'habitat', species.conservation_attributes.habitat)" />
                    </div>
                </div>
            </div>
            <div class="row mb-3">
                <label for="" class="col-sm-3 control-label">Habitat:</label>
                <div class="col-sm-8">
                    <textarea :disabled="isReadOnly" type="text" class="form-control" id="habitat"
                    placeholder="" v-model="species_community.conservation_attributes.habitat"/>
                </div>
            </div>

            <div>
                <div class="row mb-3" v-for="species in original_species_combine_list">
                    <label for="" class="col-sm-3 control-label">{{ species.species_number }} Hydrology:</label>
                    <div class="col-sm-8">
                        <textarea :disabled="true" type="text" class="form-control" id="hydrology"
                        placeholder="" v-model="species.conservation_attributes.hydrology"/>
                    </div>
                    <div class="col-sm-1">
                        <!- - checkInput(checkbox_name,checkbox_id , v-model object attribute of this field) - ->
                        <input class="form-check-input" type="checkbox" name="hydrology_chk" :id="'hydrology_chk'+species.id"
                        @change="checkConservationInput('hydrology_chk','hydrology_chk'+species.id,'hydrology', species.conservation_attributes.hydrology)" />
                    </div>
                </div>
            </div>
            <div class="row mb-3" v-show="!isFauna">
                <label for="" class="col-sm-3 control-label">Hydrology:</label>
                <div class="col-sm-8">
                    <textarea :disabled="isReadOnly" type="text" class="form-control" id="hydrology"
                    placeholder="" v-model="species_community.conservation_attributes.hydrology"/>
                </div>
            </div>

            <div v-show="isFauna">
                <div class="row mb-3" v-for="species in original_species_combine_list">
                    <label for="" class="col-sm-3 control-label">{{ species.species_number }} Diet and Food Source:</label>
                    <div class="col-sm-8">
                        <textarea :disabled="true" type="text" class="form-control" id="diet_food_source"
                        placeholder="" v-model="species.conservation_attributes.diet_and_food_source"/>
                    </div>
                    <div class="col-sm-1">
                        <!- - checkInput(checkbox_name,checkbox_id , v-model object attribute of this field) - ->
                        <input class="form-check-input" type="checkbox" name="diet_src_chk" :id="'diet_src_chk'+species.id"
                        @change="checkConservationInput('diet_src_chk','diet_src_chk'+species.id,'diet_and_food_source', species.conservation_attributes.diet_and_food_source)" />
                    </div>
                </div>
            </div>
            <div class="row mb-3" v-show="isFauna">
                <label for="" class="col-sm-3 control-label">Diet and Food Source:</label>
                <div class="col-sm-8">
                    <textarea :disabled="isReadOnly" type="text" class="form-control" id="diet_food_source"
                    placeholder="" v-model="species_community.conservation_attributes.diet_and_food_source"/>
                </div>
            </div>

            <div v-show="isFauna">
                <div class="row mb-3" v-for="species in original_species_combine_list">
                    <label for="" class="col-sm-3 control-label">{{ species.species_number }} Home Range:</label>
                    <div class="col-sm-8">
                        <textarea :disabled="true" type="text" class="form-control" id="home_range"
                        placeholder="" v-model="species.conservation_attributes.home_range"/>
                    </div>
                    <div class="col-sm-1">
                        <!- - checkInput(checkbox_name,checkbox_id , v-model object attribute of this field) - ->
                        <input class="form-check-input" type="checkbox" name="home_rng_chk" :id="'home_rng_chk'+species.id"
                        @change="checkConservationInput('home_rng_chk','home_rng_chk'+species.id,'home_range', species.conservation_attributes.home_range)" />
                    </div>
                </div>
            </div>
            <div class="row mb-3" v-show="isFauna">
                <label for="" class="col-sm-3 control-label">Home Range:</label>
                <div class="col-sm-8">
                    <textarea :disabled="isReadOnly" type="text" class="form-control" id="home_range"
                    placeholder="" v-model="species_community.conservation_attributes.home_range"/>
                </div>
            </div>

            <div>
                <div class="row mb-3" v-for="species in original_species_combine_list">
                    <label for="" class="col-sm-3 control-label">{{ species.species_number }} Research Requirements:</label>
                    <div class="col-sm-8">
                        <textarea :disabled="true" type="text" class="form-control"
                        id="research_requirements"
                        placeholder="" v-model="species.conservation_attributes.research_requirements"/>
                    </div>
                    <div class="col-sm-1">
                        <!- - checkInput(checkbox_name,checkbox_id , v-model object attribute of this field) - ->
                        <input class="form-check-input" type="checkbox" name="research_req_chk" :id="'research_req_chk'+species.id"
                        @change="checkConservationInput('research_req_chk','research_req_chk'+species.id,'research_requirements', species.conservation_attributes.research_requirements)" />
                    </div>
                </div>
            </div>
            <div class="row mb-3">
                <label for="" class="col-sm-3 control-label">Research Requirements:</label>
                <div class="col-sm-8">
                    <textarea :disabled="isReadOnly" type="text" class="form-control"
                    id="research_requirements"
                    placeholder="" v-model="species_community.conservation_attributes.research_requirements"/>
                </div>
            </div>

            <div v-show="!isFauna">
                <div class="row mb-3" v-for="species in original_species_combine_list">
                    <label for="" class="col-sm-3 control-label">{{ species.species_number }} Response to Dieback:</label>
                    <div class="col-sm-8">
                        <textarea :disabled="true" type="text" class="form-control"
                        id="response_to_dieback"
                        placeholder="" v-model="species.conservation_attributes.response_to_dieback"/>
                    </div>
                    <div class="col-sm-1">
                        <!- - checkInput(checkbox_name,checkbox_id , v-model object attribute of this field) - ->
                        <input class="form-check-input" type="checkbox" name="dieback_resp_chk" :id="'dieback_resp_chk'+species.id"
                        @change="checkConservationInput('dieback_resp_chk','dieback_resp_chk'+species.id,'response_to_dieback', species.conservation_attributes.response_to_dieback)" />
                    </div>
                </div>
            </div>
            <div class="row mb-3" v-show="!isFauna">
                <label for="" class="col-sm-3 control-label">Response to Dieback:</label>
                <div class="col-sm-8">
                    <textarea :disabled="isReadOnly" type="text" class="form-control"
                    id="response_to_dieback"
                    placeholder="" v-model="species_community.conservation_attributes.response_to_dieback"/>
                </div>
            </div>

            <div>
                <div class="row mb-3" v-for="species in original_species_combine_list">
                    <label for="" class="col-sm-3 control-label">{{ species.species_number }} Other relevant diseases:</label>
                    <div class="col-sm-8">
                        <textarea :disabled="true" type="text" class="form-control"
                        id="other_relevant_diseases"
                        placeholder="" v-model="species.conservation_attributes.other_relevant_diseases"/>
                    </div>
                    <div class="col-sm-1">
                        <!- - checkInput(checkbox_name,checkbox_id , v-model object attribute of this field) - ->
                        <input class="form-check-input" type="checkbox" name="disease_chk" :id="'disease_chk'+species.id"
                        @change="checkConservationInput('disease_chk','disease_chk'+species.id,'other_relevant_diseases', species.conservation_attributes.other_relevant_diseases)" />
                    </div>
                </div>
            </div>
            <div class="row mb-3">
                <label for="" class="col-sm-3 control-label">Other relevant diseases:</label>
                <div class="col-sm-8">
                    <textarea :disabled="isReadOnly" type="text" class="form-control"
                    id="other_relevant_diseases"
                    placeholder="" v-model="species_community.conservation_attributes.other_relevant_diseases"/>
                </div>
            </div>

        </FormSection> -->
        <FormSection
            :form-collapse="false"
            label="General"
            :Index="generalBody"
        >
            <div>
                <div
                    v-for="species in original_species_combine_list"
                    :key="species.id"
                    class="row mb-3"
                >
                    <label for="" class="col-sm-3 control-label"
                        >{{ species.species_number }} Department File
                        Numbers:</label
                    >
                    <div class="col-sm-8">
                        <input
                            id="department_file_numbers"
                            v-model="species.department_file_numbers"
                            :disabled="true"
                            type="text"
                            class="form-control"
                            placeholder=""
                        />
                    </div>
                    <div class="col-sm-1">
                        <!-- checkInput(checkbox_name,checkbox_id , v-model object attribute of this field) -->
                        <input
                            :id="'dept_file_chk' + species.id"
                            class="form-check-input"
                            type="checkbox"
                            name="dept_file_chk"
                            @change="
                                checkDistributionInput(
                                    'dept_file_chk',
                                    'dept_file_chk' + species.id,
                                    'department_file_numbers',
                                    species.department_file_numbers
                                )
                            "
                        />
                    </div>
                </div>
            </div>
            <div class="row mb-3">
                <label for="" class="col-sm-3 control-label"
                    >Department File Numbers:</label
                >
                <div class="col-sm-8">
                    <input
                        id="department_file_numbers"
                        v-model="species_community.department_file_numbers"
                        :disabled="isReadOnly"
                        type="text"
                        class="form-control"
                        placeholder=""
                    />
                </div>
            </div>

            <div class="row mb-3">
                <label for="" class="col-sm-3 control-label"
                    >Last data curation date:
                </label>
                <div class="col-sm-8">
                    <input
                        ref="last_data_curation_date"
                        v-model="species_community.last_data_curation_date"
                        :disabled="isReadOnly"
                        type="date"
                        class="form-control"
                        name="last_data_curation_date"
                        min="1990-01-01"
                        :max="new Date().toISOString().split('T')[0]"
                        @change="checkDate()"
                    />
                </div>
            </div>
            <div>
                <div
                    v-for="species in original_species_combine_list"
                    :key="species.id"
                    class="row mb-3"
                >
                    <label for="" class="col-sm-3 control-label"
                        >{{ species.species_number }} Comment:</label
                    >
                    <div class="col-sm-8">
                        <textarea
                            id="comment"
                            v-model="species.comment"
                            :disabled="true"
                            class="form-control"
                            rows="3"
                            placeholder=""
                        />
                    </div>
                    <div class="col-sm-1">
                        <!-- checkInput(checkbox_name,checkbox_id , v-model object attribute of this field, value) -->
                        <input
                            :id="'comment_chk' + species.id"
                            class="form-check-input"
                            type="checkbox"
                            name="comment_chk"
                            @change="
                                checkCommentInput(
                                    'comment_chk',
                                    'comment_chk' + species.id,
                                    'comment',
                                    species.comment
                                )
                            "
                        />
                    </div>
                </div>
            </div>
            <div class="row mb-3">
                <label for="" class="col-sm-3 control-label">Comment:</label>
                <div class="col-sm-8">
                    <textarea
                        id="comment"
                        v-model="species_community.comment"
                        :disabled="isReadOnly"
                        class="form-control"
                        rows="3"
                        placeholder=""
                    />
                </div>
            </div>
        </FormSection>
    </div>
</template>

<script>
import { v4 as uuid } from 'uuid';
import FormSection from '@/components/forms/section_toggle.vue';
import { api_endpoints } from '@/utils/hooks';
export default {
    name: 'SpeciesCombineProfile',
    components: {
        FormSection,
    },
    props: {
        species_community: {
            type: Object,
            required: true,
        },
        original_species_combine_list: {
            type: Array,
            required: true,
        },
    },
    data: function () {
        let vm = this;
        return {
            scientific_name_lookup:
                'scientific_name_lookup' + vm.species_community.id,
            select_scientific_name:
                'select_scientific_name' + vm.species_community.id,
            select_flowering_period:
                'select_flowering_period' + vm.species_community.id,
            select_flowering_period_readonly:
                'select_flowering_period_readonly' + vm.species_community.id,
            select_fruiting_period:
                'select_fruiting_period' + vm.species_community.id,
            select_fruiting_period_readonly:
                'select_fruiting_period_readonly' + vm.species_community.id,
            select_breeding_period:
                'select_breeding_period' + vm.species_community.id,
            select_breeding_period_readonly:
                'select_breeding_period_readonly' + vm.species_community.id,
            select_regions: 'select_regions' + vm.species_community.id,
            select_districts: 'select_districts' + vm.species_community.id,
            taxonBody: 'taxonBody' + uuid(),
            distributionBody: 'distributionBody' + uuid(),
            conservationBody: 'conservationBody' + uuid(),
            generalBody: 'generalBody' + uuid(),
            //---to show fields related to Fauna
            isFauna: vm.species_community.group_type === 'fauna' ? true : false,
            //----list of values dictionary
            species_profile_dict: {},
            //scientific_name_list: [],
            region_list: [],
            district_list: [],
            filtered_district_list: [],
            //---conservatiuon attributes field lists
            flora_recruitment_type_list: [],
            root_morphology_list: [],
            post_fire_habitatat_interactions_list: [],
            // to display the species Taxonomy selected details
            species_display: '',
            common_name: null,
            taxon_name_id: null,
            taxon_previous_name: null,
            phylogenetic_group: null,
            family: null,
            genus: null,
            name_authority: null,
            name_comments: null,
            period_list: [
                { id: 1, name: 'January' },
                { id: 2, name: 'February' },
                { id: 3, name: 'March' },
                { id: 4, name: 'April' },
                { id: 5, name: 'May' },
                { id: 6, name: 'June' },
                { id: 7, name: 'July' },
                { id: 8, name: 'August' },
                { id: 9, name: 'September' },
                { id: 10, name: 'October' },
                { id: 11, name: 'November' },
                { id: 12, name: 'December' },
            ],
            minimum_fire_interval_range_new: false,
            average_lifespan_range_new: false,
            generation_length_range_new: false,
            time_to_maturity_range_new: false,
            interval_choice: [
                { id: 1, name: 'year/s' },
                { id: 2, name: 'month/s' },
            ],
            errors: {
                minimum_fire_interval_error: null,
                average_lifespan_error: null,
                generation_length_error: null,
                time_to_maturity_error: null,
            },
        };
    },
    computed: {
        isReadOnly: function () {
            let action = this.$route.query.action;
            if (
                action === 'edit' &&
                this.species_community &&
                this.species_community.user_edit_mode
            ) {
                return false;
            } else {
                return this.species_community.readonly;
            }
        },
    },
    watch: {
        'species_community.distribution.noo_auto': function (newVal) {
            let vm = this;
            var selectedValue = newVal;
            if (selectedValue === 'true') {
                vm.species_community.distribution.number_of_occurrences =
                    vm.species_community.distribution.cal_number_of_occurrences;
            } else {
                vm.species_community.distribution.number_of_occurrences = null;
            }
        },
        'species_community.distribution.eoo_auto': function (newVal) {
            let vm = this;
            var selectedValue = newVal;
            if (selectedValue === 'true') {
                vm.species_community.distribution.extent_of_occurrences =
                    vm.species_community.distribution.cal_extent_of_occurrences;
            } else {
                vm.species_community.distribution.extent_of_occurrences = null;
            }
        },
        'species_community.distribution.aoo_actual_auto': function (newVal) {
            let vm = this;
            var selectedValue = newVal;
            if (selectedValue === 'true') {
                vm.species_community.distribution.area_of_occupancy_actual =
                    vm.species_community.distribution.cal_area_of_occupancy_actual;
            } else {
                vm.species_community.distribution.area_of_occupancy_actual =
                    null;
            }
        },
    },
    created: async function () {
        let vm = this;
        //----set the distribution field values if auto onload
        if (vm.species_community.distribution.noo_auto == true) {
            vm.species_community.distribution.number_of_occurrences =
                vm.species_community.distribution.cal_number_of_occurrences;
        }
        if (vm.species_community.distribution.eoo_auto == true) {
            vm.species_community.distribution.extent_of_occurrences =
                vm.species_community.distribution.cal_extent_of_occurrences;
        }
        if (vm.species_community.distribution.aoo_actual_auto == true) {
            vm.species_community.distribution.area_of_occupancy_actual =
                vm.species_community.distribution.cal_area_of_occupancy_actual;
        }
        if (
            vm.species_community.conservation_attributes
                .minimum_fire_interval_to != null &&
            vm.species_community.conservation_attributes
                .minimum_fire_interval_to != '' &&
            vm.species_community.conservation_attributes
                .minimum_fire_interval_to != undefined
        ) {
            vm.minimum_fire_interval_range_new = true;
        }
        if (
            vm.species_community.conservation_attributes.average_lifespan_to !=
                null &&
            vm.species_community.conservation_attributes.average_lifespan_to !=
                '' &&
            vm.species_community.conservation_attributes.average_lifespan_to !=
                undefined
        ) {
            vm.average_lifespan_range_new = true;
        }
        if (
            vm.species_community.conservation_attributes.generation_length_to !=
                null &&
            vm.species_community.conservation_attributes.generation_length_to !=
                '' &&
            vm.species_community.conservation_attributes.generation_length_to !=
                undefined
        ) {
            vm.generation_length_range_new = true;
        }
        if (
            vm.species_community.conservation_attributes.time_to_maturity_to !=
                null &&
            vm.species_community.conservation_attributes.time_to_maturity_to !=
                '' &&
            vm.species_community.conservation_attributes.time_to_maturity_to !=
                undefined
        ) {
            vm.time_to_maturity_range_new = true;
        }
        //------fetch list of values
        const response = await fetch('/api/species_profile_dict/');
        vm.species_profile_dict = await response.json();
        vm.flora_recruitment_type_list =
            vm.species_profile_dict.flora_recruitment_type_list;
        vm.flora_recruitment_type_list.splice(0, 0, {
            id: null,
            name: null,
        });
        vm.root_morphology_list = vm.species_profile_dict.root_morphology_list;
        vm.root_morphology_list.splice(0, 0, {
            id: null,
            name: null,
        });
        vm.post_fire_habitatat_interactions_list =
            vm.species_profile_dict.post_fire_habitatat_interactions_list;
        vm.post_fire_habitatat_interactions_list.splice(0, 0, {
            id: null,
            name: null,
        });
        vm.fetchRegions();
    },
    mounted: function () {
        let vm = this;
        vm.eventListeners();
        vm.initialiseScientificNameLookup();
        vm.loadTaxonomydetails();
        vm.initialiseRegionSelect();
        vm.initialiseDistrictSelect();
    },
    methods: {
        filterDistrict: function (event) {
            this.$nextTick(() => {
                if (event) {
                    this.species_community.district_id = null; //-----to remove the previous selection
                }
                this.filtered_district_list = [];
                this.filtered_district_list = [
                    {
                        id: null,
                        name: '',
                        region_id: null,
                    },
                ];
                //---filter districts as per region selected
                for (let choice of this.district_list) {
                    if (choice.region_id === this.species_community.region_id) {
                        this.filtered_district_list.push(choice);
                    }
                }
            });
        },
        checkDate: function () {
            if (this.species_community.last_data_curation_date === '') {
                this.species_community.last_data_curation_date = null;
                return;
            }
            if (
                isNaN(new Date(this.species_community.last_data_curation_date))
            ) {
                return;
            }
            if (
                new Date(this.species_community.last_data_curation_date) >
                new Date()
            ) {
                this.species_community.last_data_curation_date = new Date()
                    .toISOString()
                    .split('T')[0];
                this.$nextTick(() => {
                    this.$refs.last_data_curation_date.focus();
                });
                swal.fire({
                    title: 'Error',
                    text: 'Last data curation date cannot be in the future',
                    icon: 'error',
                    customClass: {
                        confirmButton: 'btn btn-primary',
                    },
                });
            }
            if (
                new Date(this.species_community.last_data_curation_date) <
                new Date('1990-01-01')
            ) {
                this.species_community.last_data_curation_date = new Date(
                    '1990-01-01'
                )
                    .toISOString()
                    .split('T')[0];
                this.$nextTick(() => {
                    this.$refs.last_data_curation_date.focus();
                });
                swal.fire({
                    title: 'Error',
                    text: 'Last data curation date cannot be before 01/01/1990',
                    icon: 'error',
                    customClass: {
                        confirmButton: 'btn btn-primary',
                    },
                });
            }
        },
        initialiseScientificNameLookup: function () {
            let vm = this;
            $(vm.$refs[vm.scientific_name_lookup])
                .select2({
                    minimumInputLength: 2,
                    dropdownParent: $('#' + vm.select_scientific_name),
                    theme: 'bootstrap-5',
                    allowClear: true,
                    placeholder: 'Select Scientific Name',
                    ajax: {
                        url: api_endpoints.scientific_name_lookup,
                        dataType: 'json',
                        data: function (params) {
                            var query = {
                                term: params.term,
                                type: 'public',
                                group_type_id:
                                    vm.species_community.group_type_id,
                                species_profile: true, // This parameter makes sure the query only returns records that don't yet have a species profile
                            };
                            return query;
                        },
                    },
                })
                .on('select2:select', function (e) {
                    let data = e.params.data.id;
                    vm.species_community.taxonomy_id = data;
                    vm.species_community.taxonomy_details = e.params.data;
                    vm.species_display = e.params.data.scientific_name;
                    vm.common_name = e.params.data.common_name;
                    vm.taxon_name_id = e.params.data.taxon_name_id;
                    vm.taxon_previous_name = e.params.data.taxon_previous_name;
                    vm.phylogenetic_group = e.params.data.phylogenetic_group;
                    vm.family = e.params.data.family_name;
                    vm.genus = e.params.data.genera_name;
                    vm.name_authority = e.params.data.name_authority;
                    vm.name_comments = e.params.data.name_comments;
                })
                .on('select2:unselect', function () {
                    vm.species_community.taxonomy_id = '';
                    vm.species_display = '';
                    vm.common_name = '';
                    vm.taxon_name_id = '';
                    vm.taxon_previous_name = '';
                    vm.phylogenetic_group = '';
                    (vm.family = ''), (vm.genus = ''), (vm.name_authority = '');
                    vm.name_comments = '';
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
        loadTaxonomydetails: function () {
            let vm = this;
            if (vm.species_community.taxonomy_details != null) {
                vm.species_display =
                    vm.species_community.taxonomy_details.scientific_name;
                vm.common_name =
                    vm.species_community.taxonomy_details.common_name;
                vm.taxon_name_id =
                    vm.species_community.taxonomy_details.taxon_name_id;
                vm.taxon_previous_name =
                    vm.species_community.taxonomy_details.taxon_previous_name;
                vm.phylogenetic_group =
                    vm.species_community.taxonomy_details.phylogenetic_group;
                vm.family = vm.species_community.taxonomy_details.family_name;
                vm.genus = vm.species_community.taxonomy_details.genera_name;
                vm.name_authority =
                    vm.species_community.taxonomy_details.name_authority;
                vm.name_comments =
                    vm.species_community.taxonomy_details.name_comments;
            }
        },
        //--------on/off checkbox value to new species--------
        checkHabitatForm: function () {
            if (
                $('#habitat_frm_chk' + this.species_community.id).is(
                    ':checked'
                ) == true
            ) {
                this.species_community.conservation_attributes.habitat_growth_form =
                    this.species_original.conservation_attributes.habitat_growth_form;
            } else {
                this.species_community.conservation_attributes.habitat_growth_form =
                    null;
            }
        },
        checkConservationInput: function (
            chkbox_name,
            chkbox_id,
            obj_field,
            value,
            select2_ref = '',
            valueTo = null,
            valueChoice = null
        ) {
            const interval_fields = [
                'minimum_fire_interval',
                'average_lifespan',
                'generation_length',
                'time_to_maturity',
            ];
            // if checkbox is checked copy value from original  species to new species
            if ($('#' + chkbox_id).is(':checked') == true) {
                if (interval_fields.includes(obj_field)) {
                    this.species_community.conservation_attributes[
                        obj_field + '_from'
                    ] = value;
                    this.species_community.conservation_attributes[
                        obj_field + '_to'
                    ] = valueTo;
                    this.species_community.conservation_attributes[
                        obj_field + '_choice'
                    ] = valueChoice;
                    if (
                        this.species_community.conservation_attributes[
                            obj_field + '_to'
                        ] != null
                    ) {
                        this[obj_field + '_range_new'] = true;
                    } else {
                        this[obj_field + '_range_new'] = false;
                    }
                } else {
                    this.species_community.conservation_attributes[obj_field] =
                        value;
                    if (select2_ref != '') {
                        $(this.$refs[select2_ref]).val(value).trigger('change');
                    }
                }
            } else {
                if (interval_fields.includes(obj_field)) {
                    this.species_community.conservation_attributes[
                        obj_field + '_from'
                    ] = null;
                    this.species_community.conservation_attributes[
                        obj_field + '_to'
                    ] = null;
                    this.species_community.conservation_attributes[
                        obj_field + '_choice'
                    ] = null;
                    this[obj_field + '_range_new'] = false;
                } else {
                    this.species_community.conservation_attributes[obj_field] =
                        null;
                    if (select2_ref != '') {
                        $(this.$refs[select2_ref]).val('').trigger('change');
                        this.species_community.conservation_attributes[
                            obj_field
                        ] = [];
                    }
                }
            }
            //--- to select only one checkbox at a time in a group
            let chkbox_name_arr = document.getElementsByName(chkbox_name);
            for (var i = 0; i < chkbox_name_arr.length; i++) {
                if (chkbox_name_arr[i].id != chkbox_id) {
                    chkbox_name_arr[i].checked = false;
                }
            }
        },
        checkDistributionInput: function (
            chkbox_name,
            chkbox_id,
            obj_field,
            value
        ) {
            // if checkbox is checked copy value from original  species to new species
            if ($('#' + chkbox_id).is(':checked') == true) {
                this.species_community.distribution[obj_field] = value;
            } else {
                this.species_community.distribution[obj_field] = null;
            }
            //--- to select only one checkbox at a time in a group
            let chkbox_name_arr = document.getElementsByName(chkbox_name);
            for (var i = 0; i < chkbox_name_arr.length; i++) {
                if (chkbox_name_arr[i].id != chkbox_id) {
                    chkbox_name_arr[i].checked = false;
                }
            }
        },
        checkCommentInput: function (chkbox_name, chkbox_id, obj_field, value) {
            // if checkbox is checked copy value from original  species to new species
            if ($('#' + chkbox_id).is(':checked') == true) {
                this.species_community[obj_field] = value;
            } else {
                this.species_community[obj_field] = null;
            }
            //--- to select only one checkbox at a time in a group
            let chkbox_name_arr = document.getElementsByName(chkbox_name);
            for (var i = 0; i < chkbox_name_arr.length; i++) {
                if (chkbox_name_arr[i].id != chkbox_id) {
                    chkbox_name_arr[i].checked = false;
                }
            }
        },
        //----------------------------------------------------------------
        eventListeners: function () {
            let vm = this;
            $(vm.$refs.flowering_period_select)
                .select2({
                    dropdownParent: $('#' + vm.select_flowering_period),
                    theme: 'bootstrap-5',
                    allowClear: true,
                    placeholder: 'Select Flowering Period',
                    multiple: true,
                })
                .on('select2:select', function (e) {
                    var selected = $(e.currentTarget);
                    vm.species_community.conservation_attributes.flowering_period =
                        selected.val();
                })
                .on('select2:unselect', function (e) {
                    var selected = $(e.currentTarget);
                    vm.species_community.conservation_attributes.flowering_period =
                        selected.val();
                });
            $(vm.$refs.flowering_period_select_readonly).select2({
                dropdownParent: $('#' + vm.select_flowering_period_readonly),
                theme: 'bootstrap-5',
                allowClear: true,
                placeholder: 'Select Flowering Period',
                multiple: true,
            });
            $(vm.$refs.fruiting_period_select)
                .select2({
                    dropdownParent: $('#' + vm.select_fruiting_period),
                    theme: 'bootstrap-5',
                    allowClear: true,
                    placeholder: 'Select Fruiting Period',
                    multiple: true,
                })
                .on('select2:select', function (e) {
                    var selected = $(e.currentTarget);
                    vm.species_community.conservation_attributes.fruiting_period =
                        selected.val();
                })
                .on('select2:unselect', function (e) {
                    var selected = $(e.currentTarget);
                    vm.species_community.conservation_attributes.fruiting_period =
                        selected.val();
                });
            $(vm.$refs.fruiting_period_select_readonly).select2({
                dropdownParent: $('#' + vm.select_fruiting_period_readonly),
                theme: 'bootstrap-5',
                allowClear: true,
                placeholder: 'Select Fruiting Period',
                multiple: true,
            });
            $(vm.$refs.breeding_period_select)
                .select2({
                    dropdownParent: $('#' + vm.select_breeding_period),
                    theme: 'bootstrap-5',
                    allowClear: true,
                    placeholder: 'Select Breeding Period',
                    multiple: true,
                })
                .on('select2:select', function (e) {
                    var selected = $(e.currentTarget);
                    vm.species_community.conservation_attributes.breeding_period =
                        selected.val();
                })
                .on('select2:unselect', function (e) {
                    var selected = $(e.currentTarget);
                    vm.species_community.conservation_attributes.breeding_period =
                        selected.val();
                });
            $(vm.$refs.breeding_period_select_readonly).select2({
                dropdownParent: $('#' + vm.select_breeding_period_readonly),
                theme: 'bootstrap-5',
                allowClear: true,
                placeholder: 'Select Breeding Period',
                multiple: true,
            });
        },
        intervalMonthsComputedOriginal: function (months, intervalChoice) {
            const totalMonths = parseInt(months);
            if (totalMonths > 12 && intervalChoice == 2) {
                const years = Math.floor(totalMonths / 12);
                const months = totalMonths % 12;
                return years + ' year/s ' + months + ' month/s';
            } else {
                return '';
            }
        },
        intervalMonthsComputedNew: function (field_from, field_choice) {
            const totalMonths = parseInt(
                this.species_community.conservation_attributes[field_from]
            );
            const intervalChoice =
                this.species_community.conservation_attributes[field_choice];
            // const isIntervalRange = this.minimum_fire_interval_range_new;

            // if(totalMonths > 12 && intervalChoice == 2 && isIntervalRange == false){
            if (totalMonths > 12 && intervalChoice == 2) {
                const years = Math.floor(totalMonths / 12);
                const months = totalMonths % 12;
                return years + ' year/s ' + months + ' month/s';
            } else {
                return '';
            }
        },
        handleMinimumFireIntervalRange: function () {
            if (this.minimum_fire_interval_range_new == false) {
                this.species_community.conservation_attributes.minimum_fire_interval_to =
                    null;
            }
        },
        handleAverageLifespanRange: function () {
            if (this.average_lifespan_range_new == false) {
                this.species_community.conservation_attributes.average_lifespan_to =
                    null;
            }
        },
        handleGenerationLengthRange: function () {
            if (this.generation_length_range_new == false) {
                this.species_community.conservation_attributes.generation_length_to =
                    null;
            }
        },
        handleTimeToMaturityRange: function () {
            if (this.time_to_maturity_range_new == false) {
                this.species_community.conservation_attributes.time_to_maturity_to =
                    null;
            }
        },
        validateRange: function (
            field_from,
            field_to,
            field_choice,
            field_error
        ) {
            const rangeFrom = parseInt(
                this.species_community.conservation_attributes[field_from]
            );
            const rangeTo = parseInt(
                this.species_community.conservation_attributes[field_to]
            );
            const intervalChoice =
                this.species_community.conservation_attributes[field_choice];
            if (
                (rangeFrom != null || rangeTo != null) &&
                intervalChoice == null
            ) {
                this.errors[field_error] = 'Please select years/months';
            } else if (rangeFrom >= rangeTo) {
                this.errors[field_error] = 'Please enter a valid range';
            } else {
                this.errors[field_error] = '';
            }
        },
        isOriginalRangeChecked: function (fullId, id, field) {
            const species_obj = this.original_species_combine_list.find(
                (i) => i.id === id
            );
            const valueTo = species_obj.conservation_attributes[field];
            if (valueTo != null && valueTo != '' && valueTo != undefined) {
                $('#' + fullId).prop('checked', true);
                return true;
            } else {
                $('#' + fullId).prop('checked', false);
                return false;
            }
        },
        getselectedRegionNames(species) {
            // Filter regions_list to get only the selected regions
            let selected_region = species.regions;
            const selectedRegions = this.region_list.filter((region) =>
                selected_region.includes(region.value)
            );
            // Map the selected regions to their names and join them with commas
            return selectedRegions.map((region) => region.text).join(', ');
        },
        getselectedDistrictNames(species) {
            // Initialize an empty array to store the names of selected districts
            let selectedNames = [];
            // Iterate over each region
            this.region_list.forEach((region) => {
                // Filter the districts of the current region
                region.districts.forEach((district) => {
                    if (species.districts.includes(district.id)) {
                        selectedNames.push(district.name);
                    }
                });
            });
            // Join the names with commas
            return selectedNames.join(', ');
        },
        checkRegionDistrictInput: function (
            chkbox,
            obj_field,
            species,
            select2_ref = ''
        ) {
            // if checkbox is checked copy value from original  species to new species
            if ($('#' + chkbox).is(':checked') == true) {
                this.species_community[obj_field] = species[obj_field];
                if (select2_ref != '') {
                    $(this.$refs[select2_ref])
                        .val(this.species_community[obj_field])
                        .trigger('change');
                    this.chainedSelectDistricts(
                        this.species_community.regions,
                        'select'
                    );
                    this.species_community[obj_field] = species[obj_field];
                }
            } else {
                if (select2_ref != '') {
                    $(this.$refs[select2_ref]).val('').trigger('change');
                    this.chainedSelectDistricts(
                        this.species_community.regions,
                        'deselect'
                    );
                }
                this.species_community[obj_field] = [];
            }
        },
        fetchRegions: function () {
            let vm = this;

            fetch(api_endpoints.regions).then(
                async (response) => {
                    vm.api_regions = await response.json();
                    for (var i = 0; i < vm.api_regions.length; i++) {
                        this.region_list.push({
                            text: vm.api_regions[i].name,
                            value: vm.api_regions[i].id,
                            districts: vm.api_regions[i].districts,
                        });
                    }
                    // vm.setProposalData2(this.regions);
                    if (vm.species_community.regions) {
                        vm.chainedSelectDistricts(
                            vm.species_community.regions,
                            'fetch'
                        );
                    }
                },
                (error) => {
                    console.log(error);
                }
            );
        },
        searchList: function (id, search_list) {
            /* Searches for dictionary in list */
            for (var i = 0; i < search_list.length; i++) {
                if (search_list[i].value == id) {
                    return search_list[i];
                }
            }
            return [];
        },
        chainedSelectDistricts: function (regions, action) {
            let vm = this;
            if (action != 'fetch') {
                vm.species_community.districts = []; //-----to remove the previous selection
            }
            vm.district_list = [];
            if (regions) {
                for (let r of regions) {
                    var api_districts = this.searchList(
                        r,
                        vm.region_list
                    ).districts;
                    if (api_districts.length > 0) {
                        for (var i = 0; i < api_districts.length; i++) {
                            this.district_list.push({
                                text: api_districts[i].name,
                                value: api_districts[i].id,
                            });
                        }
                    }
                }
            }
        },
        initialiseRegionSelect: function () {
            let vm = this;
            $(vm.$refs.regions_select)
                .select2({
                    theme: 'bootstrap-5',
                    allowClear: true,
                    multiple: true,
                    dropdownParent: $('#' + vm.select_regions),
                    placeholder: 'Select Region',
                })
                .on('select2:select', function (e) {
                    var selected = $(e.currentTarget);
                    vm.species_community.regions = selected.val();
                    vm.chainedSelectDistricts(
                        vm.species_community.regions,
                        'select'
                    );
                })
                .on('select2:unselect', function (e) {
                    var selected = $(e.currentTarget);
                    vm.species_community.regions = selected.val();
                    vm.chainedSelectDistricts(
                        vm.species_community.regions,
                        'deselect'
                    );
                });
        },
        initialiseDistrictSelect: function () {
            let vm = this;
            $(vm.$refs.districts_select)
                .select2({
                    theme: 'bootstrap-5',
                    allowClear: true,
                    dropdownParent: $('#' + vm.select_districts),
                    multiple: true,
                    placeholder: 'Select District',
                })
                .on('select2:select', function (e) {
                    var selected = $(e.currentTarget);
                    vm.species_community.districts = selected.val();
                })
                .on('select2:unselect', function (e) {
                    var selected = $(e.currentTarget);
                    vm.species_community.districts = selected.val();
                });
        },
    },
};
</script>

<style lang="css" scoped>
fieldset.scheduler-border {
    border: 1px groove #ddd !important;
    padding: 0 1.4em 1.4em 1.4em !important;
    margin: 0 0 1.5em 0 !important;
    -webkit-box-shadow: 0px 0px 0px 0px #000;
    box-shadow: 0px 0px 0px 0px #000;
}

legend.scheduler-border {
    width: inherit;
    /* Or auto */
    padding: 0 10px;
    /* To give a bit of padding on the left and right */
    border-bottom: none;
}

input[type='text'],
select {
    width: 100%;
}

input[type='number'] {
    width: 50%;
}

.interval-margin {
    margin-right: -100px;
}

.interval-range-true-input {
    width: 20%;
    margin-left: -80px;
}

.interval-range-true-choice {
    width: 20%;
}
</style>
