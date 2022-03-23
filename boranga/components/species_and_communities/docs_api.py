import json
import traceback
from urllib import request
from django.views.decorators.http import require_http_methods

from django.http import HttpResponse
from rest_framework import viewsets
from rest_framework.decorators import action as list_route
from rest_framework.decorators import action as detail_route
from rest_framework_datatables.pagination import DatatablesPageNumberPagination
from ledger_api_client.settings_base import TIME_ZONE
from rest_framework_datatables.renderers import DatatablesRenderer
from boranga.components.species_and_communities.docs_serializers import SpeciesDocumentsSerializer
from boranga.components.species_and_communities.models import Species, SpeciesDocument
from rest_framework_datatables.filters import DatatablesFilterBackend
import logging

logger = logging.getLogger(__name__)


class SpeciesDocumentsFilterBackend(DatatablesFilterBackend):
    def filter_queryset(self, request, queryset, view):
        total_count = queryset.count()
        
        species_id = request.GET.get('species_id')
        if species_id:
            queryset = queryset.filter(species_id=species_id)

        getter = request.query_params.get
        fields = self.get_fields(getter)
        ordering = self.get_ordering(getter, fields)
        queryset = queryset.order_by(*ordering)
        if len(ordering):
            queryset = queryset.order_by(*ordering)

        queryset = super(SpeciesDocumentsFilterBackend, self).filter_queryset(request, queryset, view)
        setattr(view, '_datatables_total_count', total_count)
        return queryset

class SpeciesDocumentsRenderer(DatatablesRenderer):
    def render(self, data, accepted_media_type=None, renderer_context=None):
        if 'view' in renderer_context and hasattr(renderer_context['view'], '_datatables_total_count'):
            data['recordsTotal'] = renderer_context['view']._datatables_total_count
        rendered_data = super(SpeciesDocumentsRenderer, self).render(data, accepted_media_type, renderer_context)
        return rendered_data


class SpeciesDocumentsViewSet(viewsets.ModelViewSet):
    filter_backends = (SpeciesDocumentsFilterBackend,)
    pagination_class = DatatablesPageNumberPagination
    renderer_classes = (SpeciesDocumentsRenderer,)
    queryset = SpeciesDocument.objects.none()
    serializer_class = SpeciesDocumentsSerializer
    page_size = 10

    def get_queryset(self):
        qs = SpeciesDocument.objects.all()
        return qs

    @list_route(methods=['GET',], detail=False)
    def species_documents_list(self, request, *args, **kwargs):
        qs = self.get_queryset()
        qs = self.filter_queryset(qs)
        self.paginator.page_size = qs.count()
        result_page = self.paginator.paginate_queryset(qs, request)
        serializer = SpeciesDocumentsSerializer(result_page, context={'request': request}, many=True)
        return self.paginator.get_paginated_response(serializer.data)


