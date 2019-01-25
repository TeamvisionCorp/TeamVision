#coding=utf-8
# coding=utf-8
'''
Created on 2014-1-5

@author: zhangtiande
'''

from teamvision.home.models import Team
from rest_framework import generics
from teamvision.api.common.serializer import team_serializer
from rest_framework.permissions import AllowAny
from teamvision.api.common.filters.team_filter import TeamFilterSet
from rest_framework.views import APIView
from rest_framework.authentication import SessionAuthentication, BasicAuthentication

class TeamListView(generics.ListCreateAPIView):
    """
    /api/common/agents
    FilterSet:'Status'
    FilterOperation:=,!=,__in,__contains,__icontains,__range,__gt,=1,2,3
    """
    serializer_class = team_serializer.TeamSerializer
    permission_classes=[AllowAny]
    authentication_classes = (SessionAuthentication,BasicAuthentication)
    queryset=Team.objects.all()
    

    def get_queryset(self):
        qs = super(TeamListView, self).get_queryset()
        return TeamFilterSet(data=self.request.GET, queryset=qs).filter()

class TeamView(generics.RetrieveUpdateDestroyAPIView):
    """
    An endpoint for users to view and update their profile information.
    """
    serializer_class = team_serializer.TeamSerializer
    permission_classes=[AllowAny]
    

    def get_object(self):
        team_id =int(self.kwargs['id'])
        return Team.objects.get(team_id)
    

    