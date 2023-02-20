<template>
    <div>

        {{ species_name }} in a child component.

    </div>
</template>
  
  <script>

    export default {
        props:{
            species_name: {
                type: String,
                required: true
            },
        },
        data() { 
            return {

            }
        },
        components:{
        },
        methods: {

        }
    }; 
  </script> 
  
  <style>

  </style>
  