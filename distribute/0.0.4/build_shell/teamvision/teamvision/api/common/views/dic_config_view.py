#coding=utf-8
# coding=utf-8
'''
Created on 2014-1-5

@author: zhangtiande
'''

from teamvision.home.models import Agent,DicData,DicType
from rest_framework import generics
from teamvision.api.common.serializer import dic_config_serializer
from rest_framework.permissions import AllowAny
from rest_framework.authentication import SessionAuthentication, BasicAuthentication

class DicConfigListView(generics.ListAPIView):
    """
    /api/common/dicconfig/type_id/dicconfigs
    """
    serializer_class = dic_config_serializer.DicConfigSerializer
    permission_classes=[AllowAny]
    authentication_classes = (SessionAuthentication,BasicAuthentication)
    
    def get_queryset(self):
        type_id=self.kwargs.get('type_id')
        print(type_id)
        qs =DicData.objects.get_datas_bytype(type_id)
        print(len(qs))
        return qs


class DicConfigView(generics.RetrieveAPIView):
    """
    /api/common/dicconfig/type_id/value
    """
    serializer_class = dic_config_serializer.DicConfigSerializer
    permission_classes=[AllowAny]
    authentication_classes = (SessionAuthentication,BasicAuthentication)
    

    def get_object(self):
        
        type_id=self.kwargs.get('type_id')
        config_value=self.kwargs.get('value')
        qs =DicData.objects.get_data_byvalue(config_value, type_id)
        return qs
    

    