<template>
    <div>
        <a @click="addSpecies" href="javascript: void(0)">Add Species</a> | <a @click="removeSpecies" href="javascript: void(0)">Remove Species</a>
        <SpeciesCommunitiesTabs :new_species_list="new_species_list" />
    </div>
</template>
  
  <script>
    import SpeciesCommunitiesTabs from '@/components/internal/species_communities/species_split_tabs.vue'

    export default {
        props:{

        },
        data() { 
            return {
                new_species_list: [
                    {
                        id: 0,
                        name: 'Species 1',
                    },
                    {
                        id: 1,
                        name: 'Species 2',
                    },
                    {
                        id: 2,
                        name: 'Species 3',
                    },
                    {
                        id: 3,
                        name: 'Species 4',
                    },                    
                ]
            }
        },
        components:{
            SpeciesCommunitiesTabs,
        },
        methods: {
            addSpecies: function() {
                this.new_species_list.push({
                    id: this.new_species_list.length,
                    name: 'Species ' + this.new_species_list.length,
                })
            },
            removeSpecies: function() {
                this.new_species_list.pop()
            },
        }
    }; 
  </script> 
  
  <style>

  </style>
  