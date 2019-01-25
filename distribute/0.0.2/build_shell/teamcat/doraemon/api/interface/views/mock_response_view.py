# coding=utf-8
# coding=utf-8
'''
Created on 2014-1-5

@author: zhangtiande
'''

from doraemon.interface.models import MockResponse
from rest_framework import generics
from doraemon.api.interface.serializer import mock_serializer
from rest_framework.permissions import AllowAny
from doraemon.api.interface.filters.mock_api_filter import MockResponseFilterSet
from doraemon.api.project.views.CsrfExemptSessionAuthentication import CsrfExemptSessionAuthentication
from rest_framework.views import APIView
from rest_framework.authentication import SessionAuthentication, BasicAuthentication


class MockResponseListView(generics.ListCreateAPIView):
    """
    /api/env/mock/apis
    FilterSet:'id','ApiID','Enable'
    FilterOperation:=,!=,__in,__contains,__icontains,__range,__gt,=1,2,3,__isnull
    """
    serializer_class = mock_serializer.MockResponseSerializer
    permission_classes = [AllowAny]
    authentication_classes = (CsrfExemptSessionAuthentication, BasicAuthentication)
    queryset = MockResponse.objects.all()

    def get_queryset(self):
        qs = super(MockResponseListView, self).get_queryset()
        return MockResponseFilterSet(data=self.request.GET, queryset=qs).filter().order_by('-id')


class MockResponseView(generics.RetrieveUpdateDestroyAPIView):
    """
    /api/env/mock/api/id
    id: api id
    """
    serializer_class = mock_serializer.MockResponseSerializer
    permission_classes = [AllowAny]
    authentication_classes = (CsrfExemptSessionAuthentication, BasicAuthentication)

    def get_object(self):
        agent_id = int(self.kwargs['id'])
        return MockResponse.objects.get(agent_id)

class MockResponseOpView(generics.RetrieveUpdateDestroyAPIView):
    """
    /api/env/mock/api/id
    id: api id
    """
    serializer_class = mock_serializer.MockResponseSerializer
    permission_classes = [AllowAny]
    authentication_classes = (CsrfExemptSessionAuthentication, BasicAuthentication)

    def get_object(self):
        agent_id = int(self.kwargs['id'])
        return MockResponse.objects.get(agent_id)
