#coding=utf-8
'''
Created on 2016-10-12

@author: zhangtiande
'''
from rest_framework import generics
from doraemon.api.ci.serializer import ci_serializer
from rest_framework.permissions import AllowAny
from doraemon.ci.models import CIDeployService
from doraemon.ci.mongo_models import DeployServiceReplaceConfig




class CIDeployServiceView(generics.RetrieveUpdateDestroyAPIView):
    """
    An endpoint for users to view and update their profile information.
    """
    serializer_class = ci_serializer.CIDeployServiceSerializer
    permission_classes=[AllowAny]
    

    def get_object(self):
        service_id =int(self.kwargs['id'])
        return CIDeployService.objects.get(service_id)


class CIDeployServiceReplaceConfigView(generics.ListAPIView):
    """
    An endpoint for users to view and update their profile information.
    """
    serializer_class = ci_serializer.ServiceReplaceConfigSerializer
    permission_classes=[AllowAny]
    
    def get_queryset(self):
        service_id=self.kwargs['id']
        return DeployServiceReplaceConfig.objects.filter(service_id=service_id).order_by('-id')
    
        