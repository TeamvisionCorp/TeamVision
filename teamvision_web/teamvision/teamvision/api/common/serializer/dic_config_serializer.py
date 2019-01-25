#coding=utf-8
'''
Created on 2016-10-12

@author: zhangtiande
'''

from rest_framework import serializers
from teamvision.home.models import DicData

class DicConfigSerializer(serializers.ModelSerializer):
    class Meta:
        model = DicData
        fields = '__all__'
        read_only_fields = ('id',)
        
        
        