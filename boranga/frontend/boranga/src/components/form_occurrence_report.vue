<template lang="html">
    <div>
        <div class="col-md-12">

            <ul class="nav nav-pills mb-3" id="pills-tab" role="tablist">
              <li class="nav-item">
                <a 
                    class="nav-link" 
                    id="pills-location-tab" 
                    data-bs-toggle="pill" 
                    :href="'#' + locationBody"
                    role="tab" 
                    :aria-controls="locationBody" 
                    aria-selected="true"
                    @click="tabClicked()">
                  Location
                </a>
              </li>
              <li class="nav-item">
                <a 
                    class="nav-link" 
                    id="pills-habitat-tab" 
                    data-bs-toggle="pill" 
                    :href="'#' + habitatBody" 
                    role="tab" 
                    :aria-selected="habitatBody" 
                    aria-selected="false"
                    @click="tabClicked()">
                  Habitat
                </a>
              </li>
              <li class="nav-item">
                <a 
                    class="nav-link" 
                    id="pills-observation-tab" 
                    data-bs-toggle="pill" 
                    :href="'#' + observationBody" 
                    role="tab" 
                    :aria-selected="observationBody" 
                    aria-selected="false"
                    @click="tabClicked()">
                  Observation
                </a>
              </li>
              <!-- <li class="nav-item">
                <a 
                  class="nav-link" 
                  id="pills-related-items-tab" 
                  data-bs-toggle="pill" 
                  :href="'#' + relatedItemBody" 
                  role="tab" 
                  :aria-controls="relatedItemBody" 
                  aria-selected="false"
                  @click="tabClicked()">
                  Related Items
                </a>
              </li> -->
            </ul>
            <div class="tab-content" id="pills-tabContent">
              <div class="tab-pane fade show active" :id="locationBody" role="tabpanel" aria-labelledby="pills-location-tab">
                <OCRLocation
                    :key="reloadcount"
                    ref="ocr_location" 
                    id="ocrLocation" 
                    :is_external="is_external"
                    :canEditStatus="canEditStatus"
                    :occurrence_report_obj="occurrence_report_obj"
                    :referral="referral">
                </OCRLocation>
              </div>
              <div class="tab-pane fade" :id="habitatBody" role="tabpanel" aria-labelledby="pills-habitat-tab">
                <OCRHabitat
                    :key="reloadcount"
                    ref="ocr_habitat" 
                    id="ocrhabitat" 
                    :is_internal="is_internal"
                    :occurrence_report_obj="occurrence_report_obj">
                </OCRHabitat>
              </div>
              <div class="tab-pane fade" :id="observationBody" role="tabpanel" aria-labelledby="pills-observation-tab">
                <OCRObservation
                    :key="reloadcount"
                    ref="ocr_observation" 
                    id="ocrObservation" 
                    :is_internal="is_internal"
                    :occurrence_report_obj="occurrence_report_obj">
                </OCRObservation>
              </div>
              <!-- <div class="tab-pane fade" :id="relatedItemBody" role="tabpanel" aria-labelledby="pills-related-items-tab">
                <RelatedItems
                    :key="reloadcount" 
                    ref="cs_related_items" 
                    id="csRelatedItems" 
                    :ajax_url="related_items_ajax_url"
                    :filter_list_url="related_items_filter_list_url">
                </RelatedItems>
              </div> -->
            </div>
        </div>
    </div>
</template>

<script>
    import OCRLocation from '@/components/common/occurrence/ocr_location.vue'
    // import CommunityStatus from '@/components/common/conservation_status/community_status.vue'
    import OCRHabitat from '@/components/common/occurrence/ocr_habitat.vue'
    import OCRObservation from '@/components/common/occurrence/ocr_observation.vue'
    // import OCRHabitat from '@/components/common/conservation_status/cs_documents.vue'
    // import RelatedItems from '@/components/common/table_related_items.vue'
    
    export default {
        props:{
            occurrence_report_obj:{
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
            let vm = this;
            return{
                values:null,
                reloadcount:0,
                locationBody: 'locationBody' + vm._uid,
                habitatBody: 'habitatBody' + vm._uid,
                observationBody: 'observationBody' + vm._uid,
                documentBody: 'documentBody' + vm._uid,
                relatedItemBody: 'relatedItemBody' + vm._uid,
            }
        },
        components: {
            OCRLocation,
            OCRHabitat,
            OCRObservation,
            // CommunityStatus,
            // CSDocuments,
            // RelatedItems,
        },
        computed:{
            isCommunity: function(){
                return this.occurrence_report_obj.group_type == "community"
            },
            related_items_ajax_url: function(){
              return '/api/conservation_status/' + this.occurrence_report_obj.id + '/get_related_items/'
            },
            related_items_filter_list_url: function(){
              return '/api/conservation_status/filter_list.json'
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
            vm.form = document.forms.new_occurrence_report;
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

