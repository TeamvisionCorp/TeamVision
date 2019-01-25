#coding=utf-8
# coding=utf-8
'''
Created on 2014-1-5

@author: zhangtiande
'''

from doraemon.home.models import Agent
from rest_framework import generics
from doraemon.api.common.serializer import agent_serializer
from rest_framework.permissions import AllowAny
from doraemon.api.common.filters.agent_filter import AutoFilterSet
from rest_framework.views import APIView
from rest_framework.authentication import SessionAuthentication, BasicAuthentication

class AgentListView(generics.ListCreateAPIView):
    """
    /api/common/agents
    FilterSet:'Status'
    FilterOperation:=,!=,__in,__contains,__icontains,__range,__gt,=1,2,3
    """
    serializer_class = agent_serializer.AgentSerializer
    permission_classes=[AllowAny]
    authentication_classes = (SessionAuthentication,BasicAuthentication)
    queryset=Agent.objects.all()
    

    def get_queryset(self):
        qs = super(AgentListView, self).get_queryset()
        return AutoFilterSet(data=self.request.GET, queryset=qs).filter()

class AgentView(generics.RetrieveUpdateDestroyAPIView):
    """
    An endpoint for users to view and update their profile information.
    """
    serializer_class = agent_serializer.AgentSerializer
    permission_classes=[AllowAny]
    

    def get_object(self):
        agent_id =int(self.kwargs['id'])
        return Agent.objects.get(agent_id)
    

    