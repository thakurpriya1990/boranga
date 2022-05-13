<template lang="html">
    <div>
        <div class="col-md-12">

            <ul class="nav nav-pills mb-3" id="pills-tab" role="tablist">
              <li class="nav-item">
                <a class="nav-link" id="pills-species-tab" data-bs-toggle="pill" href="#pills-species" role="tab" aria-controls="pills-species" aria-selected="true">
                  {{ species_community_label }}
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
              <div class="tab-pane fade show active" id="pills-species" role="tabpanel" aria-labelledby="pills-species-tab">
                <Community
                    v-if="isCommunity"  
                    :proposal="proposal" 
                    :species_community="species_community" 
                    id="speciesInformation" 
                    :canEditActivities="canEditActivities" 
                    ref="community_information" 
                    :is_external="is_external">
                </Community>
                <Species
                    v-else
                    :proposal="proposal" 
                    :species_community="species_community" 
                    id="speciesInformation" 
                    :canEditActivities="canEditActivities" 
                    ref="species_information" 
                    :is_external="is_external">
                </Species>
              </div>
              <div class="tab-pane fade" id="pills-documents" role="tabpanel" aria-labelledby="pills-documents-tab">
                <Documents 
                    :proposal="proposal" 
                    :species_community="species_community" 
                    id="speciesDocuments" 
                    :canEditActivities="canEditActivities" 
                    ref="documents" 
                    :is_external="is_external">
                </Documents>
              </div>
              <div class="tab-pane fade" id="pills-threats" role="tabpanel" aria-labelledby="pills-threats-tab">
                <Threats 
                    :proposal="proposal" 
                    :species_community="species_community" 
                    id="speciesThreats" 
                    :canEditActivities="canEditActivities" 
                    ref="threats" 
                    :is_external="is_external">
                </Threats>
              </div>
              <div class="tab-pane fade" id="pills-conservation-plans" role="tabpanel" aria-labelledby="pills-conservation-plans-tab">
                <ConservationPlans 
                    :proposal="proposal" 
                    :species_community="species_community" 
                    id="speciesConservationPlans" 
                    ref="conservation_plans">
                </ConservationPlans>
              </div>
              <div class="tab-pane fade" id="pills-related-items" role="tabpanel" aria-labelledby="pills-related-items-tab">
                <RelatedItems 
                    :proposal="proposal" 
                    :species_community="species_community" 
                    id="speciesRelatedItems">
                </RelatedItems>
              </div>
            </div>
        </div>
    </div>
</template>

<script>
    import Species from '@/components/common/species_communities/species.vue'
    import Community from '@/components/common/species_communities/community.vue'
    import Documents from '@/components/common/species_communities/documents.vue'
    import Threats from '@/components/common/species_communities/threats.vue'
    import ConservationPlans from '@/components/common/species_communities/conservation_plans.vue'
    import RelatedItems from '@/components/common/species_communities/related_items.vue'

    export default {
        props:{
            proposal:{
                type: Object,
                required:true
            },
            species_community:{
                type: Object,
                required:true
            },
            canEditActivities:{
              type: Boolean,
              default: true
            },
            is_external:{
              type: Boolean,
              default: false
            },
            is_internal:{
              type: Boolean,
              default: false
            },
            is_referral:{
              type: Boolean,
              default: false
            },
            hasReferralMode:{
                type:Boolean,
                default: false
            },
            hasAssessorMode:{
                type:Boolean,
                default: false
            },
            referral:{
                type: Object,
                required:false
            },
            proposal_parks:{
                type:Object,
                default:null
            },
        },
        data:function () {
            return{
                values:null,
                species_community_label: this.species_community.group_type === "community" ? "Community" : "Species",
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
            applicantType: function(){
                return this.proposal.applicant_type;
            },
            isCommunity: function(){
                return this.species_community.group_type == "community"
            },

        },
        methods:{
            set_tabs:function(){
                let vm = this;

                /* set Applicant tab Active */
                //$('#pills-tab a[href="#pills-species"]').tab('show');
            },
            eventListener: function(){
              let vm=this;
              $('a[href="#pills-activities-land"]').on('shown.bs.tab', function (e) {
                vm.$refs.activities_land.$refs.vehicles_table.$refs.vehicle_datatable.vmDataTable.columns.adjust().responsive.recalc();
              });
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

