from django.contrib.auth import login
from rest_framework import generics, views, viewsets, status
from rest_framework.response import Response
from rest_framework.authentication import (
    BasicAuthentication, SessionAuthentication
)
from rest_framework.permissions import (
    AllowAny, IsAdminUser, IsAuthenticated
)

from utils.mixins import AccountsPermissionMixin
from .serializers import (
    AccountSerializer, ChangePasswordSerializer,
    LoginSerializer,
)
from .models import Account


class AccountViewSet(AccountsPermissionMixin,
                     viewsets.ModelViewSet):
    """
    Account model viewset
    """
    # authentication_classes = [
    #     SessionAuthentication, BasicAuthentication
    # ]
    # permission_classes = [IsAdminUser]
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

    def list(self, request):
        """ GET list """
        qs = self.get_queryset()
        serializer = self.get_serializer(qs, many=True)
        return Response(serializer.data)

    def create(self, request):
        """ POST """
        return super().create(request)

    def retrieve(self, request, pk=None):
        """ GET instance """
        return super().retrieve(request, pk=pk)

    def update(self, request, pk=None, **kwargs):
        """ PUT instance """
        return super().update(request, pk=pk, **kwargs)

    def partial_update(self, request, pk=None, **kwargs):
        """ PATCH instance """
        return super().partial_update(request, pk=pk)

    def destroy(self, request, pk=None):
        """ DELETE instance """
        return super().destroy(request, pk=pk)


class ChangePasswordView(generics.UpdateAPIView):
    """
    Change account password view,
    allows PUT and PATCH.
    """
    queryset = Account.objects.all()
    permission_classes = (IsAuthenticated,)
    serializer_class = ChangePasswordSerializer


class LoginView(views.APIView):
    """ Login api view,
    returns sessionid in Set-Cookie header"""
    permission_classes = (AllowAny,)
    serializer_class = LoginSerializer  
    
    def post(self, request):
        context = {'request': self.request}
        serializer = self.serializer_class(
                            data=self.request.data,
                            context=context
                    )
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        login(request, user)
        return Response(status=status.HTTP_202_ACCEPTED)
