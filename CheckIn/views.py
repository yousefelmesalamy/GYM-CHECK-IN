from .serializers import UserSerializer
from .permissons import UserPermission
from django.http import Http404
from .models import InMemberShip
from .serializers import InMemberShipSerializer
from django.shortcuts import get_object_or_404
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework import filters
from django_filters.rest_framework import DjangoFilterBackend
from django.http import HttpResponse
from .models import USER
from django.shortcuts import render, redirect


class InmemberShipViewSet(viewsets.ModelViewSet):
    queryset = InMemberShip.objects.all()
    serializer_class = InMemberShipSerializer
    permission_classes = [UserPermission]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter, DjangoFilterBackend]
    search_fields = ['id', 'user', 'membership_type', 'membership_type_name', 'membership_start_date',
                     'membership_end_date',
                     'membership_days_of_week', 'membership_check_in_count', 'membership_check_in_count_remaining',
                     'membership_check_in_count_remaining']



def check_in(request, subscriber_id):
    try:
        subscriber = get_object_or_404(InMemberShip, pk=subscriber_id)
        subscriber.check_in()
        return render(request, 'check_in_success.html', {'subscriber': subscriber})
    except Http404:
        error_message = 'Invalid ID. Please try again.'
        return render(request, 'id_ask.html', {'error_message': error_message})


def check_in_view(request, subscriber_id):
    return HttpResponse(f"Checking in subscriber with ID {subscriber_id}")


def ask_for_id(request):
    if request.method == 'POST':
        user_id = request.POST.get('userID')
        if user_id:
            if is_valid_id(user_id):
                return redirect('check_in', subscriber_id=user_id)
            else:
                error_message = 'INVALID ID PLEASE TRY AGAIN'
                return render(request, 'id_ask.html', {'error_message': error_message})
    return render(request, 'id_ask.html')


def is_valid_id(user_id):
    try:
        user_id = int(user_id)
        if user_id > 0:
            return True
        else:
            return False
    except ValueError:
        return False


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
