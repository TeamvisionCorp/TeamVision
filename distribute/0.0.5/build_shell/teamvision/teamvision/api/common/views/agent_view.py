#coding=utf-8
# coding=utf-8
'''
Created on 2014-1-5

@author: zhangtiande
'''

from teamvision.home.models import Agent
from rest_framework import generics,response,status
from teamvision.api.common.serializer import agent_serializer
from rest_framework.permissions import AllowAny
from teamvision.api.common.filters.auto_filter import AgentFilterSet
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from business.ci.ci_agent_service import  CIAgentService
from teamvision.api.project.views.CsrfExemptSessionAuthentication import CsrfExemptSessionAuthentication

class AgentListView(generics.ListCreateAPIView):
    """
    /api/common/agents
    FilterSet:'Status'
    FilterOperation:=,!=,__in,__contains,__icontains,__range,__gt,=1,2,3
    """
    serializer_class = agent_serializer.AgentSerializer
    permission_classes=[AllowAny]
    authentication_classes = (BasicAuthentication,CsrfExemptSessionAuthentication)
    queryset=Agent.objects.all()
    

    def get_queryset(self):
        qs = super(AgentListView, self).get_queryset()
        return AgentFilterSet(data=self.request.GET, queryset=qs).filter()

    def post(self, request, *args, **kwargs):
        agent = CIAgentService.create_ci_agent(request.data,request.user)
        serializer = agent_serializer.AgentSerializer(instance=agent)
        headers = self.get_success_headers(serializer.data)
        return response.Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

class AgentView(generics.RetrieveUpdateDestroyAPIView):
    """
    An endpoint for users to view and update their profile information.
    """
    serializer_class = agent_serializer.AgentSerializer
    permission_classes=[AllowAny]
    authentication_classes = (BasicAuthentication, CsrfExemptSessionAuthentication)
    

    def get_object(self):
        agent_id =int(self.kwargs['id'])
        return Agent.objects.get(agent_id)

    def put(self, request, *args, **kwargs):
        agent_id = int(self.kwargs['id'])
        agent = CIAgentService.edit_ci_agent(request.data,agent_id,request.user)
        serializer = agent_serializer.AgentSerializer(instance=agent)
        return response.Response(serializer.data, status=status.HTTP_202_ACCEPTED)
    

    