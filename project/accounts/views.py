from django.contrib.auth import login
from django.http import HttpRequest

from rest_framework import generics, status, views, viewsets
# from rest_framework.authentication import (
#     BasicAuthentication,
#     SessionAuthentication
# )
from rest_framework.permissions import AllowAny  # IsAdminUser,
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from utils.mixins import AccountsPermissionMixin

from .models import Account
from .serializers import (AccountSerializer, ChangePasswordSerializer,
                          LoginSerializer)


class AccountViewSet(AccountsPermissionMixin,
                     viewsets.ModelViewSet):
    """
    Account model viewset.
    """
    # authentication_classes = (
    #     SessionAuthentication, BasicAuthentication
    # )
    # permission_classes = IsAdminUser,
    serializer_class = AccountSerializer

    def get_queryset(self):
        """
        lets to format queryset
        """
        qs = Account.objects.all()
        return qs

    def get_serializer_context(self):
        """
        lets to update and pass the additional
        context data to the serializer
        """
        context = super().get_serializer_context()
        return context

    # HTTP methods

    def list(self,
             request: HttpRequest) -> Response:
        """ GET list """
        qs = self.get_queryset()
        serializer = self.get_serializer(qs, many=True)
        return Response(serializer.data)

    def create(self,
               request: HttpRequest) -> Response:
        """ POST """
        return super().create(request)

    def retrieve(self,
                 request: HttpRequest,
                 pk: str) -> Response:
        """ GET instance """
        return super().retrieve(request, pk=pk)

    def update(self,
               request: HttpRequest,
               pk: str,
               **kwargs) -> Response:
        """ PUT instance """
        return super().update(request, pk=pk, **kwargs)

    def partial_update(self,
                       request: HttpRequest,
                       pk: str,
                       **kwargs) -> Response:
        """ PATCH instance """
        return super().partial_update(request, pk=pk)

    def destroy(self,
                request: HttpRequest,
                pk: str) -> Response:
        """ DELETE instance """
        return super().destroy(request, pk=pk)


class ChangePasswordView(generics.UpdateAPIView):
    """
    Change account password view,
    allows PUT and PATCH HTTP methods.
    """
    queryset = Account.objects.all()
    permission_classes = IsAuthenticated,
    serializer_class = ChangePasswordSerializer


class LoginView(views.APIView):
    """ Login api view,
    returns sessionid in Set-Cookie header"""
    permission_classes = AllowAny,
    serializer_class = LoginSerializer

    def post(self,
             request: HttpRequest) -> Response:
        """
        Post HTTP method handler function.
        """
        context = {'request': self.request}
        serializer = self.serializer_class(
                            data=self.request.data,
                            context=context
                    )
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        login(request, user)
        return Response(status=status.HTTP_202_ACCEPTED)
