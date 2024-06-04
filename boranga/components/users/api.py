import logging

from django.core.cache import cache
from django.db import transaction
from django.db.models import CharField, Value
from django.db.models.functions import Concat
from django.shortcuts import get_object_or_404
from django_countries import countries
from ledger_api_client.ledger_models import EmailUserRO as EmailUser
from rest_framework import filters, generics, mixins, views, viewsets
from rest_framework.decorators import action as detail_route
from rest_framework.decorators import action as list_route
from rest_framework.decorators import renderer_classes
from rest_framework.exceptions import PermissionDenied
from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response

from boranga.components.main.utils import retrieve_department_users
from boranga.components.users.models import SubmitterCategory, SubmitterInformation
from boranga.components.users.serializers import (
    EmailUserActionSerializer,
    EmailUserCommsSerializer,
    EmailUserLogEntrySerializer,
    SubmitterCategorySerializer,
    SubmitterInformationSerializer,
    UserFilterSerializer,
    UserSerializer,
)
from boranga.permissions import IsApprover, IsAssessor

logger = logging.getLogger(__name__)


class DepartmentUserList(views.APIView):
    renderer_classes = [
        JSONRenderer,
    ]

    def get(self, request, format=None):
        data = cache.get("department_users")
        if not data:
            retrieve_department_users()
            data = cache.get("department_users")
        data = retrieve_department_users()
        return Response(data)


class GetCountries(views.APIView):
    renderer_classes = [
        JSONRenderer,
    ]

    def get(self, request, format=None):
        country_list = []
        for country in list(countries):
            country_list.append({"name": country.name, "code": country.code})
        return Response(country_list)


class GetProfile(views.APIView):
    renderer_classes = [
        JSONRenderer,
    ]

    def get(self, request, format=None):
        serializer = UserSerializer(request.user, context={"request": request})
        return Response(serializer.data)


class GetSubmitterCategories(views.APIView):
    renderer_classes = [
        JSONRenderer,
    ]

    def get(self, request, format=None):
        submitter_categories = SubmitterCategory.objects.all()
        serializer = SubmitterCategorySerializer(submitter_categories, many=True)
        return Response(serializer.data)


class SaveSubmitterInformation(views.APIView):
    renderer_classes = [
        JSONRenderer,
    ]

    def put(self, request, format=None):
        instance = get_object_or_404(SubmitterInformation, pk=request.data["id"])
        if not instance.email_user == request.user.id:
            raise PermissionDenied("You do not have permission to perform this action.")

        serializer = SubmitterInformationSerializer(
            instance=instance, data=request.data
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)


class UserListFilterView(generics.ListAPIView):
    queryset = EmailUser.objects.none()
    serializer_class = UserFilterSerializer
    filter_backends = (filters.SearchFilter,)
    permission_classes = [IsAssessor | IsApprover]
    search_fields = ("email", "first_name", "last_name")


class UserViewSet(viewsets.GenericViewSet, mixins.RetrieveModelMixin):
    queryset = EmailUser.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAssessor | IsApprover]

    @list_route(
        methods=[
            "GET",
        ],
        detail=False,
    )
    def get_users(self, request, *args, **kwargs):
        search_term = request.GET.get("term", "")

        # Allow for search of first name, last name and concatenation of both
        department_users = EmailUser.objects.annotate(
            search_term=Concat(
                "first_name",
                Value(" "),
                "last_name",
                Value(" "),
                "email",
                output_field=CharField(),
            )
        )
        if kwargs.get("is_staff", False):
            department_users = department_users.filter(is_staff=True)

        id_field = "email"
        if kwargs.get("id_field", False):
            id_field = kwargs.get("id_field")

        department_users = department_users.filter(
            search_term__icontains=search_term
        ).values("id", "email", "first_name", "last_name")[:10]

        data_transform = [
            {
                "id": person[id_field],
                "text": f"{person['first_name']} {person['last_name']} ({person['email']})",
            }
            for person in department_users
        ]
        return Response({"results": data_transform})

    @list_route(
        methods=[
            "GET",
        ],
        detail=False,
    )
    def get_users_ledger_id(self, request, *args, **kwargs):
        return self.get_users(request, id_field="id")

    @list_route(
        methods=[
            "GET",
        ],
        detail=False,
    )
    def get_department_users(self, request):
        return self.get_users(request, is_staff=True)

    @list_route(
        methods=[
            "GET",
        ],
        detail=False,
    )
    def get_department_users_ledger_id(self, request, *args, **kwargs):
        return self.get_users(request, is_staff=True, id_field="id")

    @detail_route(
        methods=[
            "GET",
        ],
        detail=True,
    )
    def action_log(self, request, *args, **kwargs):
        instance = self.get_object()
        qs = instance.action_logs.all()
        serializer = EmailUserActionSerializer(qs, many=True)
        return Response(serializer.data)

    @detail_route(
        methods=[
            "GET",
        ],
        detail=True,
    )
    def comms_log(self, request, *args, **kwargs):
        instance = self.get_object()
        qs = instance.comms_logs.all()
        serializer = EmailUserCommsSerializer(qs, many=True)
        return Response(serializer.data)

    @detail_route(
        methods=[
            "POST",
        ],
        detail=True,
    )
    @renderer_classes((JSONRenderer,))
    @transaction.atomic
    def add_comms_log(self, request, *args, **kwargs):
        instance = self.get_object()
        mutable = request.data._mutable
        request.data._mutable = True
        request.data["emailuser"] = f"{instance.id}"
        request.data["staff"] = f"{request.user.id}"
        request.data._mutable = mutable
        serializer = EmailUserLogEntrySerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        comms = serializer.save()

        # Save the files
        for f in request.FILES:
            document = comms.documents.create()
            document.name = str(request.FILES[f])
            document._file = request.FILES[f]
            document.save()

        return Response(serializer.data)
