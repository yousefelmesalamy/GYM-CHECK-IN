from django.contrib.auth.models import User
from django.conf import settings
from rest_framework.response import Response
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.authtoken.models import Token

from .serializers import UserSerializer
from rest_framework.views import APIView
from .permissons import UserPermission
from django.contrib.auth.signals import user_logged_in, user_logged_out
from django.utils import timezone
from rest_framework.serializers import DateTimeField
from rest_framework.settings import api_settings
# -------------------------------------------------------------------------------------------
# Create your views here.
# Knox
from django.contrib.auth import login
# from knox.views import LoginView as KnoxLoginView
from rest_framework.authtoken.serializers import AuthTokenSerializer
from rest_framework import permissions
from rest_framework.response import Response
from rest_framework import status
# from knox.models import AuthToken

#
# class LoginView(KnoxLoginView):
#     permission_classes = [UserPermission]
#
#     def post(self, request, format=None):
#         serializer = AuthTokenSerializer(data=request.data)
#         if serializer.is_valid():
#             user = serializer.validated_data['user']
#             login(request, user)
#             token_ttl = self.get_token_ttl()
#             instance, token = AuthToken.objects.create(user, token_ttl)
#             return Response({
#                 'token': token,
#                 'user_id': user.pk,
#                 'email': user.email
#             })
#         else:
#             return Response({"Response": "username or password was incorrect"}, status=status.HTTP_401_UNAUTHORIZED)


# -------------------------------------------------------------------------------------------
from django.shortcuts import render
from .models import InMemberShip
from .serializers import InMemberShipSerializer
from django.shortcuts import get_object_or_404
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework import filters
from django_filters.rest_framework import DjangoFilterBackend


class InmemberShipViewSet(viewsets.ModelViewSet):
    queryset = InMemberShip.objects.all()
    serializer_class = InMemberShipSerializer
    permission_classes = [UserPermission]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter, DjangoFilterBackend]
    search_fields = ['id', 'user', 'membership_type', 'membership_type_name', 'membership_start_date',
                     'membership_end_date',
                     'membership_days_of_week', 'membership_check_in_count', 'membership_check_in_count_remaining',
                     'membership_check_in_count_remaining']


# -------------------------------------------------------------------------------------------
def check_in(request, subscriber_id):
    subscriber = get_object_or_404(InMemberShip, pk=subscriber_id)
    subscriber.check_in()
    return render(request, 'check_in_success.html', {'subscriber': subscriber})


from django.http import HttpResponse


def check_in_view(request, subscriber_id):
    return HttpResponse(f"Checking in subscriber with ID {subscriber_id}")


# -------------------------------------------------------------------------------------------
from .models import USER


class UserViewSet(viewsets.ModelViewSet):
    queryset = USER.objects.all()
    serializer_class = UserSerializer
    permission_classes = [UserPermission]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter, DjangoFilterBackend]
    search_fields = ['username', 'first_name', 'last_name', 'email', 'phone_number', 'is_staff', 'is_active',
                     'is_superuser']

    filterset_fields = ['id', 'username', 'first_name', 'last_name', 'email', 'phone_number', 'is_staff', 'is_active',
                        'is_superuser']

    lookup_field = 'id'
    ordering_fields = ['username', 'first_name', 'last_name', 'email', 'phone_number', 'is_staff', 'is_active',
                       'is_superuser']
