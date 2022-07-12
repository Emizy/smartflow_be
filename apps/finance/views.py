import logging

from django.shortcuts import get_object_or_404
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.response import Response
from apps.finance.models import Sales
from apps.finance.serializer import SalesSerializer, SalesFormSerializer
from apps.utils.base import BaseViewSet

finance_log = logging.getLogger('finance')


class SalesViewSet(BaseViewSet):
    queryset = Sales.objects.all().order_by('-pk')
    serializer_class = SalesSerializer
    search_fields = ('customer_name', 'created_at',)
    filter_fields = ('status',)

    def get_queryset(self):
        return self.queryset.filter(agent=self.request.user)

    def get_object(self):
        return get_object_or_404(Sales, id=self.kwargs.get('pk'))

    @swagger_auto_schema(
        operation_summary="LIST ALL SALES"
    )
    def list(self, request, *args, **kwargs):
        context = {'status': status.HTTP_200_OK}
        try:
            finance_log.info(f'Fetching all sales for user_id {request.user.id}')
            paginate = self.paginator(queryset=self.get_list(self.get_queryset()),
                                      serializer_class=self.serializer_class)
            context.update({'status': status.HTTP_200_OK, 'message': 'OK',
                            'data': paginate})
        except Exception as ex:
            finance_log.error(f'Error fetching all sales for user_id {request.user.id} due to {str(ex)}')
            context.update({'status': status.HTTP_400_BAD_REQUEST, 'message': str(ex)})
        return Response(context, status=context['status'])

    @swagger_auto_schema(request_body=SalesFormSerializer, operation_summary='CREATE SALES')
    def create(self, request, *args, **kwargs):
        context = {'status': status.HTTP_201_CREATED}
        finance_log.info(f'creating sales entry for user_id {request.user.id}')
        try:
            data = self.get_data(request)
            serializer = SalesFormSerializer(data=data)
            if serializer.is_valid():
                serializer.validated_data.update({'agent': request.user})
                instance = serializer.create(validated_data=serializer.validated_data)
                context.update({'data': self.serializer_class(instance).data})
                finance_log.info(f'done creating sales entry for user_id {request.user.id}')
            else:
                context.update({'errors': serializer.error_messages, 'status': status.HTTP_400_BAD_REQUEST})
        except Exception as ex:
            context.update({'status': status.HTTP_400_BAD_REQUEST, 'message': str(ex)})
            finance_log.info(f'error creating sales entry for user_id {request.user.id} due to {str(ex)}')
        return Response(context, status=context['status'])

    @swagger_auto_schema(request_body=SalesFormSerializer, operation_summary='UPDATE SALES')
    def update(self, request, *args, **kwargs):
        context = {'status': status.HTTP_200_OK}
        try:
            data = self.get_data(request)
            instance = self.get_object()
            serializer = SalesFormSerializer(data=data, instance=instance)
            if serializer.is_valid():
                obj = serializer.update(validated_data=serializer.validated_data, instance=instance)
                context.update({'data': self.serializer_class(obj).data})
                finance_log.info(f'done updating sales entry for user_id {request.user.id} pk {self.kwargs.get("pk")}')
            else:
                context.update({'errors': serializer.error_messages, 'status': status.HTTP_400_BAD_REQUEST})
        except Exception as ex:
            context.update({'status': status.HTTP_400_BAD_REQUEST, 'message': str(ex)})
        return Response(context, status=context['status'])

    @swagger_auto_schema(operation_summary='DELETE SALES')
    def destroy(self, request, *args, **kwargs):
        context = {'status': status.HTTP_204_NO_CONTENT}
        try:
            instance = self.get_object()
            instance.delete()
            context.update({'message': 'Entry deleted successfully'})
        except Exception as ex:
            context.update({'message': str(ex), 'status': status.HTTP_400_BAD_REQUEST})
        return Response(context, status=context['status'])
