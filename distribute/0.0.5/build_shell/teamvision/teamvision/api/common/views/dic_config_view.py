#coding=utf-8
# coding=utf-8
'''
Created on 2014-1-5

@author: zhangtiande
'''

from teamvision.home.models import DicData,DicType
from rest_framework import generics,response
from teamvision.api.common.serializer import dic_config_serializer
from teamvision.api.common.filters.dicdata_filter import DicTypeFilterSet
from business.common.system_config_service import SystemConfigService
from rest_framework.permissions import AllowAny
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from teamvision.api.project.views.CsrfExemptSessionAuthentication import CsrfExemptSessionAuthentication

class DicConfigListView(generics.ListAPIView):
    """
    /api/common/dicconfig/type_id/dicconfigs
    """
    serializer_class = dic_config_serializer.DicConfigSerializer
    permission_classes=[AllowAny]
    authentication_classes = (SessionAuthentication,BasicAuthentication)
    
    def get_queryset(self):
        type_id=self.kwargs.get('type_id')
        qs =DicData.objects.get_datas_bytype(type_id)
        return qs


class DicTypeListView(generics.ListAPIView,generics.UpdateAPIView):
    """
    /api/common/dicconfig/all_configs/

    """
    serializer_class = dic_config_serializer.DicTypeSerializer
    permission_classes = [AllowAny]
    authentication_classes = (CsrfExemptSessionAuthentication, BasicAuthentication)

    def get_queryset(self):
        dic_types = DicType.objects.all()
        return DicTypeFilterSet(data=self.request.GET,queryset=dic_types).filter()

    def update(self, request, *args, **kwargs):
        result = list()
        dicdata_list = SystemConfigService.save_dic_datas(request.data)
        for dicdata in dicdata_list:
            temp_serlizer = dic_config_serializer.DicConfigSerializer(instance=dicdata)
            result.append(temp_serlizer.data)
        return response.Response(result)


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
    

    