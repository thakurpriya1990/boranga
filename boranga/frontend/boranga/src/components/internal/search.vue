<template>
<div class="container" id="internalSearch">
    <div class="row">
        <div class="col-sm-12">
            <div class="panel panel-default">
                <div class="panel-heading">
                    <h3 class="panel-title">Search Organisations
                        <a :href="'#'+oBody" data-toggle="collapse"  data-parent="#userInfo" expanded="true" :aria-controls="oBody">
                            <span class="glyphicon glyphicon-chevron-up pull-right "></span>
                        </a>
                    </h3>
                </div>
                <div class="panel-body collapse in" :id="oBody">
                    <div class="row">
                        <form name="searchOrganisationForm">
                            <div class="col-md-4">
                                <div class="form-group">
                                    <label class="control-label" for="Organisation">Search Organisation</label>

                                    <TextFilteredOrgField :url="filtered_org_url" name="Organisation" id="id_org"/>
                                </div>
                            </div>
                            <div class="col-md-12 text-center">
                                <input type="button" @click.prevent="viewOrgDetails" class="btn btn-primary" style="margin-bottom: 5px" value="View Details"/>
                            </div>
                        </form>
                    </div>
                </div>
            </div>
        </div>
    </div>
    <div class="row">
        <div class="col-sm-12">
            <div class="panel panel-default">
                <div class="panel-heading">
                    <h3 class="panel-title">Search User
                        <a :href="'#'+uBody" data-toggle="collapse"  data-parent="#userInfo" expanded="true" :aria-controls="uBody">
                            <span class="glyphicon glyphicon-chevron-up pull-right "></span>
                        </a>
                    </h3>
                </div>
                <div class="panel-body collapse in" :id="uBody">
                    <div class="row">
                        <form name="searchUserForm">
                          <div class="">
                            <div class="col-md-4">
                                <div class="form-group">
                                    <label class="control-label" for="User">Search User</label>

                                    <TextFilteredField :url="filtered_url" name="User" id="id_holder"/>
                                </div>
                            </div>
                            <div class="">
                              <div class="col-md-12 text-center">
                                <div >
                                  <input type="button" @click.prevent="viewUserDetails" class="btn btn-primary" style="margin-bottom: 5px" value="View Details"/>
                                </div>
                              </div>
                            </div>
                          </div>
                        </form>
                    </div>
                </div>
            </div>
        </div>
    </div>
    <div class="row">
        <div class="col-sm-12">
            <div class="panel panel-default">
                <div class="panel-heading">
                    <h3 class="panel-title">Search Keywords
                        <a :href="'#'+kBody" data-toggle="collapse"  data-parent="#userInfo" expanded="true" :aria-controls="kBody">
                            <span class="glyphicon glyphicon-chevron-up pull-right "></span>
                        </a>
                    </h3>
                </div>
                <div class="panel-body collapse in" :id="kBody">
                    <div class="row">
                      <div>
                            <div class="form-group">
                              <label for="" class="control-label col-lg-12">Filter</label>
                              <div class="form-check form-check-inline col-md-3">
                                  <input  class="form-check-input" ref="searchProposal" id="searchProposal" name="searchProposal" type="checkbox" v-model="searchProposal" />
                                  <label class="form-check-label" for="searchProposal">Application</label>

                              </div>
                              <div class="form-check form-check-inline col-md-3">
                                  <input  class="form-check-input" ref="searchApproval" id="searchApproval" name="searchApproval" type="checkbox" v-model="searchApproval" />
                                  <label class="form-check-label" for="searchApproval">Licence</label>
                              </div>
                              <div class="form-check form-check-inline col-md-3">
                                  <input  class="form-check-input" ref="searchCompliance" id="searchCompliance" name="searchCompliance" type="checkbox" v-model="searchCompliance" />
                                  <label class="form-check-label" for="searchCompliance">Compliance with requirements</label>
                              </div>
                              <label for="" class="control-label col-lg-12">Keyword</label>
                                <div class="col-md-8">
                                  <input type="search"  class="form-control input-sm" name="details" placeholder="" v-model="keyWord"></input>
                                </div>
                                <div class="col-md-1">
                                </div>
                                <div class="col-md-3">
                                  <input type="button" @click.prevent="add" class="btn btn-primary" value="Add"/>
                                </div>
                            </div>

                      </div>

                    </div>

                    <div class="row">
                      <div class="col-lg-12">
                          <ul class="list-inline" style="display: inline; width: auto;">
                              <li class="list-inline-item" v-for="(item,i) in searchKeywords">
                                <button @click.prevent="" class="btn btn-light" style="margin-top:5px; margin-bottom: 5px">{{item}}</button><a href="" @click.prevent="removeKeyword(i)"><span class="glyphicon glyphicon-remove "></span></a>
                              </li>
                          </ul>
                      </div>
                    </div>

                    <div class="row">
                      <div class="col-lg-12">
                        <div >
                          <input type="button" @click.prevent="search" class="btn btn-primary" style="margin-bottom: 5px"value="Search"/>
                          <input type="reset" @click.prevent="reset" class="btn btn-primary" style="margin-bottom: 5px"value="Clear"/>

                        </div>
                      </div>
                    </div>
                    <div class="row">
                    <div class="col-lg-12">
                        <alert :show.sync="showMessage" type="danger"><strong><p v-html="messageString"></p></strong></alert>
                    </div>
                    </div>

                    <div class="row">
                    <div class="col-lg-12">
                        <datatable ref="proposal_datatable" :id="datatable_id" :dtOptions="proposal_options"  :dtHeaders="proposal_headers"/>
                    </div>
                    </div>
                </div>
            </div>
        </div>
    </div>
    <div class="row">
        <div class="col-sm-12">
            <div class="panel panel-default">
                <div class="panel-heading">
                    <h3 class="panel-title">Search Reference Number
                        <a :href="'#'+rBody" data-toggle="collapse"  data-parent="#userInfo" expanded="true" :aria-controls="rBody">
                            <span class="glyphicon glyphicon-chevron-up pull-right "></span>
                        </a>
                    </h3>
                </div>
                <div class="panel-body collapse in" :id="rBody">
                    <div class="row">
                       <label for="" class="control-label col-lg-12">Reference</label>
                          <div class="col-md-8">
                              <input type="search"  class="form-control input-sm" name="referenceWord" placeholder="" v-model="referenceWord"></input>
                          </div>
                          <div >
                            <input type="button" @click.prevent="search_reference" class="btn btn-primary" style="margin-bottom: 5px" value="Search"/>
                        </div>
                        <alert :show.sync="showError" type="danger"><strong>{{errorString}}</strong></alert>
                    </div>
                </div>
            </div>
        </div>
    </div>
