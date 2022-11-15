<template lang="html">
    <div>
        <div class="col-md-12">

            <ul v-if="is_internal" class="nav nav-pills mb-3" id="pills-tab" role="tablist">
              <li class="nav-item">
                <a 
                    class="nav-link" 
                    id="pills-status-tab" 
                    data-bs-toggle="pill" 
                    href="#pills-status" 
                    role="tab" 
                    aria-controls="pills-status" 
                    aria-selected="true">
                  Status
                </a>
              </li>
              <!-- <li class="nav-item">
                <a 
                    class="nav-link" 
                    id="pills-documents-tab" 
                    data-bs-toggle="pill" 
                    href="#pills-documents" 
                    role="tab" 
                    aria-controls="pills-documents" 
                    aria-selected="false"
                    @click="tabClicked()">
                  Documents
                </a>
              </li>
              <li class="nav-item">
                <a 
                    class="nav-link" 
                    id="pills-threats-tab" 
                    data-bs-toggle="pill" 
                    href="#pills-threats" 
                    role="tab" 
                    aria-controls="pills-threats" 
                    aria-selected="false"
                    @click="tabClicked()">
                  Threats
                </a>
              </li>
              <li class="nav-item">
                <a 
                    class="nav-link" 
                    id="pills-related-items-tab" 
                    data-bs-toggle="pill" 
                    href="#pills-related-items" 
                    role="tab" 
                    aria-controls="pills-related-items" 
                    aria-selected="false">
                  Related Items
                </a>
              </li> -->
            </ul>
            <div class="tab-content" id="pills-tabContent">
              <div class="tab-pane fade show active" id="pills-status" role="tabpanel" aria-labelledby="pills-status-tab">
                <CommunityStatus
                    v-if="isCommunity"  
                    ref="community_conservation_status" 
                    id="communityStatus" 
                    :is_external="is_external"
                    :canEditStatus="canEditStatus"
                    :conservation_status_obj="conservation_status_obj"
                    :referral="referral">
                </CommunityStatus>
                <SpeciesStatus
                    v-else
                    ref="species_conservation_status" 
                    id="speciesStatus" 
                    :is_external="is_external"
                    :canEditStatus="canEditStatus"
                    :conservation_status_obj="conservation_status_obj"
                    :referral="referral">
                </SpeciesStatus>
              </div>
              <!-- <div class="tab-pane fade" id="pills-documents" role="tabpanel" aria-labelledby="pills-documents-tab">
                <CommunityDocuments 
                    v-if="isCommunity"
                    :key="reloadcount"
                    ref="community_documents" 
                    id="communityDocuments" 
                    :is_internal="is_internal"
                    :species_community="species_community">
                </CommunityDocuments>
                <SpeciesDocuments 
                    v-else 
                    :key="reloadcount"
                    ref="species_documents" 
                    id="speciesDocuments" 
                    :is_internal="is_internal"
                    :species_community="species_community">
                </SpeciesDocuments>
              </div>
              <div class="tab-pane fade" id="pills-threats" role="tabpanel" aria-labelledby="pills-threats-tab">
                <CommunityThreats 
                    v-if="isCommunity"
                    :key="reloadcount"
                    ref="community_threats" 
                    id="communityThreats" 
                    :is_internal="is_internal"
                    :species_community="species_community">
                </CommunityThreats>
                <SpeciesThreats
                    v-else 
                    :key="reloadcount"
                    ref="species_threats" 
                    id="speciesThreats" 
                    :is_internal="is_internal"
                    :species_community="species_community">
                </SpeciesThreats>
              </div>
              <div class="tab-pane fade" id="pills-related-items" role="tabpanel" 
                aria-labelledby="pills-related-items-tab">
                <RelatedItems 
                    ref="species_related_items" 
                    id="speciesRelatedItems"
                    :is_internal="is_internal"
                    :species_community="species_community">
                </RelatedItems>
              </div> -->
            </div>
        </div>
    </div>
</template>

<script>
    import SpeciesStatus from '@/components/common/conservation_status/species_status.vue'
    import CommunityStatus from '@/components/common/conservation_status/community_status.vue'
    /*import SpeciesDocuments from '@/components/common/species_communities/documents.vue'
    import CommunityDocuments from '@/components/common/species_communities/community_documents.vue'
    import SpeciesThreats from '@/components/common/species_communities/species_threats.vue'
    import CommunityThreats from '@/components/common/species_communities/community_threats.vue'
    import RelatedItems from '@/components/common/species_communities/related_items.vue'*/

    export default {
        props:{
            conservation_status_obj:{
                type: Object,
                required:true
            },
            referral:{
                type: Object,
                required:false
            },
            is_external:{
              type: Boolean,
              default: false
            },
            is_internal:{
              type: Boolean,
              default: false
            },
            canEditStatus:{
              type: Boolean,
              default: true
            },
        },
        data:function () {
            return{
                values:null,
                reloadcount:0,
            }
        },
        components: {
            SpeciesStatus,
            CommunityStatus,
            /*SpeciesDocuments,
            CommunityDocuments,
            SpeciesThreats,
            CommunityThreats,
            RelatedItems,*/
        },
        computed:{
            isCommunity: function(){
                return this.conservation_status_obj.group_type == "community"
            },

        },
        methods:{
            //----function to resolve datatable exceeding beyond the div
            tabClicked: function(param){
                this.reloadcount = this.reloadcount+1;
            },
            eventListener: function(){
              let vm=this;
            },

        },
        mounted: function() {
            let vm = this;
            //vm.set_tabs();
            vm.form = document.forms.new_conservation_status;
            vm.eventListener();
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

