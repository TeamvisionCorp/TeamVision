#coding=utf-8
'''
Created on 2016-10-12

@author: zhangtiande
'''

from rest_framework import serializers
from teamvision.home.models import Team

class TeamSerializer(serializers.ModelSerializer):

    class Meta:
        model = Team
        exclude=('IsActive','CreationTime')
        read_only_fields = ('id',)