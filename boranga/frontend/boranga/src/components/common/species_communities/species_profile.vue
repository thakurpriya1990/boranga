<template lang="html">
    <div id="species">
        <fieldset id="species-profile-fieldset" @change="saveSpeciesCommunity">
            <FormSection
                :form-collapse="false"
                label="Taxonomy"
                :Index="taxonBody"
            >
                <div class="row mb-3">
                    <label
                        for=""
                        class="col-sm-3 col-form-label"
                        :class="!scientificNameIsReadOnly ? 'fw-bold' : ''"
                        >Scientific Name:
                        <span
                            v-if="!scientificNameIsReadOnly"
                            class="text-danger"
                            >*</span
                        ></label
                    >
                    <div :id="select_scientific_name" class="col-sm-9">
                        <select
                            v-if="!scientificNameIsReadOnly"
                            :id="scientific_name_lookup"
                            :ref="scientific_name_lookup"
                            :name="scientific_name_lookup"
                            class="form-select"
                        />
                        <input
                            v-else
                            id="taxon_name_id"
                            v-model="
                                species_community.taxonomy_details
                                    .scientific_name
                            "
                            :disabled="true"
                            type="text"
                            class="form-control"
                            placeholder=""
                        />
                    </div>
                </div>
                <div
                    v-if="species_community.scientific_name != species_display"
                    class="row mb-3"
                >
                    <label for="" class="col-sm-3 col-form-label"></label>
                    <div class="col-sm-9">
                        <textarea
                            id="species_display"
                            v-model="species_display"
                            disabled
                            class="form-control"
                            rows="2"
                        />
                    </div>
                </div>
                <div v-if="showField(common_name)" class="row mb-3">
                    <label for="" class="col-sm-3 col-form-label"
                        >Common Name:</label
                    >
                    <div class="col-sm-9">
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
                    <label for="" class="col-sm-3 col-form-label"
                        >Taxon Name ID:</label
                    >
                    <div class="col-sm-9">
                        <input
                            id="taxon_name_id"
                            v-model="taxon_name_id"
                            :disabled="true"
                            type="text"
                            class="form-control"
                            placeholder=""
                        />
                    </div>
                </div>
                <div v-if="showField(taxon_previous_name)" class="row mb-3">
                    <label for="" class="col-sm-3 col-form-label"
                        >Previous Name:</label
                    >
                    <div class="col-sm-9">
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
                <div v-if="showField(phylogenetic_group)" class="row mb-3">
                    <label for="" class="col-sm-3 col-form-label"
                        >Phylogenetic Group:</label
                    >
                    <div class="col-sm-9">
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
                <div v-if="showField(family)" class="row mb-3">
                    <label for="" class="col-sm-3 col-form-label"
                        >Family:</label
                    >
                    <div class="col-sm-9">
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
                <div v-if="showField(genus)" class="row mb-3">
                    <label for="" class="col-sm-3 col-form-label">Genus:</label>
                    <div class="col-sm-9">
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
                <div v-if="showField(name_authority)" class="row mb-3">
                    <label for="" class="col-sm-3 col-form-label"
                        >Name Authority:</label
                    >
                    <div class="col-sm-9">
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
                <div v-if="showField(name_comments)" class="row mb-3">
                    <label for="" class="col-sm-3 col-form-label"
                        >NOMOS names comments:</label
                    >
                    <div class="col-sm-9">
                        <textarea
                            id="name_comments"
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
                v-if="distribution_public || is_internal"
                :form-collapse="false"
                label="Distribution"
                :Index="distributionBody"
            >
                <div class="row mb-3">
                    <label
                        for=""
                        class="col-sm-3 col-form-label"
                        :class="isReadOnly ? '' : 'fw-bold'"
                        >Distribution:
                        <span v-if="!isReadOnly" class="text-danger"
                            >*</span
                        ></label
                    >
                    <div class="col-sm-9">
                        <textarea
                            id="distribution"
                            v-model="
                                species_community.distribution.distribution
                            "
                            :disabled="isReadOnly"
                            class="form-control"
                            rows="1"
                            placeholder=""
                        />
                    </div>
                </div>
                <div class="row mb-3">
                    <label
                        for=""
                        class="col-sm-3 col-form-label"
                        :class="isReadOnly ? '' : 'fw-bold'"
                        >Region:
                        <span v-if="!isReadOnly" class="text-danger"
                            >*</span
                        ></label
                    >
                    <div class="col-sm-9">
                        <select
                            ref="regions_select"
                            v-model="species_community.regions"
                            :disabled="isReadOnly"
                            class="form-select"
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
                <div v-if="species_community.regions" class="row mb-3">
                    <label
                        for=""
                        class="col-sm-3 col-form-label"
                        :class="isReadOnly ? '' : 'fw-bold'"
                        >District:
                        <span v-if="!isReadOnly" class="text-danger"
                            >*</span
                        ></label
                    >
                    <div class="col-sm-9">
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
                <template v-if="show_calculated_distribution_fields">
                    <div class="row mb-3 pt-3">
                        <label for="" class="col-sm-4 col-form-label"
                            >Number of Occurrences:</label
                        >
                        <div
                            v-if="
                                showField(
                                    species_community.distribution
                                        .number_of_occurrences
                                )
                            "
                            class="col-sm-4"
                        >
                            <input
                                v-if="species_community.distribution.noo_auto"
                                id="no_of_occurrences"
                                v-model="species_community.occurrence_count"
                                :disabled="isNOOReadOnly"
                                type="number"
                                class="form-control"
                                placeholder=""
                            />
                            <input
                                v-else
                                id="no_of_occurrences"
                                ref="number_of_occurrences"
                                v-model="
                                    species_community.distribution
                                        .number_of_occurrences
                                "
                                :disabled="isNOOReadOnly"
                                type="number"
                                class="form-control"
                                placeholder=""
                            />
                        </div>
                        <div
                            v-if="!isReadOnly"
                            class="col-sm-3 d-flex align-items-center"
                        >
                            <div class="form-check form-check-inline">
                                <input
                                    id="noo_auto"
                                    v-model="
                                        species_community.distribution.noo_auto
                                    "
                                    :disabled="isReadOnly"
                                    type="radio"
                                    :value="true"
                                    class="form-check-input"
                                    @click="switchNOO('true')"
                                />
                                <label class="form-check-label">auto</label>
                            </div>
                            <div class="form-check form-check-inline">
                                <input
                                    id="noo_manual"
                                    v-model="
                                        species_community.distribution.noo_auto
                                    "
                                    :disabled="isReadOnly"
                                    type="radio"
                                    :value="false"
                                    class="form-check-input"
                                    @click="switchNOO('false')"
                                />
                                <label class="form-check-label">manual</label>
                            </div>
                        </div>
                    </div>
                    <div class="row mb-3">
                        <label for="" class="col-sm-4 col-form-label"
                            >Extent of Occurrences:
                            <HelpText
                                v-if="species_community.distribution.eoo_auto"
                                section_id="species_extent_of_occurrences"
                        /></label>
                        <div class="col-sm-4">
                            <div class="input-group">
                                <input
                                    v-if="
                                        species_community.distribution.eoo_auto
                                    "
                                    id="extent_of_occurrence"
                                    v-model="
                                        species_community.area_occurrence_convex_hull_km2
                                    "
                                    :disabled="isEOOReadOnly"
                                    type="number"
                                    class="form-control"
                                    placeholder=""
                                />
                                <input
                                    v-else
                                    id="extent_of_occurrence"
                                    ref="extent_of_occurrence"
                                    v-model="
                                        species_community.distribution
                                            .extent_of_occurrences
                                    "
                                    :disabled="isEOOReadOnly"
                                    type="number"
                                    class="form-control"
                                    placeholder=""
                                />
                                <span
                                    id="area_of_occupancy_km2-addon"
                                    class="input-group-text"
                                    >km&#xb2;</span
                                >
                            </div>
                        </div>
                        <div
                            v-if="!isReadOnly"
                            class="col-sm-3 d-flex align-items-center"
                        >
                            <div class="form-check form-check-inline">
                                <input
                                    id="eoo_auto"
                                    v-model="
                                        species_community.distribution.eoo_auto
                                    "
                                    :disabled="isReadOnly"
                                    type="radio"
                                    :value="true"
                                    class="form-check-input"
                                    @click="switchEOO('true')"
                                />
                                <label class="form-check-label">auto</label>
                            </div>
                            <div class="form-check form-check-inline">
                                <input
                                    id="eoo_manual"
                                    v-model="
                                        species_community.distribution.eoo_auto
                                    "
                                    :disabled="isReadOnly"
                                    type="radio"
                                    :value="false"
                                    class="form-check-input"
                                    @click="switchEOO('false')"
                                />
                                <label class="form-check-label">manual</label>
                            </div>
                        </div>
                    </div>
                    <div class="row mb-3">
                        <label for="" class="col-sm-4 col-form-label"
                            >Area of Occupancy:</label
                        >
                        <div class="col-sm-4">
                            <div class="input-group">
                                <input
                                    id="area_of_occupany"
                                    v-model="
                                        species_community.distribution
                                            .area_of_occupancy
                                    "
                                    :disabled="isReadOnly"
                                    type="number"
                                    class="form-control"
                                    placeholder=""
                                />
                                <span
                                    id="area_of_occupancy-addon"
                                    class="input-group-text"
                                    >10km x 10km</span
                                >
                            </div>
                        </div>
                    </div>
                    <div class="row mb-3">
                        <label for="" class="col-sm-4 col-form-label"
                            >Actual Area of Occupancy:
                            <HelpText
                                v-if="
                                    species_community.distribution
                                        .aoo_actual_auto
                                "
                                section_id="species_actual_area_of_occupancy"
                        /></label>
                        <div class="col-sm-4">
                            <div class="input-group">
                                <input
                                    v-if="
                                        species_community.distribution
                                            .aoo_actual_auto
                                    "
                                    id="area_of_occupancy_actual"
                                    v-model="
                                        species_community.area_of_occupancy_km2
                                    "
                                    :disabled="isAOOActualReadOnly"
                                    type="number"
                                    step="any"
                                    class="form-control"
                                    placeholder=""
                                    area-describedby=""
                                />
                                <input
                                    v-else
                                    id="area_of_occupancy_actual"
                                    ref="area_of_occupancy_actual"
                                    v-model="
                                        species_community.distribution
                                            .area_of_occupancy_actual
                                    "
                                    :disabled="isAOOActualReadOnly"
                                    type="number"
                                    step="any"
                                    class="form-control"
                                    placeholder=""
                                />
                                <span
                                    id="area_of_occupancy_km2-addon"
                                    class="input-group-text"
                                    >km&#xb2;</span
                                >
                            </div>
                        </div>
                        <div
                            v-if="!isReadOnly"
                            class="col-sm-3 d-flex align-items-center"
                        >
                            <div class="form-check form-check-inline">
                                <input
                                    id="aoo_actual_auto"
                                    v-model="
                                        species_community.distribution
                                            .aoo_actual_auto
                                    "
                                    :disabled="isReadOnly"
                                    type="radio"
                                    :value="true"
                                    class="form-check-input"
                                    @click="switchAOOActual('true')"
                                />
                                <label class="form-check-label">auto</label>
                            </div>
                            <div class="form-check form-check-inline">
                                <input
                                    id="aoo_actual_manual"
                                    v-model="
                                        species_community.distribution
                                            .aoo_actual_auto
                                    "
                                    :disabled="isReadOnly"
                                    type="radio"
                                    :value="false"
                                    class="form-check-input"
                                    @click="switchAOOActual('false')"
                                />
                                <label class="form-check-label">manual</label>
                            </div>
                        </div>
                    </div>
                </template>
                <div
                    v-if="
                        showField(
                            species_community.distribution
                                .number_of_iucn_locations
                        )
                    "
                    class="row mb-3"
                >
                    <label for="" class="col-sm-4 col-form-label"
                        >Number of IUCN Locations:</label
                    >
                    <div class="col-sm-4">
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
                <div
                    v-if="
                        showField(
                            species_community.distribution
                                .number_of_iucn_subpopulations
                        )
                    "
                    class="row mb-1"
                >
                    <label for="" class="col-sm-4 col-form-label"
                        >Number of IUCN Sub-populations:</label
                    >
                    <div class="col-sm-4">
                        <input
                            id="number_of_iucn_subpopulations"
                            v-model="
                                species_community.distribution
                                    .number_of_iucn_subpopulations
                            "
                            :disabled="isReadOnly"
                            type="number"
                            class="form-control"
                            placeholder=""
                        />
                    </div>
                </div>
            </FormSection>

            <BasicConservationStatus
                v-if="
                    species_community.conservation_status &&
                    (conservation_status_public || is_internal)
                "
                :conservation_status="species_community.conservation_status"
                :is_internal="is_internal"
            />
            <!-- <FormSection v-if="conservation_attributes_public || is_internal" :formCollapse="false"
            label="Conservation Attributes" :Index="conservationBody">
            <div class="row mb-3">
                <label for="" class="col-sm-3 col-form-label">Habitat/Growth Form:</label>
                <div class="col-sm-9">
                    <textarea :disabled="isReadOnly" type="text" class="form-control" id="habitat_growth_form"
                        placeholder="" v-model="species_community.conservation_attributes.habitat_growth_form" />
                </div>
            </div>
            <div class="row mb-3" v-show="!isFauna">
                <label for="" class="col-sm-3 col-form-label">Flowering Period:</label>
                <div class="col-sm-9">
                    <select :disabled="isReadOnly" style="width:100%;" class="form-select" multiple
                        ref="flowering_period_select"
                        v-model="species_community.conservation_attributes.flowering_period">
                        <option v-for="option in period_list" :value="option.id" :key="option.id">
                            {{ option.name }}
                        </option>
                    </select>
                </div>
            </div>
            <div class="row mb-3" v-show="!isFauna">
                <label for="" class="col-sm-3 col-form-label">Fruiting Period:</label>
                <div class="col-sm-9">
                    <select :disabled="isReadOnly" style="width:100%;" class="form-select" multiple
                        ref="fruiting_period_select"
                        v-model="species_community.conservation_attributes.fruiting_period">
                        <option v-for="option in period_list" :value="option.id" :key="option.id">
                            {{ option.name }}
                        </option>
                    </select>
                </div>
            </div>
            <div class="row mb-3" v-show="!isFauna">
                <label for="" class="col-sm-3 col-form-label">Flora Recruitment Type:</label>
                <div class="col-sm-9">
                    <select :disabled="isReadOnly" class="form-select"
                        v-model="species_community.conservation_attributes.flora_recruitment_type_id">
                        <option v-for="option in flora_recruitment_type_list" :value="option.id" v-bind:key="option.id">
                            {{ option.name }}
                        </option>
                    </select>
                </div>
            </div>
            <div class="row mb-3" v-show="!isFauna">
                <label for="" class="col-sm-3 col-form-label">Flora Recruitment Notes:</label>
                <div class="col-sm-9">
                    <textarea :disabled="isReadOnly" type="text" class="form-control" id="recruitment_notes"
                        placeholder="" v-model="species_community.conservation_attributes.flora_recruitment_notes" />
                </div>
            </div>
            <div class="row mb-3" v-show="!isFauna">
                <label for="" class="col-sm-3 col-form-label">Seed Viability and Germination Info:</label>
                <div class="col-sm-9">
                    <textarea :disabled="isReadOnly" type="text" class="form-control" placeholder=""
                        v-model="species_community.conservation_attributes.seed_viability_germination_info" />
                </div>
            </div>
            <div class="row mb-3" v-show="!isFauna">
                <label for="" class="col-sm-3 col-form-label">Root Morphology:</label>
                <div class="col-sm-9">
                    <select :disabled="isReadOnly" class="form-select"
                        v-model="species_community.conservation_attributes.root_morphology_id">
                        <option v-for="option in root_morphology_list" :value="option.id" v-bind:key="option.id">
                            {{ option.name }}
                        </option>
                    </select>
                </div>
            </div>
            <div class="row mb-3" v-show="!isFauna">
                <label for="" class="col-sm-3 col-form-label">Pollinator Information:</label>
                <div class="col-sm-9">
                    <textarea :disabled="isReadOnly" type="text" class="form-control" placeholder=""
                        v-model="species_community.conservation_attributes.pollinator_information" />
                </div>
            </div>
            <div class="row mb-3" v-show="isFauna">
                <label for="" class="col-sm-3 col-form-label">Breeding Period:</label>
                <div class="col-sm-9">
                    <select :disabled="isReadOnly" style="width:100%;" class="form-select" multiple
                        ref="breeding_period_select"
                        v-model="species_community.conservation_attributes.breeding_period">
                        <option v-for="option in period_list" :value="option.id" :key="option.id">
                            {{ option.name }}
                        </option>
                    </select>
                </div>
            </div>
            <div class="row mb-3" v-show="isFauna">
                <label for="" class="col-sm-3 col-form-label">Fauna Breeding:</label>
                <div class="col-sm-9">
                    <textarea :disabled="isReadOnly" type="text" class="form-control" placeholder=""
                        v-model="species_community.conservation_attributes.fauna_breeding" />
                </div>
            </div>
            <div class="row mb-3" v-show="isFauna">
                <label for="" class="col-sm-3 col-form-label">Fauna Reproductive capacity:</label>
                <div class="col-sm-9">
                    <input :disabled="isReadOnly" type="text" class="form-control" id="fauna_reproductive_capacity"
                        placeholder=""
                        v-model="species_community.conservation_attributes.fauna_reproductive_capacity" />
                </div>
            </div>
            <div class="row mb-3">
                <label for="" class="col-sm-3 col-form-label">Time to Maturity:</label>
                <div class="col-sm-3 d-flex align-items-center">
                    <div class="form-check form-check-inline">
                        <input class="form-check-input" type="checkbox" name="time_to_maturity_range"
                            id="time_to_maturity_range" v-model="time_to_maturity_range" :disabled="isReadOnly"
                            @change="handleTimeToMaturityRange()" />
                        <label for="" class="form-check-label">Range</label>
                    </div>
                </div>
                <label for="" class="col-sm-6 col-form-label" style="color: red;">{{ errors.time_to_maturity_error
                    }}</label>
            </div>
            <div class="row mb-3" v-if="!time_to_maturity_range">
                <label for="" class="col-sm-3 col-form-label"></label>
                <div class="col-sm-4">
                    <div class="input-group">
                        <input :disabled="isReadOnly" type="number" class="form-control" id="time_to_maturity_from"
                            placeholder=""
                            @change="validateRange('time_to_maturity_from', 'time_to_maturity_to', 'time_to_maturity_choice', 'time_to_maturity_error')"
                            v-model="species_community.conservation_attributes.time_to_maturity_from" />
                        <select :disabled="isReadOnly" class="form-select"
                            @change="validateRange('time_to_maturity_from', 'time_to_maturity_to', 'time_to_maturity_choice', 'time_to_maturity_error')"
                            v-model="species_community.conservation_attributes.time_to_maturity_choice">
                            <option v-for="option in interval_choice" :value="option.id" v-bind:key="option.id">
                                {{ option.name }}
                            </option>
                        </select>
                    </div>
                </div>
                <div class="col-sm-4">
                    <label for="" class="col-form-label">{{
                        intervalMonthsComputed('time_to_maturity_from', 'time_to_maturity_choice') }}</label>
                </div>
            </div>
            <div class="row mb-3" v-else>
                <div class="col-sm-3"></div>
                <div class="col-sm-7">
                    <div class="input-group">
                        <label class="input-group-text" for="time_to_maturity_from">From:</label>
                        <input :disabled="isReadOnly" type="number" class="form-control" id="time_to_maturity_from"
                            placeholder=""
                            @change="validateRange('time_to_maturity_from', 'time_to_maturity_to', 'time_to_maturity_choice', 'time_to_maturity_error')"
                            v-model="species_community.conservation_attributes.time_to_maturity_from" />
                        <label class="input-group-text" for="time_to_maturity_to">To:</label>
                        <input :disabled="isReadOnly" type="number" class="form-control" id="time_to_maturity_to"
                            placeholder=""
                            @change="validateRange('time_to_maturity_from', 'time_to_maturity_to', 'time_to_maturity_choice', 'time_to_maturity_error')"
                            v-model="species_community.conservation_attributes.time_to_maturity_to" />

                        <select :disabled="isReadOnly" class="form-select"
                            @change="validateRange('time_to_maturity_from', 'time_to_maturity_to', 'time_to_maturity_choice', 'time_to_maturity_error')"
                            v-model="species_community.conservation_attributes.time_to_maturity_choice">
                            <option v-for="option in interval_choice" :value="option.id" v-bind:key="option.id">
                                {{ option.name }}
                            </option>
                        </select>
                    </div>
                </div>
            </div>
            <div class="row mb-3">
                <label for="" class="col-sm-3 col-form-label">Generation Length:</label>
                <div class="col-sm-3 d-flex align-items-center">
                    <div class="form-check form-check-inline">
                        <input class="form-check-input" type="checkbox" name="generation_length_range"
                            id="generation_length_range" v-model="generation_length_range" :disabled="isReadOnly"
                            @change="handleGenerationLengthRange()" />
                        <label for="" class="form-check-label">Range</label>
                    </div>
                </div>
                <label for="" class="col-sm-6 col-form-label" style="color: red;">{{ errors.generation_length_error
                    }}</label>
            </div>
            <div class="row mb-3" v-if="!generation_length_range">
                <label for="" class="col-sm-3 col-form-label"></label>
                <div class="col-sm-4">
                    <div class="input-group">
                        <input :disabled="isReadOnly" type="number" class="form-control" id="generation_length_from"
                            placeholder=""
                            @change="validateRange('generation_length_from', 'generation_length_to', 'generation_length_choice', 'generation_length_error')"
                            v-model="species_community.conservation_attributes.generation_length_from" />
                        <select :disabled="isReadOnly" class="form-select"
                            @change="validateRange('generation_length_from', 'generation_length_to', 'generation_length_choice', 'generation_length_error')"
                            v-model="species_community.conservation_attributes.generation_length_choice">
                            <option v-for="option in interval_choice" :value="option.id" v-bind:key="option.id">
                                {{ option.name }}
                            </option>
                        </select>
                    </div>
                </div>
                <div class="col-sm-4">
                    <label for="" class="col-form-label">{{
                        intervalMonthsComputed('generation_length_from', 'generation_length_choice') }}</label>
                </div>
            </div>
            <div class="row mb-3" v-else>
                <div class="col-sm-3"></div>
                <div class="col-sm-7">
                    <div class="input-group">
                        <label class="input-group-text" for="generation_length_from">From:</label>
                        <input :disabled="isReadOnly" type="number" class="form-control" id="generation_length_from"
                            placeholder=""
                            @change="validateRange('generation_length_from', 'generation_length_to', 'generation_length_choice', 'generation_length_error')"
                            v-model="species_community.conservation_attributes.generation_length_from" />
                        <label class="input-group-text" for="generation_length_to">To:</label>
                        <input :disabled="isReadOnly" type="number" class="form-control" id="generation_length_to"
                            placeholder=""
                            @change="validateRange('generation_length_from', 'generation_length_to', 'generation_length_choice', 'generation_length_error')"
                            v-model="species_community.conservation_attributes.generation_length_to" />
                        <select :disabled="isReadOnly" class="form-select"
                            @change="validateRange('generation_length_from', 'generation_length_to', 'generation_length_choice', 'generation_length_error')"
                            v-model="species_community.conservation_attributes.generation_length_choice">
                            <option v-for="option in interval_choice" :value="option.id" v-bind:key="option.id">
                                {{ option.name }}
                            </option>
                        </select>
                    </div>
                </div>
            </div>
            <div class="row mb-3">
                <label for="" class="col-sm-3 col-form-label">Average Lifespan:</label>
                <div class="col-sm-3 d-flex align-items-center">
                    <div class="form-check form-check-inline">
                        <input class="form-check-input" type="checkbox" name="average_lifespan_range"
                            id="average_lifespan_range" v-model="average_lifespan_range" :disabled="isReadOnly"
                            @change="handleAverageLifespanRange()" />
                        <label for="" class="form-check-label">Range</label>
                    </div>
                </div>
                <label for="" class="col-sm-6 col-form-label" style="color: red;">{{
                    errors.average_lifespan_error
                    }}</label>
            </div>
            <div class="row mb-3" v-if="!average_lifespan_range">
                <label for="" class="col-sm-3 col-form-label"></label>
                <div class="col-sm-4">
                    <div class="input-group">
                        <input :disabled="isReadOnly" type="number" class="form-control" id="average_lifespan_from"
                            placeholder=""
                            @change="validateRange('average_lifespan_from', 'average_lifespan_to', 'average_lifespan_choice', 'average_lifespan_error')"
                            v-model="species_community.conservation_attributes.average_lifespan_from" />
                        <select :disabled="isReadOnly" class="form-select"
                            @change="validateRange('average_lifespan_from', 'average_lifespan_to', 'average_lifespan_choice', 'average_lifespan_error')"
                            v-model="species_community.conservation_attributes.average_lifespan_choice">
                            <option v-for="option in interval_choice" :value="option.id" v-bind:key="option.id">
                                {{ option.name }}
                            </option>
                        </select>
                    </div>
                </div>
                <div class="col-sm-4">
                    <label for="" class="col-form-label">{{
                        intervalMonthsComputed('average_lifespan_from', 'average_lifespan_choice') }}</label>
                </div>
            </div>
            <div class="row mb-3" v-else>
                <div class="col-sm-3"></div>
                <div class="col-sm-7">
                    <div class="input-group">
                        <label class="input-group-text" for="average_lifespan_from">From:</label>
                        <input :disabled="isReadOnly" type="number" class="form-control" id="average_lifespan_from"
                            placeholder=""
                            @change="validateRange('average_lifespan_from', 'average_lifespan_to', 'average_lifespan_choice', 'average_lifespan_error')"
                            v-model="species_community.conservation_attributes.average_lifespan_from" />
                        <label class="input-group-text" for="average_lifespan_to">To:</label>
                        <input :disabled="isReadOnly" type="number" class="form-control" id="average_lifespan_to"
                            placeholder=""
                            @change="validateRange('average_lifespan_from', 'average_lifespan_to', 'average_lifespan_choice', 'average_lifespan_error')"
                            v-model="species_community.conservation_attributes.average_lifespan_to" />
                        <select :disabled="isReadOnly" class="form-select"
                            @change="validateRange('average_lifespan_from', 'average_lifespan_to', 'average_lifespan_choice', 'average_lifespan_error')"
                            v-model="species_community.conservation_attributes.average_lifespan_choice">
                            <option v-for="option in interval_choice" :value="option.id" v-bind:key="option.id">
                                {{ option.name }}
                            </option>
                        </select>
                    </div>
                </div>
            </div>
            <div class="row mb-3">
                <label for="" class="col-sm-3 col-form-label">Minimum Fire Interval:</label>
                <div class="col-sm-3 d-flex align-items-center">
                    <div class="form-check form-check-inline">
                        <input class="form-check-input" type="checkbox" name="minimum_fire_interval_range"
                            id="minimum_fire_interval_range" v-model="minimum_fire_interval_range"
                            :disabled="isReadOnly" @change="handleMinimumFireIntervalRange()" />
                        <label for="" class="form-check-label">Range</label>
                    </div>
                </div>
                <label for="" class="col-sm-6 col-form-label" style="color: red;">{{
                    errors.minimum_fire_interval_error
                    }}</label>
            </div>
            <div class="row mb-3" v-if="!minimum_fire_interval_range">
                <label for="" class="col-sm-3 col-form-label"></label>
                <div class="col-sm-4 d-flex align-items-center">
                    <div class="input-group">
                        <input :disabled="isReadOnly" type="number" class="form-control" id="minimum_fire_interval_from"
                            placeholder=""
                            @change="validateRange('minimum_fire_interval_from', 'minimum_fire_interval_to', 'minimum_fire_interval_choice', 'minimum_fire_interval_error')"
                            v-model="species_community.conservation_attributes.minimum_fire_interval_from" />
                        <select :disabled="isReadOnly" class="form-select"
                            @change="validateRange('minimum_fire_interval_from', 'minimum_fire_interval_to', 'minimum_fire_interval_choice', 'minimum_fire_interval_error')"
                            v-model="species_community.conservation_attributes.minimum_fire_interval_choice">
                            <option v-for="option in interval_choice" :value="option.id" v-bind:key="option.id">
                                {{ option.name }}
                            </option>
                        </select>
                    </div>
                </div>
                <div class="col-sm-4">
                    <label for="" class="col-form-label">{{
                        intervalMonthsComputed('minimum_fire_interval_from', 'minimum_fire_interval_choice')
                        }}</label>
                </div>
            </div>
            <div class="row mb-3" v-else>
                <label for="" class="col-sm-3 col-form-label"></label>
                <div class="col-sm-7 d-flex align-items-center">
                    <div class="input-group">
                        <label class="input-group-text" for="minimum_fire_interval_from">From:</label>
                        <input :disabled="isReadOnly" type="number" class="form-control" id="minimum_fire_interval_from"
                            placeholder=""
                            @change="validateRange('minimum_fire_interval_from', 'minimum_fire_interval_to', 'minimum_fire_interval_choice', 'minimum_fire_interval_error')"
                            v-model="species_community.conservation_attributes.minimum_fire_interval_from" />
                        <label class="input-group-text" for="minimum_fire_interval_to">To:</label>
                        <input :disabled="isReadOnly" type="number" class="form-control" id="minimum_fire_interval_to"
                            placeholder=""
                            @change="validateRange('minimum_fire_interval_from', 'minimum_fire_interval_to', 'minimum_fire_interval_choice', 'minimum_fire_interval_error')"
                            v-model="species_community.conservation_attributes.minimum_fire_interval_to" />
                        <select :disabled="isReadOnly" class="form-select"
                            @change="validateRange('minimum_fire_interval_from', 'minimum_fire_interval_to', 'minimum_fire_interval_choice', 'minimum_fire_interval_error')"
                            v-model="species_community.conservation_attributes.minimum_fire_interval_choice">
                            <option v-for="option in interval_choice" :value="option.id" v-bind:key="option.id">
                                {{ option.name }}
                            </option>
                        </select>
                    </div>
                </div>
            </div>
            <div class="row mb-3">
                <label for="" class="col-sm-3 col-form-label">Response to Fire:</label>
                <div class="col-sm-9">
                    <textarea :disabled="isReadOnly" type="text" class="form-control" id="response_to_fire"
                        placeholder="" v-model="species_community.conservation_attributes.response_to_fire" />
                </div>
            </div>
            <div class="row mb-3">
                <label for="" class="col-sm-3 col-form-label">Post Fire Habitat Interactions:</label>
                <div class="col-sm-9">
                    <select :disabled="isReadOnly" class="form-select"
                        v-model="species_community.conservation_attributes.post_fire_habitat_interaction_id">
                        <option v-for="option in post_fire_habitatat_interactions_list" :value="option.id"
                            v-bind:key="option.id">
                            {{ option.name }}
                        </option>
                    </select>
                </div>
            </div>

            <div class="row mb-3">
                <label for="" class="col-sm-3 col-form-label">Habitat:</label>
                <div class="col-sm-9">
                    <textarea :disabled="isReadOnly" type="text" class="form-control" id="habitat" placeholder=""
                        v-model="species_community.conservation_attributes.habitat" />
                </div>
            </div>
            <div class="row mb-3">
                <label for="" class="col-sm-3 col-form-label">Hydrology:</label>
                <div class="col-sm-9">
                    <textarea :disabled="isReadOnly" type="text" class="form-control" id="hydrology" placeholder=""
                        v-model="species_community.conservation_attributes.hydrology" />
                </div>
            </div>
            <div class="row mb-3" v-show="isFauna">
                <label for="" class="col-sm-3 col-form-label">Diet and Food Source:</label>
                <div class="col-sm-9">
                    <textarea :disabled="isReadOnly" type="text" class="form-control" id="diet_food_source"
                        placeholder="" v-model="species_community.conservation_attributes.diet_and_food_source" />
                </div>
            </div>
            <div class="row mb-3" v-show="isFauna">
                <label for="" class="col-sm-3 col-form-label">Home Range:</label>
                <div class="col-sm-9">
                    <textarea :disabled="isReadOnly" type="text" class="form-control" id="home_range" placeholder=""
                        v-model="species_community.conservation_attributes.home_range" />
                </div>
            </div>
            <div class="row mb-3">
                <label for="" class="col-sm-3 col-form-label">Research Requirements:</label>
                <div class="col-sm-9">
                    <textarea :disabled="isReadOnly" type="text" class="form-control" id="research_requirements"
                        placeholder="" v-model="species_community.conservation_attributes.research_requirements" />
                </div>
            </div>
            <div class="row mb-3" v-show="!isFauna">
                <label for="" class="col-sm-3 col-form-label">Response to Dieback:</label>
                <div class="col-sm-9">
                    <textarea :disabled="isReadOnly" type="text" class="form-control" id="response_to_dieback"
                        placeholder="" v-model="species_community.conservation_attributes.response_to_dieback" />
                </div>
            </div>
            <div class="row mb-3">
                <label for="" class="col-sm-3 col-form-label">Other relevant diseases:</label>
                <div class="col-sm-9">
                    <textarea :disabled="isReadOnly" type="text" class="form-control" id="other_relevant_diseases"
                        placeholder="" v-model="species_community.conservation_attributes.other_relevant_diseases" />
                </div>
            </div>
        </FormSection> -->
            <FormSection
                v-if="is_internal"
                :form-collapse="false"
                label="General"
                :Index="generalBody"
            >
                <div class="row mb-3">
                    <label for="" class="col-sm-3 col-form-label"
                        >Department File Numbers:</label
                    >
                    <div class="col-sm-9">
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
                    <label for="" class="col-sm-3 col-form-label"
                        >Last data curation date:
                    </label>
                    <div class="col-sm-9">
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
                <div class="row mb-3">
                    <label
                        for="conservation_plan_exists"
                        class="col-sm-3 col-form-label"
                        >Conservation Plan Exists:
                    </label>
                    <div class="col-sm-9">
                        <label for="conservation_plan_exists" class="me-2"
                            >No</label
                        >
                        <input
                            id="conservation_plan_exists"
                            v-model="species_community.conservation_plan_exists"
                            :disabled="isReadOnly"
                            type="radio"
                            :value="false"
                            class="form-check-input me-2"
                        />
                        <label for="conservation_plan_exists" class="me-2"
                            >Yes</label
                        >
                        <input
                            id="conservation_plan_exists"
                            v-model="species_community.conservation_plan_exists"
                            :disabled="isReadOnly"
                            type="radio"
                            :value="true"
                            class="form-check-input"
                            @change="focusConservationPlanReference"
                        />
                    </div>
                </div>
                <div
                    v-if="species_community.conservation_plan_exists"
                    class="row mb-3"
                >
                    <label
                        for="conservation_plan_reference"
                        class="col-sm-3 col-form-label"
                        >Conservation Plan Reference:
                    </label>
                    <div class="col-sm-9">
                        <input
                            ref="conservation_plan_reference"
                            v-model="
                                species_community.conservation_plan_reference
                            "
                            :disabled="isReadOnly"
                            type="text"
                            class="form-control"
                            name="conservation_plan_reference"
                            @change="checkDate()"
                        />
                    </div>
                </div>
                <div class="row mb-3">
                    <label for="" class="col-sm-3 col-form-label"
                        >Comment:</label
                    >
                    <div class="col-sm-9">
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
            <FormSection
                v-if="is_internal"
                :form-collapse="false"
                label="Publishing"
                Index="publishing"
            >
                <div class="row mb-3">
                    <label
                        for="distribution_publishing"
                        class="col-sm-3 col-form-label"
                        >Distribution:
                    </label>
                    <div class="col-sm-9">
                        <div class="form-check form-check-inline">
                            <label for="distribution_publishing">Private</label>
                            <input
                                id="distribution_publishing"
                                v-model="
                                    species_community.publishing_status
                                        .distribution_public
                                "
                                :disabled="isReadOnly || !isPublic || !isActive"
                                type="radio"
                                :value="false"
                                class="form-check-input me-2"
                            />
                        </div>
                        <div class="form-check form-check-inline">
                            <label for="distribution_publishing">Public</label>
                            <input
                                id="distribution_publishing"
                                v-model="
                                    species_community.publishing_status
                                        .distribution_public
                                "
                                :disabled="isReadOnly || !isPublic || !isActive"
                                type="radio"
                                :value="true"
                                class="form-check-input"
                            />
                        </div>
                    </div>
                </div>
                <div class="row mb-3">
                    <label
                        for="conservation_status_publishing"
                        class="col-sm-3 col-form-label"
                        >Conservation Status:
                    </label>
                    <div class="col-sm-9">
                        <div class="form-check form-check-inline">
                            <label for="conservation_status_publishing"
                                >Private</label
                            >
                            <input
                                id="conservation_status_publishing"
                                v-model="
                                    species_community.publishing_status
                                        .conservation_status_public
                                "
                                :disabled="isReadOnly || !isPublic || !isActive"
                                type="radio"
                                :value="false"
                                class="form-check-input me-2"
                            />
                        </div>
                        <div class="form-check form-check-inline">
                            <label for="conservation_status_publishing"
                                >Public</label
                            >
                            <input
                                id="conservation_status_publishing"
                                v-model="
                                    species_community.publishing_status
                                        .conservation_status_public
                                "
                                :disabled="isReadOnly || !isPublic || !isActive"
                                type="radio"
                                :value="true"
                                class="form-check-input"
                            />
                        </div>
                    </div>
                </div>
                <!-- <div class="row mb-3">
                <label for="conservation_attributes_publishing" class="col-sm-3 col-form-label">Conservation Attributes:
                </label>
                <div class="col-sm-9">
                    <div class="form-check form-check-inline">
                        <label for="conservation_attributes_publishing">Private</label>
                        <input :disabled="isReadOnly || !isPublic || !isActive" type="radio" :value="false"
                            class="form-check-input me-2" id="conservation_attributes_publishing"
                            v-model="species_community.publishing_status.conservation_attributes_public">
                    </div>
                    <div class="form-check form-check-inline">
                        <label for="conservation_attributes_publishing">Public</label>
                        <input :disabled="isReadOnly || !isPublic || !isActive" type="radio" :value="true"
                            class="form-check-input" id="conservation_attributes_publishing"
                            v-model="species_community.publishing_status.conservation_attributes_public">
                    </div>
                </div>
            </div> -->
                <div class="row mb-3">
                    <label
                        for="threats_publishing"
                        class="col-sm-3 col-form-label"
                        >Threats:
                    </label>
                    <div class="col-sm-9">
                        <div class="form-check form-check-inline">
                            <label for="threats_publishing">Private</label>
                            <input
                                id="threats_publishing"
                                v-model="
                                    species_community.publishing_status
                                        .threats_public
                                "
                                :disabled="isReadOnly || !isPublic || !isActive"
                                type="radio"
                                :value="false"
                                class="form-check-input me-2"
                            />
                        </div>
                        <div class="form-check form-check-inline">
                            <label for="threats_publishing">Public</label>
                            <input
                                id="threats_publishing"
                                v-model="
                                    species_community.publishing_status
                                        .threats_public
                                "
                                :disabled="isReadOnly || !isPublic || !isActive"
                                type="radio"
                                :value="true"
                                class="form-check-input"
                            />
                        </div>
                    </div>
                </div>
                <div class="row mb-3">
                    <div class="col-sm-12">
                        <button
                            v-if="!updatingPublishing"
                            :disabled="isReadOnly || !isPublic || !isActive"
                            class="btn btn-primary btn-sm float-end"
                            @click.prevent="updatePublishingDetails()"
                        >
                            Update
                        </button>
                        <button
                            v-else
                            disabled
                            class="float-end btn btn-primary"
                        >
                            Updating
                            <span
                                class="spinner-border spinner-border-sm"
                                role="status"
                                aria-hidden="true"
                            ></span>
                            <span class="visually-hidden">Loading...</span>
                        </button>
                    </div>
                </div>
            </FormSection>
        </fieldset>
    </div>
