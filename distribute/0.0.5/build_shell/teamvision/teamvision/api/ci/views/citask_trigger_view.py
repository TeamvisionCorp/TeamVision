#coding=utf-8
'''
Created on 2016-10-12

@author: zhangtiande
'''
from rest_framework import generics,response,status
from teamvision.api.ci.serializer import ci_serializer
from rest_framework.permissions import AllowAny
from teamvision.ci.models import CITaskApiTrigger
from teamvision.api.ci.filters.ci_task_trigger_filter import CITaskTriggerFilterSet
from business.ci.citask_trigger_service import CITaskTriggerService
from rest_framework.response import Response


class CITaskTriggerView(generics.RetrieveDestroyAPIView,generics.UpdateAPIView):
    """
    GET  /api/ci/task_trigger/<tk_uuid>
    """
    serializer_class = ci_serializer.CITaskTriggerSerializer
    permission_classes=[AllowAny]
    

    def get_object(self):
        tk_uuid =self.kwargs['tk_uuid']
        trigger = CITaskApiTrigger.objects.get_by_tkuuid(tk_uuid)
        if trigger is None:
            trigger = CITaskApiTrigger.objects.get_by_truuid(tk_uuid)
        return  trigger


class CITaskTriggerListView(generics.ListAPIView):
    """
    GET  /api/ci/task_triggers
    """
    serializer_class = ci_serializer.CITaskTriggerSerializer
    permission_classes = [AllowAny]

    def get_queryset(self):
        trigger = CITaskApiTrigger.objects.all()
        return CITaskTriggerFilterSet(data=self.request.GET, queryset=trigger).filter()



class CITaskTriggerStartView(generics.CreateAPIView,generics.RetrieveAPIView):
    """
    GET/POST  /api/ci/task/start?TaskID=1&TriggerUUID=12&TriggerName='API'
    """
    serializer_class = ci_serializer.CITaskTriggerSerializer
    permission_classes=[AllowAny]


    def get_object(self):
        return None

    def get(self, request, *args, **kwargs):
        trigger = CITaskTriggerService.create_start_trigger(request,request.GET,request.user)
        serializer = ci_serializer.CITaskTriggerSerializer(instance=trigger)
        headers = self.get_success_headers(serializer.data)
        return response.Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def post(self, request, *args, **kwargs):
        trigger = CITaskTriggerService.create_start_trigger(request,request.data,request.user)
        serializer = ci_serializer.CITaskTriggerSerializer(instance=trigger)
        headers = self.get_success_headers(serializer.data)
        return response.Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


class CITaskTriggerStopView(generics.CreateAPIView,generics.RetrieveAPIView):
    """
    GET/POST  /api/ci/task/stop?TaskID=1&TriggerUUID=12&TriggerName='API'
    """
    serializer_class = ci_serializer.CITaskTriggerSerializer
    permission_classes=[AllowAny]


    def get_object(self):
        return None


    def get(self, request, *args, **kwargs):
        trigger = CITaskTriggerService.create_stop_trigger(request,request.GET,request.user)
        serializer = ci_serializer.CITaskTriggerSerializer(instance=trigger)
        headers = self.get_success_headers(serializer.data)
        if trigger is None:
            status_code = status.HTTP_204_NO_CONTENT
        else:
            status_code = status.HTTP_201_CREATED
        return response.Response(serializer.data, status=status_code, headers=headers)



    def post(self, request, *args, **kwargs):
        trigger = CITaskTriggerService.create_stop_trigger(request,request.data,request.user)
        serializer = ci_serializer.CITaskTriggerSerializer(instance=trigger)
        headers = self.get_success_headers(serializer.data)
        if trigger is None:
            status_code = status.HTTP_204_NO_CONTENT
        else:
            status_code = status.HTTP_201_CREATED
        return response.Response(serializer.data, status=status_code, headers=headers)


    
    
        