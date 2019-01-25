#coding=utf-8
# coding=utf-8
'''
Created on 2014-1-5

@author: zhangtiande
'''

from doraemon.interface.models import MockAPI
from rest_framework import generics
from doraemon.api.interface.serializer import mock_serializer
from rest_framework.permissions import AllowAny
from doraemon.api.interface.filters.mock_api_filter import MockAPIFilterSet
from doraemon.api.project.views.CsrfExemptSessionAuthentication import CsrfExemptSessionAuthentication
from rest_framework.authentication import SessionAuthentication, BasicAuthentication

class MockApiListView(generics.ListCreateAPIView):
    """
    /api/env/mock/apis
    FilterSet:'Parent','MockHandler','ApiType','ApiPath','Enable','id'
    FilterOperation:=,!=,__in,__contains,__icontains,__range,__gt,=1,2,3,__isnull
    """
    serializer_class = mock_serializer.MockAPISerializer
    permission_classes=[AllowAny]
    authentication_classes = (CsrfExemptSessionAuthentication,BasicAuthentication)
    

    def get_queryset(self):
        queryset=MockAPI.objects.all()
        return MockAPIFilterSet(data=self.request.GET, queryset=queryset).filter()


class MockApiTreeView(generics.ListCreateAPIView):
    """
    /api/env/mock/apis
    FilterSet:'id'
    FilterOperation:=,!=,__in,__contains,__icontains,__range,__gt,=1,2,3
    """
    serializer_class = mock_serializer.MockAPITreeSerializer
    permission_classes=[AllowAny]
    authentication_classes = (CsrfExemptSessionAuthentication,BasicAuthentication)


    def get_queryset(self):
        queryset=MockAPI.objects.all()
        return MockAPIFilterSet(data=self.request.GET, queryset=queryset).filter()

class MockApiView(generics.RetrieveUpdateDestroyAPIView):
    """
    /api/env/mock/api/id
    id: api id
    """
    serializer_class = mock_serializer.MockAPISerializer
    permission_classes=[AllowAny]
    authentication_classes = (CsrfExemptSessionAuthentication,BasicAuthentication)

    def get_object(self):
        api_id =int(self.kwargs['id'])
        return MockAPI.objects.get(api_id)
    

    