</div>
</template>
<script>
import $ from 'jquery'
import datatable from '@/utils/vue/datatable.vue'
import TextFilteredField from '@/components/forms/text-filtered.vue'
import TextFilteredOrgField from '@/components/forms/text-filtered-org.vue'
import {
  api_endpoints,
  constants,
  helpers
}
from '@/utils/hooks'
import utils from './utils'
export default {
  name: 'ExternalDashboard',
  props: {

  },
  data() {
    let vm = this;
    return {
      rBody: 'rBody' + vm._uid,
      oBody: 'oBody' + vm._uid,
      uBody: 'uBody' + vm._uid,
      kBody: 'kBody' + vm._uid,
      loading: [],
      filtered_url: api_endpoints.filtered_users + '?search=',
      filtered_org_url: api_endpoints.filtered_organisations + '?search=',
      user_id:null,
      searchKeywords: [],
      searchProposal: true,
      searchApproval: false,
      searchCompliance: false,
      referenceWord: '',
      keyWord: null,
      selected_organisation:'',
      organisations: null,
      results: [],
      errors: false,
      errorString: '',
      messages: false,
      messageString:'',
      datatable_id: 'proposal-datatable-'+vm._uid,
      proposal_headers:["Number","Type","Proponent","Text found","Action"],
      proposal_options:{
          language: {
              processing: constants.DATATABLE_PROCESSING_HTML
          },
          responsive: true,
          /*ajax: {
              "url": 'api/empty_list',
              "dataSrc": ''
          },*/
          data: vm.results,
          columns: [
              {data: "number"},
              {data:"type"},
              {data: "applicant"},
              {//data: "text.value"
                data: "text",
                mRender: function (data,type,full) {
                  if(data.value){
                    return data.value;
                  }
                  else
                  {
                    return data;
                  }
                }
              },
              {
                data: "id",
                  mRender:function (data,type,full) {
                        let links = '';
                        if(full.type == 'Proposal' || full.type == 'Application'){
                          links +=  `<a href='/internal/proposal/${full.id}'>View</a><br/>`;
                        }
                        if(full.type == 'Compliance'){
                          links +=  `<a href='/internal/compliance/${full.id}'>View</a><br/>`;
                        }
                        if(full.type == 'Approval' || full.type == 'Licence'){
                          links +=  `<a href='/internal/approval/${full.id}'>View</a><br/>`;
                        }
                        return links;
                  }
              }
          ],
          processing: true,
      }
    }

  },
    watch: {

    },
    components: {
        datatable,
        TextFilteredField,
        TextFilteredOrgField,
    },
//    beforeRouteEnter:function(to,from,next){
//        utils.fetchOrganisations().then((response)=>{
//            next(vm => {
//                vm.organisations = response;
//            });
//        },
//        (error) =>{
//            console.log(error);
//        });
//    },
    computed: {
        showError: function() {
            var vm = this;
            return vm.errors;
        },
        showMessage: function() {
            var vm = this;
            return vm.messages;
        }
    },
    methods: {
        addListeners: function(){
            let vm = this;
            // Initialise select2 for region
            $(vm.$refs.searchOrg).select2({
                "theme": "bootstrap",
                allowClear: true,
                placeholder:"Select Organisation"
            }).
            on("select2:select",function (e) {
                var selected = $(e.currentTarget);
                vm.selected_organisation = selected.val();
            }).
            on("select2:unselect",function (e) {
                var selected = $(e.currentTarget);
                vm.selected_organisation = selected.val();
            });
        },
        viewOrgDetails: function(){
          let vm=this;
          let form=document.forms.searchOrganisationForm
          var org_selected=form.elements['Organisation-selected']
          if(org_selected!=undefined || org_selected!=null){
            var org_id= org_selected.value;
            vm.$router.push({
              name:"internal-org-detail",
              params:{org_id:org_id}
            });
          }
          else{
            swal({
                    title: 'Organisation not selected',
                    html: 'Please select the organisation to view the details',
                    type: 'error'
                }).then(() => {

                });
                return;
          }
        },
        viewUserDetails: function(){
          let vm=this;
          let form=document.forms.searchUserForm
          var user_selected=form.elements['User-selected']
          if(user_selected!=undefined || user_selected!=null){
            var user_id= user_selected.value;
            vm.$router.push({
              name:"internal-user-detail",
              params:{user_id:user_id}
            });
          }
          else{
            swal({
                    title: 'User not selected',
                    html: 'Please select the user to view the details',
                    type: 'error'
                }).then(() => {

                });
                return;
          }
        },

        add: function() {
          let vm = this;
          if(vm.keyWord != null)
          {
            vm.searchKeywords.push(vm.keyWord);
          }
        },
        removeKeyword: function(index) {
          let vm = this;
          if(index >-1)
          {
            vm.searchKeywords.splice(index,1);
          }
        },
        reset: function() {
          let vm = this;
          if(vm.keyWord != null)
          {
            vm.searchKeywords = [];
          }
          /*vm.searchProposal = false;
          vm.searchApproval = false;
          vm.searchCompliance = false; */
          vm.keyWord = null;
          vm.results = [];
          vm.messages=false;
          vm.messageString='';
          vm.$refs.proposal_datatable.vmDataTable.clear()
          vm.$refs.proposal_datatable.vmDataTable.draw();
        },

        search: function() {
          let vm = this;
          if(this.searchKeywords.length > 0)
          { vm.messages=true;
            vm.messageString="Searching <i class='fa fa-2x fa-spinner fa-spin'></i>";
            vm.$http.post('/api/search_keywords.json',{
              searchKeywords: vm.searchKeywords,
              searchProposal: vm.searchProposal,
              searchApproval: vm.searchApproval,
              searchCompliance: vm.searchCompliance,
              is_internal: true,
            }).then(res => {
              vm.results = res.body;
              vm.$refs.proposal_datatable.vmDataTable.clear()
              vm.$refs.proposal_datatable.vmDataTable.rows.add(vm.results);
              vm.$refs.proposal_datatable.vmDataTable.draw();
              vm.message=false;
              vm.messageString='';
            },
            err => {
              console.log(err);
            });
          }

        },


    search_reference: function() {
          let vm = this;
          if(vm.referenceWord)
          {
            vm.$http.post('/api/search_reference.json',{
              reference_number: vm.referenceWord,

            }).then(res => {
              console.log(res)
              vm.errors = false;
              vm.errorString = '';
              vm.$router.push({ path: '/internal/'+res.body.type+'/'+res.body.id });
              },
            error => {
              console.log(error);
              vm.errors = true;
              vm.errorString = helpers.apiVueResourceError(error);
            });
          }

        },
    },
    mounted: function () {
        let vm = this;
        vm.proposal_options.data = vm.results;
        //vm.proposal_options.processing=true;
        vm.$refs.proposal_datatable.vmDataTable.draw();
        $( 'a[data-toggle="collapse"]' ).on( 'click', function () {
            var chev = $( this ).children()[ 0 ];
            window.setTimeout( function () {
                $( chev ).toggleClass( "glyphicon-chevron-down glyphicon-chevron-up" );
            }, 100 );
        } );
    },
    updated: function(){
        let vm = this;
        this.$nextTick(() => {
            vm.addListeners();
        });

    }
}
</script>
