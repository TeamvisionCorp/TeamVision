#coding=utf-8
'''
Created on 2016-10-12

@author: Administrator
'''

from rest_framework import serializers
from django.contrib.auth.models import User

class UserSerializer(serializers.ModelSerializer):
    name=serializers.SerializerMethodField()
    class Meta:
        model = User
        exclude=('password','first_name','last_name','is_superuser','groups','user_permissions')
        read_only_fields = ('id',)
        depth=2
    
    def get_name(self, obj):
        return obj.last_name+obj.first_name
        
        
        