</template>

<script>
import { v4 as uuid } from 'uuid';
import FormSection from '@/components/forms/section_toggle.vue';
import BasicConservationStatus from './basic_conservation_status.vue';
import HelpText from '@/components/common/help_text.vue';

import { api_endpoints, helpers } from '@/utils/hooks';
export default {
    name: 'SpeciesProfile',
    components: {
        FormSection,
        BasicConservationStatus,
        HelpText,
    },
    emits: ['save-species-community'],
    props: {
        species_community: {
            type: Object,
            required: true,
        },
        species_community_original: {
            type: Object,
            required: true,
        },
        // this prop is only send from split species form to make the original species readonly
        is_readonly: {
            type: Boolean,
            default: false,
        },
        // this prop is only send from rename species form to make the taxon select editable
        rename_species: {
            type: Boolean,
            default: false,
        },
        is_internal: {
            type: Boolean,
            default: false,
        },
    },
    data: function () {
        let vm = this;
        return {
            datepickerOptions: {
                format: 'DD/MM/YYYY',
                showClear: true,
                useCurrent: false,
                keepInvalid: true,
                allowInputToggle: true,
            },
            updatingPublishing: false,
            scientific_name_lookup: 'scientific_name_lookup' + uuid(),
            select_scientific_name: 'select_scientific_name' + uuid(),
            select_flowering_period: 'select_flowering_period' + uuid(),
            taxonBody: 'taxonBody' + uuid(),
            distributionBody: 'distributionBody' + uuid(),
            conservationStatusBody: 'conservationStatusBody' + uuid(),
            conservationBody: 'conservationBody' + uuid(),
            generalBody: 'generalBody' + uuid(),
            //---to show fields related to Fauna
            isFauna: vm.species_community.group_type === 'fauna' ? true : false,
            //----list of values dictionary
            taxon_names: [],
            species_profile_dict: {},
            region_list: [],
            district_list: [],
            filtered_district_list: [],
            flora_recruitment_type_list: [],
            root_morphology_list: [],
            post_fire_habitatat_interactions_list: [],
            // to display the species Taxonomy selected details
            species_display: '',
            conservation_category: '',
            conservation_list: '',
            conservation_criteria: '',
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
            minimum_fire_interval_range: false,
            average_lifespan_range: false,
            generation_length_range: false,
            time_to_maturity_range: false,
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
        distribution_public: function () {
            return (
                this.isPublic &&
                this.species_community.publishing_status.distribution_public
            );
        },
        conservation_status_public: function () {
            return (
                this.isPublic &&
                this.species_community.publishing_status
                    .conservation_status_public
            );
        },
        conservation_attributes_public: function () {
            return (
                this.isPublic &&
                this.species_community.publishing_status
                    .conservation_attributes_public
            );
        },
        isReadOnly: function () {
            // this prop (is_readonly = true) is only send from split/combine species form to make the original species readonly
            if (this.is_readonly) {
                return this.is_readonly;
            }
            //---else the normal serializer value
            else {
                let action = this.$route.query.action;
                if (action === 'view') {
                    return true;
                } else if (
                    action === 'edit' &&
                    this.species_community &&
                    this.species_community.user_edit_mode
                ) {
                    return false;
                } else {
                    return this.species_community.readonly;
                }
            }
        },
        scientificNameIsReadOnly: function () {
            return (
                (this.isReadOnly ||
                    this.species_community.processing_status === 'Active') &&
                !this.rename_species
            );
        },
        isActive: function () {
            return this.species_community.processing_status === 'Active'
                ? true
                : false;
        },
        isPublic: function () {
            return this.isActive &&
                this.species_community.publishing_status.species_public
                ? true
                : false;
        },
        isNOOReadOnly: function () {
            let vm = this;
            if (vm.species_community.distribution.noo_auto === true) {
                return true;
            } else {
                return vm.isReadOnly;
            }
        },
        isEOOReadOnly: function () {
            let vm = this;
            if (vm.species_community.distribution.eoo_auto === true) {
                return true;
            } else {
                return vm.isReadOnly;
            }
        },
        isAOOActualReadOnly: function () {
            let vm = this;
            if (vm.species_community.distribution.aoo_actual_auto === true) {
                return true;
            } else {
                return vm.isReadOnly;
            }
        },
        show_calculated_distribution_fields: function () {
            return (
                this.is_internal ||
                (this.species_community.distribution.noo_auto &&
                    this.species_community.occurrence_count > 0) ||
                (!this.species_community.distribution.noo_auto &&
                    this.species_community.distribution.number_of_occurrences >
                        0)
            );
        },
    },
    watch: {
        // "species_community.distribution.eoo_auto": function(newVal) {
        //     let vm=this;
        //     var selectedValue = newVal;
        //         if(selectedValue === "true"){
        //             vm.species_community.distribution.extent_of_occurrences=vm.species_community.distribution.cal_extent_of_occurrences;
        //         }
        //         else{
        //             vm.species_community.distribution.extent_of_occurrences=null;
        //         }
        // },
        'species_community.distribution.number_of_iucn_locations': function (
            newVal
        ) {
            let vm = this;
            if (newVal == '') {
                vm.species_community.distribution.number_of_iucn_locations =
                    null;
            }
        },
        'species_community.distribution.number_of_iucn_subpopulations':
            function (newVal) {
                let vm = this;
                if (newVal == '') {
                    vm.species_community.distribution.number_of_iucn_subpopulations =
                        null;
                }
            },
    },
    created: async function () {
        let vm = this;
        if (vm.species_community.conservation_attributes) {
            if (
                vm.species_community.conservation_attributes
                    .minimum_fire_interval_to != null &&
                vm.species_community.conservation_attributes
                    .minimum_fire_interval_to != '' &&
                vm.species_community.conservation_attributes
                    .minimum_fire_interval_to != undefined
            ) {
                vm.minimum_fire_interval_range = true;
            }
            if (
                vm.species_community.conservation_attributes
                    .average_lifespan_to != null &&
                vm.species_community.conservation_attributes
                    .average_lifespan_to != '' &&
                vm.species_community.conservation_attributes
                    .average_lifespan_to != undefined
            ) {
                vm.average_lifespan_range = true;
            }
            if (
                vm.species_community.conservation_attributes
                    .generation_length_to != null &&
                vm.species_community.conservation_attributes
                    .generation_length_to != '' &&
                vm.species_community.conservation_attributes
                    .generation_length_to != undefined
            ) {
                vm.generation_length_range = true;
            }
            if (
                vm.species_community.conservation_attributes
                    .time_to_maturity_to != null &&
                vm.species_community.conservation_attributes
                    .time_to_maturity_to != '' &&
                vm.species_community.conservation_attributes
                    .time_to_maturity_to != undefined
            ) {
                vm.time_to_maturity_range = true;
            }
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
        vm.enablePopovers();
    },
    methods: {
        showField(fieldValue) {
            if (!this.isReadOnly) {
                return true;
            }
            return this.isReadOnly && fieldValue;
        },
        updatePublishing(data) {
            let vm = this;
            fetch(
                helpers.add_endpoint_json(
                    api_endpoints.species,
                    vm.species_community.id + '/update_publishing_status'
                ),
                {
                    method: 'PATCH',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: data,
                }
            ).then(
                async (response) => {
                    vm.updatingPublishing = false;
                    vm.species_community.publishing_status =
                        await response.json();
                    vm.species_community_original.publishing_status =
                        helpers.copyObject(
                            vm.species_community.publishing_status
                        );
                    swal.fire({
                        title: 'Saved',
                        text: 'Publishing settings have been updated',
                        icon: 'success',
                        customClass: {
                            confirmButton: 'btn btn-primary',
                        },
                    });
                },
                (error) => {
                    var text = helpers.apiVueResourceError(error);
                    swal.fire({
                        title: 'Error',
                        text:
                            'Publishing settings cannot be updated because of the following error: ' +
                            text,
                        icon: 'error',
                        customClass: {
                            confirmButton: 'btn btn-primary',
                        },
                    });
                    vm.updatingPublishing = false;
                }
            );
        },
        updatePublishingDetails: function () {
            let vm = this;
            vm.updatingPublishing = true;
            //if not already public, we make it public (notify user first)
            //but only if it is active
            if (vm.isPublic && vm.isActive) {
                //send just publishing form data
                let data = JSON.stringify(
                    vm.species_community.publishing_status
                );
                vm.updatePublishing(data);
            } else {
                swal.fire({
                    title: 'Error',
                    text: 'Record not active and cannot be made public',
                    icon: 'error',
                    customClass: {
                        confirmButton: 'btn btn-primary',
                    },
                });
                vm.updatingPublishing = false;
            }
        },
        switchNOO: function (value) {
            let vm = this;
            var selectedValue = value;
            if (selectedValue === 'true') {
                swal.fire({
                    title: 'Changing from Manual to Auto',
                    text: 'If you choose to revert back to manual in future the manually entered value will still be there for you. It is not deleted.',
                    icon: 'info',
                    confirmButtonText: 'Ok',
                    showCancelButton: false,
                    customClass: {
                        confirmButton: 'btn btn-primary',
                    },
                    reverseButtons: true,
                }).then(
                    (swalresult) => {
                        if (swalresult.isConfirmed) {
                            document.getElementById('noo_auto').checked = true;
                            document.getElementById('noo_manual').checked =
                                false;
                            vm.species_community.distribution.noo_auto = true;
                        } else if (
                            swalresult.dismiss === swal.DismissReason.cancel
                        ) {
                            document.getElementById('noo_manual').checked =
                                true;
                            document.getElementById('noo_auto').checked = false;
                            vm.species_community.distribution.noo_auto = false;
                        }
                    },
                    (error) => {
                        console.error('Error:', error);
                    }
                );
            } else {
                document.getElementById('noo_manual').checked = true;
                document.getElementById('noo_auto').checked = false;
                vm.species_community.distribution.noo_auto = false;
                vm.$nextTick(() => {
                    vm.$refs.number_of_occurrences.focus();
                });
            }
        },
        switchEOO: function (value) {
            let vm = this;
            var selectedValue = value;
            if (selectedValue === 'true') {
                swal.fire({
                    title: 'Changing from Manual to Auto',
                    text: 'If you choose to revert back to manual in future the manually entered value will still be there for you. It is not deleted.',
                    icon: 'info',
                    confirmButtonText: 'Ok',
                    showCancelButton: false,
                    customClass: {
                        confirmButton: 'btn btn-primary',
                    },
                    reverseButtons: true,
                }).then(
                    (swalresult) => {
                        if (swalresult.isConfirmed) {
                            // set EOO field to calculted_EOO vale
                            document.getElementById('eoo_auto').checked = true;
                            document.getElementById('eoo_manual').checked =
                                false;
                            // set eoo to true to fire the change of value so the EOO input box readonly
                            vm.species_community.distribution.eoo_auto = true;
                            vm.$nextTick(() => {
                                vm.enablePopovers();
                            });
                        } else if (
                            swalresult.dismiss === swal.DismissReason.cancel
                        ) {
                            document.getElementById('eoo_manual').checked =
                                true;
                            document.getElementById('eoo_auto').checked = false;
                            // set eoo to false to fire the change of value so the EOO input box will be editable
                            vm.species_community.distribution.eoo_auto = false;
                            //Otherwise revert back to its manual value if swal cancelled
                        }
                    },
                    (error) => {
                        console.error('Error:', error);
                    }
                );
            } else {
                // set EOO value to null if manual selected
                document.getElementById('eoo_manual').checked = true;
                document.getElementById('eoo_auto').checked = false;
                // set eoo to false to fire the change of value so the EOO input box will be editable
                vm.species_community.distribution.eoo_auto = false;
                vm.$nextTick(() => {
                    vm.$refs.extent_of_occurrence.focus();
                });
            }
        },
        switchAOOActual: function (value) {
            let vm = this;
            var selectedValue = value;
            if (selectedValue === 'true') {
                swal.fire({
                    title: 'Changing from Manual to Auto',
                    text: 'If you choose to revert back to manual in future the manually entered value will still be there for you. It is not deleted.',
                    icon: 'info',
                    confirmButtonText: 'Ok',
                    showCancelButton: false,
                    customClass: {
                        confirmButton: 'btn btn-primary',
                    },
                    reverseButtons: true,
                }).then(
                    (swalresult) => {
                        if (swalresult.isConfirmed) {
                            // set AOOActual field to calculted_AOOActual vale
                            document.getElementById('aoo_actual_auto').checked =
                                true;
                            document.getElementById(
                                'aoo_actual_manual'
                            ).checked = false;
                            // set aoo_actual to true to fire the change of value so the AOOActual input box readonly
                            vm.species_community.distribution.aoo_actual_auto = true;
                            vm.$nextTick(() => {
                                vm.enablePopovers();
                            });
                        } else if (
                            swalresult.dismiss === swal.DismissReason.cancel
                        ) {
                            document.getElementById(
                                'aoo_actual_manual'
                            ).checked = true;
                            document.getElementById('aoo_actual_auto').checked =
                                false;
                            // set eoo to false to fire the change of value so the EOO input box will be editable
                            vm.species_community.distribution.aoo_actual_auto = false;
                            //Otherwise revert back to its manual value if swal cancelled
                        }
                    },
                    (error) => {
                        console.error('Error:', error);
                    }
                );
            } else {
                // set AOOActual value to null if manual selected
                document.getElementById('aoo_actual_manual').checked = true;
                document.getElementById('aoo_actual_auto').checked = false;
                // set aoo_actual to false to fire the change of value so the AOOActual input box will be editable
                vm.species_community.distribution.aoo_actual_auto = false;
                vm.$nextTick(() => {
                    vm.$refs.area_of_occupancy_actual.focus();
                });
            }
        },
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
                                species_profile: true,
                                species_id: vm.species_community.id, // to filter species  current/non_current
                            };
                            return query;
                        },
                        // results: function (data, page) { // parse the results into the format expected by Select2.
                        //     // since we are using custom formatting functions we do not need to alter remote JSON data
                        //     return {results: data};
                        // },
                    },
                })
                .on('select2:select', function (e) {
                    let data = e.params.data.id;
                    vm.species_community.taxonomy_id = data;
                    vm.species_display = e.params.data.scientific_name;
                    if (e.params.data.conservation_status) {
                        vm.conservation_category =
                            e.params.data.conservation_status.conservation_category;
                        vm.conservation_list =
                            e.params.data.conservation_status.conservation_list;
                        vm.conservation_criteria =
                            e.params.data.conservation_status.conservation_criteria;
                    }
                    vm.common_name = e.params.data.common_name;
                    vm.taxon_name_id = e.params.data.taxon_name_id;
                    vm.taxon_previous_name = e.params.data.taxon_previous_name;
                    vm.phylogenetic_group = e.params.data.phylogenetic_group;
                    vm.family = e.params.data.family_name;
                    vm.genus = e.params.data.genera_name;
                    vm.name_authority = e.params.data.name_authority;
                    vm.name_comments = e.params.data.name_comments;
                    vm.$emit('save-species-community');
                })
                .on('select2:unselect', function () {
                    vm.species_community.taxonomy_id = null;
                    vm.species_display = '';
                    vm.conservation_category = '';
                    vm.conservation_criteria = '';
                    vm.conservation_list = '';
                    vm.common_name = '';
                    vm.taxon_name_id = '';
                    vm.taxon_previous_name = '';
                    vm.phylogenetic_group = '';
                    (vm.family = ''), (vm.genus = ''), (vm.name_authority = '');
                    vm.name_comments = '';
                    vm.$emit('save-species-community');
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
                var newOption = new Option(
                    vm.species_community.taxonomy_details.scientific_name,
                    vm.species_community.taxonomy_id,
                    false,
                    true
                );
                // newOption.setAttribute('data-select2-id', '2');
                $('#' + vm.scientific_name_lookup).append(newOption);
                vm.species_display =
                    vm.species_community.taxonomy_details.scientific_name;
                if (vm.species_community.conservation_status) {
                    vm.conservation_category =
                        vm.species_community.conservation_status.conservation_category;
                    vm.conservation_list =
                        vm.species_community.conservation_status.conservation_list;
                }
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
        eventListeners: function () {
            let vm = this;
            $(vm.$refs.flowering_period_select)
                .select2({
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
            $(vm.$refs.fruiting_period_select)
                .select2({
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
            $(vm.$refs.breeding_period_select)
                .select2({
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
        },
        handleMinimumFireIntervalRange: function () {
            if (this.minimum_fire_interval_range == false) {
                this.species_community.conservation_attributes.minimum_fire_interval_to =
                    null;
            }
        },
        handleAverageLifespanRange: function () {
            if (this.average_lifespan_range == false) {
                this.species_community.conservation_attributes.average_lifespan_to =
                    null;
            }
        },
        handleGenerationLengthRange: function () {
            if (this.generation_length_range == false) {
                this.species_community.conservation_attributes.generation_length_to =
                    null;
            }
        },
        handleTimeToMaturityRange: function () {
            if (this.time_to_maturity_range == false) {
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
        intervalMonthsComputed: function (field_from, field_choice) {
            const totalMonths = parseInt(
                this.species_community.conservation_attributes[field_from]
            );
            const intervalChoice =
                this.species_community.conservation_attributes[field_choice];

            if (totalMonths > 12 && intervalChoice == 2) {
                const years = Math.floor(totalMonths / 12);
                const months = totalMonths % 12;
                return years + ' year/s ' + months + ' month/s';
            } else {
                return '';
            }
        },
        focusConservationPlanReference: function () {
            this.$nextTick(() => {
                this.$refs.conservation_plan_reference.focus();
            });
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
                // Remove any districts that are not in the selected regions
                var selected_districts = vm.species_community.districts;
                for (let i = 0; i < selected_districts.length; i++) {
                    var district = selected_districts[i];
                    var region = vm.searchList(district, vm.region_list);
                    if (region == []) {
                        vm.species_community.districts.splice(i, 1);
                    }
                }
            }
            vm.district_list = [];
            if (regions) {
                for (let r of regions) {
                    var api_districts = this.searchList(
                        r,
                        vm.region_list
                    ).districts;
                    if (api_districts.length > 0) {
                        for (let i = 0; i < api_districts.length; i++) {
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
                    placeholder: 'Select Region',
                })
                .on('select2:select', function (e) {
                    var selected = $(e.currentTarget);
                    vm.species_community.regions = selected.val();
                    vm.chainedSelectDistricts(
                        vm.species_community.regions,
                        'select'
                    );
                    vm.$emit('save-species-community');
                })
                .on('select2:unselect', function (e) {
                    var selected = $(e.currentTarget);
                    vm.species_community.regions = selected.val();
                    vm.chainedSelectDistricts(
                        vm.species_community.regions,
                        'deselect'
                    );
                    vm.$emit('save-species-community');
                });
        },
        initialiseDistrictSelect: function () {
            let vm = this;
            $(vm.$refs.districts_select)
                .select2({
                    theme: 'bootstrap-5',
                    allowClear: true,
                    multiple: true,
                    placeholder: 'Select District',
                })
                .on('select2:select', function (e) {
                    var selected = $(e.currentTarget);
                    vm.species_community.districts = selected.val();
                    vm.$emit('save-species-community');
                })
                .on('select2:unselect', function (e) {
                    var selected = $(e.currentTarget);
                    vm.species_community.districts = selected.val();
                    vm.$emit('save-species-community');
                });
        },
        enablePopovers: function () {
            var popoverTriggerList = [].slice.call(
                document.querySelectorAll('[data-bs-toggle="popover"]')
            );
            popoverTriggerList.map(function (popoverTriggerEl) {
                return new bootstrap.Popover(popoverTriggerEl);
            });
        },
        saveSpeciesCommunity: function (e) {
            // For the select2 we emit after the select/unselect event as otherwise the value is not yet updated
            if (!e.target.className.includes('select2-')) {
                this.$emit('save-species-community');
            }
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
</style>
