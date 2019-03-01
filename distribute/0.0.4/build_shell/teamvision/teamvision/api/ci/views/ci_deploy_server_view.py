#coding=utf-8
'''
Created on 2016-10-12

@author: zhangtiande
'''
from rest_framework import generics
from teamvision.api.ci.serializer import ci_serializer
from rest_framework.permissions import AllowAny
from teamvision.ci.models import CIServer
from rest_framework.response import Response
from teamvision.api.ci.filters.ci_deploy_servers_filter import DeployServerFilterSet




class CIDeployServerView(generics.RetrieveUpdateDestroyAPIView):
    """
    An endpoint for users to view and update their profile information.
    """
    serializer_class = ci_serializer.CIDeployServerSerializer
    permission_classes=[AllowAny]
    

    def get_object(self):
        server_id =int(self.kwargs['id'])
        return CIServer.objects.get(server_id)

class CIDeployServerListView(generics.ListCreateAPIView):
    """
    /api/ci/deploy_servers:return all servers
    /api/ci/deploy_servers?id__in=2,3：return servers with id=2 or id=3
    """
    serializer_class = ci_serializer.CIDeployServerSerializer
    permission_classes=[AllowAny]
    queryset = CIServer.objects.all()
    
    def get_queryset(self):
        qs = super(CIDeployServerListView, self).get_queryset()
        return DeployServerFilterSet(data=self.request.GET, queryset=qs).filter()
    
    
        