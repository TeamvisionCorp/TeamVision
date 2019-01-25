#coding=utf-8
'''
Created on 2016-10-12

@author: zhangtiande
'''

from rest_framework import serializers
from django.contrib.auth.models import User,Group
from business.ucenter.account_service import AccountService
from business.auth_user.user_service import UserService

class UserSerializer(serializers.ModelSerializer):
    avatar = serializers.SerializerMethodField()
    system_permision = serializers.SerializerMethodField()

    def get_avatar(self,obj):
        return AccountService.get_avatar_url(obj)

    def get_system_permision(self,obj):
        return UserService.get_system_permission(obj.id)


    class Meta:
        model = User
        exclude = ('password',)
        read_only_fields = ('id',)
        
        
        