@require_http_methods(['GET'])
def species_data_internal(request, species_id):
    # TODO: Hack to provide mandatory Proposal fields to page.
    d = {"species_id": species_id,"id":1634,"application_type":"Commercial operations","activity":None,"approval_level":None,"approval_level_document":None,"region":None,"district":None,"tenure":None,"title":None,"data":None,"schema":[{}],"customer_status":"Under Review","processing_status":"With Assessor","review_status":"Not Reviewed","applicant":"My Org Ltd","org_applicant":{"id":182,"name":"My Org Ltd","trading_name":"My Org","abn":"1234567890","address":{"id":123,"line1":"100 Some Road","locality":"Howard Springs","state":"Australia","country":"AU","postcode":"0835"},"email":"info@my_org.com","organisation":{"id":194,"name":"My Org Ltd","abn":"1234567890","identification":None,"email":"info@my_org.com","trading_name":"My Org","postal_address":1425,"billing_address":193},"pins":{"one":"123","two":"456","three":"789","four":"012"},"delegates":[{"id":102473,"name":"AAA BBB","email":"info@my_org.com","is_admin":True}],"apply_application_discount":False,"application_discount":0.0,"apply_licence_discount":False,"licence_discount":0.0,"charge_once_per_year":None,"max_num_months_ahead":0,"last_event_application_fee_date":None},"proxy_applicant":None,"submitter":{"id":102473,"email":"info@my_org.com","first_name":"AAA","last_name":"BBB","dob":None,"title":None,"organisation":None,"residential_address":None,"phone_number":"1234567890","mobile_number":""},"applicant_type":"ORG","assigned_officer":None,"assigned_approver":None,"previous_application":734,"get_history":[{"id":734,"modified":"2021-09-30T18:01:56.753000Z"},{"id":250,"modified":"2019-12-10T07:32:53.388097Z"}],"lodgement_date":"2021-12-06T00:30:46.613243Z","modified_date":"2021-12-06T00:30:50.068316Z","documents":[5005,5006,5007],"requirements":[2829,2828],"readonly":True,"can_user_edit":False,"can_user_view":True,"documents_url":"/media/cols/proposals/1634/documents/","assessor_mode":{"assessor_mode":True,"has_assessor_mode":True,"assessor_can_assess":True,"assessor_level":"assessor","assessor_box_view":True},"current_assessor":{"id":255,"name":"Jaw Mus","email":"jaw.mus@dbca.wa.gov.au"},"assessor_data":None,"comment_data":None,"latest_referrals":[],"allowed_assessors":[{"id":102712,"email":"sss.hhh@dbca.wa.gov.au","first_name":"SSS","last_name":"HHH","title":"Licensing Officer","organisation":None}],"proposed_issuance_approval":None,"proposed_decline_status":False,"proposaldeclineddetails":None,"permit":None,"reference":"A001634-0","lodgement_number":"A001634","lodgement_sequence":0,"can_officer_process":True,"proposal_type":"Renewal","qaofficer_referrals":[],"applicant_details":"My Org Ltd \n123 Some Road, Howard Springs, Australia, AU, 0835","other_details":{"id":2918,"accreditations":[{"id":1109,"accreditation_type":"atap","accreditation_expiry":None,"comments":"","proposal_other_details":2918,"accreditation_type_value":"QTA"}],"preferred_licence_period":"3_year","nominated_start_date":"01/02/2022","insurance_expiry":"01/03/2022","other_comments":".. in which case we would apply for one.","credit_fees":False,"credit_docket_books":True,"docket_books_number":"5","mooring":[""],"proposed_end_date":"31/01/2025"},"activities_land":None,"land_access":[3],"trail_activities":[],"trail_section_activities":[],"activities_marine":None,"training_completed":True,"can_edit_activities":True,"can_edit_period":True,"reversion_ids":[{"cur_version_id":12134131,"prev_version_id":12133999,"created":"2021-12-06T00:30:50.068316Z"},{"cur_version_id":12134131,"prev_version_id":12068457,"created":"2021-12-06T00:30:48.412148Z"},{"cur_version_id":12134131,"prev_version_id":12068378,"created":"2021-12-02T01:54:40.309170Z"}],"assessor_assessment":{"id":1326,"completed":False,"submitter":None,"referral_assessment":False,"referral_group":None,"referral_group_name":"","checklist":[{"id":12488,"question":{"id":37,"text":"Valid public liability insurance certificate","answer_type":"yes_no"},"answer":None,"text_answer":None},{"id":12489,"question":{"id":18,"text":"Adequate level of accreditation provided","answer_type":"yes_no"},"answer":None,"text_answer":None},{"id":12490,"question":{"id":8,"text":"Deed Poll signed, witnessed and dated","answer_type":"yes_no"},"answer":None,"text_answer":None},{"id":12491,"question":{"id":36,"text":"Is a higher assessment required for any activities or parks? If yes please list.","answer_type":"free_text"},"answer":None,"text_answer":None},{"id":12492,"question":{"id":11,"text":"Aboriginal culture tours - WAITOC Member","answer_type":"yes_no"},"answer":None,"text_answer":None},{"id":12493,"question":{"id":10,"text":"Aboriginal culture tours - Approval given by  AHU representative","answer_type":"yes_no"},"answer":None,"text_answer":None},{"id":12494,"question":{"id":23,"text":"Aircraft activities - Valid CASA Air Operator's Certificate (AOC) and Certificate of Registration supplied","answer_type":"yes_no"},"answer":None,"text_answer":None},{"id":12495,"question":{"id":16,"text":"4WD Training - COL assessment to Districts","answer_type":"yes_no"},"answer":None,"text_answer":None},{"id":12496,"question":{"id":21,"text":"Maps of access points and vessel routes in marine parks.","answer_type":"free_text"},"answer":None,"text_answer":None},{"id":12497,"question":{"id":38,"text":"Assessor notes","answer_type":"free_text"},"answer":None,"text_answer":None}]},"referral_assessments":None,"fee_invoice_url":"/cols/payments/invoice-pdf/05575281113","fee_paid":True,"requirements_completed":True}
    dumped_data = json.dumps(d)
   
    return HttpResponse(dumped_data, content_type='application/json')