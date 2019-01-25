#coding=utf-8
# coding=utf-8
'''
Created on 2014-1-5

@author: zhangtiande
'''
from rest_framework import generics
from teamvision.api.ci.serializer import autotesting_serializer
from rest_framework.permissions import AllowAny
from teamvision.ci.models import ServiceHost
from teamvision.api.ci.filters.ci_pagination import CIPagination
from teamvision.api.ci.filters.service_host_filter import ServiceHostFilterSet


class ServiceHostView(generics.RetrieveUpdateDestroyAPIView):
    """
    An endpoint for users to view and update their profile information.
    """
    serializer_class = autotesting_serializer.ServiceHostSerializer
    permission_classes=[AllowAny]
    

    def get_object(self):
        host_id =int(self.kwargs['id'])
        return ServiceHost.objects.get(host_id)



class ServiceHostListView(generics.ListCreateAPIView):
    """
    /api/ci/service_hosts?EnvID=1446: return host info with EnvID 1446
    /api/ci/service_hosts return all
    """
    serializer_class = autotesting_serializer.ServiceHostSerializer
    permission_classes=[AllowAny]
    queryset=ServiceHost.objects.all()
    pagination_class = CIPagination
    
    def get_queryset(self):
        qs = super(ServiceHostListView, self).get_queryset()
        return ServiceHostFilterSet(data=self.request.GET, queryset=qs).filter()
    



