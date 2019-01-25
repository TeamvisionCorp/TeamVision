#coding=utf-8
# coding=utf-8
'''
Created on 2014-1-5

@author: ETHAN
'''
from rest_framework import generics
from doraemon.api.logcat.serializer import logcat_serializer
from rest_framework.permissions import AllowAny
from doraemon.logcat.models import Logger
from rest_framework import status
from rest_framework.response import Response




class LoggerListView(generics.ListAPIView):
    """ 
    获取全部logger。一个logger代表一个设备
    """
    serializer_class = logcat_serializer.LoggerSerializer
    permission_classes=[AllowAny]
    

    def get_queryset(self):
        return Logger.objects.all()

class LoggerCreateView(generics.CreateAPIView):
    """ 
    注册新的logger,已经存在的log，不再注册
    """
    serializer_class = logcat_serializer.LoggerSerializer
    permission_classes=[AllowAny]
    
    
    
    def post(self, request, *args, **kwargs):
        print(request.META['HTTP_USER_AGENT'])
        device_id=request.data['deviceId']
        logger=Logger.objects.get_by_deviceid(device_id)
        if not logger:
            return self.create(request, *args, **kwargs)
        else:
            headers=self.get_success_headers(request.data)
            return Response(request.data, status=status.HTTP_201_CREATED, headers=headers)
    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        device_id=request.data['deviceId']
        logger=Logger.objects.get_by_deviceid(device_id)
        if logger:
            logger.userAgent=request.META['HTTP_USER_AGENT']
            logger.save()
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
            
    

class LoggerView(generics.RetrieveUpdateDestroyAPIView):
    """
    通过logger id 获取logger信息
    """
    serializer_class = logcat_serializer.LoggerSerializer
    permission_classes=[AllowAny]
    

    def get_object(self):
        logger_id =int(self.kwargs['id'])
        return Logger.objects.get(logger_id)

    

    