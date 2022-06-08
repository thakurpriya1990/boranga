<template lang="html">
    <div>
        <div class="col-md-12">

            <ul class="nav nav-pills mb-3" id="pills-tab" role="tablist">
              <li class="nav-item">
                <a class="nav-link" id="pills-profile-tab" data-bs-toggle="pill" href="#pills-profile" role="tab" aria-controls="pills-profile" aria-selected="true">
                  Profile
                </a>
              </li>
              <li class="nav-item">
                <a class="nav-link" id="pills-documents-tab" data-bs-toggle="pill" href="#pills-documents" role="tab" aria-controls="pills-documents" aria-selected="false">
                  Documents
                </a>
              </li>
              <li class="nav-item">
                <a class="nav-link" id="pills-threats-tab" data-bs-toggle="pill" href="#pills-threats" role="tab" aria-controls="pills-threats" aria-selected="false">
                  Threats
                </a>
              </li>
              <li class="nav-item">
                <a class="nav-link" id="pills-conservation-plans-tab" data-bs-toggle="pill" href="#pills-conservation-plans" role="tab" aria-controls="pills-management-plans" aria-selected="false">
                  Conservation Plans
                </a>
              </li>
              <li v-if="is_internal" class="nav-item" id="li-relate-items">
                <a class="nav-link" id="pills-related-items-tab" data-bs-toggle="pill" href="#pills-related-items" role="tab" aria-controls="pills-related-items" aria-selected="false">
                  Related Items
                </a>
              </li>
            </ul>
            <div class="tab-content" id="pills-tabContent">
              <div class="tab-pane fade show active" id="pills-profile" role="tabpanel" aria-labelledby="pills-profile-tab">
                <Community
                    v-if="isCommunity"  
                    :species_community="species_community" 
                    id="speciesInformation" 
                    ref="community_information" 
                    :is_external="is_external">
                </Community>
                <Species
                    v-else
                    :species_community="species_community" 
                    id="speciesInformation" 
                    ref="species_information" 
                    :is_external="is_external">
                </Species>
              </div>
              <div class="tab-pane fade" id="pills-documents" role="tabpanel" aria-labelledby="pills-documents-tab">
                <Documents 
                    :species_community="species_community" 
                    id="speciesDocuments" 
                    ref="documents" 
                    :is_external="is_external">
                </Documents>
              </div>
              <div class="tab-pane fade" id="pills-threats" role="tabpanel" aria-labelledby="pills-threats-tab">
                <Threats 
                    :species_community="species_community" 
                    id="speciesThreats" 
                    ref="threats" 
                    :is_external="is_external">
                </Threats>
              </div>
              <div class="tab-pane fade" id="pills-conservation-plans" role="tabpanel" aria-labelledby="pills-conservation-plans-tab">
                <ConservationPlans 
                    :species_community="species_community" 
                    id="speciesConservationPlans" 
                    ref="conservation_plans">
                </ConservationPlans>
              </div>
              <div class="tab-pane fade" id="pills-related-items" role="tabpanel" aria-labelledby="pills-related-items-tab">
                <RelatedItems 
                    :species_community="species_community" 
                    id="speciesRelatedItems">
                </RelatedItems>
              </div>
            </div>
        </div>
    </div>
</template>

<script>
    import Species from '@/components/common/species_communities/species_profile.vue'
    import Community from '@/components/common/species_communities/community_profile.vue'
    import Documents from '@/components/common/species_communities/documents.vue'
    import Threats from '@/components/common/species_communities/threats.vue'
    import ConservationPlans from '@/components/common/species_communities/conservation_plans.vue'
    import RelatedItems from '@/components/common/species_communities/related_items.vue'

    export default {
        props:{
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
            return{
                values:null,
            }
        },
        components: {
            Species,
            Community,
            Documents,
            Threats,
            ConservationPlans,
            RelatedItems,
        },
        computed:{
            isCommunity: function(){
                return this.species_community.group_type == "community"
            },

        },
        methods:{
            set_tabs:function(){
                let vm = this;

                /* set Applicant tab Active */
                //$('#pills-tab a[href="#pills-profile"]').tab('show');
            },
            eventListener: function(){
              let vm=this;
            },

        },
        mounted: function() {
            let vm = this;
            vm.set_tabs();
            vm.form = document.forms.new_species;
            vm.eventListener();
            //window.addEventListener('beforeunload', vm.leaving);
            //indow.addEventListener('onblur', vm.leaving);

        }
 
    }
</script>

<style lang="css" scoped>
    .section{
        text-transform: capitalize;
    }
    .list-group{
        margin-bottom: 0;
    }
    .fixed-top{
        position: fixed;
        top:56px;
    }

    .nav-item {
        margin-bottom: 2px;
    }

    .nav-item>li>a {
        background-color: yellow !important;
        color: #fff;
    }

    .nav-item>li.active>a, .nav-item>li.active>a:hover, .nav-item>li.active>a:focus {
      color: white;
      background-color: blue;
      border: 1px solid #888888;
    }

        .admin > div {
          display: inline-block;
          vertical-align: top;
          margin-right: 1em;
        }
    .nav-pills .nav-link {
        border-bottom-left-radius: 0;
        border-bottom-right-radius: 0;
        border-top-left-radius: 0.5em;
        border-top-right-radius: 0.5em;
        margin-right: 0.25em;
    }
    .nav-pills .nav-link {
        background: lightgray;
    }
    .nav-pills .nav-link.active {
        background: gray;
    }
</style>

