#coding=utf-8
'''
Created on 2016-10-12

@author: zhangtiande
'''

from rest_framework import serializers
from teamvision.home.models import DicData,DicType

class DicConfigSerializer(serializers.ModelSerializer):
    class Meta:
        model = DicData
        fields = '__all__'
        read_only_fields = ('id',)

class DicTypeSerializer(serializers.ModelSerializer):
    DicDatas = serializers.SerializerMethodField()

    def get_DicDatas(self,obj):
        result = list()
        dicDatas = DicData.objects.get_datas_bytype(obj.id)
        for dic_data in dicDatas:
            temp_serlizer = DicConfigSerializer(instance=dic_data)
            result.append(temp_serlizer.data)
        return result

    class Meta:
        model = DicType
        fields = '__all__'
        read_only_fields = ('id',)