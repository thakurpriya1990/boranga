<template lang="html">
    <div>
        <div class="col-md-12">
            <ul v-if="is_internal" class="nav nav-pills" id="pills-tab" role="tablist">
              <li class="nav-item">
                <a
                    class="nav-link active"
                    id="pills-profile-tab"
                    data-bs-toggle="pill"
                    :href="'#' + profileBody"
                    role="tab"
                    :aria-controls="profileBody"
                    aria-selected="true">
                  Profile
                </a>
              </li>
              <li class="nav-item">
                <a
                    class="nav-link"
                    id="pills-documents-tab"
                    data-bs-toggle="pill"
                    :href="'#' + documentBody"
                    role="tab"
                    aria-controls="pills-documents"
                    :aria-selected="documentBody"
                    @click="tabClicked()">
                  Documents
                </a>
              </li>
              <li class="nav-item">
                <a
                    class="nav-link"
                    id="pills-threats-tab"
                    data-bs-toggle="pill"
                    :href="'#' + threatBody "
                    role="tab"
                    :aria-controls="threatBody"
                    aria-selected="false"
                    @click="tabClicked()">
                  Threats
                </a>
              </li>
            </ul>
            <div class="tab-content" id="pills-tabContent">
              <div class="tab-pane fade show active" :id="profileBody" role="tabpanel" aria-labelledby="pills-profile-tab">
                <SpeciesProfile
                    ref="species_information"
                    id="speciesInformation"
                    :is_internal="is_internal"
                    :species_community="species_community"
                    :species_original="species_original">
                </SpeciesProfile>
              </div>
              <div class="tab-pane fade" :id="documentBody" role="tabpanel" aria-labelledby="pills-documents-tab">
                <SpeciesDocuments
                    :key="reloadcount"
                    ref="species_documents"
                    id="speciesDocuments"
                    :is_internal="is_internal"
                    :species_community="species_community"
                    :species_original="species_original">
                </SpeciesDocuments>
              </div>
              <div class="tab-pane fade" :id="threatBody" role="tabpanel" aria-labelledby="pills-threats-tab">
                <SpeciesThreats
                    :key="reloadcount"
                    ref="species_threats"
                    id="speciesThreats"
                    :is_internal="is_internal"
                    :species_community="species_community"
                    :species_original="species_original">
                </SpeciesThreats>
              </div>
            </div>
        </div>
    </div>
</template>

<script>
    import SpeciesProfile from '@/components/common/species_communities/species_split/species_split_profile.vue'
    import SpeciesDocuments from '@/components/common/species_communities/species_split/species_split_documents.vue'
    import SpeciesThreats from '@/components/common/species_communities/species_split/species_split_threats.vue'

    export default {
        props:{
            species_original:{
                type: Object,
                required:true
            },
            species_community:{
                type: Object,
                required:true
            },
            is_external:{
              type: Boolean,
              default: false
            },
            is_internal:{
              type: Boolean,
              default: false
            },
        },
        data:function () {
            let vm = this;
            return{
                profileBody: 'profileBody' + vm._uid,
                documentBody: 'documentBody' + vm._uid,
                threatBody: 'threatBody' + vm._uid,
                relatedItemBody: 'relatedItemBody' + vm._uid,
                values:null,
                reloadcount:0,
                document_selection:null,
                threat_selection:null,
            }
        },
        components: {
            SpeciesProfile,
            SpeciesDocuments,
            SpeciesThreats,
        },
        computed:{
            related_items_ajax_url: function(){
                return '/api/species/' + this.species_community.id + '/get_related_items/'
            },
            related_items_filter_list_url: function(){
                return '/api/species/filter_list.json'
            },
        },
        methods:{
            //----function to resolve datatable exceeding beyond the div
            tabClicked: function(param){
                this.reloadcount = this.reloadcount+1;
            },
        },
        mounted: function() {
            let vm = this;
            vm.form = document.forms.new_species;
        }
    }
</script>
