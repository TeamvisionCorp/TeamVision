#coding=utf-8
# coding=utf-8
'''
Created on 2014-1-5

@author: ETHAN
'''
from rest_framework import generics
from teamvision.api.logcat.serializer import logcat_serializer
from rest_framework.permissions import AllowAny
from teamvision.logcat.mongo_models import BusinessLog

from business.logcat.logger_service import LoggerService
from gatesidelib.common.simplelogger import SimpleLogger
from rest_framework import status
from rest_framework.response import Response
from django.http.response import HttpResponse




class BusinessLogListView(generics.ListAPIView):
    """ 
    get all story log by device id
    """
    serializer_class = logcat_serializer.BusinessLogSerializer
    permission_classes=[AllowAny]
    

    def get_queryset(self):
        device_id=self.kwargs['device_id']
        return BusinessLog.objects.all().filter(deviceId=device_id)

class BusinessLogCreateView(generics.CreateAPIView):
    """ 
    add new log to db
    """
    serializer_class = logcat_serializer.BusinessLogSerializer
    permission_classes=[AllowAny]
    
    def post(self, request, *args, **kwargs):
        try:
            device_id=request.data['deviceId']
            message=LoggerService.get_log_from_request(request)
            LoggerService.publicsh_message("logcat_"+device_id,message)
        except Exception as ex:
            SimpleLogger.exception(ex)
        return self.create(request, *args, **kwargs)

    

    

    