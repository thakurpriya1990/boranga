import logging
import traceback

from django.core.cache import cache
from django.core.exceptions import ValidationError
from django.db import transaction
from django.db.models import CharField, Value
from django.db.models.functions import Concat
from django_countries import countries
from ledger_api_client.ledger_models import Address
from ledger_api_client.ledger_models import EmailUserRO as EmailUser
from rest_framework import filters, generics, serializers, views, viewsets
from rest_framework.decorators import action as detail_route
from rest_framework.decorators import action as list_route
from rest_framework.decorators import renderer_classes
from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response

from boranga.components.main.models import UserSystemSettings
from boranga.components.main.utils import retrieve_department_users
from boranga.components.organisations.serializers import OrganisationRequestDTSerializer
from boranga.components.users.serializers import (
    ContactSerializer,
    EmailUserActionSerializer,
    EmailUserCommsSerializer,
    EmailUserLogEntrySerializer,
    PersonalSerializer,
    UserAddressSerializer,
    UserFilterSerializer,
    UserSerializer,
    UserSystemSettingsSerializer,
)
from boranga.permissions import IsApprover, IsAssessor, IsConservationStatusEditor

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

        # serializer  = UserSerializer(request.user)


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


class UserListFilterView(generics.ListAPIView):
    """https://cop-internal.dbca.wa.gov.au/api/filtered_users?search=russell"""

    queryset = EmailUser.objects.all()
    serializer_class = UserFilterSerializer
    filter_backends = (filters.SearchFilter,)
    search_fields = ("email", "first_name", "last_name")


class UserViewSet(viewsets.ModelViewSet):
    queryset = EmailUser.objects.all()
    serializer_class = UserSerializer
    # Add permission groups that can access the userviewset, can add more group later as required
    permission_classes = [IsAssessor | IsApprover | IsConservationStatusEditor]

    @list_route(
        methods=[
            "GET",
        ],
        detail=False,
    )
    def get_department_users(self, request, *args, **kwargs):
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
        ).filter(is_staff=True)

        department_users = department_users.filter(
            search_term__icontains=search_term
        ).values("id", "email", "first_name", "last_name")[:10]

        data_transform = [
            {
                "id": person["email"],
                "text": f"{person['first_name']} {person['last_name']} ({person['email']})",
            }
            for person in department_users
        ]
        return Response({"results": data_transform})

    @detail_route(
        methods=[
            "POST",
        ],
        detail=True,
    )
    def update_personal(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            serializer = PersonalSerializer(instance, data=request.data)
            serializer.is_valid(raise_exception=True)
            instance = serializer.save()
            serializer = UserSerializer(instance)
            return Response(serializer.data)
        except serializers.ValidationError:
            print(traceback.print_exc())
            raise
        except ValidationError as e:
            print(traceback.print_exc())
            raise serializers.ValidationError(repr(e.error_dict))
        except Exception as e:
            print(traceback.print_exc())
            raise serializers.ValidationError(str(e))

    @detail_route(
        methods=[
            "POST",
        ],
        detail=True,
    )
    def update_contact(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            serializer = ContactSerializer(instance, data=request.data)
            serializer.is_valid(raise_exception=True)
            instance = serializer.save()
            serializer = UserSerializer(instance)
            return Response(serializer.data)
        except serializers.ValidationError:
            print(traceback.print_exc())
            raise
        except ValidationError as e:
            print(traceback.print_exc())
            raise serializers.ValidationError(repr(e.error_dict))
        except Exception as e:
            print(traceback.print_exc())
            raise serializers.ValidationError(str(e))

    @detail_route(
        methods=[
            "POST",
        ],
        detail=True,
    )
    def update_address(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            serializer = UserAddressSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            address, created = Address.objects.get_or_create(
                line1=serializer.validated_data["line1"],
                locality=serializer.validated_data["locality"],
                state=serializer.validated_data["state"],
                country=serializer.validated_data["country"],
                postcode=serializer.validated_data["postcode"],
                user=instance,
            )
            instance.residential_address = address
            instance.save()
            serializer = UserSerializer(instance)
            return Response(serializer.data)
        except serializers.ValidationError:
            print(traceback.print_exc())
            raise
        except ValidationError as e:
            print(traceback.print_exc())
            raise serializers.ValidationError(repr(e.error_dict))
        except Exception as e:
            print(traceback.print_exc())
            raise serializers.ValidationError(str(e))

    @detail_route(
        methods=[
            "POST",
        ],
        detail=True,
    )
    def update_system_settings(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            # serializer = UserSystemSettingsSerializer(data=request.data)
            # serializer.is_valid(raise_exception=True)
            user_setting, created = UserSystemSettings.objects.get_or_create(
                user=instance
            )
            serializer = UserSystemSettingsSerializer(user_setting, data=request.data)
            serializer.is_valid(raise_exception=True)
            # instance.residential_address = address
            serializer.save()
            instance = self.get_object()
            serializer = UserSerializer(instance)
            return Response(serializer.data)
        except serializers.ValidationError:
            print(traceback.print_exc())
            raise
        except ValidationError as e:
            print(traceback.print_exc())
            raise serializers.ValidationError(repr(e.error_dict))
        except Exception as e:
            print(traceback.print_exc())
            raise serializers.ValidationError(str(e))

    @detail_route(
        methods=[
            "GET",
        ],
        detail=True,
    )
    def pending_org_requests(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            serializer = OrganisationRequestDTSerializer(
                instance.organisationrequest_set.filter(status="with_assessor"),
                many=True,
                context={"request": request},
            )
            return Response(serializer.data)
        except serializers.ValidationError:
            print(traceback.print_exc())
            raise
        except ValidationError as e:
            print(traceback.print_exc())
            raise serializers.ValidationError(repr(e.error_dict))
        except Exception as e:
            print(traceback.print_exc())
            raise serializers.ValidationError(str(e))

    @detail_route(
        methods=[
            "GET",
        ],
        detail=True,
    )
    def action_log(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            qs = instance.action_logs.all()
            serializer = EmailUserActionSerializer(qs, many=True)
            return Response(serializer.data)
        except serializers.ValidationError:
            print(traceback.print_exc())
            raise
        except ValidationError as e:
            print(traceback.print_exc())
            raise serializers.ValidationError(repr(e.error_dict))
        except Exception as e:
            print(traceback.print_exc())
            raise serializers.ValidationError(str(e))

    @detail_route(
        methods=[
            "GET",
        ],
        detail=True,
    )
    def comms_log(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            qs = instance.comms_logs.all()
            serializer = EmailUserCommsSerializer(qs, many=True)
            return Response(serializer.data)
        except serializers.ValidationError:
            print(traceback.print_exc())
            raise
        except ValidationError as e:
            print(traceback.print_exc())
            raise serializers.ValidationError(repr(e.error_dict))
        except Exception as e:
            print(traceback.print_exc())
            raise serializers.ValidationError(str(e))

    @detail_route(
        methods=[
            "POST",
        ],
        detail=True,
    )
    @renderer_classes((JSONRenderer,))
    def add_comms_log(self, request, *args, **kwargs):
        try:
            with transaction.atomic():
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
                # End Save Documents

                return Response(serializer.data)
        except serializers.ValidationError:
            print(traceback.print_exc())
            raise
        except ValidationError as e:
            print(traceback.print_exc())
            raise serializers.ValidationError(repr(e.error_dict))
        except Exception as e:
            print(traceback.print_exc())
            raise serializers.ValidationError(str(e))
