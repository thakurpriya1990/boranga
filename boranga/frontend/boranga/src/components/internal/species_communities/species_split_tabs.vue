<template>
    <div>

        <ul class="nav nav-tabs">

            <li v-for="(species, index) in new_species_list" :key="'li' + species.id" class="nav-item" role="tablist">
                <button :class="0==index ? 'nav-link':'nav-link'" aria-current="page" href="#" data-bs-toggle="tab" :data-bs-target="'#nav-' + index" role="tab">{{ species.name }} Test</button>
            </li>

        </ul>

        <div class="tab-content" id="nav-tabContent">

            <div v-for="(species, index) in new_species_list" :key="'div' + species.id" :class="0==index ? 'active show':''" class="tab-pane fade" :id="'nav-' + index" role="tabpanel" :aria-labelledby="'nav-' + index + '-tab'">
                <SpeciesSplitTabsChildComponent :species_name="species.name" :key="'child'+ index"/>
            </div>

        </div>

    </div>
</template>
  
  <script>
    import SpeciesSplitTabsChildComponent from '@/components/internal/species_communities/species_split_tabs_child_component.vue'

    export default {
        props:{
            new_species_list: {
                type: Array,
                required: true
            },
        },
        data() { 
            return {

            }
        },
        components:{
            SpeciesSplitTabsChildComponent,
        },
        methods: {

        }
    }; 
  </script> 
  
  <style>

  </style>
  