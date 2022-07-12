# Create your views here.
import logging

from django.shortcuts import redirect
from django.contrib.auth import logout
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet

from apps.core.models import User
from apps.core.serializer import UserSerializer, UserRegisterSerializer
from apps.utils.base import Addon, BaseViewSet

api_log = logging.getLogger('core')


def account_logout(request):
    try:
        logout(request)
    except Exception as ex:
        pass
    return redirect('/')


class RegisterViewSet(ViewSet, Addon):
    serializer_class = UserSerializer

    @staticmethod
    def get_request_data(request) -> dict:
        return request.data if isinstance(request.data, dict) else request.data.dict()

    @swagger_auto_schema(request_body=UserRegisterSerializer,
                         operation_description="",
                         responses={},
                         operation_summary="USER SIGN-UP ENDPOINT"
                         )
    @action(detail=False, methods=['post'], description='USER SIGN-UP ENDPOINT')
    def register(self, request, *args, **kwargs):
        context = {'status': status.HTTP_201_CREATED}
        try:
            api_log.info(f'Registering new user on the system')
            data = self.get_request_data(request)
            serializer = UserRegisterSerializer(data=data)
            if serializer.is_valid():
                validata_data = serializer.validated_data
                validata_data.update({'username': self.unique_generator(User, 'username', 10)})
                _ = serializer.create(validata_data)
                context.update({'message': 'Account created successfully'})
                api_log.info(f'User created successfully')
            else:
                context.update({'status': status.HTTP_400_BAD_REQUEST, 'errors': serializer.error_messages})
        except Exception as ex:
            api_log.info(f'Something went wrong while creating user account due to {str(ex)}')
            context.update({'status': status.HTTP_400_BAD_REQUEST, 'message': str(ex)})
        return Response(context, status=context['status'])


class UserViewSet(BaseViewSet):
    serializer_class = UserSerializer
    query_set = User.objects.all()

    @swagger_auto_schema(
        operation_description="",
        responses={},
        operation_summary="RETRIEVE USER INFORMATION"
    )
    @action(detail=False, methods=['get'], description='Fetch personal information of a logged in user', url_path='me')
    def get_user(self, request, *args, **kwargs):
        context = {'status': status.HTTP_200_OK}
        try:
            api_log.info(f'Retrieving user information for user {request.user.id}')
            context.update({'data': self.serializer_class(request.user).data})
        except Exception as ex:
            api_log.info(f'Something went wrong while fetching user information {request.user.id}')
            context.update({'message': str(ex), 'status': status.HTTP_400_BAD_REQUEST})
        return Response(context, status=context['status'])
