<template lang="html">
<div class="row" id="userInfo">
    <div class="col-sm-12">
        <div class="panel panel-default">
            <div class="panel-heading">
                <h3 class="panel-title">Conservation Plans <small></small>
                <a class="panelClicker" :href="'#'+lBody" data-toggle="collapse"  data-parent="#userInfo" expanded="true" :aria-controls="lBody">
                <span class="glyphicon glyphicon-chevron-up pull-right "></span>
                </a>
                </h3>
            </div>
            <div class="panel-body collapse in" :id="lBody">
                <div class="" >                        
                    <div class="form-horizontal col-sm-12 borderDecoration">
                        
                        <div class="form-group">
                            <div class="row">
                                <div class="col-sm-3">
                                    <label class="control-label pull-left"  for="Name">Some conservation plan data</label>
                                </div>
                                <div class="col-sm-9" style="margin-bottom: 5px; width:53% !important">
                                    <input type="text" class="form-control" name="Some species data" placeholder="" :disabled="species_community.readonly">
                                </div>
                            </div>
                        </div> 
                    </div>
                </div>
            </div>                
        </div>
    </div>

</div>
</template>

<script>
import Vue from 'vue' 
import {
  api_endpoints,
  helpers
}
from '@/utils/hooks'
export default {
        props:{
            species_community:{
                type: Object,
                required:true
            }
        },
        data:function () {
            let vm = this;
            return{
                pBody: 'pBody'+vm._uid,
                lBody: 'lBody'+vm._uid,
                iBody: 'iBody'+vm._uid,
                mBody: 'mBody'+vm._uid,
                oBody: 'oBody'+vm._uid,
                cBody: 'cBody'+vm._uid,
                dBody: 'dBody'+vm._uid,
                values:null,
                datepickerOptions:{
                    format: 'DD/MM/YYYY',
                    showClear:true,
                    useCurrent:false,
                    keepInvalid:true,
                    allowInputToggle:true,
                },
            }
        },
        components: {
        },
        computed: {
        },
        watch:{
            
        },
        methods:{
            eventListeners:function (){
                let vm=this;

                var date= new Date()
                var today= new Date(date.getFullYear(), date.getMonth(), date.getDate());

            },
        },
        mounted: function(){
            let vm = this;
        }
    }
</script>

<style lang="css" scoped>
    /*ul, li {
        zoom:1;
        display: inline;
    }*/
    fieldset.scheduler-border {
    border: 1px groove #ddd !important;
    padding: 0 1.4em 1.4em 1.4em !important;
    margin: 0 0 1.5em 0 !important;
    -webkit-box-shadow:  0px 0px 0px 0px #000;
            box-shadow:  0px 0px 0px 0px #000;
    }
    legend.scheduler-border {
    width:inherit; /* Or auto */
    padding:0 10px; /* To give a bit of padding on the left and right */
    border-bottom:none;
    }
</style>

